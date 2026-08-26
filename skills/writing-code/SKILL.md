---
name: writing-code
description: Runs the implementation cycle over a change — the analyzer agent scopes it, the coder agent writes it, the reviewer reviews it, the tester verifies it, iterating until review passes and tests are green. Use for any feature, bug fix, or refactor, and always once a change spans two or more files.
---

# Writing Code Skill

## Workflow

Four agents, four steps, always in this order (※8):

1. **Analyze** — the analyzer agent establishes scope: affected files, dependencies, risks, recommended approach. Understanding that spans 2+ files, refactor and migration planning, duplication hunts, and anything phrased "across the codebase" or "all files" all land here.
2. **Implement** — the coder agent makes the changes, delegating mechanical bulk edits itself (see `{reference-root}/delegation-workflow.md`).
3. **Review** — the reviewer agent.
4. **Test** — only after review passes, the tester agent.

Steps 2 and 3 are a loop: re-invoke the coder on the review's findings and re-review, until review passes. A test failure re-enters at step 2, and the loop runs again before the tester does.

- The reviewer's verdict is an input the tester should have, so the two never run in parallel.
- Each step's output forwards to the next: analysis to the coder, implementation summary to the reviewer, review to the tester.
- A one-line fix in a single file needs no delegation and does not enter this chain.
- Bounds over the work, and the assay for whether they earn a dispatch, are `governing-work`'s.

### Transition Artifacts

Results pass in-context between steps by default — each agent's returned summary is the next one's input, and the cycle writes no files of its own. A caller may override that with file-based transition artifacts, naming the exact output path in every dispatch and asking each agent to return a one-line status in place of its content. The chain is identical either way; only where a step's output lands changes.

### Output Context Forwarding

When the user or command provides output constraints (project path, naming conventions, file location rules, forbidden paths), you MUST include these verbatim in every agent prompt. Output constraints go near the top of the prompt, before task-specific instructions.

Example: If the user says "all files in plans/metrics-refactor/ using Phase-X-{Subject}.md naming", every agent prompt must include: "Place your output in plans/metrics-refactor/ using the naming convention Phase-X-{Subject}.md. Do NOT use {analysis-root} or any other default location."

## Coding Standards

Language-specific standards live under `{reference-root}/standards/` — `python/principles.md`, `rust/principles.md`. The coder agent reads the one matching the change's language.
