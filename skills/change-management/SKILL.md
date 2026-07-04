---
name: change-management
description: Use whenever the firm is planning a Skill Pack rollout, designing a 6-8 week pilot, recognising an AI Champion, observing resistance patterns (shadow refusal, perception gap, sceptic alignment), running a 12-month plateau review, or contributing the change-management side of a Klarna Test scoring. Activates for "we're rolling out the Code & QA pack — what's the plan?", "Tomislav's adoption is high — should he be an AI Champion?", "the team self-reports +25% productivity but DORA shows +5% — what do we do?", "5 partners are quietly not using the new tool — diagnose". Enforces the mandatory 90-day METR baseline before any major rollout, the recognised-not-appointed AI Champion discipline, the 70/20/10 pilot cohort composition, and the discipline that the rollout itself is a Klarna Test trigger separate from the pilot.
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
oot_pack_id: S6
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1, S2, S3, S5]
oot_provides_to: [S4]
oot_klarna_test: true  # Pack invokes R7 at decision points
last_updated: 2026-05-08
---

# Change Management / Resistance

> **Generation marker:** Hardened in v1.0.
> **Klarna Test interaction:** **YES** — the pack invokes R7 at decision points (post-pilot proceed, 90-day reversal-or-continue) and contributes the change-management side of the rubric.
> **Brain interaction:** Both — reads X1 outputs, partner profiles, prior pilots; writes pilot summaries, AI Champion designations, resistance observations, plateau plans.

## 1. Purpose

The framework's response to the **central problem** (`MANIFESTO.md` Thesis 1: *resistance is the bottleneck on AI value capture, not model quality*). Encodes Kotter's eight-step framework, the ADKAR model, the **METR perception-gap baseline discipline**, the AI Champion criteria, and the 6–8 week pilot template. Mandatory before any major Skill Pack rollout.

This pack is what stops an ØØT firm from joining the 95% of MIT NANDA's pilots that produce no measurable P&L impact. The discipline is non-negotiable because the failure mode is invisible without it.

## 2. When to invoke this pack

1. **Before any Skill Pack rollout** affecting >25% of partners — METR baseline mandatory.
2. **When designing a 6-8 week pilot** for a new tool / Skill / workflow.
3. **When recognising an AI Champion** — provides the 4 criteria.
4. **When resistance patterns are observed** — shadow refusal, perception gap, sceptic alignment.
5. **At Klarna Test pre-rollout step** — provides the change-management side of the rubric.
6. **At the 90-day post-deployment review** of any Klarna-passed decision — re-run baseline; check perception gap evolution.
7. **When the 12-24 month plateau hits** (typically months 6-12) — provides the persistence playbook.

## 3. When NOT to invoke this pack

1. Tool changes that don't affect partner workflows (backend infra swap with no surface change).
2. One-off experiments (a single partner trying a new tool for a week without firm-level rollout intent).
3. **After-the-fact** — if the rollout already happened without baseline, the pack flags this as a discipline failure rather than retroactively pretending; it does **not** reconstruct a baseline from memory.

## 4. Operational instructions

### 4.1 METR baseline procedure

Mandatory before any major rollout. Procedure:

1. **Identify the metrics** appropriate to the rollout. Canonical set:
   - **DORA:** deployment_frequency, lead_time_for_changes, change_failure_rate, time_to_restore_service.
   - **SPACE:** satisfaction_score (survey), performance_metric (domain-specific), activity_count, communication_quality, efficiency_index.
   - **DX Core 4:** deep_work_hours, cycle_time, dx_score, ai_assist_uptake.
2. **Choose the measurement window**: **90 days**. Shorter windows risk seasonality contamination.
3. **Pre-populate X5 Baseline_Metrics** with the chosen metrics, the data source, the owner, the capture cadence.
4. **Run the measurement for the full 90 days BEFORE any pilot starts.**
5. **Lock the baseline at day 90.** Recorded as a decision (`firm/decisions/D-YYYY-NNN.md`); locked values written to X5.
6. **Continue parallel measurement during the pilot.** The pack's weekly update populates X5 Self_Report_vs_Actual sheet.
7. **Compute the perception gap weekly** — formula `=IF(ABS(self_report - measured) > 20, "PERCEPTION_GAP", "OK")` flags gaps >20 points (≈ half the METR 39-point swing). Tighten to 15 once the firm has 90 days of internal baseline data.
8. **Surface gaps at the BR.** Every flagged perception gap becomes a Klarna-status-block agenda item.

### 4.2 Pilot cohort selection (15–20%)

**Inclusion criteria** (all four required):
1. Partner volunteers (no draft selection — pilots run on consent).
2. Partner has a baseline measurement (per §4.1).
3. Partner's output mix in the rollout's domain is sufficient for meaningful measurement.
4. Partner's reward species declaration is compatible with the pilot's incentive structure.

**Cohort composition target:**
- **Participants** (the pilot users): 70%.
- **Control** (continues current workflow): 20% — provides the counterfactual.
- **Champion-candidates** (high-output, AI-curious, willing to mentor): 10%.

**Selection process:**
1. Founder + S6-running partner draft candidate list.
2. Each candidate gets 15-min conversation: *"we're piloting X; would you want in?"* (consent first; no pressure).
3. Volunteers matched to roles per composition target.
4. Cohort recorded in X5 Pilot_Cohort sheet.

### 4.3 Pilot execution (6–8 weeks)

- **Week 0 (pre-pilot):** cohort selection complete; baseline locked; partners briefed; tooling provisioned.
- **Week 1:** tool/Skill in use. Daily friction notes captured by partners in their `firm/partners/<id>/private/pilot-notes.md` (private — partner controls visibility).
- **Weekly check-ins** (each Wednesday, 30 min): facilitated by S6-running partner. Format: each cohort partner shares one win + one friction. Friction items tagged in Brain.
- **Week 4 mid-point review:** cohort + founder. Measured DORA/SPACE/DX delta vs. baseline. Perception gap check. Decision: continue / iterate / abandon.
- **Weeks 5–7:** continued pilot with iterations from mid-point.
- **Week 8 close:** final measurement; close-out report at `firm/change/pilots/<pilot_id>.md` per `templates/brain/pilot-summary.md`.

**Success criteria:**
- **Proceed to full rollout** if: measured delta positive, perception gap <20 points, ≥80% cohort recommendation, no Klarna obstruction.
- **Iterate** if: measured delta positive but perception gap large; or one criterion missed but recoverable.
- **Abandon** if: measured delta zero or negative after 8 weeks; or cohort recommendation <50%.

### 4.4 Post-pilot decision (proceed / iterate / abandon)

If proceeding:

1. **The full rollout is itself a Klarna Test trigger** even if pilot passed. Rationale: pilot-to-full-rollout often involves capacity that *could* displace partners (the same Skill applied to 100% of the team may make some roles redundant in ways the pilot did not).
2. Pack invokes R7 with the rollout decision summary; test scored per `governance/KLARNA-TEST.md`.
3. Only on `proceed` (≥14/20) does rollout commence.
4. The 90-day post-rollout review (Q9) scheduled with founder as owner.

If iterating: fresh pilot cycle starts, iteration scope explicitly recorded.

If abandoning: lessons-learned Brain page; partners thanked and unwound.

### 4.5 AI Champion designation — recognised, not appointed

Criteria (all four required for recognition):

1. **Demonstrably increased throughput** — measured. Partner's `total_outputs × value_envelope` (from X1) increased ≥30% in 90 days following AI tool adoption vs. prior 90-day baseline.
2. **Demonstrably maintained or increased quality** — `rework_within_30d` rate has not increased; ideally decreased.
3. **Mentorship signals** — partner voluntarily helped ≥3 other partners with AI tooling questions (visible in Slack/dChat helps thread, in `Co-authored-by:` patterns, or pair-programming records).
4. **AI-curious cultural posture** — visible by Brain contributions (prompts in `firm/prompts/`, ADRs involving AI tooling decisions).

A partner meeting all four is **recognised** at the next BR. Brain page at `firm/change/ai-champions/<partner_id>.md`. Recognition includes:
- The data (measurements that triggered recognition).
- A small variable-pay multiplier bump (recommended +0.1 on `output_multiplier` for next 6 months — small but real).
- The explicit mentorship role (firm's go-to for tooling questions; part-time, not full-time).

**Revoked** if criteria stop holding ("honest revocation").

> ⚠️ **Don't appoint.** If the firm has no partner meeting the criteria, the firm has no AI Champion. The Tecknoworks/Caplaz pattern — appointing before earning — is the failure mode.

### 4.6 Resistance pattern recognition

Three patterns. Each has signals + responses.

**Shadow refusal** (licensed-but-unused):
- **Signal:** tool provisioned (Bitwarden seat, license active), actual usage <10% of team's median.
- **Cause:** partner doesn't trust the tool, or tried-once-failed, or philosophically opposed.
- **Response:** 1-1 conversation. **Not** an escalation. Shadow refusal is information, not insubordination. The partner may be right.

**Perception gap** (METR-style swing):
- **Signal:** weekly self-report claims +15-25% productivity; measured DORA/SPACE/DX delta is flat or negative.
- **Cause:** structural feature of human self-assessment under AI assistance (METR 2025).
- **Response:** surface gently in next BR. **Don't** confront. **Do** show the data side-by-side. Most partners adjust their self-assessment within 2-3 cycles.

**Sceptic alignment** (partnership-against-tool):
- **Signal:** ≥3 partners independently flag the same friction; not addressed in iteration cycle.
- **Cause:** real friction; rollout has a flaw early pilot didn't surface.
- **Response:** **pause the rollout.** Convene the sceptics. When ≥3 partners independently flag the same issue, the issue is real. Treat as Tier-2 escalation (per DECISION-RIGHTS if compensation-affecting; per working session otherwise).

### 4.7 Rollout communication

Post-Klarna proceed:

1. **Founder announcement** in next BR (verbal) + Brain page at `firm/change/rollouts/<rollout_id>.md` (written).
2. **Honest framing:**
   - What the pilot found (measured delta, perception gap, cohort feedback).
   - What Klarna scored and conditions imposed.
   - The reversal threshold (per Klarna Q3): if pilot pattern degrades beyond X, we revert.
   - The 90-day review date and owner (per Klarna Q9).
3. **No marketing language.** No "exciting transformation" / "synergy" / "leverage". Rollouts are operational decisions, not motivational events.
4. **Q&A window (1 week):** partners raise concerns asynchronously in `#change`; addressed in next BR.

### 4.8 12–24 month plateau planning

MIT NANDA: most failed pilots failed because the team quit after pilot disappointment, not because the technology didn't work. Discipline:

- **Pre-commit an 18-month operational horizon** for any major rollout. Klarna Q10 (founder defends in 2 years) is the long-horizon check.
- **Plan for a plateau** at months 6-12. Uptake stalls; novelty wears off; partners who were going to adopt have adopted; partners who weren't are visible.
- **Plateau response is NOT "double down on the rollout".** It's "iterate the workflow around the partners who didn't adopt". Sometimes the partners are right; the workflow is wrong; the rollout was the wrong scope.
- **Schedule a plateau review at month 12** (calendar invite at rollout start). Pre-read: full DORA/SPACE/DX trajectory, AI Champion register, Klarna 90-day reviews, sceptic-alignment incidents.
- **Plateau decisions:** continue / refocus / partial-rollback / full-rollback. Each is a `firm/decisions/` page.

## 5. Brain interaction protocol

**Reads:** `firm/output-logs/*` (for AI Champion eligibility); `firm/partners/<id>/profile.md` (for cohort eligibility); `firm/klarna-tests/*` (for cross-referencing pilot outcomes).

**Writes:** `firm/change/pilots/<pilot_id>.md`; `firm/change/ai-champions/<partner_id>.md`; `firm/change/rollouts/<rollout_id>.md`; `firm/change/plateau-plans/YYYY-MM.md`; `firm/change/resistance-observations/YYYY-MM-DD-<pattern>.md`.

## 6. Excel interaction protocol

> **On the `mcp__excel__*` tools in this pack's frontmatter (ADR-001):** Excel writes go through **openpyxl in code execution on the Ledger clone on BOTH tracks** — cloud and privacy Routines perform the identical operation, then signed-commit + push; there is no Google Sheets path. The `mcp__excel__*` tools are **optional, human-in-the-loop only** (a founder inspecting or hand-patching a workbook at their workstation) and are never the Routine write path. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md).

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X5 metr-baseline.xlsx | Baseline_Metrics | Write | Pre-rollout |
| X5 | Self_Report_vs_Actual | Append | Weekly during pilot |
| X5 | Pilot_Cohort | Write | Per pilot |
| X5 | Adoption_Curve | Append | Weekly during pilot |

## 7. Routine integration

Pack invokes **R7** (Klarna Test) at decision points (post-pilot proceed, 90-day reversal-or-continue). Contributes to **R2** via change-status block.

## 8. Don'ts

1. Don't roll out without a METR baseline. Mandatory — no exceptions.
2. Don't appoint an AI Champion. Recognised, not named.
3. Don't ignore shadow refusal. Investigate; do not escalate.
4. Don't extend a failing pilot past 8 weeks. Stop and re-design.
5. Don't measure post-rollout against post-rollout perception. Always vs. baseline.
6. Don't confront a perception gap directly. Surface the data; let the partner adjust.
7. Don't proceed to full rollout without a Klarna Test on the rollout itself, even if pilot was clean.
8. Don't run a rollout without a 90-day review on the calendar.
9. Don't assume a plateau means failure. Plateaus are predictable; response is iteration, not despair.

## 9. Quick reference

| Situation | Action | Output |
|---|---|---|
| Planning a rollout | §4.1 baseline 90 days first | X5 Baseline_Metrics locked |
| Pilot starting | §4.2 cohort + §4.3 8-week structure | X5 Pilot_Cohort + weekly notes |
| Pilot mid-point | Week-4 review; continue/iterate/abandon | Pilot summary update |
| Pilot close | §4.4 final decision; if proceed → R7 fires | Pilot summary; Klarna entry |
| AI Champion criteria met | §4.5 recognition with data | `firm/change/ai-champions/<id>.md` + multiplier bump |
| Shadow refusal observed | §4.6 1-1 conversation, no escalation | Resistance observation Brain page |
| Perception gap | §4.6 surface in BR with side-by-side data | BR notes + X5 row |
| Sceptic alignment | Pause rollout; convene sceptics | Tier-2 escalation Brain page |
| 12-month plateau review | §4.8 review with full trajectory | Plateau decision Brain page |

## 10. References

1. **Kotter, J. P.** *Leading Change* (HBS Press, 1996).
2. **Hiatt, J.** *ADKAR* (Prosci, 2006).
3. **METR.** *RCT on AI tools and developer productivity* (July 2025) and February 2026 follow-up.
4. **MIT NANDA.** *The GenAI Divide* (August 2025).
5. **Microsoft.** *Work Trend Index 2025: The Frontier Firm.*
6. **Forsgren, N. et al.** *Accelerate* + *DORA Report 2025.*
7. **Tecknoworks / Caplaz.** *AI Champion case studies* (2024–2025).
8. **Dell'Acqua et al.** *The Cybernetic Teammate* (HBS WP 25-043, 2025).
9. ØØT `MANIFESTO.md`, Thesis 1.
10. ØØT `governance/KLARNA-TEST.md`.
