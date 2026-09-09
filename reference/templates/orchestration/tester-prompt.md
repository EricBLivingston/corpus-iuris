# Tester Dispatch Prompt

The tester agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 4.D.

```text
Write and run tests to verify the implementation for the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Implementation summary: {Project Path}/Phase-X-Implementation.md
Review: {Project Path}/Phase-X-Review.md

{File Rules}

Write a test report to: {Project Path}/Phase-X-Test-Report.md
Include: tests run, pass/fail counts, coverage if available, and any failures with details.

Your verification includes the §16 cross-boundary end-to-end gate wherever the phase's work crosses a boundary.

Return only a one-line status summary indicating pass/fail and test counts.
```
