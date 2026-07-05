# CLAUDE.md — Repository orientation for Claude Code

This file orients Claude Code (and any other agentic coding assistant) when working in the ØØT framework repository.

> **Status: v1.3.0 released 2026-07-05** (tags on `main`: `v1.0.0` · `v1.0.1` · `v1.1.0` · `v1.2.0` · `v1.3.0`). Gen 1 operational and **live-validated end-to-end** (2026-07-05: community + privacy tracks, signed routine cycles, scheduled fire). The 2026-07-03 audit-driven improvement effort is complete; residual roadmap in "Active conversations" below and the gitignored `IMPROVEMENT-PLAN.md`. Repository at [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework).

---

## What this repository is

`oot-framework` — the canonical reference implementation of **ØØT (Organisation of Tomorrow)**. A markdown-first framework for partner-run, AI-augmented organisations.

**Initiator:** Dr. Tali Režun (Vice Dean Frontier Technologies, COTRUGLI Business School; founder of Lumina AI, 4thtech, PollinationX, Block Labs, Immu3, Online Guerrilla).
**Founding contributors:** Dražen Kapusta (Cotrugli Ledger); COTRUGLI Business School.
**Licence:** Apache 2.0 (code) + CC BY-SA 4.0 (docs/Skills).

---

## Current state — what shipped in v1.0.0

**At v1.0.0: 165 files; ~70,000 words; 17 phase-numbered commits.** (The repo has since grown — as of v1.2.0 it is ~188 tracked files / ~218,000 words of markdown. This section describes the v1.0.0 baseline; see `CHANGELOG.md` for v1.0.1/v1.1.0/v1.2.0.)

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
│   ├── excel/                        (SPEC.md + 9 .xlsx files; X1 now A–N, X2 partner_id-keyed, X4 A–M per ADR-004/005)
│   ├── brain/                        (FIRM-ONTOLOGY.md, SPEC.md, 15 page templates incl. brain-health-week.md)
│   ├── partner-charter.md
│   ├── output-spec.md                (tutorial copy with inline guidance; optional attribution_split field per ADR-005)
│   └── partner-onboarding/           (PROVISIONING-SPEC.md, checklist.md, provisioning-script.sh, first-90-days.md)
├── routines/
│   ├── SPEC.md
│   ├── README.md                     (16-file index + install order)
│   ├── cloud/                        (R1.md – R8.md)
│   └── privacy/                      (R1.md – R8.md; OpenCode-headless invocation per Phase 4)
├── docs/
│   ├── SPEC.md                       (doc generation spec)
│   ├── ECOSYSTEM.md                  (plain-language ecosystem index; #cost-summary canonical cost tables)
│   ├── MODULES.md                    (module dependency map; #community-track section)
│   ├── AUTOMATION-PIPELINE.md        (cloud + privacy pipeline diagrams)
│   ├── 00-quickstart-cloud.md ... 08-faq.md  (12 Tier-1 user guides; 02 split cloud/privacy)
│   ├── glossary.md                   (alias of /GLOSSARY.md)
│   ├── walkthroughs/                 (W1.md – W6.md, UI walkthroughs; screenshot binaries land in v1.x)
│   ├── images/                       (screenshot placeholders; binaries land in v1.x)
│   └── internal/                     (MANIFEST.md build provenance; ADR-001…ADR-005; agent-compatibility-log; install-test-report)
├── research/
│   ├── README.md                     (research index)
│   ├── external-resources.md         (curated ecosystem index)
│   ├── articles/                     (2 stubs)
│   └── papers/                       (3 paper summaries)
├── scripts/
│   ├── build_excel.py                (Excel generator — regenerates the 9 .xlsx from the SPEC)
│   └── validate_skills.py            (SKILL.md frontmatter + tier/status/uniqueness validator, hardened Phase 5B)
├── tests/                            (pytest suite — 51 tests: validator round-trip, build_excel structural, wizard state machine)
├── installer/
│   ├── README.md                     (18-step wizard index, 0–17)
│   ├── bootstrap.sh                  (one-line curl installer → clone + venv → hands off to wizard)
│   ├── wizard.py                     (18 steps, branded /17; steps 1–4 + 12 + klarna-gate functional; remainder reference the docs)
│   ├── agent-assisted/              (Path A: START-HERE, DAILY/WEEKLY/MONTHLY-OPS, cloud/privacy install plans, AGENT-CAPABILITY-SPEC, OPENCODE-SETUP.md [community track])
│   ├── cloud/install.sh              (thin pointer to Paths A/B/C)
│   └── privacy/install.sh            (thin pointer to Paths A/B/C)
└── examples/
    ├── README.md
    ├── SPEC.md                       (reference org spec)
    ├── small-org/                    (Solunar Studio, 3 partners — POPULATED: 25 firm/ pages, 2-week slice, Phase 5C)
    ├── medium-org/                   (Brda Cooperative, 12 partners — README-only; population lands in v1.x)
    └── regulated-eu-org/            (AdriaLex AI, 6 partners — README-only; population lands in v1.x)
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
11. **Excel `.xlsx` files live in the firm's Ledger GitHub repo and are mutated by Routines via openpyxl + signed commits — not via Google Sheets, not via the native Drive connector, not via a hosted Excel MCP.** Track-symmetric: cloud and privacy Routines do the same operation against the same repo. Recorded in [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](docs/internal/ADR-001-cloud-routine-excel-writeback.md). Spreadsheet viewers are user choice (Excel / LibreOffice / Numbers / Excel-for-Web). Don't reintroduce Sheets-as-state without an ADR superseding ADR-001.
12. **Cloud Routines product name is "Claude Code Routines"** (launched 14 April 2026), not "Anthropic Remote Routines" (the framework's older naming, retired in v1.0.1). Per-day limits: 5 (Pro) / 15 (Max, Team) / 25 (Enterprise). Plan-tier guidance: **Pro for solo or 2-partner firms with no R7 activity; Max for 3+ partner firms or any firm with active R7 / Klarna gate**.
13. **Bitwarden / Trezor / Yubikey are recommended-but-optional in Gen 1.** Trezor stores crypto keys not used until Gen 2 (stablecoin payroll). Bitwarden + Yubikey are best-practice for any firm but not gating for a beginning founder. The install paths must allow a founder to start without these and add them as the firm matures. Decision recorded 2026-05-10.
14. **The Firm Brain is a Curator Shared Brain instance, in a separate GitHub repo from the Ledger. The framework provisions exactly two firm repos per firm: `<firm>-ledger` and `<firm>-brain`.** Three distinct primitives: **Ledger** (`<firm>-ledger`, Excel + audit logs, written by Routines per ADR-001), **Firm Brain** (`<firm>-brain`, Curator Shared Brain v3.0.0-beta+, written by partners Push-ing from their personal Curators, synthesized weekly by the admin), **Second Brain** (each partner's *personal* Curator wiki on their own machine; one of its domains is opted-in to contribute to the Firm Brain). The pre-v1.0.1 `<firm>-secondbrain` repo is **retired as a framework concept** — cloud Routines that need firm context read `collective/<firm-domain>/wiki/` in the Firm Brain repo; personal Curator backup-to-GitHub is a personal-tooling choice, not framework-orchestrated. Existing v1.0 `<firm>-secondbrain` repos may stay as personal backup, be archived, or be deleted at firm discretion. Recorded in [`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](docs/internal/ADR-002-firm-brain-curator-shared-brain.md). Don't conflate these three terms; don't collapse the Firm Brain and the Ledger into one repo without an ADR superseding ADR-002.
15. **IP mode default for ØØT firms = `organisational`** (partners assign IP to the operating LLC per their partner charter); **`contributor_retains` for advisors / contractors / outside collaborators**. Both Curator attribution flags (`allow_name_attribution` org-side, `attribute_by_name` contributor-side) default to **`false`** — UUID-pseudonymous attribution is the safe baseline; real names surface only when both sides explicitly opt in. The `data_handling_terms` field locks at admin setup and cannot be changed after invites go out. The partner charter ([`templates/partner-charter.md`](templates/partner-charter.md)) must carry an explicit IP-assignment clause for `organisational` mode to be defensible — Tier-2 follow-up to verify.
16. **GitHub plan-tier guidance now applies to *two* protected repos per firm** (Ledger + Firm Brain). GitHub Free private repos do not enforce branch protection on either (Finding #16, amplified). **3+ partner firms: GitHub Team minimum.** **EU firms requiring GDPR data residency: GitHub Enterprise Cloud with EU residency option** on the Firm Brain repo (and ideally the Ledger too). Curator v3.1's Cloudflare R2 backend (with per-bucket `jurisdiction = "eu"`) will relieve this in the future; firms launching today on EU residency must use Enterprise Cloud.
17. **A third operating configuration exists: the community track** (free-to-start, no Anthropic subscription, no dedicated hardware, no sovereignty claims). Harness + daily-ops agent is **OpenCode** (free built-in / own-key / local models); Ledger + Firm Brain are GitHub unchanged (ADR-001/002 verbatim); Brain ingest is Curator + Gemini Flash Lite pay-as-you-go; scheduled Routines run on a **three-rung automation ladder** — manual playbook runs → laptop cron running `opencode run` on the substrate-neutral prompt bodies → GitHub Actions scheduled workflows (laptop-closed). Routines/Skill Packs/Excel/governance are **byte-identical across all three tracks**; only harness and scheduler differ (any divergence is a bug). Budget-motivated founders use this; sovereignty-motivated founders use the privacy track. Recorded in [`docs/internal/ADR-003-community-track-no-subscription.md`](docs/internal/ADR-003-community-track-no-subscription.md). Harness setup: [`installer/agent-assisted/OPENCODE-SETUP.md`](installer/agent-assisted/OPENCODE-SETUP.md).
18. **X4 Decision_Log gains column M — `status`** (ADR-004). Literal enum, never a formula: `scoring | remediation | monitoring | proceeded | held`. It answers a *different* question than column I (`decision`): I is the **threshold verdict** (what the score says: PROCEED at ≥14, else HOLD); M is the **lifecycle state** (where the process is). They may disagree transiently (I=PROCEED while M=monitoring during the 90-day window). The `oot/klarna-test` gate is unaffected — it reads Klarna_Score directly, never `status`. **The appended-row contract is now a required per-workbook SPEC section:** every workbook whose rows a Routine appends carries an "Appended-row contract" block in `templates/excel/SPEC.md` listing per column — literal / formula-the-routine-MUST-write / human-only. This generalises the Finding-6 fix (R1 previously left K/L formulas blank → silent zero-pay); R7 replicated the same bug on X4 and is now bound by the contract. Recorded in [`docs/internal/ADR-004-klarna-status-column.md`](docs/internal/ADR-004-klarna-status-column.md).
19. **`partner_id` (`P-NNN`) is the universal Excel join key; X1 gains column N `weight`** (ADR-005). `Base_Variable_Split` and `Long_Tail_Schedule` each gain a **leading `partner_id` column** (all other columns shift right by one — weights are now D:F, `output_multiplier` is G, bonus splits H:J; Long_Tail's `partner_share_pct` is D, `total_settled_to_date` is H). Both stay **single shared sheets** (one row per partner / per partner-artifact) — per-partner *sheets* are explicitly rejected. R1/R3/R4 join on `partner_id`. X1 Output_Log gains column **N `weight`** (number in (0,1], default 1.0); the L formula becomes `=K*J*N*IF(rework)` so co-authored outputs **share** the envelope (one row per co-author with `weight=1/N` or the output spec's optional `attribution_split`) instead of double-paying. Recorded in [`docs/internal/ADR-005-partner-join-key-and-output-weight.md`](docs/internal/ADR-005-partner-join-key-and-output-weight.md).

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

- **Python ≥3.11 minimum, 3.13 recommended** for installer scripts and any glue code. `pyproject.toml` declares `requires-python = ">=3.11"`; the framework's tooling (`ruff`, `black`, `mypy`) targets 3.13 for new code. `uv` for dependency management when available. Type hints required. Black for formatting. Ruff for linting. The install plan tries `python3.13` / `python3.12` / `python3.11` / `python3` in order and uses whichever first satisfies the floor.
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

1. Run `python3 scripts/validate_skills.py` if SKILL.md files were touched (must be 12/12).
2. Run `python3 scripts/build_excel.py` if the Excel SPEC was touched, then verify the regenerated `.xlsx` files (the `excel-validation.yml` CI job does a cell-level drift check).
3. Run the pytest suite: `python3 -m pytest tests/ -q` (51 tests — validator round-trip, build_excel structural asserts incl. the ADR-004/005 schema checks, wizard state machine). CI runs this as a **hard gate** in `python-tests.yml`; `ruff`/`black` cover `scripts/` + `installer/` but stay `continue-on-error` until a formatting pass clears pre-existing F401/F541.
4. Run `python3 -m py_compile installer/wizard.py scripts/*.py` and `bash -n installer/*/install.sh installer/bootstrap.sh` for glue-code / shell changes.
5. Check links: `lychee --offline --no-progress .` (0 errors) if docs were touched.
6. Commit with `<phase|fix|feat>-<n>: <what>` convention. Examples:
   - `fix-skill-s7: harden EU AI Act §4.1 with worked example`
   - `feat-routine-r9: add monthly Brain semantic-duplicate scan`
   - `phase-11: tier-2 hardening pass for S7-S11` (if a future phase is named).
7. AI-authored commits use the `Co-Authored-By:` trailer per `skills/code-qa/SKILL.md` §4.6.
8. Push to GitHub. (Note: this framework repo's own commits are *not* GPG-signed — the "requires signed commits" discipline applies to the *firm's* Ledger + Firm Brain repos, not to `oot-framework` itself.)

---

## When the user asks about the framework

The user is **Dr. Tali Režun** (initiator) or a collaborator. Treat questions about the framework's intellectual basis (theses, citations, edge cases) as substantive — they often reflect ongoing refinement.

**The framework's discipline applies to the framework itself.** If a refinement contradicts the foundation kit, propose updating the foundation kit explicitly via PR + ADR rather than diverging silently. If a refinement would weaken the Klarna Test discipline, push back hard.

---

## Where to start in a fresh session

1. Read this file (CLAUDE.md) — the post-v1.0 orientation.
2. Read `CHANGELOG.md` — what shipped in each release (latest: v1.2.0).
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

This section is intended for ephemeral state across sessions.

**As of 2026-07-04 (post-v1.2.0 — audit-driven improvement effort: Phases 0–5 complete):**

**Release state reconciled 2026-07-03.** The Shared Brain branch was merged to `main` (fast-forward); tags `v1.1.0` + `v1.2.0` now live on main. `v1.0.1` was tagged retroactively at the bridge-complete commit (`c59595e`). CHANGELOG restructured into v1.0.1 / v1.1.0 / v1.2.0 sections + an `## Unreleased` section holding the improvement-effort work. Stale worktree branches deleted.

**Full-repo audit completed 2026-07-03** (five parallel deep reviews). The phased improvement effort is now **done through Phase 5 and pushed to `main`**. **The working plan lives in `IMPROVEMENT-PLAN.md` at the repo root — LOCAL ONLY, gitignored, the cross-session memory for this effort. Read it first in any session continuing this work.** Phases and their commits:

- **Phase 0 — release-state untangle** — DONE, `ffcdb8d`.
- **Phase 1 — trust-critical bug fixes** — DONE, `cdf0fd8` (installer state machine; klarna-gate reworked to always-post / read base branch / framework-repo guard; R1 output_ref dedupe; real CI test suite; money-path routine fixes).
- **Phase 2 — doc-truth sweep** — DONE, `001e2af` (Second Brain bridge into Path C; contradiction kill-list; ECOSYSTEM canonical cost tables; wizard grew to 18 steps; 88 visible Tier-2 TODOs).
- **Phase 3 — community track (ADR-003)** — DONE, `1a1778e` (OpenCode as first-class harness; `OPENCODE-SETUP.md`; community track threaded through all entry docs).
- **Phase 4 — privacy-track grounding** — DONE, `f01f460` (privacy Routines invoke **OpenCode headless** — `opencode run --model lmstudio/<model>` — against the llmster-hosted LM Studio server; the fabricated `--skill`/`--prompt-file`/`--backfill` flag interface is gone; `lms` for model management; scoped-unattended `opencode.json`; install.sh files shrunk to thin pointers).
- **Phase 5 — structural hardening + docs-sync sweep** — DONE, this commit (ADR-004 X4 `status` column + appended-row contract; ADR-005 `partner_id` join key + X1 `weight` column; validator hardened with 6 new checks; Klarna per-question 0/1/2 anchors; small-org populated; 51-test suite with hard-gating lint; full documentation sync).

**Remaining open items (deliberate, tracked in IMPROVEMENT-PLAN.md):**

- **The live-test session** (needs the maintainer at the keyboard, on the test instance): the privacy-track end-to-end run (LM Studio + OpenCode + the test company) **and** the OpenCode community-track e2e install. Everything above is author-verified but not yet run against real accounts. Bundled as one queued session.
- **v1.3 roadmap:** full retirement of the legacy `<firm>-secondbrain` bridge to the Firm Brain read-path (migration banners are in place in `routines/cloud/R5.md`, `installer/wizard.py` step_12, `docs/AUTOMATION-PIPELINE.md`, cloud-install-plan Step 9b); the Rung-3 routine-runner GitHub Actions workflow template (`templates/ci/routine-runner.yml` candidate per ADR-003); the 25 walkthrough screenshots + installer web-UI choke-point captures; medium-org + regulated-eu-org population (small-org shipped Phase 5C); Tier-2 Skill Pack hardening (S7 first — owns the R6/Article-12 chain); the remaining ADR-001 amendment items (binary-xlsx conflict recovery, timezone pinning, R3 polling-window semantics, R6 hourly-retry unschedulability).

Test instance preserved for e2e work:
- GitHub: `talirezun/oot-test-company` (private)
- Local: `/Users/talirezun/00T-test-company/`
- GPG key: `oot-test-bot <blocklabstech@gmail.com>` (FF2AE322B7F4C193)
- Curator domain: `00t-test-company` in `/Users/talirezun/second-brain/`

**Real-world adoption.** Tali plans to adopt the framework for his own firms (4thtech, PollinationX) as the first real-world test. Repository at [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework).

> Future sessions: update this section with what's currently in flight. Stale items get pruned at v1.x release boundaries.

---

> **The framework's authors** ([`MANIFESTO.md`](MANIFESTO.md) closing): *"The pieces are real. The infrastructure is here. The legal landmines are mapped. The discipline is in the framework."*

> v1.0 is operational. The rest is execution.
