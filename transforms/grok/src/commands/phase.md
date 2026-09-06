---
description: Converts the Spec-Driven Development specs into the folder orchestrate consumes — an Overview carrying what more than one phase needs, one Phase-N file of work each, superseded specs archived. Takes the plan folder; use between authoring the specs and executing them.
argument-hint: "[plan-folder]"
---

# Phase Command

Invoke the analyzer agent to break the indicated plan into an overview and phase documents.

## Process

### Break Plan Into Phases

Have the analyzer do the following:

A. Create `Overview.md` in the plan folder:

1. Overall orchestration of the planned implementation
2. Relevant background and context that guides the process
3. Content and instructions relevant to more than one phase

B. Create one or more `Phase-X.md` files in the plan folder:

1. One file per phase
2. Not redundant with Overview (both are provided during each implementation phase)
3. Specific, actionable tasks for that phase

C. Populate the `## Governance Bounds` section of `Overview.md` and of every `Phase-X.md` from the limits the plan folder's source documents place on the work, in those documents' own words. Overview carries the bounds spanning phases; each phase file carries the bounds scoped to that phase alone. Each template states the shape a bound must take, and `bounds-sources.md` beside them carries the source map, the filters every candidate passes before it is written, and the rank the two lists stand in; work both.

#### Templates

Use the following templates when creating plan files. Provide all three paths to the analyzer.

- `{reference-root}/templates/plan/Overview-template.md` — skeleton for `Overview.md`
- `{reference-root}/templates/plan/Phase-X-template.md` — skeleton for each `Phase-N.md`
- `{reference-root}/templates/plan/bounds-sources.md` — the source map, filters and ranks step C mandates

### Review

Invoke the reviewer agent to compare the Overview and Phase files against the source specs, handing it `bounds-sources.md` as well — the enforcement list below turns on terms defined there. The Sweep below archives the sources, leaving a coder `Overview.md` plus one phase file. The standard is reconstruction, not mention: a canonical file *discussing* the subject is a miss, and a decision surviving only in a source document is lost whatever its quality.

1. **Completion**: walk every section and every table row of every source document, `Implementation.md` and later arrivals included, keying the sweep to source location, never to bolding — bold marks conclusions, so a bold-keyed sweep misses warrant by construction and reads a table as zero items. Test each of these per item:

   - **Conclusion carried** — the decision is reconstructible from the canonical set.
   - **Warrant carried** — why-this-constraint-must-hold travels with the constraint, or an implementer tidies the rule away; why-it-was-chosen-over-the-alternatives stays behind with the source. Test each: needed to build correctly and resist undoing → travels; record of how it was decided → stays. Report a constraint carried without its warrant as a partial loss.
   - **Qualification carried** — rank this highest. Qualifications travel with what they qualify; enumerate the sources' own directly.

2. **Efficiency**: Phase files are not redundant and don't introduce content beyond the source specs

Edit the files as needed to satisfy these criteria.

**Analyzer instructions:**

1. Copy the relevant skeleton, fill all `<placeholder>` markers, and delete optional sections that do not apply to this plan.
2. If Config Literal Audit or Serde Defaults Audit blocks appear in Overview but are actually phase-local concerns, lift them into the specific phase file.
3. Config Literal Audit must scan inline-TOML-literal sites (e.g., `toml::from_str(r#"..."#)` inside tests, fixture strings, docs) in addition to on-disk `.toml` files. Inline literals are the most common hiding place for stale field names after a schema rename.

**Reviewer enforcement (apply to every Overview and Phase file):**

- Flag any AC that lacks a verifier hint (soft rule — flag, do not reject)
- Confirm the Deviations section is present and filled (not left as a `<placeholder>`)
- Reject any file that still contains literal `<placeholder>` markers
- Reject any bound failing a filter in `bounds-sources.md § Filters on every row's output` — a repair made here costs no governor round trip at the Assay step below

### Assay the Bounds

Make the inverted-charter governor dispatch `{command-root}/orchestrate.md` § 2 Validate Boundaries specifies — its Content and its Criteria — over this plan folder, routed as below. It runs here, before the Sweep, because the source documents are still unarchived and the analyzer that wrote the bounds is still the party that can repair them.

- `STOP` — hand the return to the analyzer, which repairs the bounds; re-run the assay. A second `STOP` routes through `governing-work` § Routing the return before the re-dispatch.
- `CLEAR` — proceed to the Sweep, so that `/orchestrate` § 2 confirms rather than discovers.

### Sweep

**Trigger:** runs immediately after the bounds assay returns `CLEAR`, as the last step of `/phase`.

**Classification question (apply to every non-canonical file):**

> "Is this content directly related to, and necessary for, implementing this phase's requirements?"

For every non-canonical file in `plans/<plan>/` (i.e., not `Overview.md` or `Phase-N.md`):

**a. Classify** — Answer the classification question. Default = SWEEP. Each file must justify a KEEP decision.

**Source specs → SWEEP unconditionally.** Any file used to author Overview + Phase (Implementation.md, Design.md, RFC.md, Plan.md, etc.) is 100% superseded once the canonical files are written. The analyzer's authoring duty is to carry forward every implementation-relevant detail into Overview/Phase. KEEPing it pulls the plan into context twice (canonical + source). Substantial content is not a reason to KEEP; it is a reason to verify the carry-forward was complete.

**Background, rationale, history, design discussions, and process artifacts of the `/phase` run itself → SWEEP unconditionally.** These are the rationale behind the specs, not the specs themselves, and Spec-Driven Development leaves them behind at this seam. Atypical plans (doc/template/command-file) should still default SWEEP for process artifacts even when they appear to be "evidence" — cure-becomes-disease risk.

**Affirmative KEEP** is reserved for **secondary reference material**: content that is NOT itself part of the implementation plan but illuminates specifics during implementation. Qualifying examples:

- Sample data files (e.g., a 1000-record JSONL the coder samples to understand structure, or an analyst writes interrogatory scripts against)
- Code/ID mappings (ANSI/ISO code tables, zip-code lookups, enum reference sheets)
- Architecture diagrams or system overviews shared across phases
- Fixture inputs and golden outputs the implementation tests against
- Existing files being edited in place by the implementation

If a file *contains the plan itself* — even partially — it is a source spec, not a secondary reference. SWEEP it regardless of size or apparent value.

**b. Reconcile** — Two reconciliation passes per KEEP file. Both are mandatory; symbolic references do not show up in path-based greps and must be hunted separately.

**b.1 File-path references.** For every KEEP file, grep for references to SWEEP candidates (filenames, relative paths, `archive/...` prefixes). Cosmetic references (Related Documents links, "see also" mentions, footnotes) → strip.

Surviving non-cosmetic file-path references after stripping indicate the original phasing failed to inline necessary content into the KEEP file — rationale leaking past the seam — and must be flagged for user decision (either backfill inline and strip, or reclassify the candidate as an implementation artifact if it qualifies). Properly phased plans should produce zero such surviving references.

**b.2 Symbolic identifier references.** For every SWEEP candidate, extract every identifier it *defines* — table-row IDs (`T-1`, `T1`), finding codes (`S5`, `W-3`, `O2`, `F-7`, `Y-12`), glossary terms, numbered-list anchors referenced elsewhere by their number, or any other code/label whose meaning lives only in that SWEEP candidate. Build the identifier set explicitly; record it in the Sweep-Manifest so the convergence test can re-grep against it.

Resolution is mechanical and single-branch: **carry the relevant subset of the source table forward into the canonical KEEP file that owns it.** Placement follows the Overview/Phase split already used everywhere else in the plan:

- **Referenced by two or more Phase files → carry into `Overview.md`.** Shared lookup table; lives where shared content lives.
- **Referenced by exactly one Phase-X.md → carry into that Phase-X.md.** Phase-local lookup table; lives with the phase that uses it.

Carry only the rows (or list items) actually referenced — not the full source table — so the KEEP file does not bloat with dropped findings. The table header and column structure carry forward unchanged so codes read against the same schema the source used. After the carry, subsequent references resolve against the KEEP file's own table.

Bare code-references to identifiers whose defining table has not been carried forward into the referring KEEP file (or its Overview, in the shared case) are forbidden. "T-1" reading standalone is a defect — the next coder cannot tell whether `T-1` is meaningful or noise without finding its defining row inside the same plan folder.

**c. Move and manifest** — Move SWEEP files to `plans/<plan>/archive/`. Write `plans/<plan>/archive/Sweep-Manifest.md` recording: per-file classification (KEEP/SWEEP + reason), file-path references stripped (from b.1), the full identifier set extracted per SWEEP candidate plus the destination KEEP file each carried-forward subset landed in — `Overview.md` (shared) or `Phase-X.md` (phase-local) (from b.2), and any user-decision-required flags.

**Convergence test:** after sweep, two greps over every KEEP file must return zero hits:

1. Any path under `archive/` — catches surviving file-path references (b.1 closure).
2. Every identifier in the Sweep-Manifest's extracted-identifier set — catches surviving symbolic references (b.2 closure). Run this grep per identifier, not as a single union pattern, so a single missed inlining is unambiguously attributable to its source.

## Output

Overview and Phase files for the implementation plan
