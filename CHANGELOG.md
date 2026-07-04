# Changelog

ØØT follows [Semantic Versioning](https://semver.org). The framework's version is independent of Generation: v1.x is the Gen-1 release line; Gen-2 will open the v2.x line; Gen-3 will open v3.x.

## Unreleased

Driven by the full-repo audit of 2026-07-03 and delivered as a phased improvement plan.

- **Audit-driven trust fixes (2026-07-04).** Installer wizard state machine hardened (missing Brain-ingest + Klarna-gate steps added; renumbered to 18 steps branded /17); the Klarna gate reworked; R1 dedupe + last-run catch-up semantics so irregular routine cadence never double-pays.
- **Doc-truth sweep.** The Second Brain bridge is now taught in Path C (`docs/00-quickstart-cloud.md` Step 8c); [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md#cost-summary) is the canonical cost page (other docs link, don't restate); contradiction kill-list resolved (Klarna ≥14/20, Routine per-day limits 5/15/15/25, Google-Sheets ghosts → openpyxl per ADR-001, retired "Brain repo" → "Ledger").
- **NEW: the community track ([ADR-003](docs/internal/ADR-003-community-track-no-subscription.md)).** A third operating configuration — **no Anthropic subscription, no dedicated hardware**. Install and operate ØØT with **OpenCode** on free/local models; scheduled automation via a 3-rung ladder (manual playbook runs → laptop cron → GitHub Actions). New harness appendix [`installer/agent-assisted/OPENCODE-SETUP.md`](installer/agent-assisted/OPENCODE-SETUP.md); MODULES / quickstart decision blocks / FAQ / ECOSYSTEM / GLOSSARY updated; OpenCode naming resolved (`anomalyco/opencode`, formerly `sst/opencode`; npm `opencode-ai`) and its R4 mapping (`"permission": {"*": "ask"}`; `--auto` prohibited during install) documented. End-to-end community-track install test QUEUED alongside the privacy-track e2e.
- **Privacy-track invocation grounded in reality (2026-07-04).** The audit found the privacy track had likely never run end-to-end because its Routines invoked a fabricated `llmster --skill/--prompt-file/--backfill` CLI. Corrected framework-wide: `llmster` is real but it is LM Studio's **headless daemon** (it *hosts* models on the OpenAI-compatible server), not an agent. The privacy harness is **OpenCode headless** — `opencode run --model lmstudio/<model> "$(cat r*.prompt.md)"` — against the llmster-hosted server; models are managed with LM Studio's real `lms` CLI (`lms load … --ttl`). A scoped-unattended `opencode.json` (allow git/python3/mktemp + edit-in-workdir, else `ask`; never `--auto`) is documented wherever cron/launchd is introduced. The `--backfill` flag is replaced by R1's real dedupe + last-run catch-up semantics. Privacy `R5` gained its own MCP-based brain-health prompt (`scan_wiki_health` + `scan_semantic_duplicates` + typo auto-fix) instead of inheriting cloud R5. `installer/cloud/install.sh` + `installer/privacy/install.sh` shrunk to thin pointers to Paths A/B/C.
- **Excel schema hardening — ADR-004 + ADR-005 (2026-07-04).** Two schema ambiguities that become defects the day a firm has a second partner are now closed. **[ADR-004](docs/internal/ADR-004-klarna-status-column.md):** X4 Decision_Log gains column **M `status`** — a lifecycle enum (`scoring | remediation | monitoring | proceeded | held`) distinct from the formula-driven `decision` verdict (column I); the "appended-row contract" (per-column literal / formula-the-routine-MUST-write / human-only) becomes a required per-workbook SPEC section, generalising the Finding-6 silent-zero-pay fix to X1/X4/X8. **[ADR-005](docs/internal/ADR-005-partner-join-key-and-output-weight.md):** `partner_id` (`P-NNN`) becomes the universal join key — `Base_Variable_Split` and `Long_Tail_Schedule` each gain a **leading `partner_id` column** (single shared sheets; per-partner sheets rejected; all downstream column letters shift right by one), and X1 Output_Log gains column **N `weight`** so co-authored outputs share the value envelope (`L = K·J·N·IF(rework)`) instead of double-paying; `templates/output-spec.md` gains an optional `attribution_split` field. Routines (R1/R3/R4/R7), S3, the 9 regenerated `.xlsx` templates, and the test suite are updated. **Migration for existing Gen-1 workbooks** is documented in `templates/excel/SPEC.md` (insert the columns, backfill `partner_id`, refill the L formula; no automated migrator in Gen 1).
- **Validator + gate hardening (2026-07-04).** `scripts/validate_skills.py` gained 6 new checks (tier/status agreement, name==folder, pack-id `S<1-12>` format + cross-file uniqueness, examples-dir + TODO-ban for hardened packs, scaffold generation-marker requirement, no future `last_updated`) — still 12/12 on the real tree. `governance/KLARNA-TEST.md` gained per-question 0/1/2 anchors for Q1–Q7/Q9/Q10 (matching the existing Q8 style). The Klarna gate workflow now always posts its status (killing the required-check deadlock), reads the workbook from the PR base branch, and guards the framework repo itself.
- **Test suite + CI (2026-07-04).** New `tests/` pytest suite (51 tests: SKILL validator round-trip, `build_excel` structural asserts incl. the ADR-004/005 schema, wizard state machine). `python-tests.yml` runs pytest as a **hard gate** and drops the old `|| true`; `excel-validation.yml` does a real regenerate-and-cell-compare drift check.
- **Reference org populated (2026-07-04).** `examples/small-org/` (Solunar Studio) ships a representative two-week slice — 25 `firm/` pages including an ADR-005 co-authored (weight 0.5/0.5) output, a resolved Tier-1 comp dispute, R6 audit logs, and a brain-health page — with every wikilink resolving. Medium-org + regulated-eu-org remain README-only pending v1.x.

## v1.2.0 — 2026-05-15

**Tier 3: user-facing surface aligned with the v1.1.0 Firm Brain primitive.** Where v1.1.0 rebuilt the framework's internal specs (ADR-002, ontology, skills, governance, routines/SPEC, partner-charter) around the three-primitive split (Ledger / Firm Brain / Second Brain), v1.2.0 carries that alignment through to the docs and tools founders actually touch on Sunday morning of Weekend One.

**Quickstarts ([`docs/00-quickstart-cloud.md`](docs/00-quickstart-cloud.md), [`docs/00-quickstart-privacy.md`](docs/00-quickstart-privacy.md)):**
- §6 (GitHub plan-tier) restated for **two protected repos** per firm (Ledger + Firm Brain), with new GitHub Enterprise Cloud + EU residency tier surfaced for EU privacy-mandate firms.
- New §9 "Firm Brain IP mode" — `organisational` vs `contributor_retains` decision before installs; both attribution flags default false → UUID-pseudonymous baseline.
- Sunday-morning Step 1 fixed: Ledger is now `<firm-slug>-ledger` (post-v1.0.1 canonical); new Step 1b creates `<firm-slug>-brain` (Firm Brain) alongside.
- New Step 7b — branch protection on the Firm Brain repo.
- New Step 8b — Curator Shared Brain admin wizard end-to-end (IP-mode selection, admin_token + invite token generation + Bitwarden save, founder's own contributor wizard, Push → Synthesize → Pull verification).
- Weekend Two onboard-first-partner adds the Firm Brain contributor wizard substep + Sunday R9 Synthesize.

**Install plans ([`installer/agent-assisted/cloud-install-plan.md`](installer/agent-assisted/cloud-install-plan.md), [`installer/agent-assisted/privacy-install-plan.md`](installer/agent-assisted/privacy-install-plan.md)):**
- Step 3 (plan-tier choice) extended for two repos + EU residency option.
- Step 5 (now "Create GitHub Ledger + Firm Brain repos + initial scaffold") creates both repos with `gh` automation where available; migration note for pre-v1.0.1 installs.
- Step 7 (branch protection) now does both repos with handling for empty Firm Brain (defer to Step 8.5).
- **New Step 8.5** — full Firm Brain admin wizard with IP-mode, tokens, Bitwarden save, founder contributor wizard, end-to-end verification.
- Privacy install plan delegates to cloud Step 8.5 with privacy-specific deltas (R9 cron on the always-on machine; `contributor_retains` often preferred for self-sovereign partners).

**Wizard (Path B, [`installer/wizard.py`](installer/wizard.py) v1.2.0):**
- `WIZARD_VERSION` bumped 1.1.0 → 1.2.0.
- `step_08_brain_repo` extended to a 5-substep flow: creates Ledger AND Firm Brain repos. Default Ledger repo name corrected to `<firm-slug>-ledger` (was `-brain` pre-v1.0.1); Firm Brain repo `<firm-slug>-brain`. `gh` automation for both; web-UI fallback; collision detection if user proposes the same name.
- `step_10_branch_protection` applies branch protection to both repos; gracefully defers the Firm Brain pass if `main` doesn't exist yet (Curator admin wizard creates the first commit).
- `step_11_curator` extended with a new Step 11b — Curator Shared Brain admin wizard sub-flow: IP-mode pick, admin_token + invite-token generation guidance, Bitwarden-save confirmation, founder contributor wizard, Push → Synthesize → Pull end-to-end verification, deferred Firm Brain branch protection reapply.
- `step_15_summary` displays both repo URLs + Firm Brain IP mode + token-save flags.

**Other docs:**
- [`docs/02-installing-routines.md`](docs/02-installing-routines.md) — R9 (Firm Brain Synthesize) added to the "Other Routines" section with the privacy-track cron line and a clear note that R9 does NOT count against Claude Code Routine per-day plan limits. Per-Routine repo-access matrix tabulated.
- [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md) — Curator entry bumped to v3.0.0-beta.1; Shared Brain capability + version requirement + Gen-1 cloud-LLM gap + v3.1 forward path.
- [`examples/small-org/README.md`](examples/small-org/README.md), [`examples/medium-org/README.md`](examples/medium-org/README.md), [`examples/regulated-eu-org/README.md`](examples/regulated-eu-org/README.md) — each reference org now names its two repos, IP mode (incl. mixed-mode handling via side-letter for Solunar Studio's contractor), attribution-flag posture, Synthesize cadence, and (for AdriaLex) Article 17 revoke rehearsal.

**Compatibility note.** Existing v1.0 installs with `<firm-slug>-brain` as the Ledger repo continue to work — both names remain valid per the GLOSSARY. Migration is offered (rename to `<firm-slug>-ledger`) but not required.

## v1.1.0 — 2026-05-15

**The Firm Brain — Curator Shared Brain integration ([ADR-002](docs/internal/ADR-002-firm-brain-curator-shared-brain.md)).** The framework's "firm IP" layer is now a first-class Curator Shared Brain instance (v3.0.0-beta+), distinct from the Ledger and from each partner's personal Second Brain. Three named primitives:

- **Ledger** (`<firm>-ledger`) — Excel + audit logs, written by Routines per ADR-001.
- **Firm Brain** (`<firm>-brain`) — Curator Shared Brain, written by partners pushing their opted-in domain; synthesized weekly by the admin.
- **Second Brain** — each partner's *personal* Curator vault on their own machine; one opted-in domain contributes to the Firm Brain.

**Three new design decisions in `CLAUDE.md`** (#14–#16): the three-primitive split + retire `<firm>-secondbrain`; IP-mode defaults (`organisational` for full-time partners, `contributor_retains` for advisors/contractors; both attribution flags default false → UUID-pseudonymous attribution); plan-tier guidance now applies to *two* protected repos per firm.

**Retired:** the pre-v1.0.1 per-partner `<firm>-secondbrain` repo pattern as a framework primitive. Cloud Routines that need firm-context knowledge now read the Firm Brain's `collective/<firm-domain>/wiki/` (synthesized, deduplicated, conflict-flagged). Personal Curator backup-to-GitHub remains available as a per-partner tooling choice. Existing v1.0 `<firm>-secondbrain` repos may be kept as personal backup, archived, or deleted at firm discretion — no forced migration.

**New routine R9 — Firm Brain Synthesize.** Admin-run weekly (Sunday evening recommended). Curator merges per-partner contributions, applies Jaccard + selective-LLM conflict resolution, rebuilds the collective index, signed-commits to the Firm Brain repo. Does **not** count against Claude Code Routine per-day limits (runs on the admin's machine via Curator CLI).

**Documents added / rewritten:**
- New ADR: [`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](docs/internal/ADR-002-firm-brain-curator-shared-brain.md).
- [`templates/brain/FIRM-ONTOLOGY.md`](templates/brain/FIRM-ONTOLOGY.md) — full rewrite. Three-primitive content layout (Ledger paths, Firm Brain `entities/concepts/summaries`, personal Second Brain). Sequence diagram of how a new firm decision propagates Push → Synthesize → Pull.
- [`templates/brain/SPEC.md`](templates/brain/SPEC.md) — per-template "Lives in" column; Firm Brain slug-prefixing rules.
- [`skills/my-curator/SKILL.md`](skills/my-curator/SKILL.md) — wrapper updated with Shared Brain context (canonical imported content untouched per upstream-import rule).
- [`skills/privacy-self-sovereign/SKILL.md`](skills/privacy-self-sovereign/SKILL.md) (S12) — new §4.11 "Curator Shared Brain on the privacy track"; data-minimisation gain; `contributor_retains` for advisors; cloud-LLM-call boundary; hardware-key alignment.
- [`skills/governance-compliance/SKILL.md`](skills/governance-compliance/SKILL.md) (S7) — new §4.6.5 GDPR Article 17 runbook for Curator's revoke endpoint.
- [`governance/EU-AI-ACT.md`](governance/EU-AI-ACT.md) — Article 12 immutability now covers both Ledger and Firm Brain; **new section** for GDPR Article 17 with Curator revoke procedure + limitations + absolute-erasure handling.
- [`governance/SECRETS-POLICY.md`](governance/SECRETS-POLICY.md) — Bitwarden vault now holds `admin_token` (founders), per-partner Firm Brain PATs (per-partner collection), Ledger Routine bot PAT (shared-services).
- [`routines/SPEC.md`](routines/SPEC.md) — new "Routine write authority: Ledger only" section + per-Routine repo access matrix; R9 specification.
- [`templates/partner-charter.md`](templates/partner-charter.md) — §8 IP clause expanded: §8.1 IP mode mapping, §8.2 what stays with partner vs firm, §8.3 GDPR Article 17 on exit. §10 Exit updated with Firm Brain access revocation.
- [`GLOSSARY.md`](GLOSSARY.md) — five new / rewritten entries: **Firm Brain**, **Shared Brain (Curator primitive)**, **opted-in domain**, **synthesized mirror**; **Second Brain** reframed as explicitly personal; **Second Brain repo** marked deprecated as framework primitive.
- [`GENERATIONS.md`](GENERATIONS.md) — Gen 1 tech layer now names two firm repos (Ledger + Firm Brain); Curator local-LLM ingest deferral clarified (admin's Synthesize step still cloud-LLM in Gen 1).

**Versioning & release process.** Added a version badge in the README. CHANGELOG now opens with the semver-and-generation policy.

## v1.0.1 — 2026-05-13

Patch release covering everything that shipped between v1.0.0 and the Firm Brain work: the Second Brain bridge, the Ledger naming pass, ADR-001 doc-alignment, and the three-path installer overhaul. *(Tag created retroactively on 2026-07-03 — these changes were on `main` by 2026-05-13 and were already referenced as "v1.0.1" throughout the docs.)*

**Installer overhaul (all three paths, driven by the 18 sandbox + live install-test findings of 2026-05-10):**
- **Path A (agent-assisted)** — new `installer/agent-assisted/` with `START-HERE.md` copy-paste prompt, LLM-agnostic `AGENT-CAPABILITY-SPEC.md`, and cloud + privacy install plans (v1.1.0, 14+ steps incl. plan-tier choice, Configuration A vs B, existing-Curator branch).
- **Path B (wizard)** — `installer/wizard.py` rewritten from a 4-step scaffold to a complete interactive wizard with resume, dry-run, back-navigation, `gh` automation, and a one-line bootstrap (`installer/bootstrap.sh`).
- **Path C (manual)** — both quickstarts rewritten end-to-end with a non-technical primer, an 8-decision section, and explicit web-UI walkthroughs.
- Agent-as-daily-UI: `DAILY-OPS.md` / `WEEKLY-OPS.md` / `MONTHLY-OPS.md` runnable playbooks for non-technical founders.
- New `docs/MODULES.md` (module-dependency map + Day-N progression) and `docs/AUTOMATION-PIPELINE.md` (cloud + privacy pipeline diagrams); README redesigned for install discoverability.

### Second Brain bridge — closes the v1.0 cloud Routines reachability gap (2026-05-12)

- Cloud Routines can now reach the firm's Second Brain (the Curator semantic graph) via Curator's existing two-way GitHub sync, without an always-on machine. Solves the gap that previously made R5 effectively broken on cloud track.
- Mechanism: Curator's Sync tab mirrors the entire local vault to a private GitHub repo. Cloud Routines (specifically R5 in v1.0.1; R2/R8 candidates for Gen-2 enrichment) clone that repo at execution time, scoped to `wiki/<firm-curator-domain>/`, and operate on plain markdown files via Pattern C (ADR-001).
- New wizard step `step_12_secondbrain_sync` — slots between Curator (11) and Routines (renumbered 13). Total wizard step count 14 → 15. Walks user through enabling Curator GitHub sync, creating a fine-grained PAT with Contents:Read only on the synced repo, verifying a clone works. PAT is never persisted to wizard state — user keeps it in their password manager and pastes into Claude Code's Routine connector at Step 13.
- R5 prompt body rewritten v1.1.0 → v1.2.0. Two GitHub connectors (Ledger read-write, Second Brain read-only). Broken-wikilink / orphan / stale scans implemented via markdown parsing. Trade-off documented: no semantic-similarity scans on cloud (defer Gen-2), no auto-fix of typo-correctable wikilinks (read-only on cloud side — typos listed in report, user fixes via Curator app).
- `docs/AUTOMATION-PIPELINE.md` gap section rewritten as "How the bridge works." Privacy-track positioning shifted from "the alternative" to "advanced / sovereignty mandate." Gen-2 paths flagged (Anthropic-hosted Curator OR stateless cloud-MCP variant).
- `installer/agent-assisted/cloud-install-plan.md` gets a new Step 9b mirroring the wizard step.
- Migration shim in `installer/wizard.py` `_migrate_state_keys()` promotes pre-rename step keys AND resets `step_13_routines` if the new bridge step isn't done, so mid-install users re-configure Routines with the second connector.

**Note on the bridge under ADR-002 (added in v1.1.0).** The bridge work above remains operational for *personal* Second Brain backup. For *firm* context, post-v1.1.0 Routines should prefer reading the Firm Brain's `collective/<firm-domain>/wiki/` per ADR-002 — the bridge's per-partner secondbrain repo is no longer the canonical firm-context source. Tier-3 updates (installer rewrites, quickstart docs) landed in v1.2.0; full retirement of the legacy bridge target lands in v1.3.

### Naming cleanup: "Brain repo" → "Ledger"; introduce "Second Brain" as canonical (2026-05-12)

- "The Brain" had six distinct meanings across the framework. Rename pass: GitHub operational repo (which holds Excel files + audit logs + Routine writebacks) is now consistently called the **Ledger** / **operational Ledger**. The Curator's semantic knowledge graph keeps its name as **the Brain** / **Second Brain** (the PKM term users will recognise). Distinct from **Cotrugli Ledger** (Gen-3 accounting/governance backbone) — first-mention disambiguators added wherever both terms appear.
- New GLOSSARY.md entries: **Ledger**, **Second Brain repo**.
- 51 files changed; ~280 line-level renames across user-facing docs (GLOSSARY, README, QUICKSTART, GENERATIONS, all of `docs/`, all 16 Routine prompts) plus internal specs (CLAUDE.md, SPEC.md, BUILD-INSTRUCTIONS.md, ADR-001, PROVISIONING-SPEC.md). State-variable renames in `installer/wizard.py` (`brain_repo_url` → `ledger_repo_url`, etc.) with a backward-compat migration shim so existing wizard state files don't lose progress.
- Kept as-is: `templates/brain/` folder (these are Curator-graph page templates), MANIFESTO.md Thesis 4 references (philosophical), Routine names like "R5 Brain Health Check" (proper names), Skill Pack S1 my-curator references (Curator-graph context).

### Other v1.0.1 items

**Documentation alignment with the actual Anthropic product surface:**
- "Anthropic Remote Routines" renamed to "Claude Code Routines" repo-wide (the actual product name; Anthropic launched the feature 14 April 2026). Old name preserved in v1.0.0 release notes for historical accuracy.
- Per-day Routine run limits documented: Pro 5, Max 15, Team 15, Enterprise 25. Plan-tier guidance added to quickstart and routines docs.

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
