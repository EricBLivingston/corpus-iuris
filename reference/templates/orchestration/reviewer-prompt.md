# Reviewer Dispatch Prompt

The reviewer agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 3.C.

```text
Review the implementation for the following phase against the plan and analysis.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Implementation summary: {Project Path}/Phase-X-Implementation-Report.md
Prior findings to address: {Prior Report Path}

{File Rules}

Write your review to: {Project Path}/Phase-X-Review.md
Include: issues found (critical/important/minor), whether implementation matches the plan, and suggested fixes.

**Scope audit (mandatory before verdict).** Establish that every file this phase touched outside the run's records and {Project Path}/audit/ is in the plan's scope or a filed Deviation. Anything else fails the phase — the plan was incomplete, or the coder departed scope. An accepted Deviation re-engages the analyzer for related collateral.

Verify Deviations was filled. Verify ACs have verifier hints. Run a Reverse Dependency Audit if the phase changed any struct, enum, or public-API surface.

Return only a one-line status summary indicating pass/fail and issue count.
```
