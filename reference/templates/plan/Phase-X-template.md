# Phase <N>: <Phase Title>

**Status:** Not Started
**Depends On:** <Phase N-1 \| None>
**Blocking:** <Phase N+1 \| ->

---

## Goals

1. <Observable outcome 1 for THIS phase only — do not restate plan-level goals>
2. <Observable outcome 2>
3. <Observable outcome N>

---

## Scope

### In Scope

- <Specific change 1 — aligns 1:1 with an entry in Affected Files>
- <Specific change 2>
- <Specific change N>

### Out of Scope

See Principle §2 (YAGNI); name adjacent work only where excluding it removes real ambiguity.

- <Adjacent change that could be mistaken for in-scope>
- <Deferred follow-up explicitly left for a later phase>
- <Item that belongs to another plan entirely>

---

## Affected Files

| File | Change |
| ---- | ---- |
| <path/to/file> | <One-line description of the specific change> |
| <path/to/other> | <One-line description of the specific change> |
| <path/to/tests> | <One-line description of the test-side change> |
| <config/file.toml> | <One-line description of the config or fixture change> |

---

## Implementation Steps

1. <Step 1: concrete, reviewable action>
2. <Step 2: concrete action (small enough to stop here and leave the tree reviewable)>
3. <Step N: concrete action>
4. **Flip phase status (mandatory tail step).** Once every Acceptance Criterion passes and the implementation summary is written, edit this file's `**Status:** Not Started` line to `**Status:** Complete` and update the matching row in `Overview.md`'s Progress Summary table and, where `Overview.md` has a Plan-Wide Inventory, the Status of this phase's rows in it. Each phase reconciles its own status, before the reviewer is invoked.

<Config Literal Audit and Serde Defaults Audit live in `Overview.md` § Cross-Cutting Concerns. Lift one here only where the analyzer determines the audit is phase-local.>

### Reverse Dependency Audit

<MANDATORY where this phase changes a struct signature, field, enum variant, or public API; delete otherwise. This is the call-site sweep that makes Principle §1 (No Backward Compatibility) safe: the break must be complete, not partial. Substitute the actual symbol names before running.>

- [ ] `rg '<TypeName>'` — direct references across the workspace
- [ ] `rg 'impl.*<TraitName>'` — implementors that must be updated
- [ ] Test call sites under the affected crate, for stale usages

### Open Questions (OPTIONAL)

<Delete if the analyzer resolved all design choices unilaterally.>

- <Unresolved design question>

---

## Acceptance Criteria

<Each `- [ ]` item contains a verifier hint: `(cargo test: <name>)`, `(grep: <pattern>)`, `(manual: <inverse check>)`, `(build: <warning/error>)`, `(benchmark: <metric vs baseline>)`, `(metric: <quantitative threshold>)`. Coin further tags as cases dictate: `(visual:)`, `(golden:)`, `(script:)`, `(log:)`. A missing hint is flagged by the reviewer, not rejected.>

- [ ] <Observable outcome 1> (cargo test: `<test_name>`)
- [ ] <Observable outcome 2> (grep: `<pattern>` returns zero hits)
- [ ] <Observable outcome 3> (manual: delete line X, verify build fails with `<error>`, restore)
- [ ] <Observable outcome 4> (build: zero new `dead_code` warnings on new fields)
- [ ] <Observable outcome 5> (cargo test: `<test_name>` — new test asserting the disabled-path branch)

---

## Testing

<Copy-pastable commands for the tester agent. No prose. Language-parameterize: the lines below are the Rust spelling.>

- `cargo test -p <crate>`
- `cargo test -p <crate> <test_filter>`
- `cargo check -p <crate> --tests 2>&1 | grep -i 'warning:' | wc -l`  # expected: 0
- <Any manual inverse check, with exact steps>

---

## Risks & Mitigations

<OPTIONAL. Delete the section entirely where there is no phase-specific risk beyond `Overview.md`.>

| Risk | Mitigation |
| ---- | ---- |
| <Specific phase risk> | <Specific concrete mitigation> |

---

## Dependencies

<One-line restatement of Depends On, plus what that prior phase produced that this phase consumes.>

---

## Deviations

<Empty at analysis time. The coder records any departure from Affected Files, Implementation Steps, or Acceptance Criteria here before invoking the reviewer.>

- None — phase executed as planned.
