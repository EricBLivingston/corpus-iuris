---
description: "Executes a phased plan folder (an Overview plus numbered phase files) end to end as the terminal stage of Spec-Driven Development, driving every phase through the analyze, code, review, test cycle. Takes the folder, optionally a phase to start from. A single unphased plan file goes to implement instead."
argument-hint: "[plan-folder] [starting at Phase X]"
---

# Orchestrate Command

## Arguments

`$ARGUMENTS` = the plan folder name, optionally followed by `starting at Phase X`. Parse it to extract:

- `{Plan Folder}` — the plan folder name (the tokens before "starting at")
- `{Starting Phase}` — the phase to begin at, phases before it skipped (default: 1)

Set `{Project Path}` = absolute path of `plans/{Plan Folder}` resolved against the invoking user's current working directory: run `pwd` and prepend its output. Sub-agents may execute with a different cwd, so a relative `plans/...` silently lands outside the project; every downstream substitution embeds the absolute prefix verbatim. Verify it begins with `/` and does NOT resolve inside your agent-configuration directory, unless the plan lives in that meta-project.

## Critical Directive: Context Preservation

You orchestrate; you do not investigate. NEVER read source, or any file a sub-agent in this run wrote; NEVER write, edit, review, or test code yourself, except that inserting a granted amendment into the remit is yours (§ 3.E). Read only `Overview.md` and the `Phase-X.md` files (the whole specification this run executes against), plus `{command-root}/{implement,debrief}.md` and the dispatch prompts under `{reference-root}/templates/orchestration/` once each; the ATO row of each statement a coder's remediation return names, and the amendment it authorizes, are the one sub-agent-written text you read; a skill this workflow directs you to invoke is not a read. The specs those phase files superseded are archived and closed to every reader in this run, the governor included. Pass file paths between sub-agents; instruct each to write detailed output to files and return only a one-line status. If something fails, dispatch a specialist.

## Workflow

### 0. Pre-Flight

Verify clean working tree: `git status --porcelain` must be empty. If dirty, enter the **Terminal** with: "Commit or stash before running orchestrate: the run requires a clean tree."

### 1. Validate Plan Folder

A. Confirm `{Project Path}/Overview.md` exists
B. Discover all `Phase-X.md` files in `{Project Path}`
C. Sort phases numerically and report the plan structure to the user before proceeding

Any of these failing (no `Overview.md`, no phase file, a gap in the numbering) enters the **Terminal**.

### 2. Learn the Implementation Cycle

Invoke the `writing-code` skill, then read `{command-root}/implement.md` to contextualize the workflow in our Implementation protocol.

### 3. Execute Each Phase Sequentially

For each `Phase-X.md` (in order, starting from `{Starting Phase}`), read the phase file, then execute the implementation cycle by dispatching specialist sub-agents directly. Each step below names its dispatch prompt's file under `{reference-root}/templates/orchestration/`; read that file and pass the prompt it contains. Resolve every placeholder before passing a prompt: sub-agents receive concrete paths, none left standing except `{Subject}`, which the sub-agent determines during execution.

`{File Rules}` is defined in `{reference-root}/templates/orchestration/file-rules.md` and substituted verbatim into each specialist prompt beside it.

∋3: each specialist writes its file and returns one line; wait for that line.

#### A. Analyze

Dispatch the analyzer agent with the prompt at `{reference-root}/templates/orchestration/analyzer-prompt.md`.

#### B. Implement

Dispatch the coder agent with the prompt at `{reference-root}/templates/orchestration/coder-prompt.md`. Omit the `Prior findings` line on the first dispatch of a phase; on re-invocation set `{Prior Report Path}` to the review, test or adjudication report that prompted it.

#### C. Review

Dispatch the reviewer agent with the prompt at `{reference-root}/templates/orchestration/reviewer-prompt.md`. Same omission rule as the coder's, `{Prior Report Path}` being the report that prompted the coder pass now under review.

**If the review fails**: re-invoke the coder agent with the review file path, then re-invoke the reviewer. Repeat until the review passes. If the review has not passed after 3 iterations, enter the **Terminal**, supplying the review gate and the iteration count in place of a verdict line.

#### D. Test

Dispatch the tester agent with the prompt at `{reference-root}/templates/orchestration/tester-prompt.md`.

**If tests fail**: re-invoke the coder agent with the test report file path, then the reviewer with that same test report as its `{Prior Report Path}`, then the tester. Repeat until tests pass. If tests have not passed after 3 iterations, enter the **Terminal**, supplying the test gate and the iteration count in place of a verdict line.

#### E. Adjudicate

Invoke `governing-work` and dispatch the governor agent with its adjudication shape, Remit being `{Project Path}/Overview.md` and `{Project Path}/Phase-X.md`, Documentation being:

- `{Project Path}/Phase-X-Analysis.md`
- `{Project Path}/Phase-X-Implementation.md`
- `{Project Path}/Phase-X-Review.md`
- `{Project Path}/Phase-X-Test-Report.md`

Before composing the dispatch, confirm every report listed above is on disk (※3, by directory listing). A missing one is a failure of the specialist step that owed it: re-invoke that specialist before dispatching the governor.

`governing-work`'s routing table narrows onto this run as follows:

- `^PASS`: Between Phases.
- `^FAIL` with an `external` finding: append the return verbatim to `{Project Path}/Phase-X-Adjudication.md`, then enter the **Terminal**.
- `^FAIL` otherwise: append the return verbatim to `Phase-X-Adjudication.md`. If three remediation dispatches have run in this phase, enter the **Terminal** (⊨7). Otherwise dispatch the coder agent with `coder-prompt.md`, `{Prior Report Path}` set to the adjudication, and route its line:
  - `^REMEDIATED`: record each grant the line names, then run § 3.C (`{Prior Report Path}` the adjudication) and § 3.D over the phase, each with its own loop and cap, then § 3.E again.
  - `^ESCALATED`: record each grant the line names, then enter the **Terminal**.
- Anything else from the governor: append the return verbatim to `Phase-X-Adjudication.md`, then enter the **Terminal**. A malformed coder line: enter the **Terminal**.

Recording a grant: read the ATO row of each named statement; on `granted`, insert what it authorizes into the plan files it amends, composing nothing. Leave the coder's Deviations entry standing.

#### Between Phases

1. Report phase completion status to the user (one line per specialist: analysis, implementation, review, test, adjudication)
2. Continue immediately to the next phase
3. Preserve every markdown file created during phase execution

### 4. Debrief

After all phases are complete, read `{command-root}/debrief.md`, then invoke the analyzer agent with a prompt derived from its instructions, passing `{Project Path}` as the plan folder. The analyzer must write the debrief report to `{Project Path}/Implementation-Debrief.md` and return only a one-line status summary.

### 5. Fact-Check

If the `auditing-subagents` skill is not installed, skip to Final Summary.

Invoke the `auditing-subagents` skill via the Skill tool with `{Project Path}` as args.

An honesty check: critical findings do NOT halt the workflow; the user reviews the audit report directly. The skill folds `{Project Path}/Implementation-Debrief.md` into its roll-up automatically.

It returns a path to `{Project Path}/subagent-audit.md` and a one-line verdict (PASS / Critical count / Major count). Capture that line for the summary and notification below, and relay it alone; do NOT read `subagent-audit.md` yourself.

### 6. Final Summary

Report to the user:

- Number of phases completed
- One-line status per phase, from the summaries you collected
- Report locations: `{Project Path}/Implementation-Debrief.md` and `{Project Path}/subagent-audit.md`
- Audit verdict: [e.g. `PASS (0 Critical, 0 Major)` or `2 Critical findings — review subagent-audit.md`]

### 7. Push Notification

- Push-notify the user, if the capability exists, carrying the final summary and the audit verdict, omitting the report locations (inaccessible from a phone): e.g. `Implementation complete. Audit: PASS`.

### Terminal

Reachable from any step: every gate enters it on failure, and no branch continues past a gate it did not clear.

1. Stop. Leave the tree exactly as it is: revert nothing, commit nothing, delete nothing.
2. Report to the user: the phase and step reached; the failing gate, details; for an adjudication, the `Phase-X-Adjudication.md` path, and on an escalation `Phase-X-Implementation.md § Remediation` too.
3. Push-notify the user with that same failure line, if the capability exists.
4. Hand control back and end the run.
