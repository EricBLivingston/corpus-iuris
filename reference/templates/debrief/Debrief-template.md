# <Plan Name> — Implementation Debrief

<One paragraph: what was implemented, whether it succeeded, and the headline outcome.>

---

## Executive Summary

| Category | Critical | Important | Minor | Total |
| --- | --- | --- | --- | --- |
| Suggestions | | | | |
| Warnings | | | | |
| Out-of-Scope | | | | |
| Technical Debt | | | | |
| Failed/Skipped Tests | | | | |

<Overall assessment: success / partial / blocked. Key takeaways in 1-2 sentences.>

---

## Findings by Category

### Suggestions

- **<S1>** `<source-file>` — <Recommended improvement, enhancement, or alternative.> _(Severity: important)_

### Warnings

- **<W1>** `<source-file>` — <Issue, risk, or concern flagged but not resolved.> _(Severity: critical)_

### Out-of-Scope

- **<O1>** `<source-file>` — <Item explicitly deferred.> → Triage: <bring in scope / close — rationale>

### Technical Debt

Every entry here is a standing violation of §1. Triage each item with a follow-up owner or delete the shortcut; do not let items accumulate.

- **<T1>** `<source-file>` — <Shortcut, workaround, or known compromise.> _(Severity: minor)_

### Failed/Skipped Tests

- **<F1>** `<source-file>` — <Test failing, skipped, or needing future attention — name and reason.> _(Severity: critical)_

---

## Tech Debt Discovered

<OPTIONAL — Use this table when any debt item needs Impact/Follow-up detail beyond the Findings bullet. Otherwise delete and record debt only in Findings > Technical Debt.>

| ID | Source | Item | Impact | Follow-up |
| -- | ------ | ---- | ------ | --------- |
| T1 | `<file>` | <Debt description> | <High/Med/Low> | <Next step> |

---

## Root Causes

<OPTIONAL — Delete if no failures had underlying causes worth tracing beyond symptoms.>

- **<Symptom>** → Root cause: <underlying cause>

---

## Subagent Usage

<OPTIONAL — Delete if no sub-agents were used non-trivially.>

- **<Agent>** for `<task>` — <Warranted? Would direct tools have sufficed?>

---

## Recommended Next Steps

1. <Step 1> — Priority: <high/med/low> — Depends on: <none / step N>
2. <Step 2> — Priority: <high/med/low> — Depends on: <step 1>

---

## Questions and Triage

- **<Q1>** <Ambiguity requiring user decision. Reference finding ID if applicable.>

---

## Appendix — Source Map

| Finding ID | Source File | Line |
| ---------- | ----------- | ---- |
| <S1> | `<path/to/file.md>` | <line or section> |
| <W1> | `<path/to/file.md>` | <line or section> |
