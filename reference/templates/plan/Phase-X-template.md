# Phase <N>: <Phase Title>

**Status:** Not Started
**Depends On:** <Phase N-1 \| None>
**Blocking:** <Phase N+1 \| ->

<Note: examples are Rust-oriented, but the template is language-agnostic: use Python or other language equivalents where appropriate.>

---

## Goals

1. <Observable outcome 1 for THIS phase only — do not restate plan-level goals>
2. <Observable outcome 2>
3. <Observable outcome N>

---

## Scope

### In Scope

- <Specific change 1 — should align 1:1 with an entry in Affected Files>
- <Specific change 2>
- <Specific change N>

### Out of Scope

See Principle §2 (YAGNI) — name adjacent work only if excluding it removes real ambiguity.

- <Adjacent change that could be mistaken for in-scope>
- <Deferred follow-up explicitly left for a later phase>
- <Item that belongs to another plan entirely>

---

## Affected Files

| File                                     | Change                                                          |
| ---------------------------------------- | --------------------------------------------------------------- |
| <crate/path/to/file.rs>                  | <One-line description of the specific change>                   |
| <crate/path/to/other.rs>                 | <One-line description of the specific change>                   |
| <crate/path/tests.rs>                    | <One-line description of the test-side change>                  |
| <config/file.toml>                       | <One-line description of the config/fixture change>             |

---

## Implementation Steps

1. <Step 1: concrete, reviewable action>
2. <Step 2: concrete action — small enough to stop here and leave tree in a reviewable state>
3. <Step 3: concrete action>
4. <Step N: concrete action>
5. **Flip phase status (mandatory tail step).** After all Acceptance Criteria pass and the implementation summary is written, edit this phase file's `**Status:** Not Started` line to `**Status:** Complete`, and update the corresponding row in the plan's `Overview.md` Progress Summary table from `Not Started` to `Complete`. Each phase reconciles its own status; downstream verification phases must not have to do it. Do this before invoking the reviewer.

<Config Literal Audit and Serde Defaults Audit now live in Overview-template.md's Cross-Cutting Concerns. Lift into this file only when the analyzer determines the audit is phase-local.>

### Reverse Dependency Audit

<MANDATORY when this phase changes a struct signature, field, enum variant, or public API. Delete this subsection otherwise. This is the call-site sweep that makes Principle §1 (No Backward Compatibility) safe — the break must be complete, not partial.>

<Replace `<StructName>` and `<TraitName>` with the actual symbol names before running.>

- [ ] `rg '<StructName>'` — grep for direct references across the workspace
- [ ] `rg 'impl.*<TraitName>'` — grep for trait implementors that must be updated
- [ ] Audit test call sites under the affected crate for stale usages

### Open Questions (OPTIONAL)

<Delete if the analyzer resolved all design choices unilaterally.>

- <Unresolved design question>

---

## Acceptance Criteria

<Every `- [ ]` item should include a verifier hint: e.g., `(cargo test: <name>)`, `(grep: <pattern>)`, `(manual: <inverse check>)`, `(build: <warning/error>)`, `(benchmark: <metric vs baseline>)`, or `(metric: <quantitative threshold>)`. Coin additional tags as cases dictate, e.g. `(visual:)`, `(golden:)`, `(script:)`, `(log:)`. Reviewer will flag missing hints — not reject the phase.>

- [ ] <Observable outcome 1> (cargo test: `<test_name>`)
- [ ] <Observable outcome 2> (grep: `<pattern>` returns zero hits)
- [ ] <Observable outcome 3> (manual: delete line X, verify build fails with `<error>`, restore)
- [ ] <Observable outcome 4> (build: zero new `dead_code` warnings on new fields)
- [ ] <Observable outcome 5> (cargo test: `<test_name>` — new test asserting the disabled-path branch)

---

## Governance Bounds

<The limits scoped to THIS phase — not outcomes to reach (those are Goals and Acceptance Criteria above), but lines this phase's work must not cross. The plan-wide bounds carried in `Overview.md` are immutable and already govern this phase's produced work whether or not this file mentions them; the two sections are read together as one list when that work is tested against them. If this phase adds no limit of its own, write "None beyond Overview.md.">

<Admissibility. A bound belongs in this list only if every test below holds. Fail one and it does not go in.>

1. **It does not conflict with the Overview's bounds.** It may narrow one, or apply one more precisely to this phase's work. It may not widen one, add an exception to one, or soften a verifier.
2. **It is not a restatement, subset, or tautology of an Overview bound.** Where an Overview bound already fully handles the thing, the phase bound is deleted — not reworded, not narrowed for form's sake.
3. **It cites its authority**, and that authority is a source document or project canon. Never another phase file.
4. **It carries its own verifier**, its false-positive trap where one exists, and its warrant — one line on why this constraint must hold.

<Test 1's failure mode looks like diligence. A bound that widens an Overview bound, or carves an exception out of one, reads as careful scoping of this phase; nothing in its own wording gives it away. Test it against the Overview's text, never against how sensible it sounds standing alone.>

<Shape. An enumerated list, one limit per item, each stated so that crossing it is checkable against what this phase actually produced rather than a matter of opinion: a countable threshold, a named file or symbol set, a construct that must not appear, an artifact that must exist. Quote the source's own words rather than paraphrasing them; a paraphrase drifts from what was actually agreed, and the drift is invisible by the time anyone checks. The constraint's substance sits in the bound itself, a citation being provenance only — so no bare ordinal into another document.>

<No hedging adverbs. A limit a reader could argue either way is not a limit: restate it as the observable it stands for, or drop it.>

<Whence they come. This phase's bounds are already written down, in the plan folder's source documents. Work the **Phase-scoped sources** table in `bounds-sources.md`, beside this template, row by row: it names each source section, the question to put to it, and the bound that answer yields, and it rules on sources the plan folder does not have. The list below is that table's output passed through the filters it states; do not fill this section without working it.>

1. <Bound 1 — e.g. "Every file modified by this phase is named in its Affected Files table, or written under `plans/<plan-folder>/`." Source: Implementation.md § Affected Files, Phase <N> rows. Verify: `git diff --name-only <baseline>` — bare, not `..HEAD`, which ignores the uncommitted tree — read against the table. Trap: none; the permitted set is enumerable from the table. Warrant: a file outside the table means the plan was incomplete or the coder left scope.>
2. <Bound 2 — e.g. "No method is added to, removed from, or re-signed on the public trait `<TraitName>`." Source: Design.md §5 Resolved Decisions ("Reject widening the trait"). Verify: the trait's method list at baseline against phase close. Trap: a defaulted addition crosses this bound, though it compiles for existing implementors. Warrant: the trait surface is a ratified decision.>
3. <Bound N — the same parts, Trap included or explicitly waived.>

---

## Testing

<Copy-pastable commands the tester agent will run. No prose. Language-parameterize — do not hardcode one toolchain; the lines below are the Rust spelling.>

- `cargo test -p <crate>`
- `cargo test -p <crate> <test_filter>`
- `cargo check -p <crate> --tests 2>&1 | grep -i 'warning:' | wc -l`  # expected: 0
- <Any manual inverse check, with exact steps>

---

## Risks & Mitigations

| Risk                                   | Mitigation                                                          |
| -------------------------------------- | ------------------------------------------------------------------- |
| <Specific phase risk>                  | <Specific concrete mitigation>                                      |

<OPTIONAL. Delete the section entirely if zero phase-specific risks beyond Overview.md.>

---

## Dependencies

<One-line restatement of Depends On + what that prior phase produced that this phase consumes.>

---

## Deviations

<Pre-authorized section for the coder to fill in during implementation. Empty at analysis time. If the coder deviates from Affected Files, Implementation Steps, or Acceptance Criteria for any reason, record it here before invoking the reviewer.>

- None — phase executed as planned.
