# Grok Transposition Guide

This guide is working discipline for the Grok transform: what may change on the way from the shared sources into a live Grok installation, and how a live Grok home is touched. The guide itself is not part of the installed corpus. It is not an install target for an adopter's `AGENTS.md`. `README.md` carries the adoption sequence.

## Scope

This is a maintained downstream realization of a live upstream corpus, not a one-time port. Resynchronization after upstream changes is normal operating procedure, so **minimum-necessary change** is the governing criterion: every edit to a copied file is a divergence that must be reconciled at every later refresh, and must earn that permanent cost. An installation's own facts belong in its instance file, where a keyed entry merges with a later upstream revision instead of colliding with it.

- Work only from sources present in this clone. A missing source is deferred, not reconstructed from memory or another installation.
- Staging, `~/.grok/corpus/staging/`, is a fourth surface beside the three `README.md § For an adopting Grok` separates. Rebuild it from the checkout for every refresh; it is disposable processing material, never scanned, never canon.
- Writing outside the clone, or changing user-level Grok configuration, requires explicit user authorization. Filesystem approval from the harness does not replace that conversation.
- Style, wording preference, exposition, clarification, and cosmetic consistency never justify a delta. Preserve formatting; do not reflow carried text.
- Prefer deleting or narrowly substituting a false clause over rewriting its sentence, paragraph, or section.
- Do not add caveats that restate immutable harness or model bounds, including instruction priority. Translate only mechanics that must change for the provision's intended behavior to survive.
- Keep doctrine declarative: state what binds, not how it is authored, admitted, loaded, or maintained. Those procedures belong in a guide like this one or in a context-curation skill, not in the statute they operate on.
- Use current Grok Build documentation for the surfaces this package touches: rules directories, skills, subagents, and `compat.claude`.

## Admit or defer

Corpus files are copied verbatim, `{placeholders}` and all, and the instance file resolves the placeholders once for every file that writes them. Copying into staging is not admission. A staged rule is **admitted** when it is copied into `~/.grok/rules/`; Grok loads every `*.md` there. There is no `@import` and no `canon.md`. File-first still holds in the trivial sense: the file is the admission.

Defer is the half that carries weight. **Defer** means do not copy into a scanned directory. Treat a reference to an unavailable skill, agent, MCP server, or reference file as a deferred dependency rather than as grounds to withhold or alter the referring content. Once the planned corpus is fully loaded, sweep its citations and resolve only what remains unresolved there.

A provision that is merely generic where Grok is specific, or that Grok contradicts outright, is neither deferred nor edited: it takes a keyed entry in the installation's instance file, which keeps its number resolvable on both sides. `../../adopting.md § Taking a provision you do not want as written` sets that route against its alternatives and gives the cost of each.

Amending a copied file is the escape hatch, and it should stay empty. A span Grok makes factually false — a tool named as a literal, an interaction model no keyed entry can reach — is upstream's defect rather than this installation's: it is wrong on every harness that is not the one it was written for, so report it upstream. Correct it locally only where waiting is not an option, confine the correction to the false span, and drop it when the upstream fix lands.

## Rule admission

A file nothing loads binds nothing. Admitting a rule is one copy into a directory Grok's rules scanner will load:

| Product | Destination |
| ---- | ---- |
| a selected rule | `~/.grok/rules/` — copying it is the admission |
| a skill directory | `~/.grok/skills/<name>/`, unchanged |
| a transposed command | `~/.grok/commands/` |
| a transposed agent | `~/.grok/agents/` |
| reference material | `~/.grok/corpus/reference/` — present, not loaded |

Preserve source-relative names under each destination so every later refresh is a diff rather than a hunt. Dual-home does not recopy rules or skills already loaded from `~/.claude/` through `compat.claude`. Transposed commands install into `~/.grok/commands/` so they shadow the Claude copies. Inspect collisions by name before installing; a name collision is a discovery conflict — report it, then skip or add a new directory; do not patch the occupant.

Reference material is copied with the rule that reaches it, but is read on that rule's terms rather than loaded merely because it is present. Do not place it in `rules/`.

A skill takes Grok's discovery admission instead of a rules copy. A command stays a command: deploy `src/commands/`, generated by `transpose_command.py` in the publish build; do not recopy corpus `commands/` and do not drop keys at install time. An agent takes Grok's agent-discovery channel — the transposed markdown in `src/agents/` — never a rules copy.

## Refreshing through staging

A refresh is a staged deployment: source files are carried into a clean staging tree, Grok-specific changes are made there, and only validated outputs reach the installation. Begin from the new source artifact and reapply only the local corrections that remain necessary; never merge old local prose wholesale into a new source.

1. Refresh the clone and record the revision, or a content digest where no stable revision exists. One tree, one copy, one line; keep it outside the resident canon.
2. Rebuild `~/.grok/corpus/staging/` as a clean copy of that clone. Do not reuse a previous staging tree or keep a resident artifact there. Preserve source-relative paths for the release's root rules, reference material, skills, and commands.
3. Overlay `src/agents/*.md` onto the staged custom-agent surface. These are the Grok-ready transpositions of root `agents/*.md`, generated by `transpose_agent.py` in the publish build; deploy the transposed markdown, not a second copy of the corpus sources. Inspect each definition for Grok-specific conflicts before selecting it.
4. Overlay `src/commands/*.md` onto the staged command surface. These are the Grok-ready transpositions of root `commands/*.md`, generated by `transpose_command.py` in the publish build; deploy the transposed markdown, not a second copy of the corpus sources. Inspect each command before selecting it.
5. Copy selected skill directories unchanged. Inspect each for name collisions before selecting it.
6. Apply only necessary Grok corrections in staging. Keep the local instance input outside the staging tree and curate the staged instance file from it; a refresh must not overwrite installation facts.
7. Diff staged carries and amendments against their release counterparts, ignoring whitespace first and then ordinarily. Account for every surviving delta; reject reflow and collateral edits.
8. Promote only validated staged outputs to their live destinations: selected rules to `~/.grok/rules/`, reference material to `~/.grok/corpus/reference/`, each skill directory to `~/.grok/skills/<name>/`, transposed commands to `~/.grok/commands/`, and transposed agents to `~/.grok/agents/`. Dual-home included for the two transposed surfaces. Do not copy the whole checkout and do not delete unselected resident files. Do not edit the adopter's `AGENTS.md`. Update the non-resident adoption ledger with source identity and retained corrections.
9. Run `grok inspect` and confirm the selected rules, skills, commands, and agents are discovered. A second deployment with unchanged staged outputs must change nothing.

## Touching live Grok configuration

Live destinations this package may add files under are `~/.grok/rules/`, `~/.grok/skills/`, `~/.grok/commands/`, `~/.grok/agents/`, and `~/.grok/corpus/` for non-scanned reference. They can collide with configuration the user depends on.

**Never write the adopter's `AGENTS.md`.** It is not an install target, not a merge target, and not a prerequisite. Do not create one to make the install look complete, and do not edit one on refresh. Do not require an edit to `config.toml`.

1. Resolve the active Grok home without assuming default paths. `GROK_HOME` may point elsewhere than `~/.grok`.
2. Inspect the complete target and the configuration around it before proposing an edit. Check whether a skill, command, or agent already claims the name a definition declares.
3. Explain material conflicts and obtain explicit user authorization for the proposed live changes, plus any filesystem or destructive-action approval the environment requires.
4. Merge minimally: add new files. Never replace a whole configuration file the installation already owns.
5. Preserve unrelated content, comments, ordering conventions, and stricter safety settings.
6. Validate discovery with `grok inspect`. Report applied, skipped, deferred, and conflicting items separately.

Superseded configuration is removed as part of an authorized migration and not otherwise. `../../rules/caselaw.md` `⊨3` requires that a replacement purge the replaced thing's whole footprint; what a third-party configuration adds is that the footprint has to be established by inspecting the live installation before the purge, not read off a manifest.

## What `src/` holds

There are no per-artifact transposition recipes, and none are planned: the corpus sources carry `{placeholders}` for whatever an installation names for itself, and the naming is done once, in the instance file.

`src/instance-example.md` is the one file copied out and refactored rather than installed as it stands. Transposed agents are generated into the published tree at `transforms/grok/src/agents/*.md` by `transpose_agent.py`; transposed commands into `transforms/grok/src/commands/*.md` by `transpose_command.py` — unpublished build tooling; not in the adopter's package as scripts they run. Adopters receive what the publish build emitted. There is no hooks directory. Read each set from its directory rather than from a list here, which would go stale by omission the moment either set changed. A body can still rest on a particular of the harness it was written for that Grok has no counterpart to, so read each definition before installing it; in the usual case install it as it stands.
