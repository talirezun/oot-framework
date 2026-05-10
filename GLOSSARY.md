# ØØT Glossary

Definitions of every term ØØT uses in a non-standard or non-obvious way. If a term means roughly what English suggests it means, it is not here.

## Core concepts

**ØØT.** The framework. Pronounced "out". The two crossed-out circles represent legacy headcount and empty hours — the things being negated; the T is Tomorrow / Threshold / the new vector. In ASCII contexts (URLs, repository names, shell commands) we use `oot`.

**Generation 1 (Gen 1).** The current release (v1.0). Cloud-track full + privacy-track parity, FIAT compensation, Excel-bridged long-tail tracking, Klarna Test, EU AI Act mapping. What works today.

**Generation 2 (Gen 2).** v2.0, expected 6–12 months. Stablecoin rails, smart-contract long-tail, Internal Unit Fund, Curator local-LLM ingest, Tier-2 Skill Pack hardening.

**Generation 3 (Gen 3).** v3.0, expected 12–24 months, research-stage. Cotrugli Ledger anchoring, autonomous agent business units (Kelly / OpenClaw pattern), per-agent compensation.

**Lego.** A composable unit of the framework — a partner concept, a tool, a Skill Pack, an Excel template, a Routine, a governance document. The framework is a Lego inventory; v1.0 is the operational subset.

## People layer

**Partner.** The unit of work in ØØT. Not an employee. Contracted for output, not hours. Receives base + variable + long-tail compensation. Declares a reward species. May (Gen 2+) hold Unit Fund credits and units.

**Reward species.** From the MHPR Advisors typology of seven partnership reward models. The three primary ØØT options: pure eat-what-you-kill, pure lockstep, declared hybrid with explicit weights. Recorded in `reward-species-declaration.xlsx`, version-controlled, renegotiable on a defined cadence.

**Cohort.** A partner's engagement type: full-time partner (full output participation, monthly variable, long-tail, unit holdings), project specialist (defined project, defined deliverable, defined amount, exit), or advisor (continuous engagement, narrow scope, smaller stake).

**Output.** A shipped artefact: a merged commit, a signed contract, a launched product, a closed deal, a published article, a delivered design. The unit the partner is paid against.

**Outcome.** The downstream value an output produced. Output is "the contract was signed"; outcome is "the contract generated €2M of revenue over three years." The long-tail layer pays against outcome.

**Output spec.** The pre-shipped definition of what "done" looks like for a committed piece of work. Authored before work begins; referenced at variable-pay calculation time.

**Value tier / value envelope.** The size category of an output's expected outcome. A flagship game spec has a larger envelope than a maintenance patch spec. Set at planning, refined as outcomes come in. Drives the variable-pay multiplier.

**Attribution agent.** The (Gen 1: Routine + Skill + Excel; Gen 2: dedicated agent) that reads commits, specs, reviews, contracts, milestones; produces a daily per-partner output ledger; trains a value-creation model on the firm's own ground truth.

**Variable pay.** The monthly payment computed from output × value tier × multiplier. Lands the month after output ships.

**Long-tail entitlement.** A percentage entitlement against an output's *outcome*. Pays quarterly for as long as the output generates value. Tracked manually in Excel in Gen 1; smart-contract in Gen 2.

**Unit Fund.** The internal open-ended fund of the company's units. Continuously priced. Dividend-paying. Bid/ask liquidity. The right to subscribe is *earned* through contribution (subscription credits issued alongside variable pay). Cash without credits cannot buy in. Generation 2.

**Subscription credits.** Non-transferable, time-bounded entitlements to subscribe to the Unit Fund. Issued alongside variable pay in proportion to contribution. Generation 2.

**Two Worlds of Code.** Karpathy's distinction between vibe coders (legacy, pre-Software-3.0) and agentic engineers (Software 3.0 native). Self-identification in onboarding helps the partner understand which world they are entering.

## Tech layer

**The Brain (Collecting Brain).** The firm's queryable knowledge graph — every conversation, decision, contract, deal, code review, customer interaction, research session captured in markdown with YAML frontmatter and wikilinks. The Curator is the canonical reference implementation.

**The Curator.** The reference Brain implementation. Open source. Includes the MyCuratorMCP server (17 tools), the Curator desktop app (knowledge ingest), and the canonical SKILL.md.

**Skill / Skill Pack.** A markdown file (or folder of files) following the SKILL.md format from Anthropic Agent Skills. Encodes operational discipline for a domain. Loaded into Claude Desktop, Claude Code, Cursor, LM Studio, or any MCP-compatible client. ØØT ships 12 packs in v1.0.

**MCP (Model Context Protocol).** The open standard for agent ↔ tool communication. Now governed by the Linux Foundation Agentic AI Foundation. ØØT depends on MCP as a primitive.

**AGENTS.md.** The cross-vendor agent orientation file at the root of an agent-readable repository. Tells any AI agent how to navigate the repo, what conventions are in force, what tools are available.

**CLAUDE.md.** The Claude Code-specific orientation file. Same purpose as AGENTS.md but Claude Code reads it preferentially. ØØT ships a `CLAUDE.md` at the root.

**Routine.** A scheduled prompt that runs on a trigger (time, GitHub event, API call). Cloud track = [Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code). Privacy track = OS-native scheduling hitting headless LM Studio. ØØT ships 8 Routines in v1.0. Operational `.xlsx` state lives in the firm's Brain repo and is mutated by Routines via openpyxl + signed commits per ADR-001.

**Cloud track.** The canonical, fastest path. Claude Desktop, Claude Code, Slack, GitHub (Brain repo holds markdown + `.xlsx` state), the Curator, MyCuratorMCP, Claude Code Routines. Anthropic infrastructure where applicable. Spreadsheet viewer is user choice (Excel / LibreOffice / Numbers / Excel-for-Web).

**Privacy track.** The full-Gen-1-parity sovereignty path. LM Studio with local Qwen / Llama / DeepSeek, Desktop Commander MCP, Excel MCP, 4thtech for on-chain communication, PollinationX for decentralised storage, GitHub MCP, OS-native scheduling.

**4thtech.** The on-chain end-to-end-encrypted communication and file-transfer framework. Wallet-as-identity, fully self-custodial, permissionless. Privacy-track comms layer. `https://github.com/4thtech`.

**PollinationX.** The decentralised storage protocol. NFT-based capacity. Encrypted, distributed across nodes. Privacy-track Drive equivalent. `https://wiki.pollinationx.io/`.

**Lumina AI.** The RAG chatbot widget. External-facing front door for sales, support, lead-capture. The "Lumina-as-front-door" pattern is referenced in the Sales & BD Skill Pack.

## Process / governance

**Klarna Test.** The signature epistemic check. Any ØØT recommendation that would have produced the Klarna outcome (publicly cut humans, quietly rehired) must be flagged. Ten-question scoring rubric in `governance/KLARNA-TEST.md`. Each question scored 0, 1, or 2 (max 20). Score **<14/20** blocks proceeding. Wired into Code & QA as a pre-merge gate on any PR labelled `ai-replaces-human`.

**METR baseline.** Pre-rollout productivity baseline using DORA + SPACE + DX Core 4 metrics. Mandatory before any major Skill rollout. The METR study showed senior engineers were 19% slower while feeling 20% faster — without a baseline, organisations cannot detect their own regressions.

**ROWE.** Results-Only Work Environment (Cali Ressler & Jody Thompson, Best Buy 2003). The intellectual ancestor of ØØT's pay-for-output principle. Reports ~35% productivity gains and ~90% reduction in voluntary turnover.

**SECI model.** Socialisation → Externalisation → Combination → Internalisation (Nonaka & Takeuchi). The knowledge-creation cycle the Brain operationalises.

**Beyond Budgeting.** Hope & Fraser's 1998 management framework. ØØT borrows the rolling-forecast and continuous-allocation principles for the Reporting & Business Review Skill Pack.

**AI Champion.** A partner who has demonstrably increased their throughput and quality via AI tooling, then mentors others. *Earned, not appointed.* Tecknoworks/Caplaz case studies show artificial champions backfire.

**Cotrugli Ledger.** The Generation 3 governance backbone. Triple-entry-style accounting via PAC-RO receipts, with Cotrugli Score / Vanguard Score reputation, IAAF agent autonomy levels. Theoretical / research-stage in v1.0. Co-authored by Dražen Kapusta.

**PAC-RO.** Policy-anchored, Co-signed Receipt Object — the unit of accounting in the Cotrugli Ledger. Composed of Facts, Evidence, Policy, and Co-signature. Generation 3.

**The Five Theses.** Resistance, Centaur work, Partner compensation, Collecting Brain, Composable Lego. The intellectual core of the framework. See `MANIFESTO.md`.

## Tooling

**Bitwarden.** Open-source password manager. ØØT secrets policy uses Bitwarden (or 1Password as commercial alternative) for software credentials — API keys, OAuth tokens, recovery codes.

**Trezor.** Hardware wallet. ØØT secrets policy uses Trezor (or Ledger as alternative) for crypto signing — payroll wallets, treasury wallets, 4thtech identity wallets.

**Yubikey.** Hardware security key. Used for org-level admin accounts (GitHub, Anthropic, Google admin). Recommended in the secrets policy.

**Excel MCP.** The MCP server (`haris-musa/excel-mcp-server`, MIT-licensed) that lets local LLMs read and write Excel files. The piece that gives the privacy track full Gen 1 automation parity.

**llmster.** A headless LM Studio CLI. Lets a privacy-track machine run local models without keeping a GUI open. Used by the privacy-track equivalents of cloud Routines.

**Desktop Commander MCP.** Local filesystem MCP server. Privacy-track replacement for the Google Drive Claude connector.

**Augment Code, Codex CLI, OpenCode.** Specialised coding assistants. ØØT references them in the Code & QA Skill Pack: Augment for big multi-file builds, Codex for review/audit, OpenCode for the open-source / privacy-track path.