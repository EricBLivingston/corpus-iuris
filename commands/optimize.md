---
description: "Rewrites prose artifacts grown slack (plan, spec, reference, rule, skill) for the strongest signal at the fewest tokens (∋1), meaning intact: a reviewed `-OPT` copy by default, or reviewed in place against a `-PRE` snapshot. Takes one or more document paths, and `in-place` to edit them directly."
argument-hint: "[document-path...] [in-place]"
model: opus
---

# Optimize Command

Invoke the analyzer agent once over the indicated documents: item 2 reads across them. Each result is written in place when the invocation says so, otherwise to an `-OPT` copy, which leaves the original untouched until the user replaces it.

## Process

### Optimization

A. Apply the following optimizations, drawn in part from ∋5 and ∋1, restated for focus and force:

1. **Lingua**: Apply each lingua the document uses, §en to its prose.
2. **Redundancy**: Apply DRY principles jointly across the batch and always-loaded context. Two kinds of repetition stay: an enumeration naming the provision it enforces (A's lead-in is the model), and a passage adding a reason or operational detail its source lacks.
3. **Verbosity**: Reduce wordiness.
4. **Tutelage**: Remove tutorial-style explanations from non-tutorial artifacts unless explicitly requested.
5. **Tautology**: Eliminate redundant phrasing.
6. **Superfluity**: Remove content that is obvious or well-understood.
7. **Obsolescence**: Remove or update outdated or incorrect information against the current state of the project or domain.
8. **Vacuity**: Remove prose that reads as guidance but commits to nothing actionable (i.e. removing it changes nothing substantive).
9. **Scaffolding**: Remove unnecessary navigation apparatus (always true for artifacts constrained by ※5).
10. **Tamarian**: Refactor, if possible, to evoke maximum model understanding with minimum tokens.
11. **Reference integrity**: Every inbound reference to the document that the cut invalidates is found, ordinals and identifiers included: in place it is repaired in this pass, for a copy it is listed in the report for the swap (⊨2); a passage rewritten to replace another leaves no residue of the replaced (⊨3).

B. In place: snapshot each document to its `-PRE` path, then overwrite it. Copy: write each result to its `-OPT` path.

### Review

Invoke the reviewer agent once over the batch to compare each result against its before-state: an `-OPT` copy against its source path, an in-place edit against its `-PRE` snapshot.

1. **Comprehensiveness**: All important source content is represented.
2. **Sufficiency**: Enough content remains to fully represent each concept without over-optimization.
3. **Accuracy**: No meaning changed or lost.

Remediate the findings and re-review (⊨7).

## Output

Per document, the `-OPT` copy goes to `{analysis-root}/{document-path-without-extension}-OPT.{extension}` and the `-PRE` snapshot to `{analysis-root}/{document-path-without-extension}-PRE.{extension}`, whichever the mode produces. `{analysis-root}/` sits outside command/skill/agent discovery paths; create it if missing. Never write beside the original: an `-OPT` copy or `-PRE` snapshot in an always-loaded directory gets loaded alongside it, doubling the cost the optimization exists to cut. The snapshot is left for the user: restoring it reverts the optimization alone.

Report:

1. Summary of optimizations performed.
2. The mode; per document, the result path and, in place, the snapshot path.
3. References left for the copy swap.
