# BUILD-INSTRUCTIONS.md — Phased orders for Claude Code

This file is the script Claude Code follows to scaffold the ØØT framework repository from the foundation kit. Read it once end-to-end before starting; then execute phase by phase, committing at each phase boundary.

**Pre-requisites before starting:**

- The foundation kit is committed at the repository root (this commit).
- You have read `MANIFESTO.md`, `SPEC.md`, `GLOSSARY.md`, and `CLAUDE.md`.
- You have access to the xlsx, docx, pdf, and frontend-design skills.
- You are working on a feature branch, not main.

**General principles:**

- Commit at the end of every phase. Each commit message is `phase-<n>: <what was built>`.
- Run `phase-8` validators after every phase that ships SKILL.md files.
- If the spec is ambiguous or you encounter a design decision not covered by the foundation kit, **stop and flag it**. Do not silently invent decisions.
- Do not generate Excel files until Phase 5. Do not generate Routines until Phase 6. Order matters.

---

## Phase 1 — Repository structure

**Goal:** Create the full directory tree per the SPEC's Layer 8.

**Tasks:**

1. Create the following directory structure:

```
oot-framework/
├── README.md                         (foundation kit)
├── MANIFESTO.md                      (foundation kit)
├── SPEC.md                           (foundation kit)
├── GLOSSARY.md                       (foundation kit)
├── QUICKSTART.md                     (foundation kit)
├── GENERATIONS.md                    (foundation kit)
├── CLAUDE.md                         (foundation kit)
├── AGENTS.md                         (Phase 1 — generate)
├── BUILD-INSTRUCTIONS.md             (foundation kit)
├── CONTRIBUTING.md                   (Phase 1 — generate)
├── CODE_OF_CONDUCT.md                (Phase 1 — generate)
├── LICENSE                           (Phase 1 — Apache 2.0)
├── LICENSE-DOCS                      (Phase 1 — CC BY-SA 4.0)
├── governance/
│   ├── KLARNA-TEST.md                (foundation kit)
│   ├── EU-AI-ACT.md                  (foundation kit)
│   ├── DECISION-RIGHTS.md            (foundation kit)
│   └── SECRETS-POLICY.md             (foundation kit)
├── skills/
│   ├── _TEMPLATE_SKILL.md            (foundation kit)
│   ├── my-curator/
│   ├── context-engineering/
│   ├── compensation-attribution/
│   ├── code-qa/
│   ├── reporting-business-review/
│   ├── change-management/
│   ├── privacy-self-sovereign/
│   ├── governance-compliance/
│   ├── legal-operations/
│   ├── marketing/
│   ├── finance-treasury/
│   └── sales-bd/
│       ├── SPEC.md                   (foundation kit, 12 of these)
│       ├── SKILL.md                  (Phase 3 — generate from SPEC)
│       ├── examples/                 (Phase 3 — generate)
│       └── references/               (Phase 3 — generate)
├── templates/
│   ├── excel/
│   │   ├── SPEC.md                   (foundation kit)
│   │   ├── partner-output-ledger.xlsx        (Phase 5 — generate)
│   │   ├── reward-species-declaration.xlsx   (Phase 5)
│   │   ├── business-review.xlsx              (Phase 5)
│   │   ├── klarna-test.xlsx                  (Phase 5)
│   │   ├── metr-baseline.xlsx                (Phase 5)
│   │   ├── agent-skill-roi.xlsx              (Phase 5)
│   │   ├── eu-ai-act-mapping.xlsx            (Phase 5)
│   │   ├── treasury-runway.xlsx              (Phase 5, optional)
│   │   └── oot-readiness.xlsx                (Phase 5)
│   ├── brain/
│   │   ├── FIRM-ONTOLOGY.md          (foundation kit — Brain folder structure + permissions)
│   │   ├── SPEC.md                   (foundation kit — Brain page template specifications)
│   │   ├── daily-output-log.md       (Phase 4 — generate)
│   │   ├── audit-log-day.md          (Phase 4)
│   │   ├── business-review.md        (Phase 4)
│   │   ├── klarna-test-page.md       (Phase 4)
│   │   ├── variable-statement.md     (Phase 4)
│   │   ├── long-tail-statement.md    (Phase 4)
│   │   ├── output-spec.md            (Phase 4)
│   │   ├── partner-profile.md        (Phase 4)
│   │   ├── reward-species-declaration-summary.md (Phase 4)
│   │   ├── decision-record.md        (Phase 4)
│   │   ├── adr.md                    (Phase 4)
│   │   ├── pilot-summary.md          (Phase 4)
│   │   ├── dispute-record.md         (Phase 4)
│   │   └── prompt-artefact.md        (Phase 4)
│   ├── partner-charter.md            (Phase 4 — generate)
│   ├── output-spec.md                (Phase 4 — generate, partner-onboarding tutorial copy)
│   └── partner-onboarding/
│       ├── PROVISIONING-SPEC.md      (foundation kit)
│       ├── checklist.md              (Phase 4 — generate)
│       ├── provisioning-script.sh    (Phase 4 — generate per PROVISIONING-SPEC.md)
│       └── first-90-days.md          (Phase 4 — generate)
├── routines/
│   ├── SPEC.md                       (foundation kit)
│   ├── cloud/                        (Phase 6 — 8 .md files)
│   └── privacy/                      (Phase 6 — 8 .md files)
├── docs/
│   ├── SPEC.md                       (foundation kit)
│   ├── 00-quickstart-cloud.md        (Phase 7 — generate from SPEC)
│   ├── 00-quickstart-privacy.md      (Phase 7)
│   ├── 01-installing-the-curator.md  (Phase 7)
│   ├── 02-installing-routines.md     (Phase 7)
│   ├── 02-installing-routines-privacy.md (Phase 7)
│   ├── 03-onboarding-a-partner.md    (Phase 7)
│   ├── 04-running-the-business-review.md (Phase 7)
│   ├── 05-using-the-klarna-test.md   (Phase 7)
│   ├── 06-when-to-call-a-lawyer.md   (Phase 7)
│   ├── 07-troubleshooting.md         (Phase 7)
│   ├── 08-faq.md                     (Phase 7)
│   ├── glossary.md                   (Phase 7 — alias of /GLOSSARY.md)
│   └── walkthroughs/                 (Phase 7 — Tier 2 UI walkthroughs)
│       ├── W1-claude-desktop-tour.md
│       ├── W2-curator-daily-use.md
│       ├── W3-excel-monthly-variable-pay.md
│       ├── W4-running-the-friday-business-review.md
│       ├── W5-running-a-klarna-test.md
│       └── W6-monitoring-routines-dashboard.md
├── installer/
│   ├── cloud/                        (Phase 9 — generate)
│   └── privacy/                      (Phase 9 — generate)
├── examples/
│   ├── SPEC.md                       (foundation kit — reference org specifications)
│   ├── small-org/                    (Phase 9 — generate per SPEC)
│   ├── medium-org/                   (Phase 9)
│   └── regulated-eu-org/             (Phase 9)
└── .github/
    └── workflows/                    (Phase 8 — CI)
```

2. Generate `AGENTS.md` — cross-vendor orientation. Should mirror `CLAUDE.md` but be agent-agnostic. ~500 words.
3. Generate `CONTRIBUTING.md` — how to contribute. Reference Apache 2.0 / CC BY-SA 4.0 split. List initiator + founding contributors per `README.md`. ~500 words.
4. Generate `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1, adapted. ~400 words.
5. Generate `LICENSE` — Apache 2.0 boilerplate.
6. Generate `LICENSE-DOCS` — CC BY-SA 4.0 boilerplate.

**Acceptance criteria:** Directory tree matches the spec. All 6 generated files committed. Foundation kit files unmodified.

**Commit message:** `phase-1: scaffold repository structure and licensing`

---

## Phase 2 — Skill template + Tier-1 Skill Pack SPECs review

**Goal:** Review and validate the foundation kit's `_TEMPLATE_SKILL.md` and the 7 Tier-1 SPECs (S1, S2, S3, S4, S5, S6, S12).

**Tasks:**

1. Read `skills/_TEMPLATE_SKILL.md`. Confirm structure matches the My Curator skill canonical pattern (frontmatter manifest, numbered sections, "don'ts" list, quick reference).
2. For each Tier-1 SPEC, read it and confirm:
   - Scope is clearly defined.
   - Allowed tools are listed.
   - Section structure is specified.
   - References (citations) are present.
   - At least one worked example concept is sketched.
3. If any SPEC is incomplete or self-contradictory, **stop and flag**.

**Acceptance criteria:** All 7 Tier-1 SPECs read and confirmed coherent. Any flags raised.

**Commit message:** `phase-2: validate skill template and tier-1 specs`

---

## Phase 3 — Generate Tier-1 Skill Packs

**Goal:** Generate the full SKILL.md for each Tier-1 pack from its SPEC.md.

**Tasks for each pack (S1, S2, S3, S4, S5, S6, S12):**

1. Read the pack's `SPEC.md`.
2. Read `skills/_TEMPLATE_SKILL.md` for the structure.
3. Generate `skills/<pack>/SKILL.md`. Follow the template structure exactly. Substantive content per the SPEC. Aim for ~2000–3500 words per pack.
4. Generate `skills/<pack>/examples/` with at least 2 worked examples per pack. Each example is a markdown file showing a realistic use case.
5. Generate `skills/<pack>/references/` with a `README.md` listing the citations from the SPEC.

**Special handling:**

- **S1 (My Curator):** Do not generate from scratch. Import the canonical SKILL.md from `https://github.com/talirezun/the-curator/blob/main/claude-skills/my-curator/SKILL.md` verbatim. Add an ØØT-specific preamble noting it is the canonical Brain Skill Pack in this framework.
- **S3 (Compensation & Attribution):** This is the most distinctive ØØT contribution. The SKILL.md must be substantive — aim for ~3500 words. Cover the seven-layer compensation picture explicitly, marked Gen 1 vs. Gen 2 vs. Gen 3.
- **S4 (Code & QA):** Wire the Klarna Test gate into the pre-merge checklist. Include the GitHub Action snippet for triggering Routine R7 on PRs labelled `ai-replaces-human`.
- **S12 (Privacy / Self-Sovereign):** Orchestrates 4thtech + PollinationX + LM Studio + Excel MCP + Desktop Commander. The pack must function as a "how to wire these together" guide.

**Acceptance criteria:** 7 SKILL.md files committed, each passing the Phase 8 frontmatter linter. Each pack has examples/ and references/.

**Commit message:** `phase-3: generate tier-1 skill packs (S1, S2, S3, S4, S5, S6, S12)`

---

## Phase 4 — Generate Tier-2 Skill Pack scaffolds + supporting templates + Brain page templates

**Goal:** Scaffold the 5 Tier-2 packs (frontmatter + section structure + TODOs only — not full content). Generate the partner-onboarding markdown templates. Generate the Brain page templates per `templates/brain/SPEC.md`.

**Tasks:**

1. For each Tier-2 pack (S7, S8, S9, S10, S11):
   - Read the pack's `SPEC.md`.
   - Generate a scaffolded `skills/<pack>/SKILL.md` with frontmatter, section headings, and `<!-- TODO: ... -->` markers for substantive content. Include the citations from the SPEC.
   - Aim for ~600–900 words per scaffold.
2. Generate `templates/partner-charter.md` — markdown template for the Partner Charter. References the reward-species declaration, the output spec, the cohort designation. ~800 words template + commentary.
3. Generate `templates/output-spec.md` — partner-onboarding tutorial version (a more annotated copy of `templates/brain/output-spec.md`).
4. Generate `templates/partner-onboarding/` directory with:
   - `checklist.md` — 30-step onboarding checklist.
   - `provisioning-script.sh` — bash script that creates the partner's Bitwarden vault entry, GitHub access, Slack invite, Brain folder. **Must follow `templates/partner-onboarding/PROVISIONING-SPEC.md` exactly** — Phase 4's PR is reviewed against that spec.
   - `first-90-days.md` — week-by-week onboarding plan.
5. Generate the 14 Brain page templates per `templates/brain/SPEC.md` (`daily-output-log.md`, `audit-log-day.md`, `business-review.md`, `klarna-test-page.md`, `variable-statement.md`, `long-tail-statement.md`, `output-spec.md`, `partner-profile.md`, `reward-species-declaration-summary.md`, `decision-record.md`, `adr.md`, `pilot-summary.md`, `dispute-record.md`, `prompt-artefact.md`).

**Acceptance criteria:** 5 Tier-2 SKILL.md scaffolds + 14 Brain page templates + 3 partner-onboarding files committed. The provisioning-script.sh validates against PROVISIONING-SPEC.md.

**Commit message:** `phase-4: scaffold tier-2 skill packs, partner-onboarding templates, and Brain page templates`

---

## Phase 5 — Generate Excel templates

**Goal:** Generate all 9 `.xlsx` files from `templates/excel/SPEC.md` using the xlsx skill.

**Tasks:**

1. Read `/mnt/skills/public/xlsx/SKILL.md` to confirm the xlsx skill's conventions and capabilities.
2. Read `templates/excel/SPEC.md` end to end.
3. For each of the 9 templates (X1–X9), generate the `.xlsx` file per the spec:
   - Sheets in the specified order.
   - Named ranges as specified.
   - Formulas exactly as specified (do not "improve" them).
   - Conditional formatting as specified.
   - README sheet at the end of every workbook explaining the file's purpose, the Routines that read/write it, and the human review cadence.
4. Save to `templates/excel/<filename>.xlsx`.
5. After generation, open each file via the xlsx skill's read tools and verify:
   - All sheets present.
   - Named ranges resolve.
   - Formulas evaluate without error on the seeded sample data.
6. If any file fails verification, stop and flag.

**Acceptance criteria:** 9 `.xlsx` files committed, all passing post-generation verification.

**Commit message:** `phase-5: generate excel templates (X1-X9)`

---

## Phase 6 — Generate Routine prompts

**Goal:** Generate the 8 cloud Routines + 8 privacy-track equivalents from `routines/SPEC.md`.

**Tasks:**

1. Read `routines/SPEC.md`.
2. For each of the 8 Routines (R1–R8):
   - Generate `routines/cloud/<routine-id>.md` — the Anthropic Remote Routine prompt, including trigger configuration, prompt body, expected outputs.
   - Generate `routines/privacy/<routine-id>.md` — the equivalent for OS-native scheduling: cron / launchd / Task Scheduler invocation, `llmster` command line, prompt body for headless LM Studio.
3. Add a `routines/README.md` summarising the 16 files and the install procedure for each track.

**Acceptance criteria:** 16 Routine markdown files + README committed.

**Commit message:** `phase-6: generate cloud routines and privacy-track equivalents`

---

## Phase 7 — Generate user documentation from docs/SPEC.md (18 docs)

**Goal:** Generate the 12 Tier-1 plain-language guides + 6 Tier-2 UI walkthroughs per `docs/SPEC.md`.

**Tasks:**

1. Read `docs/SPEC.md` end-to-end. The spec specifies, per doc: audience, purpose, structure, required sections, what to reference from elsewhere in the repo. **Note especially the "Documentation philosophy — write for the non-technical partner first" section** — every Tier-1 doc that involves a UI tool follows the three-layer pattern (orientation → walkthrough → pitfalls), and every Tier-2 walkthrough is screenshot-rich and assumes no shell-command literacy.
2. **Tier 1 — generate the 12 docs in `docs/`:** `00-quickstart-cloud.md`, `00-quickstart-privacy.md`, `01-installing-the-curator.md`, `02-installing-routines.md`, `02-installing-routines-privacy.md`, `03-onboarding-a-partner.md`, `04-running-the-business-review.md`, `05-using-the-klarna-test.md`, `06-when-to-call-a-lawyer.md`, `07-troubleshooting.md`, `08-faq.md`, `glossary.md`.
3. **Tier 2 — generate the 6 walkthroughs in `docs/walkthroughs/`:** `W1-claude-desktop-tour.md`, `W2-curator-daily-use.md`, `W3-excel-monthly-variable-pay.md`, `W4-running-the-friday-business-review.md`, `W5-running-a-klarna-test.md`, `W6-monitoring-routines-dashboard.md`.
4. Every doc with UI steps shows both Microsoft Excel and Google Sheets variants where they diverge, and both cloud-track and privacy-track variants where the underlying tool differs.
5. Every screenshot placeholder is in the form `![Description](images/<doc-id>-<step-number>.png)` with descriptive alt-text and an italic caption underneath that tells the reader what to look for. The actual image binaries are added in a follow-up PR (one PR per doc).
6. Cross-reference correctly — each doc should link to the relevant SPEC files, Skill Packs, Excel templates, and other docs.

**Acceptance criteria:** 18 doc files committed. Cross-references resolve. Tier-1 quickstarts are ≥4,500 words; Tier-2 walkthroughs are 1,500–3,000 words. Every Tier-1 doc that involves a UI tool follows the three-layer pattern.

**Commit message:** `phase-7: generate plain-language user documentation (12 Tier-1 + 6 Tier-2 walkthroughs)`

---

## Phase 8 — CI, linting, and validation

**Goal:** Set up GitHub Actions, frontmatter validation, and link checking.

**Tasks:**

1. Generate `.github/workflows/lint-skills.yml` — runs on every PR; validates SKILL.md frontmatter against the canonical schema (defined in `_TEMPLATE_SKILL.md`).
2. Generate `.github/workflows/markdown-lint.yml` — runs markdownlint and link checker.
3. Generate `.github/workflows/excel-validation.yml` — opens each `.xlsx` file and verifies named ranges resolve.
4. Generate a small Python script `scripts/validate-skills.py` that the workflow uses.
5. Run all workflows locally; fix any issues that surface.

**Acceptance criteria:** All workflows pass on the current commit. Any issues found are fixed.

**Commit message:** `phase-8: ci, frontmatter linting, link checking, excel validation`

---

## Phase 9 — Installers and reference org examples

**Goal:** Generate the one-command quickstart installers for both tracks, plus three reference org examples.

**Tasks:**

1. **Cloud installer (`installer/cloud/install.sh`):** Bash script that prompts the user for their Anthropic API key, GitHub token, Slack webhook, Google credentials path; clones the framework; sets up Bitwarden integration; configures the Curator; installs the 4 immediately-active Routines (R1, R2, R5, R6).
2. **Privacy installer (`installer/privacy/install.sh`):** Bash script that prompts for Trezor wallet address, GitHub token, PollinationX storage capacity NFT, 4thtech wallet; sets up LM Studio + Qwen 3; configures local cron jobs for the 4 immediately-active Routines.
3. **Reference org `examples/small-org/`:** A 3-partner org. Skeleton Brain with 10 sample documents. Reward Species Declarations for each partner. One filled-in `partner-output-ledger.xlsx` showing two months of operation.
4. **Reference org `examples/medium-org/`:** A 12-partner org. Cohort mix (5 full-time, 4 project specialists, 3 advisors). Filled-in business review sheets showing one full quarter.
5. **Reference org `examples/regulated-eu-org/`:** A 6-partner EU-based org with the EU AI Act mapping fully populated, daily audit trail samples, a worked Klarna Test scoring example.

**Acceptance criteria:** Installers run end-to-end on a fresh machine. Reference orgs are coherent and reviewed for realism.

**Commit message:** `phase-9: cloud and privacy installers, reference org examples`

---

## Phase 10 — Final review and release

**Goal:** Comprehensive review, then merge to main and tag v1.0.0.

**Tasks:**

1. Run all CI workflows. Confirm green.
2. Read the entire repository as a new founder would. Note any rough edges.
3. Check every Skill Pack opens cleanly in Claude Desktop (load each SKILL.md as a Project Document, run the example prompts).
4. Check every Excel template opens in both Microsoft Excel and Google Sheets without errors.
5. Verify the cloud installer works on a fresh machine (or a clean VM).
6. Tag `v1.0.0` and create a GitHub Release with the README's "What's in the box" section as the release notes.

**Acceptance criteria:** All checks pass. Tagged release published.

**Commit message:** `phase-10: v1.0.0 release`

---

## When to escalate

If any of the following happen during the build, **stop and consult the user (Dr. Tali Režun) before proceeding:**

- A SPEC is internally contradictory.
- A SPEC requires a design decision (e.g., a tool choice between two valid options) and the foundation kit does not specify.
- Generation of a file diverges materially from the spec (e.g., the xlsx skill cannot implement a specified formula).
- A citation in a SPEC is incorrect or outdated.
- An external dependency (an MCP server, a tool referenced in the SPEC) has changed materially since the foundation kit was written.

The framework's authority lives in the foundation kit. Drifting from it silently is the single biggest risk during scaffolding.