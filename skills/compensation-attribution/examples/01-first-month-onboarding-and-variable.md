# Example 1 — First-month onboarding + first variable pay

A complete worked example of S3 from partner-signs-on through their first variable-pay statement landing.

## The setup

- **Partner:** Mira Tek (`mira-tek`).
- **Cohort:** full-time partner.
- **Jurisdiction:** SI (Slovenia).
- **Reward species:** hybrid — variable_weight_personal=0.6, variable_weight_team=0.3, variable_weight_company=0.1.
- **Base:** €30,000 / year (€2,500 / month).
- **Output multiplier:** 1.0.
- **Stablecoin upgrade preference:** Yes (activates in Gen 2).
- **Two Worlds of Code:** agentic-engineer.
- **Start date:** 2026-03-15 (mid-month).

## Step 1 — Onboarding (the 90-min session)

The founder + Mira run §4.1 of S3:

1. Open `templates/excel/reward-species-declaration.xlsx`.
2. Add sheet `mira-tek`.
3. Populate Partner_Profile and Base_Variable_Split per the values above.
4. Validate: 0.6 + 0.3 + 0.1 = 1.0 ✓; bonus_split sum = 1.0 ✓ (default 1/3 each).
5. Generate signed PDF; store at `firm/partners/mira-tek/legal/reward-species-2026-03-15.pdf`.
6. Compile Brain summary at `firm/partners/mira-tek/reward-species-declaration.md`.
7. Both sign. The first decision in the partnership: D-2026-007 — *"Onboard Mira Tek as full-time partner per attached declaration."*

## Step 2 — March outputs (16 days of work)

R1 captures Mira's outputs from 2026-03-15 → 2026-03-31:

| Date | output_type | output_ref | output_spec_ref | value_tier | ai_pct | rework? | computed_variable |
|---|---|---|---|---|---|---|---|
| 2026-03-18 | pr_merged | gh:1234 | `[[partners/mira-tek/output-specs/2026-03-15--login-flow]]` | M | 30% | No | €2,000 |
| 2026-03-22 | pr_merged | gh:1247 | `[[partners/mira-tek/output-specs/2026-03-20--auth-tests]]` | L | 5% | No | €500 |
| 2026-03-25 | review_completed | gh:1251 | (no spec — review work) | L | 0% | No | €500 |
| 2026-03-30 | pr_merged | gh:1268 | `[[partners/mira-tek/output-specs/2026-03-28--session-fix]]` | XS | 0% | No | €100 |

Total outputs: 4. Total variable: €3,100.

## Step 3 — Monthly variable calculation (R3 fires 2026-04-01 09:00)

§4.4 runs:

1. Lock March Output_Log.
2. Verify rework flags current — none flagged.
3. Aggregate for `mira-tek`: total_outputs=4, total_variable=€3,100.
4. Read X2: base_amount=€30,000, multiplier=1.0.
5. Compute base_pay (calendar-day proration): 17 days / 31 days × €2,500 = **€1,371.**
6. Total compensation: €1,371 + €3,100 = **€4,471.**
7. Generate `firm/partners/mira-tek/variable-statements/2026-03.md`:

```markdown
---
title: "Variable pay statement — Mira Tek — 2026-03"
type: variable-statement
partner_id: mira-tek
month: 2026-03
total_compensation: 4471.00
ack_status: pending
---

# Variable pay statement — March 2026

| Component | Amount |
|---|---:|
| Base (proportional, 17/31 days) | €1,371 |
| Variable | €3,100 |
| **Total** | **€4,471** |

## Top 4 outputs by computed_variable

- 2026-03-18 — pr_merged — gh:1234 — value tier `M` — €2,000 — [[partners/mira-tek/output-specs/2026-03-15--login-flow]]
- 2026-03-22 — pr_merged — gh:1247 — value tier `L` — €500 — [[partners/mira-tek/output-specs/2026-03-20--auth-tests]]
- 2026-03-25 — review_completed — gh:1251 — value tier `L` — €500 — *(no spec — review work)*
- 2026-03-30 — pr_merged — gh:1268 — value tier `XS` — €100 — [[partners/mira-tek/output-specs/2026-03-28--session-fix]]

## Acknowledgement

- [ ] I have reviewed this statement and agree with the calculation.
- [ ] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).
```

8. Mira receives an email/dMail with the link.
9. R3 polls the page once daily.

## Step 4 — Mira disputes (variant of the example)

Mira reads the statement and notices that her 2026-03-25 review work was tagged `L` but she actually did three substantive reviews that day, each independently substantive. She thinks the tier should be `M`.

She edits the Brain page:

```markdown
- [ ] I have reviewed this statement and agree with the calculation.
- [x] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).
```

She commits with a commit message: *"Variable dispute: 2026-03-25 review tier should be M."*

Within 24 hours, R3's poll detects the change. `sign_off_status` flips to `partner_disputed`. Founder is notified via Slack `#compensation`. The pack opens a Tier-1 dispute record:

```markdown
---
title: "Dispute D-2026-03-001 — Mira Tek — 2026-03 variable"
type: dispute
dispute_id: D-2026-03-001
tier: 1
raised_by: mira-tek
against: founder-tali
status: open
---

# Tier-1 dispute — variable pay calculation 2026-03

**Raised:** 2026-04-02 by [[partners/mira-tek]]
**Against:** [[partners/founder-tali]] (Accountable for variable pay per DECISION-RIGHTS matrix)
**Disputed item:** 2026-03-25 review work — partner argues `M` not `L`.

**Linked artefacts:**
- Disputed statement: [[../variable-statements/2026-03]]
- Underlying X1 row: OL-20260325-003
- Reward Species Declaration in effect: [[../reward-species-declaration]]

**Tier 1 procedure:** founder + partner discuss within 5 business days; outcome documented here.
```

## Step 5 — Resolution (Tier 1)

Founder + Mira meet for 30 min. Founder agrees the review work was substantive — 3 independent reviews, each at the depth of a `L`-tier output. Compromise: keep one row at L, append two more rows for the additional reviews. Net effect: +€1,000 to Mira's March variable.

The dispute record is updated:

```markdown
status: resolved
resolution_date: 2026-04-04
resolution_summary: "Founder agrees the review work was 3 substantive reviews, not 1. R1 backfills 2 additional L-tier rows. Net +€1,000 to variable. No compromise on tier upgrade — the L-tier classification of each individual review stands; the count was the issue."
```

X1 gets two backfill rows. The March variable statement is regenerated (with `ack_status` reset to pending). Mira ticks the agree box. Founder approves. Total: €5,471.

## What this example demonstrates

- The full §4.1 → §4.3 → §4.4 → §4.8 flow, end-to-end.
- The Brain checkbox acknowledgement mechanism in action.
- The Tier-1 dispute flow resolving cleanly.
- The framework's discipline that **tier classification stays even when count is corrected** — disagreements are about facts, not fudging.
- The audit trail at every step (commits, Brain pages, X1 rows, dispute record).
