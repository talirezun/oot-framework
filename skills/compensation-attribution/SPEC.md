# Skill Pack S3 — Compensation & Attribution: SPEC

> **Historical build spec (pre-v1.0.1 in places). Where this file and SKILL.md disagree, SKILL.md is authoritative.**

**ID:** S3
**Name:** Compensation & Attribution
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

The most distinctive ØØT Skill Pack. Operationalises the seven-layer YOLO compensation model — base, output variable, long-tail outcome, subscription credits, role-weighted bonus, dividends, capital appreciation. v1.0 ships **layers 1, 2, 3, and 5** as fully operational; layers 4, 6, 7 are deferred to Generation 2.

Encodes the **attribution agent pattern**: read commits, specs, reviews, contracts, milestones; produce a daily per-partner output ledger; compute monthly variable; track quarterly long-tail entitlements; surface anomalies for human review; and gate via the Klarna Test any decision that would automate a partner's primary function.

This is the pack the framework's authors believe most clearly differentiates ØØT from generic Skill catalogues. The depth in this SPEC is intentional.

---

## The seven-layer compensation picture (Gen 1 / 2 / 3 markers)

Re-stated here for the pack's own reference (the canonical version is `MANIFESTO.md` Thesis 3):

| # | Layer | Status (Gen 1) | Cadence | Owner artefact |
|---|---|---|---|---|
| 1 | Guaranteed base | ✅ Operational | Monthly | `reward-species-declaration.xlsx` (X2) `base_amount` field |
| 2 | Output variable | ✅ Operational | Monthly | X2 `variable_weight_*`, X1 Output_Log → Monthly_Variable, R3 |
| 3 | Long-tail outcome | ✅ Operational (Excel-tracked, quarterly settlement) | Quarterly | X2 Long_Tail_Schedule, R4 |
| 4 | Subscription credits | 🔜 Gen 2 | Issued alongside variable | X2 Unit_Fund_Eligibility (locked in Gen 1) |
| 5 | Role-weighted annual bonus | ✅ Operational (manual; one-third / one-third / one-third default) | Annual | X2 `bonus_split_*`, founder runs |
| 6 | Dividends on units held | 🔜 Gen 2 | Quarterly (Gen 2) | Locked in Gen 1 |
| 7 | Capital appreciation | 🔜 Gen 2 | Per redemption (Gen 2) | Locked in Gen 1 |

Gen 1 partner Charter sign-on must explicitly note layers 4/6/7 as locked; Gen 2 activation requires written re-affirmation (it is not automatic).

---

## Scope

**Covers (Generation 1):**
- Reward Species Declaration onboarding and renegotiation.
- Output Spec drafting and storage in the Brain.
- Daily output capture from GitHub, Slack, Drive, contracts (via Routine R1).
- Variable pay calculation against value-tier multipliers (monthly, via Routine R3).
- Long-tail entitlement tracking (Excel-based, quarterly settlement via Routine R4).
- Annual bonus calculation (third-third-third with role weighting).
- Variable pay dispute initiation (handing off to the dispute resolution playbook in `governance/DECISION-RIGHTS.md`).
- **Klarna Test interaction**: any Skill that would automate a partner's primary function triggers Routine R7 via the `ai-replaces-human` PR label.

**Deferred (Generation 2):**
- Stablecoin payroll rail integration (Rise / Circle).
- Smart-contract long-tail entitlements (replaces Excel-based quarterly settlement with on-chain auto-payment).
- Subscription credit issuance.
- Internal Unit Fund subscription, dividend payments, capital appreciation tracking.

**Deferred (Generation 3):**
- Per-agent compensation (autonomous business units earning variable).
- Cotrugli Ledger PAC-RO co-signature for compensation events.

**Does NOT cover:**
- Treasury management (S10 Finance & Treasury).
- Tax handling (jurisdiction-specific; pointed to `docs/06-when-to-call-a-lawyer.md`).
- Equity / cap-table management for existing investors (corporate governance, not compensation).

---

## Allowed tools / dependencies

- **Curator MCP** — read Brain partner pages and reward-species declarations; write ledger entries, statements, and dispute records.
- **openpyxl in code execution on the Ledger clone (both tracks, per [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md))** — read/write X1 partner-output-ledger.xlsx and X2 reward-species-declaration.xlsx, then signed-commit + push; cloud and privacy Routines perform the identical operation (no Google Sheets). The cross-workbook discipline (write multiplier into X1.J at row-append time) is enforced. Excel MCP is an optional human-in-the-loop inspection tool only, not the write path.
- **GitHub MCP** — read commits, PR metadata for R1 capture.
- **Slack MCP** (cloud track) **/ 4thtech CLI** (privacy track) — read configured channels for output signals; post statements to `#compensation`.
- **Email MCP / dMail CLI** — send variable-pay statement notifications to partners.
- **Filesystem MCP / Desktop Commander** (privacy track) — for local Brain operations.

---

## Section structure

The eventual SKILL.md follows the canonical template. Numbered sections below correspond to §4 of the SKILL.md.

---

## When to invoke

1. **Partner onboarding** — to draft and sign the Reward Species Declaration.
2. **Output Spec drafting** — when a partner commits to a new piece of work.
3. **Daily output capture** — invoked by R1 every day at 18:00.
4. **Monthly variable pay calculation** — invoked by R3 on the 1st at 09:00.
5. **Quarterly long-tail settlement** — invoked by R4 on quarter open at 09:00.
6. **Annual bonus calculation** — invoked manually by the founder once a year (the framework's authors run this in January).
7. **Klarna Test PR detection** — when the auto-labeller (Phase 8) tags a PR `ai-replaces-human`, R7 fires this pack's Klarna invocation.
8. **Variable pay dispute** — when a partner ticks the `dispute` box on a variable statement, the pack opens the Tier-1 dispute flow.
9. **Reward Species renegotiation** — at quarterly partner check-in, or partner-initiated, or founder-initiated.

---

## When NOT to invoke

1. **Treasury, runway, agent-cost ROI** — those are S10's responsibility.
2. **Tax filing** — counsel territory; the pack does not file taxes, it produces the data tax filings need.
3. **Annual bonus calculation, before the year is closed** — the calculation runs after the December ledger is locked, not mid-year.
4. **Unit Fund operations** — locked in Gen 1; pack returns "Not available in Gen 1" when invoked for unit-fund ops.
5. **Cap-table management** — unrelated to compensation; routed to S10 / counsel.

---

## Operational instructions

### 4.1 Reward Species Declaration workflow (initial + renegotiation)

**Initial declaration (during onboarding):**

1. Open `reward-species-declaration.xlsx` (X2) in the firm's spreadsheet tool.
2. Add the new partner's row to the single shared sheets (ADR-005: no per-partner sheets — one `Partner_Profile` row and one `Base_Variable_Split` row, each keyed by `partner_id` in column A).
3. Populate Partner_Profile (A: partner_id, B: full_name, C: cohort, D: start_date, E: jurisdiction, F: base_currency, G: stablecoin_upgrade_pref [Yes|No], H: unit_fund_interest [Yes|No], I: two_worlds_self_id).
4. Populate Base_Variable_Split (A: partner_id, B: reward_species, C: base_amount, D+E+F sum-to-1.0 variable weights, G: output_multiplier defaulted to 1.0, H+I+J sum-to-1.0 bonus splits — ADR-005 leading partner_id shift).
5. Long_Tail_Schedule starts empty; populated as outputs ship with long-tail eligibility.
6. Unit_Fund_Eligibility is **locked** in Gen 1 (sheet protection enabled; activation flag in `firm/decisions/D-...md` when Gen 2 opens).
7. Renegotiation_Log starts empty.
8. Generate a signed PDF of the populated sheet (a Python script — e.g. openpyxl/LibreOffice headless export — on either track). Store the PDF in `firm/partners/<partner_id>/legal/reward-species-YYYY-MM-DD.pdf`.
9. Create the corresponding Brain stub at `firm/partners/<partner_id>/reward-species-declaration.md` from `templates/brain/reward-species-declaration-summary.md`. Wikilink to the X2 sheet row + the signed PDF.
10. Both founder and partner sign (digital signature on PDF; commit to Brain via signed git commit).

**Renegotiation flow:**

A renegotiation triggers when:
- A partner requests it (commonly: cohort change, life change, jurisdiction move).
- The founder initiates (rare; usually tied to firm-level changes).
- A quarterly check-in surfaces drift between declared species and lived experience.

The pack's procedure:
1. Open the partner's X2 sheet.
2. Append a row to Renegotiation_Log with: date, initiated_by, reason, fields_to_change.
3. Apply the changes to Base_Variable_Split / Long_Tail_Schedule fields.
4. Update `start_date` of the new terms in Partner_Profile (the prior period's variable pay was computed under the old terms; do not retroactively rewrite).
5. Re-sign the PDF; commit a new versioned PDF to `firm/partners/<partner_id>/legal/`.
6. Update the Brain summary page with the new wikilink + a `## Renegotiations` section.
7. Notify the founder + the partner; record the renegotiation as a Brain decision record (`firm/decisions/D-YYYY-NNN.md`) for the firm's audit trail.

**Important constraint:** the prior period's compensation never recomputes. If a renegotiation lands on the 15th, the month closes 15 days under the old terms and continues 15 days under the new terms — the partner statement for that month explicitly shows the split.

### 4.2 Output Spec drafting

Output Specs are drafted **before** work begins. They define what "done" looks like. They live at `firm/partners/<partner_id>/output-specs/YYYY-MM-DD--<slug>.md` per `templates/brain/output-spec.md`.

The pack's drafting procedure:
1. Partner + founder open a fresh Claude Desktop session.
2. Partner describes the work in plain language.
3. The pack walks them through filling the template:
   - Title, value tier (S/M/L/XS — see §4.10 rubric below), expected outcome (one sentence), outcome review date.
   - Acceptance criteria (the bulleted list of "what done looks like").
   - Out of scope.
   - Risks / dependencies.
   - Long-tail entitlement section (only if the output is eligible — see §4.5).
4. Sign-off recorded inline in the Brain page (`drafted by`, `accepted by`).
5. Linked from the partner's profile page; cross-domain linked to `products/` if product-relevant.

The Output Spec is the **artefact R1 will reference at output-capture time** (column F in X1: `output_spec_ref` is a wikilink to this page). If R1 captures an output that has no Output Spec, it flags `status: needs-spec` in the daily summary and surfaces it at the next BR.

### 4.3 Daily output capture (R1 invocation pattern)

R1 invokes this pack's daily-capture skill at 18:00. The pack's procedure:

1. Read all output signals from the past 24 hours per `routines/SPEC.md` R1.
2. For each detected signal:
   a. Resolve `partner_id` from author / owner; if multiple authors, append fractional rows.
   b. Classify `output_type` from the canonical list: `commit | pr_merged | contract_signed | deal_closed | spec_drafted | review_completed | design_shipped | content_published`.
   c. Cross-reference `output_spec_ref` with the partner's `firm/partners/<id>/output-specs/`; if no match, flag `status: needs-spec` and continue.
   d. Determine `value_tier` per §4.10 rubric (default L if no Output Spec exists).
   e. Estimate `ai_authored_pct` from commit `Co-authored-by:` trailers and diff patterns; conservative default 0% unless evidence.
   f. Set `rework_within_30d` to `No` (R1 retroactively flips this per its detection rule — see `routines/SPEC.md` R1).
   g. **Resolve `partner_multiplier` (X1 column J)** by reading X2's `output_multiplier` (Base_Variable_Split column G, after the ADR-005 leading-partner_id shift) for that partner *at runtime* — join on `partner_id` (column A) — and writing the resolved number into X1; do not rely on a cross-workbook formula.
   h. Compute `value_envelope` (X1 column K) per the embedded value-envelope lookup (XS=100, L=500, M=2000, S=8000 — Gen 1 defaults; firms can adjust).
3. Append rows to X1 Output_Log; never edit existing rows except for the retroactive rework flip.
4. Refresh `Partner_Multipliers_Snapshot` sheet on the first run of each calendar month (this is R3's job in subsequent runs).
5. Write the daily summary to `firm/output-logs/YYYY-MM-DD.md` per `templates/brain/daily-output-log.md`.
6. Post the summary to Slack `#output-log` (cloud) or 4thtech dChat `#output-log` (privacy).

Failure handling: per R1's own SPEC. The pack also: if no output detected for a partner for >3 consecutive days, log an `## Anomalies` entry; >7 consecutive days, escalate to the next BR's agenda.

### 4.4 Monthly variable pay calculation (R3 invocation pattern)

On the 1st of each month at 09:00, R3 invokes this pack:

1. Lock the previous month's Output_Log (X1) — the pack writes a metadata flag `month_locked: YYYY-MM` to a hidden sheet so accidental edits to closed-month rows are visible at audit time.
2. For each row in the closed month, **verify `rework_within_30d` is current** — look forward to today's date; if any new commit since the row's date triggered the rework rule (per R1's regex), ensure the flip happened.
3. Aggregate per partner: `total_outputs = COUNTIFS(B,month,C,partner_id)`; `total_variable = SUMIFS(L,month,C,partner_id)`. Write to Monthly_Variable sheet.
4. Read the partner's X2: `base_amount`, `output_multiplier`, current reward_species. Compute `base_pay` proportional to the month (calendar-day proration; not pay-period proration — the framework prefers transparency over alignment with pay periods).
5. Compute `total_compensation = base_pay + total_variable`.
6. Set `sign_off_status='draft'` and `approval_date` empty.
7. Generate the per-partner Brain statement at `firm/partners/<partner_id>/variable-statements/YYYY-MM.md` per `templates/brain/variable-statement.md`. Includes:
   - The headline numbers.
   - The five top outputs by `computed_variable`.
   - Any retroactive zero-outs from prior months affecting this month's pool.
   - The Acknowledgement block (Brain checkbox per `routines/SPEC.md` R3).
   - The audit trail: linked X1 row indexes, linked X2 reward-species version.
8. Email / dMail the partner with a link to the Brain page.
9. Post to Slack/dChat `#compensation` with the totals.
10. Poll the partner's Brain statement page once daily; update `sign_off_status` per the table in `routines/SPEC.md` R3.
11. Compile the founder-approval packet at `firm/compensation/YYYY-MM/founder-approval.md` after either: all partners have acknowledged, OR 5 business days have elapsed.
12. Founder approval flips `sign_off_status='founder_approved'`; payment is then triggered (Gen 1: manual SEPA / wire; Gen 2: stablecoin via Rise/Circle).

### 4.5 Long-tail entitlement entry (manual + Routine R4 settlement)

**Manual entry (when an output ships with long-tail eligibility):**

1. Output ships, R1 captures it, R1 flags it for human review of long-tail eligibility (since this is non-default).
2. At the next BR, the founder + the partner agree on long-tail terms:
   - The outcome metric (e.g., revenue from this contract; cost saved from this Skill rollout; customer NPS lift).
   - The partner's share % (a number 0-100; typical: 5-15%; the framework's authors find anything above 25% creates incentive distortions and recommend caution).
   - Settlement period (Gen 1: quarterly; Gen 2: per-milestone for stablecoin).
   - Start and end dates (or "ongoing" if the output's outcome compounds indefinitely).
3. Record in X2 Long_Tail_Schedule (columns A: output_id, B: description, C: partner_share_pct, D: settlement_period, E: start_date, F: end_date, G: total_settled_to_date).
4. Cross-link in the partner's Brain Output Spec page (its `## Long-tail entitlement` section).

**Quarterly settlement (R4):**

1. R4 reads all X2 Long_Tail_Schedule rows where `start_date <= quarter_end` AND (`end_date` empty OR `end_date > quarter_end`).
2. For each (partner, output) pair, query the Brain or financial system for the realised outcome attributable to the output during the quarter.
3. Compute payment = outcome_attributable × partner_share_pct / 100.
4. Update X2 Long_Tail_Schedule `total_settled_to_date += payment`.
5. Generate the partner's quarterly statement at `firm/partners/<partner_id>/long-tail-statements/YYYY-QN.md` per `templates/brain/long-tail-statement.md`.
6. Send via email/dMail; founder approves; payment processes.

**The hard part (and the framework's honesty):** outcome attribution is not always clean. The pack's procedure for ambiguous cases:
- Flag the output_id for founder + affected partner review.
- Do not pay until resolved.
- If unresolvable in a single quarter, defer to the next quarter; the entitlement does not lapse.
- Document the resolution in the partner's long-tail statement page.

### 4.6 Annual bonus calculation

Once a year, after the December ledger is locked:

1. The pack reads each partner's X2 Base_Variable_Split bonus_split fields (G personal, H team, I company; sum to 1.0).
2. The firm sets the **bonus pool** (founder decides; typically 5-15% of net profit; not specified by the framework).
3. **Personal third** = sum across the year of the partner's `computed_variable` × the partner's bonus_split_personal weight.
4. **Team third** = the firm's team component (founder allocates, typically uniform across partners).
5. **Company third** = pool × bonus_split_company.
6. Partner's annual bonus = personal third + team third + company third (each weighted to sum to 1.0 within the partner's bonus_split).
7. Brain page generated at `firm/partners/<partner_id>/annual-bonus/YYYY.md`.

The framework does not auto-calculate the bonus pool size — that is a founder decision tied to treasury runway and reserve discipline (S10).

### 4.7 Klarna Test interaction (R7 trigger)

When R7 fires (PR labelled `ai-replaces-human`), this pack participates in the Klarna scoring:

1. R7 invokes S6 (Change Management) for the scoring rubric and the affected-partner consultation.
2. **This pack's contribution**: identify the affected partner(s) by checking which partners have an Output Spec (in `firm/partners/<id>/output-specs/`) whose `expected_outcome` overlaps with the PR's automated capability.
3. Identify the **non-beneficiary reviewer**: a partner whose `total_variable` (rolling 90 days) does not increase as a result of the action — the pack reads X1 Monthly_Variable and X2 Long_Tail_Schedule to confirm.
4. The pack writes the `affected_partners` and `non_beneficiary_reviewer` fields into the X4 Decision_Log and the `firm/klarna-tests/KT-YYYY-NNN.md` page.
5. The pack does **not** score the Klarna Test itself — humans score, per `governance/KLARNA-TEST.md`. The pack only sets up the scoring artefact.

### 4.8 Dispute initiation

When a partner ticks the dispute box on a variable statement:

1. R3's poll detects the box state change; it sets `sign_off_status='partner_disputed'` and notifies the founder via Slack/dMail.
2. The pack opens a Tier-1 dispute record at `firm/compensation/YYYY-MM/disputes/D-YYYY-NN-NNN.md` per `templates/brain/dispute-record.md`.
3. The dispute record links to the disputed variable statement, the underlying X1 rows, and the partner's X2 reward-species declaration.
4. The pack does **not** resolve the dispute — that's the Tier-1 / Tier-2 / Tier-3 flow in `governance/DECISION-RIGHTS.md`. The pack's role is to surface the dispute and lock the variable until resolved (no `founder_approved` flip allowed while a dispute is open).

### 4.9 Anomaly surfacing

The pack runs three anomaly checks each time it's invoked:

1. **Zero-output partner** — a full-time partner with zero captured outputs for >3 consecutive days. Surface in the next R1 daily summary and the next BR's agenda.
2. **Spike in `rework_within_30d`** — a partner whose rework_flagged-rate exceeds 25% of their captured outputs in a rolling 30-day window. May indicate (a) the partner's environment is broken, (b) the output_type classification is being mis-applied, or (c) a real quality issue. Surface to the founder.
3. **Variable pay outlier** — a partner whose monthly variable is >2σ from their 6-month rolling average (high or low). Surface to founder + partner.

Each anomaly becomes a Brain note at `firm/anomalies/YYYY-MM-DD-<partner_id>-<type>.md`.

### 4.10 Value-tier rubric

Four tiers, with concrete examples per `output_type`:

| Tier | Envelope (Gen 1) | What it looks like (engineering) | What it looks like (sales) | What it looks like (legal/contract) |
|---|---|---|---|---|
| **S** (flagship) | €8,000 | Major feature shipping with measurable customer impact (e.g. a new product surface, a 6-week build) | A landed deal with a Tier-1 customer or a multi-year ARR commitment | A successfully negotiated foundational contract (e.g. master services agreement, SaaS resale agreement) |
| **M** (significant) | €2,000 | A feature improving an existing surface; a substantial refactor; a new dashboard | A landed deal with a standard customer in expected cycle | A standard customer contract execution; a funding term sheet redline |
| **L** (standard) | €500 | A typical 1-3 day commit; a documented design choice; a code review with substantive feedback | An expanded SOW; a meaningful customer touch that progresses pipeline | A routine vendor agreement; an NDA execution |
| **XS** (maintenance) | €100 | Bug fix; dependency bump; small refactor; PR review of routine changes | A pipeline-tracking touch (call notes, follow-up email) | A routine document review (signed-off, no negotiation) |

Firms calibrate the envelope to their business: a SaaS firm and a consultancy will set very different absolute numbers. The framework recommends keeping the **ratio** (XS:L:M:S = 1:5:20:80) approximately constant — that's the framework's opinion on what relative effort/value differences look like.

The value tier is set at Output Spec drafting time and **refined as outcomes come in**. A drafted-as-M output that lands and produces an S-level outcome at Q+1 is *kept M for variable* (variable pays on output, not outcome) and *recorded as S in long-tail* (long-tail pays on outcome). This separation is the framework's mechanism for paying for shipping AND paying for compounding without double-counting.

---

## Brain interaction protocol

**Reads:**
- `firm/partners/<id>/profile.md`, `reward-species-declaration.md`, `output-specs/*` — at every invocation.
- `firm/output-logs/*` — for monthly aggregation.
- `firm/decisions/*` — for renegotiation history.
- `firm/klarna-tests/*` — for Klarna interaction (writes too).

**Writes:**
- `firm/partners/<id>/variable-statements/*` — monthly.
- `firm/partners/<id>/long-tail-statements/*` — quarterly.
- `firm/output-logs/*` — daily (via R1).
- `firm/compensation/<month>/founder-approval.md` — monthly.
- `firm/compensation/<month>/disputes/*` — on dispute initiation.
- `firm/anomalies/*` — on anomaly detection.

Wikilink discipline: every Brain page this pack writes references existing slugs (X1 row indexes, X2 sheet rows, X4 test_ids); the pack must not invent wikilinks.

---

## Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X1 partner-output-ledger.xlsx | Output_Log | Append | R1 daily |
| X1 | Output_Log column I (rework_within_30d) | Update on prior rows | R1 retroactive detection |
| X1 | Monthly_Variable | Write | R3 monthly |
| X1 | Partner_Multipliers_Snapshot | Refresh | R3 monthly |
| X2 reward-species-declaration.xlsx | Partner_Profile, Base_Variable_Split | Write at onboarding | Manual via 4.1 |
| X2 | Long_Tail_Schedule | Append on long-tail eligibility | Manual via 4.5 |
| X2 | Long_Tail_Schedule | Update `total_settled_to_date` | R4 quarterly |
| X2 | Renegotiation_Log | Append | Manual via 4.1 renegotiation flow |
| X4 klarna-test.xlsx | Decision_Log, Klarna_Score | Write | R7 trigger via 4.7 |

The pack never modifies X3 (business-review), X5 (METR baseline), X6 (agent-skill-roi), X7 (EU AI Act), X8 (treasury), X9 (readiness) — those are owned by S5, S6, S6, S7, S10, founder respectively.

---

## Routine integration

This pack is invoked by:
- **R1** (daily output capture) — the pack provides §4.3.
- **R3** (monthly variable calc) — the pack provides §4.4.
- **R4** (quarterly long-tail settlement) — the pack provides §4.5.
- **R7** (Klarna Test trigger) — the pack provides §4.7 (affected-partner identification + non-beneficiary selection).

The pack is also invoked manually for: §4.1 (onboarding/renegotiation), §4.2 (output spec drafting), §4.6 (annual bonus), §4.8 (dispute initiation).

---

## Don'ts

1. **Don't compute variable pay without monthly human sign-off** — the calculator is advisory; the founder pays.
2. **Don't override a partner's Reward Species Declaration** without signed renegotiation — the declaration is contractual.
3. **Don't aggregate output across partners** in ways that obscure individual attribution.
4. **Don't treat AI-generated commits as equivalent** to human-written ones for attribution; track AI-vs-human authorship via `Co-authored-by:` trailers and the `ai_authored_pct` field. The framework's discipline is rework-within-30d zero-outs, not ai-pct discount; do not change this without an ADR.
5. **Don't bypass the Klarna Test** when a Skill rollout would replace a partner's primary function. The Routine R7 enforces; do not work around it.
6. **Don't retroactively recompute closed-month variable pay** — the month-locked flag exists for this reason.
7. **Don't pay variable pay through any mechanism that bypasses the Brain audit trail** — every payment must reference its `firm/partners/<id>/variable-statements/<month>.md` page.
8. **Don't open a Tier-1 dispute** without first surfacing in conversation with the affected partner. The dispute is the formal step; conversation comes first.
9. **Don't compute long-tail without a written attribution methodology** for the outcome metric. Vague "this contract generated revenue" is not enough; the X2 Long_Tail_Schedule entry must specify the metric.

---

## Quick reference

| Situation | Action | Output lands at |
|---|---|---|
| Onboard a new partner | Run §4.1 initial declaration | X2 sheet + `firm/partners/<id>/reward-species-declaration.md` + signed PDF |
| Daily ledger capture | R1 fires; §4.3 runs automatically | X1 Output_Log + `firm/output-logs/<date>.md` |
| Detect rework on prior commit | R1 detection rule fires; §4.3 step (f) | X1 row column I flips to "Yes" |
| Monthly variable | R3 fires; §4.4 runs | X1 Monthly_Variable + per-partner statement Brain page + founder packet |
| Partner ticks "dispute" | R3 detects; §4.8 opens dispute record | `firm/compensation/<month>/disputes/<id>.md` |
| New long-tail-eligible output | Manual at next BR; §4.5 entry | X2 Long_Tail_Schedule row + Output Spec cross-link |
| Quarterly settlement | R4 fires; §4.5 settlement runs | Per-partner long-tail statement + X2 update |
| AI replaces partner function (PR labelled) | R7 fires; §4.7 sets up scoring | X4 Decision_Log + `firm/klarna-tests/<id>.md` |
| Reward species renegotiation | §4.1 renegotiation flow | X2 Renegotiation_Log + new signed PDF + decision record |
| Annual bonus | §4.6 once per year (Jan typical) | Per-partner annual-bonus Brain page |

---

## Worked examples concept

The pack's `examples/` folder ships with **four worked examples**:

1. **First-month onboarding + first variable**. New partner Mira joins on 2026-03-15. Reward species: hybrid 60/30/10. Base €30k. Output multiplier 1.0. By 2026-03-31 she has shipped 4 outputs (1 M, 2 L, 1 XS). Monthly_Variable computation walked through end-to-end, including the proration of the half-month base and the variable pay computation showing each row's contribution. The final statement Brain page is shown verbatim. The example also shows what happens if Mira ticks "dispute" — the resulting Tier-1 dispute record is included.
2. **A long-tail entitlement that compounds**. Partner ships a contract worth €120,000 ARR; long-tail is 8% over 3 years; the example walks through Q1, Q2, Q3, Q4 statements showing the cumulative `total_settled_to_date` and the final-quarter check that the contract is still active.
3. **A retroactive rework zero-out**. R1 detects on day 22 that day-3's commit was reverted/redone; the example shows the Brain audit entry, the X1 row update, the next monthly variable statement showing the prior-month zero-out as a line item.
4. **A Klarna trigger walk-through**. A PR labelled `ai-replaces-human`; this pack's role: identify the affected partner (cross-reference Output Specs against the PR's automated capability), pick the non-beneficiary reviewer (read X1 Monthly_Variable rolling-90-day), set up the X4 row + Brain page. The actual Klarna scoring (humans) happens in S6's worked example.

---

## References

1. **Yolo Investments** (Tim Maslyukov). *Stop paying for hours. Start paying for output.* (May 2026). The seven-layer compensation framing the pack operationalises.
2. **Levin, J. & Tadelis, S.** *Profit Sharing and the Role of Professional Partnerships* (Stanford GSB working paper, 2005). The empirical case for partnership structures in human-capital-intensive production.
3. **Ressler, C. & Thompson, J.** *Why Work Sucks and How to Fix It* (Penguin, 2008). The ROWE framework's authoritative source.
4. **MHPR Advisors.** *Reward Species Typology* — the seven partnership reward models. (Industry working paper, 2023.)
5. **Hope, J. & Fraser, R.** *Beyond Budgeting: How Managers Can Break Free from the Annual Performance Trap* (Harvard Business School Press, 2003).
6. **Weitzman, M. L.** *The Share Economy: Conquering Stagflation* (Harvard University Press, 1984). The macroeconomic case for share/profit-sharing compensation.
7. **MBO Partners.** *State of Independence in America 2025*. (Industry report, 2025.) — for the gig-economy framing in `MANIFESTO.md`.
8. **DORA Report 2025.** *State of AI-Assisted Software Development*. — for the centaur-pattern context in §4.10's value-tier examples.
9. ØØT `MANIFESTO.md`, Thesis 3 — Employees become Partners.
10. ØØT `governance/KLARNA-TEST.md`.
11. ØØT `governance/DECISION-RIGHTS.md` — the dispute resolution flow.
12. ØØT `templates/excel/SPEC.md` — X1, X2, X4 schemas the pack relies on.

---

## Acceptance criteria for the eventual SKILL.md

Standard structure (all sections from `_TEMPLATE_SKILL.md`). Plus:

- The seven-layer compensation picture (§"layers" table) is reproduced verbatim with Gen 1 / 2 / 3 markers.
- The Klarna Test interaction (§4.7) is wired and references R7 explicitly.
- The value-tier rubric (§4.10) includes concrete examples per output_type for at least three role categories (engineering, sales, legal).
- The cross-workbook discipline (X1.J written at row-append, not formula) is explicit in §4.3.
- The retroactive rework rule reference (`routines/SPEC.md` R1) is explicit.
- 4 worked examples in `examples/` (variable, long-tail, retroactive zero-out, Klarna trigger).
- 12+ references with at least 5 academic / institutional sources.
- Frontmatter passes the Phase 8 linter.
