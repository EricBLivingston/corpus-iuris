# Repository Guide

This repository is source material for Corpus Iuris and its harness transforms. Cloning or reading
it does not install or admit any provision into the reader's agent configuration.

## Codex adoption

When the user asks to adopt or configure this corpus for Codex:

1. Read `README.md` and `adopting.md` for the corpus model, then `transforms/codex/README.md`, which carries the adoption sequence end to end; `transforms/codex/AGENTS.md` governs the work itself.
2. Inspect the live Codex configuration read-only, report the proposed changes and conflicts, and obtain explicit user authorization before writing outside this clone.
3. If authorized, make the inert SessionStart loader the first installation change, and write the installation's instance file from `transforms/codex/src/instance-example.md` before admitting anything. Admit no artifact through `canon.md` until the user selects it.

For other work, follow the user's requested scope. Guidance in a nested `AGENTS.md` governs its own
subtree and supplements this repository-level routing.
