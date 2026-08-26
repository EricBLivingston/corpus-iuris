---
description: Executes a phased plan folder end to end — an Overview plus numbered phase files, the terminal stage of Spec-Driven Development — driving every phase through the analyze, code, review, test cycle. Takes the folder, optionally a phase to start from. A single unphased plan file goes to implement instead.
argument-hint: "[plan-folder] [starting at Phase N]"
model: fable
---

# Orchestrate Command

Execute a complete implementation plan from a prepared plan folder containing `Overview.md` and one or more `Phase-X.md` files.

## Arguments

`$ARGUMENTS` = the plan folder name, optionally followed by `starting at Phase X`. Parse it to extract:

- `{Plan Folder}` — the plan folder name (the tokens before "starting at")
- `{Starting Phase}` — the phase to begin at, phases before it skipped (default: 1)

Set `{Project Path}` = absolute path of `plans/{Plan Folder}` resolved against the **invoking user's current working directory** — run `pwd` and prepend its output. Sub-agents may execute with a different cwd, so a relative `plans/...` silently lands outside the project, losing files; every downstream substitution embeds the absolute prefix verbatim. Verify by inspection: it begins with `/`, and does NOT resolve inside your agent-configuration directory — the tree holding your rules, agents and commands — unless the plan genuinely lives in that meta-project.

## Critical Directive: Context Preservation

You orchestrate; you do not investigate. **NEVER** read source / analysis / review / test / audit output yourself; **NEVER** write, edit, review, or test code yourself. Read only `Overview.md` and the `Phase-X.md` files — the whole specification this run executes against — plus `{command-root}/{implement,debrief}.md` once each; a skill this workflow directs you to invoke is not a read. The specs those phase files superseded are archived and closed to this run. **DO** pass file paths between sub-agents and instruct each to write detailed output to files and return only a one-line status. If something fails, dispatch a specialist — don't investigate yourself.

## Workflow

### 0. Pre-Flight

A. Verify clean working tree: `git status --porcelain` must be empty. If dirty, abort with: "Commit or stash before running orchestrate — diff baseline requires clean tree." Do not proceed.
B. Capture `git rev-parse HEAD` as `{Baseline Commit}`. Every reviewer pass in this run diffs against it.
C. Report `{Baseline Commit}` to the user before continuing.

### 1. Validate Plan Folder

A. Confirm `{Project Path}/Overview.md` exists
B. Discover all `Phase-X.md` files in `{Project Path}`
C. Sort phases numerically and report the plan structure to the user before proceeding

### 2. Learn the Implementation Cycle

Invoke the `writing-code` skill, then read `{command-root}/implement.md` to contextualize the workflow in our Implementation protocol.

### 3. Execute Each Phase Sequentially

For each `Phase-X.md` (in order, starting from `{Starting Phase}`), read the phase file, then execute the implementation cycle by dispatching specialist sub-agents directly. Resolve every placeholder before passing a prompt — sub-agents receive concrete paths, none left standing except `{Subject}`, which the sub-agent determines during execution.

※3 — each specialist writes its file and returns one line; wait for that line.

#### A. Analyze

Invoke the analyzer agent with:

```
Analyze the codebase to understand the scope and impact of the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md

File rules:
- Reports: {Project Path}/Phase-X-{Subject}.md
- Test scripts: {Project Path}/tests/*.py
- Test logs: {Project Path}/tests/*.log
- ALL files MUST be within: {Project Path}
- NO files in: .analysis/, /tmp, or any location outside the project path

Write your analysis to: {Project Path}/Phase-X-Analysis.md
Include: affected files, dependencies, risks, and recommended implementation approach.

Return only a one-line status summary. Do NOT return the full analysis content.
```

#### B. Implement

Invoke the coder agent with:

```
Implement the changes described in the following phase.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Prior findings to address: {Prior Report Path}

File rules:
- Reports: {Project Path}/Phase-X-{Subject}.md
- Test scripts: {Project Path}/tests/*.py
- Test logs: {Project Path}/tests/*.log
- ALL files MUST be within: {Project Path}
- NO files in: .analysis/, /tmp, or any location outside the project path

Write an implementation summary to: {Project Path}/Phase-X-Implementation.md
Include: files modified/created, deviations from plan (with justification), and any issues encountered.

After implementing, fill the Deviations section of the phase file before invoking the reviewer.

Return only a one-line status summary.
```

Omit the `Prior findings` line on the first dispatch of a phase; on re-invocation set `{Prior Report Path}` to the review or test report that prompted it.

#### C. Review

Invoke the reviewer agent with:

```
Review the implementation for the following phase against the plan and analysis.

Phase file: {Project Path}/Phase-X.md
Project overview: {Project Path}/Overview.md
Analysis: {Project Path}/Phase-X-Analysis.md
Implementation summary: {Project Path}/Phase-X-Implementation.md
Baseline commit (orchestrate run kickoff): {Baseline Commit}
Prior findings to address: {Prior Report Path}

File rules:
- Reports: {Project Path}/Phase-X-{Subject}.md
- Test scripts: {Project Path}/tests/*.py
- Test logs: {Project Path}/tests/*.log
- ALL files MUST be within: {Project Path}
- NO files in: .analysis/, /tmp, or any location outside the project path

Write your review to: {Project Path}/Phase-X-Review.md
Include: issues found (critical/important/minor), whether implementation matches the plan, and suggested fixes.

**Scope audit (mandatory before verdict).** Establish that every file touched since {Baseline Commit} is in the plan's scope or a filed Deviation. Anything else fails the phase — the plan was incomplete, or the coder departed scope. An accepted Deviation re-engages the analyzer for related collateral.

Verify Deviations was filled. Verify ACs have verifier hints. Run a Reverse Dependency Audit if the phase changed any struct, enum, or public-API surface.

Return only a one-line status summary indicating pass/fail and issue count.
```

Omit the `Prior findings` line on the first dispatch of a phase; on re-invocation set `{Prior Report Path}` to the review or test report that prompted the coder pass now under review.

**If the review reports critical issues**: re-invoke the coder agent with the review file path, then re-invoke the reviewer. Repeat until the review passes. If the review has not passed after 3 iterations, enter the **Terminal**, supplying the review gate and the iteration count in place of a verdict line.

#### D. Test

Invoke the tester agent with:

```
Write and run tests to verify the implementation for the following phase.

Phase file: {Project Path}/Phase-X.md
Implementation summary: {Project Path}/Phase-X-Implementation.md
Review: {Project Path}/Phase-X-Review.md
Test scripts directory: {Project Path}/tests/
Test logs directory: {Project Path}/tests/

File rules:
- Reports: {Project Path}/Phase-X-{Subject}.md
- Test scripts: {Project Path}/tests/*.py
- Test logs: {Project Path}/tests/*.log
- ALL files MUST be within: {Project Path}
- NO files in: .analysis/, /tmp, or any location outside the project path

Write a test report to: {Project Path}/Phase-X-Test-Report.md
Include: tests run, pass/fail counts, coverage if available, and any failures with details.

Your verification includes the §16 cross-boundary end-to-end gate wherever the phase's work crosses a boundary.

Return only a one-line status summary indicating pass/fail and test counts.
```

**If tests fail**: re-invoke the coder agent with the test report file path, then the reviewer with that same test report as its `{Prior Report Path}`, then the tester. Repeat until tests pass. If tests have not passed after 3 iterations, enter the **Terminal**, supplying the test gate and the iteration count in place of a verdict line.

#### E. Adjudicate

Invoke `governing-work`, prompting the governor agent with the following parameters:

**Bounds** — the `## Governance Bounds` section of each of these two files, taken together:

- `{Project Path}/Overview.md`
- `{Project Path}/Phase-X.md`

**Content**:

- `{Project Path}/Phase-X-Analysis.md`
- `{Project Path}/Phase-X-Implementation.md`
- `{Project Path}/Phase-X-Review.md`
- `{Project Path}/Phase-X-Test-Report.md`

Before composing the dispatch, confirm every artifact listed under **Content** is on disk (※3 — a directory listing, not a read). A missing one is a failure of the specialist step that owed it: re-invoke that specialist — do not dispatch the governor, and do not put the gap to it as a governance question.

Route the governor's return per `governing-work`'s table, narrowed onto this run's own procedure:

- `^CLEAR.*` — continue to Between Phases.
- Anything else — a `STOP` line, prose, several lines, no line at all:
  - **Document the adjudication**: create or append to `{Project Path}/Phase-X-Adjudication.md` with the governor's return verbatim, and the bounds it was dispatched against.
  - Enter the **Terminal**.

#### Terminal

1. Stop. Leave the tree exactly as it is — revert nothing, commit nothing, delete nothing.
2. Report to the user: the phase and step reached; the failing gate, details.
3. Push-notify the user with that same failure line, if the capability exists.
4. Hand control back and end the run.

#### Between Phases

1. Report phase completion status to the user (one line per specialist: analysis, implementation, review, test, adjudication)
2. Continue immediately to the next phase
3. Trust the sub-agent status summaries; read no output file yourself
4. Preserve every markdown file created during phase execution

### 4. Debrief

After all phases are complete, read `{command-root}/debrief.md`, then invoke the analyzer agent with a prompt derived from its instructions, passing `{Project Path}` as the plan folder. The analyzer must write the debrief report to `{Project Path}/Implementation-Debrief.md` and return only a one-line status summary.

### 5. Fact-Check

Note: If the `auditing-subagents` skill is not installed, skip this step and move to step 6. Final Summary

Invoke the `auditing-subagents` skill via the Skill tool with `{Project Path}` as args.

An **honesty check, not a quality gate**: critical findings do NOT halt the workflow — the user reviews the audit report directly. The skill folds `{Project Path}/Implementation-Debrief.md` into its roll-up automatically.

It returns a path to `{Project Path}/subagent-audit.md` and a one-line verdict (PASS / Critical count / Major count). Capture that line for the summary and notification below, and relay it alone — do NOT read `subagent-audit.md` yourself.

### 6. Final Summary

Report to the user:

- Number of phases completed
- One-line status per phase, from the summaries you collected
- Location of the debrief report: `{Project Path}/Implementation-Debrief.md`
- Location of the audit report: `{Project Path}/subagent-audit.md`
- Audit verdict: [e.g. `PASS (0 Critical, 0 Major)` or `2 Critical findings — review subagent-audit.md`]

### 7. Push Notification

- Push-notify the user, if the capability exists, carrying the final summary and the audit verdict, omitting the report locations (inaccessible from a phone): e.g. `Implementation complete. Audit: PASS`.

## Rules

- Do NOT skip phases or execute them out of order
- All file writes must stay within `{Project Path}`
- An exhausted review or test loop, and any governor return that is not `CLEAR`, enter the Terminal. No branch exists in which a run continues past a gate it did not clear.
