# FMEA — The Requestor Protocol

For the agent weighing a spend, and for the launch that follows if one is warranted.

**Default is don't.** The cost is certain and immediate; the benefit is discounted three times independently — it must occur, escape detection, and resist cheap repair. Those three discounts are the only thing that overrides the default.

## Preconditions, then oracles

- **Reachability** — no path from the event to a caller, dependent, reader, or downstream artifact: severity is **zero**, whatever class the event belongs to. Establish the path before estimating damage along it.
- **Has it already happened?** — assess the unresolved consequence, never the class of the triggering event. Retrospective triggers route to **Narrow** by default.
- **Cheap oracles first** — ask the user (dispositive in one turn for anything a human could have authored); reason from the artifact's structure (settles reachability with no query). A launch that has tried neither is not narrowed, merely large.

## Limbs

**Severity** — calibrated:

| High here | Low here |
| ---- | ---- |
| Irreversible act: deleted file, pushed commit, sent message, dropped data | Stack trace, failed test, lint error |
| A wrong answer delivered confidently and acted on | A wrong path that errors on first use |
| Corruption of a durable artifact — guidance, memory, plan, schema | A local edit, one revert away |
| Cascade: half-applied tree, orphaned process, poisoned state | Contained to the current turn |

Both columns presuppose reachability: with no path, the row does not apply at all — severity is zero, not "low pending confirmation".

Note: **Scrutinize underlying assumptions** — examples:

| Prima facie severe | Actual circumstance |
| ---- | ---- |
| "Repo exposes a secret" | "Code already clean, key already rotated" |
| "API endpoint is reachable" | "Behind a firewall, exposed to localhost only" |
| "A safety guard vanished from config" | "The user removed it deliberately, minutes ago" |
| "Critical CVE in a dependency" | "The vulnerable path is never invoked" |
| "Output data looks corrupted" | "A rendering artifact; the bytes on disk are correct" |

**Occurrence** — observed, boundary-adjacent, or conceivable-only. Conceivable-only never clears the bar at any severity; an observed claim needs an independently checkable citation or it downgrades, and the assessment will test exactly that.

**Detection and recovery** — this environment detects well, so most candidate defenses target failures that would have been loud and one edit from fixed.

## Bands — the decision predicate

Conceivable-only occurrence never clears the bar, at any severity. Above that floor, and nowhere else:

- **Proceed** — severity irreversible, silent, or durable **with** occurrence at least boundary-adjacent, those severity terms being themselves a failed detection or an unrecoverable cost; or detection poor with occurrence observed or boundary-adjacent **and** recovery costly once it fires.
- **Narrow** — the default: same question, cheaper probe, tighter bound.
- **Skip** — otherwise. Let it fail; fix it if it does.

This predicate is stated here and nowhere else; the assessment protocol tests a table against it.

Weigh the tax before drafting, not after: if the launch is not worth an assessment round-trip, narrow until what remains is ordinary diligence on the task actually asked for.

## One lifecycle

The table is the assay's record, not a launch order. Draft it, band it, and then:

- **Narrow** re-assays at the tighter bound. Nothing launches: the narrowed work either falls to micro and settles inline, or returns as a proceed table.
- **Skip** ends the matter silently.
- **Proceed at bound** — and only this — is dispatched for ATO.

**Verdict** is your band; **ATO** is the AO's decision. Different rows, different authors; never write one into the other.

## Launch procedure

1. Fill the template at `{reference-root}/templates/fmea-statement.md` into a file of its own, named `FMEA-YYYY-MM-DD-<slug>.md`, the slug naming the ask in three to five kebab-case words. Cost is a bound, never an estimate; the ATO row travels present and empty. One file per request, never one accumulating file per folder: subagents run concurrently, and two of them appending to one file collide.

   Where it lands — the first of these three that applies:

   - **The plan folder governing the work** — the `plans/<name>/fmea/` your implementation is running inside.
   - **The project you are working in**, when no plan folder governs — its own `{analysis-root}/fmea/`.
   - **The corpus itself**, when the work belongs to no project at all — its own `{analysis-root}/fmea/`.

   The last two are not lesser records: a launch no plan called for is the kind this protocol exists to catch.

2. Dispatch to the authorizer agent as Authorizing Official, giving it the statement file's absolute path — the file is what it assesses, never a copy of the table in the prompt — and pointing it at `{skill-root}/performing-fmea/fmea-assessment.md` for the standard it assesses against.
3. **Wait on the decision.** The AO fills the ATO row in the file you handed it, grant or denial alike; read it back there. The launch does not start until that row carries a grant. A denial is binding: narrow and resubmit, or drop — disagreement escalates to the user, never past the AO. A missing, partial, or malformed response is a denial: restore the ATO row to empty, resubmit once, then escalate to the user.

Where the framing deviates from what the borrowed term already carries:

- The AO is the authorizer agent, not you and not the user.
- The authorization boundary is the statement's Cost bound. Crossing it is not overrun, it is operating unauthorized: re-assay, re-grant.
- The user sits above the framework: standing veto over any grant. Where a request's true cost runs far past what it implied, surface the estimate before the spend, not after.
- The statement binds the session that drafted it. A subagent's dispatch prompt is its own ask and its own bound (※12); the drafting session's Cost bound reaches that subagent only as the prompt writes it in (⊢5).

## Collisions

- **Never a license to remove boundary validation.** External input is boundary-adjacent by construction, so occurrence is granted; §6 and §8 already draw that line and are untouched here.
- **Never an argument against tests.** Tests are the detection infrastructure that makes default-deny safe (§12, §16). Cutting them worsens detection and *increases* the warrant for defense.
- **Never a warrant for skipping diligence on the requested task.** "Severity is low" is not a reason to leave the file unread.
