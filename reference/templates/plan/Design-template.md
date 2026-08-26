# Design — <Title>

> **Advisory template.** This file is connective-tissue guidance, not a rigid form. The four-part spine below (Orientation, §1 Design spine, §2 Data model/Components, Verification) is expected in every Design. Every other section is OPTIONAL. Authors are **expected** to rename §3 to their actual hard part and to add or delete sections freely — the skeleton is a menu, not a cap. The strongest Design docs in the corpus earned their shape by renaming the central section to the specific thing that makes this work hard. Do **not** add a Table of Contents, a Conclusion, or a Future Enhancements section — these are the cruft the strongest Designs omit: a Conclusion merely restates the Orientation, and Future Enhancements speculates against §2 (YAGNI).

**Status:** <Draft | Ratified — ready for Implementation>
**Last updated:** YYYY-MM-DD
**Routed from:** <PRD.md §N link — delete if no PRD>

<One-paragraph orientation: what this Design specifies and what it does NOT. It specifies the "how" at architecture level, not the line-level build. State any ratifications, language/toolchain decisions, or assumptions a reader needs to orient in 30 seconds.>

---

## 1. Design spine

<The load-bearing idea in 1–3 sentences. State the ONE central invariant or insight the rest of the design serves — the thing that, if wrong, unravels everything else. Then a text diagram of the data or control flow. This is the highest-signal section; do not skip it.>

```text
<source>             <transform / decision>          <consumer>
  │                          │                           │
  ▼                          ▼                           ▼
<input type>  ──▶  <intermediate type / step>  ──▶  <output type>
                             │
                             ▼
                   <side effect / persistence>
```

## 2. Data model / Components

<Typed models and/or component responsibilities. Use Pydantic/dataclass in Python projects; struct/enum/trait in Rust projects — the substance is language-invariant even when the syntax differs. Where a type carries a rejection or invalid state, encode the *reason* in the type rather than in a comment or runtime guard. For a pure refactor with no new types, describe the components touched and their responsibilities instead. This section is CORE — it is the substance of a Design.>

## 3. <The mechanism> (rename to the actual hard part)

<**Rename this heading** to what this work is actually about: "Clustering algorithm", "Migration strategy", "Dual-logger API", "Streaming final-DF strategy" — whatever the actual hard part is. This is the single highest-value move per the cross-project research; the strongest designs in the corpus all did it.>

<Show the rule, algorithm, or pseudocode and the failure case it guards against. Explain how edge cases and invalid paths are handled. Strong designs make this the longest section.>

## 4. Reuse vs. replace (OPTIONAL)

<Use when the work touches existing code and the choice to reuse or replace is non-obvious. Delete for greenfield work with nothing to reuse.>

| Component | Reuse / Replace | Notes |
| --------- | --------------- | ----- |
| <Name> | <Reuse \| Replace> | <One-line rationale> |

## 5. Resolved Decisions / Open Questions (OPTIONAL)

<Use when the PRD routed open questions here, or when design choices required a ruling. High signal when present — keep. Delete if the author resolved everything unilaterally and silently. Scope: architecture / design decisions only — product and requirement decisions live in the PRD's Decisions table, not here.>

**Resolved:**

- <Imperative title — "Use X" / "Reject Y"> — <ruling>. Rule: <§N or rationale>. Consequences: <what gets easier or harder as a result>. Ratified: <YYYY-MM-DD>.

**Open:**

- <Question> — <what must be settled before implementation can proceed>

## 6. Risks / Trade-offs (OPTIONAL)

<Use when a real failure mode or a deliberate trade-off exists. Delete if there are no non-obvious risks — do NOT pad with hypotheticals nobody will verify.>

| Risk | Mitigation |
| ---- | ---------- |
| <Specific failure mode> | <Specific concrete mitigation — not "review carefully"> |

## 7. Configuration & structure (OPTIONAL)

<Use when the work adds config fields, or when you made a deliberate weight call — for example, using a lightweight `ScriptConfig` rather than full `AppConfig`/`AppContext`. Name the call and why. Delete if config is unchanged.>

## 8. Verification strategy

<How this design will be proven correct. The invariant assertions, measured baselines, regression targets, and canonical fixture cases — each tracing to the PRD acceptance criterion (§4) or guardrail (§3) it discharges. **CORE** — but it must carry concrete checks: counts, greps, named fixtures, or runnable commands with expected output. Empty "write unit tests" stubs are not acceptable here; they are the only failure mode observed in otherwise-strong Design docs.>

- <Invariant assertion: e.g., `assert len(result) == N` where N is derived from input fixture>
- <Regression target: e.g., row-count preserved across refactor — verify with `grep -c` on output>
- <Named fixture / test: e.g., `test_clustering_deduplicates_exact_duplicates` in `tests/test_clustering.py`>

## 9. Collaborator Feedback (OPTIONAL)

<Gemini or Codex second-opinion summary, if consulted. Delete if none.>

## 10. Related Documents (OPTIONAL)

<Delete if standalone.>

- <`[Implementation.md](path)`> — execution plan for this Design
- <`[PRD.md](path)`> — product requirements that prompted this work
- <Any sibling plans, prior Designs, or Background research>
