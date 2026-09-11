# Execution: inside one phase

The [pipeline](pipeline.md) produces a folder of phases. This page sets out what happens inside one of them: four specialists in a fixed order, two loops that re-enter it, and a gate at the end that tests the produced work against the limits the plan set before any of it ran.

![The production chain inside one phase, its loops, and the governor gate](diagrams/phase-cycle.svg)

## The chain

`※8` orders four steps and makes review never skippable, and `skills/writing-code/SKILL.md` drives them:

1. **Analyze.** The analyzer establishes scope: affected files, dependencies, risks, the recommended approach. Understanding that spans two or more files lands here, as does refactor and migration planning, a duplication hunt, and anything phrased "across the codebase".
2. **Implement.** The coder makes the changes.
3. **Review.** The reviewer returns findings ranked critical, important, nice-to-have.
4. **Test.** The tester runs only once review has passed.

Each step's output is the next step's input: the analysis to the coder, the implementation summary to the reviewer, the review to the tester. Review and test never run in parallel, because the reviewer's verdict is an input the tester should be holding.

The chain scales to the work rather than the reverse. Where the content is smaller than the round trip that would move it, analysis and testing fall away and the coding happens in the session that asked for it, with the review dispatched under a bounded charter. What does not scale away is the review: an independent pass over a change is the one stage sizing never removes, including for a non-code refactor.

## The roster

Each row is one definition file under `agents/`, and the charter column paraphrases what that file states for itself.

| Agent | Charter in one sentence | Barred from |
| ---- | ---- | ---- |
| analyzer | Investigates code or text at scale and reports what it finds, including as the author of prose and Markdown artifacts. | Writing code; amending a bound the work cannot land inside, without authorization first |
| coder | Writes and modifies source to the project's existing conventions. | Reviewing or testing its own work, or dispatching anything to do so; running git; an edit that cannot land inside a bound, without authorization first |
| reviewer | Reviews an already-written change and ranks what it finds. | Editing; recording a deviation that crosses a bound, which takes authorization instead |
| tester | Writes tests, runs suites, and decides whether a failure is a code defect or a test defect. | Editing the code under test; refactoring project code to make a test pass |
| governor | Tests handed content against handed bounds and reports, per bound, whether it was crossed. | Deriving or judging a bound, saying whether a crossing was acceptable, or dispatching at all |
| authorizer | Assesses a draft statement of assumed risk as Authorizing Official and records the decision. | Performing or redesigning the proposed act, acting as a stage of this chain, or dispatching at all |
| knowledge | Writes and curates persistent memory. | Writing without the scope-aware duplicate search that precedes every write, or duplicating an entry rather than updating the one already there |

The governor, the authorizer and the knowledge agent are not chain stages. The governor and the authorizer belong to [the governance apparatus](governance.md), and both are barred from dispatching precisely because a referee that can dispatch the work it referees is not a referee. The knowledge agent belongs to neither chain nor apparatus: `※6` routes every memory write to it, and searching needs no agent at all.

## Periti, and which specialists engage them

A peritus is an external model engaged through a command-line program for reach or a second judgement, one question at a time. It inherits no session and remembers no prior call, so the prompt is the whole of the engagement, and the responsum is weighed against the artifact it claims rather than against its exit status.

Delegation to a peritus is not the re-delegation the two-file rule bars, so the analyzer, coder and reviewer all engage them directly. The coder's use is the narrowest, and narrow by rule: mechanical transformation across two or more files, reaching no architecture decision and no judgement call. Confirming that the peritus changed the files it was asked to, and that the suite still passes, is not the coder reviewing its own work.

## Where the loops re-enter

Implement and review are a loop: the coder is re-invoked on the review's findings, and the change is re-reviewed, until review passes. A test failure re-enters at the coder, and the review loop runs again before the tester does.

Under `orchestrate` each re-invocation carries the report that prompted it as an explicit parameter, so the coder is never left to infer why it was called back.

## The fifth stage: adjudicate

`orchestrate` adds a stage the chain itself does not carry. After the tester, the phase's produced work is dispatched to the governor: the bounds are the Overview's and the phase file's bounds sections taken together, and the content is the reports the phase just produced.

The return routes four ways, and which one applies is the dispatcher's call alone:

- A clear return continues to the next phase.
- A crossed row where the work overran sends the coder back to cut it inside the bound, and the chain re-runs.
- A crossed row where the bound itself was wrong takes authorization before anything is amended, since amending it is ultra vires; [the governance page](governance.md) covers what that costs.
- An undetermined row means supplying what the governor's evidence column named as absent, and re-assaying.

Between phases the orchestrator reports one line per specialist, continues immediately, and preserves every Markdown file the phase produced.

## Related pages

- [The pipeline](pipeline.md): what produces the phases this chain executes.
- [Governance](governance.md): the bounds the adjudication tests against, and the path an act takes when it needs to move one.
