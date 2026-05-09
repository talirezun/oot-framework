---
title: "Decision {{DECISION_ID}} — {{HEADLINE}}"
slug: decisions/{{DECISION_ID}}
domain: firm
type: decision
decision_id: {{DECISION_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [{{ACCOUNTABLE}}]
status: {{proposed_or_accepted_or_superseded}}
accountable: {{ACCOUNTABLE}}
consulted: {{CONSULTED_LIST}}
reversal_threshold: "{{THRESHOLD_OR_IRREVERSIBLE}}"
review_date: {{REVIEW_DATE_OR_NA}}
---

# {{HEADLINE}}

**Date:** {{DATE}}
**Accountable:** [[partners/{{ACCOUNTABLE}}]]
**Consulted:** {{CONSULTED_LINKS}}

## Context

{{WHY_THIS_DECISION_IS_BEING_MADE}}

## Options considered

{{OPTIONS}}

## Decision

{{CHOSEN_OPTION_AND_RATIONALE}}

## Reversal threshold

{{IF_REVERSIBLE_WHAT_WOULD_TRIGGER_REVERSAL}}

## Review date

{{REVIEW_DATE_OR_NA}}

## Cross-references

- BR where decision was taken: [[../business-reviews/{{BR_DATE}}]]
- Related Klarna Test (if any): [[../klarna-tests/{{TEST_ID}}]]
- Related ADR (if any): [[../architecture/{{ADR_ID}}]]
