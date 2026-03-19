# Upstream Contribution Ideas

If you want to make real PRs while learning, avoid aiming at the hardest core library first.

## Best First Targets

### `NVIDIA/cuda-samples`

Good starter contributions:

- clarify README instructions
- modernize build notes
- fix stale sample docs
- improve small example comments
- add environment notes for newer toolchains

### `NVIDIA/nccl-tests`

Good starter contributions:

- clearer CLI help
- better result formatting
- benchmark output parsing helpers
- docs around topology interpretation

### `NVIDIA/nvshmem`

Good starter contributions:

- example walkthroughs
- docs cleanup
- minimal example fixes

## Harder Target

### `NVIDIA/nccl`

This is worth studying, but the bar for useful code contributions is higher. Use it more as a reading repo until you have real topology and collectives intuition.

## Good PR Rule

Do not start by changing the deepest performance-critical kernel path. Start by making the repo easier to learn, build, run, or validate.
