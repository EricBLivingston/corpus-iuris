# <Plan Title>

<One-paragraph purpose statement: why this plan exists and what the reader needs in 30 seconds.>

---

## Goals

1. <Observable outcome 1 — "System does X", not "System is better at X">
2. <Observable outcome 2>
3. <Observable outcome N>

## Non-Goals

Explicitly excluded scope. See Principle §2 (YAGNI).

- <Excluded scope item 1>
- <Excluded scope item 2>
- <Anything adjacent that might otherwise be assumed in-scope>

## Prerequisites

- <Link to calibration / research / hardware-audit doc — delete section if none>

## Plan-Wide Inventory (OPTIONAL)

<Delete if no fixed item list spans phases. When used, assign IDs (C1..Cn) and reference them in phase files.>

| ID | Item | Phase | Status |
| ---- | ---- | ---- | ---- |

---

## Progress Summary

**Layout A — Linear sequential:**

| Phase | Name | Status | Blocked By |
| ---- | ---- | ---- | ---- |
| 1 | <Phase 1 short name> | Not Started | - |
| 2 | <Phase 2 short name> | Not Started | Phase 1 |
| N | <Phase N short name> | Not Started | Phase N-1 |

**Layout B — Parallel sub-phase (use when phases have parallel tracks):**

| Phase | Track | Name | Status | Blocked By |
| ---- | ---- | ---- | ---- | ---- |
| 1a | <Track A> | <Phase 1 track-A task> | Not Started | - |
| 1b | <Track B> | <Phase 1 track-B task> | Not Started | - |
| 2 | — | <Phase 2 short name> | Not Started | 1a, 1b |

Sub-numbering scheme is open (1a/1b, 1.1/1.2, 1-rust/1-rhai).

**Legend:** Not Started | In Progress | Complete | Blocked

---

## Architecture Overview (OPTIONAL)

<Delete if topology is unchanged from the prior plan or does not apply.>

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

| Component | Location | Phase |
| ---- | ---- | ---- |
| <Component A> | <path/to/file> | 1 |
| <Component B> | <path/to/file> | 2 |

---

## Cross-Cutting Concerns

<Content relevant to more than one phase. Anything here is not repeated in phase files.>

### Principle Deviations

Pre-authorized deviations from project principles (e.g. threading a parameter through a framework-constructed struct that cannot accept a context object). Non-deviating principles are assumed and not enumerated. If none apply, write "None anticipated."

### Numerical & Performance Invariants (OPTIONAL)

<Delete if the plan contains no numerical or performance requirement. When used, state tolerance bounds, NaN/Inf policy, performance targets, and feature-flag matrices, so every phase enforces them consistently.>

- Tolerance bounds: <e.g. loss delta < 1e-4 between equivalent runs>
- NaN/Inf policy: <e.g. assert_finite in forward pass; training aborts on first NaN>
- Performance targets: <e.g. inference latency < 50 ms p99>
- Feature-flag matrix: <e.g. flags A+B must be tested together>

### Config Literal Audit (OPTIONAL, plan-level)

<Magic numbers, hardcoded strings, and untyped values the plan must eliminate or surface as config. See Principles §3 (Explicit Configuration) and §4 (Strict Typing — enums over magic strings). Where this applies to one phase only, put the audit items in that phase file and delete this section.>

### Serde Defaults Audit (OPTIONAL, plan-level)

<Serde-defaulted fields that are unwarranted. See Principle §3 (Explicit Configuration). Where this applies to one phase only, put the audit items in that phase file and delete this section.>

---

## Governance Bounds

The limits below apply for the whole orchestration: no phase overrides them, and they bind every phase's produced work whether or not that phase mentions them. A limit scoped to a single phase goes in that phase file's own Governance Bounds section instead, never in both; the two sections are read together as one list. They are amended only through ※12.

<Fill from the Plan-wide sources table in `bounds-sources.md`, beside this template, row by row, through the filters it states. Do not fill this section without working it.>

1. <Bound 1 — e.g. `PRD.md §3 Non-goals` directs that this work introduces no new crates, so no crate is added to a runtime dependency table of any `Cargo.toml`.>
2. <Bound 2 — e.g. `Design.md §4 Reuse vs. replace` directs Replace for `LegacyStore`, so `LegacyStore` and its `LEGACY_` env prefix are absent from the tree at plan close. Its warrant: a replacement leaving the old path callable is not a replacement (⊨3).>
3. <Bound N — the same parts: the citation, what it directs with the observable inline, and the cited element's own warrant where it states one.>

### Amendments

<Empty until a bound above is amended through ※12; leave the heading standing. One entry per grant: the bound, the statement, and the text it replaced.>

---

## Risk Mitigations

| Risk | Mitigation |
| ---- | ---- |
| <Specific failure mode> | <Specific concrete mitigation — not "review carefully"> |
| <Cross-phase invariant that could be broken> | <How it is preserved, and which phase owns the check> |

---

## Testing Strategy

<Cross-cutting testing policy. Per-phase commands go in phase files.>

- Baseline Capture: record any pre-existing test failures before Phase 1 starts.
- <e.g. "Unit tests only: no full training pipelines per MEMORY.md">
- <e.g. "GPU-dependent tests marked `#[ignore]`; CI runs them separately">

---

## Related Documents

- <One bullet per phase file, shaped `[Phase-N.md](./Phase-N.md) - short name`.>
- <Any sibling doc still live after the Sweep. Not the source specs this Overview was built from: those are archived, and the Sweep strips links to them.>
