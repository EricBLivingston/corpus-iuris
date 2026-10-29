# File Rules

The `{File Rules}` block substituted verbatim into each specialist prompt beside it. Consumer: `commands/orchestrate.md` § 3.

```text
File rules: the run's records stay within {Project Path}: each report at {Project Path}/Phase-X-{Subject}.md. Under {Project Path}/tests/ keep only the record of a non-repeatable event a report cites (a real-data build's log lines, a deployment's verification, a digest, the script that produced one); a repeatable run's output (a test tier, the lint gate, a retest) is reported by its counts and not kept, so run it from the session scratchpad. The records are reviewed and archived with the plan, so none goes to {analysis-root}/ or /tmp.
```
