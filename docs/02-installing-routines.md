# 02 — Installing Routines (Cloud Track)

**Audience:** Cloud-track founder.
**Time:** ~2 hours for the 4 Day-1 Routines (R1, R2, R5, R6).
**You will end with:** the framework's automation engine running on Anthropic infrastructure, generating daily output captures, weekly BR agendas, Sunday Brain health checks, and daily audit-log entries.

> 📖 **Reference:** [`routines/README.md`](../routines/README.md) summarises all 16 Routine files (8 cloud + 8 privacy). Per-Routine setup checklists at `routines/cloud/<R>.md`.

---

## What this is + the first 5 minutes

ØØT ships **8 scheduled Routines**. The cloud-track equivalents run on [**Claude Code Routines**](https://claude.com/blog/introducing-routines-in-claude-code) — Anthropic's cloud-hosted scheduled-agent product, launched 14 April 2026. Routines execute on Anthropic's infrastructure, so they fire whether or not your laptop is open. The Routine prompts are markdown files at `routines/cloud/R1.md` through `R8.md`; you upload them via Claude Code's `/schedule` command (or the dashboard at claude.com/routines).

## Operational state lives in your Brain repo (ADR-001)

The Routines that read/write `.xlsx` operational state — R1 (X1 Output_Log), R2 (X1, X3, X4, X6), R3 (X1 Monthly_Variable + X2), R4 (X2 Long_Tail_Schedule), R6 (X7 Audit_Log_Index), R7 (X4 Decision_Log), R8 (X8 Runway_Calc) — do so by **cloning your firm's Brain GitHub repo, mutating the `.xlsx` file via Python's `openpyxl` library in code execution, then signed-committing and pushing the change to `main`**. This is the same operation cloud and privacy Routines perform; only the substrate (Anthropic infrastructure vs. local cron on your always-on machine) differs. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](internal/ADR-001-cloud-routine-excel-writeback.md) for the full decision rationale.

What this means for setup:
- Your Brain repo's `firm/excel/*.xlsx` files are the canonical store for `.xlsx` state. Don't keep a separate Google Sheets copy as the source of truth.
- The bot identity executing Routines (e.g. `oot-bot`) needs a GPG or SSH signing key uploaded to GitHub plus push access to the Brain repo's protected `main` branch.
- Code execution must be enabled in each Routine's config (default for Pro+).
- For viewing the `.xlsx` files manually you can use Excel, LibreOffice, Numbers, Excel-for-Web, or any other `.xlsx`-compatible app.

The 8 Routines:

| # | Trigger | What it does | Day 1? |
|---|---|---|---|
| R1 | Daily 18:00 | Reads commits/PRs/messaging for the day; appends X1 Output_Log; writes daily Brain summary | ✓ |
| R2 | Friday 08:00 | Builds BR agenda; populates X3; posts Slack draft | ✓ |
| R3 | 1st of month 09:00 | Calculates monthly variable; sends per-partner statements; founder approval | wait |
| R4 | 1st of quarter 09:00 | Settles long-tail entitlements per X2 | wait |
| R5 | Sunday 09:00 | Curator brain-health scan; fixes safe categories; surfaces unsafe to Slack | ✓ |
| R6 | Daily 23:00 | EU AI Act audit trail; signed commits to protected branch | ✓ (mandatory if EU) |
| R7 | GitHub event | Klarna Test trigger on PR labelled `ai-replaces-human` | wait |
| R8 | Monday 08:00 | Treasury runway (OPTIONAL — Unit Fund only) | optional |

Day-1 install is **R5, R6, R1, R2** in that order (R5 has no dependencies so it goes first; R6 needs branch protection one-time; R1 needs a partner with X2 sheet; R2 needs R1 to have data).

---

## Pre-requisites

- **Anthropic Pro or Max plan** (Routines require Pro+). Plan tiering:
  - **Pro** (5 runs/day) — solo or 2-partner firm with no R7 (Klarna gate) firing yet.
  - **Max** (15 runs/day) — **recommended default** for 3+ partner firms or any firm with active R7.
  - **Team / Enterprise** (25 runs/day) — 5+ partner firms, or firms running R8 + extended R7.
- **Curator + my-curator MCP** installed and verified ([docs/01-installing-the-curator.md](01-installing-the-curator.md)).
- **GitHub Brain repo** — your firm's Brain repo (markdown wiki + `.xlsx` operational state). Pre-configured with branch protection per `routines/cloud/R6.md` setup checklist.
- **Bot identity for Routines** — typically `oot-bot` GitHub user, with: a GPG or SSH signing key uploaded; push access to the Brain repo's `main` branch; the `[skip review]` exemption on `firm/excel/*` and `firm/audit-logs/*` paths per `skills/code-qa/SKILL.md` §4.0.
- **Slack workspace** with the [Claude integration](https://slack.com/apps/A0848GFRZ54-claude) enabled.
- *(Optional)* Google Workspace seat — only if you want the Anthropic native connectors for Drive / Calendar / Gmail **read-only** convenience. Operational state does NOT live in Google services per ADR-001.

---

## Step-by-step (per Routine)

For each Routine, the install pattern is the same. Here's the full procedure for R5; the other Routines follow the identical pattern with track-specific differences.

### R5 — Brain Health Check (do first)

**Why first:** no dependencies. If R5 fires successfully, your Curator + MCP + Slack stack is wired.

1. **Open the Claude Code Routines dashboard.** [claude.com/routines](https://claude.com/routines) (or via the `/schedule` command in Claude Code, or Settings → Routines in Claude Desktop).
2. Click **"New Routine"**.
3. **Name:** `R5 Brain Health Check`.
4. **Trigger:** Schedule. Time zone: your firm's primary. Recurrence: weekly. Day: Sunday. Time: 09:00.

   ![R5 trigger configuration](images/02-1-r5-trigger.png)

   *Look for the "Sunday 09:00 (your firm timezone)" confirmation underneath the trigger picker.*

5. **Prompt:** copy the body from [`routines/cloud/R5.md`](../routines/cloud/R5.md) (everything inside the `## Prompt body` fenced block).
6. **Skill Packs:** attach `my-curator` (the canonical S1 SKILL.md, already in Claude Desktop as a Project Document — the Routines dashboard lets you select it from your skill library).
7. **Connectors:** Slack (post permission for `#brain-health` and `#ops`), GitHub (read for the Brain repo).
8. **Save** the Routine.
9. **Manual test fire:** in the Routine's detail page, click "Run now". The Routine executes immediately (instead of waiting until Sunday).
10. **Verify outputs:**
    - Slack `#brain-health`: a summary message appears.
    - Brain repo: `firm/brain-health/2026-WW.md` (current ISO week) is committed.

If both verifications pass, R5 is operational. ✓

---

### R6 — EU AI Act Audit Trail (do second)

**Pre-requisite:** GitHub branch protection configured on `main` (force-push disabled, deletion disabled, signed commits required, ≥1 reviewer for `firm/audit-logs/*`). See [`routines/cloud/R6.md`](../routines/cloud/R6.md) one-time setup.

**Why second:** R6 is critical for EU founders (Article 12 obligation from 2 August 2026); recommended for everyone. Must be configured before partners start producing AI-augmented work.

1. Claude Code → `/schedule` → **"New Routine"**.
2. **Name:** `R6 EU AI Act Audit Trail`.
3. **Trigger:** Schedule. Daily. Time: 23:00.
4. **Prompt body** from [`routines/cloud/R6.md`](../routines/cloud/R6.md).
5. **Skill Packs:** `governance-compliance` (S7 scaffold).
6. **Connectors:** GitHub (push to `main` with signed-commit capability), Curator MCP (read agent-decision data), Slack (escalation to `#ops`).
7. **Save.** Manual fire.
8. **Verify:** `firm/audit-logs/<today>.md` exists and is a **signed** commit (`git log --show-signature` shows `gpg: Good signature`).

---

### R1 — Daily Output Capture (do third)

**Pre-requisite:** at least one partner onboarded (you, the founder, count).

1. Routines dashboard → **"New Routine"**.
2. **Name:** `R1 Daily Output Capture`.
3. **Trigger:** Schedule. Daily. Time: 18:00.
4. **Prompt body** from [`routines/cloud/R1.md`](../routines/cloud/R1.md).
5. **Skill Packs:** `compensation-attribution`, `my-curator`, `reporting-business-review`.
6. **Connectors:** GitHub, Slack, Drive.
7. **Template variables:** set `{{TRACKED_CHANNELS}}` (e.g. `#commercial,#sales,#engineering`) and `{{TRACKED_FOLDERS}}` (Drive folder IDs you want monitored).
8. Save. Manual fire.
9. **Verify:** `templates/excel/partner-output-ledger.xlsx` Output_Log has a new row for today; `firm/output-logs/<today>.md` exists.

---

### R2 — Weekly BR Prep (do fourth)

**Pre-requisite:** R1 has been running for ≥7 days (so X1 has data).

1. Routines dashboard → **"New Routine"**.
2. **Name:** `R2 Weekly BR Prep`.
3. **Trigger:** Schedule. Weekly. Friday. 08:00.
4. **Prompt body** from [`routines/cloud/R2.md`](../routines/cloud/R2.md).
5. **Skill Packs:** `reporting-business-review`, `my-curator`.
6. **Connectors:** GitHub (Brain repo, read+write with signing), Slack. **Code execution must be enabled** for the openpyxl writes.
7. Save. Manual fire (will populate X3 with the current partial-week's data via a signed commit on `main`).
8. **Verify:** X3 Weekly_Review has a new row; the change is on `main` as a signed commit by the bot identity; Slack `#business-review` has a draft summary.

---

## Other Routines (when to install)

- **R3** — install after the first month closes (so the partner-output-ledger has 30+ days of data). Recommended model: Opus.
- **R4** — install after the first quarter (so partners have shipped long-tail-eligible outputs).
- **R7** — install after Phase 8 ships `.github/workflows/klarna-gate.yml` and you have configured the `ai-replaces-human` auto-labeller and the required-status-check branch protection.
- **R8** — install only if the firm adopts the Unit Fund (Generation 2 readiness).

---

## Common pitfalls

**1. Routine fires but Brain page doesn't appear.**
- Cause: my-curator MCP is configured for Claude Desktop but the Routine on Anthropic's infrastructure can't reach your local Curator app. (Stdio MCPs cannot run in cloud Routines — there's no local machine to dial.)
- Fix: the my-curator MCP must run as a remote-HTTP MCP reachable from Anthropic's infrastructure. Options: deploy MyCuratorMCP on a tiny always-on Pi 5 with a Tailscale-routed HTTPS endpoint; or use Anthropic's Curator-as-a-service offering (Q3 2026 launch). Privacy-track partners use the always-on machine for the same purpose.

**1a. Routine fires but no commit lands on main.**
- Cause: bot identity's signing key is missing, branch protection rejects the push, or `[skip review]` exemption is misconfigured.
- Fix: re-check the R6 setup checklist (it covers branch protection + signing). Run `git log --show-signature` against the Brain repo's `main` to verify what's actually being signed. The Routine retries with backoff; if it gives up, you'll see a `#ops` Slack alert.

**2. Slack post fails: "channel not found".**
- Cause: the channel doesn't exist or the Claude Slack app isn't a member.
- Fix: create the channel; add the Claude app via Slack `/invite @Claude`.

**3. R6 push fails: "GPG signature required".**
- Cause: the bot account executing R6 doesn't have a GPG key uploaded to GitHub.
- Fix: generate a GPG key for `oot-bot`; upload public key at [github.com/settings/keys](https://github.com/settings/keys); configure `git config --global user.signingkey <key-id>`.

**4. R1 captures everything as `value_tier=L`.**
- Cause: no Output Specs exist yet.
- Fix: this is correct behaviour for the first weeks. As Output Specs accumulate at `firm/partners/<id>/output-specs/`, R1 references them and assigns better tiers.

**5. Routine cost spikes unexpectedly.**
- Cause: typically the prompt is reading too much context (e.g. all GitHub commits for 30 days instead of 24h).
- Fix: review the prompt body; ensure it filters to "past 24 hours" not "all time"; check X6 agent-skill-roi for the spike's source Skill.

---

## When to escalate

- **A Routine consistently fails** despite Anthropic infrastructure being healthy: open an issue on this repo with the Routine's run log.
- **A Routine produces incorrect output** (wrong partner_id assignment, wrong value_tier): the framework's authors review these as quality-of-prompt issues; surface in the next Friday BR.
- **A Routine triggers a Klarna Test you don't think it should**: the auto-labeller is a heuristic; review per S4 §4.8 and dismiss with a documented reason if false-positive.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. The R6 audit trail addresses EU AI Act Article 12; counsel review is mandatory before relying on the framework's classification.
