# Reference Org: Solunar Studio (3-partner small org)

## Profile

- **Firm:** Solunar Studio. Generative-software studio. Founded 2026-Q1.
- **Partners:** 3
  1. **Mira Tek** — founder, full-time partner, agentic-engineer, jurisdiction SI. Reward species: hybrid 60/30/10.
  2. **Davor Krznar** — full-time partner, agentic-engineer, SI. Reward species: pure eat-what-you-kill.
  3. **Anya Gorska** — project specialist, vibe-coder, PL. Reward species: hybrid 80/15/5 (project-bound).
- **Track:** cloud.
- **Brain status:** Level 4 (Curator + MyCuratorMCP) from day 1. **Firm Brain** as a Curator Shared Brain instance per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md).
- **GitHub repos:** two — `solunar-studio-ledger` (operational state, Routines write) and `solunar-studio-brain` (Curator Shared Brain, partners contribute). Both on GitHub Team ($4/seat/mo × 2 seats — admin + Davor; Anya uses collaborator access as a project-bound contractor).
- **Firm Brain IP mode:** `organisational` for Mira + Davor (the full-time partners — Partner Charter §8.1 IP-assignment clause). Anya joins under `contributor_retains` (project specialist — her output specs and contributions retain her copyright; firm owns only the synthesized output during her project window). Implementation note: with v3.0.0-beta the brain is single-mode (`organisational`); Anya's `contributor_retains` posture is recorded as a side-letter in her project agreement until v3.x supports per-cohort mode mixing.
- **Attribution flags:** both `allow_name_attribution` and `attribute_by_name` left at default false — UUID-pseudonymous attribution. Mira opts in to name attribution for her thesis pages by mid-Q2 (the firm wants her name on the public-facing positioning).
- **Synthesize cadence:** weekly, Sunday evening, Mira runs Curator's `Synthesize` button from her laptop. Typical cost: $0.003-0.008/week.
- **Legal posture:** Slovenian d.o.o.; counsel engaged; Mira 70% / Davor 30%; Anya is contractor.
- **EU AI Act exposure:** Limited risk (Lumina-style RAG widget, Code & QA tooling). No high-risk Annex III exposure.

## Awkward edges to find

1. **A perception-gap finding** — see `firm/change/perception-gap-2026-04.md`. Davor's +25% self-report vs. +5% DORA-measured. Confronted in BR; data accepted; 30-day re-baseline.
2. **A Tier-1 dispute** — see `firm/compensation/2026-04/disputes/D-2026-04-001.md`. Anya's value_tier classification dispute on output #14. Resolved in 4 days; April variable +€1,500.
3. **A blocker that pushed a deal slip** — see `firm/business-reviews/2026-03-27.md`. Lumina widget qualification step blocker; resolved via ADR-2026-007 a week later.

## What this example demonstrates

- The framework works at 3 partners.
- The Klarna Test pass-flow is end-to-end (`firm/klarna-tests/KT-2026-001.md` shows the customer-onboarding email automation; passed at score 16/20; 90-day review on calendar).
- Disputes resolve at Tier 1 in days, not weeks.
- The Curator-fed Brain is operationally complete after 60 days.

## v1.0 scaffold status

This reference org ships as a scaffold in v1.0. The directory structure is specified in this README (and in [`examples/SPEC.md`](../SPEC.md)); population lands in v1.x. Two representative Brain pages are in place today (`firm/klarna-tests/KT-2026-001.md`, `firm/partners/index.md`). The full 60-day operational data (X1 ledger rows, R1 daily logs, weekly BRs, R6 audit logs) — and all the `firm/...` paths referenced in the awkward-edges list above, which are **(v1.x)** — land in v1.x.
