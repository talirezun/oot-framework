# W6 — Monitoring the Routines Dashboard

**Audience:** Founder or designated ops partner.
**Time:** 60 seconds daily; 5 min weekly; 15 min monthly.
**You will end with:** confidence that the framework's automation is healthy and a clear escalation path when it isn't.

> 📖 **Concept doc:** [`routines/README.md`](../../routines/README.md). **Per-Routine specs:** [`routines/cloud/<R>.md`](../../routines/cloud/) and [`routines/privacy/<R>.md`](../../routines/privacy/).

---

## What this is + the first 5 minutes

The framework's 8 Routines run on schedule. **Failures should not be silent.** Your monitoring job:

| Cadence | Time | What |
|---|---|---|
| Daily | 60 seconds | `#output-log` + `#brain-health` confirms R1 ran yesterday and R5 ran on Sunday. |
| Weekly (Friday after BR) | 5 min | `business-review.xlsx` populated; `agent-skill-roi.xlsx` reviewed for week's spend. |
| Monthly (1st of month, after R3) | 15 min | Founder-approval packet exists; partner statements sent; X8 runway check (if applicable). |

---

## Cloud track — the Anthropic Routines dashboard

### Where it is

In Claude Desktop: **Settings → Routines**. Or directly at `claude.com/routines`.

### What you'll see

![Anthropic Routines dashboard with 4 active routines](../images/W6-1-anthropic-dashboard.png)

*The dashboard lists each Routine with: status (green = healthy, amber = warning, red = failed), last-run timestamp, next-scheduled timestamp, and a per-Routine drilldown.*

### Daily check-in (60 seconds)

1. Open the dashboard.
2. Glance at all listed Routines. Each should show "last run: yesterday" with a green status (R1, R6) or "last run: this week" (R5 weekly, R2 weekly).
3. If any shows a red status: click into it; read the run log; address.
4. Close.

### Weekly check-in (5 min)

After the Friday BR (so X3 is populated):

1. Open `business-review.xlsx`. Confirm R2 populated this week's row.
2. Open `agent-skill-roi.xlsx`. Check the week's total cost in Agent_Costs sheet.
3. If cost is materially higher than last week: investigate. Most common cause: a partner ran an exploratory chain in Claude Desktop that consumed many tokens.

### Monthly check-in (15 min)

After R3 fires on the 1st:

1. Confirm `firm/compensation/<month>/founder-approval.md` exists.
2. Spot-check 2-3 partner statements at `firm/partners/<id>/variable-statements/<month>.md`.
3. Review X6 ROI_Calc sheet: any Skill Pack with `roi_multiple < 1.0` for two consecutive months is a signal — that Skill is costing more than the value it produces. Surface at the next BR.
4. If X8 is populated (Unit Fund firm): R8 fired Monday; check Runway_Calc sheet. Runway_months > 9, reserve_coverage_ratio > 1.0.

---

## Privacy track — the always-on machine + cron logs

### Where the logs live

`~/oot-framework/logs/` on the always-on machine. One log file per Routine: `r1.log`, `r2.log`, `r5.log`, `r6.log`.

### How to tail (macOS / Linux)

```bash
ssh oot@always-on-machine.local
tail -f ~/oot-framework/logs/r1.log
```

(Or use Tailscale to get to the machine remotely.)

### What a successful R1 run looks like

```
2026-04-15 17:59:58 — startup OK
2026-04-15 18:00:00 — connecting to LM Studio MCP host (localhost:1234)
2026-04-15 18:00:01 — connected. Loaded skills: compensation-attribution, my-curator
2026-04-15 18:00:02 — reading GitHub commits past 24h via github-mcp
2026-04-15 18:00:08 — found 14 commits across 3 partners
2026-04-15 18:00:10 — reading 4thtech dChat past 24h
2026-04-15 18:00:15 — found 2 #output tags
2026-04-15 18:00:17 — appending 16 rows to X1 Output_Log via excel-mcp
2026-04-15 18:00:23 — writing daily summary to firm/output-logs/2026-04-15.md
2026-04-15 18:00:26 — committing signed commit to Brain repo
2026-04-15 18:00:29 — posted summary to 4thtech dChat #output-log
2026-04-15 18:00:30 — done. duration: 32s.
```

### What a failed R1 run looks like

```
2026-04-12 17:59:58 — startup OK
2026-04-12 18:00:00 — connecting to LM Studio MCP host (localhost:1234)
2026-04-12 18:00:00 — ERROR: connection refused
2026-04-12 18:00:30 — retry 1/3 failed: connection refused
2026-04-12 18:01:00 — retry 2/3 failed: connection refused
2026-04-12 18:01:30 — retry 3/3 failed: connection refused
2026-04-12 18:01:30 — fatal: aborting after 3 retries
```

### Daily check-in (60 seconds)

1. Open 4thtech dChat `#output-log` on your laptop. Yesterday's R1 summary should be visible.
2. Open `#brain-health`. Sunday's R5 summary visible (if it's Monday-Friday, last Sunday's; if Saturday, last week's).
3. If summary missing: SSH into the always-on machine, tail the relevant log.

---

## What "broken" looks like — the four most common failure modes

### Failure 1: R1 missed a day

**Symptom:** no `firm/output-logs/<yesterday>.md`. No `#output-log` post.

**Diagnostic:**
- Cloud: Anthropic Routines dashboard shows red for that day.
- Privacy: `tail ~/oot-framework/logs/r1.log` shows error or absence of run.

**Recovery:**
- Cloud: re-fire from dashboard ("Run now"). The Routine is idempotent (keyed on date).
- Privacy: `llmster --backfill 2026-04-12 --skill compensation-attribution --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r1.prompt.md`.

**Document the gap:** create `firm/privacy-track/troubleshooting/<date>-r1-missed.md` (privacy track) or `firm/decisions/D-...-r1-incident.md` (cloud track) with: cause, recovery action, prevention.

### Failure 2: R6 audit log gap

**Symptom:** no `firm/audit-logs/<yesterday>.md`. The Article 12 record-keeping has a hole.

**Recovery:**
- Backfill via the same pattern: `llmster --backfill <date> --skill governance-compliance ...`.
- The R6 prompt's discipline: an empty day is a *noted "no agent activity"* entry, not a missing day. R6 produces this automatically when no decisions were logged.

**This failure is more serious than R1** because the audit trail is the EU AI Act compliance evidence. Document the gap in the Brain immediately.

### Failure 3: R7 didn't catch a PR label

**Symptom:** a PR labelled `ai-replaces-human` exists but no Klarna Test entry in X4 Decision_Log.

**Diagnostic:**
- The auto-labeller may not have applied the label (heuristic miss).
- The R7 webhook may not have fired (cloud) or the listener may have crashed (privacy).

**Recovery:**
- Manually trigger R7: in `klarna-test.xlsx` Decision_Log, add a row with `trigger=manual`, `trigger_ref=<PR URL>`, the rest of the test_id pattern; assign scorer + non-beneficiary; the rest follows the normal flow.

### Failure 4: R3 partner statements not delivered

**Symptom:** R3 fired (Brain founder-approval packet exists) but a partner didn't receive their email/dMail.

**Diagnostic:**
- Email connector failure (cloud) or 4thtech dMail issue (privacy).
- Check `~/oot-framework/logs/r3.log` for the send failure line.

**Recovery:**
- Resend manually with a copy-paste from the Brain statement page.
- Document in the Brain that the partner received the statement late (so the 5-business-day acknowledgement window resets from the resend date).

---

## Escalation path

**Level 1 (you can fix it):**
- Re-fire a Routine.
- Backfill a missed day.
- Restart the LM Studio MCP host.

**Level 2 (founder + ops partner together):**
- Repeated failures (a Routine misses 3 days in a row).
- Anomalies that can't be explained from logs alone.
- Branch protection blocking R6 push (config issue, not Routine issue).

**Level 3 (open an issue):**
- The framework's authors monitor [github.com/talirezun/oot-framework/issues](https://github.com/talirezun/oot-framework/issues).
- Include: run log, Brain page state, what you tried.

---

## What "healthy" looks like (long-term)

After 90 days of operation:
- 100% R1 daily fire rate (no missed days).
- 100% R6 daily audit trail (Article 12 compliance maintained).
- R5's weekly health-check report is 5-15 items, mostly typo-fixes; no >25-item Brain decay.
- R2's BR agenda has 2-5 decisions due each week (not 0, not 10+).
- R3's monthly pay calc has zero open disputes after Tier-1 resolution within 5 business days.
- R7 fires 0-3 times per quarter (if more, your AI rollout pace is fast — that's not bad, but the Klarna discipline must keep up).

---

> ⚖️ This document is part of the ØØT framework. The Routines are the framework's automation; their health is the partnership's responsibility.
