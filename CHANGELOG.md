# Changelog

## Unreleased — post-v1.0.0 (in progress, May 2026)

Doc + spec updates that land between v1.0.0 and the next tagged release. Code/spec only — no functional Routine changes.

**Second Brain bridge — closes the v1.0 cloud Routines reachability gap (2026-05-12):**
- Cloud Routines can now reach the firm's Second Brain (the Curator semantic graph) via Curator's existing two-way GitHub sync, without an always-on machine. Solves the gap that previously made R5 effectively broken on cloud track.
- Mechanism: Curator's Sync tab mirrors the entire local vault to a private GitHub repo. Cloud Routines (specifically R5 in v1.0.1; R2/R8 candidates for Gen-2 enrichment) clone that repo at execution time, scoped to `wiki/<firm-curator-domain>/`, and operate on plain markdown files via Pattern C (ADR-001).
- New wizard step `step_12_secondbrain_sync` — slots between Curator (11) and Routines (renumbered 13). Total wizard step count 14 → 15. Walks user through enabling Curator GitHub sync, creating a fine-grained PAT with Contents:Read only on the synced repo, verifying a clone works. PAT is never persisted to wizard state — user keeps it in their password manager and pastes into Claude Code's Routine connector at Step 13.
- R5 prompt body rewritten v1.1.0 → v1.2.0. Two GitHub connectors (Ledger read-write, Second Brain read-only). Broken-wikilink / orphan / stale scans implemented via markdown parsing. Trade-off documented: no semantic-similarity scans on cloud (defer Gen-2), no auto-fix of typo-correctable wikilinks (read-only on cloud side — typos listed in report, user fixes via Curator app).
- `docs/AUTOMATION-PIPELINE.md` gap section rewritten as "How the bridge works." Privacy-track positioning shifted from "the alternative" to "advanced / sovereignty mandate." Gen-2 paths flagged (Anthropic-hosted Curator OR stateless cloud-MCP variant).
- `installer/agent-assisted/cloud-install-plan.md` gets a new Step 9b mirroring the wizard step.
- Migration shim in `installer/wizard.py` `_migrate_state_keys()` promotes pre-rename step keys AND resets `step_13_routines` if the new bridge step isn't done, so mid-install users re-configure Routines with the second connector.

**Naming cleanup: "Brain repo" → "Ledger"; introduce "Second Brain" as canonical (2026-05-12):**
- "The Brain" had six distinct meanings across the framework. Rename pass: GitHub operational repo (which holds Excel files + audit logs + Routine writebacks) is now consistently called the **Ledger** / **operational Ledger**. The Curator's semantic knowledge graph keeps its name as **the Brain** / **Second Brain** (the PKM term users will recognise). Distinct from **Cotrugli Ledger** (Gen-3 accounting/governance backbone) — first-mention disambiguators added wherever both terms appear.
- New GLOSSARY.md entries: **Ledger**, **Second Brain repo**.
- 51 files changed; ~280 line-level renames across user-facing docs (GLOSSARY, README, QUICKSTART, GENERATIONS, all of `docs/`, all 16 Routine prompts) plus internal specs (CLAUDE.md, SPEC.md, BUILD-INSTRUCTIONS.md, ADR-001, PROVISIONING-SPEC.md). State-variable renames in `installer/wizard.py` (`brain_repo_url` → `ledger_repo_url`, etc.) with a backward-compat migration shim so existing wizard state files don't lose progress.
- Kept as-is: `templates/brain/` folder (these are Curator-graph page templates), MANIFESTO.md Thesis 4 references (philosophical), Routine names like "R5 Brain Health Check" (proper names), Skill Pack S1 my-curator references (Curator-graph context).



**Documentation alignment with the actual Anthropic product surface:**
- "Anthropic Remote Routines" renamed to "Claude Code Routines" repo-wide (the actual product name; Anthropic launched the feature 14 April 2026). Old name preserved in v1.0.0 release notes for historical accuracy.
- Per-day Routine run limits documented: Pro 5, Max 15, Team 25, Enterprise 25. Plan-tier guidance added to quickstart and routines docs.

**ADR-001 — cloud-track Excel writeback canonical pattern:**
- Operational `.xlsx` files (X1–X9) now live in the firm's Ledger GitHub repo at `firm/excel/`, not in Google Sheets / Drive.
- Routines mutate them via openpyxl in code execution, signed-commit, push. Track-symmetric: cloud and privacy Routines do the same operation against the same repo.
- Native Google Workspace connector remains available for read-only Drive / Calendar / Gmail integration; not used as a state store.
- See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](docs/internal/ADR-001-cloud-routine-excel-writeback.md) for the full decision rationale and alternatives considered.

**User-side spreadsheet app independence:**
- Microsoft Excel, LibreOffice (free, open-source), Apple Numbers, Excel for Web, WPS Office, OnlyOffice — all officially supported. The framework writes native `.xlsx` and is app-agnostic. Google Sheets is supported for one-off pivots via "Open with" but is not the canonical store.

**Bitwarden / Trezor / Yubikey re-tiered as recommended-but-optional in Gen 1:**
- Day-1 minimum is Anthropic + GitHub + Slack only. Bitwarden + Yubikey best-practice but not gating for solo / 2-partner founders. Trezor stores keys not used until Gen 2 stablecoin payroll — beginning founders skip it entirely until v2.0.

**Library polish:**
- `research/articles/` standardised to a single contribution format with visible author block, summary, "why this matters for ØØT", and cross-references. Three Curator articles linked as recommended pre-reading.
- `.lycheeignore` filters known v1.x-deferred placeholders (screenshot binaries, template-variable fragments) so CI link-check passes.

## v1.0.0 — 2026-05-09

The framework's first stable release. **Generation 1 is operational.**

### What's in the box

**Foundation (Phase 0):**
- 16 foundation-kit specification files (MANIFESTO, SPEC, GLOSSARY, QUICKSTART, GENERATIONS, CLAUDE.md, BUILD-INSTRUCTIONS, plus 4 governance docs, the skill template, the per-pack SPECs, the Excel SPEC, the Routine SPEC, the docs SPEC).
- Citation integrity verified across the manifesto (MIT NANDA, METR, HBS Cybernetic Teammate, Klarna trajectory, EU AI Act timeline, MiCA, GENIUS Act).
- 12 spec corrections applied (cross-workbook discipline, R3 Brain checkbox, R6 signed-commit immutability, X5 perception threshold, X9 Q05 phrasing, etc.).

**Repository structure (Phase 1):**
- Apache 2.0 + CC BY-SA 4.0 licence pair.
- AGENTS.md + CLAUDE.md cross-vendor orientation.
- README hub with "Read in this order" navigation table, repository map, external ecosystem links.

**12 Skill Packs (Phase 3 + Phase 4):**
- 7 Tier-1 hardened: My Curator (S1, imported verbatim from talirezun/the-curator), Context Engineering (S2), Compensation & Attribution (S3), Code & QA (S4), Reporting & Business Review (S5), Change Management (S6), Privacy / Self-Sovereign Stack (S12).
- 5 Tier-2 scaffolds: Governance & Compliance (S7), Legal Operations (S8), Marketing (S9), Finance & Treasury (S10), Sales & BD (S11).
- 14+ worked examples across the Tier-1 packs.

**Brain templates (Phase 4):**
- `FIRM-ONTOLOGY.md` — the canonical `firm/` namespace.
- 14 page templates (daily output log, audit log, BR, Klarna test, variable statement, long-tail statement, output spec, partner profile, reward species declaration, decision record, ADR, pilot summary, dispute record, prompt artefact).

**Onboarding (Phase 4):**
- Partner Charter template (11 sections; counsel review required).
- Output Spec tutorial copy with inline guidance.
- 30-step onboarding checklist.
- POSIX-compatible `provisioning-script.sh` (8 steps; idempotent; resumable; track-aware).
- 90-day onboarding plan.

**9 Excel templates (Phase 5):**
- All formulas verified; conditional formatting; data validation; per-spec sample data.
- Generated via `scripts/build_excel.py` (openpyxl); reproducible.
- Hidden `_metadata` sheet + README per file.

**16 Routine markdown files (Phase 6):**
- 8 cloud Routines (Anthropic Remote Routines).
- 8 privacy-track equivalents (cron / launchd / Task Scheduler hitting headless LM Studio).
- Comprehensive `routines/README.md` with recommended install order.

**18 user guides (Phase 7):**
- 12 Tier-1 plain-language guides (`docs/00-...` through `docs/08-...` plus `ECOSYSTEM.md` and `glossary.md`).
- 6 Tier-2 UI walkthroughs (`docs/walkthroughs/W1-` through `W6-`).
- Three-layer pattern (orientation → walkthrough → pitfalls) for every UI-touching guide.

**CI / Klarna gate (Phase 8):**
- `scripts/validate_skills.py` — SKILL.md frontmatter validator.
- `.github/workflows/lint-skills.yml` — runs validator on PR.
- `.github/workflows/markdown-lint.yml` — markdown style + offline link check.
- `.github/workflows/excel-validation.yml` — opens all 9 .xlsx; verifies critical formulas.
- **`.github/workflows/klarna-gate.yml`** — the framework's signature pre-merge gate. Posts `oot/klarna-test` status check; turns green only when ≥14/20 + scorer signoff + non-beneficiary signoff.
- `.github/workflows/auto-label.yml` + `.github/labeler.yml` — applies `ai-replaces-human` label per the auto-labeller signatures from S4 §4.8.
- `.github/PULL_REQUEST_TEMPLATE.md` + 2 issue templates.

**Installer (Phase 9):**
- `installer/wizard.py` — Python terminal wizard scaffold (steps 1-4 functional in v1.0; steps 5-12 land in v1.x).
- `installer/cloud/install.sh` + `installer/privacy/install.sh` — fallback scripts for users who refuse the wizard.

**3 Reference orgs (Phase 9):**
- `examples/small-org/` — 3-partner Solunar Studio scaffold.
- `examples/medium-org/` — 12-partner Brda Cooperative scaffold.
- `examples/regulated-eu-org/` — 6-partner AdriaLex AI scaffold; the **abandoned engagement** (KT-2026-005) is the most important single artefact.

**Research (Phase 7):**
- `research/README.md` — articles index + paper summaries index by thesis.
- `research/external-resources.md` — comprehensive ecosystem index with URLs, licences, ØØT cross-references.
- 2 article stubs (`2026-05-prompts-to-precision.md`, `2026-04-three-philosophies.md`).
- 3 paper summaries (MIT NANDA, METR, Klarna 2024-2026).

### Statistics

- **165 files** total.
- **~70,000 words** of structured specification + documentation.
- **15 phase-numbered commits** representing the build's discrete stages.

### What's deferred to v1.x / v2.0

Per [`GENERATIONS.md`](GENERATIONS.md):

- **v1.x:** Tier-2 Skill Packs hardening (S7-S11); installer wizard steps 5-12 programmatic; reference orgs full operational data; additional Tier-2 walkthroughs.
- **Generation 2 (6-12 months):** stablecoin payroll (Rise/Circle); smart-contract long-tail entitlements; Internal Unit Fund; Curator local-LLM ingest.
- **Generation 3 (12-24 months, theoretical):** Cotrugli Ledger anchoring; Kelly-style autonomous business units.

### Acknowledgements

- **Initiator:** Dr. Tali Režun (COTRUGLI Business School; Lumina AI; 4thtech; PollinationX).
- **Founding contributors:** Dražen Kapusta (Cotrugli Ledger); COTRUGLI Business School (institutional anchor).
- **AI co-authorship:** the v1.0 build used Claude Opus 4.7 extensively in scaffolding the framework's 165 files. The AI's contributions are tracked via `Co-authored-by:` trailers per the framework's own discipline.

The framework's intellectual core (theses, Skill Pack designs, governance disciplines, Klarna Test) is the human contribution. The artefact production (file scaffolding, Excel template generation, doc writing) is the AI contribution. This is the centaur model the framework prescribes, applied to the framework itself.

---

### Repository

[github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)
