# AGENTS.md — Cross-vendor orientation for ØØT

This file orients **any AI agent** (Claude, Cursor, Cody, GitHub Copilot, OpenAI Codex, Gemini, OpenCode, Augment, Aider, LM Studio-hosted local models, or future agents working through Linux Foundation Agentic AI Foundation conventions) when working in the ØØT framework repository. (OpenCode is also the framework's own first-class **community-track** install harness — see `docs/internal/ADR-003-community-track-no-subscription.md`.)

It is the vendor-neutral counterpart to `CLAUDE.md`. Both files exist; both should be read; if your harness reads AGENTS.md preferentially, this is the file you want.

---

## What this repository is

`oot-framework` — the canonical reference implementation of **ØØT (Organisation of Tomorrow)**. A markdown-first framework for partner-run, AI-augmented organisations. Contents:

- The intellectual core (`MANIFESTO.md`) and technical specification (`SPEC.md`).
- 12 hand-built Skill Packs (`skills/` — 7 hardened S1–S6/S12, 5 scaffolded S7–S11).
- 9 pre-built Excel templates with formulas and Routine integration (`templates/excel/`; generated from `templates/excel/SPEC.md` by `scripts/build_excel.py`).
- 8 cloud Routines + 8 privacy-track equivalents (`routines/`).
- 4 governance documents (`governance/`).
- Plain-language user guides (`docs/`) + 6 UI walkthroughs (`docs/walkthroughs/`).
- Reference org examples (`examples/`; `small-org/` populated, others README-only).
- Installer for **three operating configurations** — cloud, privacy, and community — across three install paths: agent-assisted (Path A), Python wizard (Path B, `installer/wizard.py`), manual docs (Path C).
- A `pytest` suite (`tests/`) that CI runs as a hard gate.
- Research index and ecosystem references (`research/`).
- Architecture Decision Records (`docs/internal/ADR-001`…`ADR-005`) recording the load-bearing design decisions — read these before changing the Excel schema, the Ledger/Firm-Brain split, or the track model.

---

## How this repository is built

The repository is **scaffolded from a foundation kit of canonical specification files** by an AI coding agent (typically Claude Code, but the build is portable to any sufficiently capable agent). The foundation kit encodes the framework's design judgement; the agent generates the rest.

The foundation kit files are **authoritative**. If a generated file disagrees with a foundation kit file, the foundation kit wins.

Build order is specified in `BUILD-INSTRUCTIONS.md`. Read that file before starting any scaffolding work.

---

## Standards the framework rests on

ØØT is built on open standards governed by the **Linux Foundation Agentic AI Foundation (AAIF)** as of December 2025:

- **SKILL.md** — Anthropic Agent Skills format. Vendor-neutral; loadable into any MCP-compatible client.
- **AGENTS.md** (this file) — cross-vendor orientation file at the root of agent-readable repositories.
- **CLAUDE.md** — the Claude-specific equivalent; both should exist on any well-maintained agent-readable repo.
- **MCP (Model Context Protocol)** — the open standard for agent ↔ tool communication.
- **MCP server cards** — discoverable tool descriptions per the AAIF spec.

If you are an agent that does not natively understand one of these formats, prefer to use them anyway — they are the lingua franca of the 2026 agentic ecosystem.

---

## Repository conventions

**Markdown is the universal substrate.** Every Skill Pack, every governance doc, every Routine prompt, every spec, every user guide is markdown with YAML frontmatter where applicable. No proprietary formats. No vendor-locked plugins.

**SKILL.md is the canonical Skill format.** Modelled on Anthropic Agent Skills + the My Curator skill. Each pack has:
- `SKILL.md` — the operational instructions.
- `SPEC.md` — the design spec (input to SKILL.md generation).
- `examples/` — worked examples.
- `references/` — citations.
- `scripts/` — optional automation scripts.

**File naming.**
- **UPPERCASE** for top-level meta documents (`README.md`, `MANIFESTO.md`, `SPEC.md`, `GLOSSARY.md`, `QUICKSTART.md`, `GENERATIONS.md`, `CLAUDE.md`, `AGENTS.md`, `BUILD-INSTRUCTIONS.md`, `LICENSE`, `LICENSE-DOCS`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
- **UPPERCASE** for governance documents (`governance/KLARNA-TEST.md`, `EU-AI-ACT.md`, `DECISION-RIGHTS.md`, `SECRETS-POLICY.md`).
- **UPPERCASE** for per-pack `SPEC.md` and `SKILL.md` inside each Skill Pack folder.
- **lowercase-hyphenated** for folder names, asset files, brain page slugs, Excel templates (`skills/compensation-attribution/`, `partner-output-ledger.xlsx`, `firm/output-logs/2026-05-08.md`).
- **lowercase-numbered** for the Phase 7 user docs (`docs/00-quickstart-cloud.md`, `docs/01-installing-the-curator.md`, `docs/walkthroughs/W1-claude-desktop-tour.md`).

**The Brain is not in this repo.** This repo is the framework. The Brain is the firm's *instance* of the framework — created from this repo, but maintained separately. Examples in `examples/` show what a small Brain looks like.

**Excel files are generated, not authored.** `templates/excel/SPEC.md` is the authoritative source. The Phase 5 builder (a Python script using `openpyxl`) generates `.xlsx` files from the spec. Do not edit `.xlsx` files directly; edit the spec and regenerate.

---

## Coding conventions

- **Python** for installer scripts and any glue code. Use `uv` for dependency management. Type hints required. Black for formatting. Ruff for linting.
- **Bash / Zsh** for shell scripts. POSIX-compatible where possible. Set `set -euo pipefail` at the top.
- **JSON / YAML** for configuration files. JSON for machine-generated configs (e.g., `mcp.json`); YAML for human-edited configs.

**No new dependencies without justification.** ØØT is a markdown framework, not a software framework. Code is glue, not the substance. If a Skill Pack needs a Python script, justify why a markdown-only approach is insufficient before adding code.

---

## When generating files from spec

The foundation kit's `SPEC.md` files (notably `templates/excel/SPEC.md`, `routines/SPEC.md`, and `skills/<pack>/SPEC.md`) are designed to be sufficient for generation without further design decisions. If you find yourself needing to make a design decision while generating a file, **stop and flag it** — do not silently invent a decision. The likely cause is a gap in the spec; the spec should be updated, then generation can proceed.

---

## When in doubt, paraphrasing the framework

The single best paraphrase of what ØØT is for: *a complete, opinionated, file-based framework for building and running an organisation in which the people producing value are paid for it as it lands, paid again as it compounds, and own a real stake in what they helped create — while the technical machinery underneath compounds the firm's intellectual property in lockstep.*

Every generated file should serve that mission. If a file you are generating does not — or worse, if it contradicts the Klarna Test, the Resistance thesis, or the partner-not-employee operating principle — pause and consult the spec.

---

## Tools your harness should expect to use

If your agent platform supports MCP-compatible tools, the framework expects access to:

- **The xlsx skill or equivalent** (Anthropic public skill `/mnt/skills/public/xlsx/SKILL.md`, or any MCP server providing equivalent capability) — for generating the 9 Excel templates from `templates/excel/SPEC.md`.
- **The docx skill or equivalent** — for generating any Word-document templates (Partner Charter, sample contracts) from spec.
- **The pdf skill or equivalent** — for any PDF generation.
- **The Curator MCP** (`my-curator`) — for Brain operations.
- **GitHub MCP** — for repo and CI operations.
- **Filesystem MCP** (Desktop Commander or equivalent) — for local file access on the privacy track.

If your agent does not have one of these, document the substitution in your session and proceed; the framework is designed to tolerate substitution as long as the resulting artefact matches the spec.

---

## What to commit

The 10-phase scaffolding build (`BUILD-INSTRUCTIONS.md`) is complete; that file is now historical. For any change to the released framework:

- Run `python3 scripts/validate_skills.py` (must be 12/12) if any `SKILL.md` changed.
- Run `python3 scripts/build_excel.py` and verify the regenerated `.xlsx` if `templates/excel/SPEC.md` changed.
- Run `python3 -m pytest tests/ -q` (the CI hard gate; 51 tests covering the validator, `build_excel` structure incl. the ADR-004/005 schemas, and the installer wizard state machine).
- Run `lychee --offline --no-progress .` (0 errors) for doc changes.
- Commit with the convention `<phase|fix|feat>-<n>: <what>` (e.g. `fix-skill-s7: harden EU AI Act §4.1`) and the `Co-Authored-By:` trailer for AI-authored work.

---

## When the user asks about the framework

The user is **Dr. Tali Režun** (the framework's initiator) or a collaborator. Treat questions about the framework's intellectual basis (theses, citations, edge cases) as substantive — they often reflect ongoing refinement. If a refinement contradicts the foundation kit, propose updating the foundation kit explicitly rather than diverging silently.
