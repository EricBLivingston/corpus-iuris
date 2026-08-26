# Governance Bounds — Source Map

Bounds are not invented at phasing time. They are already written, in the documents sitting in the plan folder, as statements of what must not regress, what is out of scope, what was rejected, and what must hold at the end. Each table below converts those statements into bounds: a source section, the question to put to it, and the bound that answer yields.

Work whichever table matches the section being written — the plan-wide table for `Overview.md`, the phase-scoped table for a `Phase-X.md` — row by row, and skip nothing.

---

## Plan-wide sources

Read for limits no single phase can breach on its own.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `PRD.md` §3 Goals → **Non-goals** | each excluded area | "No <file, symbol, dependency, or behaviour> implementing <the excluded item> exists when the plan closes" — name the thing whose presence would disprove it |
| `PRD.md` §3 Goals → **Guardrails** | each metric that must not regress | "<metric> is at or below the figure the Baseline Capture recorded before Phase 1" — a guardrail without that recorded number is unverifiable, so capture it or drop the bound |
| `PRD.md` §3 Goals → **Output goal** | the qualifying tail, not the target | a goal reading "cut X by 30% *without raising the error rate*" carries a guardrail in that trailing clause; the target itself is a Goal, not a bound |
| `PRD.md` §4 Acceptance Criteria | criteria no single phase discharges | the criterion's standing form: what must be true continuously, across every phase, for it to hold at the end |
| `PRD.md` §5 Decisions & Open Questions | settled rows, and rows still open | a settled row forecloses its alternative — "<rejected approach> appears nowhere"; an open row bounds the build — "nothing turning on <question> is built before it is answered" |
| `Design.md` §1 Design spine | the one central invariant | the strongest plan-wide bound available; state it as the assertion that fails the moment it breaks |
| `Design.md` §4 Reuse vs. replace | every row | Reuse → "<component> is not forked, copied, or rewritten"; Replace → "<old component> and everything it owned — config keys, env prefixes, aliases, inbound pointers — are gone, not left standing beside the new" (⊨3) |
| `Design.md` §5 Resolved Decisions / Open Questions | every "Reject Y" ruling | "Y does not appear", paired with the grep or file check that shows it |
| `Design.md` §6 Risks / Trade-offs | the Mitigation column, not the Risk column | the named mitigation is present in the produced work — a risk with no mitigation yields no bound |
| `Design.md` §7 Configuration & structure | the deliberate weight call | "<the heavier machinery the Design declined> is not introduced" |
| `Design.md` §8 Verification strategy | regression targets and measured baselines that span phases | "<measure> is unchanged from baseline"; a target one phase alone can hold belongs in that phase file |
| `Implementation.md` § Orientation | the conventions stated once, and any acceptable residual named "do not chase X" | a ratified residual is a bound against repairing it: "<X> is left as it is" |
| `Implementation.md` § No-List (close-out plans only) | every dropped finding | the No-list is that plan's out-of-scope statement, and the place scope re-enters — "no work item addresses <dropped finding>" |

---

## Phase-scoped sources

Read for limits that narrow to phase <N> alone.

| Source | Read it for | The bound it yields |
| ---- | ---- | ---- |
| `Implementation.md` § Affected Files, rows whose Phase column is <N> | the file set this phase may touch | "Every file modified by this phase is either named in this phase's Affected Files table, or is a file this phase writes under `plans/<plan-folder>/`" — populate that table from these rows first, so the bound and the table cannot drift apart. If the section was deleted as OPTIONAL, derive the set from this phase's own steps |
| `Implementation.md` § Phase <N> steps | the file and symbol each imperative step names | the tightest form the steps license: "No symbol in <file> other than <the named ones> changes signature" |
| `Implementation.md` § Risks & Mitigations | the Mitigation column of any risk belonging to this phase | the named mitigation is present in this phase's diff — a risk with no mitigation yields no bound |
| `Implementation.md` § Risks & Mitigations → **Rollback** | state git does not capture | "This phase creates no DB migration, system-file edit, or external-service change beyond the rollback steps listed there" |
| The phase file's § Scope → **Out of Scope** | every item | already a bound in prose — restate it as its observable: the file not touched, the symbol that does not appear |
| `Design.md` §2 Data model / Components | the responsibility this phase's component owns, and any invalid state its types encode | "<Component> does not take on <the adjacent responsibility>"; "<invalid state> is unrepresentable rather than runtime-guarded" |
| `Design.md` §3 <the mechanism> | the failure case the mechanism exists to guard against | "The guard against <failure case> is present and reachable on the path this phase builds" |
| `Design.md` §5 Resolved Decisions / Open Questions | rulings naming this phase's mechanism | "<rejected approach> appears nowhere in this phase's diff", with the grep that shows it |
| `PRD.md` §4 Acceptance Criteria | the criterion this phase discharges | not the criterion itself — that is an Acceptance Criterion in the phase file — but its edge: what must not change while this phase satisfies it |

**Filling the Affected Files bound.** Write the whole prefix as the repository-relative path the diff reports — the only path space the bound is tested in.

---

## When a source is missing

**A missing document is not a missing bound.** `Design.md` is the artifact most often absent, since the PRD's §6 Next Step routes some work straight to Implementation. When a row's source document does not exist, put that row's "Read it for" question to the artifacts that do — what a Design would have ratified usually sits in the PRD's Decisions table, the Implementation's Orientation, or the Implementation's phase steps — then write the bound and cite the source actually read.

A section deleted as OPTIONAL from a document that is present is the one case that genuinely yields nothing: record none and move on. A missing document is not that case, and never shortens either table.
