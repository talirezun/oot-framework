# 00 — Quickstart: Privacy Track

**Audience:** Sovereignty-focused founder. Privacy track. Some technical comfort required.
**Time:** Two weekends + 1 week of preparation (~25 hours total). The privacy track is materially more setup work than the cloud track.
**You will end with:** a fully-operational ØØT instance with no cloud dependency for daily operations.

> 📖 **Read first:** [`MANIFESTO.md`](../MANIFESTO.md), [`docs/MODULES.md`](MODULES.md), [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md), [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md), Skill Pack [`skills/privacy-self-sovereign/SKILL.md`](../skills/privacy-self-sovereign/SKILL.md).

> 🤖 **Faster install path:** if you have a coding agent that meets the [capability spec](../installer/agent-assisted/AGENT-CAPABILITY-SPEC.md) — Aider or OpenCode against LM Studio + Qwen 3 32B is the privacy-track-friendly option — use [Path A — Coding-agent-assisted install](../installer/agent-assisted/README.md). The agent walks you through the same setup but does the file-edits, key-generation, and MCP-wiring on your behalf. Total wall-clock similar (the bottleneck is hardware shipping + model download time, not the install steps). Recommended for less-technical founders.

This document is the **manual path** (Path C) — every step is something you type yourself.

> ⚠️ The privacy track requires an **always-on machine** (Mac mini / NUC / Pi 5) and **per-partner Trezors**. For a 5-partner firm: roughly €2,460 one-time + €45–115/month — see the canonical [cost summary](ECOSYSTEM.md#cost-summary). If the cost is prohibitive or you don't yet have a sovereignty mandate, start with the [cloud track](00-quickstart-cloud.md).

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

> 💸 **Choosing the privacy track only to avoid a Claude subscription?** That's a budget motivation, not a sovereignty one — and the privacy track's hardware (Mac mini, UPS, Trezors) costs ~€2,460 up front. If your driver is *budget, not sovereignty*, use the **community track** instead ([ADR-003](../docs/internal/ADR-003-community-track-no-subscription.md)): OpenCode + free models, no Anthropic plan, no dedicated hardware. See [`docs/MODULES.md`](MODULES.md#community-track) + [`installer/agent-assisted/OPENCODE-SETUP.md`](../installer/agent-assisted/OPENCODE-SETUP.md).

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

**Privacy track still uses GitHub** for both the Ledger (Routines push signed commits there for audit trail) and the Firm Brain (Curator Shared Brain — per [ADR-002](../docs/internal/ADR-002-firm-brain-curator-shared-brain.md)). Your firm provisions **two GitHub repos**: `<firm-slug>-ledger` + `<firm-slug>-brain`. Branch protection applies to both. Same Finding 16 caveat as cloud:

| Config | Cost | Branch protection enforced? | Suitable for |
|---|---|---|---|
| **GitHub Team** | $4/user/month per repo seat | ✓ YES | **Recommended default** for any firm taking R6 audit trail + Article 17 erasure seriously |
| **GitHub Enterprise Cloud + EU residency** | ~$21/user/month | ✓ YES + EU storage | **Required today for EU privacy-mandate firms.** GitHub Free/Pro/Team is US-only storage; the Firm Brain holds firm IP, which for an EU firm must reside in the EU. Curator v3.1's Cloudflare R2 will offer a cheaper EU-residency path. |
| **GitHub Public repo** | Free | ✓ YES | Open-source orgs only — your operational data becomes public |
| **GitHub Free + private** | Free | ✗ NO (advisory only) | Solo / 2-person v1 pilot only — **and not on the Firm Brain repo** (the Article 17 audit-trail claim only holds with enforced branch protection) |

EU privacy-mandate firms typically end up on **GitHub Enterprise Cloud with EU data residency** by necessity. Pilots without EU mandates can start on Free + private with procedural discipline; upgrade to Team before adding a third committer. See [`docs/00-quickstart-cloud.md`](00-quickstart-cloud.md) §6 of "decisions" for the longer explanation.

### 8. Firm Brain IP mode

Your **Firm Brain** is a Curator Shared Brain — the firm's synthesized IP layer, populated by partners pushing from their personal Curators (running locally on each partner's machine — privacy-track partners with LM Studio + Qwen) and merged weekly by the admin.

The IP mode is locked once you distribute invite tokens, so decide now:

| Mode | When to pick |
|---|---|
| **`organisational`** (recommended for ØØT firms) | **Default for full-time partners** signing the standard Partner Charter (§8.1 IP-assignment clause). Standard for operating LLCs. |
| **`contributor_retains`** | **For advisors, contractors, outside collaborators.** Especially relevant on the privacy track where partners may explicitly value self-custody of their IP — matches S12's discipline. |

**Attribution flags** default to false (UUID-pseudonymous attribution) — strongly aligned with the privacy track's posture. Surface real names only when explicitly opted in by both firm and contributor.

**Privacy-track caveat — the synthesis LLM is still cloud.** Curator v3.0.0-beta uses Gemini Flash Lite at the admin's weekly Synthesize step. Partners' own Curator MCP interactions run locally on LM Studio; only the admin's weekly synthesis step calls a cloud LLM (~$0.01/week for a 100-page brain with 5 contributors). This is the single remaining cloud-LLM dependency in Gen 1 privacy; Curator v3.1 closes it.

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
2. **Run the model server headless (three-piece stack).** LM Studio is only the model server; the scheduled Routines need three pieces (full detail in [`02-installing-routines-privacy.md`](02-installing-routines-privacy.md) and [`../installer/agent-assisted/OPENCODE-SETUP.md`](../installer/agent-assisted/OPENCODE-SETUP.md)):
   - **`llmster`** — LM Studio's headless daemon (per [lmstudio.ai/docs/developer/core/headless](https://lmstudio.ai/docs/developer/core/headless)); serves the model at `http://127.0.0.1:1234/v1`. Not an agent — it runs no prompts.
   - **`lms`** — LM Studio's CLI: `lms server start`, then `lms load qwen-3-14b-instruct --ttl 3600` to keep the model warm.
   - **OpenCode** — the agent harness (`opencode run`) the schedulers invoke; point its `lmstudio` provider at that endpoint.
3. **MCP servers** configured in OpenCode's `opencode.json` (`mcp` block — not in LM Studio). Add:
   - `my-curator` — Curator MCP.
   - `excel-mcp` — `haris-musa/excel-mcp-server`. `pip install excel-mcp-server` first (optional — human-in-the-loop only; Routines write via openpyxl).
   - `desktop-commander` — local filesystem MCP.
   - `github-mcp` — cross-machine sync.
4. **Self-test:** from OpenCode on the always-on machine, ask: *"Use my-curator; list the firm domains."* Successful response = the stack is configured.
5. **The Curator desktop app** installed on the Mac mini. Cloud-LLM ingest configured (Gemini Flash Lite — Gen 2 will replace with local LLM).

### Sunday afternoon (2-3 hours)

1. **4thtech firm domain.** Acquire your firm's 4thtech dMail domain (e.g. `acme.4thtech` ~€50/year). Configure dChat workspace.
2. **PollinationX storage NFT.** Acquire on the [PollinationX dApp](https://wiki.pollinationx.io/). Sizes: 100GB (small org), 500GB (medium), 1TB+ (regulated). Cost: ~€10-80/month equivalent.
3. **Per-partner read access** to PollinationX granted: `pollinationx grant-read --nft <storage-nft> --to <partner-wallet>` for each partner.
4. **GitHub MCP** configured with PAT (stored in Bitwarden under `shared-services`).
5. **Two GitHub repos created + cloned to the always-on machine.** Per [ADR-002](../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), provision both `<firm-slug>-ledger` (operational state) and `<firm-slug>-brain` (Firm Brain / Curator Shared Brain). The GitHub-side setup (create repos, generate signing key, configure branch protection on **both** repos) is identical to the cloud track — follow [`docs/00-quickstart-cloud.md`](00-quickstart-cloud.md) "Weekend One — Sunday morning" Steps 1, 4, 5, 6, 7, **and 7b** against the always-on machine. Differences from cloud: the local clone paths are under `<FIRM_FOLDER>` on the always-on machine (not your laptop), and the GPG key is generated on the always-on machine.
6. **First Curator domain** created in your personal Second Brain. If Configuration A: add a domain to your existing second-brain. If Configuration B: the Curator's vault root IS `<FIRM_FOLDER>`. First five documents ingested (LM Studio + Qwen for the local-LLM ingest path on the privacy track once Curator v3.1 ships; cloud-LLM ingest in Gen 1).
7. **Firm Brain admin wizard.** Identical to cloud-track Step 8b — open Curator → Shared Brain → Admin Setup → paste the `<firm-slug>-brain` repo URL → name the brain → select IP mode per §8 of "decisions" → save `admin_token` to Bitwarden (founders collection) → generate and save the invite token (`sbi_…`) for future partners. Then run your own contributor wizard (the founder is the first contributor) — paste invite token, create a fine-grained PAT scoped to the Firm Brain repo, select your opted-in `<firm-slug>` domain, consent to IP terms. Verify with a Push → admin Synthesize → Pull loop end-to-end before considering the privacy-track stack done.

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
- **Firm Brain contributor wizard** (identical to cloud-track Step 8 of Weekend Two): share the invite token via 4thtech dMail (not Slack — privacy track uses 4thtech for firm comms). Partner accepts GitHub collaborator invite, creates a fine-grained PAT scoped to the `<firm-slug>-brain` repo (stored in their per-partner Bitwarden collection), selects their opted-in `<firm-slug>` domain, consents to the IP-mode terms surfaced in the wizard (which mirror Partner Charter §8.1). The partner's Curator runs locally on their laptop — they author pages via LM Studio + Qwen MCP interactions, then click Push when ready. Verify the wire-up with a first one-line page Push.

The 30-step onboarding checklist at [`templates/partner-onboarding/checklist.md`](../templates/partner-onboarding/checklist.md) applies identically; the [provisioning script](../templates/partner-onboarding/provisioning-script.sh) auto-detects the privacy track from `firm.yaml`.

---

## What success looks like

- The personal Second Brain has 10–30 ingested documents on the always-on machine.
- The Firm Brain (Curator Shared Brain) has had its first weekly Synthesize; the `<firm-slug>-brain` repo's `collective/<firm-slug>/wiki/` shows synthesized pages with UUID Provenance.
- 4thtech dMail / dChat working for the founder + first partner.
- PollinationX storage configured; first large file uploaded with `[[px:<cid>]]` wikilink in Brain.
- 4 Day-1 Routines firing on schedule on the always-on machine.
- **R9 (admin-run Firm Brain Synthesize)** scheduled for Sunday evenings on the always-on machine (cron `0 19 * * 0` invoking `curator sharedbrain synthesize`).
- Branch protection enforced on **both** GitHub repos (Ledger + Firm Brain), or on EU residency tier if regulatory mandate.
- Cloud subscriptions scoped down to: Curator personal-Second-Brain ingest (Gemini Flash Lite or Anthropic) + Firm Brain weekly Synthesize (admin-run; same LLM). All other operations are sovereign.
- One partner onboarded with their own Trezor + 4thtech identity + PollinationX read access + Curator Shared Brain contributor wizard completed.
- `admin_token` and invite token (`sbi_…`) safely stored in your Bitwarden founders collection.

You are now operating ØØT Generation 1, privacy track.

---

## Common pitfalls (privacy-specific)

1. **Skipping the UPS.** A 6-hour outage kills R1, R2, R5, R6 for that day. The audit-log gap is documented as "no agent activity" but the missed compensation captures hurt.
2. **Storing 4thtech seeds digitally.** This is the single biggest privacy-track failure mode. Paper, fireproof safe, separate location. Always.
3. **Sharing Trezors between partners.** Don't. One Trezor per partner identity. The seed is the partner's, not the firm's.
4. **Auto-updating LM Studio or local models without testing.** Model behaviour changes affect Routine outputs. New versions go through a 1-week dry-run before cutover.
5. **Trying to run R3 (Monthly Variable) on Qwen 3 14B without testing.** R3 is high-stakes. Use Llama 3.3 70B for R3 specifically; the framework's authors learned this the hard way.
6. **Skipping the GitHub plan-tier decision (Finding 16).** Privacy track still uses GitHub for the Ledger. Free + private = advisory branch protection only. Plan to upgrade to Team within 90 days of pilot.
7. **Forgetting that the Curator app still uses cloud-LLM ingest in Gen 1.** Gemini Flash Lite or Anthropic API calls happen during personal Second Brain ingest AND during the admin's weekly Firm Brain Synthesize. Partners' own MCP read/write interactions with their local Second Brain run on LM Studio (local). The privacy track's *local-LLM* ingest + synthesis is Curator v3.1 / Generation 2. For now, your firm's privacy posture is "operational queries are local; document ingest + admin synthesis are cloud-LLM with the API key in your name". Make that explicit in your privacy notice if you ingest customer data.
8. **Skipping the second branch-protection step (the Firm Brain repo).** The cloud-quickstart's Step 7b is essential — without enforced branch protection on the Firm Brain, Curator's Provenance attribution and Article 17 revoke endpoint don't carry meaningful guarantees. Don't treat it as optional just because the Ledger's branch protection is the more-discussed piece.

---

## When to escalate

- **MCP host not connecting** to a server: see Skill Pack S12 §4.7-4.9 for per-MCP install guides; if still failing, open an issue on the relevant MCP's GitHub.
- **4thtech wallet identity lost** (Trezor seed lost): the wallet's contents are unrecoverable per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md). Create a new identity; firm updates routing. This is the price of self-custody.
- **PollinationX storage NFT misconfigured**: the [PollinationX wiki](https://wiki.pollinationx.io/) has a thorough troubleshooting section.
- **Cron job missed** repeatedly: review UPS battery state; consider upgrading to a larger UPS or adding redundant always-on machine.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md) for the eleven legal touchpoints.
