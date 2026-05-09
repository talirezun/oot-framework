---
title: "Daily output log {{DATE}}"
slug: output-logs/{{DATE}}
domain: firm
type: output-log
date: {{DATE}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r1]
status: active
---

# Daily output log {{DATE}}

## Summary

Captured **{{N_OUTPUTS}}** outputs from **{{N_PARTNERS}}** partners.

## Outputs

{{#each outputs}}
- [[partners/{{partner_id}}]] — `{{output_type}}` — {{output_ref}} — value tier `{{value_tier}}` — {{ai_authored_pct}}% AI-authored — output spec: {{output_spec_ref}}
{{/each}}

## Anomalies

{{#if anomalies}}
{{#each anomalies}}
- {{this}}
{{/each}}
{{else}}
None.
{{/if}}

## Retroactive rework detections

{{#if rework_updates}}
{{#each rework_updates}}
- {{prior_log_id}} (originally captured {{original_date}}) — flipped to `rework_within_30d=Yes`. Trigger: commit {{trigger_ref}} ({{trigger_message}}). Affected partner: [[partners/{{partner_id}}]].
{{/each}}
{{else}}
None.
{{/if}}

## Source coverage

- GitHub: {{github_status}} ({{github_signal_count}} signals)
- Slack / dChat: {{messaging_status}} ({{messaging_signal_count}} signals)
- Drive / filesystem: {{filesystem_status}} ({{filesystem_signal_count}} signals)

{{#if source_failures}}
## Source failures

{{#each source_failures}}
- {{source}}: {{error_summary}} — flagged to `#ops`.
{{/each}}
{{/if}}
