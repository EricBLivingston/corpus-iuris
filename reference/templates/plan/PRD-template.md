# [Feature / Initiative Name]

## 1. Header

**Links**

- Related plans:
- Analytics / dashboards:
- Incident / ticket:

---

## 2. Problem

1. **Customer** — which subsystem, user, or operator hits this.
2. **Problem** — the concrete pain, with its failure mode.
3. **Evidence** — incident link, log, benchmark, ticket.

---

## 3. Goals

**Output goal** — the single outcome metric this initiative is judged on.

- e.g. _cut p95 request latency by 30% without raising the error rate_

**Input metrics** — 2–3 leading indicators that move the output.

- e.g. _cache hit ratio at the read path_
- e.g. _DB query count per request_

**Non-goals** — areas this initiative will not touch.

- e.g. _admin panel UX refresh_
- e.g. _migration of the legacy reporting service_

**Guardrails** — metrics that must not regress.

- e.g. _peak memory footprint stays under current ceiling_
- e.g. _existing public API contracts remain byte-compatible_

---

## 4. Acceptance Criteria

Observable checks that close out the PRD, each written from the outside: what an observer or test confirms, atomic, falsifiable, silent on implementation strategy.

- [ ] …
- [ ] …
- [ ] …

---

## 5. Decisions & Open Questions

| Topic | Decision / Status | Owner |
| ---- | ---- | ---- |
| … | … | … |

---

## 6. Next Step

**Route:** `Design.md` | `Implementation.md`

**Rationale** — the patterns this work slots into (→ Implementation), or the gaps, new components and new boundaries it requires (→ Design). The call turns on whether the existing codebase can accommodate the requirements, not on size or effort.

---

## A. Appendix

Link-outs only.

- Prior art / related plans:
- Benchmarks / data:
- Research / references:
- Risks register:
