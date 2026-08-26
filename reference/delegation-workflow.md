# Delegation Workflow

The orchestration protocol shared by every delegate. CLI-agnostic on purpose: nothing here names a flag, a binary, or a settings key. Each delegate's own always-loaded rule file carries the shape to copy, and its skill carries what that shape's elements mean.

## Run in the foreground

Never background a delegation. Where a harness wakes only its main session when a backgrounded job finishes, a subagent that backgrounds a task **exits** and never sees the result — while the orphaned run completes anyway, writing its document after the agent has already reported back as though nothing happened. The failure mode is a silently incomplete report, not lost work.

The asymmetry is the whole rule, and it is why the prohibition reads as absolute but is really subagent-scoped: **the main session is re-invoked** when a backgrounded job finishes, so it alone can background one safely. Two neighbouring rules follow from the same fact rather than contradicting it.
Push notification is for the *user*, who is waiting on a long foreground run and would otherwise poll; it is not a mechanism for an agent to learn its own delegation finished. And ※3's "do not poll" is about **not** re-checking or re-spawning after an async agent invocation — a foreground delegation never reaches that state, because the tool call does not return until the run is over.

## Split at the ceiling

Work that will not fit one call is split into several prompts, each self-contained. The bound is the harness tool timeout, with the delegate's own internal limit binding first where it has one; both are in the shape being copied. Raising them is not an option, so splitting is the only move — and a split is cheaper than a truncated answer, which arrives looking complete.

## Verify before relaying

Never pass on a delegate's claim that it wrote, changed, or found something without looking. A delegate's exit status establishes nothing: several return success on a refusal.

- **A document delegation** is verified by the file existing and being non-empty, then read.
- **An edit delegation** is verified by the diff over the enumerated file set, taken before and
  after. No diff means no edit, whatever the summary says.
- **Any delegation** is verified against the working tree for changes nobody asked for. A run that
  was not asked to edit and did is a failure, not a bonus — check the tree state before and after
  whenever a delegate has any write capability at all.

## Hand back the delegate's own output

Relay what the delegate actually said, plus what was verified, and say so explicitly when a delegation returned nothing. A summary of a summary loses the thing the delegation was spent on, and silence about an empty return reads as a finding of "nothing to report".

## Second opinions are advisory

Produce the primary deliverable first, fold the review in if it returns, and never block, defer, or condition the deliverable on the delegation. If the run times out or comes back empty, ship the deliverable and note that the review was unavailable.

## Chained delegations

Every delegation is single-shot with no memory of the previous call, so
**state lives on disk between links**: run N writes its findings to a file, run N+1 reads that file.
Each link gets its own foreground budget, and each intermediate file is checked non-empty before the next call is spent on it — a chain that carries an empty file forward spends every remaining link on nothing.
