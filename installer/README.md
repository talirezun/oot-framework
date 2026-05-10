# Installer

Three ways to install ØØT, in order of preference for v1.0.1+:

## 1. Path A — Coding-agent-assisted (recommended)

Hand the install plan to a coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, Continue.dev, or any agent meeting the [capability spec](agent-assisted/AGENT-CAPABILITY-SPEC.md)). The agent reads the plan, executes the steps, asks you the questions, and produces a written install summary.

```bash
# In your coding agent of choice, run:
# "Read installer/agent-assisted/cloud-install-plan.md and execute it."
```

- [`installer/agent-assisted/README.md`](agent-assisted/README.md) — how it works, when to use vs. the other paths.
- [`installer/agent-assisted/AGENT-CAPABILITY-SPEC.md`](agent-assisted/AGENT-CAPABILITY-SPEC.md) — is your agent compatible?
- [`installer/agent-assisted/cloud-install-plan.md`](agent-assisted/cloud-install-plan.md) — cloud track plan (60-90 min).
- [`installer/agent-assisted/privacy-install-plan.md`](agent-assisted/privacy-install-plan.md) — privacy track plan (~25 hours over two weekends + 1 week hardware shipping).

This path is recommended for ≥80% of founders, especially less-technical ones. The agent does the JSON edits, the GPG key generation, the branch protection configuration, the MCP wiring, and the verification — the most error-prone steps in any framework install.

**LLM-agnostic:** the install plans are written so any agent meeting the capability spec works, including agents running against local LM Studio models.

## 2. Path B — The wizard (Python terminal)

For founders who prefer not to use a coding agent:

```bash
python3 installer/wizard.py
```

Interactive 12-step terminal wizard. Resumable (`--resume`). Dry-run available (`--dry-run`).

v1.0 ships the wizard scaffold (steps 1-4 implemented; steps 5-12 reference the manual docs at [`docs/00-quickstart-cloud.md`](../docs/00-quickstart-cloud.md)). v1.x hardens the remaining steps to be programmatic. Pick this path if you don't have access to a coding agent or are philosophically opposed to handing one shell access.

## 3. Path C — Manual setup (the docs)

For founders who want every step to be something they typed themselves:

- [`docs/00-quickstart-cloud.md`](../docs/00-quickstart-cloud.md) — cloud track
- [`docs/00-quickstart-privacy.md`](../docs/00-quickstart-privacy.md) — privacy track
- [`docs/MODULES.md`](../docs/MODULES.md) — what to install and what's optional (read this first regardless of path)

These cover the same ground as Paths A and B but in markdown form. Most transparent; nothing happens you didn't type. Slowest and most error-prone for non-technical founders.

## Fallback shell scripts (Path B variant)

- `installer/cloud/install.sh` — cloud track minimal scaffold.
- `installer/privacy/install.sh` — privacy track minimal scaffold.

These scripts are deliberately thin. They reference the user docs rather than duplicating them. Functionally equivalent to Path C with a printed checklist.

---

## What the wizard does (the spec)

The wizard's full spec is in [`BUILD-INSTRUCTIONS.md`](../BUILD-INSTRUCTIONS.md) Phase 9. Twelve steps:

1. Welcome + framework overview.
2. Track selection (cloud vs. privacy).
3. Firm profile (name, partner count, jurisdictions, EU AI Act exposure).
4. Pre-requisite check (`git`, `bw`, `gh`, `curl`, `jq`, plus track-specific).
5. Hardware (privacy track only) — confirm always-on machine + UPS + FDE.
6. Secrets vault — Bitwarden / 1Password org + canonical collections.
7. GitHub setup — org + Brain repo + 5 repo-level setup pre-requisites.
8. Track-specific tools.
9. The Curator install + first domain.
10. Routine configuration (R5, R6, R1, R2).
11. Klarna gate setup.
12. Smoke test + summary.

The wizard:
- Explains *why* it's asking each question.
- Requires explicit consent for every consequential action.
- Is **idempotent** — `--resume` skips completed steps.
- Has a `--dry-run` flag that walks the questions without actions.
- Stores credentials only in Bitwarden/keychain — never in the wizard's state file.

## v1.0 vs. v1.x

In v1.0 (this release):
- Wizard scaffold ships with steps 1-4 functional.
- Steps 5-12 reference the corresponding sections in `docs/00-quickstart-cloud.md` / `docs/00-quickstart-privacy.md`.
- Founders complete steps 5-12 manually using the docs.

In v1.x:
- Steps 5-12 are programmatic (Bitwarden via `bw` CLI, GitHub via `gh` CLI, Anthropic via API, etc.).
- The wizard becomes a single end-to-end run.
