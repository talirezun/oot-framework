---
title: "Friday Business Review — {{DATE}}"
slug: business-reviews/{{DATE}}
domain: firm
type: business-review
week_starting: {{MONDAY_DATE}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r2, {{FACILITATOR}}]
status: {{draft_or_active}}
attendees: {{ATTENDEE_LIST}}
decisions_logged: {{N_DECISIONS}}
---

# Friday Business Review — {{DATE}}

**Week:** {{MONDAY_DATE}} → {{DATE}}
**Facilitator:** [[partners/{{FACILITATOR}}]]
**Scribe:** [[partners/{{SCRIBE}}]]

## Pre-meeting (R2 — generated 08:00 today)

### Notable outputs (top 5 by value envelope)

{{NOTABLE_OUTPUTS}}

### Open blockers

{{BLOCKERS}}

### Klarna Test status

{{KLARNA_STATUS}}

### KPI movements (week-over-week)

{{KPI_DELTA}}

### Decisions due

{{DECISIONS_DUE}}

---

## Meeting (post-14:00 — facilitator authors)

### Outputs discussion (10 min)

{{OUTPUTS_NOTES}}

### Blockers (5 min)

{{BLOCKER_NOTES}}

### Decisions (10 min)

{{#each decisions_taken}}
- **D-{{decision_id}}** — {{summary}} — Accountable: [[partners/{{accountable}}]] — Decision: {{outcome}} → see [[decisions/{{decision_id}}]]
{{/each}}

### Klarna status (3 min)

{{KLARNA_DISCUSSION}}

### KPI snapshot (2 min)

{{KPI_DISCUSSION}}

## Post-meeting

- Recording / transcript: {{RECORDING_LINK}}
- Action items committed: {{N_ACTIONS}}
- Next BR: {{NEXT_FRIDAY_DATE}}
