# First Week Learning Plan

## Goal

Build a practical mental model for how GPU compute, topology, and collectives interact.

## Day 1: CUDA Basics

- Clone `https://github.com/NVIDIA/cuda-samples`
- Build a few basic samples
- Focus on device query, memory copies, and any peer-to-peer sample that matches your hardware

Questions to answer:

- What capabilities does your GPU expose?
- What changes when you move from host-device copies to peer-to-peer copies?

## Day 2: Topology

- Run `nvidia-smi topo -m`
- Save the topology output
- Compare it against the conceptual presets in `sim/fabric_sim.py`

Questions to answer:

- Which GPUs are close to each other?
- Which transfers likely hit a shared switch or CPU root complex?

## Day 3: NCCL Benchmarks

- Clone `https://github.com/NVIDIA/nccl-tests`
- Build `all_reduce_perf`
- Compare results across message sizes

Questions to answer:

- Where does bandwidth flatten out?
- Which sizes expose latency and which sizes expose bandwidth ceilings?

## Day 4: Profiling

- Use `Nsight Systems` if available
- Profile a communication-heavy run

Questions to answer:

- Is communication overlapping with compute?
- Are the slowdowns fabric-bound, launch-bound, or host-bound?

## Day 5: NVSHMEM

- Read the `NVSHMEM` examples
- Identify how its programming model differs from `NCCL`

Questions to answer:

- When would one-sided communication be a better fit than a bulk collective?

## Day 6: Read The Roadmap Again

- Revisit [docs/roadmap.md](../docs/roadmap.md)
- Rewrite the roadmap in your own words after the hands-on work

Questions to answer:

- What part of the roadmap is mostly compute?
- What part is really about memory and interconnect?

## Day 7: Explain It Back

- Write one page answering: "How do CUDA, NVLink, NVSwitch, NCCL, and networking fit together?"
- Add your notes as a markdown file in this repo

That final step matters. If you cannot explain the stack cleanly, you do not own it yet.
