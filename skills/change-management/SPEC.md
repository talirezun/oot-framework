# Skill Pack S6 — Change Management / Resistance: SPEC

**ID:** S6
**Name:** Change Management / Resistance
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

The framework's response to the **central problem** (`MANIFESTO.md` Thesis 1: *resistance is the bottleneck on AI value capture, not model quality*). Encodes Kotter's eight-step framework, the ADKAR model, the **METR perception-gap baseline discipline**, the AI Champion criteria, and the 6–8 week pilot template. Mandatory before any major Skill Pack rollout.

This pack is what stops an ØØT firm from joining the 95% of MIT NANDA's pilots that produce no measurable P&L impact. The discipline is non-negotiable because the failure mode is invisible without it.

---

## Scope

**Covers:**
- **METR baseline procedure** (DORA + SPACE + DX Core 4 metrics captured before AI rollout).
- 6–8 week pilot template (15–20% of team, structured cohort).
- AI Champion designation criteria (**earned, not appointed**).
- Resistance-pattern recognition (shadow refusal, perception gap, sceptic alignment).
- Communication patterns for AI rollout announcements.
- The 12–24 month resistance plateau plan.
- **Klarna Test pre-rollout integration** — every major rollout is a Klarna trigger.
- The "AI Champion misfire" diagnostic — what to do when an appointed champion fails to gain organic uptake.

**Does NOT cover:**
- The Klarna Test itself (`governance/KLARNA-TEST.md`).
- Domain-specific rollout patterns (those live in the relevant Skill Pack).
- HR / employment law dimensions of change management (counsel territory).
- Specific tool training (that's the tool's own documentation, not the framework's).

---

## Allowed tools / dependencies

- **Curator MCP** — read pilot history, write pilot summaries, AI Champion designations, resistance observations.
- **Excel MCP / Google Sheets** — write to X5 (METR baseline).
- **Slack MCP / 4thtech** — rollout communication.
- **The Klarna Test interaction** (R7 trigger via S3 integration).
- **DORA / SPACE / DX Core 4 measurement tooling** — the firm chooses (LinearB, Jellyfish, in-house scripts); the pack is tool-neutral.

---

## When to invoke

1. **Before any Skill Pack rollout** affecting >25% of partners — the METR baseline is mandatory.
2. **When designing a 6-8 week pilot** for a new tool / Skill / workflow.
3. **When recognising an AI Champion** — the pack provides the criteria; recognition is an event, not an appointment.
4. **When resistance patterns are observed** — shadow refusal (licensed but unused), perception gap (claims of speedup not matched in measurement), sceptic alignment (partners forming an explicit opposition).
5. **At the Klarna Test pre-rollout step** — the pack provides the change-management side of the rubric.
6. **At the 90-day post-deployment review** of any Klarna-Test-passed decision — re-run baseline; check perception gap evolution.
7. **When the 12-24 month plateau hits** (months 6-12 typically) — partners are tired; uptake plateaus; the pack provides the persistence playbook.

---

## When NOT to invoke

1. **For tool changes that don't affect partner workflows** (e.g., a backend infrastructure swap with no surface change).
2. **For a one-off experiment** (a single partner trying a new tool for a week without firm-level rollout intent).
3. **After-the-fact** — if the rollout already happened without baseline, the pack flags this as a discipline failure rather than retroactively pretending; it does **not** reconstruct a baseline from memory.

---

## Operational instructions

### 4.1 METR baseline procedure

Mandatory before any major Skill Pack rollout. The procedure:

1. **Identify the metrics** appropriate to the rollout. The canonical set:
   - **DORA**: deployment_frequency, lead_time_for_changes, change_failure_rate, time_to_restore_service.
   - **SPACE**: satisfaction_score (survey), performance_metric (domain-specific), activity_count, communication_quality, efficiency_index.
   - **DX Core 4**: deep_work_hours, cycle_time, dx_score, ai_assist_uptake.
2. **Choose the measurement window**: 90 days is the framework's recommended baseline length. Shorter windows risk seasonality contamination.
3. **Pre-populate X5 Baseline_Metrics** with the chosen metrics, the data source, the owner, the capture cadence.
4. **Run the measurement** for the full 90 days **before any pilot starts**. The framework's authors find that ~30% of organisations skip this; ~30% try to compress to 30 days; the remaining ~40% who run the full 90 days are also the ~40% who detect the perception gap accurately at month 3.
5. **Lock the baseline** at day 90. The locked baseline is the comparator for every subsequent measurement. The pack records the lock as a decision (`firm/decisions/D-YYYY-NNN.md`) and writes the locked values into X5.
6. **Continue parallel measurement during the pilot**. The pack's weekly update populates X5 Self_Report_vs_Actual sheet — partner self-report (collected via a 1-question survey) vs. the measured DORA/SPACE/DX delta.
7. **Compute the perception gap** weekly. The X5 formula `=IF(ABS(self_report - measured) > 20, "PERCEPTION_GAP", "OK")` flags gaps >20 points (≈ half the 39-point swing METR found in 2025). Tighten to 15 once the firm has 90 days of internal baseline data.
8. **Surface gaps at the BR**. Every flagged perception gap becomes a Klarna-status-block agenda item.

### 4.2 Pilot cohort selection (15–20%, criteria for inclusion, cohort composition)

The pilot cohort is **15-20% of the affected partner population**. Criteria:

- **Inclusion criteria** (all four required):
  1. The partner volunteers (no draft selection — pilots run on consent).
  2. The partner has a baseline measurement (per §4.1).
  3. The partner's output mix in the rollout's domain is sufficient for meaningful measurement (not zero outputs in 90 days).
  4. The partner's reward species declaration is compatible with the pilot's incentive structure (e.g. don't pilot a productivity tool with a partner whose reward species is pure-lockstep — the incentives don't align).

- **Cohort composition** (target):
  - **Participants** (the pilot users): 70%.
  - **Control** (continues current workflow without the new tool): 20% — provides the counterfactual.
  - **Champion-candidates** (high-output, AI-curious, willing to mentor): 10%.

- **Cohort selection process**:
  1. Founder + S6-running partner draft a candidate list from the firm roster.
  2. Each candidate gets a 15-minute conversation: "we're piloting X; would you want in?" (no pressure; consent first).
  3. Volunteers are matched to roles per the composition target.
  4. Cohort recorded in X5 Pilot_Cohort sheet.

### 4.3 Pilot execution (6–8 weeks, weekly check-ins, success criteria)

The 6-8 week structure:

- **Week 0** (pre-pilot): cohort selection complete; baseline locked; partners briefed; tooling provisioned.
- **Week 1**: tool/Skill in use. Daily friction notes captured by partners in their `firm/partners/<id>/private/pilot-notes.md` (private — the partner controls visibility).
- **Weekly check-ins** (each Wednesday, 30 min): facilitated by the S6-running partner. Format: each cohort partner shares one win + one friction. Friction items are tagged in the Brain.
- **Week 4 mid-point review**: cohort + founder. Measured DORA/SPACE/DX delta vs. baseline. Perception gap check. Decision: continue / iterate / abandon.
- **Weeks 5-7**: continued pilot with iterations from the mid-point review.
- **Week 8 close**: final measurement; close-out report at `firm/change/pilots/<pilot_id>.md` per `templates/brain/pilot-summary.md`.

**Success criteria** (the pack's recommended decision rule at week 8):

- **Proceed to full rollout** if: measured delta is positive, perception gap is <20 points, ≥80% of cohort partners would recommend, no Klarna Test obstruction.
- **Iterate** if: measured delta is positive but perception gap is large; or one of the three criteria above is missed but recoverable.
- **Abandon** if: measured delta is zero or negative after 8 weeks; or cohort recommendation rate is <50%.

### 4.4 Post-pilot decision (proceed / iterate / abandon — with Klarna Test if proceed)

If proceeding to full rollout:

1. **The full rollout is a Klarna Test trigger** even if the pilot passed. The framework's authors find this surprising to many founders; the rationale is that pilot-to-full-rollout often involves capacity that *could* displace partners (the same Skill, applied to 100% of the team, may make some roles redundant in a way the pilot did not).
2. The pack invokes R7 with the rollout decision summary; the test is scored per `governance/KLARNA-TEST.md`.
3. Only on `proceed` (≥14/20) does the rollout commence.
4. The 90-day post-rollout review (Q9 of the rubric) is scheduled with the founder as owner.

If iterating: a fresh pilot cycle starts, with the iteration scope explicitly recorded.

If abandoning: the pack writes a "lessons learned" Brain page; the partners involved are thanked and unwound.

### 4.5 AI Champion designation (criteria, what they do, how they're not appointed)

Per the manifesto's discipline: **AI Champions are recognised, not appointed.** The criteria for recognition:

1. **Demonstrably increased throughput** — measured. The partner's `total_outputs` × `value_envelope` (from X1) has increased ≥30% in the 90 days following AI tool adoption, vs. the prior 90-day baseline.
2. **Demonstrably maintained or increased quality** — `rework_within_30d` rate has not increased; ideally decreased.
3. **Mentorship signals** — the partner has voluntarily helped ≥3 other partners with AI tooling questions (visible in Slack/dChat helps thread, in commit `Co-authored-by:` patterns, or in pair-programming records).
4. **AI-curious cultural posture** — visible by their Brain contributions (prompts in `firm/prompts/`, ADRs in `firm/architecture/` involving AI tooling decisions).

A partner meeting all four criteria is **recognised** at the next BR with a Brain page at `firm/change/ai-champions/<partner_id>.md`. The recognition includes:

- The data (the measurements that triggered recognition).
- A small variable-pay multiplier bump (the framework recommends +0.1 on `output_multiplier` for the next 6 months — small but real).
- The explicit mentorship role (the AI Champion is the firm's go-to for tooling questions; the role is part-time, not full-time).

The role is **revoked** if the criteria stop holding (the framework's authors call this "honest revocation" — letting an AI Champion role linger past its merit is the failure mode).

**The Tecknoworks/Caplaz failure mode**: appointing an AI Champion before the criteria are met. The pack's discipline: **never appoint**. If the firm has no partner meeting the criteria, the firm has no AI Champion. This is a finding, not a problem to paper over.

### 4.6 Resistance pattern recognition (shadow refusal, perception gap, sceptic alignment)

Three patterns the pack monitors, with concrete signals and responses:

**Shadow refusal** (the licensed-but-unused pattern):

- **Signal**: tool is provisioned (Bitwarden seat, license active), but the partner's actual usage (measurable via the tool's own analytics) is <10% of the team's median.
- **Cause** (typical): the partner doesn't trust the tool; or they tried it once and it failed; or they're philosophically opposed.
- **Response**: a 1-1 conversation with the partner. **Not** an escalation. The framework's discipline: shadow refusal is information, not insubordination. The partner may be right.

**Perception gap** (the METR-style swing):

- **Signal**: weekly self-report claims +15-25% productivity; measured DORA/SPACE/DX delta is flat or negative.
- **Cause**: well-documented (METR 2025); structural feature of human self-assessment under AI assistance.
- **Response**: surface gently in the next BR. **Don't** confront the partner. **Do** show the data side-by-side. Most partners adjust their self-assessment within 2-3 cycles.

**Sceptic alignment** (the partnership-against-tool pattern):

- **Signal**: ≥3 partners are independently flagging the same friction; the friction has not been addressed in the iteration cycle.
- **Cause**: real friction; the rollout has a flaw the early pilot didn't surface.
- **Response**: pause the rollout. Convene the sceptics. The framework's discipline: when ≥3 partners independently flag the same issue, the issue is real. Treat it as a Tier-2 escalation (per DECISION-RIGHTS.md if compensation-affecting; per a working session otherwise).

### 4.7 Rollout communication (the partnership-wide announcement pattern)

When proceeding to full rollout (post-Klarna):

1. **Founder announcement** in the next BR (verbal) + a Brain page at `firm/change/rollouts/<rollout_id>.md` (written).
2. **Honest framing**:
   - What the pilot found (measured delta, perception gap, cohort feedback).
   - What the Klarna Test scored and any conditions imposed.
   - The reversal threshold (per Klarna Q3): if the pilot pattern degrades beyond X, we revert.
   - The 90-day review date and owner (per Klarna Q9).
3. **No marketing language**. No "exciting transformation" / "synergy" / "leverage". The framework's discipline: rollouts are operational decisions, not motivational events.
4. **Q&A window** (1 week): partners can raise concerns asynchronously in `#change` channel; concerns are addressed in the next BR.

### 4.8 12–24 month plateau planning (persistence as the key correlate of success)

MIT NANDA's finding: most failed pilots failed because the team quit after pilot disappointment, not because the technology didn't work. The pack's discipline:

- **Pre-commit a 18-month operational horizon** for any major rollout. The Klarna Test's Q10 (founder defends in 2 years) is the long-horizon check.
- **Plan for a plateau** at months 6-12. Uptake stalls; novelty wears off; the partners who were going to adopt have adopted; the partners who weren't going to adopt are visible.
- **Plateau response** is **not** "double down on the rollout". It's "iterate the workflow around the partners who didn't adopt". Sometimes the right answer is the partners are right; the workflow is wrong; the rollout was the wrong scope.
- **Schedule a plateau review** at month 12 (calendar invite at rollout start). Plateau review pre-read: full DORA/SPACE/DX trajectory, AI Champion register, Klarna Test 90-day reviews, sceptic-alignment incidents.
- **Plateau decisions**: continue / refocus / partial-rollback / full-rollback. Each is a `firm/decisions/` page.

---

## Brain interaction protocol

**Reads:**
- `firm/output-logs/*` — for AI Champion eligibility computation.
- `firm/partners/<id>/profile.md` — for cohort eligibility checks.
- `firm/klarna-tests/*` — for cross-referencing pilot outcomes against tests.

**Writes:**
- `firm/change/pilots/<pilot_id>.md` — per pilot.
- `firm/change/ai-champions/<partner_id>.md` — per recognition.
- `firm/change/rollouts/<rollout_id>.md` — per full rollout.
- `firm/change/plateau-plans/YYYY-MM.md` — at plateau reviews.
- `firm/change/resistance-observations/YYYY-MM-DD-<pattern>.md` — when patterns are surfaced.

---

## Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X5 metr-baseline.xlsx | Baseline_Metrics | Write | Pre-rollout |
| X5 | Self_Report_vs_Actual | Append weekly | Weekly during pilot |
| X5 | Pilot_Cohort | Write at cohort selection | Per pilot |
| X5 | Adoption_Curve | Append weekly | Weekly during pilot |

---

## Routine integration

- The pack invokes **R7** (Klarna Test) at decision points (post-pilot proceed, post-90-day-review reversal-or-continue).
- The pack contributes to **R2** (Weekly BR Prep) via the change-status block.

---

## Don'ts

1. **Don't roll out without a METR baseline.** Mandatory — no exceptions. The 90-day measurement is the framework's most expensive discipline-cost; it pays itself back at the perception-gap detection.
2. **Don't appoint an AI Champion.** They are recognised, not named. The Tecknoworks/Caplaz pattern is the failure mode.
3. **Don't ignore shadow refusal.** If the tool is licensed but unused, the rollout is failing — investigate; do not escalate.
4. **Don't extend a failing pilot past 8 weeks.** Stop and re-design. Continuing a failed pilot is the framework's "throw good money after bad" pattern.
5. **Don't measure post-rollout against post-rollout perception.** Always vs. baseline. The whole point of the baseline is to be the immutable comparator.
6. **Don't confront a perception gap directly.** Surface the data; let the partner adjust. Confrontation creates resistance, not learning.
7. **Don't proceed to full rollout without a Klarna Test on the rollout itself**, even if the pilot was clean. The pilot's Klarna Test does not cover the full rollout's Klarna Test.
8. **Don't run a rollout without a 90-day review on the calendar.** The review is part of the test (Klarna Q9); without it, the test was incomplete.
9. **Don't assume a plateau means failure.** Plateaus are predictable; the response is iteration, not despair.

---

## Quick reference

| Situation | Action | Output |
|---|---|---|
| Planning a Skill rollout | Run §4.1 baseline 90 days first | X5 Baseline_Metrics locked |
| Pilot starting | §4.2 cohort + §4.3 8-week structure | X5 Pilot_Cohort + weekly check-in notes |
| Pilot mid-point | Week-4 review; decide continue/iterate/abandon | Pilot summary update |
| Pilot close | §4.4 final decision; if proceed → R7 fires | Pilot summary; Klarna Test entry |
| AI Champion criteria met | §4.5 recognition with data | `firm/change/ai-champions/<id>.md` + multiplier bump |
| Shadow refusal observed | §4.6 1-1 conversation, no escalation | Resistance observation Brain page |
| Perception gap flagged | §4.6 surface in BR with side-by-side data | BR notes + X5 row |
| Sceptic alignment | Pause rollout; convene sceptics | Tier-2 escalation Brain page |
| 12-month plateau review | §4.8 review with full trajectory | Plateau decision Brain page |

---

## Worked examples concept

**3 worked examples in `examples/`:**

1. **A Code & QA pack rollout that worked.** 18-partner firm. 90-day DORA baseline captured. 4-partner pilot ran for 8 weeks. Mid-point review caught a perception gap (one partner reporting +25%, DORA +5%); confronted with data; partner adjusted self-assessment. Full rollout passed Klarna Test with score 17. 90-day review showed sustained +12% DORA delta. AI Champion recognised at month 4. The example shows X5 evolution week by week.

2. **A pilot that was abandoned at week 8.** Same firm; rollout of an AI marketing tool. Pilot showed flat DORA delta and 2 of 3 cohort partners would not recommend. The pack walks through the close-out: lessons-learned Brain page, partners thanked, the tool's features that were valuable were carved off into a smaller-scope rollout (which the pack frames as iteration, not failure).

3. **A perception-gap incident handled well.** A senior partner self-reported +30% productivity from Code & QA tools at the 6-week pilot mid-point. Measured delta: -5% (slightly slower). The pack's response: data side-by-side at the BR; founder framed neutrally ("the data says X; let's understand together"); partner adjusted their workflow and the gap closed at week 12. The example shows the actual conversation transcripts (anonymised) and the recovery curve.

---

## References

1. **Kotter, J. P.** *Leading Change* (HBS Press, 1996, updated editions).
2. **Hiatt, J.** *ADKAR: A Model for Change in Business, Government, and our Community* (Prosci, 2006).
3. **METR.** *RCT on AI tools and developer productivity* (July 2025) and February 2026 follow-up. The perception-gap study.
4. **MIT NANDA.** *The GenAI Divide* (August 2025). The 95% pilot-failure finding and its causes.
5. **Microsoft.** *Work Trend Index 2025: The Frontier Firm*. The plateau and human-agent-ratio framing.
6. **Forsgren, N. et al.** *Accelerate* + *DORA Report 2025*. The DORA metrics.
7. **Tecknoworks / Caplaz.** *AI Champion case studies* (2024–2025). The "appointed champion fails" pattern.
8. **Dell'Acqua et al.** *The Cybernetic Teammate* (HBS WP 25-043, 2025). The pilot-cohort composition framing.
9. ØØT `MANIFESTO.md`, Thesis 1.
10. ØØT `governance/KLARNA-TEST.md`.

---

## Acceptance criteria

Standard. Plus:
- The METR baseline procedure (§4.1) is reproduced step-by-step with a concrete example metric set.
- The AI Champion criteria (§4.5) are explicit and operational (the four criteria, the recognition Brain page template, the small variable-pay multiplier bump).
- The pilot cohort composition (§4.2) is shown with a worked example — actual cohort selection from a 12-partner firm.
- The plateau plan (§4.8) is shown as a calendar artefact with the 12-month review pre-read enumerated.
- 3+ worked examples in `examples/`.
- Frontmatter passes the Phase 8 linter.
