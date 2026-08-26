# Codex Transposition Guide

This guide is working discipline for the Codex transform: what may change on the way from the shared sources into a live Codex installation, and how a live Codex home is touched. The guide itself is not part of the installed corpus. `README.md` carries the adoption sequence.

## Scope

This is a maintained downstream realization of a live upstream corpus, not a one-time port. Resynchronization after upstream changes is normal operating procedure, so **minimum-necessary change** is the governing criterion: every edit to a copied file is a divergence that must be reconciled at every later refresh, and must earn that permanent cost. An installation's own facts belong in its instance file, where a keyed entry merges with a later upstream revision instead of colliding with it.

- Work only from sources present in this clone. A missing source is deferred, not reconstructed from memory or another installation.
- Staging, `<codex-home>/corpus-staging/`, is a fourth surface beside the three `README.md § For an adopting Codex` separates. Rebuild it from the checkout for every refresh; it is disposable processing material, never canon.
- Writing outside the clone, or changing user-level Codex configuration, requires explicit user authorization. Filesystem approval from the harness does not replace that conversation.
- Style, wording preference, exposition, clarification, and cosmetic consistency never justify a delta. Preserve formatting; do not reflow carried text.
- Prefer deleting or narrowly substituting a false clause over rewriting its sentence, paragraph, or section.
- Do not add caveats that restate immutable harness or model bounds, including instruction priority. Translate only mechanics that must change for the provision's intended behavior to survive.
- Keep doctrine declarative: state what binds, not how it is authored, admitted, loaded, or maintained. Those procedures belong in a guide like this one or in a context-curation skill, not in the statute they operate on.
- Use current official OpenAI documentation for the Codex surfaces this package touches.

## Admit or defer

Corpus files are copied verbatim, `{placeholders}` and all, and the instance file resolves the placeholders once for every file that writes them. Copying into staging is not admission. A staged rule is **admitted** only when its `@import` is written in `canon.md`; otherwise it is **deferred**.

Defer is the half that carries weight. The loader fails closed, so an import written ahead of its file rejects the entire canon rather than the one entry — premature admission is the only adoption mistake whose blast radius exceeds itself. Defer any artifact whose file is not yet in place, and treat a reference to an unavailable skill, agent, MCP server, hook, memory or reference file as a deferred dependency rather than as grounds to withhold or alter the referring content. Once the planned corpus is fully loaded, sweep its citations and resolve only what remains unresolved there.

A provision that is merely generic where Codex is specific, or that Codex contradicts outright, is neither deferred nor edited: it takes a keyed entry in the installation's instance file, which keeps its number resolvable on both sides. `../../adopting.md § Taking a provision you do not want as written` sets that route against its alternatives and gives the cost of each.

Amending a copied file is the escape hatch, and it should stay empty. A span Codex makes factually false — a tool named as a literal, an interaction model no keyed entry can reach — is upstream's defect rather than this installation's: it is wrong on every harness that is not the one it was written for, so report it upstream. Correct it locally only where waiting is not an option, confine the correction to the false span, and drop it when the upstream fix lands.

## Rule admission

A staged rule nothing loads binds nothing, so admitting one to the resident corpus is two edits:

| Product | Destination |
| ---- | ---- |
| the artifact | its source-relative path inside the production corpus root, unless Codex requires otherwise |
| its admission | an `@import` line naming that path, in `canon.md` |

Preserve the source-relative tree: mirrored paths keep every later refresh a diff rather than a hunt. The order of the two edits is fixed — file first, then import — because an import ahead of its file rejects the whole canon.

`canon.md` is the entrypoint the SessionStart loader expands into the next session's context; `src/hooks/corpus_iuris_session_start.py` implements its syntax, its budget and its failure modes, and is the authoritative account of them. An import resolves relative to the directory of the file declaring it, and its target must resolve inside the corpus root; an imported file may import in turn under the same rule. The global entrypoint sits beside the corpus root rather than inside it, so its imports have to reach in — `corpus/rules/ius.md` under the default layout, and a `../`-relative path wherever the installation puts the corpus elsewhere. Expansion is literal and in order, so the entrypoint's order is the corpus's reading order: place each import where the artifact should be read.

The instance file takes one import however many rows it accumulates. Reference material is copied with the rule that reaches it, but is read on that rule's terms rather than imported merely because it is present. A skill takes Codex's discovery admission instead, never both.

## Refreshing through staging

A refresh is a staged deployment: source files are carried into a clean staging tree, Codex-specific changes are made there, and only validated outputs reach the installation. Begin from the new source artifact and reapply only the local corrections that remain necessary; never merge old local prose wholesale into a new source.

1. Refresh the clone and record the revision, or a content digest where no stable revision exists. One tree, one copy, one line; keep it outside the resident canon.
2. Rebuild `<codex-home>/corpus-staging/` as a clean copy of that clone. Do not reuse a previous staging tree or keep a resident artifact there. Preserve source-relative paths for the release's root rules, reference material, and skills.
3. Overlay `src/agents/*.toml` onto the staged custom-agent surface. These are the Codex-ready transpositions of root `agents/*.md`; deploy the TOML definitions, not a second copy of the Markdown sources. Inspect each definition for Codex-specific conflicts before selecting it.
4. Transpose any `commands/<name>.md` into a skill directory under staging, as `<codex-home>/corpus-staging/skills/<name>/SKILL.md`. The conversion adds `name: <name>` and removes the command-only `argument-hint` and `model` frontmatter fields. Inspect each resulting skill for Codex-specific conflicts before selecting it.
5. Apply only necessary Codex corrections in staging. Keep the local instance input outside the staging tree and curate the staged instance file from it; a refresh must not overwrite installation facts.
6. Read the existing `canon.md` as the rule-selection manifest. Resolve its import closure against staging, then choose any newly staged rules to admit. A rule's staged file must be in place before its import is added.
7. Diff staged carries and amendments against their release counterparts, ignoring whitespace first and then ordinarily. Account for every surviving delta; reject reflow and collateral edits.
8. Promote only validated staged outputs to their live destinations: rules and reference material under the production corpus root, each skill directory to `<codex-home>/skills/<name>/`, and TOML agents to `<codex-home>/agents/`. Do not copy the whole checkout and do not delete unselected resident files. Update the non-resident adoption ledger with source identity and retained corrections.
9. Run the installed loader directly, then start a matching session and confirm the selected canon is injected exactly once. Confirm Codex discovers selected skills and agents. A second deployment with unchanged staged outputs must change nothing.

## Touching live Codex configuration

Two things land in the live Codex home rather than in the corpus root: the loader's hook registration and the custom-agent definitions. Both can collide with configuration the user depends on, and the hook registration is the more dangerous of the two.

1. Resolve the active Codex home and the target files without assuming default paths. The loader honours `CODEX_HOME`, so the default is not guaranteed.
2. Inspect the complete target and the configuration around it before proposing an edit. Check override files and other layers that can make the nominal target inactive, and check whether a custom agent already claims the `name` a definition declares.
3. Explain material conflicts and obtain explicit user authorization for the proposed live changes, plus any filesystem or destructive-action approval the environment requires.
4. Merge minimally. Never replace a whole configuration file the installation already owns.
5. Preserve unrelated content, comments, ordering conventions, and stricter safety settings.
6. Validate syntax and Codex discovery behavior. Report applied, skipped, deferred, and conflicting items separately.

Superseded configuration is removed as part of an authorized migration and not otherwise. `../../rules/caselaw.md` `⊨3` requires that a replacement purge the replaced thing's whole footprint; what a third-party configuration adds is that the footprint has to be established by inspecting the live installation before the purge, not read off a manifest.

## What `src/` holds

There are no per-artifact transposition recipes, and none are planned: the corpus sources carry `{placeholders}` for whatever an installation names for itself, and the naming is done once, in the instance file.

`src/` is installed or run, not applied. `src/hooks/` holds the SessionStart loader and its tests; `src/agents/` holds one Codex custom-agent definition per corpus agent, each generated from its corpus original before this package reached you. `src/instance-example.md` is the one exception: another installation's filled instance file, copied out and refactored rather than installed as it stands. Read each set from its directory rather than from a list here, which would go stale by omission the moment either set changed. A body can still rest on a particular of the harness it was written for that Codex has no counterpart to, so read each definition before installing it; in the usual case install it as it stands.
