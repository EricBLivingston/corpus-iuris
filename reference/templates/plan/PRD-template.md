# [Feature / Initiative Name]

## 1. Header

**Links**

- Related plans:
- Analytics / dashboards:
- Incident / ticket:

**Last updated:** YYYY-MM-DD

---

## 2. Problem

Answer in a few sentences:

1. **Who is the customer?** (which subsystem, user, or operator hits this)
2. **What is the problem?** (concrete pain, with the failure mode)
3. **How do we know?** (incident link, log evidence, benchmark, ticket)

---

## 3. Goals

**Output goal** — the single outcome metric this initiative is judged on.

- e.g. _cut p95 request latency by 30% without raising the error rate_

**Input metrics** — 2–3 leading indicators that move the output.

- e.g. _cache hit ratio at the read path_
- e.g. _DB query count per request_

**Non-goals** — explicit areas this initiative will not touch.

- e.g. _admin panel UX refresh_
- e.g. _migration of the legacy reporting service_

**Guardrails** — metrics that must NOT regress.

- e.g. _peak memory footprint stays under current ceiling_
- e.g. _existing public API contracts remain byte-compatible_

---

## 4. Acceptance Criteria

Observable, testable checks that close out the PRD. Each criterion is written from the outside — what an observer or test confirms, not how the code achieves it — atomic, falsifiable, and silent on implementation strategy, which `Design.md` / `Implementation.md` owns.
- [ ] …
- [ ] …
- [ ] …

---

## 5. Decisions & Open Questions

| Date | Topic | Decision / Status | Owner |
| ---- | ---- | ---- | ---- |
| YYYY-MM-DD | … | … | … |

---

## 6. Next Step

**Route:** `Design.md` | `Implementation.md`

**Rationale** — 2–3 sentences. Cite the patterns this work slots into (→ Implementation) or the gaps/new components/new boundaries it requires (→ Design). The call is about whether the existing codebase can clearly accommodate the requirements, not about size or effort.

---

## A. Appendix

Link-outs only — keep the PRD body short.

- Prior art / related plans:
- Benchmarks / data:
- Research / references:
- Risks register:
