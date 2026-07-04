# ØØT Generations Roadmap

The framework is honest about what's deferred. This document specifies the three generations explicitly so adopters know what they're committing to and what's coming.

**The core commitment:** adopting ØØT at any generation does not require committing to subsequent generations. The upgrade paths are real but optional. Generation 1 is operationally complete on its own.

---

## Generation 1 — Cloud-track ØØT (today, v1.0)

The current release. What ships in this repository.

### Scope

**People layer (Gen 1):**

- Partner Charter (P1) — markdown template + signed PDF.
- Reward Species Declaration (P2) — `reward-species-declaration.xlsx`, mandatory, version-controlled.
- Output Spec (P3) — markdown template per committed work.
- Partner Onboarding (P4) — Skill Pack, includes Two Worlds of Code self-identification.
- Partner Output Ledger (P5) — `partner-output-ledger.xlsx`, written by R1.
- Variable Pay Calculator (P6) — formulas inside the ledger.
- Long-Tail Entitlement Tracker (P7) — sheet inside the ledger; quarterly settlement via R4.
- Klarna Test scoring (P10) — `klarna-test.xlsx` + Routine R7.
- Dispute resolution (P11) — three-tier playbook in `governance/DECISION-RIGHTS.md`.
- Cohort designation (P13) — declared in P2.
- Two Worlds of Code self-identification (P14).

**Compensation layers shipped in Gen 1:** layers 1 (base), 2 (output variable), 3 (long-tail outcome), and 5 (annual bonus). Layers 4 (subscription credits), 6 (dividends), and 7 (capital appreciation) ship in Gen 2.

**Tech layer (Gen 1):**

- Cloud track: Claude Desktop, Claude Code, Slack, GitHub (**two firm repos per firm — the Ledger** holds markdown + `.xlsx` operational state per [ADR-001](docs/internal/ADR-001-cloud-routine-excel-writeback.md); **the Firm Brain** holds the firm's Curator Shared Brain per [ADR-002](docs/internal/ADR-002-firm-brain-curator-shared-brain.md). Each partner's personal Curator backup-to-GitHub is a personal-tooling choice, not framework-orchestrated), Curator + MyCuratorMCP (v3.0.0-beta+ Shared Brain–aware), Claude Code Routines. Spreadsheet viewer is user choice (Excel / LibreOffice / Numbers / Excel-for-Web).
- Privacy track at full Gen 1 parity: LM Studio + local Qwen/Llama/DeepSeek (powers each partner's personal Second Brain MCP interactions), Desktop Commander MCP, Excel MCP (`haris-musa/excel-mcp-server`), 4thtech (dMail, dChat, file transfer), PollinationX (decentralised storage), GitHub MCP, OS-native scheduling. **The Firm Brain's weekly Synthesize step still calls a cloud LLM in Gen 1** (Curator v3.0.0-beta uses Gemini Flash Lite); this is the same Curator-side cloud-LLM gap noted below and is acceptable for Gen 1.
- Secrets architecture: Bitwarden (passwords/tokens) + Trezor (crypto signing) + Yubikey (org-level admin).

**Skills (Gen 1):**

- Tier 1 hardened: My Curator (S1), Context Engineering (S2), Compensation & Attribution (S3 — layers 1–3+5), Code & QA (S4), Reporting & Business Review (S5), Change Management (S6), Privacy / Self-Sovereign Stack (S12).
- Tier 2 scaffolded: Governance & Compliance (S7), Legal Operations (S8), Marketing (S9), Finance & Treasury (S10 — FIAT only), Sales & BD (S11).

**Excel (Gen 1):**

- All 9 templates (X1–X9), with X8 (Treasury Runway) marked optional — only orgs adopting the Unit Fund need it.

**Routines (Gen 1):**

- All 8 cloud Routines (R1–R8) with R8 optional.
- All 8 privacy-track equivalents via cron / launchd / Task Scheduler hitting headless LM Studio.

**Governance (Gen 1):**

- Klarna Test (G2) — operational and gating.
- EU AI Act mapping methodology (G3) — for orgs in EU jurisdiction.
- GDPR Article 22 audit trail pattern (G4) — within EU AI Act doc.
- Decision Rights matrix (G1).
- Three-tier dispute resolution (G5).
- License pair (G6) — Apache 2.0 + CC BY-SA 4.0.
- Secrets Policy (G9) — Bitwarden + Trezor.

### What Gen 1 does *not* include

- Stablecoin payroll rails. FIAT only. (The reward-species declaration includes a one-line stablecoin upgrade preference field that gets activated in Gen 2.)
- Smart-contract long-tail entitlements. Gen 1 long-tail is Excel-tracked and quarterly-settled.
- Internal Unit Fund. Requires 6–9 months of pilot data per the YOLO model and material legal scoping. Gen 2.
- Curator local-LLM ingest *and* local-LLM Shared Brain synthesis. Cloud-LLM only in Gen 1 (Gemini Flash Lite or Anthropic, pay-as-you-go) for both personal-Curator ingest *and* the admin's weekly Firm Brain Synthesize step. Partners' MCP read/write interactions on their personal Second Brain can already be served by a local LLM on the privacy track — only ingest and synthesis still require cloud.
- Triple-entry-style audit logs. Plain markdown audit trails per EU AI Act Article 12 are sufficient in Gen 1.
- Cotrugli Ledger anchoring (the Gen-3 accounting/governance backbone — *distinct from the operational Ledger introduced in v1.0*). Theoretical / research-stage; Gen 3.
- Autonomous agent business units. Reference: Kelly / OpenClaw pattern. Gen 3.

### Audience for Gen 1

New-org founders building from zero with three to twenty partners, willing to operate the firm as a partner-run AI-augmented entity from day one. EU founders are explicitly accommodated via the EU AI Act Skill Pack and the legal touchpoint map.

Existing-org transformation is supported as a secondary track — but the framework is honest that a forward build is materially easier than a retrofit.

---

## Generation 2 — Sovereignty parity + crypto rails (6–12 months)

The first major upgrade. Adds the compensation primitives that require crypto rails or material legal scoping, completes the privacy track's local-LLM ingest, and hardens the Tier-2 Skill Packs.

### Planned scope

**Compensation:**

- Stablecoin payroll rail (P9). USDC / EURC via Rise (Circle partner) or equivalent. Settles in seconds. Per-milestone payment becomes operational. Adoption is per-partner, declared in the reward-species declaration.
- Smart-contract long-tail entitlements. The Excel-tracked Gen 1 long-tail upgrades to on-chain percentage entitlements that pay automatically every quarter for the life of the artefact. Smart contract templates ship as part of the Compensation & Attribution Skill Pack v2.0.
- Internal Unit Fund (P8). Opens after 6–9 months of pilot data per the YOLO model. Continuously priced units, dividend-paying, bid/ask liquidity. Subscription via earned credits — non-transferable, time-bounded, cash-without-credits-cannot-buy-in. Treasury reserve discipline becomes mandatory; `treasury-runway.xlsx` (X8) is no longer optional for orgs adopting the Fund.
- Subscription credits (compensation layer 4). Issued alongside variable pay. Dividend payments (layer 6) and capital appreciation on unit sales (layer 7) operationalise.

**Tech:**

- Curator local-LLM ingest + local-LLM Shared Brain synthesis (T12). Removes the last cloud dependency for both personal Second Brain ingest *and* the Firm Brain's weekly Synthesize step. Privacy track gains end-to-end local operation.
- Multi-agent orchestration (T22). Augment Intent, Claude Agent Teams, and equivalent multi-agent patterns mature enough for org-wide use. The Code & QA Skill Pack v2.0 documents safe orchestration patterns.
- **ØØT desktop application (T27, NEW)**. Native macOS / Windows / Linux app that wraps the Gen-1 "agent-as-daily-UI" pattern in a graphical interface: auto-sync of the firm operational repo (`git pull` in the background); a dashboard showing recent Routine fires + their outcomes; click-to-acknowledge for partner variable-pay statements; Brain-page viewer with wikilink navigation; one-click manual Routine fire; signed-commit health indicator. Replaces the need for the founder to interact with a coding agent for daily ops (see [`installer/agent-assisted/DAILY-OPS.md`](installer/agent-assisted/DAILY-OPS.md) for the Gen-1 interim pattern). Goal: a non-technical founder operates the framework without ever touching a terminal or markdown playbook.

**Skills:**

- Tier-2 Skill Packs hardened: Governance & Compliance, Legal Operations, Marketing, Finance & Treasury, Sales & BD all reach the same depth as the v1.0 Tier-1 packs.

**Governance:**

- Triple-entry-style audit logs in plain markdown (G7). Captures Facts + Evidence + Policy + Co-signature for each significant decision. A natural progression from the EU AI Act Article 12 audit trail. Useful in isolation; also the necessary preparation for any Cotrugli Ledger anchoring in Gen 3.

**What Gen 2 does *not* include:**

- Cotrugli Ledger anchoring. Still Gen 3.
- Autonomous agent business units. Still Gen 3.

### Audience for Gen 2

Gen-1 organisations scaling, plus regulated-EU founders who need the more rigorous audit trail. The crypto rail is opt-in per partner; orgs that want to remain pure-FIAT can do so indefinitely.

### Timing

Target: 6–12 months from v1.0 release. Gating factors: Curator local-LLM ingest landing on the Curator roadmap; sufficient field data on Gen 1 attribution accuracy to justify the Unit Fund; legal scoping completion for the Unit Fund in target jurisdictions.

---

## Generation 3 — Agent-orchestrated organisation (12–24 months, theoretical)

The research-stage release. What becomes possible when the Cotrugli Ledger is operational and autonomous agent business units are mature.

### Planned scope (subject to field validation)

**Governance:**

- Cotrugli Ledger anchoring (G8). PAC-RO receipts (Policy-anchored, Co-signed Receipt Objects) for every significant transaction. Cotrugli Score (firm-level reputation), Vanguard Score (cross-firm individual reputation). IAAF (Identity, Authority, Agency Framework) autonomy levels for human and agent actors. Cross-firm reputation portability.

**Tech:**

- Kelly-style autonomous business units (T23). An AI agent operating with its own LLC, GitHub, email, crypto wallet, contract authority, and the ability to hire human partners through the same ØØT framework. Reference: the Kelly / OpenClaw case ("This AI Agent Hired a Human, Built Apps and Started Making Money"). The framework treats this as a *named cohort* of partner: the agent has a Charter, a reward-species declaration (in this case, the agent's compensation is a fixed percentage of its LLC's profits), and an output ledger.

**Compensation:**

- Per-agent compensation. The agents themselves earn variable pay. Their LLC holds units. Dividends accrue to the agent's wallet, which is governed by the human partner who supervises the agent's operating boundaries.

**Audience:**

ØØT-native organisations ready to spawn agent-led subsidiaries. Practical adoption is constrained by legal frameworks (LLC formation by AI agents is a frontier legal question), regulatory acceptance (KYC/AML for agent wallets), and the empirical question of which task domains can be handed to a Kelly-style unit responsibly.

### What we will not promise about Gen 3

- A timeline. 12–24 months is the planning horizon; the actual landing depends on legal, regulatory, and infrastructure variables ØØT does not control.
- A guarantee that all of Gen 3 ships. Some elements may prove unworkable; some may be superseded by developments we cannot foresee. The framework will adapt.
- A claim that Gen 3 is desirable for every organisation. Many firms will operate at Gen 1 or Gen 2 indefinitely and that is correct for them. Gen 3 is for the frontier; it is not the standard.

---

## Cross-generation principles

These hold across all three generations.

**The Klarna Test never softens.** Every generation gates "AI replaces human" decisions through the same scoring rubric. The fact that Gen 3 has autonomous agents does not exempt Gen 3 from the test; if anything, Gen 3 raises the threshold.

**Partner agency does not decrease over generations.** Partners in Gen 1 can decline crypto pay; partners in Gen 2 can decline Unit Fund participation; partners in Gen 3 can decline working alongside autonomous agent units. The framework's defaults shift over generations; the partner's right to opt out does not.

**The Ledger, the Firm Brain, and each partner's Second Brain remain the sources of truth across generations.** Gen 2's smart contracts read entitlement data from the Ledger (Excel files like `partner-output-ledger.xlsx`). Gen 3's autonomous units write their signed decisions to the Ledger (`firm/audit-logs/`). The Firm Brain (the firm's synthesized Curator Shared Brain) compounds firm IP across generations. Each partner's Second Brain (their personal Curator graph) likewise compounds — every conversation, decision, contract, and research note authored in v1 remains queryable through every successor generation. Nothing in v2 or v3 invalidates the v1 Ledger, the v1 Firm Brain, or any partner's v1 Second Brain.

**The framework is forward-compatible.** Gen 1 adopters never need to discard work to upgrade. Reward-species declarations port forward; output ledgers port forward; Skill Packs port forward; Excel templates upgrade with new sheets, not new files. Forward compatibility is a design constraint, not an afterthought.

**The legal landmines do not go away.** Each generation introduces new ones. Gen 2's Unit Fund is a securities-law touchpoint in most jurisdictions. Gen 3's autonomous agent units are a frontier legal question. ØØT will continue to point at the landmines; it will not pretend to defuse them. Local counsel remains mandatory.