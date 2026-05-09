# Example 2 — A pilot that was abandoned at week 8

A worked example of the discipline working in the **other direction**: a pilot that produced negative results, the pack's framework caused the firm to abandon, and the lessons-learned page surfaces the genuine value (which was real) without pretending the rollout itself was the right answer.

## The setup

Same 18-partner SaaS firm. Different rollout: this time the firm wants to roll out an AI Marketing pack (a custom Skill that drafts marketing emails, social posts, and customer-facing landing copy) to the 4 customer-success partners.

## Phase 1 — 90-day baseline (2026-01-15 → 2026-04-15)

Pack runs §4.1. Different metrics for the marketing domain:

| metric | source | baseline_value |
|---|---|---|
| email_open_rate | Mailchimp | 28% |
| social_engagement_rate | Buffer | 3.1% |
| landing_conversion_rate | GA4 | 2.7% |
| content_pieces_per_week_per_partner | manual count | 6 |
| cs_partner_dx_score | survey | 7.2 / 10 |

Baseline locked 2026-04-15. Decision record: *"Marketing pack pilot greenlit for 4-week duration with 2 cohort partners."*

## Phase 2 — 6-week pilot (2026-04-22 → 2026-06-03)

Cohort: 2 of 4 customer-success partners (Jana + Anya).

**Week 1-2:** AI drafting works mechanically. Email open rates: 28% → 26% (slight drop). Social engagement: 3.1% → 2.8% (slight drop). Both partners report "the AI's drafts feel like AI" and they spend significant time editing.

**Week 4 mid-point:**
- email_open_rate: 28% → 25% (-11%)
- social_engagement_rate: 3.1% → 2.6% (-16%)
- landing_conversion_rate: 2.7% → 2.5% (-7%)
- content_pieces_per_week: 6 → 8 (+33%)
- self-report from partners: "the *quantity* is up, but the *quality* drop is real and measurable in engagement metrics."

The pack's mid-point decision rule: continue / iterate / abandon.
- **Continue:** would require the assumption that engagement will recover with iteration.
- **Iterate:** revise the pack's prompts, retrain, try again for 4 more weeks.
- **Abandon:** acknowledge that the AI's drafts genuinely feel like AI to customers, and that the engagement drop is real.

The cohort + founder discuss. They decide to **iterate** — revise the prompt-chain to add a "human voice" layer (every AI-drafted piece passes through the partner's voice-tuning pass before publishing).

**Weeks 5-6:** iterated workflow runs.

**Week 8 close (2026-06-03):**
- email_open_rate: 25% → 27% (recovered slightly but still below baseline 28%)
- social_engagement_rate: 2.6% → 2.9% (recovered but still below 3.1%)
- landing_conversion_rate: 2.5% → 2.6% (essentially flat vs. baseline)
- content_pieces_per_week: 8 → 7 (the human voice pass slowed throughput back down)
- partner self-report: 3 of 4 customer-success partners (the 2 in the pilot + 1 of the 2 outside) say "would not recommend full rollout"

## Phase 3 — Decision: abandon

Per §4.4 success criteria:
- Measured delta is **slightly negative** (engagement dropped; content volume up but not by enough to offset).
- Cohort recommendation rate: **50%** (Jana would proceed; Anya would not). Below the 80% threshold.
- One of two control partners would not adopt.

**Decision: abandon.**

## Phase 4 — Lessons-learned (2026-06-04)

The pack writes `firm/change/pilots/marketing-2026-q2-abandoned.md`. Key sections:

```markdown
---
title: "Marketing pack pilot — ABANDONED"
type: pilot-summary
pilot_id: marketing-2026-q2
status: abandoned
start_date: 2026-04-22
end_date: 2026-06-03
cohort_partner_ids: [jana-kos, anya-gorska]
---

# Why we abandoned

The data spoke clearly: the AI's drafting reduced engagement metrics by 7-16% across the pilot, and even with a "human voice" iteration the recovery was incomplete. 50% of the cohort would not recommend full rollout. The framework's criterion (≥80% recommendation, no negative delta) was not met.

# What the data showed

- Email open rate down 7% even after iteration.
- Social engagement down 6% even after iteration.
- Landing conversion essentially flat.
- Content volume up modestly (+17% sustained).
- Customer-success partners' time freed up by ~3 hours/week.

# What we kept

The volume gain is real. We're carving off **two narrow use cases** where the AI drafting is genuinely valuable:

1. **Internal newsletter drafting** — internal-only, voice constraints are weaker, no engagement-rate stakes. Anya will use it informally.
2. **Routine customer status emails** (e.g. "your monthly invoice is ready" templates) — high-volume, low-creativity, no engagement-rate sensitivity.

These do NOT constitute a full Marketing pack rollout. They are individual partner tools.

# What the partners thanked

Jana: "I appreciated being included in the pilot. The mid-point review was honest. I'm glad we abandoned rather than rolling out."
Anya: "Same. The volume gain was tempting but I'm relieved we trusted the engagement data."

# Lessons for future pilots

1. **Marketing AI rollouts have a quality bar that's hard to measure pre-pilot.** Email open-rate is a meaningful KPI, not vanity. We should always have a customer-facing engagement metric in the baseline before pilots like this.
2. **Iteration is not always the right response to mid-point gaps.** Sometimes the gap is fundamental and iteration just delays the abandonment.
3. **The human voice gap is real.** AI drafts feel like AI to customers, even with iteration prompts that try to add voice. This may change with future models; we'll re-pilot in 6-12 months.
4. **Carve-offs are honest.** Abandoning the full rollout doesn't mean discarding all value; the narrow use cases survive.

# Brain links

- Baseline: [[../baselines/marketing-2026-q1]]
- Mid-point review notes: [[./marketing-2026-q2/week-4-review]]
- Cohort partners' private pilot notes (read access via partner consent): [[partners/jana-kos/private/pilot-notes]] and [[partners/anya-gorska/private/pilot-notes]]
```

## Phase 5 — Communicating the abandonment

Tali at the next BR:

> The AI Marketing pack pilot abandons at week 8. Engagement metrics did not recover even with iteration. We're carving off two narrow use cases (internal newsletter, routine customer status emails) but not rolling out the full pack. Lessons-learned page in the Brain. Jana and Anya thanked for the pilot work.

No marketing language. No "we're pivoting" / "evolving the strategy". The pilot abandoned. The partnership accepts the data. Move on.

## What this example demonstrates

- **The discipline works in the other direction too.** Most pilots that should abandon don't, because nobody wants to admit a pilot didn't work. The framework's measurement-first discipline takes the embarrassment out of abandonment.
- **Iteration is not free.** The week-4 iteration cost 4 weeks; in retrospect, the pattern was clear at week 4 and the abandonment could have been called then. Future pilots will be more willing to call it earlier.
- **Carve-offs are honest.** The internal newsletter use case is real value. The framework doesn't force a binary "all or nothing" on rollouts.
- **No Klarna Test was needed** because the pack was abandoned (no human displacement happened). If the firm had pushed through to full rollout despite the data, R7 would have triggered and the Klarna Test would have likely failed (Q1 fails because quality dropped).
- **Partners get thanked for the abandonment**, not just for proceedings. The framework's culture protects partners who participate in pilots that don't work out.
