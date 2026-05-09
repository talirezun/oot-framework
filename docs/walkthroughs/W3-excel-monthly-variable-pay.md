# W3 — Excel: Monthly Variable Pay Sign-off

**Audience:** Founder doing the monthly variable-pay review.
**Time:** 30-60 minutes per partner per month (most months — fast; first month with a new partner — slower).
**You will end with:** every partner's variable pay statement reviewed, founder-approved, and executed via the firm's banking partner.

> 📖 **Concept doc:** [`docs/04-running-the-business-review.md`](../04-running-the-business-review.md). **Skill Pack:** [`skills/compensation-attribution/SKILL.md`](../../skills/compensation-attribution/SKILL.md).

---

## What this is + the first 5 minutes

On the 1st of each month at 09:00, Routine R3 fires:
1. Locks the previous month's `Output_Log` (X1).
2. Aggregates per-partner variable pay.
3. Writes per-partner statement Brain pages.
4. Sends each partner email/dMail with a link.
5. Polls the partner's Brain page once daily for the acknowledgement checkbox.

**Your job (founder):** review the calculation, verify it's correct, approve payment.

---

## Step 0 — Context: what just happened

Last night R3 fired. Open Slack `#compensation`:

> Monthly variable drafts for 2026-04 are ready. 8 partners. Total: €38,400. Review window: 5 business days. Founder approval required before payment.

Open `templates/excel/partner-output-ledger.xlsx`. Navigate to the **Monthly_Variable** sheet.

![Monthly_Variable sheet showing per-partner rows for 2026-04](../images/W3-1-monthly-variable.png)

*The sheet has one row per partner per month. Each row's `total_compensation` (column F) = `total_variable` (D) + `base_pay` (E). `sign_off_status` (G) is `draft` for all rows initially.*

---

## Step 1 — Inspect the four columns that matter

For each partner row, four columns matter most:

| Column | Name | What you check |
|---|---|---|
| C | total_outputs | Does it match what you remember the partner shipping this month? |
| D | total_variable | Is it consistent with the partner's recent average? |
| E | base_pay | Is the base correct (matches their X2)? |
| F | total_compensation | The sum. |

If any of these looks materially off, drill into the Output_Log.

---

## Step 2 — Drill into a partner's outputs

1. Open the **Output_Log** sheet (X1's first sheet).
2. Filter to the closed month (e.g. `B` = 2026-04-*).
3. Filter further to the partner (`C` = `<partner_id>`).
4. Spot-check:
   - Are there outputs with `value_tier=S` that look like XS jobs?
   - Are there `value_tier=L` outputs that should have been M (the partner's complaint vector)?
   - Any rows with `rework_within_30d=Yes` (which zeroes out `computed_variable`)?

![Output_Log filtered to one partner, one month](../images/W3-2-filtered-output-log.png)

*Filter UI: each column header has a filter arrow. Click → set value. Multiple filters AND together.*

> 💡 **The most common scrutiny target:** a partner's value_tier S claim. Ask "what was the expected outcome from the Output Spec? Has it landed?" If the outcome hasn't yet materialised, the tier is provisional.

---

## Step 3 — Read the partner's Brain statement

Open the partner's `firm/partners/<id>/variable-statements/2026-04.md` page in your markdown viewer (Obsidian, the Curator app, or Claude Desktop).

The page shows:
- Total compensation (matches X1).
- Top 5 outputs by `computed_variable`.
- Any retroactive zero-outs from prior months affecting this month's pool.
- The acknowledgement block (checkboxes).

![Brain variable statement page open in Obsidian](../images/W3-3-statement-obsidian.png)

*The Acknowledgement section at the bottom has two checkboxes: "I agree" and "I dispute".*

---

## Step 4 — Read the partner's acknowledgement

Has the partner ticked the agree box, the dispute box, or neither?

| State | Meaning | Your action |
|---|---|---|
| Agree ticked | Partner accepts the calculation | Proceed to founder approval (Step 5) |
| Dispute ticked | Partner disputes; Tier-1 dispute opens automatically | Halt approval; engage in Tier-1 conversation per [`governance/DECISION-RIGHTS.md`](../../governance/DECISION-RIGHTS.md) |
| Both ticked | Ambiguous | Treat as dispute; ask the partner to clarify |
| Neither, ≥5 business days | Partner unresponsive | Founder makes a call: pay anyway with a documented note, or hold + escalate |
| Neither, <5 business days | Partner has time | Wait |

> ⚠️ **Slack reactions are NOT canonical.** Per the framework's design, only the Brain checkbox counts. This makes the audit trail self-contained in the Brain.

---

## Step 5 — Approve in the spreadsheet

For each partner row in `Monthly_Variable`:

1. Change column G (`sign_off_status`) from `partner_reviewed` to `founder_approved`.
2. Set column H (`approval_date`) to today.
3. Save.

The provisioning script's auto-generated founder-approval packet at `firm/compensation/2026-04/founder-approval.md` shows the structured payment list.

![Setting sign_off_status to founder_approved](../images/W3-4-founder-approved.png)

*Use the dropdown in column G; the data validation provided by the spreadsheet's `oot-build-excel` generator allows only specific values.*

---

## Step 6 — Trigger payment (Gen 1 manual)

ØØT v1.0 is FIAT-default. Payment execution is manual via your banking portal.

1. Open the founder-approval packet at `firm/compensation/2026-04/founder-approval.md`. It has the structured payment list:

   ```
   - jane-doe — €4,471 — IBAN SI56... — ref "ØØT 2026-04 variable + base"
   - john-smith — €5,200 — IBAN HR93... — ref "ØØT 2026-04 variable + base"
   ...
   ```

2. Open your banking portal (Revolut Business, Wise, your local bank, etc.).
3. Initiate SEPA transfers (EU) or wires (international).
4. After execution, return to `Monthly_Variable` sheet:
   - Column I (`payment_date`): set to today.
   - Column G: optionally update to `paid` (terminal status).

> 💡 **Generation 2:** stablecoin payroll via Rise / Circle automates this step entirely. R3 invokes Rise's API after founder approval. See [`GENERATIONS.md`](../../GENERATIONS.md).

---

## Step 7 — Commit (the audit trail)

After all partners are paid:

1. Save the X1 spreadsheet.
2. Commit the changes via signed git commit.
3. The R6 audit trail Routine (firing tonight at 23:00) will log this batch's compensation events.

---

## Common pitfalls

**1. A partner's Reward Species Declaration changed mid-month.**
- The first calculation may produce a split-month result (15 days under old terms, 15 days under new). The X2 Renegotiation_Log is the source of truth.
- The variable statement template (`templates/brain/variable-statement.md`) handles split-month correctly when R3's prompt generates the page.

**2. A retroactive `rework_within_30d` zero-out from a prior month appears.**
- Per the framework's discipline, closed-month variable does NOT retroactively recompute. The retroactive zero-out shows up as a "prior-month zero-out line item" in the current month's statement (audit-only, no payment effect).
- Don't try to claw back already-paid amounts.

**3. The `partner_multiplier` (X1.J) doesn't match the partner's X2.**
- Cause: the Routine wrote a stale value at row-append (the partner's X2 changed since).
- Fix: R3's `Partner_Multipliers_Snapshot` refresh should have caught this. If not, manually update X1.J for the affected rows; recompute column L.

**4. A partner ticks both boxes ("agree" and "dispute").**
- Treat as dispute (the framework's discipline: ambiguity goes to the partner-protective interpretation).
- Open a Tier-1 dispute conversation; ask the partner to clarify intent.

**5. A founder approves a partner-disputed row.**
- The framework's discipline: don't. The dispute resolution flow exists for a reason.
- If you genuinely disagree with the dispute, escalate to Tier 2 per `governance/DECISION-RIGHTS.md`.

---

## What's next

- **[W4 — Running the Friday BR](W4-running-the-friday-business-review.md)** — the weekly heartbeat that catches issues before they accumulate to monthly disputes.
- **[W5 — Running a Klarna Test](W5-running-a-klarna-test.md)** — the discipline that gates AI-replaces-human decisions.
