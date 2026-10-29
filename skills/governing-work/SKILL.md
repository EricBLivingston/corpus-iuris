---
name: governing-work
description: "Use this skill when work must be held to its charter: before work begins, to check that its charter is clear and complete enough to hold the work to, and once work is documented (a phase, an unwatched delegate, or any task and its record), to have the governor judge whether the work was necessary to its task."
---

# Governing work

※12 routes ultra vires work here. The governor agent referees scope over executable production source alone, taking the Markdown that documents it at face value; the charter is read from where it already lives and never authored a second time.

## When a dispatch earns its round trip

Per ⊨5. `phase` takes the charter check and `orchestrate` the adjudication after each phase, each at its own step. A session's own work takes none. Other work takes an adjudication when it ran unwatched or its record is larger than the dispatcher will read. A verdict on record is re-asked only after a remediation changed the work or a grant changed the charter.

## Dispatch shapes

Filled with absolute paths.

```text
Adjudicate the documentation below against the charter below: judge whether the documented work was necessary to accomplish the task, and return the verdict.

Charter:
{what defined the work}

Documentation:
{what documents the work done}
```

```text
Check whether the charter below defines the work clearly and completely enough that a later adjudication could tell whether work exceeded it: report each part it cannot hold the work to, and return the verdict.

Charter:
{what defines the work to be done}
```

## Routing the verdict

The last line routes.

| Verdict | Before the work | After the work |
| ---- | ---- | ---- |
| `PASS` | Proceed. | Accept. |
| `FAIL` of the charter check | Its author repairs the charter, then it is checked again (⊨7). | — |
| `FAIL`, any `external` finding | — | Stop for the user. |
| `FAIL`, `beyond` findings only | — | Remediation (below). |
| Malformed | Stop. | Stop for the user. |

The governor returns the verdict and its findings; halting is the dispatcher's call, made here. `phase` and `orchestrate` narrow this table onto their own steps.

## Remediation

`FAIL` returns the adjudication to the party that produced the work, as prior findings. It disposes of every `beyond` finding by contracting the work, filing one statement under `performing-fmea` and dispatching the authorizer itself (⊢5), or escalating. A denial leaves that finding to contract or escalate in the same dispatch. Dispositions are recorded under `## Remediation` in its report, and it returns one line:

```text
REMEDIATED <n> of <n> — <c> contracted, <g> granted: <statement paths>
ESCALATED <e> of <n> — <c> contracted, <g> granted: <statement paths>
```

A grant's amendment is inserted into the charter it amends, and the work is then re-verified and re-adjudicated. Three remediation dispatches cap the cycle (⊨7). A launch stays prospective under `performing-fmea`.
