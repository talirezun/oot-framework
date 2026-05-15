# Brain Page Templates — SPEC

Specification for the markdown templates Routines and partners use when creating pages. Phase 4 of `BUILD-INSTRUCTIONS.md` generates the actual `.md` template files in this folder; this SPEC defines what each one must contain.

All templates use Mustache-style `{{placeholders}}`. Frontmatter follows the schema in [`FIRM-ONTOLOGY.md`](FIRM-ONTOLOGY.md).

**Two-repo split (per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md)):** Routine-authored operational artefacts live in the **Ledger** repo; partner-authored firm IP lives in the **Firm Brain** repo as a Curator Shared Brain. The "Lives in" column below names the destination for each template.

**Slug prefixing inside the Firm Brain:** Curator Shared Brain prescribes a top-level `entities / concepts / summaries` taxonomy. Firm Brain pages use the appropriate prefix in their slug — e.g., `entities/decisions/D-2026-005`, `entities/architecture/ADR-2026-003`, `entities/partners/<id>`, `concepts/theses`, `summaries/retrospectives/2026-Q2`. Ledger pages keep their flat `firm/<category>/<file>` slugs because they're plain markdown in a git repo, not Curator-managed.

---

## Templates to generate (Phase 4)

| File | Used by | Lives in | Purpose |
|---|---|---|---|
| `daily-output-log.md` | R1 | **Ledger** | One file per day under `firm/output-logs/`. Lists outputs captured, anomalies, retroactive rework detections. |
| `audit-log-day.md` | R6 | **Ledger** | One file per day under `firm/audit-logs/`. Article 12 audit trail. |
| `business-review.md` | R2 + facilitator | **Ledger** | One file per Friday under `firm/business-reviews/`. Pre-meeting agenda + post-meeting outcomes. |
| `klarna-test-page.md` | R7 + S6 | **Ledger** | One file per Klarna Test (`KT-YYYY-NNN`). Full context, scores, decision, 90-day review pointer. |
| `variable-statement.md` | R3 | **Ledger** | One file per partner per month under `firm/partners/<id>/variable-statements/`. Statement + ack block. |
| `long-tail-statement.md` | R4 | **Ledger** | One file per partner per quarter under `firm/partners/<id>/long-tail-statements/`. Per-output settlement detail. |
| `dispute-record.md` | DECISION-RIGHTS.md three-tier flow | **Ledger** | One file per dispute under `firm/compensation/<month>/disputes/`. |
| `output-spec.md` | S3 (partner-authored) | **Firm Brain** | One file per Output Spec under `entities/partners/<id>/output-specs/`. Pushed via the partner's `firm` opted-in domain; referenced by R1 (which clones the Firm Brain to read it). |
| `partner-profile.md` | S3 onboarding (partner-authored) | **Firm Brain** | The per-partner identity page at `entities/partners/<id>`. Each partner authors their own. |
| `reward-species-declaration-summary.md` | S3 onboarding (partner-authored) | **Firm Brain** | The summary page at `entities/partners/<id>/reward-species-declaration`. **Operative truth is in the Ledger** (X2 row + signed PDF); this is the human-readable mirror. |
| `decision-record.md` | S5 (partner-authored) | **Firm Brain** | One file per decision at `entities/decisions/D-YYYY-NNN`. Lightweight ADR for non-architectural decisions. |
| `adr.md` | S4 (partner-authored) | **Firm Brain** | One file per architectural decision at `entities/architecture/ADR-YYYY-NNN`. |
| `pilot-summary.md` | S6 (partner-authored) | **Firm Brain** | One file per pilot at `entities/pilots/<pilot_id>`. |
| `prompt-artefact.md` | S2 (partner-authored) | **Firm Brain** | One file per reusable prompt at `entities/prompts/<prompt_slug>`. |

**Write paths:** Ledger templates are written by Routines (signed commits on protected branch) or by partners editing in the Ledger repo (ack edits, dispute filing). Firm Brain templates are authored in the partner's *personal* Curator opted-in domain and pushed via Curator's `DeltaSummary` protocol; the admin's weekly Synthesize merges contributions into `collective/<firm-domain>/wiki/`.

Each template below specifies: required frontmatter, required sections, optional sections, hard constraints. Generators must not omit required sections or rename them.

---

## `daily-output-log.md`

```markdown
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
```

---

## `audit-log-day.md`

```markdown
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

This page is part of the firm's Article 12 record-keeping. It is append-only; do not edit historical entries. Corrections are made by appending a new dated entry that supersedes the prior. The branch protecting this path requires signed commits and disallows force-push.

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
- **Human reviewer:** {{human_reviewer | "(none — fully agentic; review use_case classification)"}}
- **Annex III mapping:** {{annex_iii_category | "Limited risk — no Annex III mapping"}}
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
```

---

## `business-review.md`

```markdown
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
```

---

## `klarna-test-page.md`

```markdown
---
title: "Klarna Test {{TEST_ID}} — {{DECISION_SUMMARY}}"
slug: klarna-tests/{{TEST_ID}}
domain: firm
type: klarna-test
test_id: {{TEST_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r7, {{SCORER}}]
status: {{scoring | proceeded | held | abandoned}}
score: {{TOTAL_SCORE}}
decision: {{PROCEED | HOLD | ABANDON}}
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
```

---

## `variable-statement.md`

```markdown
---
title: "Variable pay statement — [[partners/{{PARTNER_ID}}]] — {{MONTH}}"
slug: partners/{{PARTNER_ID}}/variable-statements/{{MONTH}}
domain: firm
type: variable-statement
partner_id: {{PARTNER_ID}}
month: {{MONTH}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r3]
status: active
total_compensation: {{TOTAL}}
ack_status: pending
---

# Variable pay statement — {{MONTH}}

**Partner:** [[partners/{{PARTNER_ID}}]]
**Month covered:** {{MONTH}} ({{MONTH_START}} → {{MONTH_END}})
**Currency:** {{CURRENCY}}

## Compensation summary

| Component | Amount |
|---|---:|
| Base (proportional) | {{BASE}} |
| Variable | {{VARIABLE}} |
| **Total** | **{{TOTAL}}** |

## Variable pay computation

- Total outputs: {{N_OUTPUTS}}
- Total `value_envelope` × `partner_multiplier`: {{RAW_VARIABLE}}
- Rework-within-30d zero-outs (this month): {{REWORK_ZEROOUTS_THIS_MONTH}}
- **Net variable: {{VARIABLE}}**

### Top 5 outputs by computed_variable

{{#each top_outputs}}
- {{date}} — `{{output_type}}` — {{output_ref}} — value tier `{{value_tier}}` — €{{computed_variable}} — [[../../output-specs/{{output_spec_slug}}]]
{{/each}}

### Retroactive zero-outs from prior months affecting this month's pool

{{#if prior_month_zeroouts}}
{{#each prior_month_zeroouts}}
- {{original_log_id}} (originally {{original_date}}, originally €{{original_variable}}) → flipped to rework=Yes by R1 on {{flip_date}}. Net effect on this month: €0.00.
{{/each}}
{{else}}
None.
{{/if}}

## Acknowledgement

- [ ] I have reviewed this statement and agree with the calculation.
- [ ] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).

_Sign by editing this page and ticking the appropriate box, then commit. R3 reads the first checked box once per day._

## Audit trail

- Generated by: routine-r3 at {{GENERATION_TIMESTAMP}}
- Source ledger snapshot: [[../../../output-logs/{{MONTH_END}}]]
- Reward species declaration in effect: [[../reward-species-declaration]] (version {{RSD_VERSION}})
- Founder approval pending — see [[../../../compensation/{{MONTH}}/founder-approval]]
```

---

## `long-tail-statement.md`

```markdown
---
title: "Long-tail statement — [[partners/{{PARTNER_ID}}]] — {{QUARTER}}"
slug: partners/{{PARTNER_ID}}/long-tail-statements/{{QUARTER}}
domain: firm
type: long-tail-statement
partner_id: {{PARTNER_ID}}
quarter: {{QUARTER}}
created: {{DATE}}
updated: {{DATE}}
authors: [routine-r4]
status: active
total_payment: {{TOTAL}}
---

# Long-tail statement — {{QUARTER}}

**Partner:** [[partners/{{PARTNER_ID}}]]
**Quarter covered:** {{QUARTER}} ({{QUARTER_START}} → {{QUARTER_END}})
**Currency:** {{CURRENCY}}

## Per-output settlements

| Output | Description | Outcome (this quarter) | Partner share % | Payment |
|---|---|---:|---:|---:|
{{#each settlements}}
| [[../output-specs/{{output_spec_slug}}]] | {{description}} | {{outcome_realised}} | {{partner_share_pct}}% | {{payment_amount}} |
{{/each}}
| | | | **Total** | **{{TOTAL}}** |

## Acknowledgement

- [ ] I have reviewed this statement and agree with the calculation.
- [ ] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).

## Audit trail

- Generated by: routine-r4 at {{GENERATION_TIMESTAMP}}
- Reward species declaration in effect: [[../reward-species-declaration]] (version {{RSD_VERSION}})
- Outcome attribution methodology: [[../../../routines/R4]]
```

---

## `output-spec.md`

```markdown
---
title: "Output spec — {{TITLE}}"
slug: partners/{{PARTNER_ID}}/output-specs/{{DATE}}--{{SHORT_SLUG}}
domain: firm
type: output-spec
partner_id: {{PARTNER_ID}}
value_tier: {{S | M | L | XS}}
created: {{DATE}}
updated: {{DATE}}
authors: [{{PARTNER_ID}}]
status: {{drafted | accepted | shipped | rework | abandoned}}
expected_outcome: "{{ONE_SENTENCE_OUTCOME}}"
outcome_review_date: {{REVIEW_DATE}}
linked_pr_or_contract: {{LINK}}
---

# Output spec — {{TITLE}}

**Partner:** [[partners/{{PARTNER_ID}}]]
**Drafted:** {{DATE}}
**Value tier:** {{VALUE_TIER}} (envelope {{ENVELOPE}})
**Expected outcome:** {{EXPECTED_OUTCOME}}
**Outcome review date:** {{REVIEW_DATE}}

## What "done" looks like

{{ACCEPTANCE_CRITERIA}}

## What's explicitly out of scope

{{OUT_OF_SCOPE}}

## Risks / dependencies

{{RISKS}}

## Long-tail entitlement (if applicable)

If this output is eligible for long-tail entitlement:

- **Outcome metric:** {{OUTCOME_METRIC}} (the realised value attributable to this output, measured at quarterly settlement)
- **Partner share %:** {{PARTNER_SHARE}}
- **Settlement period:** quarterly
- **Long-tail end date or "ongoing":** {{LONG_TAIL_END}}

## Sign-off

- Drafted by: [[partners/{{PARTNER_ID}}]] on {{DATE}}
- Accepted by: [[partners/{{ACCEPTOR_ID}}]] on {{ACCEPTANCE_DATE}}
- Shipped: {{SHIP_DATE | "not yet"}}
```

---

## `partner-profile.md`, `reward-species-declaration-summary.md`

Standard structure: identity fields, jurisdiction, two-worlds-of-code self-declaration, links to all other partner pages. Generators follow the frontmatter schema in `FIRM-ONTOLOGY.md`.

---

## `decision-record.md`

```markdown
---
title: "Decision {{DECISION_ID}} — {{HEADLINE}}"
slug: decisions/{{DECISION_ID}}
domain: firm
type: decision
decision_id: {{DECISION_ID}}
created: {{DATE}}
updated: {{DATE}}
authors: [{{ACCOUNTABLE}}]
status: {{proposed | accepted | superseded}}
accountable: {{ACCOUNTABLE}}
consulted: {{CONSULTED_LIST}}
reversal_threshold: "{{THRESHOLD_OR_IRREVERSIBLE}}"
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

## Review date (if applicable)

{{REVIEW_DATE_OR_NA}}
```

---

## `adr.md`

Same shape as `decision-record.md` but `type: adr`, slug `architecture/ADR-YYYY-NNN`, includes a `status_chain` field tracking proposed → accepted → superseded. Used for technology / architecture choices specifically; `decisions/` is for everything else.

---

## `pilot-summary.md`, `dispute-record.md`, `prompt-artefact.md`

Standard structure per their corresponding Skill Pack (S6, the dispute flow in DECISION-RIGHTS.md, S2 respectively). Generators must include:

- For `pilot-summary.md`: `pilot_id`, `start_date`, `end_date`, `cohort_partner_ids`, METR-baseline-vs-result table, decision (proceed / iterate / abandon), Klarna Test reference if proceed.
- For `dispute-record.md`: tier (1/2/3), parties, raised date, resolution date, outcome, links to renegotiation if applicable.
- For `prompt-artefact.md`: prompt_id, version (semver), input/output signatures, fenced prompt body, success criteria, citations.

---

## Acceptance criteria for Phase 4 generation

For each template:

- All required frontmatter fields present.
- All required sections present in the order specified.
- Mustache placeholders use the exact names listed in this SPEC.
- The first three lines of the file are `---\ntitle: ...` (frontmatter open) — no shebang or BOM.
- Examples of populated outputs live in `examples/` once Phase 9 generates the reference orgs.
