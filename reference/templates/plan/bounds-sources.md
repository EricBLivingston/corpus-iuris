# Governance Bounds — Source Map

Bounds are not invented at phasing time. They are already written, in the plan folder's documents, as statements of what must not regress, what is out of scope, what was rejected, and what must hold at the end. Each table below converts those statements into bounds. Work the table matching the section being written (plan-wide for `Overview.md`, phase-scoped for a `Phase-X.md`), row by row, skipping nothing.

---

## Filters on every row's output

A row's conversion produces a candidate. Every bound traces to a specific, named element of the plan folder's documents; a limit tracing to no such element is invalid whatever its merits. Since nothing in those documents names a command, a tree state or a search, no bound names one either. Apply every filter below before writing anything into the list; a faithful quotation of the source clears none of them on its own.

**Shape.** An enumerated list, one limit per item, each stated so that a reader holding only that item and the produced work can decide whether it was crossed: a countable threshold, a named file, directory or symbol set, a construct that must not appear, an artifact that must exist. The form is one citation plus one question: `plan file X directs A. Bound: Was A and no more than A implemented?` A bound stating an outcome to reach is a Goal; these lists hold only limits not to cross. A bound turning on a qualifier that can be argued either way ("appropriately", "reasonable", "as needed", "where it makes sense") is no limit: restate it as the observable it stands for, or drop it. Quote the source's own words rather than paraphrasing them; a paraphrase drifts from what was actually agreed, and the drift is invisible by the time anyone checks.

**Authority.** The element cited is a decision the user ratified, durable project canon, or a measurement, never the source document's own elaboration however well it reasons, and never another phase file. Quoting elaboration faithfully launders it into a bound, and every fidelity check on the quotation passes clean. Give prohibitions the closer look: an invented value reads as a claim and invites challenge, an invented prohibition reads as discipline and gets praised for caution. Where a candidate traces no further than elaboration, it stays in the source file's body as a design note.

Qualifications travel into the bound's own text. A hedge promoted to an assertion is how an unverified claim becomes an enforced rule.

**Evaluability.** A governor evaluates each bound from the enumerated list alone, so the constraint's substance sits in the bound's own text and the citation carries its provenance. The subject must exist in this plan: a bound over an artifact no phase produces can never be crossed. An adjective no evidence decides leaves the bound; where it is load-bearing it becomes an Acceptance Criterion or an Open Question instead. These shapes fail as well:

- **An intent clause** ("no alternative is derived", "none removed as redundant") asks after motive, which no evidence settles, so it returns undetermined every run. State the observable; move the reason into the citation.
- **A bare ordinal** — "the columns listed in step 2". Restate the set by its defining property (∋4).
- **A by-number citation without its file** — `bound 7` written in a phase file resolves to that phase's own bound 7. Write `Overview.md bound 7`. Where a quoted source numbers its provisions on a different scheme, gloss that numbering inside the quotation.
- **Two bounds worded identically over different objects** collide into a false blocker, the plan-wide and phase-scoped lists being read as one. Name the object each governs.

**Satisfiability.** No bound may require what another forbids, across both lists and against the phase files' Acceptance Criteria. A pair that cannot both hold is a halt already scheduled for orchestration time.

**Self-execution.** Walk the phase's own Implementation Steps and Acceptance Criteria against the bound as if they had run. Required work includes what doctrine obliges and no step states, a ※10 sweep or a ※8 chain step among them (⊢4). A bound the phase's own required work crosses is unsatisfiable however sound its intent; the remedy is a narrower bound naming the sanctioned write, never a weakened step.

**Warrant.** Where the cited element says why the constraint must hold, that line travels with the bound, or the next author tidies the constraint away without ever seeing what it was holding. Where it says nothing, the bound carries nothing: a reason composed at phasing time traces to no element and is the defect this rule names.

An edit to a bound re-tests that bound against every filter, not only the one that failed: a repair that clears one routinely crosses another.

---

## Two ranks, not two scopes

The plan-wide table produces the bounds governing the whole orchestration, immutable once the plan starts; the phase-scoped table produces bounds subordinate to those, admissible only on the tests in `Phase-X-template.md` § Governance Bounds. Several source sections appear in both tables, and a phase-scoped row yields nothing where a plan-wide row already covered it.

A phase bound narrowing a plan-wide one earns its "and …" clause by adding a fact the Overview cannot state: which subset this phase touches. Where the Overview already protects the object under the same warrant, strike the clause.

**The gate.** A governor assays every bound set in the plan folder before orchestration begins, on the criteria `/orchestrate`'s Validate Boundaries step assembles: the filters above, plus two relational criteria it states there. A bound set that has not been through that assay is not ready to orchestrate.

### The author's own assay

Run the gate yourself before hand-off, per bound: the filters above, plus Non-conflicting and Non-restating per Overview/phase pair.

---

## Plan-wide sources

Read for limits no single phase can breach on its own.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `PRD.md` §3 Goals → **Non-goals** | each excluded area | "No <file, symbol, dependency, or behaviour> implementing <the excluded item> exists when the plan closes"; name the thing whose presence would disprove it |
| `PRD.md` §3 Goals → **Guardrails** | each metric that must not regress | "<metric> is at or below the figure the Baseline Capture recorded before Phase 1"; a guardrail without that recorded number is unverifiable, so capture it or drop the bound |
| `PRD.md` §3 Goals → **Output goal** | the qualifying tail, not the target | a goal reading "cut X by 30% *without raising the error rate*" carries a guardrail in that trailing clause; the target itself is a Goal, not a bound |
| `PRD.md` §4 Acceptance Criteria | criteria no single phase discharges | the criterion's standing form: what must be true continuously, across every phase, for it to hold at the end |
| `PRD.md` §5 Decisions & Open Questions | settled rows, and rows still open | a settled row forecloses its alternative: "<rejected approach> appears nowhere"; an open row bounds the build: "nothing turning on <question> is built before it is answered" |
| `Design.md` §1 Design spine | the one central invariant | the strongest plan-wide bound available; state it as the assertion that fails the moment it breaks |
| `Design.md` §4 Reuse vs. replace | every row | Reuse → "<component> is not forked, copied, or rewritten"; Replace → "<old component> and everything it owned (config keys, env prefixes, aliases, inbound pointers) are gone, not left standing beside the new" (⊨3) |
| `Design.md` §5 Resolved Decisions / Open Questions | every "Reject Y" ruling | "Y does not appear" |
| `Design.md` §6 Risks / Trade-offs | the Mitigation column, not the Risk column | the named mitigation is present in the produced work; a risk with no mitigation yields no bound |
| `Design.md` §7 Configuration & structure | the deliberate weight call | "<the heavier machinery the Design declined> is not introduced" |
| `Design.md` §8 Verification strategy | regression targets and measured baselines that span phases | "<measure> is unchanged from baseline"; a target one phase alone can hold belongs in that phase file |
| `Implementation.md` § Orientation | the conventions stated once, and any acceptable residual named "do not chase X" | a ratified residual is a bound against repairing it: "<X> is left as it is" |
| `Implementation.md` § No-List (close-out plans only) | every dropped finding | the No-list is that plan's out-of-scope statement, and the place scope re-enters: "no work item addresses <dropped finding>" |

---

## Phase-scoped sources

Read for limits that narrow to phase <N> alone.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `Implementation.md` § Affected Files, rows whose Phase column is <N> | the file set this phase may touch | "Every file modified by this phase is either named in this phase's Affected Files table, or is a file this phase writes under `plans/<plan-folder>/`"; populate that table from these rows first, so the bound and the table cannot drift apart. If the section was deleted as OPTIONAL, derive the set from this phase's own steps |
| `Implementation.md` § Phase <N> steps | the file and symbol each imperative step names | the tightest form the steps license: "No symbol in <file> other than <the named ones> changes signature" |
| `Implementation.md` § Risks & Mitigations | the Mitigation column of any risk belonging to this phase | the named mitigation is present in this phase's diff; a risk with no mitigation yields no bound |
| `Implementation.md` § Risks & Mitigations → **Rollback** | state git does not capture | "This phase creates no DB migration, system-file edit, or external-service change beyond the rollback steps listed there" |
| The phase file's § Scope → **Out of Scope** | every item | already a bound in prose; restate it as its observable: the file not touched, the symbol that does not appear |
| `Design.md` §2 Data model / Components | the responsibility this phase's component owns, and any invalid state its types encode | "<Component> does not take on <the adjacent responsibility>"; "<invalid state> is unrepresentable rather than runtime-guarded" |
| `Design.md` §3 <the mechanism> | the failure case the mechanism exists to guard against | "The guard against <failure case> is present and reachable on the path this phase builds" |
| `Design.md` §5 Resolved Decisions / Open Questions | rulings naming this phase's mechanism | "<rejected approach> appears nowhere in this phase's work" |
| `PRD.md` §4 Acceptance Criteria | the criterion this phase discharges | not the criterion itself (that is an Acceptance Criterion in the phase file) but its edge: what must not change while this phase satisfies it |

Write every path in the Affected Files bound repository-relative, the one path space the plan's file sets are stated in.

---

## When a source is missing

**A missing document is not a missing bound.** `Design.md` is the artifact most often absent, since the PRD's §6 Next Step routes some work straight to Implementation. When a row's source document does not exist, put that row's "Read it for" question to the artifacts that do (what a Design would have ratified usually sits in the PRD's Decisions table, the Implementation's Orientation, or the Implementation's phase steps), then write the bound and cite the source actually read.

A section deleted as OPTIONAL from a document that is present is the one case that genuinely yields nothing: record none and move on. A missing document is not that case, and never shortens either table.
