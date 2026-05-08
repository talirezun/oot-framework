# ØØT Foundation Kit — Master Manifest

**Status:** Foundation kit complete. Ready to hand to Claude Code for repository scaffolding.

**Initiator:** Dr. Tali Režun
**Repository target:** `https://github.com/talirezun/oot-framework`
**Generation:** 1.0.0
**Date:** 2026-05-08

---

## What's in the foundation kit (27 files total)

The foundation kit consists of canonical markdown specifications. Claude Code uses these to scaffold the full repository (filled-out SKILL.md files, .xlsx templates, Routine files, user docs, installers, reference org examples).

### Root-level files (8)

| File | Purpose | Source |
|---|---|---|
| `README.md` | Public face; 5-min tour; who it's for; the five theses | Batch 1 (inline) |
| `MANIFESTO.md` | The five theses in full with citations | Batch 1 (inline) |
| `SPEC.md` | Technical specification — eight-layer architecture; full Lego inventory | Batch 2 (inline) |
| `GLOSSARY.md` | Definitions of every non-obvious term | Batch 2 (inline) |
| `GENERATIONS.md` | Three-generation roadmap (Gen 1 / Gen 2 / Gen 3) | Batch 2 (inline) |
| `QUICKSTART.md` | Weekend setup path for both Cloud and Privacy tracks | Batch 3 (inline) |
| `CLAUDE.md` | Claude Code orientation for this repository | Batch 3 (inline) |
| `BUILD-INSTRUCTIONS.md` | Phased orders for Claude Code (10 phases) | Batch 3 (inline) |

### Governance files (4)

| File | Purpose | Source |
|---|---|---|
| `governance/KLARNA-TEST.md` | The signature epistemic check — narrative + 10-question rubric | Batch 4 (inline) |
| `governance/EU-AI-ACT.md` | Article-by-article mapping methodology | Batch 4 (inline) |
| `governance/DECISION-RIGHTS.md` | RACI-style matrix template + 3-tier dispute resolution | Batch 4 (inline) |
| `governance/SECRETS-POLICY.md` | Bitwarden + Trezor + Yubikey two-layer architecture | Batch 4 (inline) |

### Skills files (13)

| File | Purpose | Source |
|---|---|---|
| `skills/_TEMPLATE_SKILL.md` | Canonical SKILL.md structure (modelled on My Curator) | Batch 5 (inline) |
| `skills/my-curator/SPEC.md` | S1 — Tier 1 — imported verbatim from talirezun/the-curator | Batch 5 (inline) |
| `skills/context-engineering/SPEC.md` | S2 — Tier 1 — foundational meta-skill | Batch 5 (inline) |
| `skills/compensation-attribution/SPEC.md` | S3 — Tier 1 — most distinctive ØØT contribution | Batch 5 (inline) |
| `skills/code-qa/SPEC.md` | S4 — Tier 1 — Code QA + Klarna Test pre-merge gate | Batch 5 (inline) |
| `skills/reporting-business-review/SPEC.md` | S5 — Tier 1 — operational heartbeat | Batch 5 (inline) |
| `skills/change-management/SPEC.md` | S6 — Tier 1 — METR baseline + AI Champions | Batch 5 (inline) |
| `skills/privacy-self-sovereign/SPEC.md` | S12 — Tier 1 — 4thtech + PollinationX + LM Studio + Excel MCP | Batch 5 (inline) |
| `skills/governance-compliance/SPEC.md` | S7 — Tier 2 — scaffold | Batch 5 (inline) |
| `skills/legal-operations/SPEC.md` | S8 — Tier 2 — scaffold | Batch 5 (inline) |
| `skills/marketing/SPEC.md` | S9 — Tier 2 — scaffold | Batch 5 (inline) |
| `skills/finance-treasury/SPEC.md` | S10 — Tier 2 — scaffold | Batch 5 (inline) |
| `skills/sales-bd/SPEC.md` | S11 — Tier 2 — scaffold | Batch 5 (inline) |

### Templates and Routines (3)

| File | Purpose | Source |
|---|---|---|
| `templates/excel/SPEC.md` | Schemas, formulas, sheet structure for 9 .xlsx files | **Batch 6 (this bundle, on disk)** |
| `routines/SPEC.md` | 8 cloud Routines + 8 privacy-track equivalents | **Batch 6 (this bundle, on disk)** |
| `docs/SPEC.md` | Generation instructions for the 12 plain-language user guides | **Batch 6 (this bundle, on disk)** |

---

## How to assemble the bundle

This master manifest, plus the three Batch 6 SPEC files, are on disk in this download. The other 24 files were delivered as inline markdown code blocks in Batches 1–5 of the conversation that produced this kit.

**Assembly procedure:**

1. Create a folder locally: `oot-foundation-kit/`.
2. Reproduce the directory structure:

```
oot-foundation-kit/
├── README.md
├── MANIFESTO.md
├── SPEC.md
├── GLOSSARY.md
├── QUICKSTART.md
├── GENERATIONS.md
├── CLAUDE.md
├── BUILD-INSTRUCTIONS.md
├── MANIFEST.md                          ← this file (on disk)
├── governance/
│   ├── KLARNA-TEST.md
│   ├── EU-AI-ACT.md
│   ├── DECISION-RIGHTS.md
│   └── SECRETS-POLICY.md
├── skills/
│   ├── _TEMPLATE_SKILL.md
│   ├── my-curator/SPEC.md
│   ├── context-engineering/SPEC.md
│   ├── compensation-attribution/SPEC.md
│   ├── code-qa/SPEC.md
│   ├── reporting-business-review/SPEC.md
│   ├── change-management/SPEC.md
│   ├── privacy-self-sovereign/SPEC.md
│   ├── governance-compliance/SPEC.md
│   ├── legal-operations/SPEC.md
│   ├── marketing/SPEC.md
│   ├── finance-treasury/SPEC.md
│   └── sales-bd/SPEC.md
├── templates/
│   └── excel/SPEC.md                    ← on disk (Batch 6)
├── routines/SPEC.md                     ← on disk (Batch 6)
└── docs/SPEC.md                         ← on disk (Batch 6)
```

3. For each Batch 1–5 file, copy the inline content from the chat into the corresponding file path. The conversation labels each file clearly with its target path (e.g., `## File 1: README.md`).
4. The Batch 6 files (`templates/excel/SPEC.md`, `routines/SPEC.md`, `docs/SPEC.md`, and this `MANIFEST.md`) are downloaded directly from the bundle.

Once assembled, the foundation kit is roughly **45,000–50,000 words of structured specification** across 27 files.

---

## How to hand off to Claude Code

Once the bundle is assembled locally, the handoff to Claude Code is a single command sequence:

### Step 1 — Initialise the GitHub repository

```bash
# At github.com/talirezun/oot-framework, the repo already exists
git clone https://github.com/talirezun/oot-framework.git
cd oot-framework
```

### Step 2 — Copy the foundation kit into the repo

```bash
cp -r /path/to/oot-foundation-kit/. ./
git add .
git commit -m "phase-0: import foundation kit"
git push
```

### Step 3 — Open Claude Code in the repo and issue the build order

In Claude Code:

```
Read the entire foundation kit, starting with CLAUDE.md and BUILD-INSTRUCTIONS.md. Then execute Phase 1 of BUILD-INSTRUCTIONS.md. Stop at the end of Phase 1 and confirm before proceeding to Phase 2.
```

Claude Code will:

1. Read the orientation files.
2. Execute Phase 1 (directory structure, `AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `LICENSE-DOCS`).
3. Commit Phase 1.
4. Wait for your confirmation.

You then say `proceed with Phase 2` and so on through Phase 10.

### The 10 phases (per `BUILD-INSTRUCTIONS.md`)

1. **Phase 1** — Repository structure + licensing.
2. **Phase 2** — Validate skill template and Tier-1 SPECs.
3. **Phase 3** — Generate Tier-1 Skill Packs (S1, S2, S3, S4, S5, S6, S12).
4. **Phase 4** — Scaffold Tier-2 packs + partner-onboarding templates.
5. **Phase 5** — Generate 9 Excel templates.
6. **Phase 6** — Generate 8 cloud Routines + 8 privacy equivalents.
7. **Phase 7** — Generate 12 plain-language user docs.
8. **Phase 8** — CI, frontmatter linting, validation.
9. **Phase 9** — Installers + 3 reference org examples.
10. **Phase 10** — Final review and v1.0.0 release.

Total estimated Claude Code time: **20–40 hours of agent-driven work** (depending on how often the user approves vs. iterates). Most of this is unattended.

---

## What Claude Code generates (from the foundation kit)

This is what the foundation kit doesn't contain — Claude Code produces it during the 10 phases:

- **Filled-out `SKILL.md` files** for the 7 Tier-1 packs and scaffolds for the 5 Tier-2 packs (Phase 3, 4).
- **9 `.xlsx` files** with formulas, named ranges, and seeded sample data (Phase 5).
- **16 Routine markdown files** (8 cloud + 8 privacy) with prompts and trigger configurations (Phase 6).
- **12 plain-language user guides** (Phase 7).
- **CI workflows** for SKILL.md frontmatter validation, markdown linting, link checking, Excel validation (Phase 8).
- **Cloud and Privacy installers** — one-command quickstart scripts (Phase 9).
- **3 reference org examples** — small (3 partners), medium (12 partners), regulated-EU (6 partners with full EU AI Act mapping) (Phase 9).
- **`AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`** at root (Phase 1).
- **`LICENSE` (Apache 2.0) and `LICENSE-DOCS` (CC BY-SA 4.0)** (Phase 1).
- **GitHub Actions CI** (Phase 8).
- **Tests** for SKILL.md frontmatter validity and Excel formula evaluation (Phase 8).

---

## Critical decisions encoded in the foundation kit

Decisions made during foundation-kit development that are now baked into the framework:

1. **ØØT — Organisation of Tomorrow** (canonical name). Tagline: "An open framework for partner-run, AI-augmented organisations."
2. **Repository:** `oot-framework` (ASCII-friendly).
3. **License:** Apache 2.0 (code) + CC BY-SA 4.0 (docs/Skills).
4. **Resistance leads** the five theses (most empirically grounded, where comparable frameworks fail).
5. **Three generations explicit:** Gen 1 = today; Gen 2 = 6–12 months (crypto rails, Unit Fund); Gen 3 = 12–24 months theoretical (Cotrugli Ledger, autonomous agents).
6. **Klarna Test** is the signature epistemic check. Threshold ≥14/20 (70%). Wired into Code & QA via PR label `ai-replaces-human` triggering Routine R7.
7. **12 Skill Packs total:** 7 Tier-1 hardened (S1, S2, S3, S4, S5, S6, S12) + 5 Tier-2 scaffolded (S7, S8, S9, S10, S11).
8. **9 Excel templates** with X8 (Treasury Runway) optional and X9 (ØØT-readiness assessment) added.
9. **8 scheduled Routines** with R8 optional.
10. **Two parallel tracks at full Gen 1 parity:** Cloud (Anthropic Remote Routines) and Privacy (4thtech + PollinationX + LM Studio + Excel MCP `haris-musa/excel-mcp-server` + OS-native scheduling).
11. **Secrets architecture:** Bitwarden (passwords/tokens) + Trezor (crypto signing) + Yubikey (org admin). Two-layer; both required.
12. **Cotrugli Ledger** anchored as Gen 3 theoretical destination (co-author: Dražen Kapusta).
13. **Cloud-first canonical, privacy track real** — privacy track is at parity, not lip service.
14. **Founders:** Dr. Tali Režun (initiator); Dražen Kapusta + COTRUGLI Business School (founding contributors).
15. **Curator pay-as-you-go honesty:** free tier for tasting only; heavy usage <€10/month on Gemini Flash Lite or Anthropic.
16. **n8n mentioned not recommended** — Claude Routines + Excel + cron cover ~80% of v1 needs.
17. **Klarna Test rubric:** 10 questions, scored 0/1/2 each; threshold ≥14/20 (70%); legacy framing ≥7/10 also valid.

---

## What's intentionally not in the foundation kit

- **No legal advice.** The framework points at the eleven legal touchpoints (`docs/06-when-to-call-a-lawyer.md`); local counsel is mandatory.
- **No financial advice.** Treasury and compensation guidance is structural, not advisory.
- **No vendor commitments.** Markdown + open standards. ØØT works on Claude, Cursor, LM Studio, ChatGPT, any MCP-compatible client.
- **No proprietary formats.** Everything is markdown, .xlsx, .pdf, or .json. Survives any single vendor's roadmap.
- **No marketing language.** The MANIFESTO has citations and honesty clauses, not slogans.

---

## Generation 2 and Generation 3 readiness

The foundation kit is forward-compatible with Gen 2 and Gen 3:

- **Gen 2 hooks** present in: reward-species-declaration.xlsx (stablecoin upgrade pref + Unit Fund interest fields exist but locked), Compensation & Attribution Skill Pack (seven-layer structure with Gen 1/2/3 markers), Finance & Treasury Skill Pack (FIAT / stablecoin upgrade path documented), GENERATIONS.md (full Gen 2 scope).
- **Gen 3 hooks** present in: Cotrugli Ledger references throughout (theoretical, opt-in), Decision Rights matrix (PAC-RO co-signature integration noted), GENERATIONS.md (full Gen 3 scope).

Gen 1 adopters never need to discard work to upgrade. Reward-species declarations port forward; output ledgers port forward; Skill Packs port forward; Excel templates upgrade with new sheets, not new files.

---

## Final note from the framework's authors

The foundation kit reflects roughly two months of design dialogue between Dr. Tali Režun and Claude across multiple conversations. The framework draws on:

- Seven years of practitioner experience in 4thtech (on-chain communication), PollinationX (decentralised storage), Lumina AI (RAG widgets), Block Labs, Immu3, Online Guerrilla.
- The Cotrugli Ledger work (with Dražen Kapusta, Matjaž Gams, Domen Brčić — published in International Leadership Journal).
- Peer-reviewed research and industry reports cited throughout (MIT NANDA, Microsoft Frontier Firm, METR, HBS Cybernetic Teammate, DORA 2025, Karpathy Software 3.0, Levin & Tadelis, Nonaka & Takeuchi, Hope & Fraser, Weitzman).
- The YOLO Investments thesis on output-based compensation.
- The framework's own Klarna Test discipline applied recursively to its own design decisions.

The framework is a living document. Generation 1 ships now. Generation 2 lands when the legal scoping for crypto rails and the Unit Fund completes in target jurisdictions. Generation 3 lands when the Cotrugli Ledger is field-validated and autonomous agent business units are mature.

What ØØT believes — at the level of theses, at the level of operational discipline, at the level of file formats — is in this foundation kit. The rest is execution.

— ØØT v1.0.0, 8 May 2026.