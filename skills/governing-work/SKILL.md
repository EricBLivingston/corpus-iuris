---
name: governing-work
description: "Use this skill when scoping work: to write and validate the bounds work will be held to, and again when the work returns and must be held to them. Carries the bound-authoring form, the two governor dispatches — the set as content before the work, the work as content after — the test for when either earns the round trip, and the routing on each return, which sends a bound that proves wrong to performing-fmea rather than across it."
---

# Governing Work

Bounds bind work. Authoring them is the scoping party's responsibility. The governor agent tests handed content against handed bounds and nothing else, and serves twice on that one contract: before the work, the bound set is the content and the filters are the bounds; after it, the produced work is the content and the set is the bounds. Either dispatch only when it earns the round trip, per ⊨5.

## Written before the work

A bound is a limit on produced content, decidable by a reader holding only the content and the bound. Not a goal, not a quality bar, not an instruction to the producer.

Where the set lives — the first that applies:

- **Plan-governed work** — the `## Governance Bounds` section of an Overview, phase, or other plan file.
- **A dispatched delegate** — its dispatch prompt.
- **Otherwise** — a stated block in the session, fixed before the first edit.

Fixed *before* is critical: a bound written afterward certifies whatever happened.

Write each by defining shape, never by enumerated vocabulary; where no shape-wise assay exists, the bound names what it excludes (⊨4, §17).

| Bound | Not a bound |
| ---- | ---- |
| No file outside `skills/governing-work/` is modified | Keep the change focused |
| No provision is minted, amended, or renumbered | Follow doctrine |
| `SKILL.md` stays under §P4's on-demand ceiling | Keep it short |
| No `agents/` body is edited | Be careful with the agents |

The filters at `{reference-root}/templates/plan/bounds-sources.md § Filters on every row's output` decide whether a candidate is a bound at all. They are written for plan bounds and hold for the other two homes as far as each one's sources reach.

## When the assay earns a dispatch

The artifact is cheap; the dispatch is not (⊨5). Dispatch the governor when any holds:

- The work ran unwatched — an orchestrated phase, a background chain, a delegate whose output you did not follow.
- The produced content is larger than the dispatcher will actually read.
- The bounds are numerous, or turn on shape a skim will not settle.
- A gate in the governing plan calls for it.

Before the work only the last two apply, and a plan folder's sets always go: that is the gate `orchestrate` runs before its first phase. Otherwise hold the work to the bounds yourself, and validate the set yourself, per bound, against the filters. Never skip the *writing* on this ground — the assay is what scales, not the artifact.

**A bound set already adjudicated is not re-dispatched**, however it was adjudicated. A verdict on record is evidence, not a question to re-ask. What earns a re-assay is a change in what is tested: content cut back inside a bound it overran, the evidence an undetermined row named as absent, or a bound replaced by an amendment granted after that verdict. Dispatching again over content already dispositioned, unchanged, reopens a call that was the dispatcher's alone.

## Dispatch to governor agent

One prompt shape, filled two ways.

```text
Test the produced content below against the bounds below, and report per bound whether that bound was crossed.

Bounds:
{the enumerated set, inline or as the numbered bounds of a named section of a file at an absolute path}

Content:
{absolute paths to the produced material}
```

**Before the work**, Bounds is the filters, one bound each, plus — for a plan folder — the two relational criteria `orchestrate` § Validate Boundaries states; Content is the bound set under validation, with the material it was written from — the ask, the plan, the dispatch prompt — read-only, as the evidence its provenance and satisfiability turn on. A governor holding no source passes those filters rather than reporting them untested.

**After the work**, Bounds is the set and Content is what the work produced. Hand it the set as it stands at that moment — each bound in its current text, an amended bound present as its replacement and never beside it (⊨3); a superseded text survives only in whatever records the grant, which is not part of the set. It opens no evidence channel beyond what you hand it, so an amendment you did not include does not exist, and neither does a bound you forgot.

## Routing the return

Read the summary line; on a `STOP`, read the evidence of every row that is not *held* as well. The summary line splits crossed from undetermined but says nothing about which crossing is which, and that is what the overran-versus-wrong call turns on; an undetermined row's evidence column is the only place what was absent is named.

| Return | Disposition |
| ---- | ---- |
| `CLEAR` | Proceed. |
| `STOP` — a crossed row, and the work overran | Cut the work back inside the bound; re-assay. |
| `STOP` — a crossed row, and the bound was wrong | Amend it (below); re-assay against the set as replaced. |
| `STOP` — an undetermined row | Supply what the evidence column names as absent; re-assay. |

A line carrying both counts routes per row, not per line.

Before the work, a crossed row is a bound that failed a filter. It goes back to its author, never repaired by the party it constrains; where you are its author, rewrite it before the first edit and re-test the rewrite against every filter, not only the one it failed (⊨7). That is authoring, not amendment: the door below opens only once the work has begun.

A second `STOP` surfacing shapes the first did not means the set holds more of those shapes than one assay samples: sweep every bound against every shape surfaced so far, author-side, before re-dispatching.

Which disposition applies is the dispatcher's call alone. The governor reports whether a bound was crossed, never whether crossing it was acceptable — read no preference into its evidence column, and never ask it for one.

## Amending a bound

A bound that proves wrong once the work has begun is amended, never crossed. The amendment is ultra vires (※12): state the FMEA through `performing-fmea`, whose § Amending a bound governs the Cost row. The grant's Cost bound *is* the amended bound: it replaces the bound it amends in the set, and the re-assay runs against the set as replaced. A denial leaves the original standing.
