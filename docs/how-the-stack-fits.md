# How The Stack Fits Together

## The Short Version

The modern NVIDIA AI system stack is not just a GPU. It is a coordinated stack across:

- `GPU compute`: tensor cores, memory hierarchy, software kernels
- `CPU`: host orchestration, memory, scheduling, data movement
- `Scale-up fabric`: `NVLink` and `NVSwitch` inside a tightly coupled GPU domain
- `Scale-out network`: `Ethernet` or `InfiniBand` across servers and racks
- `System software`: `CUDA`, `NCCL`, `NVSHMEM`, `DOCA`, profilers, firmware, drivers

## Mental Model

Think in three layers:

1. `Single GPU`
   This is where `CUDA`, kernels, memory bandwidth, occupancy, and tensor core behavior matter most.

2. `Single node or NVLink domain`
   This is where `NVLink`, `NVSwitch`, peer-to-peer copies, and `NCCL` collectives dominate performance.

3. `Multi-node cluster`
   This is where `NICs`, `Ethernet` or `InfiniBand`, congestion, topology mapping, and collective scheduling dominate performance.

## Why NVLink Exists

`PCIe` is useful and general, but tightly coupled multi-GPU systems need much more bandwidth and lower communication overhead. `NVLink` and `NVSwitch` exist to make groups of GPUs behave more like one large accelerated system.

## Where NCCL Fits

`NCCL` is the communication layer many training and inference stacks use for collectives such as:

- `all-reduce`
- `all-gather`
- `reduce-scatter`
- `broadcast`

It chooses communication patterns based on topology. That is why understanding the physical fabric matters.

## Where NVSHMEM Fits

`NVSHMEM` is useful when you want a partitioned global address space and GPU-initiated communication. It is a different learning angle than `NCCL`: less about standard collectives, more about one-sided communication and shared-memory style programming across GPUs.

## Why Blackwell, Rubin, Vera, and Feynman Get Mentioned Together

NVIDIA increasingly talks about the stack as one co-designed system:

- chips
- memory
- interconnect
- rack-scale layout
- networking
- software libraries

That is why roadmap discussions mention `GPU`, `CPU`, `HBM`, `NVLink`, `Spectrum`, `ConnectX`, and software in one breath. The architecture story is no longer only about a chip.
