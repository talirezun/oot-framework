#!/usr/bin/env python3
"""
ØØT Installer Wizard — terminal-based, OpenClaw-style.

Entry point: `python3 installer/wizard.py` or `oot-wizard` (after pip install).

Per BUILD-INSTRUCTIONS.md Phase 9: 12-step resumable flow guiding a founder
through cloud or privacy track setup. Idempotent (state at ~/.oot/wizard-state.yaml);
--resume picks up after any step; --dry-run produces config preview without action.

Design: every prompt explains *why*. The wizard is also a teaching tool.
Every consequential action requires explicit consent.

NOT YET IMPLEMENTED — v1.0 ships the spec + a minimal scaffold. v1.x hardens
to a fully runnable wizard. Founders in v1.0 follow docs/00-quickstart-cloud.md
or docs/00-quickstart-privacy.md manually.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

OOT_HOME = Path(os.environ.get("OOT_HOME", Path.home() / ".oot"))
STATE_FILE = OOT_HOME / "wizard-state.yaml"


def step_01_welcome() -> None:
    print("\n" + "=" * 70)
    print("ØØT — Organisation of Tomorrow — Installer Wizard")
    print("=" * 70)
    print("""
Welcome. This wizard guides you through setting up the framework
end-to-end. About 60 minutes for the cloud track, 90+ minutes for
the privacy track.

The wizard is resumable: re-run with --resume to pick up where you
left off. --dry-run shows what would happen without doing it.

Read these first if you haven't:
  - MANIFESTO.md (15 min) — the framework's intellectual core.
  - SPEC.md (30 min) — the technical specification.
  - governance/KLARNA-TEST.md (10 min) — the signature discipline.

Press Enter to continue, or Ctrl-C to exit.
""")
    input()


def step_02_track_selection() -> str:
    print("\n--- Step 2/12 — Track selection ---\n")
    print("Cloud track: Anthropic + Google + Slack. Fastest setup.")
    print("Privacy track: 4thtech + PollinationX + LM Studio. Sovereign; needs always-on machine.")
    print()
    print("Most founders should start with cloud unless you have a clear sovereignty mandate.\n")

    while True:
        choice = input("Track [cloud/privacy]: ").strip().lower()
        if choice in {"cloud", "privacy"}:
            return choice
        print(f"Invalid: {choice!r}. Type 'cloud' or 'privacy'.")


def step_03_firm_profile() -> dict[str, str]:
    print("\n--- Step 3/12 — Firm profile ---\n")
    name = input("Firm name: ").strip()
    partner_count = input("Estimated number of partners: ").strip()
    jurisdictions = input("Jurisdictions (ISO codes, comma-separated, e.g. SI,HR): ").strip()
    eu_high_risk = input("Will any AI use case be high-risk Annex III (employment / essential services)? [y/N]: ").strip().lower()
    return {
        "name": name,
        "partner_count": partner_count,
        "jurisdictions": jurisdictions,
        "eu_high_risk": "yes" if eu_high_risk == "y" else "no",
    }


def step_04_prereq_check(track: str) -> None:
    print("\n--- Step 4/12 — Pre-requisite check ---\n")
    print(f"Checking required CLI tools for {track} track...")
    tools_required = {
        "cloud": ["git", "bw", "gh"],
        "privacy": ["git", "bw", "gh", "llmster"],
    }
    import shutil
    missing = []
    for tool in tools_required[track]:
        if shutil.which(tool):
            print(f"  ✓ {tool}")
        else:
            print(f"  ✗ {tool} NOT installed")
            missing.append(tool)

    if missing:
        print(f"\nMissing tools: {missing}.")
        print("Install instructions:")
        for tool in missing:
            install_hint = {
                "git": "macOS: pre-installed; Linux: apt install git; Windows: git-scm.com",
                "bw": "https://bitwarden.com/help/cli/",
                "gh": "https://cli.github.com/",
                "llmster": "https://lmstudio.ai/ + brew install llmster (privacy track)",
            }.get(tool, "see tool docs")
            print(f"  - {tool}: {install_hint}")
        print()
        proceed = input("Install missing tools and re-run wizard? [Y/n]: ").strip().lower()
        if proceed != "n":
            sys.exit(0)
    else:
        print("\nAll pre-requisites present.\n")


def step_05_to_12_stub() -> None:
    print("""
--- Steps 5-12 (TODO in v1.0) ---

Steps 5-12 are scaffolded but require completion in v1.x:

  5. Hardware (privacy track only) — confirm always-on machine + UPS + FDE.
  6. Secrets vault — Bitwarden / 1Password org + canonical collections.
  7. GitHub setup — org + Brain repo + 5 repo-level setup pre-requisites.
  8. Track-specific tools — Anthropic / Google / Slack (cloud) OR LM Studio +
     models + 4thtech firm domain + PollinationX storage NFT (privacy).
  9. Curator install — desktop app + MyCuratorMCP + first domain.
  10. Routines — install R5, R6, R1, R2 (the 4 Day-1 Routines).
  11. Klarna gate setup — confirm `oot/klarna-test` workflow + auto-labeller +
      branch protection.
  12. Smoke test + summary — run validators; print summary card.

For v1.0: follow the manual setup at:
  - docs/00-quickstart-cloud.md (cloud track)
  - docs/00-quickstart-privacy.md (privacy track)

The manual setup hits the same checkpoints; the wizard automates them in v1.x.
""")


def main() -> int:
    parser = argparse.ArgumentParser(description="ØØT installer wizard")
    parser.add_argument("--resume", action="store_true", help="Resume from last completed step")
    parser.add_argument("--dry-run", action="store_true", help="Preview without actions")
    args = parser.parse_args()

    OOT_HOME.mkdir(parents=True, exist_ok=True)

    step_01_welcome()
    track = step_02_track_selection()
    profile = step_03_firm_profile()

    print(f"\nFirm: {profile['name']} ({profile['partner_count']} partners) on {track} track in {profile['jurisdictions']}.")
    if profile["eu_high_risk"] == "yes":
        print("⚠ EU high-risk use cases planned: governance/EU-AI-ACT.md mapping is mandatory.")

    if args.dry_run:
        print("\n--dry-run set; would proceed with steps 4-12 against this profile.")
        return 0

    step_04_prereq_check(track)
    step_05_to_12_stub()

    return 0


if __name__ == "__main__":
    sys.exit(main())
