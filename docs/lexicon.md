# Why the Latin, and the odd symbols

This page is the long form of [the lexicon section of the README](../README.md). It covers the two properties every term and symbol here was selected for, the failure at each end of that selection, and the table of what each one was chosen to carry.

We are not trying to be pretentious or pedantic. We select for two properties, and both do the same job: minimizing competition for the referent.

## Rarity: one antecedent in context

A token like `※11` is not reaching into training data for its meaning. Its definition is already in context, loaded at session start, and the token's whole job is to be a bright, unambiguous path back to that defining site.

That resolution is a mechanical operation. The model scans the context for previous occurrences of the current token and attends to what followed them: prefix matching, the induction-head circuit. It matches on the exact token, and its precision degrades as that token accumulates prior occurrences pulling toward different continuations.

So we seek terms and symbols that are:

1. **Rare in our own authored artifacts** (documentation, source, prose, commit messages), so nothing in the working context competes to be the match.
2. **Rare in ordinary technical usage**, so nothing the harness injects, and no training data, competes either.

`※11` has one antecedent in a session: its provision. A word like "rule" or "scope" has dozens, each pulling somewhere else.

That count is what has to survive scaling up. Attention is a fixed budget, and softmax spreads it thinner across everything present as a window fills; accuracy falls with context length on its own. Nor does irrelevant material sit inertly beside the signal; it competes for attention. Retrieval that can lean on a literal token match holds up under that pressure, while retrieval working by resemblance degrades sharply as the haystack grows.

`※11` has one antecedent at 8k and one at 500k. The count does not grow with the window, so the path back to the ius stays as bright at the top of the range as at the bottom. "Scope" might have thirty antecedents at 8k and hundreds at 500k, and is lost in exactly the sea of context we are trying to stay out of.

### The Goldilocks zone

Rarity has a floor as well as a ceiling. A term too common competes for its own referent; a token too rare is *undertrained*, vocabulary entries a model has barely seen carrying degenerate embeddings and behaving erratically. This is why we do not just make up nonsense words. We want a term rare enough to be unambiguous, but not so rare that it is untrained.

## Semantic alignment: no fight with the prior

Where a term *does* occur in training data, its sense there should be close to ours.

A term whose trained default contradicts our stipulated use sets what the context says against what the weights expect, and that conflict resolves unreliably. Operating against a trained default is also expensive; the same task gets worse when familiar terms are given unfamiliar meanings.

So we avoid that fight rather than trying to win it. Where the prior already agrees, term fidelity comes free: `provision` means a discrete citable clause in ordinary legal use, so nothing has to be overridden.

Alignment also buys compression. A trained name arrives carrying its own frame, and *peritus*, *ultra vires* and *rubric* each retrieve in one word what would otherwise cost a paragraph of stipulation.

## The ladder we are climbing

Precision of reference has rungs:

1. **No rules at all: ad hoc** — "When writing this, make sure not to introduce functions and things we don't need right now. Keep it to just what we discussed and no more" (and variations repeated time and time again)
2. **Rule defined in general terms** — "When writing this, remember our Rule about going out of scope"
3. **Precept defined rigorously** — "Abide by §2" (often not needed, but sometimes worth reinforcement)

The whole apparatus exists to make the third rung available at the cost of the first.

## The terms and symbols, and what each was chosen for

The terms below are also a taxonomy: they sort what binds from what does not, and what is guaranteed present from what binds only once read. That sorting is drawn on its own sheet, and the ranking it feeds is covered in [the structure page](structure.md).

![Corpus, precepts, canon, doctrine, rubric and adventitia, and what falls outside](diagrams/corpus-taxonomy.svg)

| Term / Symbol | Typical Definition | How we leverage that in our own usage |
| ---- | ---- | ---- |
| **Ius** | Roman law: law as a body of right (*ius civile*), as against *lex*, the single enacted statute. | Names our body of rules as a whole, so no one rule can be mistaken for the whole. |
| **Corpus** | In scholarly publishing, the live collection, with withdrawn and archived material excluded by definition; in ML, a curated dataset, where membership follows from active inclusion rather than mere availability. | Membership by inclusion, not by presence on disk: what no loader, invoker, or live reference reaches is dead code, and dead code is not corpus. |
| **Adventitia** | Latin: "externally added"; Descartes' *ideae adventitiae*, ideas arriving from outside the mind — neither innate nor self-made. | Marks rubric the harness supplies. It is a provenance decorator, and does not affect authority. |
| **Precept** | A rule of conduct laid down by an authority. | The umbrella for everything that binds, whichever instrument minted it. |
| **Canon** | The closed, admitted set of texts constituting a body — always read, as against material that may be read but is not guaranteed. | Admission by guaranteed presence, so a citation always resolves in context; what lies outside is deuterocanonical, and binds once read. |
| **Provision** | A clause of a statute or contract: a discrete, citable term. | A uniquely labeled precept, so it can be cited from anywhere instead of quoted as text. |
| **Doctrine** | Legal doctrine: the systematized principles of a field, accreted through commentary and experience rather than enacted a priori. | Signals that nothing here was reasoned out in advance; each provision represents an a posteriori remediation. |
| **Rubric** | Liturgical rubric: the red-letter directions governing how the rite is performed, as against the words of the rite. | Separates procedure from the precepts it carries out: rubric instructs without minting anything citable. |
| **Caselaw** | Judge-made law: rules established in deciding cases, binding later ones through *stare decisis*. | A collision between provisions is decided once, and the holding binds every later reading. |
| **Instrument** | Legal instrument: the vehicle creating or recording an obligation; a *statutory instrument* is a whole class of enactment. | Names which of the four provision classes a specific provision falls within. |
| **Ambit** | The scope or reach of a rule: "within the ambit of the statute". | The reach position in a provision token: universal, one installation, one project, or one agent. |
| **Lingua** | Latin: tongue, a language as such. | Scopes a provision to a language by membership, so `cc` reaches `.cc`, `.cpp`, and `.h` alike. |
| ***Lex specialis*** | *Lex specialis derogat legi generali* — the specific rule displaces the general one. | Adopted intact as the precedence rule; the ambit ladder supplies the ranking it needs. |
| **Peritus** | Later civil and canon law: the expert a tribunal engages for an opinion it cannot reach itself. | An external AI model, engaged for peritia (skills, expertise, etc.) this session lacks. |
| **Responsum** | Roman law: *responsa prudentium*, a jurist's written answer to the question as put, carrying the answerer's standing rather than an office's. | What a peritus returns, one per engagement, weighed against the artifact it claims and reaching no wider than the question asked. |
| **Charter** | A founding instrument conferring powers on a body, and the measure of what that body may do. | The grant a piece of work runs under: the ask, the dispatch prompt, the plan and its ratified bounds, and any authorization issued under `※12`, together with the author who granted it. |
| **Ultra vires** | Public law: an act beyond the powers conferred, void for want of authority rather than condemned on its merits. | Names an act that would put more work under a charter than the charter granted, and says nothing about whether the act was warranted. |
| **ATO** | Risk management: authority to operate, an authorizing official's signed acceptance of the residual risk a documented assessment leaves. | The row an Authorizing Official fills in the statement of assumed risk, and the thing an ultra vires act waits on before it starts. |
| **FMEA** | Failure mode and effects analysis: the reliability method out of military and aerospace practice, which enumerates how a thing can fail, grades each mode on severity, occurrence and detection, and acts on what scores. | A reader who knows the method arrives already holding the grading discipline the assay runs on. We keep its three limbs and add recovery. What we discard is the apparatus: no ordinal scales, no risk-priority number and no worksheet, because what is graded here is the decision to spend rather than a product's reliability. |
| `§` | Section sign (silcrow): marks a numbered section or clause of a statute, contract, or treatise. | Statutory weight, plus an address: `§4` resolves corpus-wide, never to nearby prose. |
| `※` | Kome / reference mark: in Japanese and Chinese typography, prefixes a note the reader must not miss. | Rare enough to arrest attention, and promoted from annotation to obligation: nothing it prefixes is optional. |
| `⊢` `⊨` | Turnstiles: `Γ ⊢ φ`, "φ is derivable from Γ"; `M ⊨ φ`, "φ holds in model M". | The distinction carries over intact: `⊢` is derivable a priori from the provisions in hand, `⊨` needs a posteriori experience to show it. |
| `⊬` `⊭` | The negated turnstiles: `Γ ⊬ φ`, "φ is not derivable from Γ"; `M ⊭ φ`, "φ does not hold in M". | Negation prefixes taking the site they sit on as the left operand, so `⊬§13` on a precept exempts that precept from `§13`. |

Most of this vocabulary never leaves the ius. In ordinary use only the symbols surface, plus the occasional category name ("scan for doctrine violations"), while the rest works internally, resolving context rather than being recited.

The definitions above are what the terms were selected for. What each one binds is set in `rules/ius.md`, which is where the corpus states them for itself.

## Related pages

- [The structure](structure.md): the four positions of a token, the ambit ladder, and how two precepts rank when they collide.
- [The references](references.md): the published work behind each claim on this page.
