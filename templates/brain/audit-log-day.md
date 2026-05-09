---
title: "EU AI Act audit trail {{DATE}}"
slug: audit-logs/{{DATE}}
domain: firm
type: audit-log
date: {{DATE}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r6]
status: active
entries_count: {{N_ENTRIES}}
anomalies_flagged: {{ANOMALIES_YES_NO}}
---

# EU AI Act audit trail — {{DATE}}

This page is part of the firm's Article 12 record-keeping. It is **append-only**; do not edit historical entries. Corrections are made by appending a new dated entry that supersedes the prior. The branch protecting this path requires signed commits and disallows force-push.

## Summary

- AI decisions logged today: **{{N_ENTRIES}}**
- Anomalies flagged: **{{N_ANOMALIES}}**
- High-risk use cases active: **{{N_HIGH_RISK_USECASES}}** ({{HIGH_RISK_USECASE_LIST}})

## Entries

{{#each entries}}
### {{timestamp}} — {{ai_system}} — {{use_case_id}}

- **Skill / Routine:** `{{skill_or_routine}}`
- **Decision context:** {{context_summary}}
- **Output:** {{output_summary}}
- **Human reviewer:** {{human_reviewer}}
- **Annex III mapping:** {{annex_iii_category}}
{{#if anomaly_flagged}}
- **⚠ Anomaly:** {{anomaly_reason}}
{{/if}}
{{/each}}

{{#unless entries}}
## No agent activity today

This is a noted entry, not a missing day. No agent decision affecting partners or customers was recorded between 23:00 yesterday and 23:00 today. Routine R6 confirms by inspecting all firm Routines (R1, R2, R3, R4, R5, R7, R8) and ad-hoc Skill invocations.
{{/unless}}

## Cross-references

- Risk register: [[../eu-ai-act-risk-register]] (mirrors the Excel X7 Audit_Log_Index sheet)
- Use-case register: [[../eu-ai-act-use-cases]]
