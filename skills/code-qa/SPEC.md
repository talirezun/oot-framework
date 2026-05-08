# Skill Pack S4 — Code & QA: SPEC

**ID:** S4
**Name:** Code & QA
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

Operationalises the centaur model for software development in ØØT-native firms. Encodes Karpathy's Software 3.0 division of labour (spec / test / review human, implementation AI), the CLAUDE.md / AGENTS.md repo conventions, Plan Mode discipline, parallel-session orchestration, and the Klarna Test pre-merge gate.

The most opinionated coding-related Skill Pack the framework ships. Disagreement with these opinions is fine; the pack is overridable. But the defaults reflect the practice the framework's authors have found to work.

## Scope

**Covers:**
- CLAUDE.md / AGENTS.md authoring discipline at repo level.
- Plan Mode workflow (when to use, what a good plan looks like, plan-then-execute pattern).
- Parallel coding-session orchestration (multiple Claude Code or Augment Code sessions on related work).
- Three Philosophies pattern: Augment Code for big multi-file builds, Claude Code for daily development, Codex CLI for review/audit.
- Pre-merge checklist with Klarna Test gating on `ai-replaces-human` labelled PRs.
- Daily commit-summary Routine integration (R1 captures code outputs).
- Code review discipline when AI authored the code.
- AI-vs-human authorship attribution (`Co-authored-by:` trailers, rework-within-30-days tracking).
- The "Two Worlds of Code" cohort sorting in onboarding (Karpathy: vibe coders vs. agentic engineers).

**Does NOT cover:**
- Specific languages or frameworks (those live in language-specific sub-skills, optional add-ons).
- DevOps / CI/CD pipelines (the pack references but does not specify them).
- Security review workflows (that is a separate concern; counsel-adjacent).

## Allowed tools / dependencies

- Claude Code (primary).
- Augment Code, Codex CLI, Open Codex (optional alternatives per task).
- GitHub MCP.
- Curator MCP (architectural decisions written to Brain).
- The Compensation & Attribution Skill Pack (S3) — for Co-authored-by tracking.

## Section structure

1. **Purpose**
2. **When to invoke**
3. **When NOT to invoke**
4. **Operational instructions:**
   - 4.1 Repo orientation: CLAUDE.md, AGENTS.md, README structure.
   - 4.2 Plan Mode workflow (the discovery → plan → review → execute pattern).
   - 4.3 Parallel session orchestration.
   - 4.4 Three Philosophies — when to use which tool.
   - 4.5 Pre-merge checklist (linting, tests, review, Klarna Test gate if labelled).
   - 4.6 AI-authorship attribution (`Co-authored-by:` trailer convention).
   - 4.7 Architectural decision records — write to Brain, link from PR.
   - 4.8 Two Worlds of Code partner self-identification (referenced from onboarding).
5. **Brain interaction protocol** — writes architectural decisions, design docs, post-mortems.
6. **Excel interaction protocol** — none direct; output flows to X1 via R1.
7. **Routine integration** — R1 reads commits/PRs daily. R7 gates on `ai-replaces-human` PR label.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts

1. Don't merge a PR labelled `ai-replaces-human` without a Klarna Test score ≥14. Routine R7 enforces; do not bypass.
2. Don't skip the Plan stage on changes touching more than three files.
3. Don't attribute AI-generated code to a human author in commit messages — use `Co-authored-by: claude@anthropic` (or equivalent).
4. Don't run more than three parallel Claude Code sessions without explicit orchestration plan in the Brain.
5. Don't commit `.env` files, API keys, seeds, or any credential to git history. Bitwarden + environment variables, always.
6. Don't reject a PR solely because it was AI-authored; review the code on its merits.

## Worked examples concept

**Example 1:** A partner is starting a non-trivial feature. The pack walks them through Plan Mode: open a planning session, describe the goal, let Claude Code propose a plan, review the plan, commit the plan to the Brain, then execute. The execute phase happens in a separate session against the committed plan.

**Example 2:** A PR is opened that adds an AI Skill replacing a human partner's manual review process. The PR is auto-labelled `ai-replaces-human` (via repo convention; Phase 8 CI applies the label). Routine R7 detects, posts to founder + affected partner, opens a Klarna Test entry. The PR is blocked from merge until the Test scores ≥14.

## References

1. Karpathy, A. *Software 3.0* (Sequoia AI Ascent 2026).
2. Anthropic. *CLAUDE.md and AGENTS.md conventions documentation*.
3. Dr. Tali Režun. *Three Philosophies, One Goal: Augment Code, Claude Code, Codex CLI* (Medium, April 2026).
4. Forsgren, N. et al. *DORA Report 2025*.
5. METR. *RCT on AI tools and developer productivity* (2025).
6. ØØT `governance/KLARNA-TEST.md`.
7. ØØT Skill Pack S6 — Change Management (METR baseline integration).

## Acceptance criteria

Standard. Plus:
- Klarna Test integration is documented with the GitHub Action snippet.
- Plan Mode example is concrete (not abstract).
- The `Co-authored-by:` trailer convention is specified.
- 3+ worked examples in `examples/`.