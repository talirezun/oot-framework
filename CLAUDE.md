# CLAUDE.md — Repository orientation for Claude Code

This file orients Claude Code (and any other agentic coding assistant) when working in the ØØT framework repository.

> **Status: v1.0.0 released 2026-05-09.** All 10 build phases complete. Tagged at `v1.0.0`. Repository at [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework).

---

## What this repository is

`oot-framework` — the canonical reference implementation of **ØØT (Organisation of Tomorrow)**. A markdown-first framework for partner-run, AI-augmented organisations.

**Initiator:** Dr. Tali Režun (Vice Dean Frontier Technologies, COTRUGLI Business School; founder of Lumina AI, 4thtech, PollinationX, Block Labs, Immu3, Online Guerrilla).
**Founding contributors:** Dražen Kapusta (Cotrugli Ledger); COTRUGLI Business School.
**Licence:** Apache 2.0 (code) + CC BY-SA 4.0 (docs/Skills).

---

## Current state — what shipped in v1.0.0

**165 files; ~70,000 words; 17 phase-numbered commits.**

Verified at release:
- ✅ All 12 SKILL.md files pass frontmatter validation (`scripts/validate_skills.py`).
- ✅ All 9 Excel templates open via openpyxl with critical formulas correct.
- ✅ Klarna gate workflow ships (`.github/workflows/klarna-gate.yml`).
- ✅ Auto-labeller ships (`.github/labeler.yml`).

### Phase-by-phase artefact map

| Phase | Commit | What's in tree |
|---|---|---|
| 0a | `phase-0a` | Filename casing + `excell→excel` typo + `_template_skills.md→_TEMPLATE_SKILL.md` + handoff deletion + my-curator SPEC formatting + `.gitignore` |
| 0b | `phase-0b` | 12 spec corrections (B1-B12: Klarna threshold, X2 col validation, X1 ai-pct, X1↔X2 cross-workbook, R1 rework rule, R3 Brain checkbox, R6 signed-commit retention, X8 burn source, X9 Q05, X5 perception threshold, R7 status-check) |
| 0c | `phase-0c` | Citation integrity pass — 7 adjusted, 2 unsourced removed |
| 2.5a | `phase-2.5a` | `templates/brain/FIRM-ONTOLOGY.md` + `templates/brain/SPEC.md` + `templates/partner-onboarding/PROVISIONING-SPEC.md` + `examples/SPEC.md` + expanded `docs/SPEC.md` (12→18 docs) |
| 2.5b | `phase-2.5b` | 6 Tier-1 SPECs expanded to implementation depth (S2, S3, S4, S5, S6, S12; S1 imported) |
| 2.5c | `phase-2.5c` | `MANIFEST.md → docs/internal/`, `research/` folder structure, installer-wizard plan, ECOSYSTEM.md spec, date-sweep tweaks |
| 1 | `phase-1` | AGENTS.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md (Contributor Covenant 2.1), LICENSE (Apache 2.0), LICENSE-DOCS (CC BY-SA 4.0), README navigation hub |
| 2 | `phase-2` | Validation pass (empty-tree commit) |
| 3 | `phase-3` | 7 Tier-1 SKILL.md files + 14 worked examples + 7 references READMEs |
| 4 | `phase-4` | 5 Tier-2 SKILL.md scaffolds (S7-S11) + 14 Brain page templates + onboarding (charter + script + checklist + 90-day plan) |
| 5 | `phase-5` | `scripts/build_excel.py` + 9 .xlsx files + `pyproject.toml` |
| 6 | `phase-6` | 16 Routine markdown files + `routines/README.md` |
| 7 | `phase-7` | 18 user guides (12 Tier-1 + 6 Tier-2 walkthroughs) + `docs/ECOSYSTEM.md` + 5 research stubs |
| 8 | `phase-8` | 6 GitHub Actions workflows + `scripts/validate_skills.py` + PR/issue templates |
| 9 | `phase-9` | `installer/wizard.py` + cloud/privacy fallback scripts + 3 reference org scaffolds |
| 10 | `phase-10` | `CHANGELOG.md` + `v1.0.0` tag |

---

## Repository structure (post-v1.0)

```
oot-framework/
├── README.md                         (navigation hub)
├── MANIFESTO.md                      (5 theses, ~26k words)
├── SPEC.md                           (8-layer architecture)
├── GLOSSARY.md
├── QUICKSTART.md
├── GENERATIONS.md                    (v1 / v2 / v3 roadmap)
├── CLAUDE.md                         (this file)
├── AGENTS.md                         (cross-vendor orientation)
├── BUILD-INSTRUCTIONS.md             (10-phase build script)
├── CHANGELOG.md                      (v1.0.0 release notes)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE                           (Apache 2.0)
├── LICENSE-DOCS                      (CC BY-SA 4.0)
├── pyproject.toml                    (Python project config)
├── .gitignore
├── .github/
│   ├── workflows/                    (6 CI workflows incl. klarna-gate.yml)
│   ├── labeler.yml                   (auto-applies ai-replaces-human)
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── governance/                       (4 docs: KLARNA-TEST, EU-AI-ACT, DECISION-RIGHTS, SECRETS-POLICY)
├── skills/
│   ├── _TEMPLATE_SKILL.md
│   ├── my-curator/                   (S1 — imported from talirezun/the-curator)
│   ├── context-engineering/          (S2)
│   ├── compensation-attribution/     (S3 — most distinctive, ~290 lines SKILL.md)
│   ├── code-qa/                      (S4)
│   ├── reporting-business-review/    (S5)
│   ├── change-management/            (S6)
│   ├── privacy-self-sovereign/       (S12)
│   ├── governance-compliance/        (S7 — Tier-2 scaffold)
│   ├── legal-operations/             (S8 — Tier-2 scaffold)
│   ├── marketing/                    (S9 — Tier-2 scaffold)
│   ├── finance-treasury/             (S10 — Tier-2 scaffold)
│   └── sales-bd/                     (S11 — Tier-2 scaffold)
│       └── per-pack: SPEC.md, SKILL.md, examples/, references/
├── templates/
│   ├── excel/                        (SPEC.md + 9 .xlsx files)
│   ├── brain/                        (FIRM-ONTOLOGY.md, SPEC.md, 14 page templates)
│   ├── partner-charter.md
│   ├── output-spec.md                (tutorial copy with inline guidance)
│   └── partner-onboarding/           (PROVISIONING-SPEC.md, checklist.md, provisioning-script.sh, first-90-days.md)
├── routines/
│   ├── SPEC.md
│   ├── README.md                     (16-file index + install order)
│   ├── cloud/                        (R1.md – R8.md)
│   └── privacy/                      (R1.md – R8.md)
├── docs/
│   ├── SPEC.md                       (doc generation spec)
│   ├── ECOSYSTEM.md                  (plain-language ecosystem index)
│   ├── 00-quickstart-cloud.md ... 08-faq.md  (12 Tier-1 user guides)
│   ├── glossary.md                   (alias of /GLOSSARY.md)
│   ├── walkthroughs/                 (W1.md – W6.md, screenshot-rich UI walkthroughs)
│   ├── images/                       (screenshot placeholders; binaries land in v1.x)
│   └── internal/MANIFEST.md          (build provenance)
├── research/
│   ├── README.md                     (research index)
│   ├── external-resources.md         (curated ecosystem index)
│   ├── articles/                     (2 stubs)
│   └── papers/                       (3 paper summaries)
├── scripts/
│   ├── build_excel.py                (Phase 5 generator)
│   └── validate_skills.py            (Phase 8 validator)
├── installer/
│   ├── README.md
│   ├── wizard.py                     (steps 1-4 functional; 5-12 in v1.x)
│   ├── cloud/install.sh              (fallback)
│   └── privacy/install.sh            (fallback)
└── examples/
    ├── README.md
    ├── SPEC.md                       (reference org spec)
    ├── small-org/                    (Solunar Studio, 3 partners — scaffold)
    ├── medium-org/                   (Brda Cooperative, 12 partners — scaffold)
    └── regulated-eu-org/             (AdriaLex AI, 6 partners — scaffold)
```

---

## Key design decisions baked into v1.0 (do not silently change)

These were debated, decided, and committed during the v1.0 build. Future agents should not relitigate without an explicit ADR.

1. **Klarna threshold ≥14/20 (70%)** is canonical across all artefacts. Legacy `≥7/10` framing is retired.
2. **X1 column J (`partner_multiplier`) is NOT a formula.** Routines (R1/R3) read X2 at runtime and write the resolved number. Cross-workbook openpyxl formulas are unreliable.
3. **AI-authored output is paid at full rate at month-1.** Correction discipline is the rework-within-30d zero-out, NOT an `ai_authored_pct` discount. Decision recorded in X1 README.
4. **R1 retroactive rework detection rule** (4 conditions: same partner + ≤30d gap + ≥50% file overlap + fix/revert/etc. regex) is in `routines/SPEC.md` R1 and reflected in S3 §4.3.
5. **R3 partner acknowledgement is a Brain checkbox**, not Slack reactions. Audit trail self-contained in Brain.
6. **R6 audit-trail immutability** is provided by branch protection + signed commits + append-only paths under `firm/audit-logs/`. Plain `git history` is NOT immutable. Generation 2 introduces external anchoring.
7. **Klarna Q8 has no "n/a" affordance.** "No public communication" must itself be a written, owned posture to score 2.
8. **X5 perception-gap threshold is 20 points** (≈ half the METR 39-point swing). Tightens to 15 with 90 days of internal baseline.
9. **X8 monthly_burn_average is from Cash_Position deltas** (realised outflow), NOT future Obligations.
10. **The `oot/klarna-test` GitHub status check name** is fixed. Branch protection on `main` must require it for the gate to enforce.

---

## How this repository was built

The repository was scaffolded by Claude Code (Opus 4.7) over a multi-week session driven by the framework's initiator. The intellectual core (theses, Skill Pack designs, governance disciplines, Klarna Test) is human contribution; the artefact production (file scaffolding, Excel template generation, doc writing) is AI co-authored. **This is the centaur model the framework prescribes, applied to the framework's own construction.**

Build order is in `BUILD-INSTRUCTIONS.md`. **The 10 phases are now complete.** Future modifications follow phase conventions (commit message: `<phase|fix|feat>-<n>: <what>`).

---

## What's deferred (per `GENERATIONS.md`)

### v1.x patch series (target: late 2026)

- **Tier-2 Skill Pack hardening** — replace `<!-- TODO -->` markers in S7, S8, S9, S10, S11. Each pack needs ~2,500-3,500 word SKILL.md + 3+ worked examples.
- **Installer wizard steps 5-12** — make programmatic. Currently steps 1-4 functional in `installer/wizard.py`; steps 5-12 reference the user docs.
- **Reference orgs full operational data** — `examples/<org>/firm/` currently scaffolds; v1.x populates 60-90 days of Brain pages + Excel data.
- **Tier-2 walkthroughs** — additional `docs/walkthroughs/` as patterns surface.
- **Screenshot binaries** — Phase 7 docs ship with `images/` placeholders; v1.x adds the actual screenshots.
- **Citation full paper summaries** — `research/papers/` ships 3 stubs; v1.x adds the rest of the cited works.

### Generation 2 (6-12 months)

Per `GENERATIONS.md`:
- Stablecoin payroll rails (Rise / Circle integration; per-partner jurisdiction verification).
- Smart-contract long-tail entitlements (replaces Excel quarterly settlement).
- Internal Unit Fund (after 6-9 months pilot data per YOLO model).
- Curator local-LLM ingest (removes the Gen-1 cloud-LLM dependency from the privacy track).
- Tier-2 Skill Pack hardening completion.
- Triple-entry-style audit logs in plain markdown (preparation for Gen 3).

### Generation 3 (12-24 months, research-stage)

- Cotrugli Ledger anchoring (PAC-RO receipts, Cotrugli Score, Vanguard Score, IAAF autonomy levels).
- Kelly-style autonomous business units (agent with own LLC, accounts, contracts).
- Per-agent compensation.

---

## Repository conventions (live)

**File naming.**
- **UPPERCASE** for top-level meta docs (`README.md`, `MANIFESTO.md`, `SPEC.md`, `GLOSSARY.md`, `QUICKSTART.md`, `GENERATIONS.md`, `CLAUDE.md`, `AGENTS.md`, `BUILD-INSTRUCTIONS.md`, `CHANGELOG.md`, `LICENSE`, `LICENSE-DOCS`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
- **UPPERCASE** for governance docs (`governance/KLARNA-TEST.md`, etc.).
- **UPPERCASE** for per-pack `SPEC.md` and `SKILL.md`.
- **UPPERCASE** for `_TEMPLATE_SKILL.md`, `FIRM-ONTOLOGY.md`, `PROVISIONING-SPEC.md`.
- **lowercase-hyphenated** for folder names, asset files, brain page slugs (`skills/compensation-attribution/`, `partner-output-ledger.xlsx`, `firm/output-logs/2026-05-08.md`).
- **lowercase-numbered** for Phase 7 user docs (`docs/00-quickstart-cloud.md`, `docs/walkthroughs/W1-claude-desktop-tour.md`).

**Markdown frontmatter.** YAML between `---` delimiters at the top. Required keys vary by file type (see `_TEMPLATE_SKILL.md` for skills; `templates/brain/SPEC.md` for Brain pages).

**Excel files are generated, not authored.** Source: `templates/excel/SPEC.md`. Generator: `scripts/build_excel.py` (uses openpyxl). Validator in CI: `.github/workflows/excel-validation.yml`.

**SKILL.md files validated** by `scripts/validate_skills.py`. CI: `.github/workflows/lint-skills.yml`.

**The Brain is not in this repo.** This repo is the framework. The firm's *instance* of the framework lives in a separate repo per `templates/brain/FIRM-ONTOLOGY.md`. Reference orgs in `examples/` show what a small Brain looks like.

---

## Coding conventions

- **Python ≥3.13** for installer scripts and any glue code. `uv` for dependency management. Type hints required. Black for formatting. Ruff for linting. `pyproject.toml` is committed.
- **Bash / Zsh** for shell scripts. POSIX-compatible. `set -euo pipefail` at the top.
- **JSON / YAML** for configuration files.
- **No new dependencies without justification.** ØØT is a markdown framework. Code is glue, not the substance.

---

## Tools the framework expects to use

- **The Curator + MyCuratorMCP** — Brain operations. Repo: [github.com/talirezun/the-curator](https://github.com/talirezun/the-curator).
- **GitHub MCP** — repo + CI operations.
- **Excel MCP** (`haris-musa/excel-mcp-server`) — privacy-track Excel automation.
- **Desktop Commander MCP** — privacy-track filesystem.
- **4thtech CLIs** — privacy-track comms.
- **PollinationX client** — privacy-track storage.
- **Trezor + Yubikey + Bitwarden** — secrets layer per `governance/SECRETS-POLICY.md`.

If the agent's harness has the Anthropic public skills available (`xlsx`, `docx`, `pdf`), prefer those for any new generated files. Always check the relevant SKILL.md before using.

---

## What to commit

After any substantive change:

1. Run `python3 scripts/validate_skills.py` if SKILL.md files were touched.
2. Run `python3 scripts/build_excel.py` if Excel SPEC was touched, then verify the regenerated `.xlsx` files.
3. Commit with `<phase|fix|feat>-<n>: <what>` convention. Examples:
   - `fix-skill-s7: harden EU AI Act §4.1 with worked example`
   - `feat-routine-r9: add monthly Brain semantic-duplicate scan`
   - `phase-11: tier-2 hardening pass for S7-S11` (if a future phase is named).
4. AI-authored commits use `Co-authored-by: Claude Opus 4.x <noreply@anthropic.com>` trailer per `skills/code-qa/SKILL.md` §4.6.
5. Push to GitHub. Branch protection on `main` requires signed commits.

---

## When the user asks about the framework

The user is **Dr. Tali Režun** (initiator) or a collaborator. Treat questions about the framework's intellectual basis (theses, citations, edge cases) as substantive — they often reflect ongoing refinement.

**The framework's discipline applies to the framework itself.** If a refinement contradicts the foundation kit, propose updating the foundation kit explicitly via PR + ADR rather than diverging silently. If a refinement would weaken the Klarna Test discipline, push back hard.

---

## Where to start in a fresh session

1. Read this file (CLAUDE.md) — the post-v1.0 orientation.
2. Read `CHANGELOG.md` — what shipped at v1.0.0.
3. Read `MANIFESTO.md` — the framework's intellectual core.
4. Read `BUILD-INSTRUCTIONS.md` — the build script (now historical; useful for understanding rationale of any phase).
5. Read `GENERATIONS.md` — what's deferred to v1.x / Gen 2 / Gen 3.

Then identify what the user wants to do:
- **Adopt the framework** for their firm → `docs/00-quickstart-cloud.md` or `docs/00-quickstart-privacy.md`.
- **Improve a Skill Pack** → read the pack's SPEC.md + SKILL.md, propose changes via PR.
- **Add a Tier-2 hardening** → S7-S11 are scaffolds; expand them per `_TEMPLATE_SKILL.md`.
- **Author a research article** → `research/articles/`.
- **Report a bug** → `docs/07-troubleshooting.md` first, then GitHub issue.
- **Adopt Generation 2** → wait for v2.0 (6-12 months); Gen 1 ships now.

---

## Active conversations / open threads (transient — update freely)

This section is intended for ephemeral state across sessions. As of release:

- v1.0.0 just shipped. No open threads.
- Tali plans to adopt the framework for his own firms (4thtech, PollinationX) as the first real-world test.
- Repository at [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework). 17 commits on `main`. Tag `v1.0.0`.
- Next priority (per Tali, May 2026): real-world adoption + community contribution acceptance.

> Future sessions: update this section with what's currently in flight. Stale items get pruned at v1.x release boundaries.

---

> **The framework's authors** ([`MANIFESTO.md`](MANIFESTO.md) closing): *"The pieces are real. The infrastructure is here. The legal landmines are mapped. The discipline is in the framework."*

> v1.0 is operational. The rest is execution.
