# W4 — Running the Friday Business Review

**Audience:** This week's BR facilitator (rotates among partners) plus all attendees.
**Time:** 30 minutes (the meeting). On time. Always.
**You will end with:** decisions logged in real time, a Ledger page committed within 30 min of meeting end, and the partnership's attention focused for next week.

> 📖 **Concept doc:** [`docs/04-running-the-business-review.md`](../04-running-the-business-review.md). **Skill Pack:** [`skills/reporting-business-review/SKILL.md`](../../skills/reporting-business-review/SKILL.md). **Routine:** [`routines/cloud/R2.md`](../../routines/cloud/R2.md).

---

## What this is + the first 5 minutes

The Friday BR replaces all status meetings. 30 minutes. R2 generates the agenda at 08:00. Meeting at 14:00. Brain page committed by 14:30.

**The 30-minute structure** (you will read this aloud as facilitator on minute 0):

| Block | Time | What |
|---|---|---|
| Outputs | 10 min | Top 5 from X3 column B. Quick acknowledgement; sharp questions only on outliers. |
| Blockers | 5 min | Each open blocker: owner, ETA, what help is needed. |
| Decisions | 10 min | Work through Decisions_Due. Each decision = a Ledger page. |
| Klarna status | 3 min | Open tests; resolved this week; new triggers. |
| KPI snapshot | 2 min | One look at the dashboard. Material movement only. |

---

## Your role this week — choose one

- **Facilitator:** keeps to time, reads agenda, calls on people. Your job is the clock + the structure.
- **Scribe:** captures decisions in real time. Creates `firm/decisions/D-YYYY-NNN.md` pages during the meeting.
- **Decision-recorder:** same as scribe in small orgs.

Roles rotate weekly. The framework's discipline: never let one partner facilitate >4 weeks in a row.

---

## Friday morning prep (09:00 — 13:30)

### 09:00 — Check Slack `#business-review`

R2 fired at 08:00. The draft summary should already be in Slack:

> **BR agenda for 2026-04-17 14:00.** Highlights: Davor S-tier onboarding rebuild merged; Anya signed Acme MSA; Mira payment-rail PR. Klarna in flight: 1 (KT-2026-015). Decisions due: 2 (Unit Fund pilot, Stripe replacement). Pre-read at [[business-reviews/2026-04-17-pre]].

![Slack #business-review draft](../images/W4-1-slack-draft.png)

*The draft includes the headline outputs, Klarna status count, decisions count, and a wikilink to the pre-meeting Brain page.*

---

### 09:30 — Open the X3 sheet

Open `templates/excel/business-review.xlsx`. Navigate to the **Weekly_Review** sheet. R2 populated this week's row at 08:00.

![X3 Weekly_Review row populated](../images/W4-2-x3-weekly-row.png)

*The row has 8 columns: week_starting, notable_outputs, blockers, klarna_test_status, kpi_movements, decisions_due, meeting_notes (filled during meeting), brain_link.*

Skim the row. Confirm with the founder if anything looks off. If a decision_due was added <24h ago, table it for next week.

---

### 13:30 — Open the pre-meeting Brain page

Open `firm/business-reviews/2026-04-17-pre.md` (the `-pre` suffix = pre-meeting state). R2 created it.

The page mirrors X3 + has post-meeting empty sections you'll fill during/after the meeting.

![Pre-meeting Brain page in Obsidian](../images/W4-3-pre-page.png)

*The pre-meeting page is the scribe's working canvas during the BR.*

---

## The meeting itself — minute by minute

### 14:00 — Open

> "BR for 2026-04-17. Mira facilitates; Davor scribes. 30 minutes. Outputs first."

**Stand up to start** if your firm meets in person. A small physical signal that the meeting is on.

### 14:00–14:10 — Outputs (10 min)

Read top 5 from X3 column B. Format your reading:

> "Top output this week: Davor's onboarding rebuild — S-tier, merged Tuesday, customer impact already visible in the new-signup metrics. Davor, anything to flag?"

Davor: brief response (10 seconds). Move on.

Continue through outputs 2-5. Sharp questions ONLY on outliers ("why is this S not M?" if the tier looks wrong; "what's the customer impact?" if the outcome is unclear). Most outputs need 30 seconds.

**Anti-pattern to suppress:** every partner narrating their week. That's the ledger's job.

### 14:10–14:15 — Blockers (5 min)

Read column C. Per blocker:
- Owner.
- ETA.
- What help is needed.

> "Anya — Acme legal review still pending. ETA 2026-04-22. Help needed?"

Anya: "No, I'm chasing. Status: open, monitoring."

> "Mira — Stripe deprecation. This rolls into the decisions block."

Move on.

**Anti-pattern:** solving the blocker in the meeting. If discussion runs >1 minute, it's a follow-up, not a BR item.

### 14:15–14:25 — Decisions (10 min)

Read column F. Work through each. **Scribe creates `firm/decisions/D-YYYY-NNN.md` during the discussion.**

> "D-2026-04-007 — Unit Fund pilot in Q3. Pre-read in Brain. Tali frames; partners discuss; decide."

Tali (60 seconds): "6 months of attribution data shows working pattern; YOLO model says wait 6-9 months; we're at 6. Risk: counsel returns 2026-05-30. Options: open Q3 anyway with caveat; defer until counsel; defer to Q4."

Senior partners discuss (3-4 minutes). Decision: defer until counsel. Davor (scribe) creates the Ledger page in real time:

```yaml
---
decision_id: D-2026-04-007
title: "Unit Fund pilot — defer Q3 decision until counsel sign-off"
accountable: founder-tali
consulted: [davor-krznar, anya-gorska, mira-tek, jana-kos, tomislav-novak]
status: accepted
reversal_threshold: "If counsel signs off before 2026-06-15, revisit at next BR for Q3 launch decision."
review_date: 2026-06-15
---
```

> "Decided. Next: D-2026-04-009 — Stripe → Adyen."

[Repeat for the second decision.]

**Anti-pattern:** one decision dominating. If a decision takes >5 minutes, it's a working session, not a BR item. Spawn it.

### 14:25–14:28 — Klarna status (3 min)

Read column D:
- KT-2026-014: proceeded; first 2-week NPS at 78 (threshold 60); 90-day review on calendar 2026-08-12.
- KT-2026-015: cohort-3 representation gap; pilot extended 2 weeks; scoring deferred.

**Standing item — never skip**, even if no open tests. The absence is information.

### 14:28–14:30 — KPI snapshot (2 min)

Read column E:
- Customer count: 84 → 87 (+3).
- Runway: 18.2 → 17.9 months.
- ai_skill_roi: 4.2 → 4.6 (rising 4 weeks running).

> "Material? AI ROI rising 4 weeks running — meaningful. Customer +3 is strong. Runway move is normal burn."

### 14:30 — Close

> "BR done. Decisions logged: 2. Blockers: 0 resolved, 1 still open (Anya, monitoring). Action items: Anya chase Acme by 2026-04-22; Mira draft ADR-2026-016 by 2026-04-24; Tali schedule counsel call by 2026-04-21. Brain summary in 30 min. Thanks all."

**Stand up. Close the meeting room. Leave on time.**

---

## Post-meeting (within 30 min of close)

### 14:30 — Scribe finalises Brain page

Open `firm/business-reviews/2026-04-17-pre.md`.

Append post-meeting content per [`templates/brain/business-review.md`](../../templates/brain/business-review.md):

```markdown
## Outputs discussion (10 min)

Davor's onboarding-rebuild S-tier output: reversal plan confirmed via ADR-2026-013.
Anya's Acme MSA: brief congrats; firm's largest customer to date.
Other three outputs acknowledged without question.

## Blockers (5 min)

- Anya / Acme legal review: ETA 2026-04-22; monitoring; no help needed.
- Mira / Stripe deprecation: rolled into D-2026-04-009.

## Decisions taken

- **D-2026-04-007** — Unit Fund pilot deferred until counsel sign-off (review 2026-06-15). → see [[decisions/D-2026-04-007]]
- **D-2026-04-009** — Stripe → Adyen, accept-in-principle pending ADR-2026-016. → see [[decisions/D-2026-04-009]]

## Klarna status (3 min)

- KT-2026-014: proceeded; first 2-week NPS 78; 90-day review on calendar 2026-08-12.
- KT-2026-015: cohort-3 representation gap; pilot extended 2 weeks.

## KPI discussion (2 min)

ai_skill_roi rising 4 weeks running (4.2 → 4.6); S3 pack earning compute cost.
Customer count +3 (Acme + 2 Tier-2 expansions).

## Action items

- Anya: chase Acme legal; report at next BR. Owner: anya-gorska. Deadline: 2026-04-22.
- Mira: author ADR-2026-016 (Stripe → Adyen). Owner: mira-tek. Deadline: 2026-04-24.
- Founder: schedule counsel call to expedite Unit Fund sign-off. Owner: founder-tali. Deadline: 2026-04-21.
```

### 14:50 — Rename + commit

Rename the Ledger page: drop `-pre` → `firm/business-reviews/2026-04-17.md`. Set frontmatter `status: active`.

Signed git commit:

```
phase-br: 2026-04-17 BR summary; 2 decisions logged; 1 Klarna closed, 1 in scoring
```

Push.

### 15:00 — Slack follow-up

Post to `#business-review`:

> 2026-04-17 BR done. 2 decisions, 0 blockers resolved (1 still open, monitoring), 0 new blockers. Summary at [[business-reviews/2026-04-17]].

---

## Common pitfalls

**1. Running long.**
- Cause: agenda overstuffed, or one decision dominating.
- Fix: stop the meeting. Run the §4.7 diagnostic at next week's BR.

**2. Scribe falls behind.**
- Cause: trying to capture verbatim instead of decisions.
- Fix: capture decisions only. Decisions get Brain pages; everything else gets summarised in the BR Brain page after.

**3. Founder dominating.**
- Cause: founder is most informed; partners defer.
- Fix: facilitator addresses directly. *"Tali, I'd like to hear from Anya on this."*

**4. Decisions made in chat post-meeting.**
- Cause: meeting ended; someone DMs "actually let's also do X".
- Fix: don't accept. Either bring it to next BR or open a working session. The BR is the canonical decision forum.

**5. Same facilitator week after week.**
- Cause: scheduling laziness.
- Fix: rotate. The meeting belongs to the partnership, not the founder.

---

## What's next

- **[W5 — Running a Klarna Test](W5-running-a-klarna-test.md)** — when the auto-labeller fires on a PR.
- **[W6 — Monitoring the Routines Dashboard](W6-monitoring-routines-dashboard.md)** — daily ops health check.
