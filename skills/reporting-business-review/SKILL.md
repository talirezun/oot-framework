---
name: reporting-business-review
description: Use whenever the partnership runs the Friday Business Review (BR), processes the daily output ledger update, generates the BR agenda (R2 invocation), captures decisions during the meeting, runs the monthly KPI rollup, or schedules the quarterly partner check-in. Activates for "prep this week's BR", "what's the agenda for Friday?", "log this decision from the BR", "monthly rollup for May", "quarterly check-in pre-read for Mira". Enforces the 30-minute BR structure (Outputs 10 / Blockers 5 / Decisions 10 / Klarna 3 / KPI 2), the decision-logging discipline (every BR decision becomes a `firm/decisions/D-YYYY-NNN.md` Brain page), the rotation of facilitator/scribe roles, and the "BR ran long" diagnostic.
version: 1.0.0
tier: 1
status: hardened
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__search_wiki
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__excel__append_row
  - mcp__slack__post_message
  - mcp__google-calendar__create_event
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S5
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1, S2, S3]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-08
---

# Reporting & Business Review

> **Generation marker:** Hardened in v1.0.
> **Klarna Test interaction:** No (the BR includes Klarna status as a standing agenda item, but the pack does not score tests).
> **Brain interaction:** Both — reads ledger, decisions, partner pages; writes BR summaries, decision records, monthly digests, quarterly check-in pages.

## 1. Purpose

The **operational heartbeat** of an ØØT firm. Replaces all status meetings with a Brain-generated agenda for the Friday Business Review (BR). Encodes the daily / weekly / monthly / quarterly cadences, the rolling-forecast principle from Beyond Budgeting, the per-partner check-in structure, and the decision-logging discipline that keeps the partnership accountable without surveillance.

## 2. When to invoke this pack

1. **Friday morning** when R2 fires at 08:00.
2. **At the BR meeting itself** (14:00 typical) — facilitator runs the structure (§4.3); scribe captures decisions.
3. **Post-BR**, when the facilitator commits the meeting summary to the Brain.
4. **Monthly** — pack rolls up four BRs into the Monthly_BR sheet.
5. **Quarterly** — pack drives per-partner check-in template generation.
6. **Ad-hoc** when a decision needs logging outside the BR (e.g. a Tier-2 dispute resolution).

## 3. When NOT to invoke this pack

1. Variable pay calculations — S3.
2. Status meetings outside the BR — discipline is BR replaces them. Mid-week status update goes in the ledger or `#output-log`, not a meeting.
3. Treasury reporting — S10.
4. Personnel discussions — quarterly check-in or ad-hoc 1-1, not the BR.

## 4. Operational instructions

### 4.1 Daily ledger update (R1, S5 contribution)

R1 is co-owned by S3 (compensation) and S5 (reporting). S5's contribution after R1 finishes daily capture:

1. Read new X1 rows.
2. Identify any `value_tier=S` output with no Output Spec — flag "needs spec or downgrade" for next BR.
3. Identify blocker tags raised in Slack/dChat that day — append to `firm/output-logs/<date>.md` `## Blockers raised today` section.
4. Refresh running KPI dashboard in X3 Monthly_BR (numbers refresh daily).

### 4.2 Friday BR agenda generation (R2 — 08:00)

R2 fires at 08:00 Friday. Procedure:

1. Read `firm/output-logs/*` for past 7 days.
2. **Notable outputs** (X3 col B): top 5 by `computed_variable`. Format: bullet per output with partner wikilink, output_type, brief description from output_spec_ref, value_tier.
3. **Blockers** (col C): query Brain for `blocker:open` tags raised in past 7 days; query Slack/dChat for `#blocker` not resolved. Format: raised_date, partner, brief description.
4. **Klarna Test status** (col D): read X4 Decision_Log for tests in `scoring | remediation | monitoring` state.
5. **KPI movements** (col E): from X6 + X8 if populated, week-over-week deltas on customer count, treasury runway months, ai_skill_roi, partner_count, agent_human_ratio.
6. **Decisions due** (col F): query Brain for `decision-pending` tags from past 7 days.
7. Write populated row to X3 Weekly_Review.
8. Post to Slack `#business-review` (or 4thtech dChat) by 09:00:

   > **BR agenda for {{TODAY}} 14:00.** Highlights: {{TOP_3_NOTABLE}}. Klarna in flight: {{COUNT}}. Decisions due: {{COUNT}}. Pre-read X3 Weekly_Review row at [[business-reviews/{{DATE}}-pre]].

### 4.3 Running the BR — the 30-minute structure

**30 minutes. On time. Non-negotiable.**

| Block | Time | What | Anti-pattern |
|---|---|---|---|
| **Outputs** | 10 min | Read top 5 from X3 col B. Brief congrats; sharp questions only on outliers. | Every partner narrating their week (that's the ledger's job). |
| **Blockers** | 5 min | Each open blocker: owner, ETA, what help is needed. | Solving the blocker in the meeting (move to follow-up). |
| **Decisions** | 10 min | Work through Decisions_Due. Each decision the scribe records in `firm/decisions/D-YYYY-NNN.md`. | One decision dominating (>5 min on a single decision = wrong forum; spawn a working session). |
| **Klarna status** | 3 min | Open tests; tests resolved this week; new tests triggered. | Skipping (the standing item is non-negotiable). |
| **KPI snapshot** | 2 min | One look at the dashboard. Comment if something moved materially. | Detailed analysis (that's monthly rollup, not BR). |

**Roles (rotate weekly):**
- **Facilitator** — keeps to time; reads agenda; calls on people.
- **Scribe** — captures decisions in real time.
- **Decision-recorder** — same as scribe in small orgs; separate role in larger.

### 4.4 BR summary commit to Brain

Within 30 minutes of meeting end:

1. Open `firm/business-reviews/<date>-pre.md` (R2 created it at 09:00).
2. Append post-meeting content per `templates/brain/business-review.md`:
   - Outputs discussion (1–3 sentences per discussed output).
   - Blocker notes (per blocker: who's helping, ETA).
   - Decisions taken (each linked to its `firm/decisions/D-YYYY-NNN.md`).
   - Klarna discussion (anything noteworthy).
   - KPI discussion (anything that moved materially).
   - Action items with owners and deadlines.
3. Rename the page: remove `-pre` suffix → `firm/business-reviews/<date>.md`.
4. Set frontmatter `status: active`.
5. Signed git commit.
6. Post follow-up to Slack/dChat `#business-review`:

   > {{DATE}} BR done. {{N_DECISIONS}} decisions, {{N_BLOCKERS_RESOLVED}} blockers resolved, {{N_NEW_BLOCKERS}} new. Summary at [[business-reviews/{{DATE}}]].

### 4.5 Monthly rollup

On the 1st of each month:

1. Read all BR pages for closed month (typically 4).
2. Populate X3 Monthly_BR row: month, total_outputs, total_variable_paid, gross_margin, treasury_runway_months, customer_count_delta, partner_count, klarna_tests_proceeded, klarna_tests_held, ai_skill_roi.
3. Generate monthly digest at `firm/business-reviews/monthly-rollups/YYYY-MM.md` (400–600 words).

### 4.6 Quarterly partner check-in

Per partner with founder. **45–60 minutes**. Quarterly cadence.

**Founder pre-read** (pack generates at quarter open):
- Variable pay trend (last 4 months from X1 Monthly_Variable).
- Long-tail growth (cumulative from X2 Long_Tail_Schedule).
- Reward species declared vs. observed cohort behaviour (from output mix).
- Any disputes in the quarter.
- Any Klarna Tests where they were affected partner or non-beneficiary reviewer.
- AI Champion candidacy signals (from S6).

**Partner pre-read:** their own variable statements + their own Output Specs from the quarter, plus the partner-side question prompts:
- Is your reward species still right?
- Is your output mix where you wanted it?
- What did the firm get wrong this quarter that affected you?
- What do you want to do differently next quarter?
- Two Worlds of Code self-id: still accurate?
- Any Klarna-test-able decisions you observed that were *not* tested?

Conversation unstructured. Outcomes recorded as **co-authored Brain page** at `firm/partners/<id>/check-ins/YYYY-Q<N>.md` (founder + partner edit; both sign by ticking ack boxes).

### 4.7 The "BR ran long" diagnostic

If a BR runs >30 min more than once in a quarter, run diagnostic at next BR's start (5 min added):

- Was the agenda overstuffed? Move excess to next week or a working session.
- Was a decision under-prepared? Decision should not appear in BR until pre-read material is committed to Brain ≥24h prior.
- Is the partnership using BR as a substitute for one-on-ones? Move to quarterly check-in or ad-hoc 1-1.
- Is one partner dominating? Facilitator addresses directly; the framework's authors find this is the most common cause.

### 4.8 Decision logging discipline

Every decision in a BR (or anywhere) is a Brain page per `templates/brain/decision-record.md`:

- `decision_id` (D-YYYY-NNN, sequential per year).
- `accountable` (single partner per RACI matrix).
- `consulted` (partners whose input was solicited).
- `reversal_threshold` (free text or "irreversible").
- `review_date` (if reversible / time-bounded).

**No decision in BR notes without a corresponding `firm/decisions/D-YYYY-NNN.md` page.** The scribe creates it during the meeting; facilitator confirms decision_id is recorded in X3 Decisions_Log.

## 5. Brain interaction protocol

**Reads:** `firm/output-logs/*`; `firm/klarna-tests/*`; `firm/decisions/*`; `firm/partners/<id>/variable-statements/*`.

**Writes:** `firm/business-reviews/<date>.md`; `firm/business-reviews/monthly-rollups/<month>.md`; `firm/decisions/D-YYYY-NNN.md`; `firm/partners/<id>/check-ins/<quarter>.md`.

## 6. Excel interaction protocol

> **On the `mcp__excel__*` tools in this pack's frontmatter (ADR-001):** Excel writes go through **openpyxl in code execution on the Ledger clone on BOTH tracks** — cloud and privacy Routines perform the identical operation, then signed-commit + push; there is no Google Sheets path. The `mcp__excel__*` tools are **optional, human-in-the-loop only** (a founder inspecting or hand-patching a workbook at their workstation) and are never the Routine write path. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md).

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X3 business-review.xlsx | Weekly_Review | Write | R2 |
| X3 | Decisions_Log | Append | During BR |
| X3 | Blockers | Update | Per resolution |
| X3 | Monthly_BR | Append | Monthly |
| X3 | Klarna_Test_Hits | Mirror from X4 | R2 weekly |
| X1 | (read-only) | Read for aggregation | Daily/weekly |
| X6, X8 | (read-only) | Read for KPI movements | Weekly |

## 7. Routine integration

- **R2** owned by this pack.
- **R1** co-owned with S3 (S5 contributes blocker-surfacing + KPI dashboard refresh).

## 8. Don'ts

1. Don't run a status meeting outside the BR.
2. Don't extend a BR past 30 min — diagnose at next BR.
3. Don't use BR for personnel discussions.
4. Don't auto-publish BR summaries externally.
5. Don't take a decision in BR without creating `firm/decisions/D-YYYY-NNN.md` during the meeting.
6. Don't skip Klarna status block even if no open tests.
7. Don't run BR with same facilitator >4 weeks in a row.
8. Don't allow a blocker to persist past 2 BRs without escalation.

## 9. Quick reference

| Situation | Action | Output |
|---|---|---|
| Friday 08:00 | R2 fires; §4.2 | X3 row + Slack draft |
| Friday 14:00 | BR meeting; §4.3 | Decisions logged in real time |
| Friday 14:30 | Scribe finalises; §4.4 | `firm/business-reviews/<date>.md` |
| 1st of month | §4.5 monthly rollup | X3 Monthly_BR + monthly digest |
| Quarterly | §4.6 check-in | Per-partner check-in Brain page |
| BR ran long | §4.7 diagnostic at next BR | Diagnostic notes |

## 10. References

1. **Hope, J. & Fraser, R.** *Beyond Budgeting: How Managers Can Break Free from the Annual Performance Trap* (HBS Press, 2003).
2. **Microsoft.** *Work Trend Index 2025: The Frontier Firm.*
3. **Cali Ressler & Jody Thompson.** *Why Work Sucks and How to Fix It* (Penguin, 2008).
4. ØØT `MANIFESTO.md`, Thesis 1 — Resistance.
5. ØØT `MANIFESTO.md`, Thesis 3 — Partner compensation (BR as compensation feedback loop).
6. ØØT `templates/excel/SPEC.md` — X1, X3 schemas.
7. ØØT `governance/DECISION-RIGHTS.md` — RACI matrix.
