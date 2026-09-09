# Coder Dispatch Prompt

The coder agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 4.B.

```text
Implement the changes described in the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Prior findings to address: {Prior Report Path}

{File Rules}

Write an implementation summary to: {Project Path}/Phase-X-Implementation.md
Include: files modified/created, deviations from plan (with justification), and any issues encountered.

After implementing, fill the Deviations section of the phase file before invoking the reviewer. A departure that would cross a bound in ## Governance Bounds is ultra vires (※12), not a Deviation: obtain the ATO before the edit and report the statement's path.

Return only a one-line status summary.
```
