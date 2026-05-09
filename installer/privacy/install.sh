#!/usr/bin/env bash
# Privacy-track fallback installer for users who refuse the wizard.

set -euo pipefail

cat <<'EOF'
ØØT Privacy-Track Fallback Installer

This script does NOT teach. It assumes:
  1. You've read docs/00-quickstart-privacy.md and skills/privacy-self-sovereign/SKILL.md.
  2. You have an always-on machine, per-partner Trezors, UPS.
  3. You've ordered hardware and waited for delivery.

For a guided setup, run:
  python3 installer/wizard.py

EOF

read -rp "Proceed with non-interactive privacy install? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 1; }

cat <<'EOF'

--- v1.0 minimal scaffold ---

Step 1: Always-on machine OS setup.
  - macOS: enable FileVault; create dedicated 'oot' user; disable iCloud Documents/Desktop sync.
  - Linux: LUKS FDE at install; SSH key auth only.
  - Windows: BitLocker; Yubikey + password 2FA.

Step 2: LM Studio + models.
  - Install from https://lmstudio.ai/
  - Download Qwen 3 14B (default), Qwen 3 9B (fallback), Llama 3.3 70B (for R3).
  - Enable headless mode + llmster CLI.

Step 3: Per-partner Trezors.
  - Order from https://trezor.io/ (one per partner; never second-hand).
  - Initialise offline. Seed on paper, fireproof safe, separate from device.

Step 4: 4thtech firm setup.
  - Install 4thtech client.
  - Acquire firm dMail domain (~€50/year).
  - Configure dChat workspace.

Step 5: PollinationX storage.
  - Acquire storage NFT via PollinationX dApp.
  - Install client + grant per-partner read access.

Step 6: MCP servers.
  - pip install excel-mcp-server
  - Install Desktop Commander MCP and GitHub MCP per upstream docs.
  - Configure LM Studio's MCP host with all 4 (my-curator, excel-mcp,
    desktop-commander, github-mcp).

Step 7: GitHub branch protection.
  - Same as cloud track step 2 (skills/code-qa/SKILL.md §4.0).
  - Plus: configure GPG signing key on the always-on machine for R6.

Step 8: Routines (cron / launchd / Task Scheduler).
  - Install R5 (Sunday 09:00), R6 (daily 23:00), R1 (daily 18:00), R2 (Friday 08:00).
  - See routines/privacy/<R>.md for the canonical plist / cron entries.

Step 9: Onboard first partner.
  - Each partner gets their own Trezor + 4thtech wallet.
  - templates/partner-onboarding/provisioning-script.sh handles the rest.

Manual setup time: 2-3 weeks (hardware delivery + 2 weekends + first-partner onboarding).

For a fully-guided experience, the wizard at installer/wizard.py walks you through
each step with prompts and explanations.
EOF
