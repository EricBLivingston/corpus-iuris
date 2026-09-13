# Design — <Title>

> Orientation, §1, §2 and §8 are expected in every Design; every other section is optional. Rename §3 to the actual hard part, and add or delete sections freely. No Table of Contents, Conclusion, or Future Enhancements: a Conclusion restates the Orientation, and Future Enhancements speculates against §2 (YAGNI).

**Status:** <Draft | Ratified — ready for Implementation>
**Routed from:** <PRD.md §N link — delete if no PRD>

<One-paragraph orientation: what this Design specifies and what it does not. The "how" at architecture level, not the line-level build. State the ratifications, language and toolchain decisions, and assumptions a reader needs to orient in 30 seconds.>

---

## 1. Design spine

<The load-bearing idea in 1–3 sentences: the ONE central invariant or insight the rest of the design serves, the thing that unravels everything else if it is wrong. Then a text diagram of the data or control flow.>

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

<Typed models and component responsibilities, in the project's own language. Where a type carries a rejection or an invalid state, encode the reason in the type rather than in a comment or a runtime guard. For a pure refactor with no new types, describe the components touched and their responsibilities instead.>

## 3. <The mechanism> (rename to the actual hard part)

<Rename this heading to what the work is actually about: "Clustering algorithm", "Migration strategy", "Dual-logger API", "Streaming final-DF strategy". Show the rule, algorithm, or pseudocode; the failure case it guards against; how edge cases and invalid paths are handled. Usually the longest section.>

## 4. Reuse vs. replace (OPTIONAL)

<Use when the work touches existing code and the reuse-or-replace call is non-obvious.>

| Component | Reuse / Replace | Notes |
| ---- | ---- | ---- |
| <Name> | <Reuse \| Replace> | <One-line rationale> |

## 5. Resolved Decisions / Open Questions (OPTIONAL)

<Use when the PRD routed open questions here, or when a design choice required a ruling. Architecture and design decisions only; product and requirement decisions stay in the PRD's §5 table.>

**Resolved:**

- <Imperative title — "Use X" / "Reject Y"> — <ruling>. Rule: <§N or rationale>. Consequences: <what gets easier or harder as a result>.

**Open:**

- <Question> — <what must be settled before implementation can proceed>

## 6. Risks / Trade-offs (OPTIONAL)

<A real failure mode or a deliberate trade-off. Delete rather than pad with hypotheticals nobody will verify.>

| Risk | Mitigation |
| ---- | ---- |
| <Specific failure mode> | <Specific concrete mitigation — not "review carefully"> |

## 7. Configuration & structure (OPTIONAL)

<Config fields the work adds, or a deliberate weight call: e.g. a lightweight `ScriptConfig` rather than a full `AppConfig`/`AppContext` (§14). Name the call and why.>

## 8. Verification strategy

<How this design is proven correct: invariant assertions, measured baselines, regression targets and canonical fixture cases, each tracing to the PRD acceptance criterion (§4) or guardrail (§3) it discharges. Concrete checks only: counts, greps, named fixtures, or runnable commands with expected output.>

- <Invariant assertion: e.g. `assert len(result) == N`, N derived from the input fixture>
- <Regression target: e.g. row count preserved across the refactor; verify with `grep -c` on output>
- <Named fixture / test: e.g. `test_clustering_deduplicates_exact_duplicates` in `tests/test_clustering.py`>

## 9. Collaborator Feedback (OPTIONAL)

<Peritus second-opinion summary, where one was consulted.>

## 10. Related Documents (OPTIONAL)

- <`[Implementation.md](path)`> — execution plan for this Design
- <`[PRD.md](path)`> — product requirements that prompted this work
- <Sibling plans, prior Designs, Background research>
