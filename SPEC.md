# ØØT Technical Specification

This document specifies the ØØT framework as it will be built. It covers the full eight-layer architecture (People, Tech, Skills, Excel, Routines, Process, Governance, Foundation), the complete Lego inventory with status labels, the Skill Pack catalogue, the Excel template schemas, and the Routine prompts.

It is the master reference. Read this once before building anything; consult it during build whenever a design question arises. If `SPEC.md` and another file disagree, `SPEC.md` is authoritative.

## How to read this document

The framework is described as a stack of **eight layers**, each containing a numbered inventory of **Legos** (composable units of work). Every Lego carries a status label:

- **✅ Exists** — a working component (often someone else's; we depend on it).
- **🌉 Bridged in Gen 1** — a gap filled with Excel + Routine + Skill, not native but functional.
- **🔜 Gen 1 (build now)** — a new component we build in this release.
- **🔜 Gen 2** — deferred to v2.0; scoped but not built.
- **🧪 Gen 3** — research-stage; scheduled for v3.0.
- **⚠️ External dependency** — we depend on someone else's roadmap; flagged for risk.

The status labels are how we are honest about the framework. v1.0 is operational because the Bridges are real bridges. The upgrade paths to v2 and v3 are real upgrade paths. Nothing in v1.0 conflicts with v2 or v3; everything in v2 and v3 has a clear preceding step in v1.0.

---

## Layer 1 — People (Partner system)

The unit of work is the **partner**, not the employee. The partner contracts for output, not hours; declares a reward species; receives a base + variable + long-tail compensation package; and (from Gen 2) holds Unit Fund credits and units.

| ID | Lego | Status | Implementation |
|---|---|---|---|
| P1 | Partner Charter (replaces employment contract) | 🌉 Gen 1 | Markdown template + signed PDF; reward-species declaration mandatory |
| P2 | Reward Species Declaration | 🌉 Gen 1 | `templates/excel/reward-species-declaration.xlsx` |
| P3 | Output Spec template — what "done" looks like for committed work | 🌉 Gen 1 | Markdown template per output |
| P4 | Partner Onboarding Skill — guided walkthrough | 🔜 Gen 1 | New SKILL.md (Skill Pack S2-adjacent) |
| P5 | Partner Output Ledger — daily record of shipped output | 🌉 Gen 1 | `partner-output-ledger.xlsx` + Routine R1 writes to it |
| P6 | Variable Pay Calculator | 🌉 Gen 1 | Built into ledger Excel (named ranges, formulas) |
| P7 | Long-Tail Entitlement Tracker | 🌉 Gen 1 | Sheet inside ledger Excel; smart-contract version is Gen 2 |
| P8 | Internal Unit Fund | 🔜 Gen 2 | Legal scoping required; YOLO recommends 6–9 months pilot first |
| P9 | Stablecoin payroll rail (USDC/EURC) | 🔜 Gen 2 | Rise / Circle integration; FIAT-only in Gen 1 |
| P10 | Klarna Test scoring (gate before any "AI replaces human" decision) | 🌉 Gen 1 | `klarna-test.xlsx` + `governance/KLARNA-TEST.md` + Routine R7 |
| P11 | Dispute resolution process | 🌉 Gen 1 | Three-tier playbook in `governance/DECISION-RIGHTS.md` |
| P12 | Partner exit + long-tail continuation | 🔜 Gen 2 | Touches legal in multiple jurisdictions |
| P13 | Cohort designation (full-time partner / project specialist / advisor) | 🌉 Gen 1 | Checkbox in reward-species declaration |
| P14 | Two Worlds of Code self-identification (Karpathy) | 🌉 Gen 1 | Section in onboarding skill; helps partner self-identify |

**Operating principle.** A partner is hired against an output spec, not a job description. The spec defines what "done" looks like. The reward-species declaration defines how the partner is compensated. The output ledger records what was shipped. The variable pay calculator computes monthly compensation. Long-tail tracker computes quarterly compounding compensation. The Klarna Test gates any decision that would replace a partner's work with AI.

---

## Layer 2 — Tech (the operational stack)

Two parallel tracks with full operational parity in Gen 1 (one trade-off: privacy track uses local cron instead of cloud Routines).

| ID | Lego | Status | Notes |
|---|---|---|---|
| T1 | The Curator + MyCuratorMCP — Collecting Brain | ✅ Exists | Reference implementation; SKILL.md canonical (S1) |
| T2 | GitHub as Brain sync substrate | ✅ Exists | Free, universal |
| T3 | Obsidian as human Brain view | ✅ Exists | Free; reads same markdown |
| T4 | Claude Desktop as daily driver (Cloud) | ✅ Exists | ⚠️ Anthropic dependency |
| T5 | Claude Code for development (Cloud) | ✅ Exists | Max plan recommended |
| T6 | Augment Code / Codex CLI / OpenCode | ✅ Exists | Optional; Augment for big builds, Codex for review/audit |
| T7 | Claude Code Routines — cloud automation engine | ✅ Exists | The connective tissue; Pro+ required, Max recommended for 3+ partners |
| T8 | Google Drive + Sheets + Docs | ✅ Exists | Cloud-track default; Claude connector |
| T9 | Microsoft Excel + Claude extension | ✅ Exists | Cloud-track alternative |
| T10 | Claude Chrome extension | ✅ Exists | Beta; works |
| T11 | Slack + Claude integration | ✅ Exists | Comms for cloud-track |
| T12 | Curator local-LLM ingest | 🔜 Gen 2 | On Curator roadmap; cloud-only today |
| T13 | LM Studio / Ollama with MCP support | ✅ Exists | Privacy-track local model runner; Qwen / Llama / DeepSeek |
| T14 | Desktop Commander MCP — local filesystem bridge | ✅ Exists | Privacy-track replacement for Drive |
| T15 | 4thtech dMail / dChat / W2W file transfer | ✅ Exists | Privacy-track on-chain comms layer |
| T16 | PollinationX — decentralised storage | ✅ Exists | Privacy-track Drive replacement; NFT-based capacity |
| T17 | GitHub MCP for cross-machine Brain sync | ✅ Exists | Free; works with local LLMs |
| T18 | Playwright MCP / Open WebUI alternatives | ✅ Exists | Open-source Cloud-track equivalents |
| T19 | Lumina AI widget — RAG chatbot for external surfaces | ✅ Exists | Sales/support front door |
| T20 | Attribution agent (reads commits/specs/reviews → ledger) | 🌉 Gen 1 | Routine + Skill + Excel; Gen 2 = dedicated agent |
| T21 | Cotrugli Ledger anchoring (PAC-ROs + Cotrugli Score + Vanguard Score) | 🧪 Gen 3 | Theoretical; field validation in progress |
| T22 | Multi-agent orchestration (Augment Intent, Claude Agent Teams) | 🔜 Gen 2 | Available but immature for org-wide use |
| T23 | Kelly-style autonomous business unit (agent with own LLC) | 🧪 Gen 3 | Reference: OpenClaw / Kelly case |
| T24 | Secrets vault — Bitwarden (passwords/tokens) + Trezor (crypto signing) | 🌉 Gen 1 | Two-layer; `governance/SECRETS-POLICY.md` |
| T25 | Excel MCP for privacy track (`haris-musa/excel-mcp-server`) | ✅ Exists | The piece that gives privacy track full automation parity |
| T26 | OS-native scheduling (launchd / cron / Task Scheduler) | ✅ Exists | Privacy-track cron equivalent of cloud Routines |

**Cloud track and privacy track at a glance.**

| Layer | Cloud (canonical) | Privacy (full Gen 1 parity) |
|---|---|---|
| Daily driver | Claude Desktop / Claude.ai | Claude Desktop with local-only MCPs **or** LM Studio / Ollama |
| Models | Claude Opus/Sonnet, Gemini | Llama, Qwen, DeepSeek, gpt-oss (local) |
| Knowledge | Curator + MyCuratorMCP (cloud ingest) | Curator + MyCuratorMCP (cloud ingest today; local LLM ingest = Gen 2) |
| Filesystem | Google Drive (Claude connector) | Desktop Commander MCP |
| Office | Drive + Sheets + Docs | Local Excel + Excel MCP (`haris-musa/excel-mcp-server`) |
| Code | Claude Code, Augment Code, Codex CLI | Open Codex / OpenCode (local-runnable) |
| Browser | Claude Chrome extension | Playwright MCP / local automation |
| Comms — internal | Slack (Claude integration) | 4thtech dChat (W2W, on-chain, E2E encrypted) |
| Comms — external | Email, Slack | 4thtech dMail (wallet-as-identity, self-custodial) |
| File transfer | Drive | 4thtech on-chain file transfer + PollinationX bulk storage |
| Automation | Claude Code Routines (laptop closed) | Local cron / launchd / Task Scheduler + headless LM Studio (laptop on) |
| Compensation rails | FIAT (Gen 1 default) | FIAT → Stablecoin upgrade path (Gen 2) |
| Governance | GitHub + EU AI Act Skill Pack | GitHub + EU AI Act Skill Pack (+ Cotrugli Ledger Gen 3) |

The privacy track is at full operational parity in Gen 1. The single trade-off: cloud Routines run while the laptop is closed; privacy-track cron equivalents need a machine on (a small always-on box like a Mac mini, NUC, or Raspberry Pi 5 covers this).

---

## Layer 3 — Skill Packs (the ØØT methodology, encoded)

Twelve hand-built Skill Packs. Each follows the canonical structure defined in `skills/_TEMPLATE_SKILL.md` (modelled on the My Curator skill). Each gets a per-pack `SPEC.md` in `skills/<pack-name>/SPEC.md` that Claude Code uses to generate the full SKILL.md.

**Tier 1 — hardened in v1.0 (full SKILL.md + examples + scripts):**

| # | Pack | Path | Anchors |
|---|---|---|---|
| S1 | My Curator | `skills/my-curator/` | Curator MCP, GraphRAG, SECI; imported from `talirezun/the-curator` |
| S2 | Context Engineering | `skills/context-engineering/` | Foundational meta-skill; "Prompts to Precision" + Schmid |
| S3 | Compensation & Attribution | `skills/compensation-attribution/` | YOLO model, ROWE, Levin & Tadelis; Gen 1 = layers 1–3+5; Gen 2 = layers 4,6,7 |
| S4 | Code & QA | `skills/code-qa/` | CLAUDE.md, AGENTS.md, Plan Mode, parallel sessions, Klarna Test pre-merge gate |
| S5 | Reporting & Business Review | `skills/reporting-business-review/` | Beyond Budgeting, daily ledger, weekly BR |
| S6 | Change Management / Resistance | `skills/change-management/` | Kotter+ADKAR, METR baseline, AI Champion criteria |
| S12 | Privacy / Self-Sovereign Stack | `skills/privacy-self-sovereign/` | 4thtech + PollinationX + LM Studio + Excel MCP — orchestrates the privacy track |

**Tier 2 — scaffolded in v1.0, hardened in v1.x (frontmatter + outline + TODO sections):**

| # | Pack | Path | Anchors |
|---|---|---|---|
| S7 | Governance & Compliance | `skills/governance-compliance/` | EU AI Act 9/12/13/14, GDPR Art. 22, decision-rights, Cotrugli Ledger as future option |
| S8 | Legal Operations | `skills/legal-operations/` | Harvey-style patterns, contract review, partner agreement templates |
| S9 | Marketing | `skills/marketing/` | AI marketing team workflow, Lumina-as-front-door |
| S10 | Finance & Treasury | `skills/finance-treasury/` | FIAT payroll first, stablecoin upgrade path, agent-cost attribution |
| S11 | Sales & BD | `skills/sales-bd/` | Brain-fed pipeline, outreach, Lumina widget integration |

**Sequencing.** S1 (My Curator) is the foundation — every other pack writes into the Brain. S2 (Context Engineering) is the meta-skill — every other pack assumes a partner who can construct context. S3 (Compensation & Attribution) is the most distinctive ØØT contribution — it is what differentiates ØØT from generic Skill catalogues. S4 (Code & QA) wires the Klarna Test into the engineering practice. S5 (Reporting & BR) is the operational heartbeat. S6 (Change Management) is the survival kit. S12 (Privacy / Self-Sovereign) ties the privacy-track tools into a coherent operating mode.

Tier 2 packs are scaffolds in v1.0 — they have the frontmatter, the section structure, and TODOs for the substantive content. Founders can fill them in for their organisation's domain; or wait for v1.x community contributions.

---

## Layer 4 — Excel Legos (gap-bridging spreadsheets)

Nine pre-built `.xlsx` files. All are formula-driven. All are written to and read from by Routines. Spreadsheets are **review and edit surfaces**, not data-entry surfaces — humans inspect, override, annotate; Routines handle the entry.

| # | File | Updated by | Reviewed by | Status |
|---|---|---|---|---|
| X1 | `partner-output-ledger.xlsx` | Daily Routine (R1) | Weekly BR | 🌉 Gen 1 |
| X2 | `reward-species-declaration.xlsx` | Manual at onboarding | Quarterly check-in | 🌉 Gen 1 |
| X3 | `business-review.xlsx` | Weekly Routine (R2) | Friday BR meeting | 🌉 Gen 1 |
| X4 | `klarna-test.xlsx` | Per-decision manual | Every "AI replaces human" event | 🌉 Gen 1 |
| X5 | `metr-baseline.xlsx` | Pilot owner | Pre + post AI rollout | 🌉 Gen 1 |
| X6 | `agent-skill-roi.xlsx` | Daily Routine (R1 + R8 inputs) | Monthly BR | 🌉 Gen 1 |
| X7 | `eu-ai-act-mapping.xlsx` | Manual w/ Skill assist | Compliance review | 🌉 Gen 1 |
| X8 | `treasury-runway.xlsx` (**OPTIONAL** — only orgs adopting Unit Fund) | Weekly Routine (R8) | Monthly BR | 🌉 Gen 1 |
| X9 | `oot-readiness.xlsx` | Founder, once at adoption | Founder | 🌉 Gen 1 |

Detailed schemas, formulas, and Routine integration points are in `templates/excel/SPEC.md`. The xlsx skill (Anthropic public skill) generates the actual files from those specs.

---

## Layer 5 — Routines (the cloud automation jobs)

Eight scheduled Routines pre-shipped as templates. Cloud track = Claude Code Routines. Privacy track = OS-native scheduling (cron / launchd / Task Scheduler) hitting headless LM Studio. Both use the same Skill Packs and the same prompts; only the execution substrate differs. Operational `.xlsx` state lives in the firm's Ledger and is mutated by Routines via openpyxl + signed commits per [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](docs/internal/ADR-001-cloud-routine-excel-writeback.md).

| # | Routine | Trigger | Output |
|---|---|---|---|
| R1 | Daily Output Capture | Daily 18:00 | Read GitHub commits, Slack threads, Drive activity → write rows to `partner-output-ledger.xlsx` |
| R2 | Weekly BR Prep | Friday 08:00 | Build agenda from ledger, list blockers, surface Klarna Test hits → populate `business-review.xlsx` |
| R3 | Monthly Variable Calc | 1st of month 09:00 | Lock previous month's ledger, calculate variable pay, send draft to each partner for review |
| R4 | Quarterly Long-Tail Settlement | 1st of quarter | Calculate long-tail entitlements per partner per output, prep payment list |
| R5 | Brain Health Check | Weekly Sunday | Run Curator `scan_wiki_health`, post issues to Slack/dChat |
| R6 | EU AI Act Audit Trail | Daily 23:00 | Append day's agent decisions to audit log per Article 12 |
| R7 | Klarna Test Trigger | GitHub event: PR labelled `ai-replaces-human` | Auto-launch Klarna Test scoring; block merge until ≥14/20 |
| R8 | Treasury Runway Update (**OPTIONAL**) | Weekly Monday 08:00 | Pull bank balances + obligations → update `treasury-runway.xlsx` |

Full Routine prompts are in `routines/SPEC.md`.

---

## Layer 6 — Process / Cadence

The operational heartbeat. Encoded as Skills (R-Routines write the data; humans run the meetings).

| # | Lego | Cadence | Status |
|---|---|---|---|
| C1 | Daily ledger update (R1) | Daily 18:00 | 🌉 Gen 1 |
| C2 | Friday Business Review (30 min, Brain-generated agenda) | Weekly | 🌉 Gen 1 |
| C3 | Quarterly partner check-in (numbers, long-tail, unit position) | Quarterly | 🌉 Gen 1 |
| C4 | Pre-rollout METR baseline (mandatory before any Skill rollout) | Per rollout | 🌉 Gen 1 |
| C5 | 6–8 week pilot template (15–20% of team) | Per rollout | 🌉 Gen 1 |
| C6 | AI Champion criteria (earned, not appointed) | Continuous | 🌉 Gen 1 |
| C7 | Klarna Test gate before any automation that displaces people | Per decision | 🌉 Gen 1 |

**The Friday Business Review.** 30 minutes. The agenda is generated by Routine R2 from the partner output ledger. Topics: outputs shipped this week (per partner), blockers, decisions due, Klarna Test hits, KPI movements. No status updates — those are visible in the ledger. The meeting is for the things the ledger cannot decide on its own.

**The quarterly partner check-in.** Per partner, with the founder or designated lead. Topics: their numbers (variable pay trend, long-tail growth, unit holdings if applicable), reward-species reconfirmation (still the right declaration?), career trajectory, framework feedback.

---

## Layer 7 — Governance

Four governance documents in `governance/`. Each is operational — it gets used in the framework's daily and decision-making rhythm, not stored on a shelf.

| # | Lego | File | Status |
|---|---|---|---|
| G1 | Decision Rights matrix (RACI-style) | `DECISION-RIGHTS.md` | 🌉 Gen 1 |
| G2 | Klarna Test (signature epistemic check) | `KLARNA-TEST.md` | 🌉 Gen 1 |
| G3 | EU AI Act mapping (Articles 9, 12, 13, 14) | `EU-AI-ACT.md` | 🌉 Gen 1 |
| G4 | GDPR Article 22 audit trail pattern | (within `EU-AI-ACT.md`) | 🌉 Gen 1 |
| G5 | Three-tier dispute resolution | (within `DECISION-RIGHTS.md`) | 🌉 Gen 1 |
| G6 | License pair (Apache 2.0 + CC BY-SA 4.0) | `LICENSE`, `LICENSE-DOCS` | 🌉 Gen 1 |
| G7 | Triple-entry-style audit logs in plain markdown | (deferred) | 🔜 Gen 2 |
| G8 | Cotrugli Ledger anchoring | (deferred) | 🧪 Gen 3 |
| G9 | Secrets policy (Bitwarden + Trezor two-layer) | `SECRETS-POLICY.md` | 🌉 Gen 1 |

**The legal touchpoint map** lives in `docs/06-when-to-call-a-lawyer.md` and identifies the eleven jurisdiction-specific places where local counsel is mandatory. ØØT does not provide legal advice; it points at the landmines.

---

## Layer 8 — Foundation kit (this repository)

The 16 canonical files that constitute the foundation kit. These are produced once, then Claude Code generates the rest of the repository from them.

| # | File | Status |
|---|---|---|
| F1 | `README.md` | 🔜 Build |
| F2 | `MANIFESTO.md` | 🔜 Build |
| F3 | `SPEC.md` (this file) | 🔜 Build |
| F4 | `GLOSSARY.md` | 🔜 Build |
| F5 | `QUICKSTART.md` (Cloud + Privacy paths) | 🔜 Build |
| F6 | `CLAUDE.md` (Claude Code orientation) | 🔜 Build |
| F7 | `BUILD-INSTRUCTIONS.md` (orders for Claude Code) | 🔜 Build |
| F8 | `governance/KLARNA-TEST.md` | 🔜 Build |
| F9 | `governance/EU-AI-ACT.md` | 🔜 Build |
| F10 | `governance/DECISION-RIGHTS.md` | 🔜 Build |
| F11 | `governance/SECRETS-POLICY.md` | 🔜 Build |
| F12 | `skills/_TEMPLATE_SKILL.md` | 🔜 Build |
| F13 | `skills/<pack>/SPEC.md` × 12 | 🔜 Build |
| F14 | `templates/excel/SPEC.md` (9 spreadsheets) | 🔜 Build |
| F15 | `routines/SPEC.md` (8 cloud + 8 privacy) | 🔜 Build |
| F16 | `GENERATIONS.md` (roadmap explicit) | 🔜 Build |

Plus `docs/SPEC.md`, which tells Claude Code what to generate for the 12 plain-language user guides.

---

## Build philosophy

A few principles to remember during scaffolding and ongoing development:

**Every Skill writes to the Brain.** The Curator is not a separate "knowledge management" tool. It is the substrate. Code & QA writes architectural decisions to the Brain. Compensation & Attribution writes ledger entries to the Brain. Reporting writes BR summaries to the Brain. Six months in, the Brain is the firm's most valuable asset, by construction.

**Every Skill is a markdown file.** No vendor-locked plugins. No proprietary formats. No SaaS dependencies that aren't strictly necessary. SKILL.md, AGENTS.md, MCP server cards, plain markdown. The framework should be readable by a text editor on any machine in any decade.

**Every Routine respects the Klarna Test.** R7 is the explicit gate. But every other Routine should also be designed so that its outputs are reviewable, reversible, and human-overridable. No silent automation of consequential decisions.

**Every spreadsheet is a review surface, not a source of truth.** The Brain is the source of truth. The Excel files are formula-driven views over the Brain's underlying data, designed for human inspection. Humans can edit them — those edits flow back to the Brain — but the canonical record is in the Brain, not the spreadsheet.

**Every cloud component has a privacy-track equivalent.** This is non-negotiable. If a cloud-only tool enters the framework, the privacy track loses parity, and ØØT's sovereignty thesis becomes lip service. Excel MCP, 4thtech, PollinationX, LM Studio, Desktop Commander, OS-native scheduling — each one exists because the cloud-only alternative fails the privacy-parity test.

**Generations are real, not marketing.** Gen 1 is what works today. Gen 2 is what works in 6–12 months *if* legal scoping completes and the necessary infrastructure (stablecoin rails, smart-contract long-tail, Curator local-LLM ingest) lands. Gen 3 is research-stage. Adopting ØØT in Gen 1 does not require commitment to Gen 2 or 3; the upgrade path is real but optional.

**The Klarna Test is not negotiable.** If a feature, recommendation, automation, or rollout would have produced the Klarna outcome, it gets flagged. No exceptions. No "but in our case…". The test exists precisely because every organisation thinks they're the exception.