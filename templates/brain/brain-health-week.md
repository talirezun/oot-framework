---
title: "Brain health snapshot {{WEEK}}"
slug: brain-health/{{WEEK}}
domain: firm
type: brain-health
week: {{WEEK}}
date: {{TODAY}}
created: {{TODAY}}
updated: {{TODAY}}
authors: [routine-r5]
status: active
domain_scope: {{SECOND_BRAIN_SUBFOLDER}}
broken_wikilinks_count: {{BROKEN_COUNT}}
orphans_count: {{ORPHAN_COUNT}}
stale_count: {{STALE_COUNT}}
pages_scanned: {{PAGES_SCANNED}}
---

# Brain health snapshot {{WEEK}}

Weekly Second Brain health check produced by Routine R5 on {{TODAY}}.

## Summary

| Metric | Count |
|---|---|
| Broken wikilinks | {{BROKEN_COUNT}} |
| Orphan pages | {{ORPHAN_COUNT}} |
| Stale pages (>90d) | {{STALE_COUNT}} |
| Pages scanned | {{PAGES_SCANNED}} |

- **Domain scope:** `{{SECOND_BRAIN_SUBFOLDER}}`
- **Sync freshness:** latest commit in the Second Brain clone is {{SYNC_AGE}} old (Curator syncs ~once/day; readings can lag reality by up to 24h).

## Broken wikilinks

{{#if broken_wikilinks}}
{{#each broken_wikilinks}}
- `{{source_page}}` → `[[{{broken_slug}}]]` (no page with this slug in the domain)
{{/each}}
{{else}}
None.
{{/if}}

## Orphan pages

Pages no other page wikilinks to (excludes `status: index` / `status: landing`).

{{#if orphans}}
{{#each orphans}}
- `{{slug}}`
{{/each}}
{{else}}
None.
{{/if}}

## Stale pages

Pages tagged `status: active` (or no status) with git-mtime older than 90 days.

{{#if stale_pages}}
{{#each stale_pages}}
- `{{slug}}` — {{days_since_modified}} days since last update
{{/each}}
{{else}}
None.
{{/if}}

## Suggested typo-fixes (informational only)

R5 has read-only access to the Second Brain repo and does NOT auto-fix on the cloud
track. Fix these in the Curator app on your next sync-up. (Privacy-track R5 auto-fixes
via the local my-curator MCP.)

{{#if typo_candidates}}
{{#each typo_candidates}}
- `{{source_page}}`: `[[{{broken_slug}}]]` → likely `[[{{suggested_slug}}]]` (Levenshtein {{distance}})
{{/each}}
{{else}}
None.
{{/if}}

## Actions for the founder

{{#if actions}}
{{#each actions}}
- {{this}}
{{/each}}
{{else}}
No action required this week.
{{/if}}

{{#if second_brain_unreachable}}
> ⚠️ **Second Brain unreachable this run.** Error: {{error_summary}}. This report is a
> flagged gap so the outage is itself audit-trailed; posted to `#ops`.
{{/if}}
