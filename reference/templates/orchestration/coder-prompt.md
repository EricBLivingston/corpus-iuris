# Coder Dispatch Prompt

The coder agent's dispatch prompt. Consumer: `commands/orchestrate.md` § 3.B and § 3.E.

```text
Implement the changes described in the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Prior findings to address: {Prior Report Path}

{File Rules}

Write an implementation summary to: {Project Path}/Phase-X-Implementation.md
Include: files modified/created, deviations from plan (with justification), and any issues encountered. On a re-dispatch, keep the existing summary and append to it.

Return only a one-line status summary.

After implementing, fill the Deviations section of the phase file: why each was needed, and any state it changed outside the repository.

Remediation, in force when the prior findings are `Phase-X-Adjudication.md`: dispose of every `beyond` finding in this dispatch by contracting the work back inside the remit, by filing one FMEA statement under the `performing-fmea` skill and dispatching the authorizer agent yourself (⊢5), or by escalating it. Contract only what the task can do without; work a Goal or Acceptance Criterion needs goes to a statement, or escalate. Record each disposition under `## Remediation` in `{Project Path}/Phase-X-Implementation.md`. In place of the status summary, return exactly one of these lines:

  REMEDIATED <n> of <n> — <c> contracted, <g> granted: <statement paths>
  ESCALATED <e> of <n> — <c> contracted, <g> granted: <statement paths>
```
