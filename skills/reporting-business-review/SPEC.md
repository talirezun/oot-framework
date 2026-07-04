# Skill Pack S5 — Reporting & Business Review: SPEC

> **Historical build spec (pre-v1.0.1 in places). Where this file and SKILL.md disagree, SKILL.md is authoritative.**

**ID:** S5
**Name:** Reporting & Business Review
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

The **operational heartbeat** of an ØØT firm. Replaces all status meetings with a Brain-generated agenda for the Friday Business Review (BR). Encodes the daily / weekly / monthly / quarterly cadences, the rolling-forecast principle from Beyond Budgeting, the per-partner check-in structure, and the decision-logging discipline that keeps the partnership accountable without surveillance.

---

## Scope

**Covers:**
- Daily ledger update (Routine R1 ownership shared with S3).
- **Friday Business Review agenda generation** (Routine R2 ownership).
- The 30-minute BR meeting structure and discipline.
- Monthly KPI rollup.
- Quarterly partner check-in structure.
- Decision logging in the Brain (every BR decision becomes a versioned `firm/decisions/D-YYYY-NNN.md`).
- Blocker surfacing (the BR's standing "what's stuck" agenda item).
- Klarna Test status as a standing BR agenda item.
- The "long meeting" anti-pattern diagnostic.

**Does NOT cover:**
- The variable pay calculation itself (S3).
- Treasury reporting (S10 — Tier 2).
- Long-cycle strategic planning (founder-level work, not BR work).
- All-hands / town-hall meetings (out of scope; the framework discourages them in favour of Brain-published founder updates).

---

## Allowed tools / dependencies

- **Curator MCP** — read ledger, write BR summaries to Brain.
- **openpyxl in code execution on the Ledger clone (both tracks, per [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md))** — read X1, write X3, then signed-commit + push; cloud and privacy Routines perform the identical operation (no Google Sheets). Excel MCP is an optional human-in-the-loop inspection tool only.
- **Slack MCP** (cloud) **/ 4thtech CLI** (privacy) — read configured channels for blockers and decisions; post BR draft summary.
- **Calendar MCP** — invite the BR meeting; schedule the quarterly partner check-in.

---

## When to invoke

1. **Friday morning**, when R2 fires at 08:00 — the pack populates X3 Weekly_Review and posts a draft to Slack.
2. **At the BR meeting itself** (14:00 typical) — the facilitator runs through the structure (§4.3); the scribe captures decisions.
3. **Post-BR**, when the facilitator commits the meeting summary to the Brain.
4. **Monthly** — the pack rolls up four BR summaries into the Monthly_BR sheet.
5. **Quarterly** — the pack drives the per-partner check-in template generation.
6. **Ad-hoc** when a decision needs logging outside the BR (e.g. a Tier-2 dispute resolution decision).

---

## When NOT to invoke

1. **For variable pay calculations** — that's S3.
2. **For status meetings outside the BR** — the discipline is that BR replaces them. If a status update is needed mid-week, it goes in the ledger or `#output-log`, not a meeting.
3. **For treasury reporting** — S10.
4. **For partner personnel discussions** (one-on-ones, performance conversations) — those are the quarterly check-in or ad-hoc, not the BR.

---

## Operational instructions

### 4.1 Daily ledger update (R1 invocation pattern, S5 contribution)

R1 is jointly owned by S3 (compensation side) and S5 (reporting side). S5's contribution at daily capture time:

1. After R1 finishes the day's capture, the pack reads the new rows.
2. Identifies any output `value_tier=S` with no Output Spec — flags as "needs spec or downgrade" for next BR.
3. Identifies any blocker tags raised in Slack/dChat that day — appends them to `firm/output-logs/<date>.md` in a `## Blockers raised today` section.
4. Updates the running KPI dashboard sheet in X3 (Monthly_BR rollup numbers refresh daily).

### 4.2 Friday BR agenda generation (R2 invocation; what to include, what to exclude)

R2 fires at 08:00 Friday. The pack's procedure:

1. Read `firm/output-logs/*` for the past 7 days. Aggregate.
2. **Notable outputs** (X3 Weekly_Review column B): top 5 outputs by `computed_variable` (which is `value_envelope × partner_multiplier × rework_flag`). Format as bullets, each with: partner wikilink, output_type, brief description (from output_spec_ref), value_tier.
3. **Blockers** (column C): query Brain for tags `blocker:open` raised in the past 7 days; query Slack/dChat for messages tagged `#blocker` that have not been resolved. Format: bullet list with raised_date, partner, brief description.
4. **Klarna Test status** (column D): read `klarna-test.xlsx` Decision_Log for any tests in `scoring | remediation | monitoring` state. Format: test_id, summary, days-since-trigger, owner.
5. **KPI movements** (column E): from X6 agent-skill-roi.xlsx and X8 treasury-runway.xlsx (if populated), compute week-over-week deltas on the canonical KPI set: customer count, treasury runway months, ai_skill_roi, partner_count, agent_human_ratio. Format: a small table.
6. **Decisions due** (column F): query Brain for pages tagged `decision-pending` in the past 7 days. Format: decision summary, owner, deadline.
7. Write the populated row to X3 Weekly_Review.
8. Post the draft summary to Slack `#business-review` (cloud) or 4thtech dChat `#business-review` (privacy) by 09:00 with this template:

   > **BR agenda for {{TODAY}} 14:00.** Highlights: {{TOP_3_NOTABLE}}. Klarna in flight: {{COUNT}}. Decisions due: {{COUNT}}. Pre-read X3 Weekly_Review row at [[business-reviews/{{DATE}}-pre]].

### 4.3 Running the BR (the 30-minute structure)

The BR is **30 minutes**, **on time**, **non-negotiable in length**. Discipline:

| Block | Time | What | Anti-pattern |
|---|---|---|---|
| **Outputs** | 10 min | Read top 5 from X3 column B. Brief congrats; sharp questions only on outliers. | Every partner narrating their week (that's the ledger's job) |
| **Blockers** | 5 min | Each open blocker: owner, ETA, what help is needed. | Solving the blocker in the meeting (move to a follow-up) |
| **Decisions** | 10 min | Work through Decisions_Due. Each decision the scribe records in `firm/decisions/D-YYYY-NNN.md`. | One decision dominating (20 min on a single decision = wrong forum; spawn a working session) |
| **Klarna status** | 3 min | Open tests; tests resolved this week; new tests triggered. | Skipping (the standing item is non-negotiable) |
| **KPI snapshot** | 2 min | One look at the KPI dashboard. Comment if something moved materially. | Detailed analysis (that's a monthly rollup, not BR) |

**Roles (rotate weekly, listed in the partners index page):**
- **Facilitator** — keeps to time, reads the agenda, calls on people.
- **Scribe** — captures decisions in the Brain page, in real time.
- **Decision-recorder** — same person as scribe in small orgs; in larger orgs a separate role.

### 4.4 BR summary commit to Brain

Within 30 minutes of the meeting ending:

1. Open the pre-meeting Brain page at `firm/business-reviews/<date>-pre.md` (R2 created it at 09:00).
2. Append the post-meeting content per `templates/brain/business-review.md`:
   - **Outputs discussion** notes (1-3 sentences per discussed output).
   - **Blocker notes** (per blocker: who's helping, ETA).
   - **Decisions taken** (each linked to its `firm/decisions/D-YYYY-NNN.md`).
   - **Klarna discussion** (anything noteworthy).
   - **KPI discussion** (anything that moved materially).
   - **Action items** with owners and deadlines.
3. Rename the page to remove the `-pre` suffix → `firm/business-reviews/<date>.md`.
4. Set `status: active` in frontmatter.
5. Commit to the Brain via signed git commit.
6. Post a short follow-up to Slack/dChat `#business-review`: "{{DATE}} BR done. {{N_DECISIONS}} decisions, {{N_BLOCKERS_RESOLVED}} blockers resolved, {{N_NEW_BLOCKERS}} new. Summary at [[business-reviews/{{DATE}}]]."

### 4.5 Monthly rollup

On the 1st of each month, the pack rolls up the prior month's BR summaries:

1. Read all BR pages for the closed month (typically 4).
2. Populate X3 Monthly_BR row: month, total_outputs, total_variable_paid, gross_margin, treasury_runway_months, customer_count_delta, partner_count, klarna_tests_proceeded, klarna_tests_held, ai_skill_roi.
3. Generate a monthly digest at `firm/business-reviews/monthly-rollups/YYYY-MM.md` summarising the four BRs in 400-600 words.
4. The founder uses this as input for the quarterly partner check-in.

### 4.6 Quarterly partner check-in structure

Per partner, with the founder or designated lead. **45-60 minutes**. Quarterly cadence.

Pre-read for the founder (the pack generates this at quarter-open):

- The partner's variable pay trend (last 4 months from X1 Monthly_Variable).
- Long-tail growth (cumulative `total_settled_to_date` from X2 Long_Tail_Schedule).
- Reward species declared vs. observed cohort behaviour (from output mix).
- Any disputes in the quarter.
- Any Klarna Tests where they were affected partner or non-beneficiary reviewer.
- Any AI Champion candidacy signals (from S6).

Pre-read for the partner: their own variable statements + their own Output Specs from the quarter, plus the partner-side question prompts:

- Is your reward species still right?
- Is your output mix where you wanted it?
- What did the firm get wrong this quarter that affected you?
- What do you want to do differently next quarter?
- Two Worlds of Code self-id: still accurate?
- Any Klarna-test-able decisions you observed that were *not* tested?

The conversation is unstructured but covers all of the above. Outcomes are recorded as a **co-authored Brain page** at `firm/partners/<id>/check-ins/YYYY-Q<N>.md` (founder + partner edit; both sign by ticking ack boxes).

### 4.7 The "long meeting" anti-pattern diagnostic

If a BR runs >30 minutes more than once in a quarter, the pack runs a diagnostic at the next BR's start (5 minutes added):

- Was the agenda overstuffed? (Move the excess to next week or a working session.)
- Was a decision under-prepared? (Decision should not appear in BR until pre-read material is committed to Brain ≥24h prior.)
- Is the partnership using BR as a substitute for one-on-ones? (Move to quarterly check-in or ad-hoc 1-1.)
- Is one partner dominating? (Facilitator addresses directly; the framework's authors find this is the most common cause.)

### 4.8 Decision logging discipline

Every decision taken in a BR (or anywhere else) is a Brain page. Per `templates/brain/decision-record.md`:

- `decision_id` (D-YYYY-NNN, sequential per year).
- `accountable` (single partner per the RACI matrix).
- `consulted` (partners whose input was solicited).
- `reversal_threshold` (free text or "irreversible").
- `review_date` (if the decision is reversible / time-bounded).

The pack's discipline: **no decision in the BR notes without a corresponding `firm/decisions/D-YYYY-NNN.md` page.** The scribe creates the page during the meeting; the facilitator confirms the decision_id is recorded in the X3 Decisions_Log.

---

## Brain interaction protocol

**Reads:**
- `firm/output-logs/*` — for BR agenda generation.
- `firm/klarna-tests/*` — for Klarna status block.
- `firm/decisions/*` — for decisions-pending tag scan.
- `firm/partners/<id>/variable-statements/*` — for quarterly check-in pre-read.

**Writes:**
- `firm/business-reviews/<date>.md` — weekly.
- `firm/business-reviews/monthly-rollups/<month>.md` — monthly.
- `firm/decisions/D-YYYY-NNN.md` — per decision.
- `firm/partners/<id>/check-ins/<quarter>.md` — quarterly.

---

## Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X3 business-review.xlsx | Weekly_Review | Write (populate Friday-morning row) | R2 |
| X3 | Decisions_Log | Append | During BR meeting |
| X3 | Blockers | Update | Per blocker resolution |
| X3 | Monthly_BR | Append | Monthly (1st of month) |
| X3 | Klarna_Test_Hits | Mirror from X4 | R2 weekly |
| X1 | (read-only) | Read for aggregation | Daily / weekly |
| X6 agent-skill-roi.xlsx | (read-only) | Read for KPI movements | Weekly |
| X8 treasury-runway.xlsx | (read-only) | Read for runway KPI | Weekly (if X8 populated) |

---

## Routine integration

- **R2** (Weekly BR Prep) — owned by this pack.
- **R1** (Daily Output Capture) — co-owned with S3; S5 contributes the blocker-surfacing and KPI-dashboard refresh.

---

## Don'ts

1. **Don't run a status meeting outside the BR** — if it's a status update, it goes in the ledger or `#output-log`.
2. **Don't extend a BR past 30 minutes** — if it's running long, the agenda is wrong; diagnose at the next BR.
3. **Don't use the BR for personnel discussions** — those go in the quarterly check-in or ad-hoc 1-1s.
4. **Don't auto-publish BR summaries externally** — they may contain sensitive partner-level data.
5. **Don't take a decision in the BR without a `firm/decisions/D-YYYY-NNN.md` page being created during the meeting** — the page is the audit trail.
6. **Don't skip the Klarna status block** even if there are no open tests — the absence is itself information.
7. **Don't run a BR with the same facilitator more than 4 weeks in a row** — rotation is a deliberate discipline (the meeting belongs to the partnership).
8. **Don't allow a blocker to persist past 2 BRs without escalation** — at the third BR, the blocker becomes a decision-pending item; the partnership decides on path forward.

---

## Quick reference

| Situation | Action | Output |
|---|---|---|
| Friday 08:00 | R2 fires; §4.2 populates X3 Weekly_Review | X3 row + Slack draft |
| Friday 14:00 | BR meeting; §4.3 30-min structure | Decisions logged in real time |
| Friday 14:30 | Scribe finalises §4.4 | `firm/business-reviews/<date>.md` |
| 1st of month | §4.5 monthly rollup | X3 Monthly_BR + monthly digest Brain page |
| Quarterly | §4.6 partner check-in | Per-partner check-in Brain page |
| BR ran long | §4.7 diagnostic at next BR | Diagnostic notes appended to next BR page |

---

## Worked examples concept

**2 worked examples in `examples/`:**

1. **A typical Friday BR end-to-end**. Real-feeling firm with 8 partners. Friday 08:00: R2 fires, populates X3, posts Slack draft. The example shows the actual draft text, the actual Brain page state. 14:00: facilitator runs the 30-min structure. The example shows the full meeting notes — what was said in each block, where the facilitator cut someone off (politely), how a decision was logged in real time. 14:30: scribe finalises. The Brain page is shown verbatim.

2. **A BR where the agenda was wrong**. The pre-read had 8 decisions due. The first decision took 22 minutes. The facilitator paused the meeting and applied §4.7 diagnostic: too many decisions, one was under-prepared. The pack walks through the recovery: tabling 5 decisions for the following week with explicit pre-read commitments, the meeting closing on time at 14:30, the next week's BR being clean.

---

## References

1. **Hope, J. & Fraser, R.** *Beyond Budgeting: How Managers Can Break Free from the Annual Performance Trap* (Harvard Business School Press, 2003). The rolling-forecast and continuous-allocation principles the pack borrows.
2. **Microsoft.** *Work Trend Index 2025: The Frontier Firm*. The "human-agent ratio" and KPI framing.
3. **Cali Ressler & Jody Thompson.** *Why Work Sucks and How to Fix It* (2008). ROWE — the basis for the "BR replaces status meetings" discipline.
4. ØØT `MANIFESTO.md`, Thesis 1 — Resistance.
5. ØØT `MANIFESTO.md`, Thesis 3 — Partner compensation (the BR as the compensation feedback loop).
6. ØØT `templates/excel/SPEC.md` — X1, X3 schemas the pack relies on.
7. ØØT `governance/DECISION-RIGHTS.md` — the RACI matrix the decisions reference.

---

## Acceptance criteria

Standard. Plus:
- The 30-minute structure (§4.3) is reproduced as a verbatim block facilitators can paste into a meeting note.
- The diagnostic for "BR ran long" (§4.7) is documented with at least one example pattern of each type.
- The decision-logging discipline (every decision = a Brain page) is enforced in the Don'ts list.
- 2+ worked examples in `examples/`.
- A sample BR summary template lives at `examples/sample-br-summary.md`.
- Frontmatter passes the Phase 8 linter.
