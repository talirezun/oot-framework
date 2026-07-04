# Ecosystem — External Tools the Framework Depends On

**Audience:** Non-technical founder picking up the framework for the first time.
**Time:** 20 minutes.
**You will end with:** a clear mental model of every external tool, what it's for, when you'll meet it, and where its own documentation lives.

> 📖 **The comprehensive citation-style index is at** [`research/external-resources.md`](../research/external-resources.md). This doc is the plain-language version.

---

## What this is + the first 5 minutes

ØØT runs on a stack of well-documented external tools. Each has its own wiki or docs site. The framework links to those rather than duplicating them. Your job: install the right tools in the right order; read the right wikis when you get stuck.

**The decision tree**:

1. **Cloud track or privacy track?**
   - **Cloud** = fastest, easiest, depends on Anthropic + Google + Slack as cloud services.
   - **Privacy** = sovereign, self-hosted, needs an always-on machine + Trezors + 4thtech + PollinationX.
2. **Are you in the EU?** EU AI Act compliance materially shapes Routine R6 + Skill Pack S7.
3. **What's your one-time + ongoing budget?**

---

## Cloud track (canonical, fastest path)

### Anthropic Claude
- **What:** the cloud track's daily driver. Includes Claude Desktop, Claude Code, [Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code), the Anthropic API.
- **Why ØØT uses it:** the framework's reference cloud-track implementation.
- **Site:** [claude.com](https://claude.com/)
- **Docs:** [docs.claude.com](https://docs.claude.com/)
- **When you'll meet it:** Saturday morning of Weekend One. You'll create an account, install Claude Desktop, configure Claude Code.
- **Cost:** Pro (~€20/month) or Max (~€100/month). **Plan-tier guidance:** Pro is enough for a solo or 2-partner firm with no active Klarna gate (R7); Max is the choice for 3+ partner firms or any firm running the Klarna gate. See the plan-tier + Routine per-day limits table in [`docs/02-installing-routines.md`](02-installing-routines.md) — that is the single canonical home for those numbers.

### Google Workspace (optional)
- **What:** Drive, Sheets, Docs, Calendar, Gmail.
- **Why ØØT uses it:** **optional** on the cloud track. If your firm already lives in Google Workspace, Claude's official read-only Drive connector can read documents into a conversation. It is **not** a provisioning step and **not** a state store — your operational `.xlsx` state lives in the Ledger repo per [ADR-001](internal/ADR-001-cloud-routine-excel-writeback.md), never in Google Sheets.
- **Site:** [workspace.google.com](https://workspace.google.com/)
- **When you'll meet it:** only if you already use it and want the read-only connector. Skip entirely otherwise — nothing in the framework requires it.
- **Cost:** Business Standard ~€12/user/month (only if you already pay for it; not counted in the framework's cost tables below).

### Slack
- **What:** team communication.
- **Why ØØT uses it:** the cloud-track comms layer; standing channels for `#output-log`, `#business-review`, `#klarna-test`, `#compensation`, `#change`, `#brain-health`, `#ops`.
- **Claude integration:** [Claude Slack app](https://slack.com/apps/A0848GFRZ54-claude)
- **When you'll meet it:** Saturday morning. Create workspace; install Claude integration.
- **Cost:** Free tier works for small teams (≤10); Pro at €7-10/user/month otherwise.

### Your spreadsheet app (user choice)
- **What:** a viewer for the framework's 9 `.xlsx` templates — Microsoft Excel, LibreOffice Calc (free, open-source), Apple Numbers, or Excel for Web all work.
- **Why ØØT uses it:** the `.xlsx` files are the firm's operational state, but you only ever *view* them by hand — the Routines mutate them programmatically via openpyxl + signed commits in the Ledger repo (per [ADR-001](internal/ADR-001-cloud-routine-excel-writeback.md)), not through any spreadsheet app. The state lives in the Ledger; the app is just how a human reads it.
- **When you'll meet it:** whenever you want to eyeball a ledger row. Pick whichever app you already have.
- **Cost:** free (LibreOffice / Numbers / Excel for Web) or whatever you already pay for Microsoft 365. Not a framework-required cost.

---

## Privacy track (full Gen 1 parity, sovereignty-first)

### LM Studio
- **What:** local LLM runner with native MCP support (≥0.3.17).
- **Why ØØT uses it:** the privacy-track default model host. Runs Qwen 3, Llama 3.x, DeepSeek, gpt-oss locally.
- **Site:** [lmstudio.ai](https://lmstudio.ai/)
- **MCP docs:** [lmstudio.ai/docs/local-server/mcp](https://lmstudio.ai/docs/local-server/mcp)
- **When you'll meet it:** Sunday of Weekend One. Install on the always-on machine; download Qwen 3 14B + Llama 3.3 70B (for R3).
- **Cost:** free. Hardware cost: ~€1,800 for a Mac mini M4 Pro 32GB.

### 4thtech (dMail, dChat, file transfer)
- **What:** on-chain end-to-end-encrypted communication. Wallet-as-identity.
- **Why ØØT uses it:** the privacy-track replacement for Slack + email.
- **Wiki:** [wiki.4thtech.io](https://wiki.4thtech.io/) — full documentation
- **Quickstart:** [wiki.4thtech.io/quickstart/index](https://wiki.4thtech.io/quickstart/index)
- **Repo:** [github.com/4thtech](https://github.com/4thtech)
- **When you'll meet it:** Pre-week (Trezor setup) + Weekend One Sunday afternoon (4thtech firm domain + dChat workspace).
- **Cost:** ~€50/year for the firm dMail domain. Per-partner Trezor (~€80) one-time.

### PollinationX
- **What:** decentralised storage with NFT-based capacity. Encrypted, distributed across nodes.
- **Why ØØT uses it:** the privacy-track replacement for Google Drive — bulk storage for recordings, videos, large attachments.
- **Wiki:** [wiki.pollinationx.io](https://wiki.pollinationx.io/) — full documentation
- **Start here:** [wiki.pollinationx.io/introduction/start-here](https://wiki.pollinationx.io/introduction/start-here)
- **When you'll meet it:** Sunday of Weekend One. Acquire storage NFT; install client.
- **Cost:** ~€10-80/month equivalent depending on storage size (100GB / 500GB / 1TB+).

### Excel MCP (optional)
- **What:** MCP server that lets a local LLM read/write Excel files interactively.
- **Why ØØT uses it:** **optional, human-in-the-loop only.** It is a convenience for a partner who wants to ask a local LLM to inspect or tweak a spreadsheet in conversation. It is **not** how the framework's 9 templates land, and **not** how the Routines write pay data — Routines (cloud and privacy alike) mutate the `.xlsx` files directly via openpyxl + signed commits in the Ledger repo (per [ADR-001](internal/ADR-001-cloud-routine-excel-writeback.md)). You can run the whole framework without ever installing Excel MCP.
- **Repo:** [github.com/haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) — MIT-licensed
- **When you'll meet it:** only if you want conversational spreadsheet edits. `pip install excel-mcp-server`.
- **Cost:** free.

### Desktop Commander MCP
- **What:** local filesystem MCP server.
- **Why ØØT uses it:** the privacy-track replacement for the Google Drive Anthropic connector.
- **Repo:** [github.com/wonderwhy-er/DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)
- **When you'll meet it:** Sunday of Weekend One.
- **Cost:** free.

### GitHub MCP
- **What:** MCP server for GitHub operations.
- **Why ØØT uses it:** cross-machine Brain sync; reads/writes commits, PRs, issues.
- **Repo:** [github.com/modelcontextprotocol/servers/tree/main/src/github](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- **When you'll meet it:** Sunday of Weekend One.
- **Cost:** free.

### Trezor
- **What:** open-source hardware wallet.
- **Why ØØT uses it:** stores 4thtech wallet identity keys, treasury wallet keys (Gen 2), payroll wallet keys (Gen 2).
- **Site:** [trezor.io](https://trezor.io/) — order direct only
- **When you'll need it:** **privacy track Day-1** (each partner's 4thtech identity is a Trezor-backed wallet — see Skill Pack S12). On the **cloud track**, a Trezor is **not needed in Gen 1** — the crypto keys it protects (stablecoin payroll, treasury) don't come into play until Gen 2. Cloud founders can add Trezors when they adopt Gen 2 rails. Per `governance/SECRETS-POLICY.md` Gen-1 tiering.
- **Cost:** ~€80 per Trezor; one per partner (privacy track).

---

## Both-track tools

### Coding agents (the install + daily-ops harness)
- **What:** the coding-agent harness that runs the install plan and, in Gen 1, drives daily operations. The framework is **LLM-agnostic** — it needs an agent that meets the behaviour bar in [`installer/agent-assisted/AGENT-CAPABILITY-SPEC.md`](../installer/agent-assisted/AGENT-CAPABILITY-SPEC.md), not any specific model or vendor.
- **Claude Code (reference):** Anthropic's CLI agent; the harness the framework's authors test against first. Native MCP, signed commits, long context. Runs on a Pro / Max / Team plan (see Anthropic Claude above for plan-tier guidance).
- **OpenCode (the no-subscription harness):** open-source, free — point it at free or local models (including an LM Studio endpoint) and you can install and operate the framework with **no Anthropic subscription**. Native MCP. The framework's fuller first-class support for OpenCode is in progress (see ADR-003, in flight). Repo: [github.com/sst/opencode](https://github.com/sst/opencode).
- **Also known-compatible:** Augment Code (strong multi-file builds), Aider (minimalist; works against any OpenAI-compatible API including local LM Studio), Cline (VSCode extension, broad model support). Per [`AGENT-CAPABILITY-SPEC.md`](../installer/agent-assisted/AGENT-CAPABILITY-SPEC.md) §Known compatible agents.
- **When you'll meet it:** the very first install step — you paste [`installer/agent-assisted/START-HERE.md`](../installer/agent-assisted/START-HERE.md) into your chosen agent and let it drive.
- **Cost:** Claude Code needs an Anthropic plan; OpenCode + Aider + Cline are free (you pay only for whatever model/API you point them at, or nothing if you run local models).

### The Curator (the reference Brain implementation)
- **What:** open-source desktop app + MyCuratorMCP server (17 tools) + **Shared Brain primitive** (v3.0.0-beta+).
- **Why ØØT uses it:** Skill Pack S1 imports the Curator's `SKILL.md` verbatim. Each partner's personal **Second Brain** is a Curator vault on their own machine. Per [ADR-002](internal/ADR-002-firm-brain-curator-shared-brain.md), the firm's collective IP (the **Firm Brain**) is a Curator Shared Brain instance — partners push from their opted-in domain, the admin runs weekly Synthesize.
- **Version requirement (Gen 1):** **Curator v3.0.0-beta+** for Shared Brain support. Older versions support only personal Second Brain. If you're on Curator v2.x, upgrade before completing the install — the Firm Brain step in the install plan requires Shared Brain features.
- **Shared Brain features:** (1) opted-in domain contribution with `DeltaSummary` preprocessing — only the opted-in domain leaves the partner's machine; (2) Jaccard + selective-LLM conflict resolution at synthesis; (3) UUID-pseudonymous Provenance attribution with optional double-gated name-attribution; (4) `data_handling_terms` field (`organisational` vs `contributor_retains`) locked at admin setup; (5) GDPR Article 17 revoke endpoint with typed-confirmation safety gate.
- **Repo + research:** [github.com/talirezun/the-curator](https://github.com/talirezun/the-curator)
- **Shared Brain docs:** [shared-brain.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md) (user guide), [shared-brain-admin.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-admin.md), [shared-brain-compliance.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-compliance.md), [shared-brain-design.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-design.md).
- **Research articles:** [github.com/talirezun/the-curator/tree/main/research](https://github.com/talirezun/the-curator/tree/main/research)
- **When you'll meet it:** Sunday morning of Weekend One. Install + first ingest + Firm Brain admin wizard. See quickstart §Step 8 / 8b.
- **Gen 1 cloud-LLM dependency (single remaining):** Curator v3.0.0-beta uses Gemini Flash Lite at personal Second Brain ingest AND at the admin's weekly Firm Brain Synthesize step. Partners' own MCP read/write interactions on the privacy track can run fully on a local LLM (LM Studio + Qwen/Llama/DeepSeek). **Curator v3.1 (Gen 2 alignment)** ships local-LLM ingest + local-LLM synthesis, plus a Cloudflare R2 backend with `jurisdiction = "eu"` for EU residency at lower cost than GitHub Enterprise Cloud.
- **Cost:** free app + cloud-LLM ingest + admin weekly synthesis at ~€5-10/month per heavy user; Firm Brain synthesis ~$0.01/week for a 100-page brain with 5 contributors.

### Bitwarden
- **What:** open-source password manager (or 1Password as commercial alternative).
- **Why ØØT uses it:** software credentials per the secrets policy. API keys, OAuth tokens, recovery codes.
- **Site:** [bitwarden.com](https://bitwarden.com/)
- **CLI:** [bitwarden.com/help/cli](https://bitwarden.com/help/cli/)
- **Self-hostable:** [Vaultwarden](https://github.com/dani-garcia/vaultwarden) (lightweight Bitwarden server)
- **When you'll need it:** a **personal** Bitwarden vault is recommended Day-1 for any founder (best practice for storing API keys and tokens). A Bitwarden **organisation** is only needed once you have **2+ admins** sharing firm credentials — a solo or 2-admin firm can start with personal vaults and add the org when the firm grows. Per `governance/SECRETS-POLICY.md` Gen-1 tiering (decision #13).
- **Cost:** personal Family plan ~€40/year; Org ~€60/year (only when 2+ admins). Self-hosted Vaultwarden is free.

### GitHub
- **What:** version control, issue tracking, PR review, CI.
- **Why ØØT uses it:** the Ledger sync substrate; the protected audit-log branch lives here; the `oot/klarna-test` status check runs here.
- **Site:** [github.com](https://github.com/)
- **CLI:** [cli.github.com](https://cli.github.com/)
- **When you'll meet it:** Saturday morning of Weekend One. Create org; create Ledger; configure 5 setup pre-requisites per Skill Pack S4 §4.0.
- **Cost:** free for public repos; Team plan ~€4/user/month for private repos.

### Yubikey
- **What:** hardware security key for org-admin 2FA.
- **Why ØØT uses it:** GitHub admin, Anthropic admin, Bitwarden organisation owner.
- **Site:** [yubico.com](https://yubico.com/)
- **When you'll need it:** best practice once you have **2+ admins** protecting shared org accounts. A solo founder can start with app-based 2FA and add Yubikeys (primary + backup) as the firm matures — not gating for Gen 1. Per `governance/SECRETS-POLICY.md` Gen-1 tiering (decision #13).
- **Cost:** ~€60 per key.

### Obsidian (optional)
- **What:** local markdown editor.
- **Why ØØT uses it:** human-readable view of the Brain. Obsidian-compatible markdown is the Brain's storage format.
- **Site:** [obsidian.md](https://obsidian.md/)
- **When you'll meet it:** anytime after first Brain ingest.
- **Cost:** free for personal use; Sync ~€8/month is optional.

---

## Standards bodies (read these to understand the framework's foundations)

### Linux Foundation Agentic AI Foundation (AAIF)
- **What:** the standards body governing MCP, AGENTS.md, MCP server cards (since December 2025).
- **Site:** [lfaidata.foundation](https://lfaidata.foundation/)

### Model Context Protocol (MCP)
- **What:** the open standard for agent ↔ tool communication.
- **Spec:** [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Servers index:** [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

### Anthropic Agent Skills (SKILL.md format)
- **Docs:** [docs.claude.com/en/docs/agents-and-tools/agent-skills/overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

---

## Reading order for the ecosystem

If you have 30 minutes to understand the framework's external dependencies before installing anything:

1. **The Curator's README** ([github.com/talirezun/the-curator](https://github.com/talirezun/the-curator)) — 5 min.
2. **MCP overview** ([modelcontextprotocol.io](https://modelcontextprotocol.io/)) — 5 min.
3. **4thtech wiki Quickstart** (privacy track) — 10 min.
4. **PollinationX Start Here** (privacy track) — 5 min.
5. **Anthropic Skills overview** — 5 min.

Then come back to the framework's [`QUICKSTART.md`](../QUICKSTART.md) and start installing.

---

## Cost summary

> 💰 **This is the framework's canonical cost page.** Other docs (the FAQ, the quickstarts) link here rather than restating figures. If you find a cost number elsewhere in the framework that disagrees with this table, this table wins — please open a PR fixing the other doc to link here.
>
> **Plan-tier assumption baked into these tables:** per the plan-tier guidance in [`docs/02-installing-routines.md`](02-installing-routines.md), a firm with **3+ partners or an active Klarna gate runs Anthropic Max (~€100/user/month)**; a solo or 2-partner firm with no Klarna-gate activity can run Pro (~€20/user/month). The tables below price the honest Max seats for multi-partner firms — earlier drafts under-counted this by pricing Pro seats.

### Cloud track — 3-partner starter

The smallest realistic cloud firm, so small teams can see the real entry cost.

| Item | One-time | Monthly |
|---|---|---|
| Anthropic seats — 3 × Max (~€100) | — | ~€300 |
| GitHub Team — 3 × €4 | — | ~€12 |
| Curator pay-as-you-go | — | ~€10 |
| Slack | — | €0 (free tier, ≤10) |
| Bitwarden (personal vaults; org only at 2+ admins) | — | €0–€10 |
| **Total** | **~€0** | **~€320–€330** |

Bitwarden org, Yubikeys, and Google Workspace are **optional in Gen 1** (see decision #13 above) — a 3-partner firm can start with none of them.

### Cloud track — 10-partner firm

| Item | One-time | Monthly |
|---|---|---|
| Anthropic seats — 10 × Max (~€100) | — | ~€1,000 |
| GitHub Team — 10 × €4 | — | ~€40 |
| Curator pay-as-you-go | — | ~€20 |
| Slack (free ≤10; Pro if you exceed free features) | — | €0–€80 |
| Bitwarden Org (2+ admins) | — | ~€10 |
| Yubikey (founder + 1 backup) | ~€120 | — |
| **Total** | **~€120** | **~€1,070–€1,150** |

Google Workspace is **optional** (read-only connector only; not required — see the Google Workspace entry above) and is not counted here. If your firm already pays for it, add ~€12/user/month.

Plus counsel: €5-15k initial; €3-8k/year ongoing.

### Privacy track (5-partner firm)

| Item | One-time | Monthly |
|---|---|---|
| Mac mini M4 Pro 32GB | ~€1,800 | — |
| UPS (CyberPower 1500VA) | ~€140 | — |
| 5 Trezors (one per partner — privacy Day-1) | ~€400 | — |
| 2 Yubikeys (founder + backup; add at 2+ admins) | ~€120 | — |
| Bitwarden Org (2+ admins) | — | ~€10 |
| 4thtech firm domain | — | ~€5 |
| PollinationX storage NFT (200GB) | — | ~€10–€80 (by size) |
| Curator pay-as-you-go (Gen 1) | — | ~€10 |
| Electricity (always-on machine) | — | ~€10 |
| **Total** | **~€2,460** | **~€45–€115** |

The privacy track runs no Anthropic seats (local models via LM Studio), which is why its monthly is far below the cloud track's despite the hardware one-time. Plus counsel: same as cloud.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Cost figures are illustrative; verify with current vendor pricing.
