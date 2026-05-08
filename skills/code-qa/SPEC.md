# Skill Pack S4 — Code & QA: SPEC

**ID:** S4
**Name:** Code & QA
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

Operationalises the centaur model for software development in ØØT-native firms. Encodes Karpathy's Software 3.0 division of labour (spec / test / review human, implementation AI), the CLAUDE.md / AGENTS.md repo conventions, Plan Mode discipline, parallel-session orchestration, and the **Klarna Test pre-merge gate**.

The most opinionated coding-related Skill Pack the framework ships. Disagreement with these opinions is fine; the pack is overridable. But the defaults reflect the practice the framework's authors have found to work.

---

## Scope

**Covers:**
- CLAUDE.md / AGENTS.md authoring discipline at repo level.
- Plan Mode workflow (when to use, what a good plan looks like, the discovery → plan → review → execute pattern).
- Parallel coding-session orchestration (multiple Claude Code or Augment Code sessions on related work).
- Three Philosophies pattern: Augment Code for big multi-file builds, Claude Code for daily development, Codex CLI for review/audit.
- **The Klarna Test pre-merge gate** wired via the `oot/klarna-test` GitHub status check.
- Daily commit-summary Routine integration (R1 captures code outputs).
- Code review discipline when AI authored the code.
- AI-vs-human authorship attribution (`Co-authored-by:` trailers, rework-within-30-days tracking).
- The "Two Worlds of Code" cohort sorting in onboarding (Karpathy: vibe coders vs. agentic engineers).
- **Repo-level setup pre-requisites** (5 GitHub configurations the SKILL.md walks through).
- The `oot-readiness` PR auto-labeller.

**Does NOT cover:**
- Specific languages or frameworks (those live in language-specific sub-skills, optional add-ons).
- DevOps / CI/CD pipelines for product code (the pack references but does not specify them).
- Security review workflows (separate concern; counsel-adjacent; recommended: a dedicated S4 sub-pack in v1.x).

---

## Allowed tools / dependencies

- **Claude Code** (primary daily driver).
- **Claude Desktop with Plan Mode** for spec → plan transitions.
- **Augment Code** for big multi-file builds (optional alternative).
- **Codex CLI / Open Codex** for review/audit passes (optional).
- **GitHub MCP** — read commits, PRs, labels; write status checks via the `oot/klarna-test` workflow.
- **Curator MCP** — write architectural decisions / ADRs to `firm/architecture/`; query Brain for prior decisions.
- **The Compensation & Attribution Skill Pack (S3)** — for `Co-authored-by:` tracking and ledger integration.

---

## When to invoke

1. **Starting a non-trivial feature** — Plan Mode workflow.
2. **Reviewing a PR** — especially one labelled `ai-replaces-human`.
3. **Choosing among Augment Code / Claude Code / Codex CLI** for a specific task.
4. **Writing or updating CLAUDE.md / AGENTS.md** in the firm's product repos.
5. **Configuring repo-level protections** (the 5 setup pre-requisites — see §4.0).
6. **Onboarding a new engineering partner** — the Two Worlds of Code self-identification step.
7. **Detecting an AI-replaces-human PR** — the auto-labeller fires; this pack handles the engineering side; S6 + S3 handle the change-management + compensation sides.

---

## When NOT to invoke

1. **For trivial commits** (typo fixes, dependency bumps with no semantic change).
2. **For pure infra** (Terraform, Kubernetes manifests) where the centaur pattern overlay is unnecessary friction.
3. **For repos without the 5 setup pre-requisites** (see §4.0) — the pack documents the gap and refuses to enforce gates that the repo cannot honour. Without those configurations, the pack's discipline is advisory rather than enforcing — invoking the pack against an unconfigured repo produces false confidence.
4. **For security reviews** of partner-handling code — defer to counsel + a future dedicated security sub-pack.

---

## Operational instructions

### 4.0 Repo-level setup pre-requisites (do this BEFORE invoking any other §4 step)

The Klarna gate, the Article 12 audit retention, and the AI-authorship attribution all assume specific GitHub repo configuration. The pack's first action against a new repo is to verify (and configure if missing):

1. **Required status check `oot/klarna-test`** on the merge target branch. Workflow at `.github/workflows/klarna-gate.yml` (shipped Phase 8). Any PR labelled `ai-replaces-human` cannot merge until the check passes.
2. **Force-push disabled, deletion disabled** on `main` (and any `audit/*` branches) — the immutability foundation for Routine R6's audit trail.
3. **Required signed commits** on the same branches — GPG or SSH-backed. The cloud installer (Phase 9) ships a setup script that configures the partner's local git for signed commits.
4. **Required reviewer count ≥ 1** for any PR touching `firm/audit-logs/` — protects the integrity of the EU AI Act record.
5. **Auto-label rule** at `.github/labeler.yml` that applies `ai-replaces-human` to any PR matching the Code & QA pack's diff signatures (see §4.7).

The pack ships a CLI helper `oot-codeqa setup-protections` that, given a GitHub org/repo, configures all five via the GitHub API (requires an admin token from Bitwarden). The same helper has a `--check` mode that reports configuration status without changing anything.

### 4.1 Repo orientation: CLAUDE.md, AGENTS.md, README structure

Every firm-controlled repo carries:

- **CLAUDE.md at the root** — the Claude Code orientation file. Tailored to the repo. ~300-800 words covering: what the repo is, who it serves, tech stack, key conventions, how to run tests, where the Brain stores related architectural decisions, the Klarna gate posture, and the `oot/klarna-test` workflow link.
- **AGENTS.md at the root** — the cross-vendor sibling. Should be substantively the same content as CLAUDE.md but written for any AI agent (avoid Claude-specific phrasing). Length similar.
- **README.md** — for humans, not agents. The pack does not specify README structure beyond "follow standard open-source conventions".

The pack's `examples/` ships with a CLAUDE.md template and a worked example for a typical TypeScript SaaS repo and a typical Python data-pipeline repo.

**Discipline:** when a Skill Pack or Routine writes Brain content related to the repo (architectural decisions, post-mortems, design docs), the page lives at `firm/architecture/` (under the `firm` Curator domain), not in the repo. Repo `README.md` and `CLAUDE.md` reference the Brain by wikilink (e.g. *"Architectural decisions for this repo: see [[architecture/ADR-2026-007]]"*).

### 4.2 Plan Mode workflow

The pack's discipline for any change touching more than 3 files OR any change that introduces a new abstraction is:

```
[Discovery] → [Plan] → [Review] → [Execute] → [Verify] → [PR]
```

Each stage is a distinct conversation in Claude Code (or equivalent), with the prior stage's output as input to the next. The discipline:

**Discovery (5-15 minutes):**
- Open Claude Code in the repo. Read the codebase via grep / explore. The Plan Mode toggle is OFF here — the model can read freely.
- Output of this stage: a short "context summary" the partner reads to confirm the model understood the codebase. Brain page: `firm/architecture/<feature-slug>/discovery.md`.

**Plan (10-30 minutes):**
- Toggle Plan Mode ON. Hand the model the discovery summary + the Output Spec.
- Ask for: a step-by-step plan, a list of files affected, an explicit risk list, an ordered test plan.
- The partner reviews the plan critically — this is where the centaur pattern earns its value.
- Output: a committed plan at `firm/architecture/<feature-slug>/plan.md` referencing the relevant ADRs.

**Review (5-15 minutes):**
- The partner shares the plan with another partner (or with the founder for high-risk plans).
- Reviewer comments inline on the Brain page.
- Plan is iterated until accepted.

**Execute (varies):**
- Open a fresh Claude Code session pointed at the accepted plan. Plan Mode is OFF (the model executes).
- The session does the actual coding, in the order the plan specifies.
- Each plan-step's commit message references the plan: `[plan-step 3/7] <description>`.

**Verify (10-30 minutes):**
- Run the test plan from the Plan stage. The partner does this, not the agent — verification is a human responsibility.
- Any test failure is a halt; iterate via a fresh planning conversation if the plan needs revision.

**PR (5 minutes):**
- The PR description references the plan Brain page, lists the plan-steps completed, lists deviations (if any).
- AI-authored commits use `Co-authored-by: claude@anthropic` (or equivalent for the model used).
- The PR is auto-labelled by the labeller if it matches §4.7 signatures.

### 4.3 Parallel session orchestration

When the work decomposes cleanly into independent sub-tasks, the partner runs ≤3 parallel Claude Code sessions, each with its own Plan Mode pre-pass and clearly-bounded scope. Discipline:

- **Maximum 3 parallel sessions** per partner. Beyond that, attention fragments and merge conflicts dominate.
- Each session has a **named branch** (`feat/<partner_id>-<short-slug>-<n>`). No shared branches across sessions.
- Each session writes to **its own Brain page** under `firm/architecture/<feature-slug>/session-<n>.md`.
- Merge order is pre-decided before any session starts; recorded in the parent Brain page.
- The partner is the merge driver, not the agent. Conflicts are resolved by the partner with model assistance; never by the model alone.

### 4.4 Three Philosophies — when to use which tool

Different tools, different strengths. The pack's recommended usage:

| Tool | Best at | When to pick it |
|---|---|---|
| **Claude Code** | Daily development, refactors, tests, debugging, Plan Mode for new features | The default daily driver |
| **Augment Code** | Large multi-file initial builds (greenfield features, big refactors) | When the change is a "rewrite" or "scaffold from spec" |
| **Codex CLI / Open Codex** | Review/audit passes after Claude Code or Augment Code shipped | When the partner wants a second opinion before merge |
| **Open Codex** (privacy track) | Local-only equivalent of Codex CLI | Privacy-track development |

The pack's discipline is to **document the choice** in the Plan stage's Brain page, not to imply tool-neutrality. Every plan states: *"Tool for execute stage: Claude Code / Augment Code / Codex CLI. Justification: ..."*.

### 4.5 Pre-merge checklist

Before any PR merges, the pack's checklist:

1. **Tests pass.** Standard CI green.
2. **Linting + type-checking pass.** Standard.
3. **At least one human reviewer** has approved (the Code & QA pack's reviewer is the *partner*, not the AI).
4. **AI-authorship attribution is correct.** Commits with AI authorship use `Co-authored-by:` trailers; commits without should not.
5. **Klarna gate passed if `ai-replaces-human` labelled.** The `oot/klarna-test` status check must be green.
6. **CLAUDE.md / AGENTS.md updated** if conventions changed.
7. **ADR committed** if an architectural decision was made (Brain page at `firm/architecture/`).
8. **Plan-step references match commits** (the plan was followed; deviations explicitly noted in PR description).

### 4.6 AI-authorship attribution (`Co-authored-by:` trailer convention)

Commits that contain AI-generated code use the `Co-authored-by:` trailer in the commit message:

```
feat: add OAuth2 PKCE flow for partner onboarding

Implements PKCE per RFC 7636. Plan-step 4/7 of [[architecture/auth-rewrite-2026/plan]].

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

Conventions:
- The trailer is the **last** line of the commit body (per git's standard).
- The model name + version is included; the framework's authors prefer specificity over generic "Claude".
- For a session that used multiple models, list each (Co-authored-by lines stack).
- For 100% human-authored commits, **omit** the trailer entirely. Do not write `Co-authored-by: human <...>` — silence is the human signal.

This convention feeds R1's `ai_authored_pct` estimation. R1 reads commit trailers and computes a per-commit AI percentage from the diff statistics (modulated by trailer presence).

### 4.7 Architectural decision records — write to Brain, link from PR

Any change that involves a new abstraction, a new dependency, a new architectural pattern, or a deprecation of an existing one is an **ADR**. ADRs live at `firm/architecture/ADR-YYYY-NNN.md` per `templates/brain/adr.md`. Every ADR has:

- A status chain (proposed → accepted → superseded).
- A "Context" section (why we needed to decide).
- A "Decision" section (what we chose).
- A "Consequences" section (what this enables / forbids in the future).
- A "Considered alternatives" section (what we didn't choose, and why).

The PR that implements an accepted ADR references its ADR-id in the description. The ADR's status flips from `proposed` to `accepted` when the PR merges.

### 4.8 The auto-labeller (`ai-replaces-human` PR signatures)

Phase 8 ships `.github/labeler.yml` that auto-applies the `ai-replaces-human` label to PRs matching any of these signatures:

1. **Code path removal** — the PR removes a function / branch that previously routed work to a human (heuristic: any deletion of a function whose body contains the regex `(?i)\b(manual_review|escalate|human_in_loop|requires_review)\b`).
2. **Output ledger formula change** — any modification to `partner-output-ledger.xlsx` formulas that reduces variable pay attribution (the script validates this by re-running the computation against the prior commit's data).
3. **New autonomous Skill** — a new SKILL.md or Skill folder under `skills/` that has `automates: human_function: yes` in its frontmatter.

The labeller is a heuristic; it flags candidates. The Code & QA pack's discipline: the partner reviews the auto-label and either confirms or removes within 24 hours. False positives are documented (the labeller learns over time via dismissal patterns); false negatives are added to the labeller config via a follow-up PR.

When confirmed, R7 fires (per `routines/SPEC.md` R7); the Klarna Test scoring proceeds.

### 4.9 Two Worlds of Code partner self-identification

Per Karpathy's framing: **vibe coders** (legacy, pre-Software-3.0) and **agentic engineers** (Software 3.0 native). The pack provides a 5-question self-assessment used at partner onboarding:

1. When you start a non-trivial change, do you (a) start typing in your editor or (b) start a Claude/Augment session and write a spec?
2. When debugging, do you (a) read the code and trace by eye or (b) ask the agent to find the issue with grep + targeted prompts?
3. Your last commit you're proud of — was it (a) hand-written, (b) AI-augmented, or (c) AI-implemented from your spec?
4. Do you (a) read the diff in GitHub or (b) review the agent's plan first, accept the diff after?
5. When the agent suggests a refactor you disagree with, do you (a) override and write your own or (b) iterate the prompt until the agent's output matches your taste?

Mostly (a) → vibe-coder cohort. Mostly (b) → agentic-engineer cohort. Mixed → **transitional cohort** (the framework's authors estimate ~40% of professional engineers in 2026 are transitional).

The cohort is recorded in the partner's `firm/partners/<id>/profile.md` `two_worlds_self_id` field. It's not a value judgement — it's an operational input to: (a) the firm's training plan for the partner, (b) the partner's expected output mix, (c) the Klarna Test triage when an automation might affect their primary function.

---

## Brain interaction protocol

**Reads:**
- `firm/architecture/*` — for prior ADRs.
- `firm/partners/<id>/profile.md` — for two-worlds self-id.
- `firm/architecture/<feature-slug>/plan.md` — at execute time.

**Writes:**
- `firm/architecture/<feature-slug>/discovery.md`, `plan.md`, `session-<n>.md` — at each Plan Mode stage.
- `firm/architecture/ADR-YYYY-NNN.md` — for each architectural decision.
- `firm/decisions/D-YYYY-NNN.md` — for non-architectural-but-significant decisions (cross-references the ADR).

---

## Excel interaction protocol

| File | Operation | Trigger |
|---|---|---|
| X1 partner-output-ledger.xlsx | Read (at PR merge time, R1 reads commits) | R1 daily |
| (none direct) | — | The pack does not write to any Excel file directly |

S3 owns X1 writes for code outputs; this pack just produces the inputs (commits, PRs) R1 captures.

---

## Routine integration

- **R1** (daily output capture) — reads commits/PRs daily. Inputs include the `Co-authored-by:` trailers this pack enforces.
- **R7** (Klarna Test trigger) — fires when the auto-labeller (§4.8) tags a PR. This pack supplies the engineering side of the scoring (technical reviewers, technical evidence); S6 supplies the change-management side; S3 supplies the affected-partner identification.

---

## Don'ts

1. **Don't merge a PR labelled `ai-replaces-human`** without a Klarna Test score ≥14. Routine R7 enforces; do not bypass.
2. **Don't skip the Plan stage** on changes touching more than three files.
3. **Don't attribute AI-generated code to a human author** in commit messages — use `Co-authored-by: claude@anthropic` (or equivalent).
4. **Don't run more than three parallel Claude Code sessions** without an explicit orchestration plan in the Brain.
5. **Don't commit `.env` files, API keys, seeds, or any credential** to git history. Bitwarden + environment variables, always (see `governance/SECRETS-POLICY.md`).
6. **Don't reject a PR solely because it was AI-authored**; review the code on its merits.
7. **Don't bypass branch protection** to push a "quick fix" — the protections are the point. If the gate is wrong, fix the gate via PR; do not work around it.
8. **Don't dismiss an `ai-replaces-human` auto-label** without writing the dismissal reason in the PR description (the dismissal reason trains the labeller).
9. **Don't merge an unsigned commit** to `main` or any `audit/*` branch. The signing is the EU AI Act retention foundation.
10. **Don't commit `_TEMPLATE_SKILL.md`-style skill scaffolds** with `<!-- TODO -->` markers to a hardened skill folder; scaffolds belong in the Tier-2 packs only.

---

## Quick reference

| Situation | Action | Output |
|---|---|---|
| Starting a non-trivial feature | Plan Mode: discovery → plan → review → execute → verify → PR | Plan + execution + ADR in Brain; PR with plan reference |
| AI-authored commit | Add `Co-authored-by: <model> <noreply@...>` trailer | Trailer feeds R1's ai_authored_pct |
| PR auto-labelled `ai-replaces-human` | R7 fires; this pack supplies engineering review; S6 + S3 do change/comp | Klarna Test scored; merge gated |
| Architectural decision needed | Author ADR-YYYY-NNN.md in `firm/architecture/`; PR references it | ADR status: proposed → accepted on merge |
| New repo onboarding | Run `oot-codeqa setup-protections`; verify 5 pre-requisites | Branch protection + status checks + labeller configured |
| Two Worlds self-id | 5-question assessment at onboarding | Recorded in partner profile |
| Tool choice | Plan stage records: Claude Code / Augment / Codex + justification | Brain page |

---

## Worked examples concept

The pack's `examples/` ships with **3 worked examples**:

1. **A non-trivial feature, full Plan Mode**. Partner builds OAuth2 PKCE for partner onboarding. Discovery → plan → execute walked through end-to-end with actual prompts, the partner's review comments, the executing session's commits with `Co-authored-by:` trailers, the merged PR, and the ADR.
2. **An `ai-replaces-human` PR end-to-end**. PR removes a manual contract-review step in favour of an AI Skill. Auto-label fires. R7 fires. The Klarna Test is scored (final score 16/20). Engineering review (this pack), change management (S6), compensation (S3) all contribute. PR merges with the test reference in the description. The 90-day review is scheduled.
3. **A parallel session example**. Partner has 3 independent sub-tasks for a refactor. The orchestration plan, the per-session Brain pages, the merge order, the actual git history, and the post-merge ADR are shown.

---

## References

1. **Karpathy, A.** *Software 3.0* (Sequoia AI Ascent 2026). The framing of human-AI division of labour the pack rests on.
2. **Anthropic.** CLAUDE.md and AGENTS.md conventions documentation — `https://docs.claude.com/en/docs/claude-code/`.
3. **Dr. Tali Režun.** *Three Philosophies, One Goal: Augment Code, Claude Code, Codex CLI* (Medium, April 2026).
4. **Forsgren, N. et al.** *Accelerate* (IT Revolution Press, 2018) and *DORA Report 2025* — the centaur-pattern productivity and quality findings.
5. **METR.** *RCT on AI tools and developer productivity* (July 2025) and February 2026 follow-up. The perception-gap study; underpins the Plan Mode discipline.
6. **Tessl / aider / Continue.dev** — open-source agentic IDE projects that influenced the parallel-session pattern.
7. ØØT `governance/KLARNA-TEST.md`.
8. ØØT Skill Pack S6 — Change Management (METR baseline integration).
9. ØØT Skill Pack S3 — Compensation & Attribution (output capture integration).
10. ØØT `governance/SECRETS-POLICY.md`.

---

## Repo-level setup pre-requisites (must be in the SKILL.md)

The Klarna gate, the Article 12 audit retention, and the AI-authorship attribution all assume specific GitHub repo configuration. The SKILL.md must walk through configuring:

1. **Required status check `oot/klarna-test`** on the merge target branch — the Klarna gate. The workflow file is at `.github/workflows/klarna-gate.yml` (shipped Phase 8). Any PR labelled `ai-replaces-human` cannot be merged until the check passes.
2. **Force-push disabled, deletion disabled** on `main` (and any `audit/*` branches) — the immutability foundation for Routine R6's audit trail.
3. **Required signed commits** on the same branches — GPG or SSH-backed. The cloud installer (Phase 9) ships a setup script for this.
4. **Required reviewer count ≥ 1** for any PR touching `firm/audit-logs/` — protects the integrity of the EU AI Act record.
5. **Auto-label rule** (`.github/labeler.yml` or equivalent) that applies `ai-replaces-human` to any PR matching the Code & QA pack's diff signatures (e.g. removes a code path routing to manual review, modifies a `partner-output-ledger.xlsx` formula in a way that reduces variable pay attribution).

Without items 1–4, the Klarna and Article 12 disciplines are advisory rather than enforcing. The pack's "When NOT to invoke" section must call this out — invoking the pack against a repo that has not configured these protections produces false confidence.

---

## Acceptance criteria

Standard. Plus:
- Klarna Test integration is documented with the **complete** `.github/workflows/klarna-gate.yml` snippet (not just a reference).
- The five repo-level setup pre-requisites are documented step-by-step.
- Plan Mode example is concrete (not abstract) — actual prompts shown, actual commits, actual ADR.
- The `Co-authored-by:` trailer convention is specified with examples.
- 3+ worked examples in `examples/`.
- Frontmatter passes the Phase 8 linter.
