---
description: Rewrites a document to strip redundancy, wordiness, tutorial explanation, tautology, and stale claims, landing a reviewed -OPT copy under `.analysis/`. Takes the document path; use to tighten a plan or spec where the meaning must survive the cut.
argument-hint: "[document-path]"
---

# Optimize Command

Invoke the analyzer agent to optimize the indicated document.

## Process

### Optimize Document

A. Apply these optimizations (this is a superset of ※11, restated and enhanced for focus and to underscore the imperative):

1. **Redundancy**: Apply DRY principles jointly across all reviewed artifacts and always-loaded context. Two duplicates are legitimate and stay: an enumeration that **names the provision it enforces** (A's own parenthetical above is the model — an enumeration naming nothing gets no exception), and a passage carrying a reason or operational detail the source lacks.
2. **Verbosity**: Reduce wordiness; every token counts
3. **Tutelage**: Remove tutorial-style explanations from non-tutorial artifacts unless explicitly requested
4. **Tautology**: Eliminate redundant phrasing and tighten language
5. **Superfluity**: Remove content that is obvious or well-understood
6. **Obsolescence**: Remove or update outdated or incorrect information based on current state of the project or domain.
7. **Vacuity**: Remove prose that reads as guidance but commits to nothing actionable (i.e. removing it changes nothing substantive)
8. **Scaffolding**: Remove unnecessary navigation apparatus, (always true for artifacts constrained by ※5)
9. **Tamaranian**: Refactor, if possible, to evoke maximum model understanding with minimum tokens.

B. Write the optimized content to the Output path.

### Review

Invoke the reviewer agent to compare the `-OPT` document in `.analysis/` against the original at its source path:

1. **Comprehensiveness**: All important source content is represented
2. **Sufficiency**: Enough content remains to fully represent each concept without over-optimization
3. **Accuracy**: No meaning changed or lost

Edit the optimized document as needed.

## Output

Write the optimized document to `.analysis/{document-path-without-extension}-OPT.{extension}`. `.analysis/` sits outside command/skill/agent discovery paths; create it if missing. Never write beside the original — an `-OPT` copy in an always-loaded directory gets loaded alongside it, doubling the cost the optimization was performed to cut.

Report:

1. Summary of optimizations performed
2. Path to the optimized document
