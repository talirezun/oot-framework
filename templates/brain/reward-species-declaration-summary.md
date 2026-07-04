---
title: "Reward Species Declaration — [[partners/{{PARTNER_ID}}]]"
slug: partners/{{PARTNER_ID}}/reward-species-declaration
domain: firm
type: reward-species-declaration
partner_id: {{PARTNER_ID}}
signed_date: {{YYYY-MM-DD}}
pdf_link: {{PDF_LINK}}
reward_species: {{eat_what_you_kill_or_lockstep_or_hybrid}}
created: {{DATE}}
updated: {{DATE}}
authors: [founder, {{PARTNER_ID}}]
status: active
---

# Reward Species Declaration — {{FULL_NAME}}

**Partner:** [[partners/{{PARTNER_ID}}]]
**Reward species:** `{{REWARD_SPECIES}}`
**Signed:** {{SIGNED_DATE}}
**Signed PDF:** [{{PDF_FILENAME}}]({{PDF_LINK}})
**X2 row:** see `templates/excel/reward-species-declaration.xlsx` → `Base_Variable_Split` sheet, row with `partner_id = {{PARTNER_ID}}` (single shared sheet, ADR-005).

## Compensation summary

| Component | Value |
|---|---|
| Annual base | {{BASE_AMOUNT}} {{CURRENCY}} |
| Variable weight personal | {{VARIABLE_WEIGHT_PERSONAL}} |
| Variable weight team | {{VARIABLE_WEIGHT_TEAM}} |
| Variable weight company | {{VARIABLE_WEIGHT_COMPANY}} |
| Output multiplier | {{OUTPUT_MULTIPLIER}} |
| Bonus split (personal/team/company) | {{G}} / {{H}} / {{I}} |
| Stablecoin upgrade preference (Gen 2) | {{Yes_or_No}} |
| Unit Fund interest (Gen 2) | {{Yes_or_No}} |

Validation: variable weights sum to 1.0; bonus splits sum to 1.0.

## Long-tail eligibility

Long-tail entries (per output) are tracked in `templates/excel/reward-species-declaration.xlsx` → `Long_Tail_Schedule` sheet, rows with `partner_id = {{PARTNER_ID}}` (single shared sheet, ADR-005). Quarterly settlement via R4.

Currently active long-tail rows: {{N_ACTIVE_LONG_TAIL_ROWS}}.

## Renegotiations

{{#each renegotiations}}
- **{{date}}** — initiated by {{initiated_by}} — reason: {{reason}} — fields changed: {{fields_changed}} — see [[../../../decisions/{{decision_id}}]].
{{/each}}

{{#unless renegotiations}}
None to date.
{{/unless}}

## Cross-references

- Partner profile: [[partners/{{PARTNER_ID}}/profile]]
- Variable statements: [[partners/{{PARTNER_ID}}/variable-statements/]]
- Long-tail statements: [[partners/{{PARTNER_ID}}/long-tail-statements/]]
