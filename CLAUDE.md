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
11. **Excel `.xlsx` files live in the firm's Ledger GitHub repo and are mutated by Routines via openpyxl + signed commits — not via Google Sheets, not via the native Drive connector, not via a hosted Excel MCP.** Track-symmetric: cloud and privacy Routines do the same operation against the same repo. Recorded in [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](docs/internal/ADR-001-cloud-routine-excel-writeback.md). Spreadsheet viewers are user choice (Excel / LibreOffice / Numbers / Excel-for-Web). Don't reintroduce Sheets-as-state without an ADR superseding ADR-001.
12. **Cloud Routines product name is "Claude Code Routines"** (launched 14 April 2026), not "Anthropic Remote Routines" (the framework's older naming, retired in v1.0.1). Per-day limits: 5 (Pro) / 15 (Max, Team) / 25 (Enterprise). Plan-tier guidance: **Pro for solo or 2-partner firms with no R7 activity; Max for 3+ partner firms or any firm with active R7 / Klarna gate**.
13. **Bitwarden / Trezor / Yubikey are recommended-but-optional in Gen 1.** Trezor stores crypto keys not used until Gen 2 (stablecoin payroll). Bitwarden + Yubikey are best-practice for any firm but not gating for a beginning founder. The install paths must allow a founder to start without these and add them as the firm matures. Decision recorded 2026-05-10.
14. **The Firm Brain is a Curator Shared Brain instance, in a separate GitHub repo from the Ledger. The framework provisions exactly two firm repos per firm: `<firm>-ledger` and `<firm>-brain`.** Three distinct primitives: **Ledger** (`<firm>-ledger`, Excel + audit logs, written by Routines per ADR-001), **Firm Brain** (`<firm>-brain`, Curator Shared Brain v3.0.0-beta+, written by partners Push-ing from their personal Curators, synthesized weekly by the admin), **Second Brain** (each partner's *personal* Curator wiki on their own machine; one of its domains is opted-in to contribute to the Firm Brain). The pre-v1.0.1 `<firm>-secondbrain` repo is **retired as a framework concept** — cloud Routines that need firm context read `collective/<firm-domain>/wiki/` in the Firm Brain repo; personal Curator backup-to-GitHub is a personal-tooling choice, not framework-orchestrated. Existing v1.0 `<firm>-secondbrain` repos may stay as personal backup, be archived, or be deleted at firm discretion. Recorded in [`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](docs/internal/ADR-002-firm-brain-curator-shared-brain.md). Don't conflate these three terms; don't collapse the Firm Brain and the Ledger into one repo without an ADR superseding ADR-002.
15. **IP mode default for ØØT firms = `organisational`** (partners assign IP to the operating LLC per their partner charter); **`contributor_retains` for advisors / contractors / outside collaborators**. Both Curator attribution flags (`allow_name_attribution` org-side, `attribute_by_name` contributor-side) default to **`false`** — UUID-pseudonymous attribution is the safe baseline; real names surface only when both sides explicitly opt in. The `data_handling_terms` field locks at admin setup and cannot be changed after invites go out. The partner charter ([`templates/partner-charter.md`](templates/partner-charter.md)) must carry an explicit IP-assignment clause for `organisational` mode to be defensible — Tier-2 follow-up to verify.
16. **GitHub plan-tier guidance now applies to *two* protected repos per firm** (Ledger + Firm Brain). GitHub Free private repos do not enforce branch protection on either (Finding #16, amplified). **3+ partner firms: GitHub Team minimum.** **EU firms requiring GDPR data residency: GitHub Enterprise Cloud with EU residency option** on the Firm Brain repo (and ideally the Ledger too). Curator v3.1's Cloudflare R2 backend (with per-bucket `jurisdiction = "eu"`) will relieve this in the future; firms launching today on EU residency must use Enterprise Cloud.

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

This section is intended for ephemeral state across sessions.

**As of 2026-05-15 (Shared Brain integration in flight):**

**Curator v3.0.0-beta Shared Brain integration started 2026-05-15.** ADR-002 ratified ([`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](docs/internal/ADR-002-firm-brain-curator-shared-brain.md)): the Firm Brain is a Curator Shared Brain instance in a separate GitHub repo from the Ledger; three distinct primitives (Ledger / Firm Brain / Second Brain) with three distinct write models. Decisions #14–#16 landed in this file. Tier 1 done — GLOSSARY terminology lock + GENERATIONS reclassification. **Tier 2 pending** — spec rewrites: `templates/brain/` (FIRM-ONTOLOGY + SPEC recast as Curator-Shared-Brain-native), `skills/my-curator/SKILL.md` (mirror semantics + onboarding), `skills/privacy-self-sovereign/SKILL.md` (map `contributor_retains` + UUID attribution to S12), `skills/governance-compliance/SKILL.md` + `governance/EU-AI-ACT.md` + `governance/SECRETS-POLICY.md` (admin_token / PAT lifecycle / revoke runbook), `routines/SPEC.md` (classify each Routine as Ledger-writing vs Firm-Brain-pushing; new R9 weekly Synthesize), `templates/partner-charter.md` (verify IP-assignment clause for `organisational` mode). **Tier 3 pending** — onboarding: install plans + wizard.py + cloud/privacy quickstarts + ECOSYSTEM + examples scaffolds.

**Resolved 2026-05-15: `<firm>-secondbrain` retired as a framework concept.** Three reasons drove the call: (1) the old pattern pushed each partner's *entire* vault to a firm repo (privacy leak on non-firm domains); (2) there was no canonical merge layer — N partners had N copies of `wiki/<firm-curator-domain>/`; (3) Shared Brain already provides a synthesized `collective/<firm-domain>/wiki/` that is strictly better as Routine context. **Framework provisions exactly two firm repos per firm: Ledger + Firm Brain.** Personal Curator backup-to-GitHub is a personal-tooling choice (Curator's built-in two-way sync handles it independently from the framework). Existing v1.0 `<firm>-secondbrain` repos may be kept as personal backup, archived, or deleted at firm discretion — no forced migration. Resolution baked into ADR-002.

**Install-path overhaul in flight.** Three install paths are being upgraded for less-technical founders:

- **Path A — coding-agent-assisted install — DONE 2026-05-10.** Built at `installer/agent-assisted/{README.md, AGENT-CAPABILITY-SPEC.md, cloud-install-plan.md, privacy-install-plan.md}`. LLM-agnostic capability spec; known-compatible agents include Claude Code (reference), Augment Code, Aider, OpenCode, Cline, Continue.dev.

- **Step 4 — sandbox + LIVE install test — DONE 2026-05-10.** Drove the cloud install plan against a sandbox at `/tmp/oot-test-install/` then against a real persistent test instance at `/Users/talirezun/00T-test-company/` + GitHub repo `talirezun/oot-test-company` (private). 18 findings recorded in [`docs/internal/install-test-report-2026-05-10.md`](docs/internal/install-test-report-2026-05-10.md). Pattern C verified live (signed commit `8bae769` lands on main with green Verified badge on GitHub). my-curator MCP integration confirmed against existing second-brain at `/Users/talirezun/second-brain/`. Test instance is **persistent** — Tali plans to use it for LM Studio testing.

  Sandbox-phase findings 1-8 fixed in commit [5ff1c55](https://github.com/talirezun/oot-framework/commit/5ff1c55):
  - **Finding 6 (CRITICAL):** R1 was not writing K (`value_envelope`) and L (`computed_variable`) formulas on appended rows → silent zero-pay bug. Fixed in `templates/excel/SPEC.md` X1 §Formulas, `routines/SPEC.md` R1 implementation, `routines/cloud/R1.md` prompt body.
  - **Finding 7:** `ws.max_row + 1` is wrong on Output_Log (the value_envelope_table at O1:P5 inflates max_row). R1 must find next empty row via column A. Fixed.
  - **Findings 1, 3, 4, 5:** install plan Step 0.1 + new Step 0.4 — Python version fallback (3.13/3.12/3.11/3 in order), per-OS install one-liners for gpg/gh/jq, and venv setup at `~/.oot/venv` to handle PEP 668.
  - **Finding 8:** install plan Step 10.1 referenced `build_excel.py --check` which doesn't exist; replaced with inline openpyxl smoke check.
  - **Finding 2:** Python ≥3.11 / 3.13-recommended canonicalised in CLAUDE.md.
  Live-phase findings 9-18 (NOT yet fixed in install plan — that's Step 5):
  - **#16 (CRITICAL):** GitHub Free private repos do not enforce branch protection. ADR-001's audit-trail-immutability claim does not hold without GitHub Team ($4/u/mo) or upgraded plan. Install plan must surface plan-tier choice as a structural decision.
  - **#13/14:** install plan's reliance on `gh` CLI is too high; web-UI fallback for repo creation, GPG upload, branch protection must be canonical for less-technical founders.
  - **#9/18:** install plan must handle (a) existing-Curator users + (b) Configuration A (separate vault and firm repo) vs. Configuration B (unified root) choice.
  - **#11/15/17:** Node preflight, clipboard sandbox issue, branch-protection instruction clarity.
  - Other findings 10/12: macOS file permissions; noreply email vs GPG email mismatch.

  Test instance preserved for follow-up:
  - GitHub: `talirezun/oot-test-company` (private)
  - Local: `/Users/talirezun/00T-test-company/`
  - GPG key: `oot-test-bot <blocklabstech@gmail.com>` (FF2AE322B7F4C193)
  - Curator domain: `00t-test-company` in `/Users/talirezun/second-brain/`

- **Step 5a — install-plan rewrite — DONE 2026-05-10.** Cloud install plan rewritten end-to-end (v1.0 → v1.1) with all 18 sandbox + live findings folded in:
  - New `installer/agent-assisted/START-HERE.md` — copy-paste prompt for any coding agent (LLM-agnostic).
  - New `installer/agent-assisted/cloud-install-plan.md` (v1.1.0): 14 steps. Adds **Step 0.5 (folder + Curator-vault location choice — Configuration A vs B per Finding 18)**, **Step 3 (GitHub plan-tier choice — Finding 16 critical)**, **Step 8 with Branch 8A (existing Curator) vs Branch 8B (greenfield) — Finding 9**. Web-UI is now the canonical user-facing path for repo creation, GPG upload, branch protection (Findings 13/14). Clipboard sandbox issue addressed (Finding 15) via print-in-chat or `open <file>`. Branch-protection instructions are now an unambiguous checkbox table (Finding 17). State-file format extended for the new dimensions.
  - The plan now also addresses Tali's meta-asks: explicit folder-selection step, plan-tier guidance up-front before any account creation, framework-script auto-install via venv (Step 0.3), Node preflight (Finding 11), email-vs-GPG-mismatch handling (Finding 12), macOS file permissions (Finding 10).
  - Privacy install plan and the wizard (Path B) and manual docs (Path C) need parallel updates → Step 5c/d remaining.

- **Step 5c — Path C / manual quickstarts polished — DONE 2026-05-10.** `docs/00-quickstart-cloud.md` rewritten end-to-end with:
  - **Non-technical primer** at the top (terminal, JSON, GitHub, MCP, signed commit, branch protection — defined in plain English).
  - **8-decision section** before any installs: cloud/privacy, EU exposure, firm folder location, existing-Curator yes/no, Configuration A vs B, **GitHub plan-tier (Finding 16 prominently surfaced as a CRITICAL decision)**, Anthropic Pro vs Max, spreadsheet app.
  - Sunday morning expanded from bullet points into a 10-step procedural walkthrough with **explicit web-UI guidance** (URLs and click sequences) for: GitHub repo creation, GPG key generation + upload, branch protection (with the clean Finding 17 checkbox table), Curator domain setup with Configuration A/B branch.
  - Per-OS install commands for `gnupg`, `node`, `python3.13` (macOS / Linux / Windows-WSL).
  - Python venv setup explained (PEP 668 fix per Finding 5).
  - macOS file-permissions step (Finding 10).
  - Email-vs-GPG-mismatch troubleshooting (Finding 12) inline with verification step.
  - "Open file in TextEdit, Cmd+A, Cmd+C" pattern for the GPG public key (Finding 15 — replaces `pbcopy` reliance).
  - Common pitfalls expanded with 3 new entries from the live-test findings.
  - File grew from ~170 lines to ~370 lines; this is hand-holding for less-technical founders, by design.

  `docs/00-quickstart-privacy.md` updated with a 7-point decisions section mirroring cloud's, plus a privacy-specific GitHub plan-tier callout (Finding 16 applies to privacy track too — it still uses GitHub for the Ledger). Common pitfalls expanded with 2 new entries (plan-tier + cloud-LLM-ingest-still-happens-in-Gen-1).

- **Step 5b — privacy install plan rewrite — DONE 2026-05-10.** `installer/agent-assisted/privacy-install-plan.md` rewritten to v1.1.0. Folds the same 18 findings as the cloud plan (where applicable) plus privacy-track-specific structure: hardware acquisition pre-week (Trezor, Mac mini / NUC / Pi 5, UPS, Yubikey), always-on machine OS setup (FDE, dedicated user, network hardening), per-partner Trezors (Day-1 not Gen-2), LM Studio + Qwen 3 14B / Llama 3.3 70B / DeepSeek-V3, 4thtech firm domain + dChat workspace, PollinationX storage NFT, OS-native scheduling (cron / launchd / Task Scheduler) instead of Claude Code Routines. Includes "agent runs on daily laptop, install target is always-on machine" handling — agent walks user through manual commands on the remote machine OR through SSH if user opts in. Same plan-tier guidance for GitHub branch protection (Finding 16 applies identically — privacy track still uses GitHub for the Ledger).
- **Step 5d — wizard implementation — DONE 2026-05-10.** `installer/wizard.py` rewritten v1.0 → v1.1.0. Now a complete 14-step interactive wizard mirroring the agent-runnable plan's structure. Programmatic where safe (folder/git/GPG/file operations); web-UI walkthrough where user must approve third-party actions. State at `~/.oot/wizard-state.yaml`; resumable via `--resume`; dry-run via `--dry-run`. Uses `questionary` + `rich` if installed, falls back to plain `input()`/`print()` if not. Implements all the Step 5a-5c findings: 8-decision flow before any installs, GitHub plan-tier choice (Finding 16), Configuration A vs B for Curator vault (Finding 18), existing-Curator detection (Finding 9), explicit branch-protection web-UI walkthrough with the clean checkbox table (Finding 17), email-vs-GPG-mismatch handling (Finding 12), `open <file>` pattern for GPG key copy (Finding 15), per-OS install commands for missing tools (Finding 3), Python venv setup at `~/.oot/venv/` (Findings 4/5).

- **Path B — wizard (`installer/wizard.py`)**: now a complete 14-step interactive wizard. (Was: scaffold with 1-4 functional, 5-12 stubbed in v1.0.)
- **Path C — manual (docs)**: `docs/MODULES.md` shipped (Step 2 of overhaul). Cloud + privacy quickstarts updated to point at Path A first. Bitwarden/Trezor/Yubikey re-tiered as recommended-but-optional. Plan-tier guidance (Pro vs Max) shipped throughout.

**Excel writeback resolved (Pattern C, ADR-001) — DONE 2026-05-10.** Cloud Routines mutate `.xlsx` files in the firm's Ledger GitHub repo via openpyxl + signed commits — not via Google Sheets. Same operation on cloud and privacy. Implemented across:
- `docs/internal/ADR-001-cloud-routine-excel-writeback.md` (the design-of-record).
- `routines/SPEC.md` (rewritten preamble + R1-R8 mcp_servers + prompt bodies).
- All `routines/cloud/R*.md` (frontmatter v1.1.0, ledger_repo_access + code_execution keys, prompt-body Pattern C blocks).
- All `routines/privacy/R*.md` (per-track delta updated from "Excel MCP" to "openpyxl on local Brain-repo clone").
- `templates/excel/SPEC.md` (new "Excel files in operation" section + spreadsheet-viewer guidance).
- `docs/00-quickstart-cloud.md`, `docs/02-installing-routines.md` (Pattern C taught to founders + plan-tier guidance + Bitwarden/Trezor/Yubikey re-tiered).
- 17 other files renamed "Anthropic Remote Routines" → "Claude Code Routines" + plan-tier nuance + spreadsheet-app-agnostic language.

**Verified (2026-05-10):** `python3 scripts/validate_skills.py` → 12/12 pass; `lychee --offline` → 0 errors / 277 excluded; `python3 scripts/build_excel.py` → all 9 templates regenerate cleanly.

**Bitwarden / Trezor / Yubikey re-tiered as optional for Gen 1.** See decision #13. Quickstart docs will be updated to make these optional rather than gating, with explicit "skip until you grow" affordances.

**Routines plan-tier guidance.** Pro plan ≤2 partners + no R7; Max for everyone else. Decision #12.

**Spreadsheet-viewer support.** Microsoft Excel, LibreOffice (free, open-source), Apple Numbers, Excel-for-Web, Google Sheets via "Open with" — all supported. Don't recommend any single paid app.

**Real-world adoption.** Tali plans to adopt the framework for his own firms (4thtech, PollinationX) as the first real-world test. Repository at [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework). 18 commits on `main`. Tag `v1.0.0`.

> Future sessions: update this section with what's currently in flight. Stale items get pruned at v1.x release boundaries.

---

> **The framework's authors** ([`MANIFESTO.md`](MANIFESTO.md) closing): *"The pieces are real. The infrastructure is here. The legal landmines are mapped. The discipline is in the framework."*

> v1.0 is operational. The rest is execution.
