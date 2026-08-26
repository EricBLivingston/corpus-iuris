# Gemini Model Reference

Model routing for the using-gemini skill.

## Selection

| Task | Model |
| ---- | ---- |
| Large-file analysis (>10k lines), architecture understanding, code review, second opinion | `--model {gemini-pro}` |
| Multi-document survey where the answer **must reason across the documents** | `--model {gemini-pro}` |
| Wide shallow sweep — the same question asked of many files independently | `--model {gemini-flash}` |
| Bulk mechanical edits | `--model {gemini-flash}` |
| Quick summaries, simple formatting or extraction, commit messages | `--model {gemini-flash}` |

Split on reasoning demand, not file count: a wide but shallow sweep is flash work, and a single knotty file is pro work. The two survey rows above are that rule applied — file count is identical across them and does not decide.

## Identifier Behaviour

- agy has no `auto` alias and no shorthand form; only a full roster identifier resolves.
- The effort tier is a **suffix inside the roster identifier** (`…-pro-high`, `…-flash-medium`), not a separate flag — which is why there is nothing to pass and nothing to raise.
- `{gemini-pro}` has **no** `medium` effort tier: no such identifier exists, and only the roster-listed tiers resolve.
- An unsubstituted placeholder or an invalid identifier fails **loudly**: exit 1, with the model list on stderr. A model error therefore never presents as a stall, so when a call appears to hang the model is not the cause.
