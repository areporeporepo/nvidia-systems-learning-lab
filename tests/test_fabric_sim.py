from math import isinf

from sim.fabric_sim import PRESETS, widest_path


def test_dual_gpu_nvlink_prefers_direct_path() -> None:
    route = widest_path(PRESETS["dual_gpu_nvlink"](), "GPU0", "GPU1")
    assert route.path == ["GPU0", "GPU1"]
    assert route.bottleneck_gbps == 200.0
    assert route.total_latency_ns == 50.0


def test_pcie_route_uses_host() -> None:
    route = widest_path(PRESETS["workstation_pcie"](), "GPU0", "GPU1")
    assert route.path == ["GPU0", "CPU", "GPU1"]
    assert route.bottleneck_gbps == 64.0
    assert route.total_latency_ns == 500.0


def test_nvswitch_box_routes_through_switch() -> None:
    route = widest_path(PRESETS["nvswitch_box"](), "GPU0", "GPU7")
    assert route.path == ["GPU0", "SW0", "GPU7"]
    assert route.bottleneck_gbps == 300.0
    assert route.total_latency_ns == 160.0


def test_same_source_target_is_trivial_route() -> None:
    route = widest_path(PRESETS["scale_out_cluster"](), "N0GPU0", "N0GPU0")
    assert route.path == ["N0GPU0"]
    assert isinf(route.bottleneck_gbps)
    assert route.total_latency_ns == 0.0
