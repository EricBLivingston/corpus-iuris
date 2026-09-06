# Ius

**Corpus**: all live content — code, tests, docs, or adventitia. The live collection, not the repository: content is live where something reaches it — a loader (residency, import, path rule, or harness injection), an invoker (a command, skill, agent, or script naming it), or a reference from something itself live. Archived, superseded, and unreached content is dead code, and dead code is not corpus.

**Precepts**: all corpus that binds.

**Canon**: precepts whose presence is guaranteed for the readers they bind — by residency, import, path rule, or harness insertion. Presence admits, not merit; a citation to canon always resolves in context. What lies outside is deuterocanonical rather than apocryphal — it binds once read.

**Provisions**: canon's instrument-labelled precepts (`§`, `※`, `⊢`, `⊨`), each at its defining site.

**Doctrine**: the set of all provisions.

**Rubric**: the rest of canon. It instructs or prescribes procedure without minting a provision.

**Adventitia**: rubric the harness supplies rather than we author: e.g., system and session prompts, built-in tool descriptions, plugin and MCP-server instructions. A provenance label only: it binds as other rubric.

## The instruments and their prefix symbols

**§ directives** — what you produce.
**※ rules** — how you work.
**⊢ interpretive rulings** — reconciles a priori logic conflicts and silences in doctrine.
**⊨ empirical resolutions** — the same office, a posteriori, surfaced in application.

## Senses

Each term takes one field's sense, not the nearest one.

- **Instrument** — the statutory sense: a class of enactment, not a single document.
- **Provision** — the statutory sense: a discrete, citable clause.
- **Rubric** — the liturgical sense: the red-letter directions for performing the rite, as against the words of the rite.
- **Adventitia** — the Cartesian sense: *ideae adventitiae*, ideas arriving from outside the mind, neither innate nor self-made. What one authors one may edit; the adventitious admit only adoption or rejection.
- **Doctrine** — principle systematized out of accumulated experience. Each provision is an a posteriori remediation of an observed failure.
- **Caselaw** — the litigants are the colliding provisions; the bench is the author and the model, arguing to a holding; the holding is codified here. A ruling is amended by rewriting it.
- **Peritus** — the civil-law sense: the expert a tribunal appoints and questions, not the expert witness a party retains and an opponent cross-examines. It answers what is asked; the tribunal weighs the answer and is not bound by it.
- **Responsum** — the Roman-law sense: *responsa prudentium*, a jurist's written answer to the question as put. Its authority is the answerer's standing; its scope is no wider than the question.

Within the ius regime (not bound thusly in non-canon corpus):

- `※` — promoted from annotation to obligation. Nothing prefixed by it is optional or parenthetical.
- `§` — resolves to directives.
- `⊢` `⊨` — prefixes, not infix operators; left operands move to the entry's `Governs:` line.

## Token grammar

A provision's token has four positions:

```text
{instrument}{ambit}{lingua}{number}
```

| Position | Values | Blank means |
| ---- | ---- | ---- |
| **Instrument** | `§`, `※`, `⊢`, `⊨` | — always present |
| **Ambit** | `A` agent, `P` project, `I` instance | universal |
| **Lingua** | a lowercase language tag, e.g. `md`, `py`, `rs` | all content, whatever the syntax |
| **Number** | 1-based within its namespace | — always present |

`§5` is a universal directive over all content. `§md2` is universal, in the Markdown lingua. `§I7` binds one installation across all linguae; `§Ipy4` binds one installation's Python. `※A3` is one agent's own rule.

### Ambit

| Ambit | Reach |
| ---- | ---- |
| Universal | every installation of the corpus |
| Instance | one installation — a machine, a deployment, one peritus's whole environment |
| Project | one project |
| Agent | one agent |

Ambit files carry rubric as well as provisions.

Instance is to one installation what Project is to one project. It outranks the universal ambit because it exists to override it, and yields to Project and Agent so a single project or agent can still deviate from an installation-wide decision. An Instance provision takes one of two forms:

- **Keyed** — headed by an existing universal token, which it overlays for this installation. The token keeps its number; location decides the ambit.
- **Minted** — a fresh token in the `I` ambit, numbered from 1, for a provision the universal ambit does not supply at all.

### Lingua

A lingua proxies a language by membership, not extension string: `§cc` reaches `.cc`, `.cpp`, `.h` and every other C/C++ source. In use: `py` Python, `rs` Rust, `md` Markdown; a lingua's namespace is defined in canon: `reference/standards/<language>/principles.md` or rules/*.

A lingua's provisions are deuterocanonical but considered canon for the purposes of ius. It is expected and directed that projects ensure harnesses auto-load appropriate lingua doctrine, per-session.

## Precedence: *lex specialis*

1. User Instructions
2. Doctrine
3. Rubric
4. Remaining precepts

User Instructions are the live instruction of the session. Not corpus: standing instruction, once written down, is precept and takes its precept rank.

Within [2, 3, 4], the more specific governs: by ambit first — Agent, then Project, then Instance, then Universal — and within one ambit, a named lingua beats a blank one. Location decides ambit where there is no instrument.

Clarifications:

- A keyed provision overlays its base rather than displacing it, at every ambit: what does not conflict passes through, what conflicts is replaced, and silence is filled. A bare token resolves to its base as overlaid by each keyed entry above it in precedence.
- Instance provisions may replace, amend, or disable anything in the universal ambit.
- Project provisions may replace or amend anything in their base namespace, and a project's own rules files may do so in place.
- Project caselaw may compose any doctrine.
- Agent provisions carry the reach of Project provisions, and may act upon Project provisions as well. Minted in an agent's own definition file, they bind that agent's conduct alone; they are not visible to invokers or invokees.
- Precedence ≠ severity/authority. Uncontested rubric carries the same authority as a provision. Provisions are minted mainly to prevail in a collision, and for citability outside canon.
