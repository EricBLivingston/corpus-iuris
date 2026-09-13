# Implementation — <Title>

**Status:** <Ready to build | In progress>
**Source of truth:** `<path>/Design.md` + `<path>/PRD.md`; read both, link to them, do not restate their rationale. (Short-circuit route: where Design was skipped for trivial work, the PRD alone.)

## Orientation

<One paragraph: what gets built and where (target file, module, or crate), pointing each concern back to its Design section (spine §1, data model §2, the mechanism §3, ...). State the conventions that hold throughout once here rather than per phase: typing discipline, test runner invocation, debug-script placement, naming. Name any ratified residual ("do not chase X") so the builder does not fight it.>

---

> **Filling this template.** Every phase carries the spine: **Goal** (observable outcome for THIS phase) → concrete steps naming the file or symbol and the exact change, each an imperative led by Add, Edit, or Delete, citing Design §N instead of re-deriving why. **Done** is recommended but sits outside the spine. Add or drop phases freely. Do not reorganize into thematic sections that re-explain architecture, and do not add per-step "Rationale / Why" (that belongs in Design). Delete this block when filling in real phases.

---

## Phase 0 — <Pre-flight / scaffold> (OPTIONAL)

<An access check, dependency install, or scaffolding step the build needs before real work can begin. Delete if the first real change can start immediately.>

**Goal:** <What must be true before Phase 1 can proceed.>

- <Step: e.g. confirm library version / create directory scaffold / verify API credentials>

**Done** (recommended): <e.g. `import X` succeeds; directory exists; `cargo check` passes.>

---

## Phase N — <Phase title>

**Goal:** <Observable outcome for THIS phase only.>

- <Concrete step: name the file or symbol and the exact change; cite Design §N.>
- <e.g. "Edit `src/pipeline/extractor.py` `extract_records()`: replace the bare dict return with the typed `ExtractedRecord` model (Design §2).">
- <Concrete step ...>

**Done** (recommended): <Checkable acceptance for this phase: counts, greps, named fixture results, or a runnable command and its expected output.>

<Repeat Phase blocks as needed. Phases may be called Commits or Stages; sub-numbering is open (1a/1b, 1.1/1.2). Keep each atomic enough that the tree is reviewable after it.>

---

## Affected Files (OPTIONAL)

<A one-glance map when phases touch many files. Delete when the per-phase steps already make the file list obvious.>

| File | Change | Phase |
| ---- | ---- | ---- |
| `<path/to/file>` | <One-line description> | <N> |

---

## Verification (OPTIONAL)

<The acceptance gate the tester agent owns: the measured targets, assertions and fixture tests that operationalize Design §8 and discharge the PRD's §4 acceptance criteria and §3 guardrails, plus the exact commands. Language-parameterize:>

- Python: `uv run pytest <test_path> -v`
- Rust: `cargo test --workspace`

<May live as a final phase instead (e.g. "Phase N — Verification"). Delete only where the per-phase **Done** checks, plus any final verification phase, fully cover acceptance.>

---

## Risks & Mitigations (OPTIONAL)

<Build-time risks beyond what Design §6 covered.>

| Risk | Mitigation |
| ---- | ---- |
| <Specific build-time risk> | <Specific mitigation> |

**Rollback:** <Git is the default net: the mandatory pre-session commit means `git reset --hard` recovers every in-scope delta. Add explicit rollback steps only for state git does not capture: system-file edits, DB migrations, external services. Omit for pure in-repo work.>

---

## Deviations (OPTIONAL — project convention)

<Empty at authoring time. The coder records any departure from Affected Files, phase steps, or a stated **Done** criterion here before invoking the reviewer. Projects that record deviations in a separate debrief artifact may omit this section.>

- None — executed as planned.
