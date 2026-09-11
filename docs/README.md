# Docs

Presentation and explanatory material about the corpus. It exists to explain the body to someone who has not read it.

## Pages

The README is the front door and each of its sections is deliberately short. Every section that introduces a layer has a page here that goes into it, named for its subject and titled with it, and each explains a mechanism rather than restating the file that governs it. [`references.md`](references.md) stands outside that pattern, carrying the published work behind every empirical claim the corpus makes about model behavior.

## Logo

`logo.svg` is the mark: the four instruments, quartered. `§` blue, `※` red, the turnstiles in ink. The glyphs are outlined paths, so the mark renders identically everywhere with no font dependency, adapts to light and dark the same way the diagrams do, and stays legible down to favicon size. In the deck it pairs with the wordmark as the running kicker on every slide, and serves as the favicon.

## Diagrams

`diagrams/` holds standalone SVGs, each named for its subject, carrying its own `<title>`, theme-aware through `prefers-color-scheme`, and embedded where the prose goes into its subject.

The two `framework-*` files answer the same question at opposite ends of the vocabulary, and are deliberately built differently so neither reads as a version of the other. `framework-in-brief.svg` is two panels and no jargon, for someone who has not been given a single term yet. `framework-overview.svg` is the dense one, and works alone as a README hero, a share image, or a printed handout. The rest each take one part of that detailed sheet further.

Embed one in Markdown the usual way. This path is written from the repository root:

```md
![The spec-driven development pipeline](docs/diagrams/sdd-pipeline.svg)
```

The remaining diagrams are authored as Mermaid rather than as SVGs, inline in the page that explains them, because those flows are worth keeping editable beside the prose that walks them.

## Deck

`deck/index.html` is a self-contained talk deck for a general developer audience. It references the diagrams by relative path, so the SVGs stay the single source of truth and editing one updates the slide that carries it.

Open the file directly, or serve `docs/` and point a browser at `deck/`. Keys: `←` `→` to move, `N` to toggle speaker notes, `Home` and `End` to jump. Clicking the left quarter of the window goes back, anywhere else advances. The URL fragment tracks the slide, so a link can open on a given one.

The deck leads with what the system does and keeps the supporting research to a closing appendix.

The two `sheet`-class slides bookend the talk: the plain-language sheet up front as a map, the detailed one at the end as a callback, once the vocabulary has been earned.
