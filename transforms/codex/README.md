# Codex Transform

This package turns the shared Corpus Iuris sources into a coherent Codex installation. It ships no replacement for a user's live Codex configuration: what it installs is merged into whatever that home already holds. `AGENTS.md` beside this file governs work performed inside the transform.

## For an adopting Codex

This repository is designed to guide its own adoption. When a user points Codex at the repository URL, the expected journey is:

1. Obtain a local working copy and read the root `README.md`, `adopting.md`, this file, and `AGENTS.md`.
2. Inspect the active Codex home and current official Codex documentation read-only. Identify active configuration layers, existing hooks, collisions, and required destinations.
3. Report the proposed bootstrap and ask the user explicitly before writing to user-level Codex configuration.
4. With approval, install and register only the inert SessionStart loader, `src/hooks/corpus_iuris_session_start.py`. Do not create or populate `canon.md` merely to make the hook appear complete.
5. Copy the corpus into the production corpus root, preserving source-relative paths. The corpus is this repository's artifact tree — every directory whose contents an admission could name — as against the documents at the repository root, which are read rather than installed. Copying admits nothing: nothing loads until it is imported.
6. Write the installation's instance file: copy `src/instance-example.md` to `rules/instance.md` inside the production corpus root and refactor it for this installation — after the copy above rather than before it, or the copy lands on top of it. It resolves the `{placeholders}` and the generic slots every other file leaves open; the doctrinal core carries unchanged behind it.
7. Admit rules one at a time, each by an `@import` line in `canon.md` written after its file is in place. `AGENTS.md § Rule admission` gives the order and why it is not negotiable.
8. Install the custom-agent definitions from `src/agents/` where Codex discovers them, reviewing each one first.

The working clone, the installed corpus, and the user's live Codex configuration are separate surfaces. An agent must not treat repository presence as installation or admission, and pulling the clone must not change resident context.

## Where the pieces go

| Piece | Destination |
| ---- | ---- |
| the corpus tree | the production corpus root |
| the instance file, refactored from `src/instance-example.md` | `rules/instance.md` inside that root |
| the SessionStart loader | wherever the active Codex home registers hooks |
| each definition in `src/agents/` | where Codex discovers custom agents |
| each skill directory in `skills/` | `<codex-home>/skills/<name>/` |
| each `<name>.md` in `commands/` | `<codex-home>/skills/<name>/SKILL.md` (needs conversion from stand-alone file to skill folder) |
| an admission | an `@import` line in `canon.md` naming the artifact's path |

The loader takes the Codex home from `CODEX_HOME`, falling back to the parent of the directory it sits in — so leaving `CODEX_HOME` unset is correct only where the loader lives one level below the Codex home, as `<codex-home>/hooks/`. Set it explicitly for any other placement: a Codex home resolved one level too high finds no `canon.md` and exits successfully with no output, which is indistinguishable from the empty-canon state below. It takes the corpus root from `CORPUS_IURIS_ROOT`, falling back to `<codex-home>/corpus`. The production root may live wherever the installation chooses; set `CORPUS_IURIS_ROOT` rather than deriving a path from the checkout, and do not place local artifacts inside an update-managed checkout.

The loader expands two entrypoints. `<codex-home>/canon.md` is read in every session. `<project-root>/.codex/canon.md` — the project root being the nearest ancestor of the session's working directory that holds a `.git` — is read only in sessions under that project, and is the surface a `P`-ambit file reaches. A project entrypoint's imports resolve inside its own `.codex/` directory and may not escape it, so a project's corpus files live there beside it.

Codex discovers custom agents at `<codex-home>/agents/*.toml` for a personal installation, or `.codex/agents/*.toml` for one project: one file per agent, and the `name` key inside the file is the identifier rather than the filename. That is Codex's own admission channel — an agent definition takes it instead of a `canon.md` import, never both.

## Initial scope

The first cut covers the corpus files this repository publishes — the tree as it stands beside this transform is the set, and this file does not restate its membership.

That set's doctrinal core carries rather than being corrected provision by provision. The upstream refactor moved the harness particulars out of those files and into the instance ambit, so what a Codex installation owes them is not a corrected copy but an instance file naming its own referents; this transform ships an example rather than a filled one. Custom-agent definitions are neither deferred nor authored here: they arrive already transposed, per AGENTS.md § What `src/` holds. Skills are native Codex discovery artifacts: an installation that selects one copies its directory unchanged to `<codex-home>/skills/<name>/`. Every other artifact an admitted source merely names remains a deferred dependency.

## Why the bootstrap is safe

Install and register the user-level SessionStart loader before admitting any doctrine. With no `canon.md`, or with an empty one, the loader exits successfully without output: it injects no context and surfaces no warning. This is the safe initial state, and an artifact admitted later becomes resident at the next matching session start.

A non-empty canon that is malformed, incomplete, cyclic, unreadable, or over budget fails closed, as does one whose imports resolve outside the corpus root: no partial doctrine is injected, and Codex surfaces a warning.

## The baseline stands alone

The baseline must work without optional MCP servers, private skills, custom agents, or trusted project hooks. The supplied loader is inert infrastructure until imports are added, and an optional capability may enhance the installation only where its absence has an explicit fallback.

## Codex references

- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## Source provenance

The public transform is authored in a private publish staging tree and promoted into this repository after review. That maintainer publication pipeline is not the adopter's workflow: adopters work from their clone and promote vetted artifacts into their own installed corpus as described above.
