---
name: compensation-attribution
description: Use whenever the partner is onboarding a new partner (Reward Species Declaration), drafting an Output Spec, processing daily output capture, computing monthly variable pay, settling quarterly long-tail entitlements, calculating the annual bonus, surfacing a compensation dispute, or identifying the affected partner / non-beneficiary reviewer for a Klarna Test. Activates for "draft Mira's reward species", "what's the August variable for Davor?", "compute long-tail for Q1", "this output should be S not M", "the partner disputes their statement", "who is affected by this PR's automation?". Enforces the seven-layer compensation picture (base + variable + long-tail + bonus operational in Gen 1; subscription credits + dividends + capital appreciation deferred to Gen 2), the cross-workbook discipline (X1 partner_multiplier written by the Routine at row-append time, not by formula), and the rework-within-30-days zero-out as the framework's correction mechanism.
version: 1.0.0
tier: 1
status: hardened
allowed_tools:
  - mcp__my-curator__list_domains
  - mcp__my-curator__get_index
  - mcp__my-curator__search_wiki
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__github__list_commits
  - mcp__github__get_pull_request
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__excel__append_row
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S3
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1, S2]
oot_provides_to: [S4, S5, S6]
oot_klarna_test: true  # The pack triggers R7 via the ai-replaces-human label
last_updated: 2026-05-08
---

# Compensation & Attribution

> **Generation marker:** Gen 1 ships layers 1, 2, 3, 5 operational. Layers 4, 6, 7 deferred to Gen 2.
> **Klarna Test interaction:** **YES** — this pack identifies affected partners and the non-beneficiary reviewer for any PR labelled `ai-replaces-human`. It does not score the test (humans score per `governance/KLARNA-TEST.md`); it sets up the scoring artefact.
> **Brain interaction:** Both — heavy reads of partner pages, output specs, output logs; heavy writes to variable statements, long-tail statements, dispute records.

## 1. Purpose

The most distinctive ØØT Skill Pack. Operationalises the **seven-layer YOLO compensation model** — base, output variable, long-tail outcome, subscription credits, role-weighted bonus, dividends, capital appreciation. v1.0 ships layers 1, 2, 3, and 5 fully operational; layers 4, 6, 7 are deferred to Generation 2 because they require crypto rails and material legal scoping.

This pack encodes the **attribution agent pattern**: read commits, specs, reviews, contracts, milestones; produce a daily per-partner output ledger; compute monthly variable; track quarterly long-tail entitlements; surface anomalies for human review.

## 2. When to invoke this pack

1. **Partner onboarding** — drafting and signing the Reward Species Declaration (X2).
2. **Output Spec drafting** — when a partner commits to a new piece of work.
3. **Daily output capture** — invoked by R1 every day at 18:00.
4. **Monthly variable calculation** — invoked by R3 on the 1st at 09:00.
5. **Quarterly long-tail settlement** — invoked by R4 on quarter open.
6. **Annual bonus** — invoked manually by the founder once a year (typical: January).
7. **Klarna Test PR detection** — when the auto-labeller tags a PR `ai-replaces-human` and R7 fires.
8. **Variable pay dispute** — when a partner ticks the dispute box on a statement.
9. **Reward Species renegotiation** — at quarterly check-in or partner-/founder-initiated.

## 3. When NOT to invoke this pack

1. Treasury, runway, agent-cost ROI — those are S10's responsibility.
2. Tax filing — counsel territory; the pack produces the data tax filings need but does not file them.
3. Annual bonus calculation **before** the year is closed — the calculation runs after the December ledger is locked.
4. Unit Fund operations — locked in Gen 1; pack returns "Not available in Gen 1".
5. Cap-table management for existing investors — unrelated to compensation; routed to S10 / counsel.

## 4. Operational instructions

### 4.1 Reward Species Declaration (initial + renegotiation)

**Initial declaration** at onboarding:

1. Open `templates/excel/reward-species-declaration.xlsx` (X2).
2. Add a sheet named `<partner_id>` (one workbook with one sheet per partner is the convention for orgs <20 partners).
3. Populate **Partner_Profile** (cohort: `full-time-partner | project-specialist | advisor`; jurisdiction; base_currency; stablecoin_upgrade_pref; unit_fund_interest; two_worlds_self_id).
4. Populate **Base_Variable_Split**:
   - `reward_species`: `eat-what-you-kill | lockstep | hybrid`
   - `base_amount` (annual)
   - `variable_weight_personal` (C) + `variable_weight_team` (D) + `variable_weight_company` (E) **must sum to 1.0**
   - `output_multiplier` (F): default 1.0; rare adjustments
   - `bonus_split_personal` (G) + `bonus_split_team` (H) + `bonus_split_company` (I) **must sum to 1.0**
5. **Long_Tail_Schedule** starts empty.
6. **Unit_Fund_Eligibility** is locked in Gen 1 (sheet protection enabled).
7. **Renegotiation_Log** starts empty.
8. Generate signed PDF; store at `firm/partners/<partner_id>/legal/reward-species-YYYY-MM-DD.pdf`.
9. Compile Brain summary at `firm/partners/<partner_id>/reward-species-declaration.md` (per `templates/brain/reward-species-declaration-summary.md`).
10. Both founder and partner sign (digital signature on PDF; signed git commit).

**Renegotiation flow:**

- Append row to Renegotiation_Log: date, initiated_by, reason, fields_to_change.
- Apply changes; **update `start_date` of new terms in Partner_Profile** (do not retroactively rewrite).
- Re-sign PDF; commit a versioned PDF.
- Update Brain summary with `## Renegotiations` section.
- Record as `firm/decisions/D-YYYY-NNN.md`.

> ⚠️ **Important:** prior period's compensation never recomputes. If a renegotiation lands mid-month, the partner statement for that month explicitly shows the split.

### 4.2 Output Spec drafting

Output Specs are drafted **before** work begins. They live at `firm/partners/<partner_id>/output-specs/YYYY-MM-DD--<slug>.md` per `templates/brain/output-spec.md`.

Procedure:
1. Partner + founder open a fresh Claude session.
2. Walk through the template: title, value tier (S/M/L/XS — see §4.10), expected outcome (one sentence), outcome review date, acceptance criteria, out of scope, risks, long-tail entitlement (if applicable).
3. Sign-off recorded inline (`drafted by`, `accepted by`).
4. Cross-link to product/customer pages where applicable.

R1 will reference the Output Spec by wikilink at output-capture time. If R1 captures an output without an Output Spec, it flags `status: needs-spec` for the next BR.

### 4.3 Daily output capture (R1 invocation pattern)

Invoked by R1 at 18:00. For each detected output signal:

1. Resolve `partner_id` from author/owner. If multiple authors, append fractional rows.
2. Classify `output_type`: `commit | pr_merged | contract_signed | deal_closed | spec_drafted | review_completed | design_shipped | content_published`.
3. Cross-reference `output_spec_ref`. If missing → `status: needs-spec`.
4. Determine `value_tier` (default L if no Output Spec).
5. Estimate `ai_authored_pct` from `Co-authored-by:` trailers + diff patterns.
6. Set `rework_within_30d=No` (R1 retroactively flips per its detection rule).
7. **Resolve `partner_multiplier` (X1.J) by reading X2's `output_multiplier` field at runtime** — do not use a cross-workbook formula.
8. Compute `value_envelope` (X1.K) from the embedded lookup (XS=100, L=500, M=2000, S=8000 — Gen 1 defaults).
9. Append rows to X1 Output_Log.
10. Write daily summary to `firm/output-logs/YYYY-MM-DD.md` (per `templates/brain/daily-output-log.md`).

**Anomaly flag** if a full-time partner has zero outputs for >3 consecutive days.

### 4.4 Monthly variable calculation (R3 invocation pattern)

On the 1st of each month at 09:00:

1. **Lock previous month's Output_Log** (X1) — write `month_locked: YYYY-MM` to a hidden metadata sheet.
2. Verify `rework_within_30d` is current — re-check R1's detection rule for any new commit since.
3. Aggregate per partner: `total_outputs`, `total_variable = SUM(L)`. Write to Monthly_Variable.
4. Read X2 for `base_amount`, `output_multiplier`, current reward_species. Compute `base_pay` (calendar-day proration).
5. Compute `total_compensation = base_pay + total_variable`.
6. Generate per-partner statement at `firm/partners/<partner_id>/variable-statements/YYYY-MM.md` per `templates/brain/variable-statement.md`. Include the Acknowledgement block with two checkboxes (agree / dispute).
7. Email/dMail partner with link to Brain page.
8. Post `#compensation` summary.
9. **Poll the partner's statement page once daily** for the acknowledgement checkbox state. Update `sign_off_status` per the table:

| Detected state | sign_off_status |
|---|---|
| First box ticked | `partner_reviewed` |
| Second box ticked | `partner_disputed` (escalates to Tier 1) |
| Both ticked | `partner_disputed` |
| Neither, ≥5 business days | `partner_unresponsive` |
| Neither, <5 business days | `draft` |

10. Compile founder-approval packet at `firm/compensation/YYYY-MM/founder-approval.md` after acknowledgements complete or 5 business days pass.
11. Founder approval flips `sign_off_status='founder_approved'`. Payment triggers (Gen 1: manual SEPA/wire; Gen 2: stablecoin via Rise/Circle).

### 4.5 Long-tail entitlement (manual entry + R4 settlement)

**Manual entry** when an output ships with long-tail eligibility:

1. R1 captures the output; flags for human review of long-tail eligibility.
2. At next BR, founder + partner agree on terms: outcome metric, partner_share_pct (0–100; typical 5–15%; rarely above 25%), settlement_period (Gen 1: quarterly), start_date, end_date or "ongoing".
3. Append to X2 Long_Tail_Schedule.
4. Cross-link in the Output Spec's `## Long-tail entitlement` section.

**Quarterly settlement** (R4):

1. Read all X2 Long_Tail_Schedule rows where `start_date <= quarter_end` AND (`end_date` empty OR `end_date > quarter_end`).
2. For each (partner, output) pair, query the realised outcome attributable to the output during the quarter.
3. Compute `payment = outcome_attributable × partner_share_pct / 100`.
4. Update `total_settled_to_date += payment`.
5. Generate quarterly statement at `firm/partners/<partner_id>/long-tail-statements/YYYY-QN.md`.
6. Email/dMail; founder approves; payment processes.

> ⚠️ **Honest framing:** outcome attribution is not always clean. For ambiguous cases, flag for founder + affected-partner review; do not pay until resolved; defer to next quarter if needed.

### 4.6 Annual bonus calculation

Once a year, after December ledger lock:

1. Founder sets the bonus pool (typically 5–15% of net profit; not specified by the framework).
2. Per partner, compute:
   - `personal_third` = sum-of-year `computed_variable` × `bonus_split_personal`.
   - `team_third` = pool × bonus_split_team (founder-allocated team component).
   - `company_third` = pool × bonus_split_company.
   - `annual_bonus = personal_third + team_third + company_third`.
3. Generate `firm/partners/<partner_id>/annual-bonus/YYYY.md`.

### 4.7 Klarna Test interaction (R7 trigger)

When R7 fires (PR labelled `ai-replaces-human`):

1. Identify **affected partner(s)** by checking which partners have an Output Spec whose `expected_outcome` overlaps with the PR's automated capability.
2. Identify the **non-beneficiary reviewer** by reading X1 Monthly_Variable + X2 Long_Tail_Schedule (rolling 90 days): pick a partner whose total comp does not increase as a result of the action.
3. Write `affected_partners` and `non_beneficiary_reviewer` fields into X4 Decision_Log and `firm/klarna-tests/KT-YYYY-NNN.md`.
4. **Do not score the test.** Humans score per `governance/KLARNA-TEST.md`.

### 4.8 Dispute initiation

When a partner ticks the dispute checkbox:

1. R3's poll detects the state change; sets `sign_off_status='partner_disputed'`; notifies founder.
2. Open Tier-1 dispute record at `firm/compensation/<month>/disputes/D-YYYY-NN-NNN.md` per `templates/brain/dispute-record.md`.
3. Link to disputed statement, X1 rows, X2 declaration.
4. **Do not flip to `founder_approved` while a dispute is open.**

The pack does not resolve disputes — that's `governance/DECISION-RIGHTS.md` Tier 1/2/3 flow.

### 4.9 Anomaly surfacing

Three checks per invocation:

1. **Zero-output partner** — full-time partner with zero captured outputs for >3 consecutive days.
2. **Rework spike** — `rework_within_30d=Yes` rate >25% of partner's outputs in rolling 30 days.
3. **Variable outlier** — monthly variable >2σ from partner's 6-month rolling average.

Each becomes a Brain note at `firm/anomalies/YYYY-MM-DD-<partner_id>-<type>.md`.

### 4.10 Value-tier rubric

| Tier | Envelope (Gen 1) | Engineering | Sales | Legal/contract |
|---|---|---|---|---|
| **S** flagship | €8,000 | Major feature with measurable customer impact (6-week build) | Tier-1 customer landed; multi-year ARR | Master services agreement; SaaS resale |
| **M** significant | €2,000 | Feature improving existing surface; substantial refactor; new dashboard | Standard customer landed in expected cycle | Standard customer execution; funding term-sheet redline |
| **L** standard | €500 | 1-3 day commit; documented design choice; substantive review | Expanded SOW; meaningful pipeline touch | Routine vendor agreement; NDA |
| **XS** maintenance | €100 | Bug fix; dependency bump; small refactor | Pipeline-tracking touch | Routine review |

Firms calibrate absolute envelope numbers; **keep the ratio approximately 1:5:20:80** across XS:L:M:S.

Value tier set at Output Spec drafting; **refined as outcomes come in**. An M output that produces an S-level outcome stays M for variable (variable pays on output); recorded as S in long-tail (long-tail pays on outcome).

## 5. Brain / Ledger interaction protocol

**Reads** (all live in the **Ledger** — the firm's GitHub operational repo, scoped to `firm/`): `firm/partners/<id>/profile.md`, `reward-species-declaration.md`, `output-specs/*`; `firm/output-logs/*`; `firm/decisions/*`; `firm/klarna-tests/*`.

**Writes** (Ledger): `firm/partners/<id>/variable-statements/*`, `long-tail-statements/*`; `firm/output-logs/*` (via R1); `firm/compensation/<month>/founder-approval.md`; `firm/compensation/<month>/disputes/*`; `firm/anomalies/*`.

Wikilink discipline: every page references existing slugs; no invented wikilinks.

### Cloud-track invocation context

When S3 is invoked from **cloud Routines** (R1, R3, R4, R7), the my-curator MCP tools listed in this Skill's frontmatter are **NOT reachable** — those tools are stdio MCPs on the founder's local machine, not on Anthropic's Routine sandbox. Inside cloud Routines the data flow is:

- **Partner resolution / profile lookup** — read from X2 (`reward-species-declaration.xlsx`) via openpyxl. X2's Partner_Profile sheet holds the per-partner metadata Routines need; my-curator is unnecessary.
- **Output spec / decision lookup** — read from the Ledger clone (markdown files under `firm/output-specs/`, `firm/decisions/`) using plain filesystem reads, since the Routine has the Ledger cloned anyway.
- **Cross-partner context that would normally come from the Curator graph** — defer to v1.x. If a particular S3 invocation needs richer semantic context, the founder runs the corresponding manual workflow (§4.1, §4.2) on their own workstation where my-curator is reachable.

When S3 is invoked **manually by a founder** (in Claude Desktop or Claude Code on their workstation), all my-curator tools work normally — that's the canonical Skill Pack execution environment.

## 6. Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X1 partner-output-ledger.xlsx | Output_Log | Append | R1 |
| X1 | Output_Log col I | Update prior rows | R1 retroactive |
| X1 | Monthly_Variable | Write | R3 |
| X1 | Partner_Multipliers_Snapshot | Refresh | R3 monthly |
| X2 reward-species-declaration.xlsx | Partner_Profile, Base_Variable_Split | Write | Manual onboarding |
| X2 | Long_Tail_Schedule | Append | Manual + R4 settlement |
| X2 | Renegotiation_Log | Append | Manual renegotiation |
| X4 klarna-test.xlsx | Decision_Log, Klarna_Score | Write | R7 |

Never touches X3, X5, X6, X7, X8, X9.

## 7. Routine integration

Invoked by **R1**, **R3**, **R4**, **R7**. Manually invoked for §4.1, §4.2, §4.6, §4.8.

## 8. Don'ts

1. Don't compute variable pay without monthly human sign-off — calculator is advisory; founder pays.
2. Don't override a partner's Reward Species Declaration without signed renegotiation.
3. Don't aggregate output in ways that obscure individual attribution.
4. Don't treat AI-generated commits as equivalent to human-written for attribution; use `Co-authored-by:` trailers + `ai_authored_pct` field. Discipline is rework-within-30d zero-out, not ai-pct discount.
5. Don't bypass the Klarna Test when a Skill rollout would replace a partner's primary function.
6. Don't retroactively recompute closed-month variable pay — the month-locked flag exists for this.
7. Don't pay variable pay through any mechanism that bypasses the Brain audit trail.
8. Don't open a Tier-1 dispute without first surfacing in conversation with the affected partner.
9. Don't compute long-tail without a written attribution methodology for the outcome metric.

## 9. Quick reference

| Situation | Action | Output |
|---|---|---|
| Onboard partner | §4.1 initial declaration | X2 sheet + Brain reward-species page + signed PDF |
| Daily ledger capture | R1 fires; §4.3 | X1 Output_Log + Brain daily log |
| Detect rework | R1 detection rule fires | X1 row col I flips to Yes |
| Monthly variable | R3 fires; §4.4 | X1 Monthly_Variable + per-partner statements + founder packet |
| Partner dispute | R3 detects ticked box; §4.8 | Tier-1 dispute record |
| Long-tail entry | Manual at BR; §4.5 | X2 Long_Tail_Schedule + Output Spec cross-link |
| Quarterly settlement | R4 fires; §4.5 | Per-partner long-tail statement + X2 update |
| AI replaces partner function | R7 fires; §4.7 | X4 Decision_Log + Klarna Brain page |
| Renegotiation | §4.1 renegotiation flow | Renegotiation_Log + new PDF + decision record |
| Annual bonus | §4.6 once per year | Per-partner annual-bonus page |

## 10. References

1. **Yolo Investments** (Tim Maslyukov). *Stop paying for hours. Start paying for output.* (May 2026). The seven-layer compensation framing.
2. **Levin, J. & Tadelis, S.** *Profit Sharing and the Role of Professional Partnerships* (Stanford GSB, 2005).
3. **Ressler, C. & Thompson, J.** *Why Work Sucks and How to Fix It* (Penguin, 2008). ROWE.
4. **MHPR Advisors.** *Reward Species Typology* (industry working paper, 2023).
5. **Hope, J. & Fraser, R.** *Beyond Budgeting* (Harvard Business School Press, 2003).
6. **Weitzman, M. L.** *The Share Economy* (Harvard University Press, 1984).
7. **MBO Partners.** *State of Independence in America 2025*.
8. **DORA Report 2025.** *State of AI-Assisted Software Development*.
9. ØØT `MANIFESTO.md`, Thesis 3.
10. ØØT `governance/KLARNA-TEST.md`.
11. ØØT `governance/DECISION-RIGHTS.md`.
12. ØØT `templates/excel/SPEC.md` — X1, X2, X4 schemas.
