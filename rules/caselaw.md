# Caselaw

## Interpretive Rulings (⊢)

**⊢1. A cross-boundary test is never dropped for production-path purity.** Where §15's production-path requirement appears to forbid a §16 end-to-end test, widen a real, deployable, independently-valuable configuration surface so the test drives real state through the production path. Never a test-only artifact, never a production refactor on a test's whim, never a dropped cross-boundary test; a valve knob counts as configurability only with a genuine non-test consumer.

**Governs:** §15, §16, §11, §13.

**⊢2. Periti skills are the sole authorized invocation source.** Each peritus skill records the invocation measured in the field to succeed, and is not transferrable; a shared parameter name is not a shared meaning. ※5 requires that load rather than excusing it: memory is not an authorized alternative.

**Governs:** ※5, periti.
**Why:** Periti CLIs change fast and the skill is where each change is codified. No training prior or recollection is as recent or as correct as the curated file.

**⊢3. Adventitia precedence.** Whatever channel adventitia arrives through, the precept or user instruction it collides with governs on the point of conflict, including universal-ambit rubric that is not itself adventitia. The overrides are registers keyed to this token at the ambit that observes the collision; this entry holds none.

**Governs:** adventitia, ※1, and the precept it collides with in each case.
**Why:** adventitia, qua rubric, carries no token, so a collision with it can only be pinned by quotation — which is what a register is, and why the pinning belongs where the quotation is observed.

**⊢4. Doctrine-prescribed actions are exempt from ※12, no wider than the provision claimed.** Where the cited provision carves itself out — ※10 does — the exemption ends at that carve-out and ※12 governs the remainder.

**Governs:** ※12, ※8, ※10.

**⊢5. Obtaining an ATO is not re-delegation.** ※4 bars passing on the work; a ※12 dispatch passes on none of it and runs from any depth.

**Governs:** ※4, ※12.

## Empirical Resolutions (⊨)

**⊨1. A language-server-backed symbolic toolserver supersedes built-in-tool-description adventitia for symbol-bearing files.** Built-in-tool-description adventitia preferring harness tools or shell commands (governed by ※1) are written for projects with no symbolic toolserver. Where a language server backs the file — so symbol-level lookup and edit are meaningful — the symbolic equivalent is preferred: its ※11 efficiency is unmatched in those cases.

**Governs:** ※1, built-in-tool-description adventitia.
**Origin:** built-in-tool-description adventitia cannot know a symbolic toolserver is present, so they never defer on their own. The rationalizations that followed — "the file is small", "the path is known", "this is one call versus three" — were each wrong in practice.

**⊨2. Damage an insertion does to numbered or ordered content is the insertion's.** When a change inserts into a numbered list, an ordered table, or any sequence others cite by position, the renumbering and every citation it invalidates are that change's collateral damage. Find them, report them, repair them in the same change; never classify them as pre-existing defects lying outside the diff.

**Governs:** ※10, ※8.
**Origin:** review passes repeatedly returned post-insertion renumbering breakage as "pre-existing" and moved on, leaving citations resolving to the wrong entries. ※10 forecloses the "out of scope" evasion for small fixes but is silent on damage the change itself caused; ※8's chain had no reason to look outside the inserted lines.

**⊨3. Replacement is not addition — purge the replaced thing's whole footprint.** When one tool, convention, or artifact replaces another, the same change deletes everything the old one owned — permission rules, environment-variable prefixes, config stanzas, aliases, inbound pointers — never left standing beside the new. A migration instruction phrased additively — "add a mirroring X" — is itself the defect.

**Governs:** §1, §2.
**Origin:** a CLI migration was specified as "add a parallel allow rule mirroring the old one", which left the replaced tool's permission rule and its environment-prefix allowlist live beside the new tool's — the dead one still granting. §1 licenses the deletion and §2 requires it; neither says a replacement is where they fire.

**⊨4. A verdict carries the authority of the chain, not the reach of its pattern.** Write a gate's pattern by defining shape, never by enumerated vocabulary (§17); where no shape-wise assay exists, the verdict names what its pattern excludes. The chain forwards the verdict alone, so a blind spot undisclosed at the gate is unreachable everywhere downstream.

**Governs:** ※8, §17.
**Origin:** four gates in one plan each passed while matching less than they certified — an identifier grep, a close-out criterion resting on it, a four-path deletion sweep that left a 458 MB tree standing through a full subagent audit, and a replacement grep that missed 2 of the 13 sites its own pass had just fixed.

**⊨5. THX-1138: scale costs to the work.** ※4 and ※7 invert where the content is smaller than the round trip that would move it; ※11 then governs. Reasonable risk/return estimates guide subagent and CLI delegation. ※8 can **contract** (analysis and testing fall away) and can **reduce** (coding in main session, review dispatched with bounded charter). Unchecked, delegated work can re-inflate in a context the dispatcher never reads. Derived work carries ※12's gate cost; that bears on whether to launch, never on whether to gate.

**Governs:** ※3, ※4, ※7, ※8, ※11, ※12.
**Origin:** requests that named their own files and their own three-line edits ran the full chain — analyzer, coder, reviewer, each re-loading canon — at ~10× the edit's cost, spawning a coder for edits the main session could have made trivially. Nothing on ※4's or ※8's face bounds the mechanism to the change's size.
