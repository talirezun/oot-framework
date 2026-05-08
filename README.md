# ØØT — Organisation of Tomorrow

**An open framework for partner-run, AI-augmented organisations.**

ØØT is a complete, opinionated, file-based framework for building and running an organisation in which the people producing value are paid for it as it lands, paid again as it compounds, and own a real stake in what they helped create — while the technical machinery underneath (AI agents, Skills, MCP, the Collecting Brain) compounds the firm's intellectual property in lockstep.

It is not a methodology, a consultancy product, or a manifesto-only document. It is a working stack — markdown specifications, hand-built Skill Packs, pre-formulated Excel templates, scheduled cloud Routines, governance documents, and reference architectures — that a founder can adopt in a weekend and run a real organisation on by the end of the first quarter.

This is **Generation 1**. It is honest about what works today, what is bridged with manual processes, and what is deferred to Generation 2 (crypto rails, smart-contract long-tail, internal unit fund) and Generation 3 (Cotrugli Ledger anchoring, autonomous agent business units).

## Who this is for

Primarily: **founders building a new organisation from zero**, with three to twenty partners (no employees, no headcount, no fixed salaries beyond a small dignified base), who want to operate the firm as a partner-run, AI-augmented entity from day one rather than retrofit it later.

Secondarily: **leaders of existing organisations** considering a transformation. The framework is honest about how hard that transformation is — the resistance literature is unambiguous — and provides a graduated adoption path. But the cleanest path is forward, not retrofit.

This framework is **not legal advice, not financial advice, and not a turnkey solution**. It is a structured set of decisions and tools that a competent founder, working with local counsel and a tax advisor, can adapt to their jurisdiction. The framework points at the legal landmines (eleven of them, mapped explicitly in `docs/06-when-to-call-a-lawyer.md`); it does not defuse them.

## The five-minute tour

ØØT rests on five theses, drawn from peer-reviewed research, industry reports, and seven years of practitioner experience. They are presented in the order of evidentiary weight, not narrative drama:

1. **Resistance is the central problem.** The MIT NANDA "GenAI Divide" research shows 95% of enterprise GenAI pilots produce no measurable P&L impact. The METR study showed senior engineers using AI were 19% slower while feeling 20% faster. Klarna cut customer-service roles publicly, then quietly rehired. The technology is ready. The organisations are not. ØØT leads with the change-management problem because that is where every comparable framework fails.

2. **Human work in the AI era is centaur work.** Karpathy's Software 3.0 framing — humans contribute spec, test, taste, and judgement; AI contributes implementation at speed — is now backed by 30+ years of literature and decisive 2025 evidence (HBS Cybernetic Teammate, DORA 2025, MIT NANDA). Skill Packs encode the centaur pattern for each domain.

3. **Employees become Partners.** The salary system is a 20th-century artefact built on assumptions (hours = output, attribution is hard, payment latency is unavoidable, ownership is a binary acquired event) that no longer hold. The intellectual lineage runs Weitzman → Levin & Tadelis → ROWE → Beyond Budgeting → DAO contributor models → stablecoin payroll. The pieces exist. ØØT puts them on paper and into running code.

4. **The firm's IP is its Collecting Brain.** Every conversation, decision, contract, deal, code review, and customer interaction is a candidate node in a queryable knowledge graph. The Curator (the canonical reference implementation, integrated as Skill Pack S1) makes this operational today, with cloud-LLM ingest, MCP-native query, and an Obsidian-compatible file format that survives any single vendor's roadmap.

5. **The framework is composable Lego.** SKILL.md, AGENTS.md, MCP server cards, and the Linux Foundation Agentic AI Foundation primitives are the open-standard substrate. ØØT's Skill Packs are not vendor-locked plugins; they are markdown files that any MCP-compatible client (Claude Desktop, Cursor, LM Studio, ChatGPT) can load.

## What's in the box

The full framework, as scaffolded in this repository:

**12 Skill Packs** — 7 hardened in v1.0 (My Curator, Context Engineering, Compensation & Attribution, Code & QA, Reporting & Business Review, Change Management, Privacy / Self-Sovereign Stack), 5 scaffolded for v1.x (Governance & Compliance, Legal Operations, Marketing, Finance & Treasury, Sales & BD).

**9 pre-built Excel templates** — partner output ledger, reward-species declaration, business review, Klarna Test, METR baseline, agent-skill ROI, EU AI Act mapping register, treasury runway (optional), ØØT-readiness assessment. All formula-driven. All written to and read from by scheduled Routines so the spreadsheet is a review surface, not a data-entry surface.

**8 scheduled Routines** — daily output capture, weekly Business Review prep, monthly variable pay calculation, quarterly long-tail settlement, weekly Brain health check, daily EU AI Act audit trail, on-event Klarna Test trigger, weekly treasury runway update. Cloud-track runs on Anthropic infrastructure (Remote Routines, laptop closed). Privacy-track runs on local cron / launchd / Task Scheduler hitting headless LM Studio.

**4 governance documents** — Klarna Test (the signature epistemic check), EU AI Act mapping methodology, decision rights matrix, secrets policy (Bitwarden + Trezor two-layer architecture).

**Two parallel tool tracks:**

- **Cloud track** (canonical, fastest path): Claude Desktop, Claude Code, Google Drive/Sheets, Slack, GitHub, the Curator + MyCuratorMCP, Claude Remote Routines.
- **Privacy track** (full Generation 1 parity): LM Studio with local Qwen / Llama / DeepSeek, Desktop Commander MCP for filesystem, Excel MCP for spreadsheet automation, 4thtech for on-chain end-to-end-encrypted communication, PollinationX for decentralised storage, GitHub MCP for cross-machine sync, OS-native scheduling.

## Status: Generation 1

This is the v1.0 release. It is honest about what's deferred:

- **Generation 1 (today):** Everything described above. Full operational parity in cloud track. Full operational parity in privacy track with one trade-off (local cron vs. cloud Routines). FIAT compensation is the default; long-tail is Excel-tracked manually with quarterly settlement.

- **Generation 2 (6–12 months):** Stablecoin payroll rails (Rise / Circle), smart-contract long-tail entitlements, the internal Unit Fund (after 6–9 months of pilot data per the YOLO model's recommendation), Curator local-LLM ingest, hardening of the five Tier-2 Skill Packs.

- **Generation 3 (12–24 months, theoretical):** Cotrugli Ledger anchoring (PAC-RO receipts, Cotrugli Score, Vanguard Score, IAAF autonomy levels), Kelly-style autonomous business units (agents with their own LLC, accounts, contracts), per-agent compensation. This is research-stage. We mark it on the roadmap, design v1 so it doesn't conflict with v3, and stop there.

See `GENERATIONS.md` for the full roadmap.

## Quick start

Read in this order:

1. **`MANIFESTO.md`** — the five theses in full, with citations. ~15 minutes.
2. **`SPEC.md`** — the technical specification: layers, Skill Packs, Excel Legos, Routines, governance. ~30 minutes.
3. **`QUICKSTART.md`** — weekend setup path, cloud or privacy track. Implementation starts here.
4. **`GENERATIONS.md`** — what's in v1, what's deferred, why.
5. **`governance/KLARNA-TEST.md`** — the signature epistemic check that must run before any "AI replaces human" decision.

## Initiator and contributors

**Initiator:** Dr. Tali Režun — Vice Dean of Frontier Technologies at COTRUGLI Business School; founder of Lumina AI, Moj AI, Block Labs, 4thTech, Immu3, PollinationX, Online Guerrilla.

**Founding contributors:**
- **Dražen Kapusta** — co-author of the Cotrugli Ledger (the Generation 3 governance backbone) and originator of the institutional thesis ØØT extends.
- **COTRUGLI Business School** — institutional anchor and EU positioning; ØØT is integrated into the MBA Frontier Technologies curriculum.

Additional collaborators will be added to this repository as named contributors as they join the project.

## Licence

- **Code, scripts, installers, Routine prompts, attribution agents:** Apache 2.0.
- **Documentation, Skill Packs (`SKILL.md` files), templates, governance documents:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

See `LICENSE` and `LICENSE-DOCS` for the full texts.

## Repository

`https://github.com/talirezun/oot-framework`

## A note on naming

ØØT is pronounced "out". The glyph is two crossed-out circles (legacy headcount, empty hours — the things being negated) struck through by T (Tomorrow / Threshold / the new vector). It is unique, search-friendly, and ownable. In ASCII contexts (URLs, shell commands, repository names) we use `oot`. The branded mark is ØØT.