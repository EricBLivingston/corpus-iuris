---
description: "Sweeps a completed plan folder for everything it left open into a severity-ranked Implementation-Debrief.md. Takes the plan folder."
argument-hint: "[plan-folder]"
model: sonnet
---

# Debrief Command

Invoke the analyzer agent to consolidate unaddressed items from a completed implementation plan folder into a debrief report.

## Every phase is in scope, always

`Implementation-Debrief.md` is the only artifact that records an assessment; until it exists no phase has been debriefed, whatever other evidence of work the folder contains.

State the full phase range in the dispatch so the analyzer cannot infer a narrower one (∋3).

## Sweep the plan folder into the debrief

### Scan the plan folder

A. Ingest all `.md` files in the plan folder root (excluding `archive/`, which holds the specs `/phase` superseded, and `audit/`, which `/finalize` reads directly) and extract items into the categories the Debrief template defines.

B. For each item, capture source file, the item itself, and severity (critical/important/minor)

### Organize and deduplicate

A. Group findings by category
B. Deduplicate across files
C. Prioritize within each category (critical first)

### Clarify the ambiguous, triage the out-of-scope

A. Identify ambiguous items requiring clarification
B. Triage Out-of-Scope items: bring each in scope or close it with rationale

### Generate the report from the Debrief template

Create `Implementation-Debrief.md` in the plan folder from `{reference-root}/templates/debrief/Debrief-template.md`, its placeholders filled with the extracted findings.
