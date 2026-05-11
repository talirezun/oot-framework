# Monthly operations — agent-runnable playbook

**Audience:** Founder, 1st of the month + over the next 5 business days for partner acknowledgement polling.
**Read by:** the founder's coding agent.

> 🚀 **One-line prompt to feed your agent:**
>
> ```
> Read installer/agent-assisted/MONTHLY-OPS.md and execute the monthly variable-pay flow for my firm at <FIRM_FOLDER>. Read ~/.oot/firm-state.yaml for context.
> ```

---

## Agent: what to do, in order

### 1. Run daily-ops first

Execute [`DAILY-OPS.md`](DAILY-OPS.md) Steps 1-4. Verify the bot is signing commits and GitHub auth is healthy.

### 2. Check R3's monthly variable calc landed

R3 fires the 1st of the month at 09:00 (firm timezone). By Day-1 evening / Day-2 morning, expect:

- New row in `firm/excel/partner-output-ledger.xlsx` Monthly_Variable for last month (per partner).
- Per-partner statement at `firm/partners/<id>/variable-statements/<YYYY-MM>.md` (last month).
- Founder-approval packet draft at `firm/compensation/<YYYY-MM>/founder-approval.md`.
- Email notification to each partner.

```bash
LAST_MONTH=$(date -v-1m +%Y-%m 2>/dev/null || date -d 'last month' +%Y-%m)
ls firm/partners/*/variable-statements/${LAST_MONTH}.md
```

If R3 hasn't fired (no statements present) by Day-2 morning: surface to the user; check the Routine run log.

### 3. Summarise the founder-approval packet

Read `firm/compensation/<YYYY-MM>/founder-approval.md` (if present). Walk the founder through:
- Total variable pool for the month
- Per-partner totals + the value-envelope tier mix
- Any retroactive `rework_within_30d` zero-outs from prior months that affected this month
- Anomalies (a partner with zero output for >3 consecutive weeks; an unusually high-value tier captured without an Output Spec)

Offer to open the file in their text editor for review.

### 4. Acknowledgement polling (days 1-5)

R3's design is: founder doesn't approve until partners acknowledge (5 business day window). The framework's discipline is **Brain checkbox** (not Slack reaction) per CLAUDE.md decision #5.

For each partner statement at `firm/partners/<id>/variable-statements/<YYYY-MM>.md`, parse the acknowledgement block:

```markdown
## Acknowledgement
- [ ] I have reviewed this statement and agree with the calculation.
- [ ] I dispute the calculation (open Tier 1 dispute per governance/DECISION-RIGHTS.md).
```

Map to sign_off_status (per CLAUDE.md decision and R3 spec):

| Detected state | sign_off_status |
|---|---|
| First box ticked, second unticked | `partner_reviewed` |
| Second box ticked, first unticked | `partner_disputed` (escalates to Tier 1; do NOT advance to founder_approved) |
| Both ticked | `partner_disputed` (ambiguous intent; treat as dispute, ask partner to clarify) |
| Neither ticked, ≥5 business days since send | `partner_unresponsive` (escalate to founder; never auto-approve) |
| Neither ticked, <5 business days | `draft` (no change) |

Update `firm/excel/partner-output-ledger.xlsx` Monthly_Variable's `sign_off_status` column for each partner with a state change. **This is a Pattern C write** — the agent does it via openpyxl in code execution + signed commit + push.

(Note: R3 itself does this polling on a daily-fires schedule on cloud track. The agent's role is to summarise the state to the founder, not to redo R3's work. If R3 is firing correctly, the state is already up-to-date in X1; you just read it.)

### 5. Founder approval (day 5 or once all partners have acknowledged)

When all partners are `partner_reviewed` (or after the 5-day window with `partner_unresponsive` for any non-responders), prompt the founder:

> "All 3 partners have acknowledged. Variable pool: €<X>. Open `firm/compensation/<YYYY-MM>/founder-approval.md` for the full packet. Sign off?"

The founder edits the founder-approval.md file to add a sign-off section with their name + date. The agent helps with this:

```markdown
## Founder approval

**Approved by:** <founder name>
**Approval date:** <YYYY-MM-DD>
**Notes:** <anything the founder wants to capture>

This packet is approved for payment. Payment processing proceeds via the firm's
existing payroll / SEPA / wire flow (manual in Gen 1; stablecoin in Gen 2).
```

Help the founder commit + sign + push this.

After founder approval, update X1 Monthly_Variable's `sign_off_status` column to `founder_approved` for each partner row. Pattern C write.

### 6. Disputes (if any)

If any partner is in `partner_disputed` state: do NOT advance to founder_approved. Instead:

- Open the partner's variable-statements page; help the founder draft a response.
- Reference [`governance/DECISION-RIGHTS.md`](../../governance/DECISION-RIGHTS.md) Tier 1 dispute resolution flow.
- Schedule a 30-min call between founder + partner + non-beneficiary reviewer.
- Once resolved: the partner re-ticks the first box (review) or amends the dispute documentation.

Disputes are normal in Gen 1 — the discipline is to handle them transparently. Per CLAUDE.md decision #5 the audit trail is in the Brain page, not in Slack.

### 7. Quarterly long-tail (every 3 months)

If today is the 1st of a quarter (1 Jan / 1 Apr / 1 Jul / 1 Oct), R4 also fired. Walk through analogous to R3 but for long-tail entitlements at `firm/partners/<id>/long-tail-statements/<YYYY-Qn>.md`.

### 8. Update firm-state file

```yaml
last_monthly_run: <YYYY-MM>
monthly_observations: |
  - R3 variable calc: <fired ok | failed | ...>
  - <N> partners; total variable: €<X>
  - <K> disputes pending
  - <Y> partners acknowledged; <Z> unresponsive
```

---

## What this playbook does NOT do

- Approve the founder-approval packet on the founder's behalf. Approval is human-only.
- Move money. Payment processing runs through the firm's existing payroll flow.
- Resolve disputes. The framework's dispute discipline (Tier 1 / Tier 2 / Tier 3 per DECISION-RIGHTS.md) is human-driven.
- Generate compensation. R3 generates the draft; founder reviews and approves; payroll executes.

---

## See also

- [`DAILY-OPS.md`](DAILY-OPS.md) — daily sync
- [`WEEKLY-OPS.md`](WEEKLY-OPS.md) — Friday BR + Sunday brain-health
- [`routines/cloud/R3.md`](../../routines/cloud/R3.md) — R3 spec + acknowledgement polling
- [`routines/cloud/R4.md`](../../routines/cloud/R4.md) — R4 quarterly long-tail spec
- [`governance/DECISION-RIGHTS.md`](../../governance/DECISION-RIGHTS.md) — Tier 1/2/3 dispute resolution
- [`CLAUDE.md`](../../CLAUDE.md) decision #5 — partner acknowledgement is Brain checkbox, not Slack reaction
