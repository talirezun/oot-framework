# Routines

The eight ØØT scheduled Routines, in two flavours: **cloud** ([Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code) — Anthropic's cloud-hosted scheduled-agent product) and **privacy** (OS-native scheduling — cron / launchd / Task Scheduler — hitting headless LM Studio via `llmster`).

The substrates differ; **the prompts are functionally identical** so a firm can switch tracks without rewriting Routine logic.

**Excel state lives in the Ledger (ADR-001).** All `.xlsx` operational state lives in the firm's Ledger GitHub repo; Routines mutate it via openpyxl in code execution and signed-commit + push. Track-symmetric. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../docs/internal/ADR-001-cloud-routine-excel-writeback.md).

---

## The 16 files

| Routine | Cloud | Privacy | Trigger | Owner Skill Pack | Optional? |
|---|---|---|---|---|---|
| R1 — Daily Output Capture | [cloud/R1.md](cloud/R1.md) | [privacy/R1.md](privacy/R1.md) | Daily 18:00 | S3 (+S5 co-owner) | No |
| R2 — Weekly BR Prep | [cloud/R2.md](cloud/R2.md) | [privacy/R2.md](privacy/R2.md) | Friday 08:00 | S5 | No |
| R3 — Monthly Variable Calc | [cloud/R3.md](cloud/R3.md) | [privacy/R3.md](privacy/R3.md) | 1st of month 09:00 | S3 | No |
| R4 — Quarterly Long-Tail Settlement | [cloud/R4.md](cloud/R4.md) | [privacy/R4.md](privacy/R4.md) | 1st of quarter 09:00 | S3 (+S10) | No |
| R5 — Brain Health Check | [cloud/R5.md](cloud/R5.md) | [privacy/R5.md](privacy/R5.md) | Sunday 09:00 | S1 | No |
| R6 — EU AI Act Audit Trail | [cloud/R6.md](cloud/R6.md) | [privacy/R6.md](privacy/R6.md) | Daily 23:00 | S7 | EU adopters: No. Non-EU: optional but recommended. |
| R7 — Klarna Test Trigger | [cloud/R7.md](cloud/R7.md) | [privacy/R7.md](privacy/R7.md) | GitHub event: PR labelled `ai-replaces-human` | S6, S4, S3 | No |
| R8 — Treasury Runway Update | [cloud/R8.md](cloud/R8.md) | [privacy/R8.md](privacy/R8.md) | Monday 08:00 | S10 | **OPTIONAL** — only orgs adopting Unit Fund |

> **R9 — Firm Brain Synthesize (v1.1.0+) has no file here by design.** It is an admin-run weekly Curator operation (CLI or wizard) on the admin's own machine, not a Claude Code Routine — so it does not count against per-day Routine plan limits and ships no `cloud/R9.md` / `privacy/R9.md`. Spec: [`SPEC.md`](SPEC.md) §R9; install: [`docs/02-installing-routines.md`](../docs/02-installing-routines.md).

---

## Recommended install order

For a new firm setting up from zero, install Routines in this order. Each subsequent Routine depends on the prior ones being operational.

1. **R5 (Brain Health Check)** — first. No dependencies on other Routines, but cloud-track R5 requires the Second Brain bridge (Curator GitHub sync + a fine-grained read-only PAT — wizard Step 12 / agent-plan Step 9b / [`docs/00-quickstart-cloud.md`](../docs/00-quickstart-cloud.md) Step 8c). Privacy-track R5 talks to the local my-curator MCP directly. A successful R5 fire confirms the stack is wired.
2. **R6 (EU AI Act Audit Trail)** — second. Depends only on Curator + GitHub. Critical for EU adopters; recommended for everyone.
3. **R1 (Daily Output Capture)** — third. Depends on partners being onboarded with X2 reward-species sheets.
4. **R2 (Weekly BR Prep)** — fourth. Depends on R1 having ≥7 days of data.
5. **R3 (Monthly Variable Calc)** — fifth. Depends on R1 having ≥30 days of data.
6. **R7 (Klarna Test Trigger)** — sixth. Depends on `.github/workflows/klarna-gate.yml` (shipped in the framework repo) being copied into your firm's Ledger repo and branch protection configured.
7. **R4 (Quarterly Long-Tail Settlement)** — seventh. Depends on R3 + at least one X2 Long_Tail_Schedule entry.
8. **R8 (Treasury Runway Update)** — eighth (optional). Depends on Unit Fund adoption decision.

The four Day-1 Routines (R1, R2, R5, R6) are sufficient for the framework's basic operational discipline. The remaining four (R3, R4, R7, R8) onboard as the partnership matures.

---

## Cloud track install (Claude Code Routines)

**Where Routines run:** on Anthropic's cloud infrastructure — not on your local machine. Your laptop can be closed; the Routines fire on schedule against your firm's Ledger on GitHub. You manage them from any of three interfaces (they all configure the same cloud-hosted feature):

- **Claude Code CLI:** `/schedule` command in any Claude Code session
- **Web dashboard:** [claude.ai/code/routines](https://claude.ai/code/routines)
- **Claude Code desktop app:** "New Remote Task" feature *(distinct from Claude Desktop chat — Claude Code has its own desktop app)*

For each Routine to install:

1. Pick one of the three management interfaces above and open it.
2. Click **"New Routine"** (or **"New Remote Task"** in the Claude Code desktop app).
3. Configure trigger per the routine's frontmatter.
4. Upload the prompt body from `routines/cloud/<R>.md`.
5. Attach the listed Skill Packs.
6. Configure connectors and the Ledger per the routine's `mcp_servers` frontmatter. Routines that mutate Excel need: GitHub connector with the Ledger cloneable + pushable, signing key configured (GPG or SSH), and **code execution enabled** (default for Pro+).
7. Manual test fire.
8. Verify expected outputs (Brain page lands, `firm/excel/<file>.xlsx` row appended via signed commit on `main`, Slack post visible).

Estimated setup time per Routine: 10-15 minutes. Total for the 4 Day-1 Routines: ~1 hour.

**Plan-tier guidance.** Pro plan (5 runs/day) is sufficient for solo / 2-partner firms with no R7 activity. **Max plan (15 runs/day, same limit on Team) is the recommended default** for 3+ partner firms or any firm with active R7 (Klarna gate enforcement). Enterprise (25 runs/day) for large firms with extended R7 + R8.

---

## Privacy track install (cron / launchd / Task Scheduler)

For each Routine to install:

1. Confirm the always-on machine is configured (Mac mini / NUC / Pi 5 with FDE + UPS) per Skill Pack S12 §4.2.
2. Confirm LM Studio MCP host is running with the required servers (per the routine's `mcp_servers` frontmatter).
3. Place the prompt body at `~/oot-framework/routines/privacy/<r>.prompt.md` (separate file containing the prompt body — extract from `cloud/<R>.md`).
4. Install the scheduling configuration:
   - **macOS:** save the launchd plist to `~/Library/LaunchAgents/oot.<r>.plist`; run `launchctl load`.
   - **Linux:** add the cron entry via `crontab -e`.
   - **Windows:** import the Task Scheduler XML via `schtasks /create /xml`.
5. Manual test fire (`launchctl start oot.<r>` or equivalent).
6. Verify expected outputs.

Estimated setup time per Routine: 15-20 minutes (longer than cloud because of MCP host config). Total for the 4 Day-1 Routines: ~1.5 hours.

---

## Cross-cutting concerns

**Privacy-track scheduling reliability.** The privacy track requires the always-on machine to be running. If it sleeps or is offline (power outage), Routines miss. The framework's discipline: missed runs are documented as gaps in the audit trail (per R6's "no agent activity today" entry); never silently faked.

**Cloud-track concurrency.** Claude Code Routines run on Anthropic infrastructure; they tolerate the partner's laptop being closed. They do not tolerate Anthropic infrastructure being down — design Routines as idempotent (running R1 twice on the same day produces the same output: idempotent appends keyed on log_id, and Pattern C produces a no-op commit if data hasn't changed).

**Routines and the Klarna Test.** Routines are themselves subject to the Klarna Test. Any new Routine that automates a function previously performed by a partner triggers R7. The framework's authors run R7 against R7 (circular but the discipline holds).

**Auditability.** Every Routine writes to the daily audit log (R6). For EU-operating firms, this is an Article 12 obligation. For others, it is good hygiene.

**Cost containment (cloud).** Estimate Routine costs monthly via X6 (`agent-skill-roi.xlsx`). Cloud Routines for a 10-partner firm running all 8 daily/weekly/monthly typically cost €30–€80/month in Anthropic API fees. R3 in particular runs on Opus (high-stakes); it's the most expensive single Routine.

**Cost containment (privacy).** Marginal cost is electricity for the always-on machine. For a Mac mini M4 Pro running Qwen 3 14B continuously, expect ~€8-15/month in EU electricity prices. Routine model upgrades (e.g. Llama 3.3 70B for R3) add to RAM requirements but not direct cost.

**Versioning.** Each Routine prompt is versioned (semver in frontmatter). Update the prompt → bump the version → log the change in `firm/routines/changelog.md`. Old prompt outputs remain valid; new outputs use the new prompt.

---

## What's coming in v1.x

The v1.0 Routines are the framework's operational core. v1.x will add (per `GENERATIONS.md`):

- **R3 stablecoin payment execution** (Gen 2) — extends R3 with automated USDC/EURC payroll via Rise/Circle after founder approval.
- **R4 smart-contract long-tail** (Gen 2) — replaces the Excel-tracked Long_Tail_Schedule with on-chain percentage entitlements that auto-pay quarterly.
- **R10 Brain semantic-duplicate scan** (Gen 2) — separate Routine running monthly on top of R5's weekly health check.
- **R11 Cotrugli Ledger anchoring** (Gen 3) — anchor R6's audit-log SHA-256s to the Cotrugli Ledger.

(R9 is taken: since v1.1.0 it is the **Firm Brain Synthesize** operation — see below.)

These are out of scope for v1.0; the existing 8 Routines remain stable.
