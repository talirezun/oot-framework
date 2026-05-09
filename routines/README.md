# Routines

The eight ØØT scheduled Routines, in two flavours: **cloud** (Anthropic Remote Routines) and **privacy** (OS-native scheduling — cron / launchd / Task Scheduler — hitting headless LM Studio via `llmster`).

The substrates differ; **the prompts are functionally identical** so a firm can switch tracks without rewriting Routine logic.

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

---

## Recommended install order

For a new firm setting up from zero, install Routines in this order. Each subsequent Routine depends on the prior ones being operational.

1. **R5 (Brain Health Check)** — first. No dependencies. Confirms Curator + my-curator MCP are working.
2. **R6 (EU AI Act Audit Trail)** — second. Depends only on Curator + GitHub. Critical for EU adopters; recommended for everyone.
3. **R1 (Daily Output Capture)** — third. Depends on partners being onboarded with X2 reward-species sheets.
4. **R2 (Weekly BR Prep)** — fourth. Depends on R1 having ≥7 days of data.
5. **R3 (Monthly Variable Calc)** — fifth. Depends on R1 having ≥30 days of data.
6. **R7 (Klarna Test Trigger)** — sixth. Depends on `.github/workflows/klarna-gate.yml` shipping (Phase 8) and branch protection configured.
7. **R4 (Quarterly Long-Tail Settlement)** — seventh. Depends on R3 + at least one X2 Long_Tail_Schedule entry.
8. **R8 (Treasury Runway Update)** — eighth (optional). Depends on Unit Fund adoption decision.

The four Day-1 Routines (R1, R2, R5, R6) are sufficient for the framework's basic operational discipline. The remaining four (R3, R4, R7, R8) onboard as the partnership matures.

---

## Cloud track install (Anthropic Remote Routines)

For each Routine to install:

1. Open the Anthropic Routines dashboard.
2. Click "New Routine".
3. Configure trigger per the routine's frontmatter.
4. Upload the prompt body from `routines/cloud/<R>.md`.
5. Attach the listed Skill Packs.
6. Configure connectors (GitHub, Slack, Drive, Email, etc. per the routine's `mcp_servers` frontmatter).
7. Manual test fire.
8. Verify expected outputs (Brain page lands, Excel row appended, Slack post visible).

Estimated setup time per Routine: 10-15 minutes. Total for the 4 Day-1 Routines: ~1 hour.

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

**Cloud-track concurrency.** Anthropic Remote Routines run on Anthropic infrastructure; they tolerate the partner's laptop being closed. They do not tolerate Anthropic infrastructure being down — design Routines as idempotent (running R1 twice on the same day produces the same output: idempotent appends keyed on log_id).

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
- **R9 Brain semantic-duplicate scan** (Gen 2) — separate Routine running monthly on top of R5's weekly health check.
- **R10 Cotrugli Ledger anchoring** (Gen 3) — anchor R6's audit-log SHA-256s to the Cotrugli Ledger.

These are out of scope for v1.0; the existing 8 Routines remain stable.
