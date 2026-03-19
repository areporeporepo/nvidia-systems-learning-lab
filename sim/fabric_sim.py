from __future__ import annotations

import argparse
from dataclasses import dataclass
from heapq import heappop, heappush
from math import inf
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Edge:
    target: str
    bandwidth_gbps: float
    latency_ns: float
    label: str


class Fabric:
    def __init__(self) -> None:
        self._adjacency: Dict[str, List[Edge]] = {}

    def add_link(
        self,
        left: str,
        right: str,
        bandwidth_gbps: float,
        latency_ns: float,
        label: str,
    ) -> None:
        self._adjacency.setdefault(left, []).append(
            Edge(right, bandwidth_gbps, latency_ns, label)
        )
        self._adjacency.setdefault(right, []).append(
            Edge(left, bandwidth_gbps, latency_ns, label)
        )

    def neighbors(self, node: str) -> Iterable[Edge]:
        return self._adjacency.get(node, [])

    def nodes(self) -> List[str]:
        return sorted(self._adjacency)


@dataclass(frozen=True)
class Route:
    path: List[str]
    bottleneck_gbps: float
    total_latency_ns: float

    def transfer_time_ms(self, size_gb: float) -> float:
        if self.bottleneck_gbps <= 0:
            raise ValueError("bottleneck bandwidth must be positive")
        return (size_gb / self.bottleneck_gbps) * 1000.0


def widest_path(fabric: Fabric, source: str, target: str) -> Route:
    if source == target:
        return Route(path=[source], bottleneck_gbps=inf, total_latency_ns=0.0)

    best_bw: Dict[str, float] = {source: inf}
    best_latency: Dict[str, float] = {source: 0.0}
    previous: Dict[str, str] = {}
    queue: List[Tuple[float, float, str]] = [(-inf, 0.0, source)]

    while queue:
        neg_bw, latency, node = heappop(queue)
        bandwidth = -neg_bw
        if node == target:
            break
        if bandwidth < best_bw.get(node, 0.0):
            continue
        for edge in fabric.neighbors(node):
            candidate_bw = min(bandwidth, edge.bandwidth_gbps)
            candidate_latency = latency + edge.latency_ns
            known_bw = best_bw.get(edge.target, 0.0)
            known_latency = best_latency.get(edge.target, inf)
            is_better = candidate_bw > known_bw or (
                candidate_bw == known_bw and candidate_latency < known_latency
            )
            if is_better:
                best_bw[edge.target] = candidate_bw
                best_latency[edge.target] = candidate_latency
                previous[edge.target] = node
                heappush(queue, (-candidate_bw, candidate_latency, edge.target))

    if target not in best_bw:
        raise ValueError(f"no route from {source} to {target}")

    path = [target]
    while path[-1] != source:
        path.append(previous[path[-1]])
    path.reverse()
    return Route(
        path=path,
        bottleneck_gbps=best_bw[target],
        total_latency_ns=best_latency[target],
    )


def preset_workstation_pcie() -> Fabric:
    fabric = Fabric()
    for gpu in range(4):
        fabric.add_link("CPU", f"GPU{gpu}", bandwidth_gbps=64.0, latency_ns=250.0, label="PCIe")
    return fabric


def preset_dual_gpu_nvlink() -> Fabric:
    fabric = Fabric()
    fabric.add_link("CPU", "GPU0", bandwidth_gbps=64.0, latency_ns=250.0, label="PCIe")
    fabric.add_link("CPU", "GPU1", bandwidth_gbps=64.0, latency_ns=250.0, label="PCIe")
    fabric.add_link("GPU0", "GPU1", bandwidth_gbps=200.0, latency_ns=50.0, label="NVLink")
    return fabric


def preset_nvswitch_box() -> Fabric:
    fabric = Fabric()
    for gpu in range(8):
        fabric.add_link(
            f"GPU{gpu}",
            "SW0",
            bandwidth_gbps=300.0,
            latency_ns=80.0,
            label="NVSwitch-port",
        )
    fabric.add_link("CPU", "SW0", bandwidth_gbps=64.0, latency_ns=300.0, label="Host-control")
    return fabric


def preset_scale_out_cluster() -> Fabric:
    fabric = Fabric()
    for node in range(2):
        switch = f"SW{node}"
        nic = f"NIC{node}"
        cpu = f"CPU{node}"
        fabric.add_link(cpu, nic, bandwidth_gbps=128.0, latency_ns=300.0, label="CPU-NIC")
        fabric.add_link(cpu, switch, bandwidth_gbps=64.0, latency_ns=250.0, label="PCIe")
        for gpu in range(4):
            fabric.add_link(
                f"N{node}GPU{gpu}",
                switch,
                bandwidth_gbps=300.0,
                latency_ns=80.0,
                label="NVSwitch-port",
            )
    fabric.add_link("NIC0", "NIC1", bandwidth_gbps=100.0, latency_ns=900.0, label="Scale-out")
    return fabric


PRESETS = {
    "workstation_pcie": preset_workstation_pcie,
    "dual_gpu_nvlink": preset_dual_gpu_nvlink,
    "nvswitch_box": preset_nvswitch_box,
    "scale_out_cluster": preset_scale_out_cluster,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Conceptual fabric simulator for learning topology, bottlenecks, and hop count. "
            "This is educational and not a product-accurate NVIDIA hardware model."
        )
    )
    parser.add_argument("--preset", choices=sorted(PRESETS), default="workstation_pcie")
    parser.add_argument("--source", default="GPU0")
    parser.add_argument("--target", default="GPU1")
    parser.add_argument("--size-gb", type=float, default=8.0)
    parser.add_argument("--list-nodes", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    fabric = PRESETS[args.preset]()

    if args.list_nodes:
        print("\n".join(fabric.nodes()))
        return 0

    route = widest_path(fabric, args.source, args.target)
    print(f"preset: {args.preset}")
    print(f"path: {' -> '.join(route.path)}")
    print(f"bottleneck_gbps: {route.bottleneck_gbps:.1f}")
    print(f"total_latency_ns: {route.total_latency_ns:.1f}")
    print(f"transfer_size_gb: {args.size_gb:.1f}")
    if route.bottleneck_gbps == inf:
        print("estimated_transfer_ms: 0.0")
    else:
        print(f"estimated_transfer_ms: {route.transfer_time_ms(args.size_gb):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
