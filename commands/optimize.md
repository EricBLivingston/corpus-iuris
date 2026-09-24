---
description: "Rewrites a document for the strongest signal at the fewest tokens (∋1), meaning intact, as a reviewed copy. Takes the document path; use on any prose artifact grown slack: plan, spec, reference, rule, skill."
argument-hint: "[document-path]"
model: opus
---

# Optimize Command

Invoke the analyzer agent to optimize the indicated document.

## Process

### Optimize Document

A. Apply the following optimizations, drawn in part from ∋5 and ∋1, restated for focus and force:

1. **Lingua**: Apply each lingua the document uses, `§en` to its prose.
2. **Redundancy**: Apply DRY principles jointly across all reviewed artifacts and always-loaded context. Two duplicates are legitimate and stay: an enumeration that **names the provision it enforces** (A's own lead-in is the model; an enumeration naming nothing gets no exception), and a passage stating a reason or operational detail the source lacks.
3. **Verbosity**: Reduce wordiness; every token counts
4. **Tutelage**: Remove tutorial-style explanations from non-tutorial artifacts unless explicitly requested
5. **Tautology**: Eliminate redundant phrasing and tighten language
6. **Superfluity**: Remove content that is obvious or well-understood
7. **Obsolescence**: Remove or update outdated or incorrect information against the current state of the project or domain.
8. **Vacuity**: Remove prose that reads as guidance but commits to nothing actionable (i.e. removing it changes nothing substantive)
9. **Scaffolding**: Remove unnecessary navigation apparatus (always true for artifacts constrained by ※5)
10. **Tamarian**: Refactor, if possible, to evoke maximum model understanding with minimum tokens.
11. **Reference integrity**: every inbound reference to the document that the cut invalidates is found and repaired in this pass, ordinals and identifiers included (`⊨2`); a passage rewritten to replace another leaves no residue of the replaced (`⊨3`).

B. Write the optimized content to the Output path.

### Review

Invoke the reviewer agent to compare the `-OPT` document in `{analysis-root}/` against the original at its source path:

1. **Comprehensiveness**: All important source content is represented
2. **Sufficiency**: Enough content remains to fully represent each concept without over-optimization
3. **Accuracy**: No meaning changed or lost

Edit the optimized document as needed.

## Output

Write the optimized document to `{analysis-root}/{document-path-without-extension}-OPT.{extension}`. `{analysis-root}/` sits outside command/skill/agent discovery paths; create it if missing. Never write beside the original: an `-OPT` copy in an always-loaded directory gets loaded alongside it, doubling the cost the optimization exists to cut.

Report:

1. Summary of optimizations performed
2. Path to the optimized document
