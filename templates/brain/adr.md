---
title: "ADR {{ADR_ID}} — {{HEADLINE}}"
slug: architecture/{{ADR_ID}}
domain: firm
type: adr
adr_id: {{ADR_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [{{AUTHOR_PARTNER_ID}}]
status: {{proposed_or_accepted_or_superseded}}
status_chain: [{{proposed_DATE}}, {{accepted_DATE_OR_NA}}, {{superseded_DATE_OR_NA}}]
superseded_by: {{ADR_ID_OR_NA}}
supersedes: {{ADR_ID_OR_NA}}
---

# {{HEADLINE}}

**ADR ID:** {{ADR_ID}}
**Status:** {{STATUS}}
**Author:** [[partners/{{AUTHOR_PARTNER_ID}}]]
**Reviewers:** {{REVIEWERS_LINKS}}

## Context

{{WHAT_FORCED_THE_DECISION}}

## Decision

{{WHAT_WE_CHOSE}}

## Consequences

### What this enables

{{ENABLES}}

### What this forbids

{{FORBIDS}}

### What this changes about how we work

{{WORKFLOW_IMPACT}}

## Considered alternatives

{{#each alternatives}}
### {{name}}

{{description}}

**Why we didn't choose it:** {{rejection_reason}}

{{/each}}

## Related

- Brain decisions: {{RELATED_DECISION_LINKS}}
- PRs: {{RELATED_PR_LINKS}}
- Skill Pack(s): {{RELATED_SKILL_PACK_LINKS}}
