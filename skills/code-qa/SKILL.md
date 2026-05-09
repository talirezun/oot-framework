---
name: code-qa
description: Use whenever the partner is starting a non-trivial feature (Plan Mode), reviewing a PR (especially one labelled `ai-replaces-human`), choosing among Augment Code / Claude Code / Codex CLI for a task, writing or updating CLAUDE.md / AGENTS.md in a product repo, configuring repo-level protections, or onboarding an engineering partner (Two Worlds of Code self-id). Activates for "plan this feature", "review this PR", "which tool should I use for this refactor", "set up the Klarna gate on this repo", "this PR removes the manual review step — should we Klarna-test it?", "what's the auto-labeller looking for". Enforces the discovery → plan → review → execute → verify → PR workflow, the `Co-authored-by:` trailer convention, the five repo-level setup pre-requisites (oot/klarna-test status check, force-push-disabled, signed commits, audit-log reviewer rule, auto-labeller), and the Klarna Test pre-merge gate.
version: 1.0.0
tier: 1
status: hardened
allowed_tools:
  - mcp__github__create_pull_request
  - mcp__github__list_commits
  - mcp__github__get_pull_request
  - mcp__github__create_or_update_file
  - mcp__github__create_branch
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__search_wiki
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S4
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1, S2, S3]
oot_provides_to: [S6]
oot_klarna_test: true  # Wires the gate via .github/workflows/klarna-gate.yml + the auto-labeller
last_updated: 2026-05-08
---

# Code & QA

> **Generation marker:** Hardened in v1.0.
> **Klarna Test interaction:** **YES** — this pack wires the pre-merge gate via the `oot/klarna-test` GitHub status check and the `ai-replaces-human` auto-labeller.
> **Brain interaction:** Both — reads ADRs and prior plans; writes architectural decisions, plans, post-mortems.

## 1. Purpose

Operationalises the centaur model for software development in ØØT-native firms. Encodes Karpathy's Software 3.0 division of labour (spec / test / review human, implementation AI), the CLAUDE.md / AGENTS.md repo conventions, Plan Mode discipline, parallel-session orchestration, and the **Klarna Test pre-merge gate**.

The most opinionated coding-related Skill Pack the framework ships. The defaults reflect the practice the framework's authors have found to work; disagreement with them is fine but should be deliberate (an ADR, not silent drift).

## 2. When to invoke this pack

1. **Starting a non-trivial feature** — Plan Mode workflow.
2. **Reviewing a PR** — especially one labelled `ai-replaces-human`.
3. **Choosing among Augment Code / Claude Code / Codex CLI** for a task.
4. **Writing or updating CLAUDE.md / AGENTS.md** in a product repo.
5. **Configuring repo-level protections** (the five setup pre-requisites — see §4.0).
6. **Onboarding a new engineering partner** — the Two Worlds of Code self-identification step.
7. **Detecting an `ai-replaces-human` PR** — auto-labeller fires; this pack handles engineering side; S6 + S3 handle the change-management + compensation sides.

## 3. When NOT to invoke this pack

1. Trivial commits (typo fixes, dependency bumps with no semantic change).
2. Pure infra (Terraform, Kubernetes manifests) where the centaur overlay is unnecessary friction.
3. Repos without the 5 setup pre-requisites (§4.0) — the pack documents the gap and **refuses to enforce gates the repo cannot honour**. Without those configurations, the pack's discipline is advisory rather than enforcing.
4. Security reviews of partner-handling code — defer to counsel + a future dedicated security sub-pack.

## 4. Operational instructions

### 4.0 Repo-level setup pre-requisites — verify FIRST

Before any other §4 step against a new repo, the pack runs `oot-codeqa setup-protections --check <org>/<repo>` and confirms:

1. **Required status check `oot/klarna-test`** on the merge target branch. Workflow at `.github/workflows/klarna-gate.yml`. Any PR labelled `ai-replaces-human` cannot merge until the check passes.
2. **Force-push disabled, deletion disabled** on `main` (and any `audit/*` branches).
3. **Required signed commits** on the same branches — GPG or SSH-backed.
4. **Required reviewer count ≥ 1** for any PR touching `firm/audit-logs/`.
5. **Auto-label rule** at `.github/labeler.yml` matching the diff signatures in §4.7.

If any are missing, the pack offers to configure them via `oot-codeqa setup-protections --apply` (requires a GitHub admin token from Bitwarden). Without items 1–4, the pack refuses to claim "Klarna gate enforced" — the discipline is advisory only.

### 4.1 Repo orientation: CLAUDE.md, AGENTS.md, README

Every firm-controlled repo carries:

- **CLAUDE.md** at root — Claude Code orientation, ~300–800 words. What the repo is, tech stack, conventions, how to run tests, where related architectural decisions live in the Brain, the Klarna gate posture.
- **AGENTS.md** at root — vendor-neutral sibling. Substantively the same content, vendor-agnostic.
- **README.md** for humans, not agents. The pack does not specify README structure beyond standard open-source conventions.

ADRs and post-mortems live at `firm/architecture/` (Brain), not in the repo. Repo files reference the Brain by wikilink.

### 4.2 Plan Mode workflow

For any change touching >3 files OR introducing a new abstraction:

```
[Discovery] → [Plan] → [Review] → [Execute] → [Verify] → [PR]
```

**Discovery (5–15 min):** Plan Mode OFF; model reads the codebase via grep/explore. Output: context summary at `firm/architecture/<feature-slug>/discovery.md`.

**Plan (10–30 min):** Plan Mode ON. Hand the model the discovery summary + Output Spec. Ask for: step-by-step plan, files affected, explicit risk list, ordered test plan. Output: `firm/architecture/<feature-slug>/plan.md`.

**Review (5–15 min):** partner shares plan with another partner (or founder for high-risk). Reviewer comments inline. Iterate until accepted.

**Execute (varies):** fresh Claude Code session pointed at accepted plan. Plan Mode OFF. Each plan-step's commit references the plan: `[plan-step 3/7] <description>`.

**Verify (10–30 min):** human runs the test plan. Test failure = halt; iterate via fresh planning conversation.

**PR (5 min):** PR description references the plan Brain page, lists plan-steps completed, lists deviations. AI-authored commits use `Co-authored-by:` trailers. Auto-labeller may apply `ai-replaces-human` (§4.7).

### 4.3 Parallel session orchestration

When work decomposes into independent sub-tasks, ≤3 parallel sessions per partner. Discipline:

- **Maximum 3 parallel sessions.** Beyond that, attention fragments.
- **Named branches** per session (`feat/<partner_id>-<short-slug>-<n>`). No shared branches.
- **Each session writes its own Brain page** at `firm/architecture/<feature-slug>/session-<n>.md`.
- **Merge order pre-decided** before any session starts; recorded in the parent Brain page.
- **The partner is the merge driver,** not the agent. Conflicts resolved by partner with model assistance.

### 4.4 Three Philosophies — when to use which tool

| Tool | Best at | Pick when |
|---|---|---|
| **Claude Code** | Daily development, refactors, tests, debugging, Plan Mode | Default daily driver |
| **Augment Code** | Large multi-file initial builds | Greenfield features, big refactors, "rewrite from spec" |
| **Codex CLI / Open Codex** | Review/audit passes after Claude/Augment shipped | Second opinion before merge |
| **Open Codex** | Local-only equivalent of Codex CLI | Privacy track |

Document the choice in the Plan stage's Brain page: *"Tool for execute stage: <X>. Justification: …"*

### 4.5 Pre-merge checklist

1. Tests pass (CI green).
2. Linting + type-checking pass.
3. ≥1 human reviewer approved (the partner, not the AI).
4. AI-authorship attribution correct (`Co-authored-by:` trailers where appropriate).
5. **Klarna gate passed if `ai-replaces-human` labelled.** `oot/klarna-test` status check green.
6. CLAUDE.md / AGENTS.md updated if conventions changed.
7. ADR committed if an architectural decision was made.
8. Plan-step references match commits.

### 4.6 AI-authorship attribution (`Co-authored-by:` trailer convention)

Commits with AI-generated code:

```
feat: add OAuth2 PKCE flow for partner onboarding

Implements PKCE per RFC 7636. Plan-step 4/7 of [[architecture/auth-rewrite-2026/plan]].

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

Conventions:
- Trailer is the **last** line of the commit body (per git standard).
- Model name + version included; specificity over "Claude".
- Multi-model sessions list each (trailers stack).
- 100% human-authored commits **omit** the trailer entirely. Silence is the human signal.

### 4.7 Architectural decision records (ADRs)

ADRs at `firm/architecture/ADR-YYYY-NNN.md` per `templates/brain/adr.md`. Status chain: proposed → accepted → superseded. Sections: Context, Decision, Consequences, Considered alternatives.

PR implementing an accepted ADR references its ADR-id in description. Status flips proposed → accepted on merge.

### 4.8 Auto-labeller signatures

`.github/labeler.yml` (Phase 8) auto-applies `ai-replaces-human` for PRs matching:

1. **Code path removal** — deletion of a function whose body matched `(?i)\b(manual_review|escalate|human_in_loop|requires_review)\b`.
2. **Output ledger formula change** — modification to `partner-output-ledger.xlsx` formulas reducing variable pay attribution.
3. **New autonomous Skill** — new SKILL.md with frontmatter `automates: human_function: yes`.

Heuristic. Partner reviews the label within 24 hours, confirms or removes. Dismissal reasons train the labeller. False negatives added via PR.

When confirmed, R7 fires (per `routines/SPEC.md` R7); Klarna Test scoring proceeds.

### 4.9 Two Worlds of Code self-id (onboarding)

Five-question assessment:

1. Starting a non-trivial change: (a) start typing in editor or (b) start a Claude/Augment session and write a spec?
2. Debugging: (a) read code by eye or (b) ask the agent to find with grep + targeted prompts?
3. Last commit you're proud of: (a) hand-written, (b) AI-augmented, (c) AI-implemented from your spec?
4. Reviewing a PR: (a) read diff in GitHub or (b) review agent's plan first, accept diff after?
5. Agent suggests refactor you disagree with: (a) override and write your own or (b) iterate prompt until it matches your taste?

Mostly (a) → vibe-coder cohort. Mostly (b) → agentic-engineer. Mixed → **transitional cohort** (~40% of professional engineers in 2026).

Recorded in `firm/partners/<id>/profile.md` `two_worlds_self_id` field. Not a value judgement — operational input to training plan, expected output mix, Klarna Test triage when automation might affect their primary function.

## 5. Brain interaction protocol

**Reads:** `firm/architecture/*` for prior ADRs; `firm/partners/<id>/profile.md` for two-worlds self-id; current feature's `plan.md` at execute time.

**Writes:** `firm/architecture/<feature-slug>/discovery.md`, `plan.md`, `session-<n>.md`; `firm/architecture/ADR-YYYY-NNN.md`; `firm/decisions/D-YYYY-NNN.md` for non-architectural significant decisions.

## 6. Excel interaction protocol

| File | Operation | Trigger |
|---|---|---|
| X1 partner-output-ledger.xlsx | Read (R1 reads commits) | R1 daily |

This pack does not write to any Excel file directly. S3 owns X1 writes for code outputs.

## 7. Routine integration

- **R1** reads commits/PRs daily; inputs include `Co-authored-by:` trailers this pack enforces.
- **R7** fires when the auto-labeller (§4.8) tags a PR. This pack supplies engineering side; S6 supplies change-management; S3 supplies affected-partner identification.

## 8. Don'ts

1. Don't merge a PR labelled `ai-replaces-human` without Klarna score ≥14. R7 enforces; do not bypass.
2. Don't skip Plan stage on changes touching >3 files.
3. Don't attribute AI-generated code to a human author — use `Co-authored-by:` trailer.
4. Don't run >3 parallel Claude Code sessions without explicit orchestration plan in Brain.
5. Don't commit `.env` files, API keys, seeds. Bitwarden + env vars, always.
6. Don't reject a PR solely because it was AI-authored. Review the code on its merits.
7. Don't bypass branch protection to push a "quick fix". Fix the gate via PR; do not work around it.
8. Don't dismiss an `ai-replaces-human` auto-label without writing the dismissal reason in PR description.
9. Don't merge an unsigned commit to `main` or any `audit/*` branch.

## 9. Quick reference

| Situation | Action | Output |
|---|---|---|
| Non-trivial feature start | Plan Mode (§4.2) | Plan + ADR + PR with plan reference |
| AI-authored commit | `Co-authored-by:` trailer | Trailer feeds R1's ai_authored_pct |
| PR auto-labelled `ai-replaces-human` | R7 fires; this pack supplies engineering review | Klarna scored; merge gated |
| Architectural decision | Author ADR-YYYY-NNN; PR references | ADR status: proposed → accepted on merge |
| New repo onboarding | `oot-codeqa setup-protections` | 5 pre-requisites configured |
| Two Worlds self-id | 5-question assessment at onboarding | Recorded in partner profile |
| Tool choice | Plan stage records: Claude Code / Augment / Codex + justification | Brain page |

## 10. References

1. **Karpathy, A.** *Software 3.0* (Sequoia AI Ascent 2026).
2. **Anthropic.** CLAUDE.md and AGENTS.md conventions — https://docs.claude.com/en/docs/claude-code/.
3. **Dr. Tali Režun.** *Three Philosophies, One Goal: Augment Code, Claude Code, Codex CLI* (Medium, April 2026).
4. **Forsgren, N. et al.** *Accelerate* (IT Revolution Press, 2018) + *DORA Report 2025*.
5. **METR.** *RCT on AI tools and developer productivity* (July 2025) and February 2026 follow-up.
6. ØØT `governance/KLARNA-TEST.md`.
7. ØØT Skill Pack S6 — Change Management (METR baseline integration).
8. ØØT Skill Pack S3 — Compensation & Attribution (output capture integration).
9. ØØT `governance/SECRETS-POLICY.md`.
