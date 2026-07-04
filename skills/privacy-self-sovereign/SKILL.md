---
name: privacy-self-sovereign
description: Use whenever the firm is setting up the privacy track from scratch, onboarding a new partner to the privacy track (per-partner Trezor + 4thtech identity provisioning), migrating from cloud to privacy track, troubleshooting a privacy-track-specific issue (cron job missed, Excel MCP unreachable, PollinationX storage stale, 4thtech wallet lost), or maintaining the always-on machine. Activates for "set up the privacy track for our 5-partner firm", "Mira lost her Trezor — what do we do?", "the R1 cron job didn't run — diagnose", "we want to migrate from cloud to privacy track in 4 weeks", "upgrade Qwen 3 to the new model release". Enforces the 4thtech-keys-on-Trezor-only secrets discipline, the always-on-machine-with-FDE-and-UPS hardware baseline, the cloud-LLM-ingest-only-in-Gen-1 Curator constraint, and the `oot/klarna-test` gate's privacy-track equivalent (signed commits via gpg-agent, not GitHub-hosted).
version: 1.0.0
tier: 1
status: hardened
allowed_tools:
  - mcp__desktop-commander__list_files
  - mcp__desktop-commander__read_file
  - mcp__desktop-commander__write_file
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__excel__append_row
  - mcp__github__create_or_update_file
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__get_node
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S12
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1]
oot_provides_to: [S2, S3, S4, S5, S6, S7, S8, S9, S10, S11]
oot_klarna_test: false
last_updated: 2026-05-15
---

# Privacy / Self-Sovereign Stack

> **Generation marker:** Hardened in v1.0. Operational parity with cloud track on a single trade-off (cron-driven Routines need an always-on machine; cloud Routines run with laptops closed).
> **Klarna Test interaction:** No directly (the pack provides the substrate; S6 / S3 / S4 are the participants).
> **Brain interaction:** Both — writes setup logs, hardware register, migration runbook, troubleshooting incidents.

## 1. Purpose

Orchestrates the privacy track's tools — **4thtech** (on-chain communication), **PollinationX** (decentralised storage), **LM Studio** (local LLM), **Excel MCP** (privacy-track spreadsheet automation), **Desktop Commander** (local filesystem), **GitHub MCP** (cross-machine sync), **OS-native scheduling** — into a coherent operating mode.

Without this pack, founders adopting the privacy track have a list of tools and no clear "how to wire them together" guide. This pack is the integration layer.

## 2. When to invoke this pack

1. **Setting up the privacy track** for a firm.
2. **Onboarding a new partner** to the privacy track (per-partner Trezor + 4thtech identity).
3. **Migrating from cloud to privacy track** mid-stream.
4. **Troubleshooting a privacy-track-specific issue** (cron missed; Excel MCP unreachable; PollinationX stale; 4thtech wallet lost).
5. **Always-on machine maintenance** (OS upgrade, model update, MCP server upgrade).

## 3. When NOT to invoke this pack

1. Cloud-track operations.
2. Privacy-track equivalents of domain-specific operations — e.g., privacy-track variable pay calc is S3's job (with privacy-track MCP routing); this pack is the integration layer, not a re-implementation of S3.
3. One-off privacy needs (a single partner wants to encrypt one document) — overkill; use a simpler tool.

## 4. Operational instructions

### 4.1 Privacy track architecture overview

The reference table from `SPEC.md` Layer 2:

| Layer | Cloud (canonical) | Privacy (Gen 1 parity) |
|---|---|---|
| Daily driver | Claude Desktop | Claude Desktop with local-only MCPs OR LM Studio / Ollama |
| Models | Claude Opus/Sonnet, Gemini | Llama, Qwen, DeepSeek, gpt-oss (local) |
| Knowledge | Curator + MyCuratorMCP (cloud ingest) | Curator + MyCuratorMCP (cloud ingest in Gen 1; local LLM ingest = Gen 2) |
| Filesystem | Google Drive (Claude connector) | Desktop Commander MCP |
| Office | Drive + Sheets + Docs | Local Excel + Excel MCP |
| Code | Claude Code, Augment Code, Codex CLI | Open Codex / OpenCode |
| Browser | Claude Chrome extension | Playwright MCP / local automation |
| Comms — internal | Slack | 4thtech dChat (W2W, on-chain, E2E encrypted) |
| Comms — external | Email, Slack | 4thtech dMail |
| File transfer | Drive | 4thtech on-chain + PollinationX bulk storage |
| Automation | Claude Code Routines (laptop closed) | OS-native scheduling → OpenCode headless against a local LM Studio server (laptop on) |
| Compensation rails | FIAT (Gen 1 default) | FIAT → Stablecoin upgrade (Gen 2) |
| Governance | GitHub + EU AI Act Skill Pack | GitHub + EU AI Act Skill Pack (+ Cotrugli Ledger Gen 3) |

### 4.2 Always-on machine setup

**Hardware (in order of decreasing cost):**

1. **Mac mini M4 Pro (32GB)** — €1500-2000. Best Qwen 3 14B + 8B inference for the price.
2. **Intel NUC 13 Pro / 14** — €700-1200. Linux-friendly.
3. **Raspberry Pi 5 (16GB)** — €120-200. Adequate for Qwen 3 9B; tight on larger.
4. **Repurposed older Mac (M1/M2 mini, 16-32GB)** — €400-800 used. Acceptable for Qwen 3 9B.

**OS setup:**
- macOS: enable FileVault FDE; Login password (not Touch ID alone); disable iCloud sync of Brain folders.
- Linux: LUKS FDE at install; unattended-upgrades; SSH key auth only.
- Windows: BitLocker; password + Yubikey 2FA; no remote desktop except VPN'd.

**Network:** not exposed to public internet. No port-forwarding. Outbound for Anthropic API, GitHub, 4thtech RPC, PollinationX gateways only.

**UPS:** small UPS (€80-150). Strongly recommended — a missed daily Routine due to a power blip is the most common privacy-track failure mode.

### 4.3 LM Studio installation + MCP host configuration

1. Download from `lmstudio.ai`. Install on the always-on machine.
2. Download models:
   - **Qwen 3 14B Instruct** (~9 GB, 4-bit quantised) — default.
   - **Qwen 3 9B Instruct** (~5 GB) — fallback.
   - **Llama 3.3 70B Instruct** (~40 GB) — higher-stakes; 32-64 GB RAM.
   - **DeepSeek-V3** — strong on code; pair with S4.
3. Run the model server headless. The privacy-track scheduled stack has **three pieces**, and LM Studio is only the model server:
   - **`llmster`** — LM Studio's headless **daemon** (per [lmstudio.ai/docs/developer/core/headless](https://lmstudio.ai/docs/developer/core/headless)). It *hosts* the local model on an OpenAI-compatible server at `http://127.0.0.1:1234/v1`. It is **not** an agent: no `--skill` / `--prompt-file` flags; it runs no prompts.
   - **`lms`** — LM Studio's own CLI (`lms server start`; keep a model warm with `lms load qwen-3-14b-instruct --ttl 3600`).
   - **OpenCode** — the agent harness (`opencode run`) that actually loads skills, clones the Ledger, runs openpyxl, and calls the MCP servers, pointing its `lmstudio` provider at the server above. See [`../../installer/agent-assisted/OPENCODE-SETUP.md`](../../installer/agent-assisted/OPENCODE-SETUP.md) → "Scheduled / unattended runs".
4. Configure MCP servers in OpenCode's runner-directory `opencode.json` `mcp` block (**not** in LM Studio):
   - `my-curator` — Curator MCP.
   - `excel-mcp` — `haris-musa/excel-mcp-server`; configure with Ledger path (optional — human-in-the-loop only; Routines use openpyxl directly).
   - `desktop-commander` — local filesystem.
   - `github-mcp` — cross-machine sync; PAT from Bitwarden.
5. Self-test: from OpenCode, ask `"use my-curator; list the firm's domains"`. Successful response = configured.

### 4.4 Trezor setup for 4thtech wallet identity (per partner)

Per-partner. Firm provides the Trezor (~€80) as part of partner onboarding. Partner physically holds the device.

1. Order from `trezor.io`. Verify packaging integrity.
2. Initialise offline. Seed phrase on paper with pencil. Stored in fire-safe location separate from device.
3. Set strong PIN. Optionally configure passphrase (the "25th word") with separate paper card.
4. Connect to partner's machine via USB. Install Trezor Bridge.
5. Open `4thtech-wallet`; pair with Trezor. Wallet's address is the partner's 4thtech identity.
6. Record wallet address in `firm/partners/<id>/profile.md` Brain page.
7. Send test dMail; founder confirms receipt; identity is live.

> ⚠️ **Per-partner Trezor cost is a partner-onboarding budget item.** Firm covers it; partner owns device + seed; firm has no recovery access. This is the point.

### 4.5 4thtech installation (dMail, dChat, file transfer)

Per partner:

1. Install 4thtech client (desktop or CLI). https://github.com/4thtech.
2. Authenticate with Trezor-paired wallet.
3. Configure firm's dMail domain (e.g. `acme.4thtech`) and dChat workspace.
4. Test: send dMail to self; join firm dChat; send `#general` message; receive file transfer from founder.

`firm.yaml` records firm's dMail domain + dChat workspace. New partners provisioned via `4thtech invite-dchat` and `4thtech grant-dmail` from founder's machine.

### 4.6 PollinationX (NFT storage + Brain wikilinks)

**One-time firm setup:**

1. Acquire storage NFT (sizes: 100GB / 500GB / 1TB+; cost: ~€10-80/month equivalent).
2. NFT held in firm's treasury wallet (Trezor-backed).
3. Install PollinationX client on always-on machine + each partner's machine.
4. Grant per-partner read access: `pollinationx grant-read --nft <storage-nft> --to <partner-wallet>`.

**Brain integration:**

Bulk files (recordings, videos, large PDFs >10MB) live on PollinationX. Brain pages reference via `[[px:<content-address>]]`. Curator's wikilink discipline supports `px:` prefix natively.

When ingesting a large file: upload to PollinationX → receive content address → Brain page references via `[[px:<cid>]]`.

### 4.7 Excel MCP installation

The privacy track's spreadsheet parity hinges on `haris-musa/excel-mcp-server`:

1. `pip install excel-mcp-server` (or `uv pip install`).
2. Configure the base path to point at the **firm Ledger clone's `firm/excel/` directory** — the operational workbooks — not at the framework's `templates/excel/`. The framework templates are pristine masters (generated by `scripts/build_excel.py`) and must never be used as operational state. Example: `EXCEL_MCP_BASE_PATH=/Users/<user>/<firm>-ledger/firm/excel/`.
3. Add to LM Studio's MCP host config (per §4.3 step 4).
4. Test: `"list the worksheets in partner-output-ledger.xlsx"` → successful response.

**Excel writes on both tracks go through openpyxl in code execution on the Ledger clone, per [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md) — identical to the cloud track.** The Excel MCP is an **optional, human-in-the-loop** convenience for inspecting or hand-patching a workbook from an LM Studio chat; it is **not** the Routine write path. The privacy-track Routines (R1, R2, R3, R4, R6, R7, R8) mutate the workbooks with openpyxl on the local Ledger clone, then signed-commit and push — the same operation cloud Routines perform.

### 4.8 Desktop Commander setup

1. Install per upstream docs.
2. Allowed-paths config:
   - `~/<firm>-ledger/` (the firm Ledger clone — operational state Routines read/write) — **read/write**.
   - `~/curator/shared-<firm-slug>/` (partner's local Firm Brain mirror) — read/write as needed.
   - `~/oot-framework/` (the framework repo — pristine masters: templates, SPECs, scripts) — **read-only**. Routines never mutate framework files; they operate on the Ledger clone.
   - System paths — denied.
3. Add to LM Studio's MCP host config.
4. Test: `"list files in the firm Ledger's output-logs"` → successful response.

Pack ships a recommended `desktop-commander.config.json` template at `examples/desktop-commander.config.json`.

### 4.9 GitHub MCP for cross-machine sync

1. Generate fine-scoped PAT at `github.com/settings/tokens`. Scopes: `repo` (full), `workflow` (for R6 signed commits).
2. Store in Bitwarden under partner's collection.
3. Install GitHub MCP per upstream docs.
4. Configure with Ledger URL + PAT (read via `bw get item`).
5. Add to LM Studio MCP host config.
6. Test: `"show me the latest commit on the firm Ledger"` → successful response.

Partner's machine + always-on machine both have GitHub MCP. Both pull/push Brain. Conflicts resolved by partner via standard git flow.

### 4.10 OS-native scheduling

The 8 cloud Routines have privacy-track equivalents per `routines/SPEC.md`. The pack provides scheduling templates:

> **The `routines/privacy/r*.prompt.md` files referenced in the schedules below are extracted at install time from the corresponding `routines/cloud/R*.md` prompt bodies** (per [`routines/README.md`](../../routines/README.md) privacy-track install, step 3) — the repo does **not** ship pre-built `r*.prompt.md` files. During privacy-track setup, copy each Routine's prompt body out of `cloud/<R>.md` into a `privacy/<r>.prompt.md` file that the scheduler points at.

The scheduler invokes **OpenCode headless** (`opencode run`) against the local LM Studio server; each `r*.prompt.md` **begins with a read-the-owner-SKILL.md-first line** (this replaces the old per-invocation `--skill` flags — the prompt loads its own skills). Run each command from the firm's runner directory (`~/{{FIRM_SLUG}}`) so OpenCode picks up that directory's scoped `opencode.json` (provider + MCP + the unattended allow-list). See [`../../installer/agent-assisted/OPENCODE-SETUP.md`](../../installer/agent-assisted/OPENCODE-SETUP.md) → "Scheduled / unattended runs".

**macOS (launchd) — R1 example:**

```xml
<!-- ~/Library/LaunchAgents/oot.r1.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>oot.r1.daily-output-capture</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-lc</string>
        <string>cd ~/{{FIRM_SLUG}} && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)"</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>18</integer><key>Minute</key><integer>0</integer></dict>
    <key>StandardOutPath</key><string>/Users/<user>/oot-framework/logs/r1.log</string>
    <key>StandardErrorPath</key><string>/Users/<user>/oot-framework/logs/r1.err</string>
</dict>
</plist>
```

Install: `launchctl load ~/Library/LaunchAgents/oot.r1.plist`. Verify: `launchctl list | grep oot.r1`.

**Linux (cron)** — each line's model is per-routine (R2/R5 use the daily driver; R6's governance work can too; R3 wants the larger model). The routine's skill mapping lives in its prompt file's read-first line, not on the command:

```cron
# R1 daily 18:00 (compensation-attribution + my-curator, per r1.prompt.md's read-first line)
0 18 * * * cd ~/{{FIRM_SLUG}} && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)" >> ~/oot-framework/logs/r1.log 2>&1

# R2 Friday 08:00 (reporting-business-review + my-curator)
0 8 * * 5 cd ~/{{FIRM_SLUG}} && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r2.prompt.md)" >> ~/oot-framework/logs/r2.log 2>&1

# R5 Sunday 09:00 (my-curator)
0 9 * * 0 cd ~/{{FIRM_SLUG}} && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r5.prompt.md)" >> ~/oot-framework/logs/r5.log 2>&1

# R6 daily 23:00 (governance-compliance; audit log signed via gpg-agent)
0 23 * * * cd ~/{{FIRM_SLUG}} && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r6.prompt.md)" >> ~/oot-framework/logs/r6.log 2>&1
```

**Windows (Task Scheduler):** XML templates ship in `examples/task-scheduler/`. Install via `schtasks /create /xml "r1.xml" /tn "ØØT R1 Daily Output Capture"`.

### 4.11 Curator Shared Brain on the privacy track (the Firm Brain)

Per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), the firm's collective knowledge (theses, decisions, ADRs, partner profiles, prompts) lives in the **Firm Brain** — a Curator Shared Brain instance (v3.0.0-beta+) in a dedicated `<firm>-brain` GitHub repo. The privacy track participates identically to the cloud track at the Shared Brain protocol layer; the deltas are about *what runs locally*.

**S12 alignment with Shared Brain's data-handling model.** Curator's Shared Brain protocol is materially better aligned with S12's self-sovereign discipline than the pre-v1.0.1 pattern:

- **Data minimisation.** Only the partner's *opted-in domain* contributes to the Firm Brain via preprocessed `DeltaSummary` JSON. Their other domains (`personal`, `customers`, `research`) stay on their machine. The retired pre-v1.0.1 `<firm>-secondbrain` pattern pushed the *entire* vault — strictly more data leakage.
- **UUID-pseudonymous attribution by default.** Both `allow_name_attribution` (org-side) and `attribute_by_name` (contributor-side) default to `false`. Real names appear in synthesized pages only when both flags are explicitly true. This is exactly the posture S12 wants for partners who value pseudonymity.
- **Right to erasure (GDPR Article 17) is first-class.** The admin can revoke a departing partner via `POST /api/sharedbrain/:id/revoke` with a typed-confirmation safety gate; all the partner's contributions are deleted and affected synthesized pages are rebuilt. S12 partners who insist on `contributor_retains` IP mode (advisors, contractors, outside collaborators) get a clean exit path.
- **`contributor_retains` IP mode for the self-sovereign-aligned.** Curator's `data_handling_terms = "contributor_retains"` keeps copyright with the contributor while the firm owns only the synthesized output. **This is S12's default recommendation for advisors and contractors**; operating-LLC partners typically use `organisational` mode per their partner charter's IP-assignment clause (the firm-side decision recorded in CLAUDE.md decision #15).

**Per-partner setup (privacy-track variant):**

1. Receive the firm's invite token (`sbi_…`) via 4thtech dMail or dChat (not Slack — privacy track uses 4thtech for firm comms).
2. Accept the GitHub collaborator invite on the `<firm>-brain` repo. **GitHub plan-tier requirement: Team minimum for branch protection** (Free private repos do not enforce protection — Finding #16); **GitHub Enterprise Cloud with EU residency option if your firm is EU-regulated**.
3. Create a fine-grained PAT in your GitHub account with Contents read/write on the `<firm>-brain` repo. Store the PAT in **Bitwarden** (or 1Password) per the secrets policy; **do not commit it anywhere**.
4. Run Curator's six-step contributor wizard. Curator runs locally on your machine — the wizard itself does not call any cloud LLM. Read the IP-mode disclosure before consenting.
5. After save, Curator's connection card shows Push and Pull buttons. Push uploads only your opted-in domain. Pull mirrors the synthesized result into `~/curator/shared-<firm-slug>/` (read-only).

**Synthesis caveat (Gen 1 gap).** The admin's weekly Synthesize step still calls a cloud LLM (Curator v3.0.0-beta uses Gemini Flash Lite). This is the **single remaining cloud-LLM dependency** in the privacy-track Gen-1 stack — the same gap [`GENERATIONS.md`](../../GENERATIONS.md) already flags for Curator broadly. Partners' own MCP interactions with their personal Second Brain can run fully on a local model (LM Studio + Qwen / Llama / DeepSeek); only Synthesize is cloud-coupled. Curator v3.1+ on the roadmap removes this dependency.

**Cloud-LLM-call boundary on the privacy track:**
- Partner authoring pages in their personal Second Brain via MCP → **local LLM** (LM Studio).
- Partner running Push → **no LLM call** (deterministic preprocessing + git push).
- Partner running Pull → **no LLM call** (git fetch + local file write).
- Admin running Synthesize → **cloud LLM** (Gemini Flash Lite in v3.0.0-beta; ~$0.01 / 100-page brain / 5 contributors / week).

**Storage residency on the privacy track.** The Firm Brain repo on GitHub is subject to GitHub's storage residency. EU firms requiring data residency must use **GitHub Enterprise Cloud with EU residency option** (paid; ~$21/seat/mo) for the `<firm>-brain` repo. Curator v3.1's Cloudflare R2 backend with per-bucket `jurisdiction = "eu"` will offer a more cost-effective EU-residency path; deferred to v3.1.

**Hardware-key alignment.** Per §4.4, partner identity in 4thtech is wallet-on-Trezor. The Firm Brain PAT is a *different secret* — held in Bitwarden, not on the Trezor (PATs are software tokens, not on-chain keys). The double-secrets-layer is intentional: 4thtech keys (on-chain identity, irrecoverable if lost) are Trezor-isolated; Curator/GitHub PATs (software credentials, rotatable) live in Bitwarden.

**Routines on the privacy track do not push to the Firm Brain.** Per ADR-002, Routines write only to the Ledger. Privacy-track Routines that need *firm-context knowledge* (e.g., R5 reporting, R2 BR pre-fill) clone the Firm Brain repo locally to read `collective/<firm-domain>/wiki/` — same pattern as cloud Routines.

### 4.12 Migration workflow (cloud → privacy)

4-week structured migration:

**Week 1 — preparation:**
- Hardware acquired (always-on machine + per-partner Trezors).
- LM Studio + models downloaded.
- 4thtech firm domain + dChat workspace provisioned.
- PollinationX storage NFT acquired.
- Ledger cloned to always-on machine.

**Week 2 — parallel operation:**
- Cloud Routines continue.
- Privacy-track equivalents installed in **dry-run** mode (logs to separate file; no Brain commits).
- Daily comparison: do privacy outputs match cloud outputs? Reconcile differences.

**Week 3 — partial cutover:**
- R5, R6 cut over fully (lowest-risk).
- R1, R2 still cloud; privacy in dry-run.
- Comms: founder + 1-2 senior partners on dChat full-time; rest on Slack still.

**Week 4 — full cutover:**
- All Routines on privacy.
- All partners on dChat / dMail.
- Bulk storage on PollinationX.
- Cloud subscriptions cancelled or scoped down (Anthropic API still used for Curator ingest until Gen 2 lands local-LLM ingest).

Migration documented in `firm/privacy-track/migration-runbook.md` per partner per week. Honest framing: **the migration is messy in week 2-3.** The framework's pack does not pretend otherwise.

## 5. Brain interaction protocol

S12 is a privacy-track-setup pack — its writes are *operational artefacts* (hardware register, migration runbook, troubleshooting logs), not partner-contributed firm IP. Per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), operational artefacts live in the **Ledger**; partner-contributed knowledge lives in the **Firm Brain**.

**Reads (Firm Brain — synthesized mirror or git clone):** `entities/partners/<id>` (partner profile), `concepts/theses` (firm theses), `entities/decisions/*` (relevant firm decisions on privacy posture).

**Reads (Ledger):** `firm/privacy-track/*` (prior setup logs, written by this pack), `firm/audit-logs/*` (for troubleshooting cross-references).

**Writes (Ledger only):** `firm/privacy-track/always-on-machine.md` (hardware register); `firm/privacy-track/per-partner-trezor.md` (per-partner inventory + wallet addresses); `firm/privacy-track/migration-runbook.md`; `firm/privacy-track/troubleshooting/*`. These are operational setup logs that need version control + signed commits, not firm-IP knowledge to be synthesized across partners.

**Does not write to the Firm Brain.** S12 is operational; firm-IP authorship (theses, decisions, ADRs about privacy-track adoption rationale) is the founder's / partners' personal-Curator authoring task, pushed via Curator's standard Shared Brain Push.

## 6. Excel interaction protocol

The pack provides the privacy-track equivalent of cloud Excel automation — reads/writes all 9 templates via Excel MCP. Does not own any Excel file directly; is the integration layer.

## 7. Routine integration

Pack provides the privacy-track substrate for all 8 cloud Routines. Execution mechanism differs (cron vs. Anthropic infrastructure); prompts are functionally identical.

## 8. Don'ts

1. Don't store 4thtech wallet seed phrases in Bitwarden or any digital store. Trezor only — paper seed in fire-safe.
2. Don't run the privacy track without an always-on machine.
3. Don't mix cloud and privacy track for the same firm without explicit migration plan (§4.11).
4. Don't skip full-disk encryption on the always-on machine.
5. Don't trust local LLM outputs at the same threshold as Claude Opus. Higher Klarna scrutiny for privacy-track AI replacements (smaller models = more failure modes).
6. Don't expose the always-on machine to public internet. No port forwarding; no public SSH.
7. Don't share Trezor devices between partners. One Trezor per partner identity.
8. Don't auto-update LM Studio or local models without testing — model behaviour changes affect Routine outputs; new versions go through 1-week dry-run.

## 9. Quick reference

| Situation | Action | Output |
|---|---|---|
| Setting up privacy track | §4.2-§4.10 in order | Working privacy-track Brain + Routines |
| Onboarding new partner | Issue Trezor → §4.4 → §4.5 → §4.7 → §4.9 | Partner has dMail/dChat + Excel MCP + GitHub MCP |
| Migrating from cloud | §4.11 4-week runbook | `firm/privacy-track/migration-runbook.md` |
| Cron job missed | Check launchd/cron logs; review UPS state | Incident log + remediation |
| Excel MCP unreachable | Restart server; test via LM Studio chat | Troubleshooting Brain page |
| 4thtech wallet identity lost | Trezor seed restore (per partner); update routing | New wallet address recorded |
| Model upgrade | 1-week dry-run; reconcile outputs; cutover | `always-on-machine.md` updated |

## 10. References

1. **4thtech project** — https://github.com/4thtech and https://wiki.4thtech.io/quickstart/index.
2. **PollinationX** — https://wiki.pollinationx.io/introduction/start-here.
3. **The Curator project** — https://github.com/talirezun/the-curator.
4. **LM Studio MCP support** — https://lmstudio.ai/docs/local-server/mcp.
5. **`haris-musa/excel-mcp-server`** — MIT-licensed; https://github.com/haris-musa/excel-mcp-server.
6. **Desktop Commander MCP** — https://github.com/wonderwhy-er/DesktopCommanderMCP.
7. **GitHub MCP** — https://github.com/modelcontextprotocol/servers/tree/main/src/github.
8. **Trezor Suite** — https://trezor.io/.
9. **Linux Foundation Agentic AI Foundation** — https://lfaidata.foundation/.
10. ØØT `MANIFESTO.md`, Thesis 5 — Composable Lego.
11. ØØT `governance/SECRETS-POLICY.md`.
12. ØØT `routines/SPEC.md` — privacy-track Routine prompts.
