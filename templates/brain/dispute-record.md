---
title: "Dispute {{DISPUTE_ID}} — {{HEADLINE}}"
slug: compensation/{{MONTH}}/disputes/{{DISPUTE_ID}}
domain: firm
type: dispute
dispute_id: {{DISPUTE_ID}}
tier: {{1_or_2_or_3}}
raised_by: {{PARTNER_ID}}
against: {{ACCOUNTABLE_PARTY_ID}}
status: {{open_or_resolved_or_escalated}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r3-or-manual]
resolution_date: {{YYYY-MM-DD_or_NA}}
---

# Dispute {{DISPUTE_ID}} — {{HEADLINE}}

**Tier:** {{TIER}}
**Raised:** {{RAISED_DATE}} by [[partners/{{RAISED_BY}}]]
**Against:** [[partners/{{AGAINST}}]] (Accountable per RACI matrix)
**Status:** {{STATUS}}

## What's disputed

{{DISPUTE_DESCRIPTION}}

## Linked artefacts

- Disputed item: [[{{DISPUTED_ARTEFACT_LINK}}]]
- Underlying X1 row(s): {{X1_ROW_REFERENCES}}
- Reward Species Declaration in effect: [[partners/{{RAISED_BY}}/reward-species-declaration]]
{{#if escalated_from}}
- Escalated from: [[../disputes/{{ESCALATED_FROM_DISPUTE_ID}}]]
{{/if}}

## Tier 1 — Direct discussion

{{#if tier_eq_1_or_higher}}
**Discussion notes:**

{{TIER_1_NOTES}}

**Outcome:** {{tier_1_outcome}}
{{/if}}

## Tier 2 — Partner panel

{{#if tier_eq_2_or_higher}}
**Panel members:**
- [[partners/{{PANELIST_1}}]]
- [[partners/{{PANELIST_2}}]]
- [[partners/{{PANELIST_3}}]] (non-beneficiary)

**Panel recommendation:** {{tier_2_recommendation}}

**Original Accountable's response:** {{accountable_response}}
{{/if}}

## Tier 3 — Founder + counsel

{{#if tier_eq_3}}
**Founder decision:** [[partners/{{FOUNDER}}]] on {{TIER_3_DATE}}.

{{TIER_3_REASONING}}

**Counsel consulted:** {{counsel_name_OR_n/a}} on {{TIER_3_COUNSEL_DATE}}.
{{/if}}

## Resolution

{{#if resolved}}
**Resolved:** {{RESOLUTION_DATE}}.

**Outcome summary:** {{RESOLUTION_SUMMARY}}.

**Implementation steps:**

{{IMPLEMENTATION_STEPS}}

**Variable / long-tail adjustment (if applicable):**

{{ADJUSTMENT_NOTES}}
{{else}}
Open. Next action: {{NEXT_ACTION_OWNER}} by {{NEXT_ACTION_DEADLINE}}.
{{/if}}

## Audit trail

- Statement disputed: [[{{DISPUTED_STATEMENT_PATH}}]]
- Underlying ledger rows: {{LEDGER_ROW_LIST}}
- Reward Species version: {{RSD_VERSION}}
