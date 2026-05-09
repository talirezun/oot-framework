# Installer

Three ways to install ØØT, in order of preference:

## 1. The wizard (recommended)

```bash
python3 installer/wizard.py
```

Interactive 12-step terminal wizard. Resumable (`--resume`). Dry-run available (`--dry-run`).

Per BUILD-INSTRUCTIONS.md Phase 9: the wizard is the framework's primary onboarding path. It teaches as it installs. v1.0 ships the wizard scaffold (steps 1-4 implemented; steps 5-12 reference manual setup); v1.x hardens the remaining steps.

## 2. Fallback shell scripts

For users who prefer scripted setup over interactive:

- `installer/cloud/install.sh` — cloud track minimal scaffold.
- `installer/privacy/install.sh` — privacy track minimal scaffold.

These scripts are deliberately thin. They reference the user docs rather than duplicating them. If you want the framework to teach you while installing, use the wizard.

## 3. Manual setup

Follow the user docs:
- [`docs/00-quickstart-cloud.md`](../docs/00-quickstart-cloud.md) — cloud track
- [`docs/00-quickstart-privacy.md`](../docs/00-quickstart-privacy.md) — privacy track

These cover the same ground as the wizard but in markdown form.

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
