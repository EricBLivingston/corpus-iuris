---
description: "Sweeps a completed plan folder for everything it left open into a severity-ranked Implementation-Debrief.md. Takes the plan folder; use once every phase is complete."
argument-hint: "[plan-folder]"
---

# Debrief Command

Invoke the analyzer agent to consolidate unaddressed items from a completed implementation plan folder into a debrief report.

## Scope

Every phase in the plan folder is in scope, always. `Implementation-Debrief.md` is the only artifact that records an assessment; until it exists no phase has been debriefed, whatever other evidence of work the folder contains.

State the full phase range in the dispatch so the analyzer cannot infer a narrower one (∋3).

## Process

### Scan Plan Folder

A. Ingest all `.md` files in the plan folder root (excluding `archive/`, which holds the specs `/phase` superseded) and extract items into the categories the Debrief template defines.

B. For each item, capture source file, the item itself, and severity (critical/important/minor)

### Organize and Deduplicate

A. Group findings by category
B. Deduplicate across files
C. Prioritize within each category (critical first)

### Questions and Triage

A. Identify ambiguous items requiring clarification
B. Triage Out-of-Scope items: bring each in scope or close it with rationale

### Generate Report

Create `Implementation-Debrief.md` in the plan folder from `{reference-root}/templates/debrief/Debrief-template.md`, its placeholders filled with the extracted findings.

## Output

`Implementation-Debrief.md` in the plan folder
