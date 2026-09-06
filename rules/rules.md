# Universal Behavioral Rules

**※0. *Quo praecepto? Cita prius*** — Before acting, cite every precept that altered your plan of action, each with a short impact statement, under the label *Quo praecepto*. A provision cites by token; a precept carrying none cites by the hardest handle it affords — rubric by its heading-form target, adventitia by the shortest fragment that resolves it. A diagnostic of precept efficacy, not a compliance record: an unaltered act cites nothing. Report deviations. e.g. `Quo praecepto: ⊨5 — main session, no analyzer; CLAUDE.md § MANDATE: No Broad Home-Directory Scans — search scoped to the project.`

**※1. Tool Correctness** — Prefer an applicable non-shell harness-provided tool over a shell stand-in for every file operation (abides ※11). Shell operations can consume disproportionate time and tokens. Reserve the shell for operations that genuinely require it, or if explicitly instructed.

**※2. No Recursive Self-Launch** — Invoke same-system subagents exclusively through the harness’s subagent workflow. Never launch the current agent system recursively through a shell or CLI stand-in: it creates an unmanaged second main session, floods context with stdout, and defeats delegation (※4).

**※3. Async Agent Channels** — After invoking a background agent, stop processing and quiesce: the harness will notify on completion. Do not poll or start redundant agents thinking the first failed; ※11 and risk of conflicting work. However, notification is not proof of completion: confirm the deliverable is on disk. A notification can fire mid-write or land in another agent's context.

**※4. 2-File Rule** — Any work involving 2+ files MUST be delegated to agents from the main session (mandatory, not advisory); a subagent already holding the work does it rather than re-delegating. Delegating preserves main context by keeping file content in the agent's context window, allowing the main conversation to stay focused on orchestration.

**※5. Progressive Disclosure** — Start with the least content that does the job; add only what a reader demonstrably needs. Detail that only specific contexts require extracts to a file loaded on demand rather than sitting in content read every session. Applies wherever content carries a load cost.

**※6. Memory Curation** — Read memory progressively, loading only material relevant to the current task (※5). Route memory writes, consolidation, and durable-knowledge promotion to the knowledge agent; the main session identifies what to retain but does not curate the memory subsystem.

**※7. Never Read Agent/Skill Definition Files in the Main Session** — Doing so pollutes main context with content that should be loaded using the proper harness mechanisms, which ensures context insertion occurs appropriately (*e.g.*, within a subagent context).

**※8. Production Workflow Chain** — Non-trivial work runs the pipeline in this order: the analyzer agent, then the coder agent, then the reviewer agent, then the tester agent, whose verification must include the §16 cross-boundary end-to-end gate. **The reviewer is never skippable** — skipping it for "small" changes has been a consistent source of defects, and that holds for every non-code refactor. Analyze and Test may be skipped only when there are no artifacts on which to operate (*e.g.*, an empty directory), or when the work is non-code-only *and* an associated plan or phase file states no analysis or testing is needed. Meta-artifacts created by the workflow are not subject to the workflow (no recursion).

**※9. Version Control** — Read-only Git commands are encouraged. Do not run mutating Git commands unless the user explicitly requests it. The user reviews, refines, and commits manually.

**※10. Leave It Better Than You Found It** — (Boy Scout Rule) Sweep into scope any small, atomic, low-risk fix opportunities, such as stale comments, resolved TODOs, dead imports, typos, obsolete flag checks, obvious local renames, etc. Do not mark them "out of scope" which causes small items to evaporate; the comprehension tax on the next reader is paid again and again. **Does not apply to anything requiring analysis or multi-point refactoring**. Never withhold a file from scrutiny because it was just written or reviewed. A carve-out is admissible only as a refinement of a sweep's own keep/cut rule, evaluated per site and justified by the file's role, never by when it was last touched.

**※11. Every Token Counts** — Aggressive brevity. Do not restate unnecessarily. No tautologies ("Escalate what warrants escalation"). No trivialities ("`src/` contains source code"). No unrequested tutorials ("How to use logging.Logger"). No narration ("I'll now read the file and check X"). No compliance recitation (quoting a rule back to prove you followed it). Think Tamarian: fewest tokens to *evoke* maximum *model* understanding.

**※12. Work Scope and Governance** — Work you were not explicitly asked for (anything at least one generation removed from your charter) must be bounded and refereed: use governing-work. A request to expand those bounds must be authorized: use performing-fmea.

**※13. Context-Free Subagents** — A **context-free subagent** starts with only the harness system prompt, environment metadata, and the skills/tools registry; every other subagent, built-in or custom, inherits the full `{core-rubric}` and rules chain. Reserve the context-free ones for operations needing zero context from this ecosystem — a "where is X" lookup with the target fully specified, standalone planning that turns on no convention — and inline every fact the prompt needs. Anything turning on §, ※, delegate or MCP-tool routing, or project paths goes to a subagent that inherits; in doubt, so does everything else.
