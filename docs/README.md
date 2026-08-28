# Docs

Presentation and explanatory material about the corpus. Nothing here is corpus: no loader, invoker, or live reference reaches it, and nothing in it mints or binds. It exists to explain the body to someone who has not read it.

## Logo

`logo.svg` is the mark: the four instruments, quartered. `§` blue, `※` red, the turnstiles in ink. The glyphs are outlined paths, so the mark renders identically everywhere with no font dependency, adapts to light and dark the same way the diagrams do, and stays legible down to favicon size. In the deck it pairs with the wordmark as the running kicker on every slide, and serves as the favicon.

## Diagrams

`diagrams/` holds standalone SVGs. Each adapts to light and dark rendering through `prefers-color-scheme`, so the same file works on both GitHub themes.

| File | Shows |
| ---- | ---- |
| `framework-in-brief.svg` | The whole system as two ideas, in plain language. No Latin, no tokens, nothing to define |
| `framework-overview.svg` | The whole framework on one sheet — the three goals, the four instruments, the SDD layer |
| `token-grammar.svg` | The four positions of a provision token, and what a blank position means |
| `corpus-taxonomy.svg` | Corpus, precepts, canon, doctrine, rubric, adventitia — and what falls outside |
| `precedence.svg` | The precept ranks and the ambit ladder inside them |
| `sdd-pipeline.svg` | `/prepare` through `/finalize`, and the archive drop that keeps specs out of the pipe |
| `phase-cycle.svg` | The production chain inside one phase, its loops, and the governor gate |
| `context-narrowing.svg` | Why the orchestrator passes paths rather than content |

The two `framework-*` files answer the same question at opposite ends of the vocabulary, and are deliberately built differently so neither reads as a version of the other. `framework-in-brief.svg` is two panels and no jargon, for someone who has not been given a single term yet. `framework-overview.svg` is the dense one, and works alone as a README hero, a share image, or a printed handout. The diagrams below them each take one part of the detailed sheet further.

Embed one in Markdown the usual way. This path is written from the repository root:

```md
![The spec-driven development pipeline](docs/diagrams/sdd-pipeline.svg)
```

## Deck

`deck/index.html` is a self-contained talk deck for a general developer audience. It references the diagrams by relative path, so the SVGs stay the single source of truth and editing one updates the slide that carries it.

Open the file directly, or serve `docs/` and point a browser at `deck/`. Keys: `←` `→` to move, `N` to toggle speaker notes, `Home` and `End` to jump. Clicking the left quarter of the window goes back, anywhere else advances. The URL fragment tracks the slide, so a link can open on a given one.

The deck leads with what the system does and keeps the supporting research to a closing appendix.

The two `sheet`-class slides bookend the talk: the plain-language sheet up front as a map, the detailed one at the end as a callback, once the vocabulary has been earned. The class trades slide padding for figure area: under the default chrome a whole-sheet figure renders at about 61%, which puts its body type below 7px.
