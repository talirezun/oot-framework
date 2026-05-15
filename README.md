# ØØT — Organisation of Tomorrow

[![Version](https://img.shields.io/github/v/tag/talirezun/oot-framework?label=version&color=blue&sort=semver)](https://github.com/talirezun/oot-framework/releases) [![License — Code](https://img.shields.io/badge/license%20(code)-Apache_2.0-green)](LICENSE) [![License — Docs](https://img.shields.io/badge/license%20(docs)-CC_BY--SA_4.0-green)](LICENSE-DOCS) [![Generation](https://img.shields.io/badge/generation-1-orange)](GENERATIONS.md)

> **TL;DR:** An open framework for partner-run, AI-augmented organisations. Three install paths below. **Most founders → use Path A.**

ØØT is a complete, opinionated, file-based framework for building and running an organisation in which the people producing value are paid for it as it lands, paid again as it compounds, and own a real stake in what they helped create — while the technical machinery underneath (AI agents, Skills, MCP, the Collecting Brain) compounds the firm's intellectual property in lockstep.

This is **Generation 1**. It is honest about what works today, what is bridged with manual processes, and what is deferred to Generation 2 (crypto rails, smart-contract long-tail, internal unit fund) and Generation 3 (Cotrugli Ledger anchoring — *the Gen-3 accounting/governance backbone, distinct from the operational Ledger you'll install in v1.0* — and autonomous agent business units).

---

## ⚡ Get started — install in 60-90 minutes

Three install paths, ordered by recommended-for-most-founders:

### 🤖 Path A — Coding-agent-assisted install *(recommended for ≥80% of founders)*

You have a coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, Continue, ChatGPT in code-execution mode). The agent reads the install plan and walks you through. **60-90 min wall-clock.** The agent does the file edits, JSON config, GPG signing-key generation, GitHub branch protection, MCP wiring, and verification. You answer questions when it asks.

→ **[Start here: `installer/agent-assisted/START-HERE.md`](installer/agent-assisted/START-HERE.md)** — single copy-paste prompt for your agent.

### 🛠️ Path B — Wizard (Python terminal) — **one-line install**

For founders who explicitly prefer a guided form over an agent. **~3-4 hours.** Same 15-step structure as Path A; interactive terminal prompts; resumable; dry-run available.

**Fresh laptop, nothing installed?** Open Terminal and paste this single line:

```bash
curl -fsSL https://raw.githubusercontent.com/talirezun/oot-framework/main/installer/bootstrap.sh | bash
```

The bootstrap checks prerequisites (git / python 3.11+ / curl / gpg), clones the framework to `~/.oot/oot-framework/`, sets up a Python venv, installs the wizard's UI dependencies, then hands off to the 15-step wizard. The wizard then guides you through every folder location, the Ledger repo (operational state), the GPG signing key, GitHub branch protection, **installing the Curator app via its own one-line installer** (the Second Brain — your semantic knowledge graph), wiring the my-curator MCP into Claude Desktop, and the Day-1 Routines. Safe to re-run — picks up where you left off.

→ [Wizard overview: `installer/README.md`](installer/README.md) (incl. `--resume` / `--dry-run` flags)

### 📄 Path C — Manual install (the docs)

For founders who want to type every step themselves. Most transparent; slowest. **~16 hours across two weekends.** Non-technical-founder-friendly: includes a plain-English primer (what's a terminal, what's a JSON file, what's a signed commit, what's an MCP).

→ [Cloud-track quickstart: `docs/00-quickstart-cloud.md`](docs/00-quickstart-cloud.md)
→ [Privacy-track quickstart: `docs/00-quickstart-privacy.md`](docs/00-quickstart-privacy.md)

---

### 🤔 Not sure which path? 30 seconds of decision-making

| Question | Path A | Path B | Path C |
|---|---|---|---|
| **Do you have a coding agent installed?** | yes | n/a | n/a |
| **Comfortable letting an agent run shell commands on your machine?** | yes | no | n/a |
| **Want to type every command yourself?** | no | partial | yes |
| **Have a free weekend (16h) for setup?** | n/a | n/a | yes |
| **Cloud or privacy track?** | both | both | both |

When in doubt: Path A. The framework was designed to be installed by an agent — that's how the framework's authors install it.

→ Before deciding: skim [`docs/MODULES.md`](docs/MODULES.md) (10 min) to see what you're actually installing.

---

## 🔄 After install — daily / weekly / monthly operations

Once the framework is installed, the same coding agent that did the install also handles day-to-day operations. Three short playbooks the agent reads:

- **[Daily ops](installer/agent-assisted/DAILY-OPS.md)** — every morning. ~2 min. Agent runs `git pull`, summarises what changed overnight, surfaces anomalies, verifies signing-key health.
- **[Weekly ops](installer/agent-assisted/WEEKLY-OPS.md)** — Fridays + Sundays. Agent reads R2's BR agenda, R5's brain-health snapshot.
- **[Monthly ops](installer/agent-assisted/MONTHLY-OPS.md)** — 1st-of-month variable-pay flow + partner-acknowledgement polling.

You paste a one-line prompt; the agent does the work. No terminal commands to memorise.

→ For the architecture: [`docs/AUTOMATION-PIPELINE.md`](docs/AUTOMATION-PIPELINE.md) — how the 8 Routines + your local clone + GitHub fit together.

---

## 📖 Read in this order *(while you install, or before)*

The framework's intellectual core is ~60 minutes of reading. You don't have to read it all *before* installing — you can read while the install runs. But you do need to read it eventually; the framework is more "discipline" than "tool" and the discipline doesn't fit in code comments.

| # | Read | Time | Why |
|---|---|---|---|
| 1 | [`MANIFESTO.md`](MANIFESTO.md) | ~15 min | The five theses with citations. The intellectual core. |
| 2 | [`SPEC.md`](SPEC.md) | ~30 min | The eight-layer technical architecture and the full Lego inventory. |
| 3 | [`GENERATIONS.md`](GENERATIONS.md) | ~10 min | What's in Gen 1, what's deferred, why. |
| 4 | [`governance/KLARNA-TEST.md`](governance/KLARNA-TEST.md) | ~10 min | The framework's signature epistemic discipline. Non-negotiable. |
| 5 | [`docs/MODULES.md`](docs/MODULES.md) | ~10 min | What to install, in what order, and what's optional. The dependency graph + a Day-N progression table. |
| 6 | [`docs/AUTOMATION-PIPELINE.md`](docs/AUTOMATION-PIPELINE.md) | ~15 min | How the 8 Routines fit together. Cloud + privacy pipeline diagrams, schedule timeline, dependency graph, **and the Second Brain bridge** — how cloud Routines reach the Curator-synced semantic graph via Curator's two-way GitHub sync. |
| 7 | [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md) | ~20 min | The external tools the framework rests on. With links to every wiki. |
| 8 | [`docs/walkthroughs/`](docs/walkthroughs/) | as needed | Tier-2 UI walkthroughs (Claude Desktop, Curator, Excel, BR, Klarna, Routines monitoring) — screenshot-rich, no shell required. |
| 9 | [`research/README.md`](research/README.md) | optional | Going deeper — paper summaries, original articles, and the curated ecosystem index. |

> 💡 **For the technically-minded:** also read [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md) — the agent-orientation files. They are vendor-neutral guides for any AI coding assistant working in this repo.

---

## 🗺️ Repository map

What lives where.

| Folder / file | Purpose |
|---|---|
| **[`installer/`](installer/)** | **Start here.** Three install paths: agent-assisted ([`agent-assisted/`](installer/agent-assisted/)), wizard ([`wizard.py`](installer/wizard.py)), fallback shell scripts ([`cloud/`](installer/cloud/), [`privacy/`](installer/privacy/)). |
| [`docs/00-quickstart-cloud.md`](docs/00-quickstart-cloud.md), [`docs/00-quickstart-privacy.md`](docs/00-quickstart-privacy.md) | Path C manual quickstarts. Non-technical-founder primer at the top. |
| [`docs/MODULES.md`](docs/MODULES.md), [`docs/AUTOMATION-PIPELINE.md`](docs/AUTOMATION-PIPELINE.md) | Module dependency map + automation pipeline diagrams. **Read these before installing.** |
| [`README.md`](README.md), [`MANIFESTO.md`](MANIFESTO.md), [`SPEC.md`](SPEC.md), [`GLOSSARY.md`](GLOSSARY.md), [`QUICKSTART.md`](QUICKSTART.md), [`GENERATIONS.md`](GENERATIONS.md) | Top-level intellectual + technical core. |
| [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md), [`BUILD-INSTRUCTIONS.md`](BUILD-INSTRUCTIONS.md) | Agent-orientation files. CLAUDE.md for Claude Code; AGENTS.md for any other agent; BUILD-INSTRUCTIONS.md for the phased scaffolding script. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`LICENSE`](LICENSE), [`LICENSE-DOCS`](LICENSE-DOCS) | Open-source standards. |
| [`governance/`](governance/) | Klarna Test, EU AI Act mapping, decision rights, secrets policy. |
| [`skills/`](skills/) | 12 hand-built Skill Packs — 7 hardened (S1–S6, S12) + 5 scaffolded (S7–S11). |
| [`templates/excel/`](templates/excel/) | 9 pre-built `.xlsx` templates with formulas + the spec they're generated from. |
| [`templates/brain/`](templates/brain/) | The Brain ontology + 14 Brain page templates that Routines and Skills write to. |
| [`templates/partner-onboarding/`](templates/partner-onboarding/) | Onboarding checklist + provisioning script + first-90-days plan. |
| [`routines/`](routines/) | 8 cloud Routines + 8 privacy-track equivalents. |
| [`docs/`](docs/) | 12 Tier-1 user guides + 6 Tier-2 UI walkthroughs ([`docs/walkthroughs/`](docs/walkthroughs/)). |
| [`research/`](research/) | Paper summaries, original articles, and the curated ecosystem index ([`external-resources.md`](research/external-resources.md)). |
| [`examples/`](examples/) | Three reference orgs: small (3-partner), medium (12-partner), regulated-EU (6-partner). |
| [`.github/workflows/`](.github/workflows/) | CI: SKILL.md frontmatter linter, link checker, Excel validator, Klarna gate. |

---

## 🔗 External ecosystem

ØØT runs on a stack of well-documented external tools. Each has its own wiki or docs site; the framework links to those rather than duplicating them. The full curated index is at [`research/external-resources.md`](research/external-resources.md).

**The reference Brain implementation:**

- **The Curator** — open-source Brain + MyCuratorMCP server. Skill Pack S1 imports the Curator's `SKILL.md` verbatim.
  - Repo + research articles: https://github.com/talirezun/the-curator
  - Research section: https://github.com/talirezun/the-curator/tree/main/research

**Cloud-track stack:**

- **Anthropic Claude** — Desktop, Code, [Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code), API. https://claude.com/ · docs: https://docs.claude.com/ · Routines dashboard: https://claude.ai/code/routines
- **Google Workspace** *(optional)* — Drive, Sheets, Docs, Calendar. https://workspace.google.com/ · Read-only convenience connector; state lives in GitHub, not Google.
- **Slack** — internal comms; Claude integration available. https://slack.com/
- **GitHub** — repo + CI + Brain canonical store. https://github.com/ · **GitHub Team plan ($4/u/mo) recommended** for branch-protection enforcement (see `docs/00-quickstart-cloud.md` §6).

**Privacy-track stack (full Gen 1 parity, sovereignty-first):**

- **4thtech** — on-chain dMail / dChat / file transfer. Wiki: https://wiki.4thtech.io/ · Repo: https://github.com/4thtech
- **PollinationX** — decentralised storage, NFT-based. Wiki: https://wiki.pollinationx.io/
- **LM Studio** — local LLM runner with native MCP. https://lmstudio.ai/ · MCP docs: https://lmstudio.ai/docs/local-server/mcp
- **Excel MCP** (`haris-musa/excel-mcp-server`) — privacy-track Excel automation (optional in Gen 1; Routines use openpyxl directly). https://github.com/haris-musa/excel-mcp-server
- **Desktop Commander MCP** — privacy-track filesystem. https://github.com/wonderwhy-er/DesktopCommanderMCP
- **GitHub MCP** — cross-machine Brain sync. https://github.com/modelcontextprotocol/servers/tree/main/src/github

**Secrets layer (both tracks, recommended-but-optional in Gen 1):**

- **Bitwarden** — open-source password manager. https://bitwarden.com/ · Recommended once 2+ admins.
- **Trezor** — hardware wallet (4thtech identity in privacy track; deferred to Gen 2 for cloud). https://trezor.io/
- **Yubikey** — hardware key for org-admin 2FA. https://yubico.com/ · Recommended once 2+ admins.

**Standards bodies:**

- **Linux Foundation Agentic AI Foundation (AAIF)** — governs MCP, AGENTS.md, MCP server cards. https://lfaidata.foundation/
- **Model Context Protocol (MCP)** — the open standard for agent ↔ tool. https://modelcontextprotocol.io/

For the comprehensive index (with licences, ØØT components that depend on each tool, and citation-grade references), see [`research/external-resources.md`](research/external-resources.md).

---

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

**8 scheduled Routines** — daily output capture, weekly Business Review prep, monthly variable pay calculation, quarterly long-tail settlement, weekly Brain health check, daily EU AI Act audit trail, on-event Klarna Test trigger, weekly treasury runway update. Cloud-track runs on Anthropic infrastructure ([Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code), laptop closed). Privacy-track runs on local cron / launchd / Task Scheduler hitting headless LM Studio.

**4 governance documents** — Klarna Test (the signature epistemic check), EU AI Act mapping methodology, decision rights matrix, secrets policy (Bitwarden + Trezor two-layer architecture).

**Two parallel tool tracks:**

- **Cloud track** (canonical, fastest path): Claude Desktop, Claude Code, GitHub (your Ledger holds markdown + `.xlsx` state; your Second Brain repo holds the Curator-synced semantic graph), Slack, the Curator + MyCuratorMCP, Claude Code Routines. Your spreadsheet app is your choice — Excel, LibreOffice, Numbers, Excel-for-Web.
- **Privacy track** (full Generation 1 parity): LM Studio with local Qwen / Llama / DeepSeek, Desktop Commander MCP for filesystem, optional Excel MCP, 4thtech for on-chain end-to-end-encrypted communication, PollinationX for decentralised storage, GitHub MCP for cross-machine sync, OS-native scheduling.

## Status: Generation 1

This is the v1.0 release. It is honest about what's deferred:

- **Generation 1 (today):** Everything described above. Full operational parity in cloud track. Full operational parity in privacy track with one trade-off (local cron vs. cloud Routines). FIAT compensation is the default; long-tail is Excel-tracked manually with quarterly settlement.

- **Generation 2 (6–12 months):** Stablecoin payroll rails (Rise / Circle), smart-contract long-tail entitlements, the internal Unit Fund (after 6–9 months of pilot data per the YOLO model's recommendation), Curator local-LLM ingest, hardening of the five Tier-2 Skill Packs, **ØØT desktop application** (graphical UI for daily ops; replaces the Gen-1 agent-as-daily-UI pattern).

- **Generation 3 (12–24 months, theoretical):** Cotrugli Ledger anchoring (PAC-RO receipts, Cotrugli Score, Vanguard Score, IAAF autonomy levels), Kelly-style autonomous business units (agents with their own LLC, accounts, contracts), per-agent compensation. This is research-stage. We mark it on the roadmap, design v1 so it doesn't conflict with v3, and stop there.

See `GENERATIONS.md` for the full roadmap.

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

https://github.com/talirezun/oot-framework

## A note on naming

ØØT is pronounced "out". The glyph is two crossed-out circles (legacy headcount, empty hours — the things being negated) struck through by T (Tomorrow / Threshold / the new vector). It is unique, search-friendly, and ownable. In ASCII contexts (URLs, shell commands, repository names) we use `oot`. The branded mark is ØØT.
