# 00 — Quickstart: Privacy Track

**Audience:** Sovereignty-focused founder. Privacy track. Some technical comfort required.
**Time:** Two weekends + 1 week of preparation (~25 hours total). The privacy track is materially more setup work than the cloud track.
**You will end with:** a fully-operational ØØT instance with no cloud dependency for daily operations.

> 📖 **Read first:** [`MANIFESTO.md`](../MANIFESTO.md), [`docs/MODULES.md`](MODULES.md), [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md), [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md), Skill Pack [`skills/privacy-self-sovereign/SKILL.md`](../skills/privacy-self-sovereign/SKILL.md).

> 🤖 **Faster install path:** if you have a coding agent that meets the [capability spec](../installer/agent-assisted/AGENT-CAPABILITY-SPEC.md) — Aider or OpenCode against LM Studio + Qwen 3 32B is the privacy-track-friendly option — use [Path A — Coding-agent-assisted install](../installer/agent-assisted/README.md). The agent walks you through the same setup but does the file-edits, key-generation, and MCP-wiring on your behalf. Total wall-clock similar (the bottleneck is hardware shipping + model download time, not the install steps). Recommended for less-technical founders.

This document is the **manual path** (Path C) — every step is something you type yourself.

> ⚠️ The privacy track requires an **always-on machine** (Mac mini / NUC / Pi 5) and **per-partner Trezors**. Total one-time cost ~€2,400 + ~€110/year for a 5-partner firm. If the cost is prohibitive or you don't yet have sovereignty mandate, start with the [cloud track](00-quickstart-cloud.md).

---

## What this is + the first 5 minutes

The privacy track replaces every cloud-track tool with a self-sovereign equivalent:

| Cloud (replaced) | Privacy (used here) |
|---|---|
| Anthropic Claude API | LM Studio + Qwen 3 / Llama 3.3 / DeepSeek (local) |
| Slack | 4thtech dChat (on-chain, E2E encrypted) |
| Email / Gmail | 4thtech dMail (wallet-as-identity) |
| Google Drive | Desktop Commander MCP (local filesystem) + PollinationX (decentralised storage for bulk files) |
| Claude Code Routines | OS-native scheduling (cron / launchd / Task Scheduler) on the always-on machine |
| Microsoft Excel + Claude extension | Excel MCP (`haris-musa/excel-mcp-server`) |

By the end of the setup, your data lives on your hardware (Trezor seeds in your fireproof safe; Brain + ledger on your encrypted Mac mini; bulk files on PollinationX you've paid for). The framework's Routines run while the always-on machine is on (and only while it's on — the trade-off vs. cloud).

Total partners using the privacy track typically have one of three motivations: (1) regulatory pressure that disallows cloud LLM ingest of customer data; (2) philosophical / political commitment to self-custody; (3) preparation for Generation 2 stablecoin payroll which requires Trezor identities anyway.

---

## Before you start — decisions to make first

Same decision-making framework as the cloud track plus three privacy-specific items. **Don't skip this section** — each decision affects later steps.

### 1. Confirm sovereignty mandate

If your customers don't require it and your founder doesn't strongly want it, the cloud track is materially less work and equally framework-compliant. Three valid privacy-track motivations: (a) regulatory pressure that disallows cloud-LLM ingest of customer data, (b) philosophical / political commitment to self-custody, (c) Generation 2 stablecoin payroll readiness which requires Trezor identities anyway.

### 2. Always-on machine choice

Mac mini M4 Pro 32GB (~€1,800) is the framework's authors' default. Intel NUC or Raspberry Pi 5 are valid alternatives at lower cost (~€1,200 / ~€350). Per [`skills/privacy-self-sovereign/SKILL.md`](../skills/privacy-self-sovereign/SKILL.md) §4.2.

**Important:** R3 (Monthly Variable Calc) wants Llama 3.3 70B 4-bit which needs ~32-64GB RAM. Pi 5 16GB will run Qwen 3 14B for R1/R2/R5/R6 only; **R3 will fail** unless you upgrade RAM.

### 3. UPS budget

~€80-150 for a small UPS. Strongly recommended — power blips kill missed Routines and break the audit trail.

### 4. EU AI Act exposure

Same as cloud track; privacy track is no exception.

### 5. Where the firm operational repo lives on the always-on machine

Default: `/Users/<oot-user>/<firm-slug>` (macOS) or `/home/<oot-user>/<firm-slug>` (Linux). Pick a path now. Some founders prefer a dedicated path like `/srv/<firm-slug>` on Linux or an external SSD mount.

### 6. Curator integration mode (Configuration A vs B)

Same trade-off as cloud track:

- **Configuration A — Separate** (recommended if you have an existing second-brain on the always-on machine): firm operational repo at `<FIRM_FOLDER>` holds `.xlsx` state and Routine-written markdown. Curator vault stays where it is.
- **Configuration B — Unified** (recommended for greenfield privacy installs — most common case): the firm operational repo IS the Curator's vault root.

For most privacy-track founders setting up a fresh always-on machine: Configuration B.

### 7. GitHub plan-tier — CRITICAL DECISION ⚠️

**Privacy track still uses GitHub for the Ledger** (Routines push signed commits there for audit trail). Same Finding 16 caveat as cloud:

| Config | Cost | Branch protection enforced? | Suitable for |
|---|---|---|---|
| **GitHub Team** | $4/user/month | ✓ YES | **Recommended default** for any firm taking R6 audit trail seriously |
| **GitHub Public repo** | Free | ✓ YES | Open-source orgs only — your operational data becomes public |
| **GitHub Free + private** | Free | ✗ NO (advisory only) | Solo / 2-person v1 pilot only |

Pilots can start on Free + private with procedural discipline; upgrade to Team before adding a third committer. See [`docs/00-quickstart-cloud.md`](00-quickstart-cloud.md) §6 of "decisions" for the longer explanation.

---

## Pre-week — Hardware acquisition (a few days of waiting)

1. **Order the always-on machine.** Mac mini direct from Apple, or NUC from Intel, or Pi 5 from a reputable supplier. Allow 5-10 days delivery.
2. **Order N Trezors** (one per partner, founder included). Direct from [trezor.io](https://trezor.io/) — never accept second-hand or third-party-shipped hardware wallets. Allow 3-7 days delivery.
3. **Order the UPS.** [CyberPower 1500VA](https://www.cyberpowersystems.com/) or APC equivalent (~€140). Same-day or next-day usually.
4. **Order Yubikeys.** Two Yubikey 5C NFCs for org-admin 2FA (~€60 each). Direct from [yubico.com](https://yubico.com/).

While you wait: read MANIFESTO, SPEC, Klarna Test, and Skill Pack S12 fully. ~3 hours of reading. The privacy track has more moving parts; you want the model in your head before you install anything.

---

## Weekend One — Saturday: hardware + OS

### Saturday morning (3-4 hours)

1. **Set up the always-on machine.**
   - macOS: install latest macOS, create a dedicated `oot` user (separate from your personal account), enable **FileVault**, generate Login password via Bitwarden (32-char), disable Touch ID for boot, disable iCloud sync of Documents/Desktop.
   - Linux (NUC/Pi): install Ubuntu Server LTS or Debian, **LUKS full-disk encryption** at install, set up unattended-upgrades, SSH key authentication only (no password).
   - Windows: install Windows 11 Pro, enable **BitLocker**, password + Yubikey 2FA, no remote desktop except VPN'd.
2. **Connect UPS.** Mac mini / NUC / Pi plugged into the UPS; the UPS plugged into wall. UPS drivers installed if needed.
3. **Network setup.** The machine is **not** exposed to the public internet. No port-forwarding. Outbound only for Anthropic API (Curator ingest), GitHub, 4thtech RPC nodes, PollinationX gateways. Tailscale or WireGuard configured if remote access needed.
4. **Bitwarden organisation account.** Same as cloud track. Create org + canonical collections.
5. **Yubikey setup.** Same as cloud — for GitHub admin, Anthropic admin (Curator ingest still uses Anthropic), Bitwarden organisation owner.

### Saturday afternoon (3-4 hours): per-partner Trezors

For each partner including the founder, ~30-45 min:

1. Verify Trezor packaging integrity (tamper-evident seals).
2. Initialise offline. 24-word seed phrase written on paper with pencil. Store in fireproof safe **separate** from the device.
3. Set strong PIN. Optionally set passphrase (the "25th word") with separate paper card.
4. `4thtech-wallet` installed; pair with Trezor.
5. Send test dMail to self via 4thtech client — receipt confirms identity is live.
6. Record wallet's address in `firm/partners/<id>/profile.md`.

> ⚠️ **The seed never goes digital.** Not in Bitwarden. Not in iCloud. Not in a photo. Not in a password manager. Paper, fireproof safe, separate location from the device. This is non-negotiable per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md).

---

## Weekend One — Sunday: software stack

### Sunday morning (3-4 hours)

1. **LM Studio.** Download from [lmstudio.ai](https://lmstudio.ai/). Install on the always-on machine. Download models:
   - **Qwen 3 14B Instruct** (~9 GB, 4-bit quantised) — default daily driver.
   - **Qwen 3 9B Instruct** (~5 GB) — fallback for smaller machines.
   - **Llama 3.3 70B Instruct** (~40 GB, 4-bit quantised) — for R3 (Monthly Variable Calc) which is high-stakes.
   - **DeepSeek-V3** — strong on code; pair with Skill Pack S4 if engineering-heavy firm.
2. **Headless mode** enabled. `llmster` CLI installed to `/usr/local/bin/llmster`.
3. **MCP host config** in LM Studio. Add:
   - `my-curator` — Curator MCP.
   - `excel-mcp` — `haris-musa/excel-mcp-server`. `pip install excel-mcp-server` first.
   - `desktop-commander` — local filesystem MCP.
   - `github-mcp` — cross-machine sync.
4. **Self-test:** open Claude Desktop on your laptop (paired to LM Studio over Tailscale), or use LM Studio's built-in chat. Ask: *"List the firm domains via my-curator's list_domains tool."* Successful response = MCP host configured.
5. **The Curator desktop app** installed on the Mac mini. Cloud-LLM ingest configured (Gemini Flash Lite — Gen 2 will replace with local LLM).

### Sunday afternoon (2-3 hours)

1. **4thtech firm domain.** Acquire your firm's 4thtech dMail domain (e.g. `acme.4thtech` ~€50/year). Configure dChat workspace.
2. **PollinationX storage NFT.** Acquire on the [PollinationX dApp](https://wiki.pollinationx.io/). Sizes: 100GB (small org), 500GB (medium), 1TB+ (regulated). Cost: ~€10-80/month equivalent.
3. **Per-partner read access** to PollinationX granted: `pollinationx grant-read --nft <storage-nft> --to <partner-wallet>` for each partner.
4. **GitHub MCP** configured with PAT (stored in Bitwarden under `shared-services`).
5. **Ledger** cloned to the always-on machine. **Note:** the GitHub-side setup (create repo, generate signing key, configure branch protection, the clean branch-protection checkbox table) is identical to the cloud track — follow [`docs/00-quickstart-cloud.md`](00-quickstart-cloud.md) "Weekend One — Sunday morning" Steps 1, 4, 5, 6, 7 against the always-on machine. The only differences: the local clone path is `<FIRM_FOLDER>` on the always-on machine (not your laptop), and the GPG key is generated on the always-on machine.
6. **First Curator domain** created. If Configuration A: add a domain to your existing second-brain. If Configuration B: the Curator's vault root IS `<FIRM_FOLDER>`. First five documents ingested.

---

## Weekend Two — Saturday: configure cron equivalents (R1, R2, R5, R6)

Each Routine has detailed setup at `routines/privacy/<R>.md`. Recommended order (no dependencies first):

1. **R5 — Brain Health Check** (Sunday 09:00). [`routines/privacy/R5.md`](../routines/privacy/R5.md).
2. **R6 — EU AI Act Audit Trail** (daily 23:00). **Pre-requisite:** GitHub branch protection configured (force-push disabled, signed commits required, ≥1 reviewer for `firm/audit-logs/*`). GPG signing key on the always-on machine; `gpg-agent` configured for 24h passphrase cache. [`routines/privacy/R6.md`](../routines/privacy/R6.md).
3. **R1 — Daily Output Capture** (daily 18:00). **Pre-requisite:** at least one partner onboarded. [`routines/privacy/R1.md`](../routines/privacy/R1.md).
4. **R2 — Weekly BR Prep** (Friday 08:00). **Pre-requisite:** R1 has 7+ days of data. [`routines/privacy/R2.md`](../routines/privacy/R2.md).

For each Routine: install the launchd plist (macOS) or cron entry (Linux) per the routine's file. Manual test fire after install. Verify expected outputs.

---

## Weekend Two — Sunday: onboard first partner

Same as cloud track ([`docs/00-quickstart-cloud.md`](00-quickstart-cloud.md) Weekend Two), with privacy-specific differences:

- Comms training: the partner needs to learn dMail and dChat, not Gmail and Slack.
- Wallet setup: partner already has their own Trezor (issued during pre-week). They create their 4thtech wallet identity if not done already.
- Storage training: PollinationX for bulk; Ledger (synced via GitHub MCP) for everything else.

The 30-step onboarding checklist at [`templates/partner-onboarding/checklist.md`](../templates/partner-onboarding/checklist.md) applies identically; the [provisioning script](../templates/partner-onboarding/provisioning-script.sh) auto-detects the privacy track from `firm.yaml`.

---

## What success looks like

- The Brain has 10–30 ingested documents on the always-on machine.
- 4thtech dMail / dChat working for the founder + first partner.
- PollinationX storage configured; first large file uploaded with `[[px:<cid>]]` wikilink in Brain.
- 4 Day-1 Routines firing on schedule on the always-on machine.
- Cloud subscriptions scoped down to: Curator ingest only (Gemini Flash Lite or Anthropic). All other operations are sovereign.
- One partner onboarded with their own Trezor + 4thtech identity + PollinationX read access.

You are now operating ØØT Generation 1, privacy track.

---

## Common pitfalls (privacy-specific)

1. **Skipping the UPS.** A 6-hour outage kills R1, R2, R5, R6 for that day. The audit-log gap is documented as "no agent activity" but the missed compensation captures hurt.
2. **Storing 4thtech seeds digitally.** This is the single biggest privacy-track failure mode. Paper, fireproof safe, separate location. Always.
3. **Sharing Trezors between partners.** Don't. One Trezor per partner identity. The seed is the partner's, not the firm's.
4. **Auto-updating LM Studio or local models without testing.** Model behaviour changes affect Routine outputs. New versions go through a 1-week dry-run before cutover.
5. **Trying to run R3 (Monthly Variable) on Qwen 3 14B without testing.** R3 is high-stakes. Use Llama 3.3 70B for R3 specifically; the framework's authors learned this the hard way.
6. **Skipping the GitHub plan-tier decision (Finding 16).** Privacy track still uses GitHub for the Ledger. Free + private = advisory branch protection only. Plan to upgrade to Team within 90 days of pilot.
7. **Forgetting that the Curator app still uses cloud-LLM ingest in Gen 1.** Gemini Flash Lite or Anthropic API calls happen during ingest. The privacy track's local-LLM ingest is Generation 2. For now, your firm's privacy posture is "operational queries are local; document ingest is cloud-LLM with the API key in your name". Make that explicit in your privacy notice if you ingest customer data.

---

## When to escalate

- **MCP host not connecting** to a server: see Skill Pack S12 §4.7-4.9 for per-MCP install guides; if still failing, open an issue on the relevant MCP's GitHub.
- **4thtech wallet identity lost** (Trezor seed lost): the wallet's contents are unrecoverable per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md). Create a new identity; firm updates routing. This is the price of self-custody.
- **PollinationX storage NFT misconfigured**: the [PollinationX wiki](https://wiki.pollinationx.io/) has a thorough troubleshooting section.
- **Cron job missed** repeatedly: review UPS battery state; consider upgrading to a larger UPS or adding redundant always-on machine.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md) for the eleven legal touchpoints.
