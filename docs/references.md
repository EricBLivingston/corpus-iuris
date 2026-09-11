# The work behind the claims

Every empirical claim the corpus makes about model behaviour sits in this table beside the work it rests on. The claims are load-bearing rather than decorative: the argument for [rare tokens](lexicon.md), for [terms whose trained sense already agrees with ours](lexicon.md), and for [handing an executing agent one phase and withholding the rest](pipeline.md) is an argument about attention and retrieval, and it is only as good as the results below.

A row that misreads the work it cites is a defect in this repository, and `CONTRIBUTING.md` names it as one of the few worth opening an issue over.

| Claim | Work |
| ---- | ---- |
| A model resolves a repeated token by matching its earlier occurrence and attending to what followed — the mechanism a citation rides on. | [In-context Learning and Induction Heads](https://arxiv.org/abs/2209.11895); [Induction Heads as an Essential Mechanism for Pattern Matching in In-context Learning](https://arxiv.org/abs/2407.07011) |
| Models bind a token to its referent in context through dedicated internal structure. | [How do Language Models Bind Entities in Context?](https://arxiv.org/abs/2310.17191) |
| Attention is a finite budget that softmax dilutes as context grows, and length alone degrades performance. | [Long Context, Less Focus: A Scaling Gap in LLMs](https://arxiv.org/abs/2602.15028); [Context Length Alone Hurts LLM Performance](https://arxiv.org/abs/2510.05381) |
| Irrelevant context competes with the signal rather than sitting beside it, measurably lowering accuracy. | [Large Language Models Can Be Easily Distracted by Irrelevant Context](https://arxiv.org/abs/2302.00093) |
| Distraction scales with resemblance: the closer irrelevant material sits to the question, the worse it hurts — which is what makes the adjacent phase the cut worth making. | [How Reasoning Models Fail with Contextual Distractors](https://arxiv.org/abs/2601.07226); [The Distracting Effect: Understanding Irrelevant Passages](https://arxiv.org/abs/2505.06914); [How Easily do Irrelevant Inputs Skew the Responses of LLMs](https://arxiv.org/abs/2404.03302) |
| Long-context retrieval leans heavily on literal token overlap, and degrades sharply without it. | [NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167) |
| Context and the parametric prior conflict, and which one wins is not reliably predictable. | [Knowledge Conflicts for LLMs: A Survey](https://arxiv.org/abs/2403.08319) |
| Operating a term against its trained default carries a measured performance cost. | [Reasoning or Reciting?](https://arxiv.org/abs/2307.02477) |
| Tokens too rare in training are undertrained, with degenerate embeddings and erratic behaviour. | [Fishing for Magikarp](https://arxiv.org/abs/2405.05417) |

The presentation deck keeps the same material in a closing appendix, so a reader who met a claim on a slide can reach the paper from either surface.
