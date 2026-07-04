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
3. **A blocker that pushed a deal slip** — the Lumina widget qualification-step blocker (raised late March, before this slice starts). Its resolution is in the slice: `firm/business-reviews/2026-04-10.md` (blocker closed) via `firm/decisions/D-2026-011.md` and the fix output OL-20260410-001.

## What this example demonstrates

- The framework works at 3 partners.
- The Klarna Test pass-flow is end-to-end (`firm/klarna-tests/KT-2026-001.md` shows the customer-onboarding email automation; passed at score 16/20; 90-day review on calendar).
- Disputes resolve at Tier 1 in days, not weeks.
- The Curator-fed Brain is operationally complete after 60 days.

## Population status — representative two-week slice

This reference org is **populated with a representative two-week operational slice (2026-04-06 → 2026-04-19)**; the full quarter (60-90 days per [`examples/SPEC.md`](../SPEC.md)) lands in v1.x. Every wikilink in the slice resolves within this example.

What IS present under `firm/`:

- `index.md` + `theses.md` — firm overview and manifesto adaptation.
- `partners/` — roster (`index.md`) + 3 partner profiles carrying `P-NNN` join keys per [ADR-005](../../docs/internal/ADR-005-partner-join-key-and-output-weight.md).
- `output-logs/` — 10 daily R1 logs (weekdays 2026-04-06 → 2026-04-17), including one **co-authored output split at weight 0.5/0.5** (2026-04-14) per ADR-005.
- `business-reviews/` — 2 Friday BRs (04-10 with the perception-gap confrontation; 04-17 with the Klarna outcome).
- `decisions/D-2026-011.md` — the qualification-step decision both BRs reference.
- `klarna-tests/KT-2026-001.md` — the pass-flow Klarna Test (16/20, PROCEED, 90-day review scheduled 2026-07-12).
- `compensation/2026-04/` — draft monthly variable-pay summary + the resolved Tier-1 dispute `D-2026-04-001` (Anya's output #14, +€1,500).
- `change/perception-gap-2026-04.md` — Davor's 20-point gap and the 30-day re-baseline.
- `audit-logs/` — 3 representative R6 Article-12 daily logs (04-08, 04-12, 04-14).
- `brain-health/2026-W16.md` — one R5 weekly snapshot.

**No `firm/excel/*.xlsx` ships in this example.** The Excel state (X1-X9) is generated at adoption by `scripts/build_excel.py` and then mutated by Routines (ADR-001); populated xlsx binaries checked into an example would rot instantly against the generator and are unreviewable in diffs. The markdown pages above are the human-readable mirror of what those workbooks contain at a real firm.

Deferred to v1.x: the remaining ~10 weeks of the quarter, per-partner variable-statement pages (`firm/partners/<id>/variable-statements/`), the founder-approval packet, and the 90-day Klarna review entry (due 2026-07-12).
