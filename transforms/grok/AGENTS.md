# Grok Transposition Guide

Working discipline for the Grok transform. This file is not installed. Do not install it as an adopter's `AGENTS.md`. `README.md` states the adoption sequence.

## Scope

Resynchronization after upstream changes is normal, so **minimum-necessary change** is the criterion: every edit to a copied file is a divergence that must be reconciled at every later refresh, and must earn that permanent cost. An installation's own facts are keyed entries in its instance file; a later upstream revision merges with the entry.

- Work only from sources present in this clone. A missing source is deferred. Do not reconstruct it from memory or another installation.
- Staging, `~/.grok/corpus/staging/`, is the staging surface `../../installing.md § The installation sequence` states. Rebuild it from the checkout for every refresh. It is disposable processing material: never scanned, never canon.
- Writing outside the clone, or changing user-level Grok configuration, requires explicit user authorization. Filesystem approval from the harness does not replace that authorization.
- Style, wording preference, exposition, clarification, and cosmetic consistency never justify a delta. Preserve formatting. Do not reflow carried text.
- Prefer deleting or narrowly substituting a false clause over rewriting its sentence, paragraph, or section.
- Do not add caveats that restate immutable harness or model bounds, including instruction priority. Translate only mechanics that must change for the provision to keep its intended behavior.
- Doctrine states what binds. Authoring, admission, loading, and maintenance procedures stay in a guide like this one or in a context-curation skill.
- Use current Grok Build documentation for rules directories, skills, subagents, and `compat.claude`.

## Admit or defer

- Corpus files are copied verbatim, `{placeholders}` included. The instance file resolves those placeholders once for every file that contains them.
- **Defer**: do not copy into a scanned directory. A reference to an unavailable skill, agent, MCP server, or reference file is a deferred dependency. Do not withhold or alter the referring content because the target is absent. Once the planned corpus is fully loaded, sweep its citations and resolve only what remains unresolved.
- A provision that is generic where Grok is specific, or that Grok contradicts, takes a keyed entry in the instance file. Do not defer it and do not edit the copy. The entry keeps the number resolvable on both sides. `../../adopting.md § Taking a provision you do not want as written` states that route, its alternatives, and the cost of each.
- Amending a copied file is the escape hatch, and it should stay empty. Report a span upstream when Grok makes it factually false (a tool named as a literal, or an interaction model no keyed entry can overlay). The span is false on every harness other than the one it was written for. Where waiting is not an option, correct only that span. Drop the correction when the upstream fix is present.

## Rule admission

- A file nothing loads binds nothing. Copying into staging is not admission. A rule is **admitted** by copying it into `~/.grok/rules/`; Grok loads every `*.md` there. There is no `@import` and no `canon.md`. In the trivial sense, file-first is this: the file is the admission.
- Preserve source-relative names under each destination.
- A skill, a command, or an agent is not admitted by a copy into `rules/`.
- Do not drop keys from a transposed command at install time.
- Reference material is copied with the rule that cites it and is read on that rule's terms. Presence does not load it.
- Destinations and same-name behavior are `README.md` § Where the pieces go and `README.md` § Discovery.

## Refreshing through staging

Begin each refresh from the new source artifact. Reapply only the local corrections that remain necessary. Do not merge old local prose wholesale into the new source.

1. Refresh the clone and record the revision, or a content digest where no stable revision exists. One tree, one copy, one line; keep it outside the resident canon.
2. Rebuild `~/.grok/corpus/staging/` as a clean copy of that clone. Do not reuse a previous staging tree. Keep no resident artifact there. Preserve source-relative paths for the release's root rules, reference material, skills, and commands.
3. Overlay `src/agents/*.md` onto the staged custom-agent surface. Deploy that transposed markdown. Do not also copy root `agents/*.md`. Inspect each definition for Grok-specific conflicts before selecting it.
4. Overlay `src/commands/*.md` onto the staged command surface. Deploy that transposed markdown. Do not also copy root `commands/*.md`. Inspect each command before selecting it.
5. Copy selected skill directories unchanged only when this install is standing up a Grok skill tree (scenario 1, or a skill that needs a Grok body). Otherwise skip.
6. Apply only necessary Grok corrections in staging. Keep the local instance input outside the staging tree and curate the staged instance file from it. A refresh must not overwrite installation facts.
7. Diff staged carries and amendments against their release counterparts, ignoring whitespace first and then ordinarily. Account for every surviving delta. Reject reflow and collateral edits.
8. Promote only validated staged outputs to the destinations in `README.md` § Where the pieces go, under the same-name behavior in `README.md` § Discovery. Do not copy the whole checkout. Do not delete unselected resident files. Do not edit the adopter's `AGENTS.md` (user or project). Update the non-resident adoption ledger with source identity and retained corrections.
9. Run `grok inspect` and confirm the selected rules, skills, commands, and agents are discovered. A second deployment with unchanged staged outputs must change nothing.

## Touching live Grok configuration

This package may add files under `~/.grok/rules/`, `~/.grok/skills/`, `~/.grok/commands/`, `~/.grok/agents/`, and `~/.grok/corpus/` for non-scanned reference. Those directories can collide with configuration the user depends on.

- Never write the adopter's `AGENTS.md` (user or project). Do not treat it as an install target, a merge target, or a prerequisite. Do not create one to make the install look complete, and do not edit one on refresh.
- The default path requires no edit to `config.toml`. Setting a `compat.claude.*` cell to `false` is an authorized overlay when a Grok-only copy of that surface is wanted. That overlay is not required to install. Inspect the cells before proposing that edit. Do not flip a cell as part of a silent install. Obtain authorization.

1. Resolve the active Grok home. Do not assume `~/.grok`; `GROK_HOME` may point elsewhere.
2. Inspect the complete target and the configuration around it before proposing an edit. Check whether a skill, command, or agent already claims the name a definition declares.
3. Explain material conflicts and obtain explicit user authorization for the proposed live changes, plus any filesystem or destructive-action approval the environment requires.
4. Merge minimally: add new files. Never replace a whole configuration file the installation already owns.
5. Preserve unrelated content, comments, ordering conventions, and stricter safety settings.
6. Validate discovery with `grok inspect`. Report applied, skipped, deferred, and conflicting items separately.

Superseded configuration is removed only as part of an authorized migration. `../../rules/caselaw.md` `⊨3` requires a replacement to purge the replaced thing's whole footprint. Inspect the live installation to establish that footprint before the purge. A manifest does not establish it.

## What `src/` holds

- There are no per-artifact transposition recipes, and none are planned. Corpus sources contain `{placeholders}` for whatever an installation names for itself. The instance file does the naming once.
- `src/instance-example.md` is the one file copied out and refactored. It is not installed as it stands.
- Transposed agents are generated into the published tree at `transforms/grok/src/agents/*.md` by `transpose_agent.py`. Transposed commands are generated into the published tree at `transforms/grok/src/commands/*.md` by `transpose_command.py`. Both generators are unpublished build tooling: an adopter does not run them and installs the markdown they emitted.
- There is no hooks directory.
- Read each set from its directory. A list here would go stale by omission the moment either set changed.
- Read each definition before installing it. Install it as it stands unless it depends on a harness particular Grok lacks.
