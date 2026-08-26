# Markdown Directives and Rules

## Directives

**§md1** — Always leave a blank line before and after: bulleted list, numbered list, fenced code block.
**§md2** — Always leave spaces surrounding table structure verticals: `| ---- | ---- | ---- |`.
**§md3** — Do not insert explicit line-breaks inside table cells. Tables should wrap with terminal width at render time.
**§md4** — Outside fenced blocks, do not break authored prose at a column boundary. A paragraph or list item is written as one line however long; a line break carries meaning or is not made.

## Rules

**※md1** — After editing Markdown, lint every changed file with a Markdown linter providing check and auto-fix modes: run check to validate, auto-fix to format. Rely on its default user-level configuration discovery — author no per-repo config and pass no config flag.
