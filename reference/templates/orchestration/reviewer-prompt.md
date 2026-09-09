# Reviewer Dispatch Prompt

The reviewer agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 4.C.

```text
Review the implementation for the following phase against the plan and analysis.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Implementation summary: {Project Path}/Phase-X-Implementation.md
Baseline commit (orchestrate run kickoff): {Baseline Commit}
Prior findings to address: {Prior Report Path}

{File Rules}

Write your review to: {Project Path}/Phase-X-Review.md
Include: issues found (critical/important/minor), whether implementation matches the plan, and suggested fixes.

**Scope audit (mandatory before verdict).** Establish that every file touched since {Baseline Commit} is in the plan's scope or a filed Deviation. Anything else fails the phase — the plan was incomplete, or the coder departed scope. A Deviation crossing a bound in ## Governance Bounds with no ATO recorded is ultra vires (※12): obtain the ATO yourself (⊢5) and report the statement's path. An accepted Deviation re-engages the analyzer for related collateral.

Verify Deviations was filled. Verify ACs have verifier hints. Run a Reverse Dependency Audit if the phase changed any struct, enum, or public-API surface.

Return only a one-line status summary indicating pass/fail and issue count.
```
