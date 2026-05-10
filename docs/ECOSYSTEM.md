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
- **Cost:** Pro (~€20/month) or Max (~€100/month). Max recommended for partners using Claude Code heavily.

### Google Workspace
- **What:** Drive, Sheets, Docs, Calendar, Gmail.
- **Why ØØT uses it:** the cloud-track substrate. Claude has official Anthropic connectors that read these.
- **Site:** [workspace.google.com](https://workspace.google.com/)
- **When you'll meet it:** Saturday morning. Provision a Workspace tenant.
- **Cost:** Business Standard ~€12/user/month.

### Slack
- **What:** team communication.
- **Why ØØT uses it:** the cloud-track comms layer; standing channels for `#output-log`, `#business-review`, `#klarna-test`, `#compensation`, `#change`, `#brain-health`, `#ops`.
- **Claude integration:** [Claude Slack app](https://slack.com/apps/A0848GFRZ54-claude)
- **When you'll meet it:** Saturday morning. Create workspace; install Claude integration.
- **Cost:** Free tier works for ≤6 partners; Pro at €7-10/user/month otherwise.

### Microsoft Excel
- **What:** alternative to Google Sheets for the cloud track. Has its own Claude extension.
- **Why ØØT uses it:** for firms that prefer Microsoft to Google.
- **When you'll meet it:** if you choose this over Sheets.
- **Cost:** ~€10/user/month for Microsoft 365 Business Basic.

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

### Excel MCP
- **What:** MCP server that lets local LLMs read/write Excel files.
- **Why ØØT uses it:** privacy-track equivalent of Google Sheets API; the framework's 9 Excel templates land via this.
- **Repo:** [github.com/haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) — MIT-licensed
- **When you'll meet it:** Sunday of Weekend One. `pip install excel-mcp-server`.
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
- **When you'll meet it:** Pre-week (order); Saturday of Weekend One (initialise per partner).
- **Cost:** ~€80 per Trezor; one per partner.

---

## Both-track tools

### The Curator (the reference Brain implementation)
- **What:** open-source desktop app + MyCuratorMCP server (17 tools).
- **Why ØØT uses it:** Skill Pack S1 imports the Curator's `SKILL.md` verbatim. The Brain is the framework's compounding-IP substrate.
- **Repo + research:** [github.com/talirezun/the-curator](https://github.com/talirezun/the-curator)
- **Research articles:** [github.com/talirezun/the-curator/tree/main/research](https://github.com/talirezun/the-curator/tree/main/research)
- **When you'll meet it:** Sunday morning of Weekend One. Install + first ingest. See [`docs/01-installing-the-curator.md`](01-installing-the-curator.md).
- **Cost:** free app + cloud-LLM ingest at ~€5-10/month per heavy user.

### Bitwarden
- **What:** open-source password manager (or 1Password as commercial alternative).
- **Why ØØT uses it:** software credentials per the secrets policy. API keys, OAuth tokens, recovery codes.
- **Site:** [bitwarden.com](https://bitwarden.com/)
- **CLI:** [bitwarden.com/help/cli](https://bitwarden.com/help/cli/)
- **Self-hostable:** [Vaultwarden](https://github.com/dani-garcia/vaultwarden) (lightweight Bitwarden server)
- **When you'll meet it:** Saturday morning of Weekend One.
- **Cost:** Family ~€40/year + Org ~€60/year. Self-hosted Vaultwarden is free.

### GitHub
- **What:** version control, issue tracking, PR review, CI.
- **Why ØØT uses it:** the Brain sync substrate; the protected audit-log branch lives here; the `oot/klarna-test` status check runs here.
- **Site:** [github.com](https://github.com/)
- **CLI:** [cli.github.com](https://cli.github.com/)
- **When you'll meet it:** Saturday morning of Weekend One. Create org; create Brain repo; configure 5 setup pre-requisites per Skill Pack S4 §4.0.
- **Cost:** free for public repos; Team plan ~€4/user/month for private repos.

### Yubikey
- **What:** hardware security key for org-admin 2FA.
- **Why ØØT uses it:** GitHub admin, Anthropic admin, Google admin, Bitwarden organisation owner.
- **Site:** [yubico.com](https://yubico.com/)
- **When you'll meet it:** Saturday morning of Weekend One. Two Yubikeys (primary + backup) for the founder.
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

### Cloud track (10-partner firm)

| Item | One-time | Monthly |
|---|---|---|
| Anthropic seats (Pro) | — | ~€200 |
| Google Workspace | — | ~€120 |
| Slack | — | ~€80 |
| GitHub Team | — | ~€40 |
| Bitwarden Org | — | ~€10 |
| Curator pay-as-you-go | — | ~€20 |
| Yubikey (founder + 1 backup) | ~€120 | — |
| **Total** | **~€120** | **~€470** |

Plus counsel: €5-15k initial; €3-8k/year ongoing.

### Privacy track (5-partner firm)

| Item | One-time | Monthly |
|---|---|---|
| Mac mini M4 Pro 32GB | ~€1,800 | — |
| UPS (CyberPower 1500VA) | ~€140 | — |
| 5 Trezors (one per partner) | ~€400 | — |
| 2 Yubikeys (founder + backup) | ~€120 | — |
| Bitwarden Org | — | ~€10 |
| 4thtech firm domain | — | ~€5 |
| PollinationX storage NFT (200GB) | — | ~€20 |
| Curator pay-as-you-go (Gen 1) | — | ~€10 |
| Electricity (always-on machine) | — | ~€10 |
| **Total** | **~€2,460** | **~€55** |

Plus counsel: same as cloud.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Cost figures are illustrative; verify with current vendor pricing.
