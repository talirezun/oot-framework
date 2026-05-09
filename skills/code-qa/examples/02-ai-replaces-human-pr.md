# Example 2 — An `ai-replaces-human` PR end-to-end

A worked example of the auto-labeller firing, R7 triggering, and the Klarna Test gating the merge — the full pre-merge discipline the framework's authors believe is the framework's most important single safeguard.

## The proposed change

Partner Davor opens PR #1502 in `firm-saas`:

> **Title:** Replace manual customer-onboarding email step with AI-drafted version
>
> **Description:** Currently, when a customer signs up, our onboarding flow routes the welcome-and-setup email to Anya (specialist partner) for personal drafting. This works but doesn't scale; we have a 3-day SLA and Anya is at capacity. This PR adds an AI Skill that drafts the onboarding email from the customer profile and sends it automatically. Anya's manual review remains as an opt-in escalation path for high-tier customers.

PR diff includes:
- Removal of `src/onboarding/route_to_anya.ts` (the function with `manual_review` in its body).
- Addition of `src/onboarding/ai_drafter.ts` with frontmatter `automates: human_function: yes`.
- New tests.

## Auto-labeller fires (within 30 seconds of PR open)

The `.github/labeler.yml` matches **two** of the §4.8 signatures:

1. Code path removal — the deleted function contained `manual_review`.
2. New autonomous Skill — frontmatter `automates: human_function: yes`.

Both trigger the `ai-replaces-human` label. GitHub applies it.

## R7 fires (within 30 seconds of label)

The `routines/cloud/R7.md` (or `routines/privacy/R7.md`) Routine wakes:

1. Generates `test_id`: KT-2026-014.
2. Appends row to X4 Decision_Log: trigger=`pr_label`, trigger_ref=PR URL, status=`scoring`.
3. **Identifies the affected partner** (S3's contribution): cross-references Output Specs in `firm/partners/*/output-specs/` for any whose `expected_outcome` overlaps with "draft customer onboarding email". Match: Anya's `2025-11-15--onboarding-email-style-guide.md` and three monthly Output Specs in early 2026 about onboarding emails. **Affected partner: Anya.**
4. **Identifies the non-beneficiary reviewer** (S3's contribution): reads X1 Monthly_Variable rolling 90 days; checks X2 Long_Tail_Schedule. Pick a partner whose total comp does not increase from this change. The founder benefits (cost saving). Davor benefits (his PR ships, he gets the variable for shipping it). Anya is the affected partner (cannot be reviewer per Q7). Mira does not benefit; Mira's reward species is hybrid 60/30/10 with no overlap with onboarding work. **Non-beneficiary reviewer: Mira.**
5. Posts `oot/klarna-test` GitHub status check on the PR's head SHA — set to **failing** with message: *"Klarna Test KT-2026-014 in progress. Score required ≥14/20."*
6. PR's merge button is now grey: GitHub's branch protection requires `oot/klarna-test` to pass.
7. Opens `firm/klarna-tests/KT-2026-014.md` Brain page with the full context.
8. Posts to `#klarna-test`: *"KT-2026-014: PR #1502 (replace manual customer-onboarding email with AI drafter) requires Klarna Test scoring before merge. Affected partner: [[partners/anya-gorska]]. Non-beneficiary reviewer: [[partners/mira-tek]]. Scoring window: 5 business days. Reference: governance/KLARNA-TEST.md."*
9. Email/dMail to founder + Anya + Mira with the same content.

## The scoring (humans, over 3 days)

Davor scores first (he's the proposer + scorer per X4 Decision_Log).

Per `governance/KLARNA-TEST.md` 10 questions, scored 0/1/2:

| Q | Question | Initial score | Evidence |
|---|---|---|---|
| 1 | Quality measured vs. human baseline ≥3 months? | 1 | 6-week pilot ran on 50 customers; quality matched Anya on routine cases; 12% drop on edge-cases. |
| 2 | Original success metrics still measured? | 2 | Customer NPS on onboarding emails + first-product-use latency tracked. |
| 3 | Defined reversal threshold? | 2 | "If onboarding NPS drops below 60 for 2 weeks, or if the failure-case pattern in pilot recurs in production, revert." |
| 4 | Reversal plan operational? | 1 | Anya retained on standby; opt-in escalation for high-tier customers is real; full reversal would take ~2 days. |
| 5 | Affected partner consulted in writing? | 2 | Anya consulted; her concerns about edge-case quality addressed in the PR (the opt-in escalation path is the result of her feedback). Written record at [[firm/klarna-tests/KT-2026-014/anya-consultation]]. |
| 6 | METR baseline? | 2 | DORA-equivalent for onboarding: cycle time, NPS, escalation rate captured for 90 days. |
| 7 | Reviewed by non-beneficiary partner? | 0 | Mira hasn't reviewed yet (this column will fill on her sign-off). |
| 8 | Public-communication posture specified? | 2 | Founder's posture: no proactive communication; if asked, "AI drafts onboarding emails for routine cases; specialist review remains for complex customers". Written and approved by founder. |
| 9 | 90-day post-deployment review scheduled? | 2 | Calendar invite created for 2026-08-12. Owner: founder. Pre-committed framework: re-check NPS, escalation rate, edge-case quality. |
| 10 | Founder willing to defend in 2 years? | 2 | Founder confirms in writing. |

Davor's score: 16/20. He signs off in X4 (column N: scorer_signoff = Yes).

But Q7 is 0 because Mira hasn't reviewed. Total can't reach 14 without Mira.

## Mira's review (the non-beneficiary)

Mira reads the PR, the pilot data, the consultation record with Anya, the reversal plan. She scores:

She agrees with Davor's scoring on Q1, Q2, Q3, Q4, Q5, Q6, Q8, Q9, Q10. On Q7, she scores **2** (her own non-beneficiary review is now happening; she's being honest). She signs off in X4 (column O: non_beneficiary_signoff = Yes).

Total: 16/20. Decision: **PROCEED**.

## The status check flips

The `klarna-gate.yml` workflow re-runs (it polls X4's Klarna_Score sheet). All three conditions now hold: `total_score >= 14` AND `scorer_signoff = Yes` AND `non_beneficiary_signoff = Yes`. Status check turns green.

PR's merge button activates. Davor merges.

## Post-merge

- The Brain page `firm/klarna-tests/KT-2026-014.md` updates: `status: proceeded`.
- X4 Decision_Log row updates: `status: proceeded`.
- The 90-day review (2026-08-12) is on the founder's calendar.
- R6 logs the audit trail entry that night.
- The next Friday BR's Klarna-status block lists KT-2026-014 as "proceeded with reversal threshold; 90-day review on calendar".

## What this example demonstrates

- The auto-labeller correctly identifies an `ai-replaces-human` PR.
- R7 fires in seconds; the gate is real, not advisory.
- S3's contribution: identifying the affected partner + non-beneficiary reviewer correctly (cross-referencing Output Specs and X1/X2).
- The scoring is human; the framework does not pretend to score.
- The Q7 (non-beneficiary review) discipline forces the bar to a partner who has no skin in the cost saving.
- The Q8 (public-communication posture) — Davor scored 2 because the framework's authors decided in advance what they'd say if asked. The Klarna failure mode is silent automation that is later spun publicly as something it isn't.
- The 90-day review is on a calendar before merge — Q9 is real, not theatre.
- Honest framing throughout: this PR is a real improvement; the discipline is what makes it safe to ship.

## What it would look like if the score had been <14

Suppose Mira scored Q4 as **0** (she thinks the 2-day reversal time is too slow given the SLA). Total would be 14. Still proceed-eligible.

But suppose she also scored Q1 as **0** (she thinks the 12% edge-case drop is unacceptable). Total: 13. Decision: **HOLD**.

X4 Decision_Log: `status: held`. Status check stays red. The remediation list lands in `#klarna-test` automatically per R7's prompt:

> KT-2026-014 held. Remediation required for Q1 (edge-case quality below threshold). Recommended: extend pilot to 12 weeks; specifically test the 12% edge-case pattern; achieve <5% drop or define a permanent escalation path for those cases. Re-score after remediation.

The PR cannot merge. Davor either remediates and re-scores, or pulls back the PR. The framework refused to ship a change that scored honestly below threshold. *That* is the framework's purpose in action.
