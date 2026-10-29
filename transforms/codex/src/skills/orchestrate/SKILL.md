---
name: orchestrate
description: "Executes a phased plan folder (an Overview plus numbered phase files) end to end as the terminal stage of Spec-Driven Development, driving every phase through the analyze, code, review, test cycle. Takes the folder, optionally a phase to start from."
---

# Orchestrate Command

## Parse the plan folder and the starting phase

`$ARGUMENTS` = the plan folder name, optionally followed by `starting at Phase X`. Parse it to extract:

- `{Plan Folder}` — the plan folder name (the tokens before "starting at")
- `{Starting Phase}` — the phase to begin at, phases before it skipped (default: 1)

Set `{Project Path}` to the absolute path of `plans/{Plan Folder}`: run `pwd` in the invoking user's working directory and prepend its output. Use that absolute prefix in every downstream substitution. It must not resolve inside your agent-configuration directory unless the plan lives in that meta-project.

## Read only the specification; delegate everything else

NEVER read source, or any file a sub-agent in this run wrote; NEVER write, edit, review, or test code yourself, except that inserting a granted amendment into the charter is yours (§ 3.E). Read only `Overview.md` and the `Phase-X.md` files, plus `{skill-root}/implement/SKILL.md` and `{skill-root}/debrief/SKILL.md` and the dispatch prompts under `{reference-root}/templates/orchestration/` once each; the ATO row of each statement a coder's remediation return names, and the amendment it authorizes, are the one sub-agent-written text you read; a skill this workflow directs you to invoke is not a read. You may also write `{Dispatch Map}` and read session identity and execution-boundary metadata. The specs those phase files superseded are archived and closed to every reader in this run, the governor included. Pass file paths between sub-agents; instruct each to write detailed output to files and return only a one-line status. If something fails, dispatch a specialist.

## Run every phase, then debrief and report

### 0. Verify a clean working tree

`git status --porcelain` must be empty. If dirty, enter the **Terminal** with: "Commit or stash before running orchestrate: the run requires a clean tree."

### 1. Validate the plan folder

A. Confirm `{Project Path}/Overview.md` exists
B. Discover all `Phase-X.md` files in `{Project Path}`
C. Sort phases numerically and report the plan structure to the user before proceeding

Any of these failing (no `Overview.md`, no phase file, a gap in the numbering) enters the **Terminal**.

### 2. Learn the implementation cycle

Invoke the `writing-code` skill, then read `{skill-root}/implement/SKILL.md` to contextualize the workflow in our Implementation protocol.

### 3. Execute each phase sequentially

Read each `Phase-X.md` in order from `{Starting Phase}` and dispatch the specialists directly. Read and pass each step's named prompt under `{reference-root}/templates/orchestration/`, resolving all placeholders except `{Subject}`, which the delegate determines.

`{File Rules}` is defined in `{reference-root}/templates/orchestration/file-rules.md` and substituted verbatim into each specialist prompt beside it.

Use agent roles as `task_name`, omitting `agent_type`. Record phase and attempt in `{Dispatch Map}`.

∋3: each specialist writes its file and returns one line; wait for it. Audit returns belong to their queued jobs (§ 5).

#### Dispatch records

Use `{Project Path}/audit/dispatch-map.jsonl` for `{Dispatch Map}`. Resolve the orchestrator's thread from `CODEX_THREAD_ID`, its `agent_path` from its original log's first `session_meta`, and its active `task_started.turn_id`. Record each dispatch's phase, role, attempt, prompt, report paths and initiating thread/path/turn.

Reuse existing role agents with `followup_task`, waiting if active; spawn missing roles. Resolve each original delegate log from its first `session_meta`, matching `parent_thread_id` to the orchestrator thread and `agent_path` to the canonical task path returned or inventoried. Record that log's `id` and absolute path; capture its EOF line before a follow-up.

After each specialist return, select its own `task_started` by `turn_attribution.initiating_agent_path` and `parent_turn_id` matching the recorded initiating path/turn; follow-ups start after the captured EOF. Match `task_complete.turn_id` and record the turn ID and inclusive 1-based start/completion line span. Inherited history carries later metadata and rewritten timestamps; `subagent_history_start_ordinal` is not a line index. Missing or nonunique ownership, start or completion enters the Terminal with phase, role, attempt and the offending metadata.

#### Audit queue

Run audit jobs serially through one reused `auditor` with `followup_task` (spawn it only if absent), while specialist work continues. Retain each verdict with its phase/role/report job.

#### A. Analyze

Dispatch the analyzer agent with the prompt at `{reference-root}/templates/orchestration/analyzer-prompt.md`.

#### B. Implement

Dispatch the coder agent with the prompt at `{reference-root}/templates/orchestration/coder-prompt.md`. Omit the `Prior findings` line on the first dispatch of a phase; on re-invocation set `{Prior Report Path}` to the review, test or adjudication report that prompted it.

#### C. Review

Dispatch the reviewer agent with the prompt at `{reference-root}/templates/orchestration/reviewer-prompt.md`. Same omission rule as the coder's, `{Prior Report Path}` being the report that prompted the coder pass now under review.

If the review fails: re-invoke the coder agent with the review file path, then re-invoke the reviewer. Repeat until the review passes. If the review has not passed after 3 iterations, enter the **Terminal**, supplying the review gate and the iteration count in place of a verdict line.

#### D. Test

Dispatch the tester agent with the prompt at `{reference-root}/templates/orchestration/tester-prompt.md`.

If tests fail: re-invoke the coder agent with the test report file path, then the reviewer with that same test report as its `{Prior Report Path}`, then the tester. Repeat until tests pass. If tests have not passed after 3 iterations, enter the **Terminal**, supplying the test gate and the iteration count in place of a verdict line.

#### E. Adjudicate

Invoke `governing-work` and dispatch the governor agent with its adjudication shape, Charter being `{Project Path}/Overview.md` and `{Project Path}/Phase-X.md`, Documentation being:

- `{Project Path}/Phase-X-Analysis.md`
- `{Project Path}/Phase-X-Implementation-Report.md`
- `{Project Path}/Phase-X-Review.md`
- `{Project Path}/Phase-X-Test-Report.md`

Before composing the dispatch, confirm every report listed above is on disk (※3, by directory listing). A missing one is a failure of the specialist step that owed it: re-invoke that specialist before dispatching the governor.

`governing-work`'s routing table narrows onto this run as follows:

- `^PASS`: § 3.F, then Between phases.
- `^FAIL` with an `external` finding: append the return verbatim to `{Project Path}/Phase-X-Adjudication.md`, then enter the **Terminal**.
- `^FAIL` otherwise: append the return verbatim to `Phase-X-Adjudication.md`. If three remediation dispatches have run in this phase, enter the **Terminal** (⊨7). Otherwise dispatch the coder agent with `coder-prompt.md`, `{Prior Report Path}` set to the adjudication, and route its line:
  - `^REMEDIATED`: record each grant the line names, then run § 3.C (`{Prior Report Path}` the adjudication) and § 3.D over the phase, each with its own loop and cap, then § 3.E again.
  - `^ESCALATED`: record each grant the line names, then enter the **Terminal**.
- Anything else from the governor: append the return verbatim to `Phase-X-Adjudication.md`, then enter the **Terminal**. A malformed coder line: enter the **Terminal**.

Recording a grant: read the ATO row of each named statement; on `granted`, insert what it authorizes into the plan files it amends, composing nothing. Leave the coder's Deviations entry standing.

#### F. Audit

Invoke `performing-audits` once per run. Queue one audit per phase role, grouping its original log and all its phase attempts:

- Work: `{Project Path}/Overview.md`, `{Project Path}/Phase-X.md`, and the role's recorded prompts.
- Record: the original log path, selected turn IDs and inclusive spans; Q1/Q2 cover those own execution spans. Include descendants whose first `session_meta.parent_thread_id` and own `task_started.turn_attribution.parent_turn_id` identify a selected parent execution, recursively, and cited records.
- Reports: the paths assigned to the role's attempts.
- Reach: `conduct`.
- Report: `{Project Path}/audit/Phase-X-<role>-Audit.md`.
- Staging: `<session scratchpad>/audit/Phase-X/<role>/`.

Continue Between phases immediately; route audit lines per `performing-audits`.

#### Between phases

1. Report phase completion status to the user (one line per specialist: analysis, implementation, review, test, adjudication)
2. Continue immediately to the next phase
3. Preserve every markdown file created during phase execution

### 4. Debrief

After all phases are complete, read `{skill-root}/debrief/SKILL.md`, then invoke the analyzer agent with `task_name: analyzer` and a prompt derived from its instructions, passing `{Project Path}` as the plan folder. The analyzer must write the debrief report to `{Project Path}/Implementation-Debrief.md` and return only a one-line status summary.

### 5. Collect the audits

Drain all queued audits through the same auditor; collect and relay every phase/role/report job's line per `performing-audits`.

### 6. Report the run to the user

Report to the user:

- Number of phases completed
- One-line status per phase, from the summaries you collected
- Report locations: `{Project Path}/Implementation-Debrief.md` and `{Project Path}/audit/`
- One `Phase-X <role> audit: <line>` per dispatched role audit

### 7. Push-notify the user

Push-notify the user, if the capability exists, with § 6's report and audit lines compressed to phase/role and counts, omitting report paths. Compress a line other than `CLEAN` or `FINDINGS` to its kind with phase/role.

### Terminal: stop, report, hand back

1. Stop specialist dispatches and enqueue no new audits. Leave the tree exactly as it is: revert nothing, commit nothing, delete nothing.
2. Push-notify the user with the failure line at once, if the capability exists.
3. Collect the audits already dispatched (§ 5).
4. Report to the user: the phase and step reached; the failing gate, details; for an adjudication, the `Phase-X-Adjudication.md` path, and on an escalation `Phase-X-Implementation-Report.md § Remediation` too; each `Phase-X <role> audit: <line>`.
5. Hand control back and end the run.
