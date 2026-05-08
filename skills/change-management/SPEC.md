# Skill Pack S6 — Change Management / Resistance: SPEC

**ID:** S6
**Name:** Change Management / Resistance
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

The framework's response to the central problem (Thesis 1). Encodes Kotter's eight-step framework, the ADKAR model, the METR perception-gap baseline discipline, the AI Champion criteria, and the 6–8 week pilot template. Mandatory before any major Skill Pack rollout.

## Scope

**Covers:**
- METR baseline procedure (DORA + SPACE + DX Core 4 metrics captured before AI rollout).
- 6–8 week pilot template (15–20% of team, structured cohort).
- AI Champion designation criteria (earned, not appointed).
- Resistance-pattern recognition (shadow refusal, perception gap, sceptic alignment).
- Communication patterns for AI rollout announcements.
- The 12–24 month resistance plateau plan.
- Klarna Test pre-rollout integration (every major rollout is a Klarna trigger).

**Does NOT cover:**
- The Klarna Test itself (that is `governance/KLARNA-TEST.md`).
- Domain-specific rollout patterns (those are in the relevant Skill Pack).
- HR / employment law dimensions of change management (counsel territory).

## Allowed tools / dependencies

- Curator MCP tools.
- Excel MCP / Google Sheets (write to X5 — METR baseline).
- Slack / 4thtech (rollout communication).
- The Klarna Test interaction (R7).

## Section structure

1. **Purpose**
2. **When to invoke** — before any Skill Pack rollout, before any major workflow change involving AI, when resistance patterns are observed in operation.
3. **When NOT to invoke** — for tools changes that don't affect partner workflows (e.g., backend infrastructure swaps).
4. **Operational instructions:**
   - 4.1 METR baseline procedure (what to capture, for how long, who owns).
   - 4.2 Pilot cohort selection (15–20%, criteria for inclusion, cohort composition).
   - 4.3 Pilot execution (6–8 weeks, weekly check-ins, success criteria).
   - 4.4 Post-pilot decision (proceed / iterate / abandon — with Klarna Test if proceed).
   - 4.5 AI Champion designation (criteria, what they do, how they're not appointed).
   - 4.6 Resistance pattern recognition (shadow refusal, perception gap, sceptic alignment).
   - 4.7 Rollout communication (the partnership-wide announcement pattern).
   - 4.8 12–24 month plateau planning (persistence as the key correlate of success).
5. **Brain interaction protocol** — writes pilot results, AI Champion designations, resistance observations to `firm/change/`.
6. **Excel interaction protocol** — writes X5 (METR baseline).
7. **Routine integration** — invokes R7 (Klarna Test) at decision points.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts

1. Don't roll out without a METR baseline. Mandatory — no exceptions.
2. Don't appoint an AI Champion. They are recognised, not named.
3. Don't ignore shadow refusal. If the tool is licensed but unused, the rollout is failing.
4. Don't extend a failing pilot past 8 weeks. Stop and re-design.
5. Don't measure post-rollout against post-rollout perception. Always vs. baseline.

## Worked examples concept

**Example 1:** The firm is rolling out the Code & QA Skill Pack. Before licensing Claude Code firm-wide, the pack instructs: capture DORA metrics for 90 days; select a 4-partner pilot cohort (out of 18 partners); run 8 weeks; measure DORA delta + qualitative; only then run Klarna Test for full rollout.

**Example 2:** Three months after a Skill Pack rollout, partners report higher productivity but DORA metrics show no improvement. The pack diagnoses the perception gap; recommends recapturing baseline, re-running cohort comparison.

## References

1. Kotter, J. P. *Leading Change* (1996, updated editions).
2. Hiatt, J. *ADKAR: A Model for Change in Business, Government, and our Community* (2006).
3. METR. *RCT on AI tools and developer productivity* (2025).
4. MIT NANDA. *The GenAI Divide* (August 2025).
5. Microsoft. *Work Trend Index 2025: The Frontier Firm*.
6. Forsgren, N. et al. *Accelerate* + *DORA Report 2025*.
7. Tecknoworks / Caplaz. *AI Champion case studies* (2024–2025).
8. ØØT `MANIFESTO.md`, Thesis 1.

## Acceptance criteria

Standard. Plus: 3+ worked examples; the AI Champion criteria are explicit and operational.