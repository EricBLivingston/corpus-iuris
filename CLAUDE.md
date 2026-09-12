# Repository Guide

This repository is source material for Corpus Iuris and its harness transforms. Cloning or reading it does not install or admit any provision into the reader's agent configuration.

## Claude Code adoption

When the user asks to adopt or configure this corpus for Claude Code:

1. Read `README.md` for what the corpus is, `adopting.md` for which provisions to take and how to key over what does not fit, and `installing.md` for where each piece goes and how it gets there.
2. Inspect the live Claude Code configuration read-only, report the proposed changes and conflicts, and obtain explicit user authorization before writing outside this clone.
3. If authorized, copy per `installing.md`, then write the installation's instance file from `instance-example.md` into `~/.claude/rules/`. It goes in after the copy rather than before it, for the reason `installing.md` § What you supply gives. A file copied into `~/.claude/rules/` without `paths` frontmatter is resident at the next session start, so the copy is the admission and no later step will hold it.

Work inside a `transforms/<harness>/` subtree is governed by the `AGENTS.md` sitting there, which Claude Code does not load on its own. Read it before editing that subtree.

For other work, follow the user's requested scope.
