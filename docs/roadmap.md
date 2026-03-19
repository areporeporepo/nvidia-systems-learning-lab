# Public Roadmap Notes

This page stays deliberately conservative. It only uses public, official NVIDIA material and separates shipping platforms from roadmap-only items.

## Snapshot

| Platform | Public status | What is public |
| --- | --- | --- |
| `Blackwell` | Shipping generation | Architecture page, HGX materials, NVLink material |
| `Rubin` | Publicly announced next generation | HGX Rubin overview, roadmap placement |
| `Vera` | Publicly named CPU on roadmap | Roadmap placement in NVIDIA materials |
| `Feynman` | Roadmap-only future generation | Investor deck roadmap references |

## Blackwell

What is public today:

- NVIDIA describes `Blackwell` as the current production architecture.
- NVIDIA publishes architecture-level information, HGX materials, and NVLink positioning.

Why it matters for learning:

- It is the best public anchor for understanding the current stack shape.
- Most practical learning should start with current tooling that maps to this generation.

## Rubin

What is public today:

- NVIDIA has public `HGX Rubin` material.
- NVIDIA positions `Rubin` after `Blackwell` in its annual roadmap rhythm.
- NVIDIA associates `Rubin` with newer `NVLink` generations and larger system-scale integration.

Why it matters for learning:

- It shows how the stack keeps pushing toward rack-scale design.
- It helps frame why `NVLink`, `NVSwitch`, networking, and software are now discussed as one system.

## Vera

What is public today:

- NVIDIA publicly names `Vera` as the CPU platform paired into later roadmap systems.
- The public detail level is much lighter than for shipping GPU architectures.

Why it matters for learning:

- It reinforces that CPU choice is part of the platform story, not an afterthought.

## Feynman

What is public today:

- `Feynman` appears in official roadmap material for `2028`.
- Public material places it in a future system generation alongside later interconnect and networking components.

What is not public:

- There is no public, detailed `Feynman` architecture brief comparable to current shipping generations.
- There is no public high-fidelity simulator that would let you accurately emulate `Feynman`.

Why it matters for learning:

- It gives you a target mental model for where the stack is going.
- The right preparation is learning current public stacks well enough to understand the direction of travel.

## Read This Page The Right Way

Use `Blackwell` for hands-on work, use `Rubin` and `Vera` for near-future system context, and treat `Feynman` as roadmap context unless NVIDIA releases deeper technical material.

## Official Sources

- Blackwell architecture: https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/
- HGX and Rubin overview: https://www.nvidia.com/en-us/data-center/hgx/
- Multi-Node NVLink Systems docs: https://docs.nvidia.com/multi-node-nvlink-systems/index.html
- Investor roadmap deck: https://investor.nvidia.com/files/doc_presentations/2025/10/NVIDIA-2025-NDR-Deck-1.pdf
