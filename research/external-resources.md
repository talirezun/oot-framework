# External Resources — the ØØT Ecosystem

A curated index of every external tool, project, wiki, standards body, and reference framework the ØØT framework depends on or cross-references. This is the canonical place to land if you're new and want to understand the ecosystem the framework operates in.

Each entry includes: what it is, why ØØT uses it, the canonical URL, the licence, and which ØØT components depend on it.

---

## Reference Brain implementation

### The Curator
- **What:** the canonical Brain implementation. Open-source desktop app + the MyCuratorMCP server (17 tools).
- **Why ØØT uses it:** Skill Pack S1 imports the Curator's `SKILL.md` verbatim. The Brain is the substrate every other Skill Pack writes to.
- **Repo:** https://github.com/talirezun/the-curator
- **Wiki / docs:** in-repo at `https://github.com/talirezun/the-curator/blob/main/README.md`
- **Research articles:** https://github.com/talirezun/the-curator/tree/main/research
- **Skill Pack:** S1 — `skills/my-curator/`
- **Licence:** open-source (see repo).

---

## Privacy-track stack

### 4thtech (dMail, dChat, file transfer)
- **What:** on-chain end-to-end-encrypted communication and file-transfer framework. Wallet-as-identity, fully self-custodial, permissionless.
- **Why ØØT uses it:** the privacy-track replacement for Slack + email. Per-partner identity is a Trezor-controlled wallet.
- **Wiki:** https://wiki.4thtech.io/
- **Quickstart:** https://wiki.4thtech.io/quickstart/index
- **Repo:** https://github.com/4thtech
- **Skill Pack:** S12 — `skills/privacy-self-sovereign/`
- **Licence:** open-source (see repo).

### PollinationX
- **What:** decentralised storage protocol. NFT-based capacity. Encrypted, distributed across nodes.
- **Why ØØT uses it:** the privacy-track replacement for Google Drive — bulk storage for recordings, videos, large attachments.
- **Wiki:** https://wiki.pollinationx.io/
- **Quickstart:** https://wiki.pollinationx.io/introduction/start-here
- **Skill Pack:** S12.

### LM Studio
- **What:** local LLM runner with native MCP support (≥0.3.17).
- **Why ØØT uses it:** the privacy-track default model host. Runs Qwen 3, Llama 3.x, DeepSeek, gpt-oss locally.
- **Site:** https://lmstudio.ai/
- **MCP docs:** https://lmstudio.ai/docs/local-server/mcp
- **Skill Pack:** S12.

### Excel MCP
- **What:** Model Context Protocol server for Excel files. MIT-licensed.
- **Why ØØT uses it:** privacy-track equivalent of Google Sheets API; gives local LLMs read/write access to the 9 ØØT Excel templates.
- **Repo:** https://github.com/haris-musa/excel-mcp-server
- **Skill Pack:** S12.

### Desktop Commander MCP
- **What:** filesystem MCP server.
- **Why ØØT uses it:** privacy-track replacement for the Google Drive Claude connector.
- **Repo:** https://github.com/wonderwhy-er/DesktopCommanderMCP
- **Skill Pack:** S12.

### GitHub MCP
- **What:** Model Context Protocol server for GitHub operations.
- **Why ØØT uses it:** cross-machine Brain sync; reads/writes commits, PRs, issues.
- **Repo:** https://github.com/modelcontextprotocol/servers/tree/main/src/github
- **Skill Pack:** S12; also used by R6, R7, R1.

### Trezor
- **What:** open-source hardware wallet.
- **Why ØØT uses it:** stores 4thtech wallet identity keys, treasury wallet keys (Gen 2), payroll wallet keys (Gen 2), Cotrugli Ledger co-signature keys (Gen 3).
- **Site:** https://trezor.io/
- **Governance:** `governance/SECRETS-POLICY.md`.

---

## Cloud-track stack

### Anthropic Claude
- **What:** the cloud track's daily driver. Includes Claude Desktop, Claude Code, Claude Remote Routines, and the Anthropic API.
- **Why ØØT uses it:** the framework's reference cloud-track implementation.
- **Site:** https://claude.com/
- **Documentation:** https://docs.claude.com/
- **Claude Desktop:** the user-friendly UI for daily work.
- **Claude Code:** the developer CLI (used by S4 Code & QA).
- **Remote Routines:** the cloud automation engine (R1–R8 cloud variants).
- **Skill format:** SKILL.md is Anthropic's Agent Skills format; ØØT's 12 packs follow it.
- **Licence:** commercial.

### Google Workspace
- **What:** Drive, Sheets, Docs, Calendar, Gmail.
- **Why ØØT uses it:** the cloud-track substrate. Claude has official connectors.
- **Site:** https://workspace.google.com/
- **Licence:** commercial.

### Slack
- **What:** team communication.
- **Why ØØT uses it:** the cloud-track comms layer; standing channels for `#output-log`, `#business-review`, `#klarna-test`, `#compensation`, `#change`, `#brain-health`, `#ops`.
- **Claude integration:** https://slack.com/apps/A0848GFRZ54-claude
- **Licence:** commercial.

### Microsoft Excel
- **What:** alternative to Google Sheets for the cloud track.
- **Why ØØT uses it:** Claude's Excel extension (https://www.microsoft.com/en-us/microsoft-365/excel) is supported as a cloud-track alternative.
- **Licence:** commercial.

---

## Secrets layer

### Bitwarden
- **What:** open-source password manager.
- **Why ØØT uses it:** software credentials (API keys, OAuth tokens, recovery codes). The secrets policy mandates either Bitwarden or 1Password.
- **Site:** https://bitwarden.com/
- **CLI:** https://bitwarden.com/help/cli/
- **Self-hostable:** Vaultwarden — https://github.com/dani-garcia/vaultwarden
- **Governance:** `governance/SECRETS-POLICY.md`.

### 1Password
- **What:** commercial alternative to Bitwarden.
- **Why ØØT uses it:** functionally equivalent for ØØT purposes; pick on team preference.
- **Site:** https://1password.com/
- **CLI:** https://1password.com/downloads/command-line/

### Yubikey
- **What:** hardware security key (FIDO2 / WebAuthn / TOTP).
- **Why ØØT uses it:** org-level admin 2FA (GitHub admin, Anthropic admin, Google Workspace super-admin, Bitwarden organisation owner).
- **Site:** https://yubico.com/
- **Governance:** `governance/SECRETS-POLICY.md`.

---

## Code & QA tooling

### GitHub
- **What:** version control, issue tracking, PR review, CI.
- **Why ØØT uses it:** the Brain sync substrate; the protected audit-log branch lives here; the `oot/klarna-test` status check runs here.
- **Site:** https://github.com/
- **CLI:** https://cli.github.com/
- **Licence:** commercial (free for public repos).
- **Skill Pack:** S4.

### Augment Code
- **What:** large-multi-file coding agent.
- **Why ØØT uses it:** S4 Code & QA's "Three Philosophies" — Augment for big builds.
- **Site:** https://www.augmentcode.com/
- **Licence:** commercial.

### Codex CLI / Open Codex
- **What:** code review/audit assistants. Open Codex is the open-source variant.
- **Why ØØT uses it:** S4's "Three Philosophies" — Codex for review/audit. Open Codex for the privacy track.
- **Repo (Open Codex):** https://github.com/openai/codex
- **Licence:** commercial / open-source (per repo).

### Obsidian
- **What:** local markdown editor.
- **Why ØØT uses it:** the human view of the Brain. Obsidian-compatible markdown is the framework's storage format.
- **Site:** https://obsidian.md/
- **Licence:** free for personal use.

---

## Governance frameworks

### EU AI Act (Regulation (EU) 2024/1689)
- **What:** the EU's AI regulation.
- **Why ØØT cites it:** `governance/EU-AI-ACT.md` maps Articles 9, 12, 13, 14 to ØØT components for EU-operating adopters.
- **Implementation timeline:** https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act
- **Skill Pack:** S7 — `skills/governance-compliance/`.

### GDPR Article 22 (solely automated decisions)
- **What:** EU data-subject right against decisions made solely by automated processing.
- **Why ØØT cites it:** the framework's compensation calculations are designed to be human-co-signed precisely to clear Article 22.
- **Reference:** https://gdpr-info.eu/art-22-gdpr/

### Italian Law 132/2025
- **What:** the first national EU AI law; complements the AI Act with criminal offences.
- **Why ØØT cites it:** leading indicator of EU enforcement seriousness; mandatory mapping for orgs operating in Italy.
- **References:**
  - https://www.nortonrosefulbright.com/en/knowledge/publications/9bfedfea/italy-enacts-law-no-132-2025-on-artificial-intelligence-sector-rules-and-next-steps
  - https://www.clearygottlieb.com/news-and-insights/publication-listing/italy-adopts-the-first-national-ai-law-in-europe-complementing-the-eu-ai-act

### EU MiCA (Markets in Crypto-Assets)
- **What:** EU regulation for crypto-assets including stablecoins.
- **Why ØØT cites it:** stablecoin payroll (Gen 2) operates under MiCA in EU jurisdictions.
- **Reference:** https://eur-lex.europa.eu/eli/reg/2023/1114/oj

### US GENIUS Act
- **What:** the first US federal stablecoin framework (signed 17 July 2025).
- **Why ØØT cites it:** stablecoin payroll (Gen 2) operates under GENIUS in US jurisdictions.
- **Reference:** https://www.weforum.org/stories/2025/09/us-genius-act-eu-mica-convergence-crypto-rules/

---

## Standards bodies

### Linux Foundation Agentic AI Foundation (AAIF)
- **What:** the standards body governing MCP and related agentic-AI primitives (Dec 2025).
- **Why ØØT cites it:** the framework rests on AAIF-governed primitives (MCP, AGENTS.md, MCP server cards).
- **Site:** https://lfaidata.foundation/

### Model Context Protocol (MCP)
- **What:** the open standard for agent ↔ tool communication.
- **Why ØØT cites it:** every Skill Pack uses MCP-compatible tools.
- **Spec:** https://modelcontextprotocol.io/
- **Servers:** https://github.com/modelcontextprotocol/servers

---

## Stablecoin payroll rails (Gen 2)

### Rise (Circle partner)
- **What:** stablecoin payroll provider; processes USDC / EURC payroll.
- **Why ØØT cites it:** Gen 2 stablecoin payroll integration (Skill Pack S10 Finance & Treasury).
- **Site:** https://riseworks.io/
- **Public stats:** $1.37B lifetime payroll volume by Q1 2026.

### Circle (USDC, EURC issuer)
- **What:** the stablecoin issuer.
- **Why ØØT cites it:** Rise's underlying issuer; direct integration also supported in Gen 2.
- **Site:** https://www.circle.com/

---

## Adjacent open-source frameworks

### My Curator (the framework's reference Brain)
- See above.

### Karpathy's Software 3.0 framing
- **What:** Karpathy's articulation of the new division of labour (spec / test / review human, implementation AI).
- **Why ØØT cites it:** Thesis 2 (centaur work).
- **Talk:** https://karpathy.bearblog.dev/sequoia-ascent-2026/

### Beyond Budgeting Roundtable
- **What:** community around the Beyond Budgeting management framework.
- **Why ØØT cites it:** Thesis 3 + Skill Pack S5; the rolling-forecast principle.
- **Site:** https://bbrt.org/

---

## Cotrugli Ledger (Generation 3)

### Cotrugli Business School
- **What:** the institutional anchor for Generation 3's Cotrugli Ledger work.
- **Why ØØT cites it:** Dr. Tali Režun is Vice Dean Frontier Technologies; Dražen Kapusta co-authors the Cotrugli Ledger work.
- **Site:** https://cotrugli.org/

### Cotrugli Ledger work
- **What:** triple-entry-style accounting via PAC-RO receipts; Cotrugli Score / Vanguard Score reputation; IAAF agent autonomy levels.
- **Why ØØT cites it:** Generation 3 governance backbone.
- **Status:** theoretical / research-stage; not yet operational.
- **Reference:** International Leadership Journal publication (Kapusta, Gams, Brčić, Režun) — citation TBD.

---

## How this index is maintained

This file is a Curator-style external-resource index. Updates flow via PR. A monthly review (recommended cadence) verifies:

- All URLs still resolve.
- Licence terms are current.
- Project statuses are accurate (active vs. archived vs. forked).
- New ecosystem entries are added when they become operationally relevant.

The framework prefers to remove a stale entry than leave a dead link standing.
