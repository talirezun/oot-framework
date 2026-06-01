---
title: "Building the Organization of Tommorow: An Open-Source Framework and Playbook for Partner-Run, AI-Augmented Organisations"
author: "Dr. Tali Režun"
author_affiliation: "Vice Dean of Frontier Technologies, COTRUGLI Business School; Founder, The Curator, Block Labs, Lumina AI, Moj AI, 4thTech, PollinationX, Immu3, Online Guerrilla"
date: 2026-05-15
topic: "Framework overview / All five theses / Generation roadmap"
peer_reviewed: no
type: original-article
publication: "ØØT Research Series — Article 1 (Overview & Foundation)"
series: "ØØT Research Series"
article_number: 1
---

# Building the Organization of Tommorow: An Open-Source Framework and Playbook for Partner-Run, AI-Augmented Organisations

**By Dr. Tali Režun**
Vice Dean of Frontier Technologies, COTRUGLI Business School; Founder, The Curator, Block Labs, Lumina AI, Moj AI, 4thTech, PollinationX, Immu3, Online Guerrilla
Published: 2026-05-15
Series: ØØT Research Articles — Article 1 (Overview & Foundation)
Repository: [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)

> An accessible, comprehensive overview of the framework's intellectual foundations, architectural structure, tool choices, knowledge infrastructure, installation pathways, and roadmap — written to enable founders of new companies, and leaders upgrading existing ones, to understand why ØØT exists, what it can do for them today, and where it is going.

---

## Abstract

The Organisation of Tomorrow (ØØT) is an open-source framework and operational playbook for partner-run, AI-augmented firms. It synthesises thirty years of entrepreneurial practice, anchored in peer-reviewed research on agentic AI, knowledge management, output-based compensation, and organisational change management. This founding article presents the intellectual thesis behind ØØT, unpacks its three-generation architecture and dual deployment tracks, explains the tool ecosystem chosen to prevent vendor lock-in, describes the role of the Curator and its SKILL.md primitives as the firm's compounding knowledge substrate, and explains how the framework can be installed in as little as sixty to ninety minutes. The article argues that the central problem of AI adoption is not technological but organisational — and that ØØT is the first open-source, composable framework to address all four structural gaps simultaneously: resistance management, output-based compensation, agentic knowledge infrastructure, and data sovereignty. The framework is offered as a practitioner contribution and as a research foundation for organisations building or transforming toward the operating model of 2026 and beyond.

---

## Section 1 — Introduction: Why Organisations Need a New Operating System

The world of work is undergoing a transition that is neither incremental nor optional. According to the McKinsey *State of AI 2025* report (n=1,993 organisations across 105 countries), 88% of organisations now use AI in at least one function — yet only 5% of enterprise generative AI pilots produce any measurable P&L impact (MIT Project NANDA, *The GenAI Divide*, August 2025). The tools are ready. The organisations are not.

This gap is not a technology problem. The dominant cause of failure, as identified by MIT NANDA, is a 'learning gap' — a failure of organisational design, process architecture, and human change management, not of model quality. The Microsoft *Work Trend Index 2025* finds that 82% of leaders call the current moment 'pivotal' for rethinking their operating model, while only 46% are actually automating workflows with agents today. The expectation-execution gap is the defining challenge of the decade.

The Organisation of Tomorrow (ØØT) was designed to close this gap. It is not a consulting methodology, not a SaaS platform, and not an academic framework divorced from operational reality. It is an open-source GitHub repository — a complete stack of technology, thesis, tools, instruction manuals, and governance documents — built on thirty years of entrepreneurial experience founding and scaling technology companies across AI, Web3, legal-tech, and decentralised infrastructure.

The framework's tagline is precise: *an open framework for partner-run, AI-augmented organisations*. Every word matters. **Partner-run** signals a specific ownership and compensation architecture. **AI-augmented** signals human primacy over agentic automation, not replacement. **Open** means the framework itself is a public good, free to adopt, fork, and improve under Creative Commons and Apache licences.

This article is the first in the ØØT Research Series. It provides an accessible, comprehensive overview of the framework's intellectual foundations, architectural structure, tool choices, knowledge infrastructure, installation pathways, and roadmap — with the goal of enabling founders of new companies, and leaders upgrading existing ones, to understand why ØØT exists, what it can do for them today, and where it is going.

> **Who This Article Is For**
>
> Founders building new companies who want to design the operating model correctly from day one. Leaders of existing firms exploring AI-augmented workflow transformation. Academics and researchers studying agentic organisational design. Technical practitioners looking to understand the framework's architecture before installing it. The article is written to be accessible to non-technical readers while remaining precise enough to be useful to those who will implement it.

---

## Section 2 — The Thesis: Five Arguments for a New Organisational Architecture

The intellectual core of ØØT is the [`MANIFESTO.md`](../../MANIFESTO.md) file in the framework repository. It advances five interlocking theses, presented in order of evidentiary strength. Each thesis carries an explicit honesty clause: what is empirically established, what is directional, and what is speculative. The framework was built to be honest about the difference. What follows is a distillation of those five arguments.

### Thesis 1 — Resistance is the Central Problem

The technology is ready. The organisations are not. This is not a slogan — it is the single most consistent finding in the 2025 enterprise-AI research literature, and the place where ØØT's contribution is sharpest.

According to MIT NANDA (2025), 95% of enterprise generative AI pilots produce no measurable P&L impact. The root cause identified is a 'learning gap' — organisational and process failure, not model quality. A rigorous randomised controlled trial by METR (July 2025) of experienced open-source developers found that participants using AI coding tools were measured 19% slower on real tasks while self-reporting they were 20% faster — a 39-point perception swing. The CIO Dive (2026) survey reports that 76% of developers refuse AI assistance for deployment and monitoring; 69% reject it for project planning. This resistance is rational, not technophobic: it stems from legitimate concerns about context gaps, code quality, and accountability.

The Klarna case is the framework's signature cautionary reference. Klarna publicly replaced approximately 700 customer-service roles with AI in 2024, then began rehiring in 2025 after service quality collapsed. The ØØT framework encodes this failure mode into a mandatory governance tool: the **Klarna Test** — a ten-question rubric (scored 0-2 per question, threshold 14/20 or 70%) that any 'AI replaces human' decision must pass before proceeding. The test is not advisory. It is a blocking gate in the framework's code-review and deployment workflow. See [`governance/KLARNA-TEST.md`](../../governance/KLARNA-TEST.md) for the canonical rubric.

As stated in the [`MANIFESTO.md`](../../MANIFESTO.md): *'Position ØØT as the framework that takes the human resistance problem seriously.'* No comparable open-source organisational framework addresses this problem at all.

### Thesis 2 — The Agentic Workforce Is Here, But Unevenly

AI does not replace knowledge workers uniformly. It augments them selectively, unevenly, and in ways that are domain-specific. Andrej Karpathy's 'Two Worlds of Code' framing — presented at Sequoia AI Ascent 2026 — distinguishes between 'vibe coding' (which raises the floor for non-engineers) and 'agentic engineering' (which raises the ceiling for professionals). ØØT encodes both realities.

The McKinsey *State of AI 2025* reports that AI high performers — the 6% of organisations with more than 5% EBIT attributable to AI — are 3.6 times more likely to pursue transformational workflow redesign and 55% redesign workflows end-to-end. Workflow redesign, not model selection, is the single strongest predictor of value capture.

ØØT structures the augmentation reality through a partner-onboarding module that includes a mandatory 'Two Worlds of Code self-identification' (P14 in the framework's people layer). Each partner identifies whether they operate as a vibe coder, an agentic engineer, or in the transitional space between the two. This self-identification informs their reward-species designation, their Skill Pack exposure, and the change-management pilot they participate in before full framework rollout.

### Thesis 3 — Output-Based Compensation Is the Right Model

Traditional time-and-attendance compensation is increasingly incoherent in a world of AI-augmented knowledge work. If a partner can produce in two hours what previously took eight, paying for the eight hours is not only inefficient — it creates perverse incentives against adoption of the very tools that could expand firm capacity.

ØØT replaces time-based compensation with a layered output-based architecture. Layer 1 is a base draw (a modest monthly floor). Layer 2 is output-variable pay, tied to completed and accepted Output Specs (defined deliverables with clear acceptance criteria). Layer 3 is long-tail outcome entitlements — a percentage of future revenue from an artefact, tracked for its operational life. Layers 4-7 (subscription credits, dividends, capital appreciation, and per-agent compensation) are deferred to Generation 2 and 3 as infrastructure matures.

This architecture draws on the Research Only Work Environment (ROWE) literature, the Beyond Budgeting movement (Hope & Fraser, 1998; Bjarte Bogsnes at Statoil), and Levin & Tadelis on partnership compensation. The framework's compensation module ([Skill Pack S3](../../skills/compensation-attribution/SKILL.md)) includes an attribution agent that reads the Brain's knowledge graph to produce daily output ledgers, monthly variable statements, and quarterly long-tail entitlement calculations — automatically.

### Thesis 4 — The Collecting Brain Is the Firm's Most Valuable Asset

Knowledge that lives in individual heads, scattered Slack messages, and unstructured document drives is knowledge that cannot be leveraged, cannot be compensated, and cannot survive the departure of the person who holds it. The ØØT framework calls this the 'Knowledge Immortality' problem — and its solution is the Collecting Brain.

The intellectual foundation draws on Michael Polanyi's distinction between explicit and tacit knowledge (*The Tacit Dimension*, 1966), Nonaka and Takeuchi's SECI model of knowledge conversion (*The Knowledge-Creating Company*, 1995), and the modern operationalisation of these ideas through Microsoft's GraphRAG architecture ([Edge et al., 2024](https://arxiv.org/abs/2404.16130)) and Karpathy's 'second brain' concept. According to Glean's enterprise search data, knowledge workers spend 8.2 hours per week looking for or recreating information — dropping to 0.7 hours per week with proper enterprise knowledge infrastructure.

The framework deploys knowledge infrastructure at the highest maturity level immediately. As specified in the [`MANIFESTO.md`](../../MANIFESTO.md): *'There is no point in retrofitting Levels 1-3 if you can start at the destination.'* Generation 1 deploys at Level 4 — an agentic MCP-native knowledge graph accessible by any Model Context Protocol-compatible AI client.

### Thesis 5 — The Framework Is Composable Lego

Every comparable framework that has attempted to define 'the operating system for the future of work' has done so as a proprietary SaaS platform with a vendor-locked data model. Holacracy requires its constitution. Teal requires its cultural philosophy. McKinsey's Agentic Organization requires McKinsey. None are open-source. None are composable.

ØØT is different by design. The Brain is a folder of plain markdown files. The Skill Packs are markdown files. The Routines are markdown prompts. The governance documents are markdown files. The Excel templates are standard `.xlsx` files. Anything ØØT writes can be read by any text editor on any operating system in any decade. As the [MANIFESTO](../../MANIFESTO.md) states: *'There is no vendor between you and the framework.'*

The composability is enabled by the open standards of the [Linux Foundation Agentic AI Foundation (AAIF)](https://lfaidata.foundation/), formed in December 2025: SKILL.md (Anthropic Agent Skills format), AGENTS.md (cross-vendor orientation), MCP (Model Context Protocol), and MCP server cards. These primitives are vendor-neutral. They are governed by a standards body, not by any AI lab. This is a deliberate architectural choice that makes ØØT durable against single-vendor risk.

The following table situates ØØT against the dominant existing organisational frameworks:

| Framework | Core Premise | Gap ØØT Addresses |
|---|---|---|
| Holacracy (Robertson, 2007) | Self-managing roles and circles | Silent on AI agents and technology layer entirely |
| Teal Organisations (Laloux, 2014) | Self-management, wholeness, evolutionary purpose | No technology operating model; no compensation primitives |
| Beyond Budgeting (Hope & Fraser, 1998) | Rolling forecasts, decentralised authority, relative performance | Strong on adaptive management but agnostic on AI agents |
| Lean Startup (Ries, 2011) | Build–measure–learn, MVP, validated learning | Product-development framework, not organisational design |
| Microsoft Frontier Firm (2025) | Hybrid human + agent teams, human-agent ratio | Vendor-led; lacks open-source, compensation-integrated layer |
| McKinsey Agentic Organisation (2025) | Humans above the loop overseeing agent populations | Not open-source; no SKILL.md primitives; no sovereignty layer |
| **ØØT (Režun, 2026)** | **Open-source, composable, compensation-redesigned, Brain-first** | **Occupies all four corners: resistance, compensation, knowledge, composability** |

*Sources: ØØT [`MANIFESTO.md`](../../MANIFESTO.md) ([github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)); ØØT Foundational Research & Strategic Analysis (2025–2026); McKinsey State of AI 2025; MIT Project NANDA 'The GenAI Divide' (August 2025); Microsoft Work Trend Index 2025.*

---

## Section 3 — Framework and Playbook: Definitions and Architecture

ØØT operates at two levels: a Framework and a Playbook. These are not synonyms.

The **Framework** is the complete stack: the intellectual thesis ([`MANIFESTO.md`](../../MANIFESTO.md)), the technical specification ([`SPEC.md`](../../SPEC.md)), the Skill Packs (twelve markdown files encoding methodology), the Excel templates (nine pre-built `.xlsx` files), the Routines (eight scheduled automation prompts), the governance documents, the Brain ontology, and the research archive. The Framework is the whole. It is what you commit to when you adopt ØØT as your organisational operating model.

The **Playbook** is a bundle of instruction manuals and tools that you can use selectively. If a founder wants only the output-based compensation module, they can adopt [Skill Pack S3](../../skills/compensation-attribution/SKILL.md) without adopting the full framework. If a firm wants only the knowledge management infrastructure, it can deploy the Curator and [Skill Pack S1](../../skills/my-curator/SKILL.md). The Playbook design principle — expressed in the [`SPEC.md`](../../SPEC.md) as 'composable Lego' — means that every module is independently useful and can be combined with other modules without conflicts.

The architecture has three layers: People, Technology, and Methodology.

| Layer | What It Contains | Core Files |
|---|---|---|
| **People Layer** | Partner Charter, Reward Species Declaration, Output Specs, Onboarding Checklist, Output Ledger, Variable Pay Calculator, Long-Tail Tracker, Dispute Resolution | P1–P14 documents; X1–X9 Excel templates ([`templates/excel/`](../../templates/excel/)) |
| **Technology Layer** | Cloud Track (Claude Desktop/Code, GitHub, Slack, Curator) and Privacy Track (LM Studio, 4thtech, PollinationX, Desktop Commander MCP, Excel MCP) | [`SPEC.md`](../../SPEC.md) Layer 2; [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md) |
| **Methodology Layer** | 12 Skill Packs (7 hardened, 5 scaffolded), 8 Routines (cloud + privacy equivalents), Klarna Test, EU AI Act mapping, Change Management playbook | [`skills/`](../../skills/) directory; [`routines/`](../../routines/) directory; [`governance/`](../../governance/) directory |

---

## Section 4 — The Three Generations: A Roadmap of Honest Ambition

ØØT is designed in three generations. The framework is explicit that this is a roadmap of honest ambition: Generation 1 is what works today; Generation 2 is what is planned for the next six to twelve months pending legal and infrastructure prerequisites; Generation 3 is research-stage. Adopting ØØT at Generation 1 does not require committing to subsequent generations. The upgrade path is real but optional. As the [`GENERATIONS.md`](../../GENERATIONS.md) document states: *'Generation 1 is operationally complete on its own.'*

### Generation 1 — Cloud-Track and Privacy-Track ØØT (Today, v1.0)

Generation 1 is what ships in the current repository. It includes: all twelve Skill Packs (seven hardened Tier-1 packs plus five scaffolded Tier-2 packs); all nine Excel templates with formulas and seeded sample data; eight cloud Routines and eight privacy-track equivalents; four governance documents ([Klarna Test](../../governance/KLARNA-TEST.md), [EU AI Act mapping](../../governance/EU-AI-ACT.md), [Decision Rights matrix](../../governance/DECISION-RIGHTS.md), [Secrets Policy](../../governance/SECRETS-POLICY.md)); the [Brain ontology](../../templates/brain/FIRM-ONTOLOGY.md) and fourteen Brain page templates; and the complete installer tooling.

Generation 1 delivers compensation layers 1 through 3 (base draw, output-variable, and long-tail entitlements) and layer 5 (annual bonus). FIAT currency is the default payment mechanism. The long-tail layer is tracked in Excel and settled quarterly by the founding partner.

Crucially, Generation 1 achieves full operational parity between two parallel technology tracks:

#### The Cloud Track

The cloud track is the canonical, fastest-path implementation. It uses Claude Desktop and Claude Code (Anthropic) as the AI layer, GitHub as the version-controlled Brain repository, Slack for team communication, the Curator desktop application with MyCuratorMCP for knowledge management, and Claude Code Routines for scheduled automation. All Routines run on Anthropic's infrastructure — meaning they execute even when the founder's laptop is closed.

#### The Privacy Track

The privacy track replaces every cloud dependency with a self-sovereign equivalent, achieving full Generation 1 parity with a single trade-off: Routines run only while the always-on machine (a Mac mini, NUC, or Raspberry Pi 5) is powered on.

| Cloud Component | Privacy-Track Equivalent |
|---|---|
| Anthropic Claude API | LM Studio + Qwen / DeepSeek (local models) |
| Slack | 4thtech dChat (on-chain, end-to-end encrypted) |
| Email / Gmail | 4thtech dMail (wallet-as-identity, self-custodial) |
| Google Drive / Desktop files | Desktop Commander MCP (local filesystem) + PollinationX (decentralised storage) |
| Claude Code Routines | OS-native scheduling (cron / launchd / Task Scheduler) on always-on machine |
| Microsoft Excel + Claude extension | Excel MCP ([haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server)) + local LM Studio |

The privacy track is not a reduced-capability version. It is a full parity alternative for founders with regulatory constraints (e.g., customer data that cannot touch cloud LLMs), philosophical commitment to self-custody, or who wish to prepare for Generation 2 stablecoin payroll — which requires hardware wallet identity infrastructure (Trezor) in any case.

The secrets architecture for both tracks relies on a two-layer design: Bitwarden (or self-hosted Vaultwarden) for software credentials (API keys, OAuth tokens, recovery codes), Trezor hardware wallets for cryptographic signing and treasury keys, and Yubikey for organisational administrator two-factor authentication on GitHub, Anthropic, and Google admin consoles. See [`governance/SECRETS-POLICY.md`](../../governance/SECRETS-POLICY.md) for the canonical layout.

### Generation 2 — Sovereignty Parity and Crypto Rails (6–12 Months)

Generation 2 adds the compensation infrastructure that requires blockchain rails or material legal scoping. Its three primary additions are:

- **Stablecoin payroll (P9):** USDC or EURC settlement via Rise (Circle partner) or equivalent. This enables per-milestone payment, settling in seconds, with per-partner opt-in declared in the Reward Species Declaration.
- **Smart-contract long-tail entitlements:** the Excel-tracked Generation 1 long-tail upgrades to on-chain percentage entitlements that pay automatically every quarter for the operational life of the artefact. Smart contract templates will ship as part of Compensation and Attribution Skill Pack v2.0.
- **Internal Unit Fund (P8):** a continuously-priced, dividend-paying fund that opens after six to nine months of pilot data — per the YOLO Investments model's recommendation — to allow partners to hold equity-equivalent positions in the firm's compounding output.

Generation 2 also hardens the five Tier-2 Skill Packs (S7–S11: [Governance & Compliance](../../skills/governance-compliance/SKILL.md), [Legal Operations](../../skills/legal-operations/SKILL.md), [Marketing](../../skills/marketing/SKILL.md), [Finance & Treasury](../../skills/finance-treasury/SKILL.md), [Sales & BD](../../skills/sales-bd/SKILL.md)) and adds Curator local-LLM ingest, allowing the Collecting Brain to process documents without any cloud API dependency.

### Generation 3 — Agent-Orchestrated Organisation (12–24 Months, Theoretical)

Generation 3 is the research-stage release. It is what becomes possible when the **Cotrugli Ledger** — a blockchain-anchored governance system developed by Dražen Kapusta and Dr. Tali Režun — is operational, and when autonomous agent business units are legally and practically mature.

The centrepiece of Generation 3 is the Kelly-style autonomous business unit: an AI agent operating with its own LLC, GitHub account, email address, cryptocurrency wallet, contract authority, and the ability to hire human partners through the same ØØT framework. The reference case is documented in the project knowledge as the 'This AI Agent Hired a Human, Built Apps and Started Making Money' case. Under ØØT, such an agent would have its own [Partner Charter](../../templates/partner-charter.md), Reward Species Declaration, and output ledger — treated as a named cohort of partner.

Generation 3 also introduces the Cotrugli Ledger governance layer: Policy-Anchored Co-signed Receipt Objects (PAC-ROs) for every significant transaction, Cotrugli Score (firm-level reputation), Vanguard Score (cross-firm individual reputation), and the Identity, Authority, Agency Framework (IAAF) with four autonomy levels for AI agents. This infrastructure enables cross-firm reputation portability and makes the full agentic economy legible and auditable.

The framework is honest about what it will not promise for Generation 3: no timeline guarantee, no claim that all elements will ship, and no assertion that Generation 3 is desirable for every organisation. Many firms will operate at Generation 1 or 2 indefinitely — and that is the correct choice for them.

> **Cross-Generation Principles**
>
> Three commitments hold unchanged across all generations. **First:** the Klarna Test never softens. Every generation gates 'AI replaces human' decisions through the same scoring rubric. **Second:** partner agency does not decrease. Partners can opt out of crypto pay, the Unit Fund, or autonomous agent units at any generation. **Third:** the Brain remains the source of truth. Generation 2 smart contracts read the Brain; Generation 3 autonomous units write to the Brain. The Brain compounds across generations; nothing in v2 or v3 invalidates the v1 Brain.

---

## Section 5 — Tools and Legos: Why These Specific Components Were Chosen

Every tool in the ØØT ecosystem was chosen against two hard criteria: (1) it must not create vendor lock-in, and (2) it must maximise simplicity for the adopting founder. These criteria are documented in [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md) and [`docs/MODULES.md`](../../docs/MODULES.md) in the repository. What follows is an explanation of the key choices and the reasoning behind each.

### The Anti-Lock-In Architecture

The history of enterprise software is a graveyard of vendor lock-in. Every ERP, CRM, and HRIS system that promised 'the operating system for the future of work' ended up trapping organisations in proprietary data formats, migration costs, and dependency on a single vendor's survival. ØØT was architected from the outset to avoid this failure mode.

The foundational choice is plain markdown as the universal substrate. Every Skill Pack, every governance document, every Routine prompt, every Brain page is a markdown file. Markdown is readable by any text editor on any operating system built in any decade. It does not require a running server, a paid subscription, or a vendor's cooperation to access.

The framework's Skill Packs are based on the SKILL.md format — Anthropic's Agent Skills standard, which became an open standard governed by the Linux Foundation Agentic AI Foundation (AAIF) in December 2025. This means ØØT Skill Packs work in Claude Desktop, Claude Code, Cursor, LM Studio, ChatGPT, and any future MCP-compatible client. A question from [`SPEC.md`](../../SPEC.md) captures the principle directly: *'What if Anthropic changes? The framework is markdown and open standards. Skill Packs work in Cursor, LM Studio, ChatGPT, Claude Desktop, and any future MCP-compatible client. ØØT survives any single vendor change.'*

The Excel templates are standard `.xlsx` files, not Google Sheets formulas or Notion databases. They open in Excel, LibreOffice, Numbers, or Excel-for-Web. The Brain is a GitHub repository — version-controlled, cryptographically auditable, free for public repos, and migratable to any Git-compatible host.

### Key Cloud-Track Tools

[Claude Desktop](https://claude.com/download) and [Claude Code](https://code.claude.com/) (Anthropic) serve as the AI layer for the cloud track. Claude Code is the coding agent used for framework installation (Path A), Routine execution, and code review with Klarna Test gating. Claude Desktop is the daily conversational interface through which partners interact with the Brain, run Skill Packs, and receive automated Routine outputs. The choice reflects the framework's authors' hands-on testing across multiple coding agents — documented in the ØØT research articles ['Three Philosophies, One Goal'](2026-04-three-philosophies.md) and 'Behind the Curtain'.

GitHub provides the version-controlled Brain repository, audit trail, CI/CD for Skill Pack validation, and the Klarna gate (an `oot/klarna-test` status check that blocks AI-replaces-human PRs until the rubric is satisfied). Slack provides team communication with native Claude integration. Bitwarden provides open-source password management and is self-hostable via Vaultwarden. Yubikey provides hardware two-factor authentication for organisational admin accounts.

### Key Privacy-Track Tools

[LM Studio](https://lmstudio.ai/) is the local AI inference engine, running open-weight models (Qwen 3, Llama 3.3, DeepSeek) on the firm's own hardware. It provides an OpenAI-compatible API endpoint, enabling the same Skill Pack prompts to run locally without cloud API calls. The Desktop Commander MCP and GitHub MCP provide filesystem and repository access without cloud intermediation.

[4thtech](https://github.com/4thtech) provides the privacy-track communications layer: dChat for team messaging (on-chain, end-to-end encrypted, wallet-as-identity), dMail for external email (self-custodial), and on-chain file transfer. [PollinationX](https://wiki.pollinationx.io/) provides decentralised storage for bulk files (PDFs, media, archives) that are too large for the GitHub Brain repository.

The Excel MCP ([haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server), MIT-licensed) enables local LLMs to read and write the framework's nine Excel templates without any cloud dependency — providing full operational parity with the cloud track's Google Sheets and Claude extension approach. Trezor hardware wallets secure partner identity keys, treasury keys (Generation 2), and payroll wallet keys (Generation 2). The full [Privacy / Self-Sovereign Skill Pack (S12)](../../skills/privacy-self-sovereign/SKILL.md) documents the integration end-to-end.

### Cost Transparency

The framework is explicit about costs — a reflection of its honesty principle. For a ten-partner firm on the cloud track, estimated monthly costs include Anthropic Pro seats at approximately €200, Google Workspace at €120, Slack at €80, GitHub Team at €40, Bitwarden at €10, and Curator pay-as-you-go ingest at €20 — totalling approximately €470 per month. For a five-partner privacy-track firm, one-time hardware costs (Mac mini M4 Pro, UPS, five Trezors, two Yubikeys) total approximately €2,460, with ongoing monthly costs of approximately €55.

In both cases, the framework strongly recommends engaging local legal counsel at an initial cost of €5,000–€15,000 and ongoing annual engagement of €3,000–€8,000, particularly for EU AI Act compliance mapping, partner charter legalisation, and Generation 2 stablecoin payroll structuring.

*Further reading: [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md) and [`docs/MODULES.md`](../../docs/MODULES.md) in the ØØT repository ([github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)). The full curated index of external tools is at [`research/external-resources.md`](../external-resources.md).*

---

## Section 6 — The Curator and the Collecting Brain: The Firm's Compounding Intelligence

Of all the components in the ØØT stack, the Curator and its associated knowledge infrastructure are the most strategically important and the most differentiating. Understanding why requires understanding what the 'Collecting Brain' thesis actually claims.

### What the Collecting Brain Is

The Collecting Brain is not a filing system. It is a compounding knowledge graph — a structured, interlinked, machine-readable representation of everything the firm has learned, decided, produced, and committed. It is built on the intellectual foundations of Polanyi's tacit/explicit knowledge distinction (*The Tacit Dimension*, 1966), Nonaka and Takeuchi's SECI model of knowledge conversion (*The Knowledge-Creating Company*, 1995), Microsoft's GraphRAG architecture ([Edge et al., 2024](https://arxiv.org/abs/2404.16130)), and Andrej Karpathy's 'second brain' concept.

The five-level maturity model defined in the MANIFESTO:

| Level | State | Indicators |
|---|---|---|
| Level 0 | None | Knowledge lives in heads, Slack, scattered Drives |
| Level 1 | Flat docs | Confluence / Notion, no graph, no retrieval, no agent access |
| Level 2 | Vector RAG | Embedding-based search, no graph, single-tool retrieval |
| Level 3 | GraphRAG | Knowledge graph, hybrid retrieval, manual curation |
| **Level 4** | **Agentic MCP-native** | **The Curator pattern: graph + MCP + skill-driven write discipline** |

ØØT deploys at Level 4 by default. As stated in the [`MANIFESTO.md`](../../MANIFESTO.md): *'There is no point in retrofitting Levels 1-3 if you can start at the destination.'*

### What the Curator Application Is

The Curator ([github.com/talirezun/the-curator](https://github.com/talirezun/the-curator)) is an open-source desktop application and MCP server developed by Dr. Tali Režun. It turns a folder of plain markdown files into a queryable, traversable knowledge graph — accessible by any MCP-compatible AI client through the MyCuratorMCP server, which exposes seventeen tools: ten read tools and seven write tools.

The ten read tools include `list_domains`, `get_index`, `search_wiki`, `get_node`, `get_connected_nodes`, `get_backlinks`, `get_graph_overview`, `get_tags`, `search_cross_domain`, and `get_summary`. The seven write tools include `compile_to_wiki`, `fix_wiki_issue`, `scan_wiki_health`, `scan_semantic_duplicates`, `get_health_dismissed`, `dismiss_wiki_issue`, and `undismiss_wiki_issue`.

The Curator's ingest pipeline reads source documents (PDFs, articles, meeting notes, decision records, contract summaries) and converts them into an atomic knowledge graph following a strict ontological structure: **entities** (specific named things — people, companies, tools, products), **concepts** (ideas, frameworks, methodologies), and **summaries** (one per ingested source, providing the narrative connecting entities to concepts for that source).

The MyCuratorMCP article in the research archive ([*From Graph to Intelligence: The My Curator MCP and the Art of Querying Your Second Brain*](2026-04-graph-to-intelligence-mcp.md)) describes this capability: *'Your second brain — the one you have been building, source by source, over months or years — becomes a first-class research environment. Not a folder of files that a search bar can skim. A graph that a frontier model can reason against systematically, following connections, tracing influences, surfacing patterns you accumulated without consciously noticing them.'*

### How the Curator Integrates with ØØT

Within ØØT, the Curator is **Skill Pack S1** — the foundational skill upon which all other eleven packs depend. As stated in the [`SPEC.md`](../../SPEC.md): *'Every Skill writes to the Brain. The Curator is not a separate knowledge management tool. It is the substrate.'* The Code & QA Skill writes architectural decisions to the Brain. The Compensation & Attribution Skill writes ledger entries to the Brain. The Reporting Skill writes Business Review summaries to the Brain. Six months in, the Brain is the firm's most valuable asset, by construction.

The Curator's SKILL.md is imported verbatim into [S1](../../skills/my-curator/SKILL.md). Every other Skill Pack writes into the Brain via S1's discipline. This means the Brain's structure (entities, concepts, summaries; slug naming conventions; per-domain siloing) is enforced consistently across all automated operations. An agent cannot write a speculative wikilink to a non-existent page. It cannot create duplicates without the semantic-duplicate scan flagging them for review. The discipline is architectural, not advisory.

The Brain is also the substrate for the compensation system. The attribution agent in [Skill Pack S3](../../skills/compensation-attribution/SKILL.md) reads the Brain's knowledge graph to produce daily output ledgers, monthly variable statements, and quarterly long-tail entitlement calculations. The same node that records 'a partner drafted the term sheet on a specific date' feeds the variable pay calculation, the long-tail tracker, and the institutional memory simultaneously. As stated in the [MANIFESTO](../../MANIFESTO.md): *'The firm's value-creation model trains on the firm's own ground truth.'*

### The Shared Brain and the ØØT Cohort

The Curator's Sync feature enables a **Shared Brain** — a GitHub-backed knowledge repository accessible to multiple partners simultaneously. In the ØØT context, this creates a firm-level collective intelligence: a single Brain repository (the `oot-brain` repo, created during installation) that all partners read from and write to via the MyCuratorMCP server and their individual Curator desktop installations.

Each partner operates within designated domains (for example, `firm`, `customers`, `products`, `legal`). The per-domain siloing model ensures that customer-specific knowledge does not bleed into the firm's internal strategy domain, and that legal documents are appropriately separated from operational records. Cross-domain reasoning remains possible via the `search_cross_domain` tool; cross-domain linking is architecturally prevented.

The Curator's Routine R5 (the Brain Health Check, scheduled weekly) uses the `scan_wiki_health` and `scan_semantic_duplicates` tools to maintain the graph's integrity automatically. Broken wikilinks, orphaned pages, and semantic duplicates surface as health issues — reviewable by the founding partner, dismissable with a recorded rationale, or fixable with a one-command apply. A poorly-curated Brain, as the [MANIFESTO](../../MANIFESTO.md) honestly notes, becomes a museum of broken wikilinks and stale summaries that nobody trusts. R5 is the discipline that prevents this.

### Why SKILL.md Files Are Important

The SKILL.md format — defined by [Anthropic's Agent Skills specification](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) and now an open standard under the Linux Foundation AAIF — is the universal primitive through which ØØT encodes its methodology into AI-readable instruction manuals. Each Skill Pack consists of a SKILL.md file (the canonical instruction manual), optionally accompanied by a SPEC.md (the specification Claude Code uses to generate the SKILL.md), a `references` directory (the intellectual foundations), and an `examples` directory (worked examples).

SKILL.md files have three distinctive properties that make them powerful in practice. **First, progressive disclosure:** an agent loads approximately 100 tokens of a SKILL.md at startup (just the YAML frontmatter and the name/description), and loads the full file only when the skill is activated. This means twelve Skill Packs can coexist in an agent's context without overwhelming it. **Second, vendor neutrality:** a SKILL.md file works in Claude Desktop, Claude Code, Cursor, LM Studio, and any future MCP-compatible client. **Third, human readability:** a SKILL.md is a plain text file that a founder can read, understand, and audit without technical expertise.

The ØØT framework currently ships twelve hand-built Skill Packs. Seven are hardened at Tier 1 and production-ready: [S1 (My Curator — the Brain)](../../skills/my-curator/SKILL.md), [S2 (Context Engineering)](../../skills/context-engineering/SKILL.md), [S3 (Compensation & Attribution)](../../skills/compensation-attribution/SKILL.md), [S4 (Code & QA)](../../skills/code-qa/SKILL.md), [S5 (Reporting & Business Review)](../../skills/reporting-business-review/SKILL.md), [S6 (Change Management)](../../skills/change-management/SKILL.md), and [S12 (Privacy / Self-Sovereign Stack)](../../skills/privacy-self-sovereign/SKILL.md). Five are scaffolded at Tier 2 and will be hardened in Generation 2: [S7 (Governance & Compliance)](../../skills/governance-compliance/SKILL.md), [S8 (Legal Operations)](../../skills/legal-operations/SKILL.md), [S9 (Marketing)](../../skills/marketing/SKILL.md), [S10 (Finance & Treasury)](../../skills/finance-treasury/SKILL.md), and [S11 (Sales & BD)](../../skills/sales-bd/SKILL.md).

The SKILL.md format has been independently adopted across the industry. OpenAI's AGENTS.md (used in Codex CLI), GitHub Copilot's chatSkills, VS Code Skills, and Block's Goose agent all converged on the same primitive in 2025. The MCP downloads metric illustrates adoption scale: from 100,000 downloads in November 2024 to 8,000,000 downloads by April 2025, with 5,800 MCP servers and 300 clients now in production at Block, Bloomberg, Amazon, and hundreds of Fortune 500 companies.

*Further reading: [github.com/talirezun/the-curator](https://github.com/talirezun/the-curator); [`skills/my-curator/SKILL.md`](../../skills/my-curator/SKILL.md); [`docs/01-installing-the-curator.md`](../../docs/01-installing-the-curator.md); [`MANIFESTO.md`](../../MANIFESTO.md) Thesis 4 (Collecting Brain); [`research/articles/`](../articles/) (MyCuratorMCP article) — all in [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework).*

---

## Section 7 — Installing the Framework: Three Paths to Operational Reality

One of the most common barriers to framework adoption is installation complexity. ØØT was designed with this barrier explicitly in mind. The framework ships three distinct installation paths, documented in the [`installer/`](../../installer/) directory of the repository, each targeting a different type of founder.

### Path A — Coding-Agent-Assisted Install (Recommended)

Path A is the recommended path for 80% of founders, including those who have never opened a terminal or edited a JSON file. It hands the installation to a coding agent — Claude Code, Augment Code, Aider, OpenCode, Cline, Continue.dev, or any agent meeting the published capability specification — which reads the install plan, executes the steps, and asks the founder the questions a human installer would have to answer.

The wall-clock time is **60 to 90 minutes** for the cloud track. The agent handles the tasks that cause 60% of failed installs: editing `claude_desktop_config.json`, generating GPG signing keys, configuring GitHub branch protection, wiring MCP connections, and verifying each step. The founder answers questions (firm name, partner count, jurisdictions, which optional modules to skip) and approves consequential actions (creating a GitHub repository, generating a cryptographic key, configuring branch protection, anything that costs money).

The install plan's ground rules, as stated in the [`START-HERE.md`](../../installer/agent-assisted/START-HERE.md) file, are: read the full plan before starting; pause and confirm before any action that costs money, sends a message to a third party, creates an account, generates a cryptographic key, pushes to a remote repository, or configures branch protection; if a step requires a third-party service action (GitHub.com, Anthropic's website, the Curator app), provide the exact button-by-button sequence and wait for confirmation; translate technical steps into non-developer language.

At the end of installation, the agent produces a written install summary at `~/.oot/install-summary.md` — a document listing every action taken, every decision deferred, and every open follow-up. This document is the founder's audit trail. It can be shared with an accountant or handed to legal counsel.

### Path B — The Interactive Wizard

Path B is a Python terminal wizard ([`installer/wizard.py`](../../installer/wizard.py)) for founders who prefer not to use a coding agent. It is an interactive 14-step guided installation: preflight checks, Python virtual environment setup, firm profile collection, module selection, GitHub plan-tier choice, Anthropic API setup, Brain repository creation, signing key generation and GPG upload, git configuration, branch protection setup, Curator integration, Day-1 Routine configuration (R5 and R6), smoke test, and install summary generation.

The wizard is resumable (`--resume` flag) and supports a dry-run mode (`--dry-run`) to preview all actions before execution. It is programmatic where safe (folder creation, git operations, GPG key generation, file edits, smoke test) and provides web-UI walkthrough guidance where the founder must approve a third-party action (GitHub repository creation, branch protection rule, GPG public-key upload, MCP installation in Claude Desktop).

### Path C — Manual Installation

Path C is the manual path: every step documented in [`docs/00-quickstart-cloud.md`](../../docs/00-quickstart-cloud.md) (cloud) or [`docs/00-quickstart-privacy.md`](../../docs/00-quickstart-privacy.md) (privacy track), executed by the founder themselves. It is the most transparent path — nothing happens that the founder did not type — and the most demanding. The quickstart documentation is written explicitly for non-technical founders, including a plain-English primer on terminals, JSON files, GitHub, Git, and MCP.

The cloud-track manual path takes approximately two weekends of 16 hours total. The privacy-track manual path requires approximately 25 hours spread across two weekends plus one week for hardware shipping and delivery.

> **What You Get at the End of Installation (Cloud Track)**
>
> A fully operational ØØT instance with one partner onboarded; a real GitHub-hosted Brain repository with signed commits and branch protection; the Curator desktop app installed and integrated with Claude Desktop via the MyCuratorMCP server; four scheduled Routines running on Anthropic's infrastructure (R5 Brain Health Check, R6 EU AI Act Audit Trail, R1 Daily Output Capture, R2 Weekly Business Review Preparation); and an install summary document suitable for sharing with accountants or legal counsel. **Total wall-clock time on Path A: 60–90 minutes.**

*Further reading: [`installer/README.md`](../../installer/README.md); [`installer/agent-assisted/START-HERE.md`](../../installer/agent-assisted/START-HERE.md); [`installer/agent-assisted/cloud-install-plan.md`](../../installer/agent-assisted/cloud-install-plan.md); [`docs/00-quickstart-cloud.md`](../../docs/00-quickstart-cloud.md); [`docs/00-quickstart-privacy.md`](../../docs/00-quickstart-privacy.md) — all in [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework).*

---

## Section 8 — Who Benefits: Industries, Use Cases, and the Non-Technical Founder

A common misconception about ØØT is that it is a framework for technical companies building software products. This is understandable — the framework's most hardened Skill Pack ([S4, Code & QA](../../skills/code-qa/SKILL.md)) is explicitly about software development workflows. But the framework's scope is much broader, and its design deliberately accommodates the non-technical founder.

### The Non-Technical Founder's Use Case

ØØT was built to give less-technical founders clarity about what their development team is doing — how they are deploying, committing, reviewing code, and spending development hours. The framework's automated reporting layer ([Skill Pack S5, Reporting & Business Review](../../skills/reporting-business-review/SKILL.md), with its weekly Routine R2) produces a human-readable Business Review document every Friday morning: a summary of the previous week's output specifications completed, commitments made, Klarna Test results, and Brain health status. A non-technical founder can read this document without understanding a single line of code.

The Klarna Test gating is equally accessible. When a development team proposes replacing a human function with AI, the PR is automatically labelled `oot/klarna-test` and blocked from merging until the ten-question rubric is completed and scored at 14/20 or above. The founder reviews the rubric in plain English. They do not need to understand the technical implementation — they need to understand what is being proposed and whether it passes the quality gate. This is transparency architecture, not technical gatekeeping.

### Industry Applicability

The ØØT repository includes three [reference organisation examples](../../examples/): a small three-partner firm, a medium twelve-partner firm (the Brda Cooperative, an AI-augmented analytics firm serving the wine industry — illustrating that ØØT applies equally to non-digital industries), and a regulated EU firm with six partners operating under full EU AI Act mapping.

The framework's Skill Pack coverage addresses use cases across: software development ([S4 Code & QA](../../skills/code-qa/SKILL.md)), customer-facing communications and marketing ([S9 Marketing](../../skills/marketing/SKILL.md)), legal operations ([S8 Legal Operations](../../skills/legal-operations/SKILL.md)), financial management ([S10 Finance & Treasury](../../skills/finance-treasury/SKILL.md)), sales and business development ([S11 Sales & BD](../../skills/sales-bd/SKILL.md)), and governance and compliance ([S7 Governance & Compliance](../../skills/governance-compliance/SKILL.md)). The [MANIFESTO](../../MANIFESTO.md) references Human-AI augmentation evidence across software development (75% developer adoption; 41-46% of code AI-written), legal (Harvey AI deployed at 42% of AmLaw 100), marketing (73% of Frontier Firm employees using AI for marketing), customer service (81-93% of routine interactions automatable), accounting, and HR.

### The Savings Case: Repetitive Tasks and the Cost of Not Knowing

The framework's economic case operates on two dimensions: cost reduction from automation of repetitive tasks, and cost avoidance from informed decision-making. **On the first dimension:** the eight scheduled Routines automate the daily output capture, weekly Business Review preparation, weekly Brain health check, daily EU AI Act audit trail, monthly partner statements, quarterly long-tail entitlement settlement, Klarna Test gating, and an optional custom automation. These are tasks that — without automation — cost between two and eight hours per week of senior partner time.

**On the second dimension:** the Klarna Test alone prevents the failure mode that cost Klarna — by their own public account — the equivalent of hundreds of re-hired customer service roles. The cost of a single 'AI replaces human' decision made without rigorous quality gating can exceed the entire annual cost of operating the framework. The McKinsey *State of AI 2025* data contextualises this: AI high performers who redesign workflows end-to-end are 3.6 times more likely to achieve measurable P&L impact. The Deloitte 2025 *Digital Transformation Survey* reports 35% reduction in decision-making time, 42% improvement in resource allocation, and 28% boost in employee satisfaction at agentic-AI deployers who invest in proper workflow redesign.

---

## Section 9 — Open Source as Contribution: The Framework's Public Commitment

ØØT is published as open-source software under a dual licence: [Apache 2.0](../../LICENSE) for code, scripts, installers, Routine prompts, and attribution agents; [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](../../LICENSE-DOCS) for documentation, Skill Packs, templates, and governance documents. The choice to open-source the framework is not incidental — it is a direct expression of the framework's composability thesis.

The framework's [`CONTRIBUTING.md`](../../CONTRIBUTING.md) is explicit about what contributions are welcome and what are not. **Welcome:** bug fixes, new Routines that compose with the existing eight, new Skill Pack scenarios, new reference organisation examples, original research articles in the [`research/`](../../research/) directory, and ecosystem tool updates. **Not welcome:** vendor-specific lock-in (PRs that introduce dependency on a single SaaS vendor for a previously-vendor-neutral component are rejected); marketing language ('leverage', 'synergy', 'transformation journey' are rejected on style); unsourced claims (any statistic or assertion without a verifiable source is rejected).

The framework also rejects patches that bypass the Klarna Test discipline — including changes to the threshold, removal of the non-beneficiary review requirement, or weakening of audit-trail requirements. These are core governance commitments; they require an Architecture Decision Record (ADR) and founder sign-off.

The open-source commitment is anchored in the framework's institutional relationships. ØØT is integrated into the MBA Frontier Technologies curriculum at [COTRUGLI Business School](https://cotrugli.org/), where Dr. Režun serves as Vice Dean of Frontier Technologies. Dražen Kapusta — co-author of the Cotrugli Ledger — is a founding contributor, providing the institutional thesis that Generation 3 extends. COTRUGLI Business School serves as the institutional anchor for the framework's EU positioning.

The framework's regulatory positioning is deliberate. Given the EU AI Act's phased enforcement timeline — high-risk obligations entering full force on 2 August 2026 — ØØT is designed to be the compliance-aware agentic-organisation framework for EU-regulated environments. [Skill Pack S7 (Governance & Compliance)](../../skills/governance-compliance/SKILL.md) explicitly maps every automated operation to EU AI Act Articles 9 (risk management), 12 (record-keeping), 13 (transparency), and 14 (human oversight). GDPR Article 22 compliance (automated decision-making with significant effects) is addressed in the same skill pack. See [`governance/EU-AI-ACT.md`](../../governance/EU-AI-ACT.md) for the canonical mapping. This makes ØØT distinctively positioned as the open-source framework that takes EU regulation seriously — at a time when no comparable framework does.

---

## Section 10 — What Founders Gain: Generation 1 Benefits and the Future Roadmap

For a founder adopting ØØT Generation 1 today, the concrete operational benefits are:

- **A complete, auditable output-based compensation system** — replacing time sheets with Output Specifications, variable pay tied to accepted deliverables, and long-tail entitlements tracked for the life of each artefact.
- **An automated weekly Business Review** — prepared every Friday morning by a scheduled Routine, summarising the prior week's output specifications completed, commitments made, and Brain health status, readable by non-technical partners and founders.
- **A compounding knowledge graph** that captures every decision, contract, customer interaction, and architectural choice — making the firm more valuable with every passing week, and enabling compensation attribution that would otherwise require expensive manual tracking.
- **A Klarna Test governance gate** — blocking 'AI replaces human' decisions until they are rigorously scored, preventing the most common and costly failure mode in AI transformation.
- **EU AI Act compliance infrastructure** — for EU-regulated organisations, a daily audit trail (Routine R6) and a full Article 9/12/13/14 mapping built into the governance layer.
- **Data sovereignty optionality** — the privacy track provides full operational parity on local infrastructure, enabling organisations with regulatory constraints or philosophical commitments to self-custody to adopt the framework without any cloud LLM dependency.
- **A transparent technical window for non-technical founders** — automated reporting on commits, deployments, code quality, and Klarna Test results, providing the founder with an accurate picture of what the development team is doing without requiring them to understand code.

For **Generation 2** (6-12 months), the additions that matter most to most founders are: stablecoin payroll rails enabling per-milestone payment in USDC or EURC, smart-contract long-tail entitlements that pay automatically without manual quarterly settlement, and the Internal Unit Fund enabling partners to build equity-equivalent positions in the firm's compounding output.

For **Generation 3** (12-24 months, theoretical), the frontier capability is the autonomous agent business unit — an AI agent with its own LLC, accounts, contract authority, and compensation structure, operating within the same ØØT governance framework as human partners. This is the model that researchers like Andrej Karpathy describe when they speak of 'one-person unicorns' — firms with a handful of human decision-makers overseeing networks of specialised agents. ØØT provides the governance architecture to make this operationally honest rather than speculative.

The framework's roadmap is constrained by an explicit epistemic discipline: nothing is promised for Generation 2 or 3 that is not already demonstrated to be architecturally feasible. The Klarna Test applies to the framework's own development. Every feature that would have produced the Klarna outcome — replacing human capability before the quality bar is proven — is flagged and held.

---

## Section 11 — Conclusion: The Right Operating Model for This Moment

The Organisation of Tomorrow framework exists because the tools are ready and the organisations are not — and because no open-source framework has addressed all four of the structural gaps simultaneously: resistance management, output-based compensation, agentic knowledge infrastructure, and data sovereignty.

ØØT is built on thirty years of entrepreneurial practice, grounded in the strongest empirical findings of 2024-2026 enterprise AI research, anchored in open standards governed by the Linux Foundation, and published as a public good under Creative Commons and Apache licences. It is a framework for founders who want to build correctly from day one, and for leaders who want to transform their existing organisations without the catastrophic failure modes that have defined the first wave of enterprise AI adoption.

The framework is honest about its limits. Generation 1 is operationally complete; Generations 2 and 3 are roadmap commitments with explicit prerequisites and explicit uncertainty. The Klarna Test is not an aspiration — it is a blocking gate. The resistance problem is not an obstacle to be overcome with enthusiasm — it is a structural reality to be managed with discipline, measurement, and a 12-to-24-month time horizon.

What ØØT offers is not a guarantee of transformation. It offers a composable, auditable, sovereignty-respecting operating system for the partner-run, AI-augmented firm — one that the founders themselves can read, understand, modify, and own. The rest is up to the humans who use it.

---

## References

### Framework Repository and Documentation

- Režun, T. (2026). ØØT — Organisation of Tomorrow (v1.0). GitHub. [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)
- Režun, T. (2026). [`MANIFESTO.md`](../../MANIFESTO.md). In ØØT Framework Repository.
- Režun, T. (2026). [`GENERATIONS.md`](../../GENERATIONS.md). In ØØT Framework Repository.
- Režun, T. (2026). [`SPEC.md`](../../SPEC.md). In ØØT Framework Repository.
- Režun, T. (2026). [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md). In ØØT Framework Repository.
- Režun, T. (2026). [`docs/MODULES.md`](../../docs/MODULES.md). In ØØT Framework Repository.
- Režun, T. (2026). [`skills/my-curator/SKILL.md`](../../skills/my-curator/SKILL.md). In ØØT Framework Repository.
- Režun, T. (2026). [`installer/README.md`](../../installer/README.md). In ØØT Framework Repository.

### The Curator

- Režun, T. (2025–2026). The Curator (open-source desktop app + MyCuratorMCP server). GitHub. [github.com/talirezun/the-curator](https://github.com/talirezun/the-curator)
- Režun, T. (2026). *The MyCuratorMCP and the Art of Querying the Second Brain*. Research Article. In The Curator Repository, [github.com/talirezun/the-curator/tree/main/research](https://github.com/talirezun/the-curator/tree/main/research).

### Enterprise AI Research

- McKinsey & Company. (November 2025). *The State of AI 2025* (n=1,993, 105 countries). McKinsey Global Institute.
- MIT Project NANDA. (August 2025). *The GenAI Divide: Why 95% of Enterprise AI Pilots Fail*. Massachusetts Institute of Technology.
- METR. (July 2025). *Randomised Controlled Trial on AI Tools and Developer Productivity*. Cited in DORA Report 2025.
- METR. (February 2026). *Follow-up: AI-Assisted Productivity Perception Gap*. Machine Learning Research.
- Microsoft. (2025). *Work Trend Index 2025: The Frontier Firm*. Microsoft Corporation.
- Deloitte. (2025). *Digital Transformation Survey*. Deloitte Insights.
- Stack Overflow. (2024). *Developer Survey 2024*. Stack Overflow.
- CIO Dive. (2026). *Developer Resistance to AI in Deployment and Planning*. Industry Report.

### Knowledge Management Foundations

- Polanyi, M. (1966). *The Tacit Dimension*. Doubleday.
- Nonaka, I., & Takeuchi, H. (1995). *The Knowledge-Creating Company: How Japanese Companies Create the Dynamics of Innovation*. Oxford University Press.
- Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., & Larson, J. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research. [arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020.
- Awad, E. (2026). *Generative AI in Knowledge Management and Organizational Memory: RAG Patterns in Remote Work*. IGI Global.

### Compensation and Organisational Design

- Hope, J., & Fraser, R. (2003). *Beyond Budgeting: How Managers Can Break Free from the Annual Performance Trap*. Harvard Business School Press.
- Bogsnes, B. (2016). *Implementing Beyond Budgeting: Unlocking the Performance Potential*. Wiley.
- Levin, J., & Tadelis, S. (2005). *Profit Sharing and the Role of Professional Partnerships*. Quarterly Journal of Economics.
- YOLO Investments. (2025). *Stop Paying for Hours, Start Paying for Output*. Research Report (referenced in ØØT research archive).

### Standards and Governance

- Linux Foundation Agentic AI Foundation (AAIF). (December 2025). *MCP, AGENTS.md, and MCP Server Cards Open Standards Governance*. [lfaidata.foundation](https://lfaidata.foundation/)
- Anthropic. (October 2025). *Agent Skills (SKILL.md format) — Open Standard Declaration*. [docs.claude.com/en/docs/agents-and-tools/agent-skills/overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- European Commission. (2024). *EU Artificial Intelligence Act (Regulation (EU) 2024/1689)*. Official Journal of the European Union.
- Model Context Protocol. (2024–2026). *Open Specification*. [modelcontextprotocol.io](https://modelcontextprotocol.io/)

### Related Research by the Author

- Režun, T. (2026). *From One Agent to Coding Agent Armies: My 15-Month Journey to AI Orchestration*. Medium / 4thTech publication.
- Režun, T. (2026). [*Three Philosophies, One Goal: A Practitioner's Comparison of Augment Code, Claude Code, and Codex CLI*](2026-04-three-philosophies.md). Medium publication.
- Režun, T. (2026). *Behind the Curtain: The Three-Phase Process I Use to Build Every AI-Coded Product*. Medium publication.
- Režun, T. (2026). [*Building Knowledge Immortality Through the Second Brain Architecture and the Curator App*](2026-04-knowledge-immortality.md). Medium publication.
- Kapusta, D., Gams, M., Brčić, M., & Režun, T. (2026). *The Cotrugli Ledger*. International Leadership Journal.
- Režun, T. (2025). *From Online to On-Chain: The Evolution of Digital Communication*. Medium / 4thtech publication.

### Practitioner Sources

- Karpathy, A. (2026). *Software 1.0, 2.0, 3.0 Progression and 'Two Worlds of Code'*. Sequoia AI Ascent 2026 presentation.
- Klarna. (2024–2025). *AI-driven customer service transformation: public reporting and reversal* (used as the framework's cautionary reference). Various press releases.

---

## About the Author

Dr. Tali Režun is a serial entrepreneur, business developer, and academic at the forefront of frontier technologies. As Vice Dean of Frontier Technologies at COTRUGLI Business School, he leads AI innovation initiatives and shapes MBA curricula for the next generation of technology leaders. With over thirty years of entrepreneurial experience — founding and scaling ventures including The Curator, Lumina AI, Moj AI, Block Labs, 4thTech, Immu3, PollinationX, Online Guerrilla, Hipersound Records, Produkcija 97 — he bridges cutting-edge research in AI and Web3 with practical business transformation.

[github.com/talirezun](https://github.com/talirezun) | [researchgate.net/profile/Tali-Rezun](https://researchgate.net/profile/Tali-Rezun) | [cotrugli.org/talirezun](https://cotrugli.org/talirezun)

---

*This article is published under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](../../LICENSE-DOCS). It is **Research Article 1** in the **ØØT Research Series**. Subsequent articles cover specific Skill Packs, case studies, and empirical validation.*
