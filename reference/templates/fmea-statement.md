# FMEA Statement Template

The canonical shape of the statement requesting authorization of an ultra vires act (※12). Filled once per act, and nothing below that scale; each row is a line or two, not a paragraph. Consumer: the `performing-fmea` skill.

| Field | Fill with |
| ---- | ---- |
| **Question** | What this would establish, in one line. If it cannot be stated, the act has no terminating condition and does not start. |
| **Severity** | What breaks if this is skipped and the working assumption is wrong. If retrospective, the *unresolved consequence*; what remains undone, unrecovered, or still propagating. |
| **Occurrence** | Evidence the assumption *is* wrong: observed, boundary-adjacent, or conceivable-only. Observed claims carry independently checkable citations (incident record, `⊨` entry, failing run, measurement log) or they downgrade. |
| **Detection** | Whether being wrong would surface on its own, and what the fix costs once it does. |
| **Cost** | The **bound** placed on the act. For a launch: which files it may read or edit, which commands or probes it may run, token cap(s), plus the stopping condition ("past N files, stop and report"). For a bound amendment: the bound's full replacement text, in the form `governing-work` authors and the governor consumes — decidable by a reader holding only the produced content and the bound, measured, never a delta. |
| **Verdict** | The band the assay chose. Only a *proceed at bound* is dispatched for ATO, as a request for it; a *narrow* re-assays at the tighter bound, a *skip* ends the matter silently. |
| **ATO** | `granted` or `denied`, and the Authorizing Official's reasoning: the row that decided it, and — on a denial — either the text the AO would grant in its place or a declaration that no statement on this act would be granted, and why. Long enough to audit the gate later, not merely the act. A grant restates the Cost bound verbatim as authorized: that text, not the request's, is what enters the dispatch prompt or replaces the original in the bound set. Carried into dispatch present and empty — the AO fills it here, in place, and a denial is recorded exactly as a grant is. |

Note: **Cost is a bound, not an estimate.** Delegated spend is not predictable within a factor of two; the dispatching session does not control delegate actions. The bound is enforceable in the dispatch prompt or assayable by the governor, and is checkable afterwards. It is also how *narrow* is executed: narrowing is mostly choosing a tighter bound rather than a different question.
