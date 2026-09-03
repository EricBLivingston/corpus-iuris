---
name: analyzing-codebases
description: Routes codebase-scale investigation to the analyzer agent — how a system is put together, what a legacy area does, where a pattern recurs, what a migration would cost, dependency and security audits. Use when understanding must span two or more files and comprehension, not an edit, is wanted.
---

# Analyzing Codebases Skill

Delegates large-scale analysis tasks to the analyzer agent, which engages periti as a complementary analysis perspective for comprehensive codebase understanding.

---

## The Analyzer Agent's Capabilities

The analyzer agent is a specialized subagent that:

- Engages periti for second-opinion analysis and review
- Can ingest and analyze 10-100+ files simultaneously
- Identifies patterns, architecture, and relationships at scale
- Performs comprehensive audits (security, quality, performance)
- Plans migrations and large-scale refactoring
- Documents complex legacy systems

---

## Key Strength: Dual-Model Analysis

Delegating to the analyzer subagent preserves main-conversation context, and a peritus adds a second analytical lens. The analyzer can:

- Read entire subsystems (50-100 files) at once
- Find patterns across the whole codebase
- Understand complex multi-file data flows
- Compare many implementations simultaneously
- Perform system-wide audits in single pass
- Map complete dependency graphs

---

## Redirects

Hand the work elsewhere for:

- Analyzing 1-5 specific files — direct tools
- Implementing code changes — the coder agent
- Writing tests — the tester agent
- Code review of recent changes — the reviewer agent
- Finding specific symbols/functions — the symbolic toolserver directly

---

## Crafting Effective Prompts

### Include in Your Prompts

1. **Clear Objective**: What needs to be understood?
2. **Scope**: Which parts of codebase to analyze?
3. **Specific Questions**: What do you need to know?
4. **Context**: Why this analysis is needed
5. **Deliverable**: What format for findings (report, diagram, strategy, etc.)

### Good Prompt Structure

```
[Context about why analysis is needed]

Please analyze [scope - specific subsystem or entire codebase]

Focus on:
1. [Specific aspect 1]
2. [Specific aspect 2]
3. [Specific aspect 3]

Deliverable: [What format you want results in]
```
