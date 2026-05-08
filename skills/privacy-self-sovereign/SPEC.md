# Skill Pack S12 — Privacy / Self-Sovereign Stack: SPEC

**ID:** S12
**Name:** Privacy / Self-Sovereign Stack
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

Orchestrates the privacy track's tools — **4thtech** (on-chain communication), **PollinationX** (decentralised storage), **LM Studio** (local LLM), **Excel MCP** (privacy-track spreadsheet automation), **Desktop Commander** (local filesystem), **GitHub MCP** (cross-machine sync), **OS-native scheduling** (cron / launchd / Task Scheduler) — into a coherent operating mode.

Without this pack, founders adopting the privacy track have a list of tools and no clear "how to wire them together" guide. This pack is the integration layer.

The privacy track achieves **full Generation 1 operational parity** with the cloud track on a single trade-off: cron-driven Routines need an always-on machine, while cloud Routines run while laptops are closed. Everything else — the Brain, the ledger, the BR, the Klarna Test, the audit trail — works identically.

---

## Scope

**Covers:**
- Architectural overview of the privacy track (cloud-track equivalents and what differs).
- LM Studio installation and local model selection (Qwen 3 ≥9B recommended; Llama 3.x; DeepSeek-V3).
- 4thtech setup: dMail, dChat, file transfer, wallet identity on Trezor.
- PollinationX setup: NFT storage acquisition, encrypted bulk file storage, content-addressing in the Brain.
- Excel MCP (`haris-musa/excel-mcp-server`) installation and configuration in LM Studio.
- Desktop Commander MCP for local filesystem.
- GitHub MCP for cross-machine Brain sync.
- **OS-native scheduling** (cron / launchd / Task Scheduler) hitting headless LM Studio (`llmster` CLI).
- The trade-off vs. cloud track and how to mitigate it (always-on machine — Mac mini / NUC / Pi 5).
- Privacy-track secret management additions (4thtech keys on Trezor; never in Bitwarden).
- **Cloud → privacy migration runbook** (4-week structured path).

**Does NOT cover:**
- The cloud-track equivalents (those live in the relevant tool sections of QUICKSTART and the corresponding Skill Packs).
- Crypto operations beyond identity and storage (S10 Finance & Treasury, Gen 2+).
- The legal landscape of self-custodial communication (counsel territory).
- Tor / VPN networking — out of scope; the framework's privacy thesis is data sovereignty, not network anonymity.

---

## Allowed tools / dependencies

- **LM Studio MCP host** (≥0.3.17 with native MCP support).
- **4thtech CLIs and SDKs** — `dmail`, `dchat`, `4thtech-file-transfer`.
- **PollinationX client** — `pollinationx`.
- **Excel MCP server** — `haris-musa/excel-mcp-server` (MIT-licensed).
- **Desktop Commander MCP**.
- **GitHub MCP**.
- **Trezor** (hardware wallet — for 4thtech wallet identity per partner).
- **`llmster`** — headless LM Studio CLI for cron-driven Routines.

---

## When to invoke

1. **Setting up the privacy track** for a firm (founder weekend two of QUICKSTART privacy track).
2. **Onboarding a new partner** to the privacy track (per-partner Trezor + 4thtech identity provisioning).
3. **Migrating from cloud to privacy track** (mid-stream firm decision).
4. **Troubleshooting a privacy-track-specific issue** (cron job missed; Excel MCP unreachable; PollinationX storage stale; 4thtech wallet lost).
5. **Always-on machine maintenance** (OS upgrade, model update, MCP server upgrade).

---

## When NOT to invoke

1. **Cloud-track operations.**
2. **Privacy-track equivalents that have a domain-specific Skill Pack** — e.g., privacy-track variable pay calc is S3's job (with privacy-track-specific MCP routing); this pack is the integration layer, not a re-implementation of S3.
3. **For one-off privacy needs** (a single partner wants to encrypt one document) — overkill; use a simpler tool.

---

## Operational instructions

### 4.1 Privacy track architecture overview

The reference table from `SPEC.md` Layer 2, reproduced here:

| Layer | Cloud (canonical) | Privacy (Gen 1 parity) |
|---|---|---|
| Daily driver | Claude Desktop | Claude Desktop with local-only MCPs OR LM Studio / Ollama |
| Models | Claude Opus/Sonnet, Gemini | Llama, Qwen, DeepSeek, gpt-oss (local) |
| Knowledge | Curator + MyCuratorMCP (cloud ingest) | Curator + MyCuratorMCP (cloud ingest in Gen 1; local LLM ingest = Gen 2) |
| Filesystem | Google Drive (Claude connector) | Desktop Commander MCP |
| Office | Drive + Sheets + Docs | Local Excel + Excel MCP (`haris-musa/excel-mcp-server`) |
| Code | Claude Code, Augment Code, Codex CLI | Open Codex / OpenCode (local-runnable) |
| Browser | Claude Chrome extension | Playwright MCP / local automation |
| Comms — internal | Slack | 4thtech dChat (W2W, on-chain, E2E encrypted) |
| Comms — external | Email, Slack | 4thtech dMail (wallet-as-identity, self-custodial) |
| File transfer | Drive | 4thtech on-chain file transfer + PollinationX bulk storage |
| Automation | Claude Remote Routines (laptop closed) | Local cron / launchd / Task Scheduler + headless LM Studio (laptop on) |
| Compensation rails | FIAT (Gen 1 default) | FIAT → Stablecoin upgrade path (Gen 2) |
| Governance | GitHub + EU AI Act Skill Pack | GitHub + EU AI Act Skill Pack (+ Cotrugli Ledger Gen 3) |

### 4.2 Always-on machine setup (hardware sizing, OS, full-disk encryption)

**Hardware recommendations (in order of decreasing cost):**

1. **Mac mini M4 Pro (32GB RAM)** — €1500-€2000. Best Qwen 3 14B + 8B inference performance for the price. Recommended for primary use.
2. **Intel NUC 13 Pro / NUC 14** — €700-€1200. Linux-friendly. Slightly slower inference but solid.
3. **Raspberry Pi 5 (16GB)** — €120-€200. Adequate for Qwen 3 9B; tight on larger models. Fine for very small firms.
4. **Repurposed older Mac (M1/M2 Mac mini, 16-32GB)** — €400-€800 used. Acceptable for Qwen 3 9B.

**OS setup:**

- macOS: enable FileVault full-disk encryption; set Login password (not Touch ID alone); disable iCloud sync of Brain folders.
- Linux (NUC, Pi): LUKS full-disk encryption at install; set up unattended-upgrades; SSH key authentication only (no password).
- Windows: BitLocker; password + Yubikey 2FA; no remote desktop except VPN'd.

**Network**: the always-on machine is **not** exposed to the public internet (no port-forwarding). Inbound connections only from the partner LAN; outbound for Anthropic API (Curator ingest), GitHub, 4thtech RPC nodes, PollinationX gateways.

**UPS**: a small UPS (€80-€150) covers ~30 minutes of outage. The framework strongly recommends one — a missed daily Routine due to a power blip is the most common privacy-track failure mode.

### 4.3 LM Studio installation; local model selection and download; MCP host configuration

1. Download LM Studio from `lmstudio.ai`. Install on the always-on machine.
2. Open LM Studio. In the model browser, download:
   - **Qwen 3 14B Instruct** (~9 GB, 4-bit quantised). The framework's authors' default for general work.
   - **Qwen 3 9B Instruct** (~5 GB). Fallback for resource-constrained machines.
   - **Llama 3.3 70B Instruct** (~40 GB, 4-bit quantised). For higher-stakes work; requires 32-64 GB RAM.
   - **DeepSeek-V3** (varies). Strong on code tasks; the framework recommends running it specifically for S4 (Code & QA) work.
3. **Enable headless mode** (LM Studio ≥0.3.10 supports `llmster` CLI). This is what cron jobs invoke.
4. **Configure MCP host** (LM Studio ≥0.3.17 native MCP support). In LM Studio settings → MCP Servers, add:
   - `my-curator` — the Curator MCP (per Curator install instructions).
   - `excel-mcp` — `haris-musa/excel-mcp-server`; configure with the Brain repo path.
   - `desktop-commander` — for local filesystem operations.
   - `github-mcp` — for cross-machine sync; PAT stored in Bitwarden, retrieved at MCP startup.
5. Run a self-test: ask the loaded model "list the firm's domains via my-curator's list_domains tool". Successful response = MCP host is configured.

### 4.4 Trezor setup for 4thtech wallet identity (per partner)

Per-partner setup. The firm provides the Trezor (~€80) as part of partner onboarding. Procedure (per-partner, the partner physically holds the device):

1. Order Trezor directly from `trezor.io`. Verify packaging integrity (tamper-evident seals).
2. Initialise offline. The seed phrase is written on paper with a pencil, never digital. Stored in fire-safe location separate from the device.
3. Set strong PIN. Optionally configure passphrase ("25th word") — the framework's authors recommend it for partner devices, with passphrase stored on a separate paper card.
4. Connect to the partner's machine via USB. Install Trezor Bridge.
5. Open the 4thtech wallet client (`4thtech-wallet`); pair with the Trezor. The wallet's address is the partner's 4thtech identity.
6. Record the wallet's address (the public key) in the partner's `firm/partners/<id>/profile.md` Brain page.
7. Send a test dMail from the partner to the founder; founder confirms receipt; identity is live.

**Per-partner trezor cost is a partner-onboarding budget item.** The firm covers it; the partner owns the device and the seed; the firm has no recovery access. This is the point.

### 4.5 4thtech installation (dMail, dChat, file transfer)

Per partner:

1. Install 4thtech client (desktop app or CLI; both supported). Latest at `https://github.com/4thtech`.
2. Authenticate with the partner's Trezor-paired wallet.
3. Configure the firm's dMail domain (the firm's domain on 4thtech, e.g. `acme.4thtech`) and the firm's dChat workspace.
4. Test:
   - Send dMail to self.
   - Join firm dChat workspace.
   - Send a dChat message to `#general`.
   - Receive a file transfer (founder sends a test PDF).

The firm's `firm.yaml` (per `templates/partner-onboarding/PROVISIONING-SPEC.md`) records the firm's dMail domain and dChat workspace; new partners are provisioned via `4thtech invite-dchat` and `4thtech grant-dmail` from the founder's machine.

### 4.6 PollinationX (NFT acquisition, encrypted storage, Brain wikilinks)

**One-time firm setup:**

1. Acquire a PollinationX storage NFT — typical sizes: 100GB (small org), 500GB (medium), 1TB+ (regulated/heavy attachments). Purchase via the PollinationX dApp. Cost: variable; ~€10-€80/month equivalent.
2. The storage NFT is held in the firm's treasury wallet (Trezor-backed).
3. Install PollinationX client on the always-on machine and on each partner's machine.
4. The firm grants per-partner read access via `pollinationx grant-read --nft <storage-nft> --to <partner-wallet>`.

**Brain integration:**

Bulk files (recordings, videos, large PDFs >10MB) live on PollinationX, not in the Brain repo. Brain pages reference them via wikilinks of the form `[[px:<content-address>]]`. The Curator's wikilink discipline supports the `px:` prefix natively (per the Curator's MCP configuration).

When a partner ingests a large file:

1. Upload to PollinationX (encrypted at rest).
2. Receive the content address (a CID-like string).
3. The Curator ingest creates the Brain page; the page references the file as `[[px:<content-address>]]`.
4. Reading partners with PollinationX read access can fetch the file via the wikilink resolution.

### 4.7 Excel MCP installation (and integration with LM Studio)

The privacy track's spreadsheet automation parity hinges on `haris-musa/excel-mcp-server`. Install:

1. `pip install excel-mcp-server` (or `uv pip install`).
2. Configure with the Brain repo path: `EXCEL_MCP_BASE_PATH=/Users/<user>/oot-framework/templates/excel/`.
3. Add to LM Studio's MCP host config (per §4.3 step 4).
4. Test: ask the loaded model "list the worksheets in `partner-output-ledger.xlsx`". Successful response = configured.

**Discipline:** the privacy-track Routines (R1, R2, R3, R4, R6, R7, R8) all read/write Excel via this MCP. The cloud-track equivalents use Google Sheets API. Both code paths are exercised in CI (Phase 8) so the privacy-track is not second-class.

### 4.8 Desktop Commander setup; folder permissioning

1. Install Desktop Commander MCP per upstream docs.
2. Configure the allowed-paths list:
   - `~/oot-framework/` — read/write.
   - `~/Documents/firm/` (the partner's local Brain mirror) — read/write.
   - System paths — denied by default.
3. Add to LM Studio's MCP host config.
4. Test: ask the loaded model "list files in the firm Brain repo's output-logs". Successful response = configured.

The pack ships a recommended `desktop-commander.config.json` template at `examples/desktop-commander.config.json`.

### 4.9 GitHub MCP for cross-machine Brain sync

1. Generate a fine-scoped Personal Access Token (PAT) at `https://github.com/settings/tokens`. Scopes: `repo` (full), `workflow` (for R6 audit-log signed commits).
2. Store in Bitwarden under the partner's per-partner collection.
3. Install GitHub MCP per upstream docs.
4. Configure with the Brain repo URL and the PAT (read from Bitwarden via `bw get item`).
5. Add to LM Studio's MCP host config.
6. Test: ask the model "show me the latest commit on the firm Brain repo". Successful response = configured.

The partner's local machine and the always-on machine both have GitHub MCP configured; both pull/push the Brain repo. Conflicts are resolved by the partner via standard git flow.

### 4.10 OS-native scheduling — cron / launchd / Task Scheduler equivalents of cloud Routines

The eight cloud Routines have privacy-track equivalents per `routines/SPEC.md`. The pack provides the OS-native scheduling templates:

**macOS (launchd) — example for R1 daily output capture:**

```xml
<!-- ~/Library/LaunchAgents/oot.r1.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>oot.r1.daily-output-capture</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/llmster</string>
        <string>--model</string><string>qwen-3-14b-instruct</string>
        <string>--skill</string><string>compensation-attribution</string>
        <string>--skill</string><string>my-curator</string>
        <string>--prompt-file</string>
        <string>/Users/<user>/oot-framework/routines/privacy/r1.prompt.md</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>18</integer><key>Minute</key><integer>0</integer></dict>
    <key>StandardOutPath</key><string>/Users/<user>/oot-framework/logs/r1.log</string>
    <key>StandardErrorPath</key><string>/Users/<user>/oot-framework/logs/r1.err</string>
</dict>
</plist>
```

Install: `launchctl load ~/Library/LaunchAgents/oot.r1.plist`. Verify: `launchctl list | grep oot.r1`.

**Linux (cron) — equivalent:**

```cron
# ~/.crontab additions for ØØT privacy-track Routines
# R1 daily 18:00
0 18 * * * /usr/local/bin/llmster --model qwen-3-14b-instruct --skill compensation-attribution --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r1.prompt.md >> ~/oot-framework/logs/r1.log 2>&1

# R2 Friday 08:00
0 8 * * 5 /usr/local/bin/llmster --model qwen-3-14b-instruct --skill reporting-business-review --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r2.prompt.md >> ~/oot-framework/logs/r2.log 2>&1

# R5 Sunday 09:00
0 9 * * 0 /usr/local/bin/llmster --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r5.prompt.md >> ~/oot-framework/logs/r5.log 2>&1

# R6 daily 23:00 (audit log; uses signed commits via gpg-agent)
0 23 * * * /usr/local/bin/llmster --skill governance-compliance --prompt-file ~/oot-framework/routines/privacy/r6.prompt.md >> ~/oot-framework/logs/r6.log 2>&1
```

Install: `crontab -e`; paste; save. Verify: `crontab -l`.

**Windows (Task Scheduler):**

XML templates ship in `examples/task-scheduler/r1.xml` etc. Install via PowerShell: `schtasks /create /xml "r1.xml" /tn "ØØT R1 Daily Output Capture"`. Verify: `schtasks /query | findstr ØØT`.

### 4.11 Migration workflow (cloud track → privacy track)

A 4-week structured migration. The pack walks through:

**Week 1 — preparation:**
- Hardware acquired (always-on machine + per-partner Trezors).
- LM Studio + models downloaded.
- 4thtech firm domain + dChat workspace provisioned.
- PollinationX storage NFT acquired.
- Brain repo cloned to the always-on machine.

**Week 2 — parallel operation:**
- Cloud Routines continue running.
- Privacy-track equivalents installed in dry-run mode (logs to a separate file; no Brain commits yet).
- Daily comparison: do the privacy-track Routines produce the same outputs as the cloud ones? Reconcile any differences.

**Week 3 — partial cutover:**
- R5, R6 cut over fully (lowest-risk Routines).
- R1, R2 still cloud-run; privacy-track in dry-run.
- Comms migration: founder + 1-2 senior partners on dChat full-time; rest on Slack (still cloud).

**Week 4 — full cutover:**
- All Routines on privacy track.
- All partners on dChat / dMail.
- Bulk storage on PollinationX.
- Cloud subscriptions cancelled or scoped down (Anthropic API still used for Curator ingest until Gen 2 lands local-LLM ingest).

The migration is documented in `firm/privacy-track/migration-runbook.md` per partner per week. Honest framing: **the migration is messy in week 2-3**; the framework's pack does not pretend otherwise. The reference org `examples/regulated-eu-org/` is mid-migration in its snapshot to demonstrate this.

---

## Brain interaction protocol

**Reads:**
- `firm/partners/<id>/profile.md` — for per-partner privacy-track configuration.
- `firm/privacy-track/*` — prior setup logs and migration progress.

**Writes:**
- `firm/privacy-track/always-on-machine.md` — hardware register, OS version, model versions.
- `firm/privacy-track/per-partner-trezor.md` — per-partner Trezor inventory + 4thtech wallet addresses.
- `firm/privacy-track/migration-runbook.md` — the migration log if applicable.
- `firm/privacy-track/troubleshooting/*` — incident logs.

---

## Excel interaction protocol

This pack provides the **privacy-track equivalent of cloud Excel automation** — reads/writes all 9 templates via Excel MCP. The pack does not own any Excel file directly; it is the integration layer that lets every other pack's Excel writes land via Excel MCP rather than Google Sheets API.

---

## Routine integration

The pack provides the privacy-track substrate for all 8 cloud Routines. The execution mechanism differs (cron vs. Anthropic infrastructure); the prompts are functionally identical. See `routines/privacy/*.md` per `routines/SPEC.md`.

---

## Don'ts

1. **Don't store 4thtech wallet seed phrases in Bitwarden**, or any digital store. Trezor only — paper seed in a fire-safe location.
2. **Don't run the privacy track without an always-on machine.** Routines that miss because the laptop slept = data loss.
3. **Don't mix cloud and privacy track for the same firm** without an explicit migration plan (§4.11). Mid-migration is fine; permanently mixed is tooling chaos.
4. **Don't skip full-disk encryption** on the always-on machine. The privacy thesis collapses without it.
5. **Don't trust local LLM outputs at the same threshold as Claude Opus** — quality varies; the Klarna Test still applies. The pack recommends *higher* Klarna scrutiny for privacy-track AI replacements (smaller models = more failure modes).
6. **Don't expose the always-on machine to the public internet.** No port forwarding; no public SSH. Tailscale or WireGuard if remote access is needed.
7. **Don't share Trezor devices** between partners. One Trezor per partner identity. The seed is the partner's, not the firm's.
8. **Don't auto-update LM Studio or the local models without testing** — model behaviour changes affect Routine outputs; new model versions go through a 1-week dry-run before cutover.

---

## Quick reference

| Situation | Action | Output |
|---|---|---|
| Setting up the privacy track | Run §4.2-§4.10 in order | Working privacy-track Brain + Routines |
| Onboarding new partner | Issue Trezor → §4.4 → §4.5 → §4.7 → §4.9 | Partner has dMail/dChat + Excel MCP + GitHub MCP |
| Migrating from cloud | §4.11 4-week runbook | `firm/privacy-track/migration-runbook.md` |
| Cron job missed | Check launchd/cron logs at `oot-framework/logs/`; review UPS state | Incident log + remediation |
| Excel MCP unreachable | Restart server; test via LM Studio chat | Pack troubleshooting Brain page |
| 4thtech wallet identity lost | Trezor seed restore (per partner); firm updates routing | New wallet address recorded; `firm/privacy-track/per-partner-trezor.md` updated |
| Model upgrade | 1-week dry-run; reconcile outputs; cutover | `firm/privacy-track/always-on-machine.md` updated |

---

## Worked examples concept

**3 worked examples in `examples/`:**

1. **A 5-partner firm setting up the privacy track from scratch.** Founder buys a Mac mini M4 Pro; provisions 5 Trezors (one per partner); configures LM Studio with Qwen 3 14B; sets up 4thtech firm domain; acquires a 200GB PollinationX storage NFT; installs Excel MCP, Desktop Commander, GitHub MCP; configures the four Day-1 Routines (R1, R2, R5, R6) via launchd. The example shows the actual config files, the test commands, the verification steps, and ~3 weeks of operational data.

2. **An existing cloud-track firm migrating to privacy track over 4 weeks.** The example follows the migration runbook (§4.11) week-by-week, including the awkward week-2-to-3 transition where Routines run in both modes and the framework's pack reconciles them. Shows the actual `firm/privacy-track/migration-runbook.md` evolving over the 4 weeks.

3. **A privacy-track incident: cron missed a day.** R1 fails to run because the always-on machine's UPS battery died after a 6-hour outage. The Routine has not run for that day. The pack walks through: detection (the next morning's R1 run notices the gap via its own state file), recovery (`llmster --backfill 2026-04-12 --skill compensation-attribution`), audit-log honesty (the gap is documented as a "no agent activity" entry in R6's audit log per the framework's discipline), and prevention (the firm upgrades to a UPS with longer battery life). The full Brain incident log is shown.

---

## References

1. **4thtech project** — `https://github.com/4thtech` and `https://wiki.4thtech.io/quickstart/index`. dMail, dChat, file transfer.
2. **PollinationX** — `https://wiki.pollinationx.io/introduction/start-here`. NFT-based decentralised storage.
3. **The Curator project** — `https://github.com/talirezun/the-curator`. Cloud-LLM ingest in Gen 1; local-LLM ingest = Gen 2 roadmap.
4. **LM Studio MCP support** — `https://lmstudio.ai/docs/local-server/mcp`.
5. **`haris-musa/excel-mcp-server`** — MIT-licensed; `https://github.com/haris-musa/excel-mcp-server`.
6. **Desktop Commander MCP** — `https://github.com/wonderwhy-er/DesktopCommanderMCP`.
7. **GitHub MCP** — `https://github.com/modelcontextprotocol/servers/tree/main/src/github`.
8. **Trezor Suite** — `https://trezor.io/`.
9. **Linux Foundation Agentic AI Foundation** — MCP governance — `https://lfaidata.foundation/`.
10. ØØT `MANIFESTO.md`, Thesis 5 — Composable Lego.
11. ØØT `governance/SECRETS-POLICY.md`.
12. ØØT `routines/SPEC.md` — privacy-track Routine prompts.

---

## Acceptance criteria

Standard. Plus:
- Cross-machine Brain sync example shown end-to-end.
- Full migration example (§4.11) walked through with a 4-week runbook.
- Privacy-track Routine equivalents are explicit (cron expressions or launchd plists shown verbatim for at least R1, R2, R5, R6).
- The hardware register template (`templates/brain/per-partner-trezor.md`) is referenced correctly.
- 3+ worked examples in `examples/`.
- Frontmatter passes the Phase 8 linter.
