---
title: "Klarna Test {{TEST_ID}} — {{DECISION_SUMMARY}}"
slug: klarna-tests/{{TEST_ID}}
domain: firm
type: klarna-test
test_id: {{TEST_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r7, {{SCORER}}]
status: {{scoring_or_proceeded_or_held_or_abandoned}}
score: {{TOTAL_SCORE}}
decision: {{PROCEED_OR_HOLD_OR_ABANDON}}
pr_url: {{PR_URL}}
affected_partners: {{AFFECTED_PARTNER_LIST}}
non_beneficiary_reviewer: {{NON_BENEFICIARY}}
review_date_90d: {{REVIEW_DATE_90D}}
---

# Klarna Test {{TEST_ID}}

**Decision under test:** {{DECISION_SUMMARY}}

**Trigger:** {{TRIGGER_TYPE}} — {{TRIGGER_REF}}
**Scorer:** [[partners/{{SCORER}}]]
**Non-beneficiary reviewer:** [[partners/{{NON_BENEFICIARY}}]]
**Affected partner(s):** {{AFFECTED_PARTNERS_LINKS}}

## Context

{{LONG_FORM_CONTEXT}}

## Scoring

(See `templates/excel/klarna-test.xlsx` row `{{TEST_ID}}` for the canonical scores; this page mirrors them for human readers.)

| # | Question | Score | Evidence |
|---|---|---|---|
| 1 | Quality measured vs. human baseline ≥3 months? | {{Q1}} | {{Q1_EVIDENCE}} |
| 2 | Original success metrics still measured? | {{Q2}} | {{Q2_EVIDENCE}} |
| 3 | Defined reversal threshold? | {{Q3}} | {{Q3_EVIDENCE}} |
| 4 | Reversal plan operational? | {{Q4}} | {{Q4_EVIDENCE}} |
| 5 | Affected partner consulted in writing? | {{Q5}} | {{Q5_EVIDENCE}} |
| 6 | METR baseline? | {{Q6}} | {{Q6_EVIDENCE}} |
| 7 | Reviewed by non-beneficiary partner? | {{Q7}} | {{Q7_EVIDENCE}} |
| 8 | Public-communication posture specified? | {{Q8}} | {{Q8_EVIDENCE}} |
| 9 | 90-day post-deployment review scheduled? | {{Q9}} | {{Q9_EVIDENCE}} |
| 10 | Founder willing to defend in 2 years? | {{Q10}} | {{Q10_EVIDENCE}} |

**Total: {{TOTAL_SCORE}} / 20.**

## Decision

**{{DECISION}}.** {{DECISION_RATIONALE}}

## Reversal plan

{{REVERSAL_PLAN}}

## 90-day review

Scheduled: {{REVIEW_DATE_90D}}
Owner: [[partners/{{REVIEW_OWNER}}]]
Pre-committed decision framework: {{REVIEW_FRAMEWORK}}

## Sign-offs

- Scorer: [[partners/{{SCORER}}]] — {{SCORER_SIGNOFF_DATE}}
- Non-beneficiary reviewer: [[partners/{{NON_BENEFICIARY}}]] — {{NB_SIGNOFF_DATE}}
- Founder (for `proceed`): [[partners/{{FOUNDER_ID}}]] — {{FOUNDER_SIGNOFF_DATE}}
