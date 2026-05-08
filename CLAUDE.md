# CLAUDE.md — Repository orientation for Claude Code

This file orients Claude Code (and any other agentic coding assistant) when working in the ØØT framework repository.

## What this repository is

`oot-framework` — the canonical reference implementation of ØØT (Organisation of Tomorrow). It is a markdown-first framework for partner-run, AI-augmented organisations. It contains:

- The intellectual core (`MANIFESTO.md`) and technical specification (`SPEC.md`).
- 12 hand-built Skill Packs (in `skills/`).
- 9 pre-built Excel templates with formulas and Routine integration (in `templates/excel/`).
- 8 cloud Routines + 8 privacy-track equivalents (in `routines/`).
- 4 governance documents (in `governance/`).
- 12 plain-language user guides (in `docs/`, generated from `docs/SPEC.md`).
- Reference org examples (in `examples/`).
- Installer scripts for Cloud and Privacy tracks (in `installer/`).

## How this repository is built

The repository is **scaffolded by Claude Code** from a foundation kit of 16 canonical specification files (the files in this commit when you first clone). The foundation kit encodes the framework's design judgement; Claude Code generates the rest.

The foundation kit files are **authoritative**. If a generated file disagrees with a foundation kit file, the foundation kit wins.

Build order is specified in `BUILD-INSTRUCTIONS.md`. Read that file before starting any scaffolding work.

## Repository conventions

**Markdown is the universal substrate.** Every Skill Pack, every governance doc, every Routine prompt, every spec, every user guide is markdown with YAML frontmatter where applicable. No proprietary formats. No vendor-locked plugins.

**SKILL.md is the canonical Skill format.** Modelled on Anthropic Agent Skills + the My Curator skill. Each pack has:
- `SKILL.md` — the operational instructions
- `SPEC.md` — the design spec (input to SKILL.md generation)
- `examples/` — worked examples
- `references/` — citations
- `scripts/` — optional automation scripts

**AGENTS.md at the root.** Cross-vendor orientation. (CLAUDE.md is the Claude-specific equivalent; both should exist.)

**File naming.** Lowercase, hyphenated. `partner-output-ledger.xlsx`, not `Partner_Output_Ledger.xlsx`. Skill Pack folder names match this convention: `compensation-attribution/`, not `CompensationAttribution/`.

**The Brain is not in this repo.** This repo is the framework. The Brain is the firm's instance of the framework — created from this repo, but maintained separately. Examples in `examples/` show what a small Brain looks like.

**Excel files are generated, not authored.** `templates/excel/SPEC.md` is the authoritative source. Claude Code uses the xlsx skill to generate `.xlsx` files from the spec. Do not edit `.xlsx` files directly; edit the spec and regenerate.

## Coding conventions

**Python** for installer scripts and any glue code. Use `uv` for dependency management. Type hints required. Black for formatting. Ruff for linting.

**Bash / Zsh** for shell scripts. POSIX-compatible where possible. Set `set -euo pipefail` at the top.

**JSON / YAML** for configuration files. JSON for machine-generated configs (e.g., `mcp.json`); YAML for human-edited configs.

**No new dependencies without justification.** ØØT is a markdown framework, not a software framework. Code is glue, not the substance. If a Skill Pack needs a Python script, justify why a markdown-only approach is insufficient before adding code.

## When generating files from spec

The foundation kit's `SPEC.md` files (notably `templates/excel/SPEC.md`, `routines/SPEC.md`, and `skills/<pack>/SPEC.md`) are designed to be sufficient for generation without further design decisions. If you find yourself needing to make a design decision while generating a file, **stop and flag it** — do not silently invent a decision. The likely cause is a gap in the spec; the spec should be updated, then generation can proceed.

## When in doubt, paraphrasing the framework

The single best paraphrase of what ØØT is for: *a complete, opinionated, file-based framework for building and running an organisation in which the people producing value are paid for it as it lands, paid again as it compounds, and own a real stake in what they helped create — while the technical machinery underneath compounds the firm's intellectual property in lockstep.*

Every generated file should serve that mission. If a file you are generating does not — or worse, if it contradicts the Klarna Test, the Resistance thesis, or the partner-not-employee operating principle — pause and consult the spec.

## Tools you should expect to use

- The xlsx skill (Anthropic public skills, `/mnt/skills/public/xlsx/SKILL.md`) — for generating the 9 Excel templates from `templates/excel/SPEC.md`.
- The docx skill — for generating any Word-document templates (Partner Charter, sample contracts) from spec.
- The pdf skill — for any PDF generation.
- The frontend-design skill — if you build any web-based widgets (Lumina-style).
- The product-self-knowledge skill — for any reference to Anthropic's products in user-facing docs.

Always `view` the relevant SKILL.md before using any of these.

## What to commit

After each phase in `BUILD-INSTRUCTIONS.md`:

- Run the SKILL.md frontmatter linter (Phase 8 ships this).
- Run any Phase-specific tests.
- Commit with a message following the convention `<phase>: <what was built>`. Example: `phase-3: scaffold tier-1 skill packs (S1–S6, S12)`.
- Push to the working branch.

## When the user asks about the framework

The user is Dr. Tali Režun (the framework's initiator) or a collaborator. Treat questions about the framework's intellectual basis (theses, citations, edge cases) as substantive — they often reflect ongoing refinement. If a refinement contradicts the foundation kit, propose updating the foundation kit explicitly rather than diverging silently.