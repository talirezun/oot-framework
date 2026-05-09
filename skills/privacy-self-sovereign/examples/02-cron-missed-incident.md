# Example 2 — Privacy-track incident: cron missed a day

A worked example of the framework's failure-mode handling on the privacy track.

## The incident

**Date:** 2026-04-13 (Monday).
**What happened:** R1 (daily output capture) did not run on Sunday 2026-04-12.

Tomislav (the firm's ops-on-call partner this week) is the first to notice — his Slack-equivalent (4thtech `#output-log`) does not have the Sunday summary at 18:30 Sunday evening. By Monday morning he investigates.

## Investigation

**Step 1 — check launchd logs.**

```
$ tail -50 /Users/oot/oot-framework/logs/r1.log
2026-04-12 17:59:58 — startup OK
2026-04-12 18:00:00 — connecting to LM Studio MCP host (localhost:1234)
2026-04-12 18:00:00 — ERROR: connection refused

$ tail -10 /Users/oot/oot-framework/logs/r1.err
2026-04-12 18:00:00 — failed to acquire MCP host on first attempt
2026-04-12 18:00:30 — retry 1/3 failed: connection refused
2026-04-12 18:01:00 — retry 2/3 failed: connection refused
2026-04-12 18:01:30 — retry 3/3 failed: connection refused
2026-04-12 18:01:30 — fatal: aborting after 3 retries
```

**Step 2 — check the Mac mini's state.**

Tomislav SSHes in (Tailscale-routed). Runs `uptime`:

```
$ uptime
12:34  up 7:24, 1 user, load averages: 0.42 0.55 0.61
```

Uptime: 7h 24m. Current time (Monday 12:34) means the machine booted Monday morning ~05:10. **The machine was off all night Sunday.**

`pmset -g log | head` shows the cause: a power outage at Sunday 16:50 lasting 6 hours. The UPS held for ~30 min, then the Mac mini shut down at 17:20. Power restored at 22:50 but Mac was off; founder remotely woke it via Tailscale Monday morning.

**Step 3 — confirm the gap.**

Tomislav lists `firm/output-logs/`. Files present for every day except 2026-04-12. Confirmed: **R1 did not run Sunday.**

## Recovery

Per §4.7 of S12 "When NOT to invoke" / "Don'ts" #2: *"Routines that miss because the laptop slept = data loss."* The framework's discipline: do not silently fake a Sunday output log. Document the gap.

**Step 1 — backfill the data.**

Tomislav runs:

```
$ /usr/local/bin/llmster --backfill 2026-04-12 --skill compensation-attribution --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r1.prompt.md
```

The `--backfill` flag tells R1 to capture outputs **for the specified date** rather than today. R1 reads GitHub commits, dChat threads, local filesystem activity for 2026-04-12 (a Sunday — typically light). Outputs land:
- 2 commits from Mira (weekend work).
- 1 dChat thread tagged `#output` from Davor about a Sunday customer call.

R1 writes `firm/output-logs/2026-04-12.md`. Header notes: *"backfilled on 2026-04-13 due to power outage; original Sunday R1 run failed at 18:00:00 — see [[firm/privacy-track/troubleshooting/2026-04-12-cron-missed-power-outage]]."*

**Step 2 — write the troubleshooting Brain page.**

Tomislav creates `firm/privacy-track/troubleshooting/2026-04-12-cron-missed-power-outage.md`:

```markdown
---
title: "R1 cron missed — 2026-04-12 — power outage"
type: freeform
date: 2026-04-12
authors: [tomislav-novak]
status: resolved
---

# R1 missed run — 2026-04-12

## What happened

A 6-hour power outage Sunday 16:50–22:50 took down our always-on Mac mini. The UPS held for ~30 min then shut the machine down gracefully at 17:20. R1 was scheduled for 18:00; did not fire because the machine was off.

## Detection

I noticed the missing 4thtech `#output-log` summary Sunday 18:30 evening. Investigated Monday morning.

## Recovery

`llmster --backfill 2026-04-12 ...` captured Sunday's outputs. Daily log now exists at `firm/output-logs/2026-04-12.md` with backfill note.

## Prevention

The CyberPower 1500VA UPS gave 30 min — enough for a typical 5-min outage but not a 6-hour one. Recommendation:
1. **Upgrade UPS** to a CyberPower 3000VA (~€280) — would provide ~90 min of runtime at our load. Still wouldn't cover 6h, but would shift the threshold.
2. **More importantly:** add a `pmset` rule to wake the Mac mini automatically on power restoration (currently it's set to "stay off after power loss"; we'll change to "wake on power"). This would have meant the machine booted at 22:50 and R1 would have caught the missed run via launchd's "missed-run" mechanism.
3. **Long-term:** consider a small UPS-protected NUC as a backup always-on machine for Routine redundancy. Not Q2 priority but on the roadmap.

## Article 12 audit-log impact

R6 also missed its 23:00 Sunday run. Per §R6 spec (`routines/SPEC.md`), the gap is itself an entry: I'm appending a "no agent activity recorded" entry for 2026-04-12 with explanation. The audit branch protection ensures this lands as a signed commit.
```

**Step 3 — append the audit-log gap entry.**

Tomislav runs R6 manually with `--backfill 2026-04-12`:

```
$ /usr/local/bin/llmster --backfill 2026-04-12 --skill governance-compliance --prompt-file ~/oot-framework/routines/privacy/r6.prompt.md
```

R6 writes `firm/audit-logs/2026-04-12.md`:

```markdown
# EU AI Act audit trail — 2026-04-12

This page is part of the firm's Article 12 record-keeping. It is append-only.

## Summary
- AI decisions logged today: **0 (machine offline due to power outage)**
- This is a noted gap, not a missing day. The R1 / R6 Routines did not fire because the always-on machine was off from 17:20 to 22:50 (and not recovered until 2026-04-13 05:10). Backfilled 2026-04-13 by [[partners/tomislav-novak]].
- Incident report: [[firm/privacy-track/troubleshooting/2026-04-12-cron-missed-power-outage]]

## Entries

(none — see above)
```

Signed commit lands on protected `main`. The gap is documented in the audit trail, not hidden.

## Friday BR follow-up

Tomislav surfaces the incident at the Friday BR (KPI snapshot block). Tali agrees with the prevention recommendations:
- Decision D-2026-04-008: *"Upgrade UPS to CyberPower 3000VA; configure pmset wake-on-power on Mac mini. Owner: Tomislav. Deadline: 2026-04-22."*

Decision lands as a Brain page; R5 (Sunday brain health) confirms next Sunday that the troubleshooting page is properly cross-linked.

## What this example demonstrates

- **The framework's discipline of not faking missed runs.** The Sunday gap is in the Brain audit trail with full provenance. Article 12 record-keeping requires this honesty.
- **Recovery is mechanical** (`--backfill` flag) but not automatic — a partner has to invoke it.
- **Prevention is structured** — UPS upgrade + `pmset` config + long-term redundancy plan, with owners and deadlines.
- **Incident → Brain page → BR decision** is the framework's standard incident flow.
- **Honest framing throughout:** the framework is honest that the privacy track has this trade-off (always-on machine can fail); the discipline is to handle the failures cleanly, not to pretend they don't happen.
