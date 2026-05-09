---
title: "Pilot {{PILOT_ID}} — {{HEADLINE}}"
slug: change/pilots/{{PILOT_ID}}
domain: firm
type: pilot
pilot_id: {{PILOT_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [{{S6_OWNER}}]
status: {{planning_or_running_or_proceeded_or_iterated_or_abandoned}}
start_date: {{YYYY-MM-DD}}
end_date: {{YYYY-MM-DD}}
cohort_partner_ids: {{COHORT_LIST}}
---

# Pilot {{PILOT_ID}} — {{HEADLINE}}

**Status:** {{STATUS}}
**Started:** {{START_DATE}}
**Ended:** {{END_DATE}}
**Cohort:** {{COHORT_LINKS}} (size {{COHORT_SIZE}}, target 15-20% of {{TOTAL_AFFECTED_PARTNERS}})

## What was piloted

{{WHAT_AND_WHY}}

## METR baseline (pre-pilot, locked)

{{BASELINE_TABLE}}

## Pilot results (week-by-week)

{{#each weeks}}
### Week {{n}}

- DORA delta: {{dora_delta}}
- SPACE delta: {{space_delta}}
- DX Core 4 delta: {{dx_delta}}
- Self-report delta: {{self_report_delta}}
- Perception gap flag: {{gap_flag}}
- Friction notes: {{friction_summary}}
- Wins notes: {{wins_summary}}
{{/each}}

## Mid-point review (week 4)

{{MIDPOINT_NOTES}}

**Decision at mid-point:** {{continue_or_iterate_or_abandon}}.

## Final results (week 8 or close)

{{FINAL_RESULTS_TABLE}}

## Cohort recommendation

- Would proceed to full rollout: {{N_RECOMMEND}} of {{COHORT_SIZE}} ({{PCT}}%).

## Decision

**{{PROCEED_OR_ITERATE_OR_ABANDON}}.**

{{DECISION_RATIONALE}}

{{#if proceeded}}

### Klarna Test triggered for full rollout

- Test ID: [[klarna-tests/{{TEST_ID}}]]
- Score: {{KLARNA_SCORE}} / 20
- 90-day post-rollout review: {{REVIEW_DATE}}

{{/if}}

{{#if abandoned}}

### Lessons learned

{{LESSONS}}

### Carve-offs (narrow use cases retained)

{{CARVE_OFFS}}

{{/if}}

## Cross-references

- METR baseline source data: `templates/excel/metr-baseline.xlsx` (pilot ID `{{PILOT_ID}}`)
- Cohort private pilot notes (read access via partner consent): {{COHORT_PRIVATE_NOTE_LINKS}}
- BR where decision was taken: [[../business-reviews/{{BR_DATE}}]]
