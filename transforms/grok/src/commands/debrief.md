---
description: Sweeps a completed plan folder for what it left open — suggestions, warnings, deferred items, technical debt, failing or skipped tests — into a severity-ranked Implementation-Debrief.md. Takes the plan folder; use once every phase is complete.
argument-hint: "[plan-folder]"
---

# Debrief Command

Invoke the analyzer agent to consolidate unaddressed items from a completed implementation plan folder into a debrief report.

## Scope

**Every phase in the plan folder is in scope, always.** Nothing marks a phase as already-assessed — including, but not limited to, a git commit, a green test report, a passing review, or an audit in an earlier session. `Implementation-Debrief.md` is the only artifact that records an assessment; until it exists no phase has been debriefed.

State the full phase range explicitly in the dispatch so the analyzer cannot infer a narrower one.

## Process

### Scan Plan Folder

A. Ingest all `.md` files in the plan folder root — not `archive/`, which holds the specs `/phase` superseded — and extract items into the categories the Debrief template defines.

B. For each item, capture source file, the item itself, and severity (critical/important/minor)

### Organize and Deduplicate

A. Group findings by category
B. Deduplicate across files
C. Prioritize within each category (critical first)

### Questions and Triage

A. Identify ambiguous items requiring clarification
B. Triage Out-of-Scope items — either bring in scope or close with rationale

### Generate Report

Create `Implementation-Debrief.md` in the plan folder:

Use the structure in `{reference-root}/templates/debrief/Debrief-template.md`. Fill placeholders with extracted findings.

## Output

`Implementation-Debrief.md` in the plan folder
