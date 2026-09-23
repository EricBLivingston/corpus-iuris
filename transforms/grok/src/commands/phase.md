---
description: "Converts the Spec-Driven Development specs into the folder orchestrate consumes: an Overview carrying what more than one phase needs, one Phase-X file of work each, superseded specs archived. Takes the plan folder; use between authoring the specs and executing them."
argument-hint: "[plan-folder]"
---

# Phase Command

Invoke the analyzer agent to break the plan folder at `$ARGUMENTS` into an Overview and phase documents.

## Process

### Break the plan into phases

Have the analyzer:

A. Create `Overview.md` in the plan folder: the overall orchestration, the background guiding it, and everything more than one phase needs.

B. Create one `Phase-X.md` per phase, the set derived as below: specific, actionable tasks for that phase, not redundant with Overview (the executor possesses both).

C. Populate the `## Governance Bounds` section of `Overview.md` and of every `Phase-X.md` from the limits the plan folder's source documents place on the work, in those documents' own words. Overview contains the bounds spanning phases; each phase file contains those scoped to it alone. `bounds-sources.md` beside the templates contains the source map, the filters every candidate passes before it is written (shape among them), and the rank the two lists stand in; each template names the table its own list draws from.

#### Deriving the phase set

A phase is one ※8 cycle; several logical units routinely close inside one. Re-derive the set rather than inheriting the source plan's phase count or its narrative units. Three forces pull against one another:

- **Overhead.** Four dispatches per phase, each re-reading canon and re-processing a large prompt before it reaches the work.
- **Coherence.** Overview plus one Phase file describe that phase's work completely, the work inside it connects, and every file the executor loads bears on the one claim the phase closes.
- **Containment.** A phase overrunning what one coder and one reviewer keep at full attention degrades the work whatever it saves in dispatches.

Test each candidate against all three:

- A step that authors nothing (pre-flight check, recorded measurement, verification run) belongs inside the phase that needs it.
- A phase repeating the preceding phase's recipe on new inputs merges into it behind an internal gate: the first instance passes review before the rest proceed.
- A phase whose review would demand two unlike competencies, or whose files span unrelated surfaces, splits.
- A phase bearing real risk, or a §16 cross-boundary gate, is kept. Where that gate sits as a phase's test step, state it as the gate, so an executor cannot read it as optional.

#### Templates

Hand the analyzer every path below (∋3).

- `{reference-root}/templates/plan/Overview-template.md` — skeleton for `Overview.md`
- `{reference-root}/templates/plan/Phase-X-template.md` — skeleton for each `Phase-X.md`
- `{reference-root}/templates/plan/bounds-sources.md` — step C's source map, filters and ranks

**Analyzer instructions:**

1. Copy the relevant skeleton, fill every `<placeholder>` marker, and delete optional sections that do not apply to this plan.
2. Config Literal Audit must scan inline-TOML-literal sites (`toml::from_str(r#"..."#)` in tests, fixture strings, docs) as well as on-disk `.toml` files: inline literals are the commonest hiding place for stale field names after a schema rename.
3. Overview plus one phase file must reconstruct the plan without the sources, which the Sweep archives: carry forward every implementation-relevant detail.

### Review

Invoke the reviewer agent to compare the Overview and Phase files against the source specs, handing it `bounds-sources.md` as well (the enforcement list below turns on terms defined there). The Sweep archives the sources, leaving the coder `Overview.md` plus one phase file, so the standard is reconstruction: an Overview or phase file *discussing* the subject is a miss, and a decision surviving only in a source document is lost whatever its quality.

1. **Completion**: walk every section and every table row of every source document, `Implementation.md` and later arrivals included, keying the sweep to source location, never to bolding (bold marks conclusions, so a bold-keyed sweep misses warrant by construction and reads a table as zero items). Test each item:

   - **Conclusion carried** — the decision is reconstructible from the Overview and phase files.
   - **Warrant carried** — needed to build correctly and resist undoing → travels with the constraint, or an implementer tidies the rule away; record of how it was chosen over the alternatives → stays with the source. Report a constraint carried without its warrant as a partial loss.
   - **Qualification carried** — rank this highest. Qualifications travel with what they qualify; enumerate the sources' own directly.

2. **Efficiency**: Phase files are not redundant and introduce no content beyond the source specs.

Edit the files as needed to satisfy these criteria.

**Reviewer enforcement (apply to every Overview and Phase file):**

- Flag any AC lacking a verifier hint (soft rule: flag, do not reject)
- Confirm the Deviations section is present and filled
- Reject any file still containing literal `<placeholder>` markers
- Reject any bound failing a filter in `bounds-sources.md § Filters on every row's output` (a repair made here costs no governor round trip at the assay below)

### Assay the bounds

Make the inverted-charter governor dispatch `{command-root}/orchestrate.md` § 2 Validate Boundaries specifies — its Content and its Criteria — over this plan folder. It runs before the Sweep, while the source documents are unarchived and the analyzer that wrote the bounds can still repair them.

- `STOP` containing no crossed row — hand the governor what its evidence column names as absent, and re-dispatch.
- `STOP` — hand the return to the analyzer to repair, and re-run the assay. A second `STOP` routes through `governing-work` § Routing the return before the re-dispatch.
- `CLEAR` — proceed to the Sweep, so `/orchestrate` § 2 confirms rather than discovers.

### Sweep

Runs immediately after the assay returns `CLEAR`, the last step of `/phase`, over every other file in `plans/<plan>/` (everything but `Overview.md` and `Phase-X.md`).

**a. Classify** — default SWEEP; a KEEP justifies itself against "is this content directly related to, and necessary for, implementing this phase's requirements?"

- **Source specs** — whatever was used to author Overview and Phase (`Implementation.md`, `Design.md`, `RFC.md`, `Plan.md`) → SWEEP unconditionally. The Overview and phase files supersede them, and keeping one pulls the plan into context twice. Substantial content is a reason to verify the carry-forward, never to KEEP.
- **Background, rationale, history, design discussion, and the `/phase` run's own process artifacts** → SWEEP unconditionally. Spec-Driven Development leaves the rationale behind at this seam. An atypical plan (doc, template, command-file) sweeps its process artifacts too, however much they look like evidence.
- **Secondary reference material** → KEEP: content that is not itself the plan but illuminates specifics during implementation — sample data files, code/ID mappings (ANSI/ISO tables, zip lookups, enum sheets), architecture diagrams or system overviews shared across phases, fixture inputs and golden outputs, files the implementation edits in place.

A file containing any part of the plan is a source spec whatever its size or apparent value.

**b. Reconcile** — both passes run over every KEEP file; symbolic references do not surface in path-based greps.

**b.1 File paths.** Grep each KEEP file for references to SWEEP candidates (filenames, relative paths, `archive/...` prefixes) and strip the cosmetic ones (Related Documents links, "see also" mentions, footnotes). A surviving non-cosmetic reference means the phasing failed to inline what the KEEP file needs; flag it for user decision — backfill inline and strip, or reclassify the candidate as an implementation artifact where it qualifies. A properly phased plan produces none.

**b.2 Symbolic identifiers.** From each SWEEP candidate extract every identifier it *defines* — table-row IDs (`T-1`), finding codes (`S5`, `W-3`, `F-7`), glossary terms, numbered-list anchors referenced elsewhere by number, and any other code whose meaning lives only there — and record the set in the Sweep-Manifest for the convergence test. Resolution is mechanical and single-branch: carry the referenced rows or list items of the defining construct into the Overview or phase file that owns them, header and column structure unchanged, so the codes read against the source's schema. Referenced by two or more Phase files → `Overview.md`; by exactly one → that `Phase-X.md`. Carry only the rows or items actually referenced. A bare code whose defining rows were not carried into the referring file, or into `Overview.md` in the shared case, is a defect: the next coder cannot tell `T-1` from noise without opening the archive.

**c. Move and manifest** — move SWEEP files to `plans/<plan>/archive/` and write `plans/<plan>/archive/Sweep-Manifest.md` recording per-file classification with reason, the file-path references stripped (b.1), the identifier set per SWEEP candidate with the destination each carried subset landed in (b.2), and any user-decision flags.

**Convergence test:** over every KEEP file, two greps must return zero hits — any path under `archive/`, and each Sweep-Manifest identifier, run one identifier at a time so a missed inlining attributes to its source.

## Output

`Overview.md` and one `Phase-X.md` per phase in the plan folder; the superseded sources under `plans/<plan>/archive/` beside `Sweep-Manifest.md`.
