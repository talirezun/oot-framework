# ØØT Quickstart — pick your install path

This is a 30-second routing page. The framework has three install paths; pick one and follow the linked doc. Each path produces the same outcome: a working Generation-1 ØØT instance, signed-commits to GitHub Brain repo, Routines configured.

---

## 🤖 Path A — Coding-agent-assisted *(recommended for ≥80% of founders)*

You have a coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, Continue.dev, ChatGPT in code-execution mode, or any agent meeting the [capability spec](installer/agent-assisted/AGENT-CAPABILITY-SPEC.md)). The agent reads the install plan and executes it; you answer questions. **60-90 min wall-clock.**

→ **[`installer/agent-assisted/START-HERE.md`](installer/agent-assisted/START-HERE.md)** — single copy-paste prompt for your agent.

After install, the same agent handles daily / weekly / monthly operations via three short playbooks:
- [`installer/agent-assisted/DAILY-OPS.md`](installer/agent-assisted/DAILY-OPS.md) — every morning
- [`installer/agent-assisted/WEEKLY-OPS.md`](installer/agent-assisted/WEEKLY-OPS.md) — Fridays + Sundays
- [`installer/agent-assisted/MONTHLY-OPS.md`](installer/agent-assisted/MONTHLY-OPS.md) — 1st of month

## 🛠️ Path B — Wizard (Python terminal)

For founders who prefer a guided interactive form over an agent. **~3-4 hours.**

```bash
python3 installer/wizard.py            # full interactive install
python3 installer/wizard.py --resume   # resume from last step
python3 installer/wizard.py --dry-run  # preview without doing
```

→ Wizard overview: [`installer/README.md` §2](installer/README.md)

## 📄 Path C — Manual install (the docs)

For founders who want to type every step themselves. **~16 hours across two weekends.** Includes a plain-English non-technical-founder primer (what's a terminal, JSON file, signed commit, MCP).

→ Cloud track: [`docs/00-quickstart-cloud.md`](docs/00-quickstart-cloud.md)
→ Privacy track: [`docs/00-quickstart-privacy.md`](docs/00-quickstart-privacy.md)

---

## Before any path — read these (~60 min)

The framework is more "discipline" than "tool"; the discipline doesn't fit in code comments. You can read while the install runs.

1. [`MANIFESTO.md`](MANIFESTO.md) — five theses with citations (~15 min)
2. [`SPEC.md`](SPEC.md) — eight-layer architecture (~30 min)
3. [`GENERATIONS.md`](GENERATIONS.md) — what's in Gen 1 vs deferred (~10 min)
4. [`governance/KLARNA-TEST.md`](governance/KLARNA-TEST.md) — the signature epistemic discipline (~10 min)
5. [`docs/MODULES.md`](docs/MODULES.md) — what to install and what's optional (~10 min)
6. [`docs/AUTOMATION-PIPELINE.md`](docs/AUTOMATION-PIPELINE.md) — how Routines + GitHub + your local fit together (~15 min)

---

## Decisions you'll need to make during install

The agent / wizard / manual docs will surface these. Knowing them ahead of time saves time:

- **Cloud track or privacy track?** Cloud is faster, easier, uses Claude Code Routines (laptop closed). Privacy is sovereign, requires an always-on machine, uses 4thtech + PollinationX + LM Studio + local cron. **Most founders should start cloud** unless they have a clear sovereignty mandate.
- **Are you in the EU?** If yes, the EU AI Act (full obligations from 2 August 2026) and GDPR materially affect your build. Governance & Compliance Skill Pack and [`governance/EU-AI-ACT.md`](governance/EU-AI-ACT.md) are mandatory reading, not optional.
- **What jurisdiction will the entity operate in?** Worker classification, variable-pay legality, securities law, and crypto-payroll regulation all vary. [`docs/06-when-to-call-a-lawyer.md`](docs/06-when-to-call-a-lawyer.md) lists the eleven touchpoints requiring local counsel.
- **Firm operational repo location?** Default `~/<firm-slug>`. You'll pick during install.
- **Existing Curator second-brain or fresh install?** Configuration A (separate vaults) vs Configuration B (firm repo IS the Curator vault).
- **GitHub plan tier?** Free + private *(branch protection advisory only — see [Finding 16](docs/internal/install-test-report-2026-05-10.md))*, Team ($4/user/month — enforced branch protection — recommended for any firm taking R6 seriously), or Public (free, but operational data is public).
- **Anthropic plan tier?** Pro (5 Routine runs/day) for solo / 2-partner with no R7; Max (15/day) recommended default for 3+ partners or active Klarna gate.

The install plans ask these as numbered questions. Have your answers ready and the install runs faster.

---

## Run the readiness diagnostic first

Open [`templates/excel/oot-readiness.xlsx`](templates/excel/oot-readiness.xlsx) in your spreadsheet app (Excel / LibreOffice / Numbers — all work; framework is `.xlsx` native). It's a 20-question diagnostic across People, Tech, Culture, Risk. Score yourself honestly. **A score below 60% suggests Gen 1 adoption is premature**; address gaps first.

---

## After install — daily / weekly / monthly operations

→ [`docs/AUTOMATION-PIPELINE.md`](docs/AUTOMATION-PIPELINE.md) — how the 8 Routines fit together. Cloud + privacy pipeline diagrams, schedule timeline, dependency graph, the my-curator-MCP-reachability gap.

→ For Path A users: the three daily-ops playbooks above keep your local clone synced and surface operational state.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel. See [`docs/06-when-to-call-a-lawyer.md`](docs/06-when-to-call-a-lawyer.md) for the eleven legal touchpoints.
