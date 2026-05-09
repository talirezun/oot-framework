# Example 1 — A typical Friday Business Review, end-to-end

A walkthrough of the full BR cycle for a real-feeling 8-partner firm: agenda generation → meeting → summary commit.

## The firm

8 partners (5 full-time + 3 specialists). Cloud track. Founder is Tali; this week's facilitator is Mira (rotating); this week's scribe is Davor.

## Friday 08:00 — R2 fires

The Routine wakes. Reads `firm/output-logs/2026-04-13.md` through `2026-04-17.md`. Aggregates.

X3 Weekly_Review row populated:

```
week_starting: 2026-04-13
notable_outputs: |
  - [[partners/davor-krznar]] — pr_merged — gh:1487 — value tier `S` — €8,000 envelope — onboarding-flow rebuild [[partners/davor-krznar/output-specs/2026-03-22--onboarding-rebuild]]
  - [[partners/anya-gorska]] — contract_signed — Acme — value tier `S` — €8,000 — 3-year ARR [[partners/anya-gorska/output-specs/2026-04-08--acme-msa]]
  - [[partners/mira-tek]] — pr_merged — gh:1495 — value tier `M` — €2,000 — payment-rail integration [[partners/mira-tek/output-specs/2026-04-10--payment-rail]]
  - [[partners/jana-kos]] — design_shipped — invoice-flow-redesign — value tier `M` — €2,000 [[partners/jana-kos/output-specs/2026-04-05--invoice-redesign]]
  - [[partners/tomislav-novak]] — review_completed — gh:1502 — value tier `M` — €2,000 — Klarna test KT-2026-014 review

blockers: |
  - 2026-04-15 — [[partners/anya-gorska]] — waiting on Acme legal review of the long-tail clause
  - 2026-04-16 — [[partners/mira-tek]] — Stripe connector deprecated; need ETA on replacement

klarna_test_status: |
  - KT-2026-014 — proceeded this week (score 16/20). 90-day review on calendar 2026-08-12.
  - KT-2026-015 — opened 2026-04-16; in scoring; affected partner: Tomislav.

kpi_movements: |
  - Customer count: 84 → 87 (+3, all from Acme MSA + 2 Tier-2 expansions)
  - Treasury runway: 18.2 → 17.9 months (consistent with month's burn)
  - ai_skill_roi: 4.2x → 4.6x (S3-driven; up week-on-week 4 weeks running)
  - partner_count: 8 (no change)
  - agent_human_ratio: 1.4 → 1.5 (Code & QA pack adoption rising)

decisions_due: |
  - D-2026-04-pending-007 — Should we open the Unit Fund pilot in Q3? Founder + senior partners. Decision overdue 1 week.
  - D-2026-04-pending-009 — Renew or replace Stripe connector? Mira draft, Tali decide.
```

R2 posts to Slack `#business-review`:

> **BR agenda for 2026-04-17 14:00.** Highlights: Davor's S-tier onboarding rebuild merged; Anya signed the Acme MSA (S-tier, 3-year ARR); Mira's payment-rail PR merged. Klarna in flight: 1 (KT-2026-015). Decisions due: 2 (Unit Fund pilot, Stripe replacement). Pre-read X3 Weekly_Review row at [[business-reviews/2026-04-17-pre]].

## Friday 14:00 — the meeting

Mira opens. Davor has the Brain page open for live editing.

### Outputs (10 min)

Mira reads top 5 from X3 col B aloud. Tali asks Davor (10s of context) about onboarding-rebuild's reversal plan; Davor: "ADR-2026-013 has it; standby Anya for high-tier customers; tested in pilot."  Anya gets a brief congrats on Acme MSA. The remaining three outputs — quick acknowledgement, no questions. **9 minutes used.**

### Blockers (5 min)

- Anya's Acme legal review: ETA 2026-04-22; Anya already chasing; **no help needed.** Status: open, monitoring.
- Mira's Stripe deprecation: this is the same issue as decision-due #2; **deferred to decisions block.**

**3 minutes used.**

### Decisions (10 min)

**D-2026-04-pending-007 — Unit Fund pilot in Q3?**

Tali frames: 6 months of Gen 1 attribution data shows a working pattern; YOLO model says wait 6–9 months before Unit Fund — we're at 6. Risk: legal scoping not complete; counsel returns 2026-05-30. Senior partners: cautiously in favour but want counsel's written sign-off first.

Davor (scribe) creates `firm/decisions/D-2026-04-007.md`:

```yaml
---
decision_id: D-2026-04-007
title: "Unit Fund pilot — defer Q3 decision until counsel sign-off"
accountable: founder-tali
consulted: [davor-krznar, anya-gorska, mira-tek, jana-kos, tomislav-novak]
status: accepted
reversal_threshold: "If counsel signs off before 2026-06-15, revisit at next BR for Q3 launch decision. If counsel cannot complete by 2026-07-30, push to Q4."
review_date: 2026-06-15
---
```

**Decision: accepted.**

**D-2026-04-pending-009 — Stripe connector?**

Mira's draft: replace with Adyen. Cost neutral; better SCA compliance for EU customers. Migration risk: 4-6 weeks of dual-running.

Tali: agreed in principle; needs ADR. Mira to author. **Decision: accept-in-principle; pending ADR-2026-016.**

Davor creates `firm/decisions/D-2026-04-009.md` with `status: accept-in-principle` and pending-ADR linkage.

**8 minutes used.**

### Klarna status (3 min)

Tali: KT-2026-014 proceeded; 90-day review on calendar; reversal threshold (NPS <60) being monitored; first 2-week post-deployment NPS holding at 78.

KT-2026-015: just opened. Tomislav (affected partner — code review automation) is concerned about the cohort-3 cases not being represented in the pilot. Founder agrees to extend pilot by 2 weeks specifically for cohort-3. Scoring deferred until extension completes.

**3 minutes used.**

### KPI snapshot (2 min)

Tali notes the ai_skill_roi rising 4 weeks running. Comments: "the S3 pack is genuinely earning its compute cost. Good signal." Customer count +3 is a strong week. **2 minutes used.**

**Total: 25 minutes.** Meeting closes.

## 14:30 — Scribe finalises

Davor opens `firm/business-reviews/2026-04-17-pre.md`. Renames to `2026-04-17.md` (drops `-pre`). Sets `status: active`.

Appends post-meeting content per `templates/brain/business-review.md`:

```markdown
## Outputs discussion (10 min)

Davor's onboarding-rebuild S-tier output: reversal plan confirmed via ADR-2026-013. Anya's Acme MSA: brief congrats; Acme is the firm's largest customer to date. Other three outputs acknowledged without question.

## Blockers (5 min)

- Anya / Acme legal review: ETA 2026-04-22; monitoring; no help needed.
- Mira / Stripe deprecation: rolled into decisions block (D-2026-04-009).

## Decisions taken

- **D-2026-04-007** — Unit Fund pilot deferred until counsel sign-off (review 2026-06-15). → see [[decisions/D-2026-04-007]]
- **D-2026-04-009** — Stripe → Adyen, accept-in-principle pending ADR-2026-016 (Mira authoring). → see [[decisions/D-2026-04-009]]

## Klarna status (3 min)

- KT-2026-014: proceeded; first 2-week NPS at 78 (threshold 60); 90-day review on calendar 2026-08-12.
- KT-2026-015: cohort-3 representation gap; pilot extended 2 weeks; scoring deferred.

## KPI discussion (2 min)

ai_skill_roi rising 4 weeks running (4.2 → 4.6); S3 pack earning its compute cost. Customer count +3 (Acme + 2 Tier-2 expansions).

## Action items

- Anya: chase Acme legal; report at next BR. Owner: anya-gorska. Deadline: 2026-04-22.
- Mira: author ADR-2026-016 (Stripe → Adyen). Owner: mira-tek. Deadline: 2026-04-24.
- Founder: schedule counsel call to expedite Unit Fund sign-off. Owner: founder-tali. Deadline: 2026-04-21.
```

Signed git commit: `phase-br: 2026-04-17 BR summary; 2 decisions logged; 1 Klarna closed, 1 in scoring`.

Pushes. Posts to `#business-review`:

> 2026-04-17 BR done. 2 decisions, 0 blockers resolved (1 still open, monitoring), 0 new blockers. Summary at [[business-reviews/2026-04-17]].

## What this example demonstrates

- **R2's agenda generation** is concrete (real wikilinks, real numbers, real KPI movements).
- **The 30-minute structure holds** (25 min total; 5 min buffer typical).
- **Decisions get Brain pages during the meeting** — Davor was creating `D-2026-04-007.md` while Tali was still talking. The scribe is the most important role.
- **The Klarna status block surfaces real things** (a 90-day review on calendar; an in-flight test extending its pilot).
- **Action items have owners + deadlines** (the BR's only acceptable form of "homework").
- **The Brain commit is a single signed commit** — auditable, immutable, time-stamped.
