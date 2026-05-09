# Example 1 — A Code & QA pack rollout that worked

A worked example of the full pre-rollout discipline: 90-day baseline → 8-week pilot → mid-point perception-gap detection → Klarna pass → full rollout → 90-day review. The framework's textbook win condition.

## The setup

- **Firm:** 18-partner SaaS development studio.
- **Rollout:** S4 Code & QA pack firm-wide, including Claude Code Max licences for all 14 engineering partners.
- **Goal:** improve deployment frequency and reduce code-review cycle time.

## Phase 1 — 90-day baseline (2025-12-01 → 2026-02-28)

Pack runs §4.1. The S6-running partner (Tomislav) sets up X5:

**Baseline_Metrics** populated with:

| metric | source | baseline_value | capture_period_days | owner |
|---|---|---|---|---|
| deployment_frequency | GitHub API + Linear | 2.4/week (avg per engineer) | 90 | Tomislav |
| lead_time_for_changes | GitHub PR data | 3.7 days (PR open → merge) | 90 | Tomislav |
| change_failure_rate | Sentry + post-merge revert tags | 11% | 90 | Tomislav |
| time_to_restore_service | Incident tracker | 4.1 hours (median) | 90 | Tomislav |
| dx_score | Quarterly survey | 6.8 / 10 | 90 | Tomislav |
| ai_assist_uptake | Self-report % weekly | 18% (of commits AI-assisted) | 90 | Tomislav |

Day 90 (2026-02-28): baseline locked. Decision record `D-2026-02-019.md` filed: *"Baseline locked; pilot greenlit for Q2 2026."*

## Phase 2 — 4-partner pilot (2026-03-01 → 2026-04-26, 8 weeks)

Pack runs §4.2-§4.3.

**Cohort selection** (18 engineering partners; target 15-20% = 3-4):
- 3 participants: Davor (vibe-coder cohort, sceptical), Mira (agentic-engineer, enthusiastic), Jana (transitional, curious).
- 1 control: Tomislav himself (continues without Claude Code; per-partner agreement).

All four volunteered. All four had 90-day baselines. All four's reward species accommodated experimentation (none lockstep).

**Week 1-3:** participants in normal use. Friction notes captured in private Brain pages. Weekly check-ins (Wed 30-min):
- Week 1: Davor friction = "the model keeps suggesting refactors I disagree with"; Mira friction = "Plan Mode workflow takes longer than I thought initially"; Jana friction = "I'm afraid to commit AI-generated code". Wins: small-PR turnaround dropped, Mira reports.
- Week 2-3: friction normalising; Davor still sceptical; Jana experimenting.

**Week 4 mid-point review.** Cohort + founder.

DORA delta vs. baseline (4 weeks of pilot data):
- deployment_frequency: 2.4 → 2.7 (+12%)
- lead_time_for_changes: 3.7 → 3.4 days (-8%)
- change_failure_rate: 11% → 12% (slight uptick — within noise)
- ai_assist_uptake: pilot cohort 18% → 41%

Self-report (X5 Self_Report_vs_Actual):
- Davor: self-report -5% productivity (he genuinely felt slower); measured +5%. Gap: -10 points (within tolerance).
- Mira: self-report +30%; measured +12%. **Gap: +18 points — within the 20-point threshold but worth watching.**
- Jana: self-report +10%; measured +8%. Gap: +2 points (no concern).

**Decision: continue.** Mira's gap surfaces but is below threshold; Tomislav adds an explicit re-measurement at week 6 to track.

**Week 6 re-measurement of Mira's gap:**
- Self-report: +35%; measured: +14%. **Gap: +21 points — flagged.**

Tomislav surfaces at the BR (per §4.6). Mira reads the data; her response: *"I really felt 35%. I'll trust the measurement and re-baseline how I'm feeling."* No confrontation. By week 8, Mira's self-report has converged to +18% with measured at +15% (gap: +3).

This is the textbook perception-gap detection-and-recovery.

**Week 8 close (2026-04-26).** Final measurement:
- deployment_frequency: 2.4 → 2.9 (+21%)
- lead_time_for_changes: 3.7 → 3.1 days (-16%)
- change_failure_rate: 11% → 10% (slight improvement after week-4 tooling iteration)
- dx_score: 6.8 → 7.4
- ai_assist_uptake: pilot cohort 18% → 53%

Cohort recommendation rate: 4/4 would proceed to full rollout (yes, even Davor — he's still personally sceptical but the data is the data).

**Pilot summary** at `firm/change/pilots/code-qa-2026-q1.md` per `templates/brain/pilot-summary.md`. Decision: **proceed to full rollout** (with Klarna Test).

## Phase 3 — Full rollout's Klarna Test (2026-04-29)

Per §4.4, the rollout itself triggers R7 even though the pilot passed. The reasoning: full rollout to 14 engineers might displace the 3 senior reviewers who currently do most code review.

R7 fires. Affected partners (from S3): the 3 senior reviewers (Tali, Anya, Tomislav). Non-beneficiary reviewer: Marin (a project specialist outside engineering whose comp is independent of code-review volume).

Klarna Test scoring (§4.7 of `governance/KLARNA-TEST.md`):

| Q | Score | Evidence |
|---|---|---|
| 1 | 2 | 90-day baseline + 8-week pilot data on actual production traffic. |
| 2 | 2 | DORA + dx_score + ai_assist_uptake all still measured post-rollout. |
| 3 | 2 | Reversal threshold: "if change_failure_rate exceeds 15% for 2 weeks, OR if any of the 3 senior reviewers reports they are no longer doing meaningful review (vs. just rubber-stamping AI), revert." |
| 4 | 2 | Reversal plan operational: senior reviewers retain their role for "human override" cases; if reverted, full code-review responsibility returns to them. No standby contracts needed (they remain employed full-time partners). |
| 5 | 2 | All 3 senior reviewers consulted in writing; written record at `firm/klarna-tests/KT-2026-022/senior-reviewer-consultation.md`. |
| 6 | 2 | METR baseline locked 90 days; pilot data is supplementary. |
| 7 | 2 | Marin reviewed; signed off as non-beneficiary. |
| 8 | 2 | Public communication: no proactive comms (this is internal tooling); if asked, "we're using AI assistance to make our engineers more effective; senior review remains for high-impact changes". Posture written by Tali; reviewed by senior partners. |
| 9 | 2 | 90-day post-rollout review on calendar 2026-07-29; owner Tomislav; pre-committed framework. |
| 10 | 2 | Founder confirmed in writing. |

**Total: 20/20.** Decision: **PROCEED.**

This is the rare 20/20 — the pilot was thorough enough that every question was easily defensible. Most Klarna tests score 14-17; 20 means the pre-work was exemplary.

## Phase 4 — Full rollout (2026-04-29)

Per §4.7 communication discipline, Tali announces in the BR + Brain page:

> Code & QA pack rolls out firm-wide effective today. Pilot showed +21% deployment frequency, -16% lead time, no quality regression. Klarna Test scored 20/20; reversal threshold set; 90-day review on 2026-07-29.
> Senior reviewers (Tali, Anya, Tomislav) retain their role for high-impact changes; the AI does not replace human review for production-critical paths.
> No marketing language. This is an operational decision based on measured data.

## Phase 5 — Month 4 (2026-08-29): AI Champion recognition

Per §4.5, the pack monitors X1 for the four criteria. By month 4 of full rollout (mid-August):

**Tomislav** (the S6-running partner, ironically, who was the *control* in the pilot):
1. Throughput +43% over 90 days vs. pre-rollout baseline. ✓
2. Rework rate dropped 13% → 9%. ✓
3. Mentorship: helped 7 partners with Plan Mode questions in `#code-qa-help`. ✓
4. Cultural posture: authored 2 ADRs about AI tooling decisions. ✓

All four criteria met. Recognition at the next BR. Brain page at `firm/change/ai-champions/tomislav-novak.md`. Variable-pay multiplier bumped from 1.0 to 1.1 for 6 months. Mentorship role: "go-to for Plan Mode questions; available for pair-programming; revoked if criteria stop holding."

## Phase 6 — 90-day review (2026-07-29)

DORA: deployment_frequency 2.4 → 3.1 (+29% vs. baseline; sustained); lead_time -22%; change_failure_rate 11% → 9% (improvement). dx_score 6.8 → 7.7. ai_assist_uptake firm-wide 18% → 47%.

Senior reviewers: all 3 confirm in writing they are still doing meaningful review (not rubber-stamping). Anecdote from Tali: *"I'm reviewing fewer PRs but the ones I review are more substantive — the routine stuff goes through faster, the hard stuff still hits my desk."*

**Decision: continue.** No reversal triggered. Next review at month 12 (plateau review).

## What this example demonstrates

- **The 90-day baseline is real work** but pays for itself by detecting Mira's perception gap accurately.
- **The 4-partner pilot is honest** — Davor remained sceptical; the data still won.
- **Mid-point check caught the perception gap** *before* full rollout.
- **The full rollout's Klarna Test is separate from the pilot's** — the pilot doesn't exempt the rollout. Full Klarna at 20/20 was earned by the pre-work.
- **AI Champion was recognised, not appointed** — Tomislav was the control in the pilot, became the highest-uptake partner, met all four criteria.
- **The 90-day review is real, not theatre** — measured DORA improvements held; senior reviewers confirmed they retained meaningful work.
- **Honest communication** — no marketing language; operational decision based on data.
