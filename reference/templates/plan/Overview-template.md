# <Plan Title>

<One-paragraph purpose statement. Why this plan exists and what the reader needs in 30 seconds.>
<Note: examples are Rust-oriented, but the template is language-agnostic: use Python or other language equivalents where appropriate.>

---

## Goals

1. <Observable outcome 1 — "System does X", not "System is better at X">
2. <Observable outcome 2>
3. <Observable outcome N>

## Non-Goals

Explicitly excluded scope. See Principle §2 (YAGNI) — non-goals pre-empt speculative scope creep.

- <Excluded scope item 1>
- <Excluded scope item 2>
- <Anything adjacent that might otherwise be assumed in-scope>

## Prerequisites

- <Link to calibration/research/hardware audit doc 1 — delete section if none>

## Plan-Wide Inventory (OPTIONAL)

<Delete if no fixed item list spans phases. When used, assign IDs (C1..Cn) and reference them in phase files.>

| ID | Item | Phase | Status |
| -- | ---- | ----- | ------ |

---

## Progress Summary

**Layout A — Linear sequential:**

| Phase | Name                   | Status      | Blocked By |
| ----- | ---------------------- | ----------- | ---------- |
| 1     | <Phase 1 short name>   | Not Started | -          |
| 2     | <Phase 2 short name>   | Not Started | Phase 1    |
| N     | <Phase N short name>   | Not Started | Phase N-1  |

**Layout B — Parallel sub-phase (use when phases have parallel tracks):**

| Phase | Track | Name                     | Status      | Blocked By |
| ----- | ----- | ------------------------ | ----------- | ---------- |
| 1a    | Rust  | <Phase 1 Rust task>      | Not Started | -          |
| 1b    | Rhai  | <Phase 1 Rhai task>      | Not Started | -          |
| 2     | —     | <Phase 2 short name>     | Not Started | 1a, 1b     |

Sub-numbering scheme is open (1a/1b, 1.1/1.2, 1-rust/1-rhai).

**Legend:** Not Started | In Progress | Complete | Blocked

---

## Architecture Overview (OPTIONAL)

<Delete if topology is unchanged from the prior plan or is not applicable. Keep to provide a shared mental model.>

```text
<source>           <transform stage>         <consumer>
  │                      │                       │
  ▼                      ▼                       ▼
<input type>   ──▶  <intermediate type>  ──▶  <output type>
                         │
                         ▼
                   <side effect / persistence>
```

### Component Ownership

| Component                   | Location                                | Phase |
| --------------------------- | --------------------------------------- | ----- |
| <Component A>               | <crate/path/to/file.rs>                 | 1     |
| <Component B>               | <crate/path/to/file.rs>                 | 2     |

---

## Cross-Cutting Concerns

<Content relevant to more than one phase. Anything here does NOT need to be repeated in phase files.>

### Principle Deviations

Record any pre-authorized deviations from project principles here (e.g., threading a parameter through a framework-constructed struct that cannot accept a context object). Non-deviating principles are assumed and not enumerated. If no deviations apply, write "None anticipated."

### Numerical & Performance Invariants (OPTIONAL)

<Delete if the plan has no numerical or performance requirements. When used, specify tolerance bounds, NaN/Inf handling policy, performance targets, and feature-flag matrices so every phase enforces them consistently. NaN/Inf handling is an application of Principle §6 (Fail Fast).>

- Tolerance bounds: <e.g., loss delta < 1e-4 between equivalent runs>
- NaN/Inf policy: <e.g., assert_finite in forward pass; training aborts on first NaN>
- Performance targets: <e.g., inference latency < 50 ms p99>
- Feature-flag matrix: <e.g., flags A+B must be tested together>

### Config Literal Audit (OPTIONAL, plan-level)
<List magic numbers, hardcoded strings, and untyped values the plan must eliminate or surface as config. See Principles §3 (Explicit Configuration) and §4 (Strict Typing — enums over magic strings). If this applies to just one phase, put the audit items in that phase file and delete this section.>

### Serde Defaults Audit (OPTIONAL, plan-level)
<List serde-defaulted fields that are unwarranted. See Principle §3 (Explicit Configuration). If this applies to just one phase, put the audit items in that phase file and delete this section.>

---

## Governance Bounds

<The limits the work must stay inside, where the limit spans more than one phase. A limit scoped to a single phase goes in that phase file's own Governance Bounds section instead — never in both. The two sections are read together as one list when a phase's produced work is tested against them, so a bound written once, in the right place, is checked everywhere it applies.>

<Shape. An enumerated list, one limit per item, each stated so that a reader holding only this list and the produced work can decide whether it was crossed: a countable threshold, a named file or directory set, a construct that must not appear, an artifact that must exist. Quote the source's own words rather than paraphrasing them; a paraphrase drifts from what was actually agreed, and the drift is invisible by the time anyone checks. The constraint's substance sits in the bound itself, a citation being provenance only — so no bare ordinal into another document.>

<A bound turning on "appropriately", "reasonable", "as needed", or "where it makes sense" is not checkable — restate it as the observable it stands for, or drop it. A bound stating an outcome to reach is a Goal, not a bound; this section holds only limits not to cross.>

<Whence they come. Bounds are not invented at phasing time — they are already written, in the documents sitting in this plan folder. Work the **Plan-wide sources** table in `bounds-sources.md`, beside this template, row by row: it names each source section, the question to put to it, and the bound that answer yields, and it rules on sources the plan folder does not have. The list below is that table's output passed through the filters it states; do not fill this section without working it.>

1. <Bound 1 — e.g. "No new dependency appears in any Cargo.toml." (PRD.md §3 Goals → Non-goals: "this work introduces no new crates")>
2. <Bound 2 — e.g. "`LegacyStore` and its `LEGACY_` env prefix are absent from the tree at plan close." (Design.md §4 Reuse vs. replace: "Replace")>
3. <Bound N>

---

## Risk Mitigations

| Risk                                          | Mitigation                                                                                          |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| <Specific failure mode>                       | <Specific concrete mitigation — not "review carefully">                                             |
| <Specific failure mode>                       | <Specific concrete mitigation>                                                                      |
| <Cross-phase invariant that could be broken>  | <How it is preserved, and which phase owns the check>                                               |

---

## Testing Strategy

<Cross-cutting testing policy. Per-phase commands go in phase files.>

- Baseline Capture: Record any pre-existing test failures BEFORE Phase 1 starts.
- <e.g., "Unit tests only — no full training pipelines per MEMORY.md">
- <e.g., "GPU-dependent tests marked `#[ignore]`; CI runs them separately">

---

## Related Documents

- <One bullet per phase file, shaped `[Phase-N.md](./Phase-N.md) - short name`.>
- <Any sibling doc still live after the Sweep. Not the source specs this Overview was built from — those are archived, and the Sweep strips links to them.>
