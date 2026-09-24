---
description: "Converts a plan's debrief into a close-out plan: every carried item takes a binary Yes or No, and the Yes list becomes an Implementation.md ready to re-phase. Takes the plan folder containing Implementation-Debrief.md; use when loose ends must be closed rather than carried forward."
argument-hint: "[plan-folder]"
model: opus
---

# Finalize Command

Convert an `/orchestrate` debrief into a binary-triage close-out plan. Workflow position: `orchestrate → finalize → (manual review) → phase → orchestrate (close-out)`.

## Arguments

`$ARGUMENTS` = the plan folder containing `Implementation-Debrief.md` (the path `/debrief` and `/phase` take).

Set `{Project Path}` = the output of `pwd` prepended to `plans/{Plan Folder}/`. It must begin with `/`: the analyzer may run in a different cwd, where a relative `plans/...` silently lands outside the project. It must NOT resolve inside your agent-configuration directory (the tree containing your rules, agents and commands) unless the plan being finalized lives in that meta-project.

## Critical Directives

**Finality.** The `Implementation.md` this command produces is the final reference to the parent plan's loose ends. After it executes and is archived, every debrief item is closed, so each takes a binary Yes or No with no tri-state escape (Step 4 greps for its recurring wordings). A "No" is a closure stating its rationale: if the item still matters, a future implementation's own analyzer rediscovers it from the live codebase, and if it is never rediscovered it was not material.

**Upstream artifacts are immutable.** Everything in `{Project Path}/` outside `debrief/` (e.g., `Overview.md`, `Phase-*.md`, analyses, reviews, test reports) is a historical record, errors and stale claims included: future forensic research depends on those files remaining exactly as the implementation left them. The only writes `/finalize` and its delegated analyzer may make are new files inside `{Project Path}/debrief/`. The sole exception is Step 2's staging move. The payload below binds the produced plan's *contents* by the same rule.

## Workflow

### 1. Validate Inputs

A. Confirm `{Project Path}/Implementation-Debrief.md` exists. If absent, abort with: "No Implementation-Debrief.md in {Project Path} — run /orchestrate first."
B. Confirm `{Project Path}/debrief/` does NOT already exist. If it does, abort with: "{Project Path}/debrief/ already exists — finalize has already been run. Remove it or pick a different plan."
C. Report the resolved `{Project Path}` to the user before continuing.

### 2. Stage the Debrief

One Bash command creates the subfolder and moves the debrief into it under its new name:

```
mkdir -p {Project Path}/debrief && mv {Project Path}/Implementation-Debrief.md {Project Path}/debrief/Debrief.md
```

### 3. Generate the Close-Out Implementation Plan

Invoke the analyzer agent with the prompt below (∋3), passing the absolute `{Project Path}` verbatim. It writes the file and returns one line; wait for that line, and do not read `debrief/Debrief.md`, `debrief/Implementation.md` or any phase artifact yourself.

```
Produce a close-out Implementation.md from the debrief at:
{Project Path}/debrief/Debrief.md

Write the plan to:
{Project Path}/debrief/Implementation.md

You may read any file in {Project Path}/ for context (Overview.md, phase files, analyses, reviews, test reports). Do NOT read anything outside {Project Path}/.

## Immutability Constraint — Read Before Drafting

The upstream plan artifacts (Overview.md, Phase-*.md, analyses, reviews, test reports, and every other file in {Project Path}/ outside debrief/) are immutable historical records. You MUST NOT modify, rename, reformat, lint-clean or delete any of them, even where you notice errors, stale claims or inconsistencies: the implementation that produced them has been archived, and future forensic research depends on them as it left them. Your ONLY permitted write is this run's new file, {Project Path}/debrief/Implementation.md.

The rule binds the Implementation.md you produce as much as your direct file operations. A defect you spot in an upstream artifact does NOT become a Yes-list work item, an acceptance criterion or a verification step; it goes on the No-list with rationale `No: upstream plan artifact, immutable historical record`. A Yes-list entry that edits an upstream artifact when executed is the same prohibited modification, postponed by one hop. If the issue still matters, the future implementation's own analyzer rediscovers it from the live codebase; that rediscovery is the closure mechanism.

## Closure Constraint — Read Before Drafting

This Implementation.md is the last reference to the debrief's loose ends. After it executes and is archived, every debrief item is closed; an item resurfaces only through a future implementation's own investigation, never by re-reading this plan.

Triage rules:

1. **Binary verdict: Yes or No.** Every finding takes exactly one label. Any wording that defers, conditions, re-queues or watch-lists an item instead of closing it is a forbidden third bucket, whatever word it wears.
2. **Every debrief finding takes a verdict.** Every item in {Project Path}/debrief/Debrief.md must appear with a Yes or No under its original finding ID, so the mapping is auditable.
3. **The No-list is the closure.** A "No" is a deliberate close-out with a one-line rationale; once the rationale is written, the item is closed.

Triage heuristics:

- **Yes** when the item is a real defect, a cheap fix, blocks dependent work, or has a clear verifier hint and concrete file/line target.
- **No** when the item is speculative coverage, style-only preference, environment-driven, documented-as-accepted in a Deviations section, subsumed by another Yes item, or would require unbounded scope expansion (entire-project sweeps, multi-phase refactors).
- When uncertain, prefer No with explicit rationale: this plan's value is finality, and a padded Yes-list inflates scope.

## Required Structure for Implementation.md

Follow this exact section ordering:

### 1. Scope and Outcome Tally

A table counting Yes / No / Total per debrief category, plus a 1-3 sentence summary of the themes driving the Yes-list and the dominant rationale categories on the No-list.

### 2. Yes-List — Ordered Work Items

Group by work-class, adjusted to the actual content: production defects first, then tech-debt closure that unlocks other work, then test quality, then ※10 sweeps in live source. No work-class reconciles plan documents or fixes upstream artifacts; the immutability constraint puts those items on the No-list. Each item contains:

- Anchor: original finding ID(s) from Debrief.md (e.g., "Y-1. W1 — ...")
- File path with line anchors where known
- Concrete change summary (what to do, not just what is wrong)
- Verifier hint (a runnable command, grep pattern, or visual diff target)

### 3. No-List — Drops with One-Line Rationale

Group by debrief category. Each entry is one bullet: the finding ID, a one-sentence summary, and a one-clause rationale beginning with "No:". Acceptable shapes: "No: coverage-only, behavior verified empirically", "No: style preference; current form is mypy-clean", "No: by-design environment guard", "No: upstream plan artifact, immutable historical record". A rationale using tri-state vocabulary is forbidden.

### 4. Acceptance Criteria

A numbered list of pass/fail conditions for the close-out plan as a whole (e.g., full test suite green, specific verifier commands return expected output). ACs target only live source artifacts (production code, tests, configs), never the state of an upstream plan document, and cover only the Yes-list: the No-list is already closed.

### 5. Verification Commands

A code block listing the runnable commands a reviewer would execute end-to-end to confirm closure, grouped by work-class to match Section 2.

## Output

Return only a one-line status summary: "Yes: N / No: M / Total: T → {Project Path}/debrief/Implementation.md".
```

### 4. Verdict-Language Check

The payload forbids tri-state language; check the draft for it before handing back. The pattern below matches only the recurring wordings, and a novel one escapes it, so a clean grep is evidence of a binary draft (⊨4):

```
grep -niE '\b(deferred|defer to|tbd|revisit|maybe|conditional|track separately|follow up in|future plan|future work|watchlist|if touched|if revisited)\b' {Project Path}/debrief/Implementation.md
```

On any hit, re-invoke the analyzer with: "The previous draft contains forbidden tri-state language at these lines: <paste grep output>. Rewrite affected entries as binary Yes/No with concrete rationale, then overwrite the file." Repeat up to twice; on a third failure, surface the offending lines to the user and stop. On zero hits, proceed.

### 5. Final Summary

Report the resolved `{Project Path}`, the analyzer's one-line status (Yes / No / Total), the location of `debrief/Debrief.md` and `debrief/Implementation.md`, and the next step: "Review and refactor `{Project Path}/debrief/Implementation.md`, then run `/phase debrief` (or equivalent) to break it into executable phases."

Do NOT continue into `/phase` or `/orchestrate` automatically: the user re-enters the workflow at this seam to refine the close-out plan before phasing.

## Output

- `{Project Path}/debrief/Debrief.md` — the parent `Implementation-Debrief.md`, relocated under its new name
- `{Project Path}/debrief/Implementation.md` — binary-triage close-out plan
