---
title: "METR — RCT on AI tools and developer productivity (July 2025)"
authors: "METR (Model Evaluation & Threat Research)"
publication: "METR research report + arXiv 2507.09089"
date: 2025-07
oot_thesis: 1 (Resistance)
external_url: "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/"
---

# METR — RCT on AI tools and developer productivity

*Stub paper-summary. Full version lands in v1.x.*

## Headline findings (cited in MANIFESTO Thesis 1)

- Senior open-source developers using **early-2025 AI coding tools** on real OSS tasks were measured **19% slower**.
- Same developers self-reported being **20% faster**.
- The **39-point perception swing** is the structural finding: humans cannot reliably self-assess AI-assisted productivity without an external baseline.
- February 2026 follow-up shows similar but wider-CI results; the structural pattern holds.

## Why ØØT cites it

This is the empirical foundation for the framework's **mandatory METR baseline discipline** (Skill Pack S6 §4.1). Without a 90-day pre-rollout baseline, the perception gap is invisible. The 20-point gap_flag threshold in `metr-baseline.xlsx` (X5) is anchored to roughly half this 39-point swing.

## Method

Randomised controlled trial. Senior open-source developers (n=16), real OSS tasks, AI tools allowed/disallowed condition. Productivity measured via task completion time. Self-report via standard survey instruments.

## Limitations

- Specific to early-2025 AI coding tools (Anthropic Claude, GitHub Copilot, Cursor as available at time of study).
- Senior developers — junior developers may show different pattern.
- OSS task domain — closed-source / enterprise contexts may differ.
- Small n (16).

## Cross-references inside ØØT

- [`MANIFESTO.md`](../../MANIFESTO.md) Thesis 1.
- Skill Pack [`skills/change-management/SKILL.md`](../../skills/change-management/SKILL.md) §4.1, §4.6.
- [`templates/excel/SPEC.md`](../../templates/excel/SPEC.md) X5 — `metr-baseline.xlsx` and the 20-point gap threshold.
