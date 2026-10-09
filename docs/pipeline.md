# Pipeline: from a request to phased work

Spec-Driven Development is one of the three layers published here. It is the part that turns a request into documents, and those documents into a folder of phases something else can execute. The commands are ordinary Markdown: each one states what it takes, which template it fills, which agent it dispatches, and what it hands on.

![The pipeline from prepare through finalize, and the archive drop that keeps specs out of the pipe](diagrams/sdd-pipeline.svg)

## The commands, and what each produces

`prepare`, `phase`, `orchestrate`, `debrief` and `finalize` are the staged line. `implement` is the unphased alternative to `orchestrate`, for a plan small enough to run as one unit. `optimize` and `audit` are off the line entirely, each a pass over one target.

| Command | Takes | Produces | Hands on | Changes code |
| ---- | ---- | ---- | ---- | ---- |
| `prepare` | the target artifact's path | `PRD.md`, `Design.md` or `Implementation.md`, plus `Background.md` on the PRD branch | the next artifact, named by the PRD's own next-step section | no |
| `phase` | the plan folder | `Overview.md`, one or more `Phase-N.md`, and a sweep manifest under `archive/` | a folder `orchestrate` can consume | no |
| `orchestrate` | the plan folder, optionally a phase to start from | per-phase analysis, implementation, review, test reports and, on a non-pass verdict, adjudication reports, a per-phase audit under `audit/`, then `Implementation-Debrief.md` | the debrief, to `finalize` | yes, through the coder agent |
| `implement` | one plan file, or a plan already in conversation | an implementation report beside the plan | nothing staged; it is the whole run | yes, through the coder agent |
| `debrief` | the plan folder, every phase complete | `Implementation-Debrief.md` | the debrief, to `finalize` | no |
| `finalize` | the plan folder holding that debrief and its audits | `debrief/Debrief.md` and `debrief/Implementation.md` | a close-out plan the user reviews, then re-phases | no |
| `optimize` | one document path | an `-OPT` copy under `{analysis-root}/`, never beside the original | nothing; a standalone pass | no |
| `audit` | one path relative to the project root | a findings table and summary line under `{analysis-root}/` | nothing; a standalone pass | no |

Only `orchestrate` and `implement` reach code, and neither writes any itself: both route every edit through the coder agent.

## The line closes into a loop

`finalize` states its own position as `orchestrate → finalize → (manual review) → phase → orchestrate`, and it stops at the review. The close-out plan it produces is a plan like any other, so the user reads it, then re-enters the pipeline at `phase`. Nothing continues automatically, because the decision the loop turns on is which of the debrief's items and the audits' findings are worth doing at all.

## `prepare`: the artifact you name is the artifact it writes

The argument is a path, for example `plans/<name>/Design.md`. Two facts are read off it: the directory is the plan folder, and the filename selects the branch.

| Target | Template filled | Precursors read | Next step |
| ---- | ---- | ---- | ---- |
| `PRD.md` | the PRD template | the user's request | routed to Design or Implementation, and the routing is recorded in the PRD |
| `Design.md` | the Design template | the sibling `PRD.md` | always Implementation |
| `Implementation.md` | the Implementation template | the sibling `PRD.md`, plus `Design.md` where one exists | terminal: `implement` or `orchestrate` |

`Background.md` is the ground: why there is a plan at all. It exists for a mechanical reason: the agent that authors the artifact does not inherit the session where the request was made, so whatever the session knows and the plan folder does not has to be written down before the dispatch.

The three artifacts are three regimes, and the test for which one owns a fact is which change would rewrite it:

- The PRD is Why, and a different problem rewrites it.
- The Design is What, and a different conceptual approach rewrites it.
- The Implementation is How, and a different technology stack rewrites it.

A regime above the rewritten one stands, which is what makes a late change cheap: it lands in one document instead of in every document downstream of it. Each regime keeps its own deliberation and passes on only its result, because justification is a context sink.

Which of the two lower regimes a PRD routes into is decided by the exploring agent from what it observed in the codebase rather than from the request. Work that fits the established architecture, patterns and boundaries with no new components or data shapes routes straight to Implementation; requirements introducing something the codebase does not yet accommodate route to Design. In doubt it prefers Design, on the ground that an unneeded design document is cheap and starting implementation against an unsettled architecture is not.

## `phase`: from specs to a folder that executes

Three steps produce a folder shaped for execution rather than for reading, with a remit check between the first two. The first two are delegated to the analyzer and the reviewer, the check to the governor; the sweep that closes the run names no delegate.

```mermaid
flowchart TD
  SPECS["The plan folder as the authoring left it: PRD, Design, Implementation, and whatever else accumulated"]
  WRITE["1. Analyzer: Overview.md, and one Phase-N.md per unit of work"]
  GATE{"1b. Governor: is the remit sound enough to hold the work to?"}
  REVIEW{"2. Reviewer: could a reader holding only these files rebuild the constraint, its warrant and its qualifications?"}
  BACK["The analyzer repairs the files"]
  STOP["Stop for the user"]
  CLASSIFY{"3a. The sweep, file by file: is this directly related to, and necessary for, implementing this phase's requirements?"}
  KEEP["3b. Keep, which each file must earn: sample data, code and ID mappings, shared diagrams, fixture inputs and golden outputs, files edited in place"]
  DROP["3c. Sweep, the default: source specs unconditionally, and background, rationale, history and the phasing run's own artifacts with them"]
  CLOSE["3d. Convergence: a check that finds no kept file still pointing at what was swept, which now sits in the plan's archive/"]

  SPECS --> WRITE --> GATE
  GATE -->|"PASS"| REVIEW
  GATE -->|"FAIL, repaired and checked again"| WRITE
  GATE -->|"a third FAIL"| STOP
  REVIEW -->|"a literal placeholder"| BACK
  BACK --> REVIEW
  REVIEW -->|"reconstructs"| CLASSIFY
  CLASSIFY -->|"earns a keep"| KEEP
  CLASSIFY -->|"default"| DROP
  KEEP --> CLOSE
  DROP --> CLOSE
```

The analyzer writes `Overview.md` and one `Phase-N.md` per unit of work (1). The Overview carries the orchestration and everything more than one phase needs; each phase file carries that phase's own actionable tasks and nothing redundant with the Overview, since both are handed to every phase.

The governor then checks the remit (1b): the new Overview and every phase file, with the sources still in the plan folder, so a remit it finds unsound is repaired from them. A `FAIL` sends the analyzer back with the findings, and a third `FAIL` stops for the user. Once it passes, the review's repair loop never re-runs it.

The reviewer then compares the produced files against the source specs (2), and the standard is reconstruction rather than mention: could a reader holding only these files rebuild the constraint, its warrant and its qualifications? Content added to satisfy the remit check is not content beyond the sources. A file still carrying a literal placeholder is rejected.

The sweep runs last, once the review passes. Every file in the folder that is not `Overview.md` or `Phase-N.md` is classified against one question (3a): is this content directly related to, and necessary for, implementing this phase's requirements? The default is to sweep (3c), and each file must earn a keep (3b). Source specs sweep unconditionally, however substantial they are, because keeping one pulls the plan into context twice; background, rationale, history and the process artifacts of the phasing run itself go with them. A keep is reserved for secondary reference material: sample data, code and ID mappings, diagrams shared across phases, fixture inputs and golden outputs, files being edited in place.

The swept files then move to the plan's `archive/`, and a convergence check over every kept file finds nothing still pointing at them (3d).

## `orchestrate`: driving the folder end to end

The plan folder's absolute path is resolved before anything else, by running `pwd` and prepending it, because sub-agents may run with a different working directory and a relative path silently lands outside the project.

The run then proceeds through gates, in order:

1. A clean working tree.
2. A plan folder with an Overview, phase files discovered and sorted, and no gap in the numbering.
3. The production chain over each phase in turn, covered in [the execution page](execution.md), each phase closing on the governor's adjudication; each governor `PASS` dispatches that phase's audit in the background.
4. A debrief.

The run closes by collecting every audit's summary line; no audit gates or halts it.

Every gate shares one failure mode, called **the Terminal**. It stops, leaves the tree exactly as it is, reverting nothing and committing nothing and deleting nothing, reports the phase and step reached and the gate that failed, and hands control back. No branch continues past a gate it did not clear.

## `implement`: the unphased alternative

`implement` takes a single plan file, or a plan already in the conversation, in which case it asks for the destination folder and confirms it before proceeding. Execution is the same production chain, with four additions:

- The coder records deviations in the plan file before review.
- The reviewer checks that they were recorded and that acceptance criteria carry verifier hints.
- The tester's verification includes the cross-boundary end-to-end gate wherever the work crosses a boundary.
- `governing-work` documents when holding the produced work to the plan's remit earns a governor dispatch.

A deviation is work the plan did not anticipate, and the plan file records it with the remit element it serves. Work beyond the remit is caught after the fact and contracted, ratified under authorization, or escalated.

## `debrief` and `finalize`: closing what the run left open

`debrief` sweeps the whole plan folder unconditionally. The debrief is the only artifact that records an assessment, so nothing else marks a phase as already assessed: not a commit, not a green test report, not a passing review. It reads every Markdown file in the folder root and none of the archived specs, extracts what the run left open into the categories its template defines, and ranks each item by severity.

`finalize` converts that into a plan, under two rules. The first rule is the binary decision: every carried item takes a Yes or a No, with no third option, and a No is a closure carrying its rationale, on the reasoning that if the item still matters a future analyzer rediscovers it from the live codebase, and if it is never rediscovered it was not material. The Yes list becomes an implementation plan grouped by work class, each item carrying its original finding ID, its file path and a verifier hint. Audit findings take Yes or No beside the debrief's items, and in any project but the corpus's own a Yes whose fix is in the corpus itself is listed as Open for review rather than executed.

The second rule is immutability, and it binds the produced plan's contents as much as its file operations. Everything in the plan folder outside `debrief/` is a historical record, errors and stale claims included, because forensic work later depends on those files reading exactly as the implementation left them. A defect spotted in an upstream artifact therefore goes on the No list with that rationale, rather than becoming a Yes-list item that would edit it: the same prohibited modification, deferred by one hop, is still prohibited.

## `optimize`: a pass over one document

The analyzer applies a fixed set of cuts (redundancy, verbosity, tutelage, tautology, superfluity, obsolescence, vacuity and scaffolding), and a ninth optimization refactors for maximum understanding at minimum tokens. The reviewer then compares the copy against the original for comprehensiveness, sufficiency and accuracy. Two kinds of duplicate are legitimate and stay: an enumeration that names the provision it enforces, and a passage carrying a reason or an operational detail the source lacks.

The copy lands under `{analysis-root}/`, the staging area the command names, rather than beside the original, because an optimized copy in an always-loaded directory is loaded alongside the file it optimized and doubles the cost the pass was run to cut.

## Why an executing phase is handed so little

![Why the orchestrator passes paths rather than content](diagrams/context-narrowing.svg)

`commands/orchestrate.md` opens with the constraint, which reads in full:

> You orchestrate; you do not investigate. NEVER read source, or any file a sub-agent in this run wrote; NEVER write, edit, review, or test code yourself, except that inserting a granted amendment into the remit is yours (§ 3.E). Read only `Overview.md` and the `Phase-X.md` files (the whole specification this run executes against), plus `{command-root}/{implement,debrief}.md` and the dispatch prompts under `{reference-root}/templates/orchestration/` once each; the ATO row of each statement a coder's remediation return names, and the amendment it authorizes, are the one sub-agent-written text you read; a skill this workflow directs you to invoke is not a read. The specs those phase files superseded are archived and closed to every reader in this run, the governor included. Pass file paths between sub-agents; instruct each to write detailed output to files and return only a one-line status. If something fails, dispatch a specialist.

The archived specs therefore reach no reader in the whole run, the governor included: it holds the work to the remit the Overview and phase files state.

The reason for the cut is that the adjacent phase is close to the worst possible distractor. Irrelevant material competes for attention rather than sitting inertly beside the signal, and the damage scales with resemblance: same project, same vocabulary, same file paths, adjacent intent, no longer relevant. Length alone degrades performance too, so dropping even harmless material pays. [The references](references.md) carry the work behind both claims.

Pruning at the outset is only half of the remedy, because an orchestrator that reads what it dispatches re-accumulates everything the split was meant to prevent. The orchestrating session therefore never reads source, and reads nothing a sub-agent in the run wrote save the ATO row of a statement a remediation names: not the analysis, not the implementation report, not the review, not the test report, not the audit. The discipline holds because the specialists return one line each and write their detail to files, rather than because the orchestrator exercises restraint over content it is holding.

It does write two things into the plan folder, and both are records of a gate rather than work product:

- A non-pass adjudication's return, verbatim, one entry per cycle.
- What a granted statement authorizes, inserted into the plan files it amends.

## Related pages

- [Execution](execution.md): the chain of specialists that executes what this pipeline produces.
- [Governance](governance.md): what the remit is, and what it costs to widen it.
- [The references](references.md): the published work behind the attention and length claims this page rests on.
