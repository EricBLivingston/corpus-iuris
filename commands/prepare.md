---
description: Authors the next Spec-Driven Development artifact — PRD, then Design, then Implementation — by exploring the codebase, reading the precursors already in the plan folder, and filling that artifact's template. Takes the target path, whose filename selects the branch; writes that artifact, plus a Background.md beside it on the PRD branch. Changes no code.
argument-hint: "[plans/<name>/PRD.md|Design.md|Implementation.md]"
model: fable
---

# Prepare Command

`/prepare` authors the next artifact in the Spec-Driven Development pipeline — **PRD → Design → Implementation** — the specs downstream execution builds from. Explore the codebase, fill the matching template, write nothing but that artifact.

## Target Artifact

The argument is the **target artifact's path** — e.g. `/prepare plans/<name>/Design.md`. Two things are read from it: its **directory** is the plan folder (where this artifact lands and where any precursors already live), and its **filename** selects the branch + template below. Point the exploring agent directly at the template in `{reference-root}/templates/plan/`; do not restate its structure here.

| Target basename | Template | Precursors (read from the plan folder) | Next step |
| ---- | ---- | ---- | ---- |
| `PRD.md` | `PRD-template.md` | the user's request | route to Design or Implementation (rubric below), recorded in PRD §6 |
| `Design.md` | `Design-template.md` | the sibling `PRD.md` | always → Implementation |
| `Implementation.md` | `Implementation-template.md` | the sibling `PRD.md`, plus `Design.md` if present (short-circuit: PRD only) | terminal → `/implement` or `/orchestrate` |

## The Regimes

An artifact's boundary is the swap that would rewrite it.

| Artifact | Regime | Rewritten by |
| ---- | ---- | ---- |
| `Background.md` | the ground — why there is a plan at all | — |
| `PRD.md` | Why (Need) | a different problem: web UI → headless LLM tool |
| `Design.md` | What (Solution) | a different conceptual approach: local stateless CLI → cloud stateful server |
| `Implementation.md` | How (Tools & Tech) | a different technology stack: Postgres/Rust → SQLite/Python |

Rows above the rewritten one stand. Each regime keeps its own deliberation and passes on only its result: why we need this at all stays in the PRD, why this design and not another stays in Design. Justification is a context sink — compartmentalizing it is what keeps each artifact focused on its own job.

## Workflow (identical for every target)

1. **Clarify** (if needed) — use AskUserQuestion for ambiguous requests.

2. **Document** — When authoring PRD.md, create `Background.md` in the plan folder summarizing the problem, goals, and the precursors' relevant content. The agent does NOT inherit main context; everything it needs goes in `Background.md` or its prompt (which references `Background.md`). Documentation for Design/Implementation.md comprises the created upstream artifacts and Background.md; no new Background.md is needed.

3. **Delegate** — DO NOT analyze yourself. Invoke the analyzer agent against the target template, instructing it to fill that template and — PRD only — populate `## 6. Next Step` per the rubric.

4. **Present** — what the artifact settled, the next-step call, and a one-line rationale for it. Nothing the artifact already says.

## Routing Rubric (PRD branch only): Design.md vs Implementation.md

The exploring agent makes the call based on what it observed in the codebase:

> Are the requirements scoped such that the existing codebase can clearly accommodate the work, or do they warrant additional design work first?

- **→ `Implementation.md`**: the path is clear from the codebase — the work fits established architecture, patterns, and boundaries. No new components, boundaries, or data shapes are required.
- **→ `Design.md`**: the requirements introduce something the codebase does not yet accommodate — new components, boundaries, data shapes, patterns, or unresolved trade-offs to settle first.

When in doubt, prefer Design — an unneeded Design.md is cheap; starting Implementation against an unsettled architecture is not.

Now resolve the target artifact and begin planning.
