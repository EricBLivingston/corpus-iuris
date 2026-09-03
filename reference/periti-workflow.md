# Periti Workflow

The orchestration protocol shared by every peritus. CLI-agnostic on purpose: nothing here names a flag, a binary, or a settings key. Each peritus's own skill carries the shape to copy and what that shape's elements mean (⊢2).

## Run in the foreground

Never background an engagement. Where a harness wakes only its main session when a backgrounded job finishes, a subagent that backgrounds a task **exits** and never sees the result — while the orphaned run completes anyway, writing its document after the agent has already reported back as though nothing happened. The failure mode is a silently incomplete report, not lost work.

The asymmetry is the whole rule, and it is why the prohibition reads as absolute but is really subagent-scoped: **the main session is re-invoked** when a backgrounded job finishes, so it alone can background one safely. Two neighbouring rules follow from the same fact rather than contradicting it.

Push notification is for the *user*, who is waiting on a long foreground run and would otherwise poll; it is not a mechanism for an agent to learn its own engagement finished. And ※3's "do not poll" is about **not** re-checking or re-spawning after an async agent invocation — a foreground engagement never reaches that state, because the tool call does not return until the run is over.

## Split at the ceiling

Work that will not fit one call is split into several prompts, each self-contained. The bound is the harness tool timeout, with the peritus's own internal limit binding first where it has one; both are in the shape being copied. Raising them is not an option, so splitting is the only move — and a split is cheaper than a truncated answer, which arrives looking complete.

## Verify before relaying

Never pass on a peritus's claim that it wrote, changed, or found something without looking. *Nullius in verba*: several return success on a refusal.

- **A document engagement** is verified by the file existing and being non-empty, then read.
- **An edit engagement** is verified by the diff over the enumerated file set, taken before and after. No diff means no edit, whatever the summary says.
- **Any engagement** is verified against the working tree for changes nobody asked for. A run that was not asked to edit and did is a failure, not a bonus — check the tree state before and after whenever a peritus has any write capability at all.

## Hand back the peritus's own output

Relay what the peritus actually said, plus what was verified, and say so explicitly when an engagement returned nothing. A summary of a summary loses the thing the engagement was spent on, and silence about an empty return reads as a finding of "nothing to report".

## Second opinions are advisory

Produce the primary deliverable first, fold the review in if it returns, and never block, defer, or condition the deliverable on the engagement. If the run times out or comes back empty, ship the deliverable and note that the review was unavailable.

## Chained engagements

**State lives on disk between links**: run N writes its findings to a file, run N+1 reads that file. Each link gets its own foreground budget, and each intermediate file is checked non-empty before the next call is spent on it — a chain that carries an empty file forward spends every remaining link on nothing.
