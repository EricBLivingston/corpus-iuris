# Analyzer Dispatch Prompt

The analyzer agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 3.A.

```text
Analyze the codebase to understand the scope and impact of the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md

{File Rules}

Write your analysis to: {Project Path}/Phase-X-Analysis.md
Include: affected files, dependencies, risks, and recommended implementation approach.

Return only a one-line status summary. Do NOT return the full analysis content.
```
