---
name: governing-work
description: Use this skill when scoping work — a plan phase, a delegate's charter, any actions not explicitly requested by the user — and again when that work returns and must be held to its bounds. Carries the bound-authoring form, the test for when the assay earns a dispatch, the governor dispatch shape, and the routing on its return, including the door by which a bound is amended rather than broken.
---

# Governing Work

Bounds bind work. Authoring them is the scoping party's responsibility and is required; testing produced work against them is the governor agent's, dispatched only when it earns the round trip, per ⊨5.

## Written before the work

A bound is a limit on produced content, decidable by a reader holding only the content and the bound. Not a goal, not a quality bar, not an instruction to the producer.

Where the set lives — the first that applies:

- **Plan-governed work** — the `## Governance Bounds` section of an Overview, phase, or other plan file.
- **A dispatched delegate** — its dispatch prompt, which is its own ask and its own bound (⊢5).
- **Otherwise** — a stated block in the session, fixed before the first edit.

Fixed *before* is critical: a bound written afterward certifies whatever happened.

Write each by defining shape, never by enumerated vocabulary; where no shape-wise assay exists, the bound names what it excludes (⊨4, §17).

| Bound | Not a bound |
| ---- | ---- |
| No file outside `skills/governing-work/` is modified | Keep the change focused |
| No provision is minted, amended, or renumbered | Follow doctrine |
| `SKILL.md` stays under §P4's on-demand ceiling | Keep it short |
| No `agents/` body is edited | Be careful with the agents |

## When the assay earns a dispatch

The artifact is cheap; the dispatch is not (⊨5). Dispatch the governor when any holds:

- The work ran unwatched — an orchestrated phase, a background chain, a delegate whose output you did not follow.
- The produced content is larger than the dispatcher will actually read.
- The bounds are numerous, or turn on shape a skim will not settle.
- A gate in the governing plan calls for it.

Otherwise hold the work to the bounds yourself. Never skip the *writing* on this ground — the assay is what scales, not the artifact.

**A bound set already adjudicated is not re-dispatched**, however it was adjudicated. A verdict on record is evidence, not a question to re-ask; only an amendment granted after that verdict earns a re-assay. Dispatching again over content already dispositioned reopens a call that was the dispatcher's alone.

## Dispatch to governor agent

```text
Test the produced content below against the bounds below, and report per bound whether that bound was crossed.

Bounds:
{the enumerated set, inline or by absolute path}

Content:
{absolute paths to the produced material}
```

Hand it the set as it stands at that moment — the original bounds plus every amendment granted since (※12). It opens no evidence channel beyond what you hand it, so an amendment you did not include does not exist, and neither does a bound you forgot.

## Routing the return

Read the summary line only.

| Return | Disposition |
| ---- | ---- |
| `CLEAR` | Proceed. |
| `STOP` — crossed, and the work overran | Cut the work back inside the bound; re-assay. |
| `STOP` — crossed, and the bound was wrong | Amend it (below); re-assay against the amended set. |
| `STOP` — undetermined | Supply what the evidence column names as absent; re-assay. |

A second `STOP` surfacing shapes the first did not means the set holds more of those shapes than one assay samples: sweep every bound against every shape surfaced so far, author-side, before re-dispatching.

Which disposition applies is the dispatcher's call alone. The governor reports whether a bound was crossed, never whether crossing it was acceptable — read no preference into its evidence column, and never ask it for one.

## Amending a bound

A bound that proves wrong is widened through ※12, never crossed. The grant's Cost bound *is* the amended bound, already in the form the governor consumes: add it to the set and re-assay. A denial leaves the original standing — cut the work back or escalate to the user, never past the Authorizing Official.

**Unattended runs do not amend.** Where no human is watching, a `STOP` is terminal and surfaces to the user with the return carried verbatim. The AO is a subagent of the same run, and a run that can widen its own bounds has none.
