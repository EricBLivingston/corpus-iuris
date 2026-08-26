# Implementation — <Title>

**Status:** <Ready to build | In progress>
**Source of truth:** `<path>/Design.md` + `<path>/PRD.md` — read both; link to them, do not restate their rationale. (Short-circuit route: when Design was skipped for trivial work, the PRD alone is the source.)
**Last updated:** YYYY-MM-DD

## Orientation

<One paragraph: what gets built and where (target file/module/crate), pointing each concern back to its Design section (spine §1, data model §2, the mechanism §3, ...). State conventions that apply throughout **once** here rather than repeating per phase — typing discipline, test runner invocation, debug-script placement, naming conventions. Name any known acceptable residual ("do not chase X") so the builder does not fight a ratified outcome.>

---

> **How to use this template.** The phase spine is the load-bearing structure. Every phase carries the spine: **Goal** (observable outcome for THIS phase) → **concrete file-named steps** (name the file/symbol and the exact change; reference Design §N instead of re-deriving why). **Done** is strongly recommended — see below — but is not part of the mandatory spine. Write each step as an imperative led by an action verb — Add, Edit, Delete — not as narration ("Add X handling to `parser.py`", not "the logic should handle X"). Add or drop phases freely. The one failure mode to avoid: do NOT reorganize into thematic sections that re-explain architecture. Do NOT add per-step "Rationale / Why" inline — push it to Design, where it belongs. Delete this block when filling in real phases.

---

## Phase 0 — <Pre-flight / scaffold> (OPTIONAL)

<Use when the build needs an access check, dependency install, or scaffolding step before real work can begin. Delete if the first real change can start immediately.>

**Goal:** <What must be true before Phase 1 can proceed.>

- <Step: e.g., confirm library version / create directory scaffold / verify API credentials>

**Done** (recommended): <Checkable confirmation: e.g., `import X` succeeds; directory exists; `cargo check` passes.>

---

## Phase N — <Phase title>

**Goal:** <Observable outcome for THIS phase only — do not restate the Design or the plan-level purpose.>

- <Concrete step: name the file/symbol and the exact change. Reference the Design section (§N) rather than re-deriving why.>
- <Concrete step: e.g., "Edit `src/pipeline/extractor.py` `extract_records()` — replace the bare dict return with the typed `ExtractedRecord` model (Design §2).">
- <Concrete step ...>

**Done** (recommended): <Checkable acceptance for this phase — counts, greps, named fixture results, or a runnable command and its expected output. **Strongly recommended**: this is the quality differentiator the best Implementation docs carry, rare in corpus-wide data but cleanly separating strong from median. The phase spine (Goal + file-named steps) is the mandatory part; Done is the mark to aim for.>

<Repeat Phase blocks as needed. Phases may be called Commits or Stages; sub-numbering is open (1a/1b, 1.1/1.2). Keep phases atomic enough that the tree is reviewable after any one of them.>

---

## Affected Files (OPTIONAL)

<Use when phases touch many files and a one-glance map helps. Delete if the per-phase steps already make the file list obvious.>

| File | Change | Phase |
| ---- | ------ | ----- |
| `<path/to/file>` | <One-line description> | <N> |

---

## Verification (OPTIONAL)

<The acceptance gate the tester agent owns: the full list of measured targets, assertions, and fixture tests — operationalizing Design §8's verification strategy (when routed through a Design) — that discharge the PRD's acceptance criteria (§4) and guardrails (§3), plus the exact commands. Language-parameterize — do not hardcode one toolchain:>

- Python: `uv run pytest <test_path> -v`
- Rust: `cargo test --workspace`

<May live as a final phase instead (e.g., "Phase N — Verification"). Delete this section only if the per-phase **Done** checks that are present (plus any final verification phase) fully cover acceptance and nothing remains for a final gate.>

---

## Risks & Mitigations (OPTIONAL)

<Use only for build-time risks beyond what Design already covered. Delete if Design §6 is sufficient.>

| Risk | Mitigation |
| ---- | ---------- |
| <Specific build-time risk> | <Specific mitigation> |

**Rollback:** <git is the default net — the mandatory pre-session commit means `git reset --hard` or discarding the working tree recovers every in-scope delta. Add explicit rollback steps ONLY for state git does not capture: system-file edits, DB migrations, external services. Omit for pure in-repo work.>

---

## Deviations (OPTIONAL — project convention)

<Empty at authoring time. The coder records any departure from Affected Files, phase steps, or any **Done** criteria that were specified, here **before** invoking the reviewer. Default when nothing deviated: "None — executed as planned." Projects that record deviations in a separate debrief artifact (e.g., `Implementation-Debrief.md` or a `debrief/`-folder workflow) may omit this section entirely — use whichever convention the project's workflow establishes.>

- None — executed as planned.
