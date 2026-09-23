# Governance Bounds — Source Map

Bounds are already written before phasing begins, in the plan folder's documents, as statements of what must not regress, what is out of scope, what was rejected, and what must obtain at the end. Work the table matching the section being written (plan-wide for `Overview.md`, phase-scoped for a `Phase-X.md`), row by row, skipping nothing.

## Filters on every row's output

Converting a row produces a candidate rather than a bound. Every bound traces to a specific, named element of the plan folder's documents; a limit tracing to no such element is invalid whatever its merits. Nothing in those documents names a command, a tree state or a search, so no bound names one either. Apply every filter below before writing anything into the list; a faithful quotation of the source clears none of them on its own.

**Shape.** An enumerated list, one limit per item, each stated so that a reader possessing only that item and the produced work can decide whether it was crossed: a countable threshold, a named file, directory or symbol set, a construct that must not appear, an artifact that must exist. One citation plus one question: `plan file X directs A. Bound: Was A and no more than A implemented?` A bound stating an outcome to achieve is a Goal. A bound turning on a qualifier arguable either way ("appropriately", "reasonable", "as needed", "where it makes sense") is no limit: restate it as the observable it stands for, or drop it. Quote the source's own words; a paraphrase drifts from what was agreed, and the drift is invisible by the time anyone checks. Qualifications travel into the bound's own text: a hedge promoted to an assertion is how an unverified claim becomes an enforced rule.

**Authority.** The element cited is a decision the user ratified, durable project canon, or a measurement, never the source document's own elaboration however well it reasons, and never another phase file. Quoting elaboration faithfully launders it into a bound past every fidelity check. Scrutinize prohibitions hardest: an invented value reads as a claim and invites challenge, an invented prohibition reads as discipline and gets praised for caution. A candidate tracing no further than elaboration stays in the source file's body as a design note.

**Evaluability.** A governor evaluates each bound from the enumerated list alone, so the constraint's substance sits in the bound's own text and the citation bears its provenance. The subject must exist in this plan: a bound over an artifact no phase produces can never be crossed. An adjective no evidence decides leaves the bound; where the plan depends on it, it becomes an Acceptance Criterion or an Open Question instead. These shapes fail as well:

- **An intent clause** ("no alternative is derived", "none removed as redundant") asks after motive, which no evidence settles, so it returns undetermined every run. State the observable; move the reason into the citation.
- **A bare ordinal** — "the columns listed in step 2". Restate the set by its defining property (∋4).
- **A by-number citation without its file** — `bound 7` written in a phase file resolves to that phase's own bound 7. Write `Overview.md bound 7`. Where a quoted source numbers its provisions on a different scheme, gloss that numbering inside the quotation.
- **Two bounds worded identically over different objects** collide into a false blocker, the plan-wide and phase-scoped lists being read as one. Name the object each binds.

**Satisfiability.** No bound may require what another forbids, across both lists and against the phase files' Acceptance Criteria. A pair that cannot both obtain is a halt already scheduled for orchestration time.

**Self-execution.** Walk the phase's own Implementation Steps and Acceptance Criteria against the bound as if they had run. Required work includes what doctrine obliges and no step states, a ※10 sweep or a ※8 chain step among them (⊢4). A bound the phase's own required work crosses is unsatisfiable however sound its intent; the remedy is a narrower bound naming the sanctioned write, never a weakened step.

**Warrant.** Where the cited element says why the constraint must obtain, that line travels with the bound, or the next author tidies the constraint away without ever seeing what it was keeping. Where it says nothing, the bound contains nothing: a reason composed at phasing time traces to no element and is the defect this rule names.

An edit to a bound re-tests it against every filter, not only the one that failed: a repair that clears one routinely crosses another.

## Two ranks

The plan-wide table produces the bounds binding the whole orchestration, immutable once the plan starts; the phase-scoped table produces bounds subordinate to those, admissible only on the tests in `Phase-X-template.md` § Governance Bounds. Several source sections appear in both tables, and a phase-scoped row yields nothing where a plan-wide row already covered it.

A phase bound narrowing a plan-wide one earns its "and …" clause by adding a fact the Overview cannot state: which subset this phase touches. Where the Overview already protects the object under the same warrant, strike the clause.

**The gate.** Before orchestration begins, a governor assays every bound set in the plan folder on the criteria `/orchestrate`'s Validate Boundaries step assembles: the filters above, plus the relational pair Non-conflicting and Non-restating, reported per Overview/phase pair. Run the same criteria yourself, per bound, before hand-off; a set that skipped the assay is not ready to orchestrate.

## Plan-wide sources

Read for limits no single phase can breach on its own.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `PRD.md` §3 Goals → **Non-goals** | each excluded area | "No <file, symbol, dependency, or behaviour> implementing <the excluded item> exists when the plan closes"; name the thing whose presence would disprove it |
| `PRD.md` §3 Goals → **Guardrails** | each metric that must not regress | "<metric> is at or below the figure the Baseline Capture recorded before Phase 1"; a guardrail without that recorded number is unverifiable, so capture it or drop the bound |
| `PRD.md` §3 Goals → **Output goal** | the qualifying tail | a goal reading "cut X by 30% *without raising the error rate*" contains a guardrail in that trailing clause; the target itself is a Goal |
| `PRD.md` §4 Acceptance Criteria | criteria no single phase discharges | the criterion's standing form: what must be true continuously, across every phase, for it to obtain at the end |
| `PRD.md` §5 Decisions & Open Questions | settled rows, and rows still open | a settled row forecloses its alternative: "<rejected approach> appears nowhere"; an open row bounds the build: "nothing turning on <question> is built before it is answered" |
| `Design.md` §1 Design spine | the one central invariant | the strongest plan-wide bound available; state it as the assertion that fails the moment it breaks |
| `Design.md` §4 Reuse vs. replace | every row | Reuse → "<component> is not forked, copied, or rewritten"; Replace → "<old component> and everything it owned (config keys, env prefixes, aliases, inbound pointers) are gone" (⊨3) |
| `Design.md` §5 Resolved Decisions / Open Questions | every "Reject Y" ruling | "Y does not appear" |
| `Design.md` §6 Risks / Trade-offs | each named mitigation | the named mitigation is present in the produced work; a risk with no mitigation yields no bound |
| `Design.md` §7 Configuration & structure | the deliberate weight call | "<the heavier machinery the Design declined> is not introduced" |
| `Design.md` §8 Verification strategy | regression targets and measured baselines that span phases | "<measure> is unchanged from baseline"; a target one phase alone can meet belongs in that phase file |
| `Implementation.md` § Orientation | the conventions stated once, and any ratified residual named "do not chase X" | a ratified residual is a bound against repairing it: "<X> is left as it is" |
| `Implementation.md` § No-List (close-out plans only) | every dropped finding | the No-list is that plan's out-of-scope statement, and the place scope re-enters: "no work item addresses <dropped finding>" |

## Phase-scoped sources

Read for limits that narrow to phase <N> alone.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `Implementation.md` § Affected Files, rows whose Phase column is <N> | the file set this phase may touch | "Every file modified by this phase is either named in this phase's Affected Files table, or is a file this phase writes under `plans/<plan-folder>/`"; populate that table from these rows first, so the bound and the table cannot drift apart. Section deleted as OPTIONAL → derive the set from this phase's own steps |
| `Implementation.md` § Phase <N> steps | the file and symbol each imperative step names | the tightest form the steps license: "No symbol in <file> other than <the named ones> changes signature" |
| `Implementation.md` § Risks & Mitigations | the Mitigation column of any risk belonging to this phase | the named mitigation is present in this phase's diff; a risk with no mitigation yields no bound |
| `Implementation.md` § Risks & Mitigations → **Rollback** | state git does not capture | "This phase creates no DB migration, system-file edit, or external-service change beyond the rollback steps listed there" |
| The phase file's § Scope → **Out of Scope** | every item | already a bound in prose; restate it as its observable: the file not touched, the symbol that does not appear |
| `Design.md` §2 Data model / Components | the responsibility this phase's component owns, and any invalid state its types encode | "<Component> does not take on <the adjacent responsibility>"; "<invalid state> is unrepresentable rather than runtime-guarded" |
| `Design.md` §3 <the mechanism> | the failure case the mechanism exists to guard against | "The guard against <failure case> is present and reachable on the path this phase builds" |
| `Design.md` §5 Resolved Decisions / Open Questions | rulings naming this phase's mechanism | "<rejected approach> appears nowhere in this phase's work" |
| `PRD.md` §4 Acceptance Criteria | the criterion this phase discharges | its edge: what must not change while this phase satisfies it; the criterion itself is an Acceptance Criterion in the phase file |

Write every path in the Affected Files bound repository-relative, the one path space the plan's file sets are stated in.

## When a source is missing

A missing document is not a missing bound. `Design.md` is most often the absent one, since the PRD's §6 Next Step routes some work straight to Implementation. Where a row's source document does not exist, put that row's "Read it for" question to the artifacts that do (what a Design would have ratified usually sits in the PRD's Decisions table, the Implementation's Orientation, or its phase steps), then write the bound and cite the source actually read.

A section deleted as OPTIONAL from a document that is present is the one case that genuinely yields nothing: record none and move on. A missing document never shortens either table.
