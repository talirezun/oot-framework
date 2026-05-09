#!/usr/bin/env bash
# Cloud-track fallback installer for users who refuse the wizard.
#
# Use this if you prefer scripted setup over the interactive wizard at
# `installer/wizard.py`. This script is shorter (no teaching) and assumes
# you've read docs/00-quickstart-cloud.md.
#
# Usage:
#   ./install.sh

set -euo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly REPO_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

cat <<'EOF'
ØØT Cloud-Track Fallback Installer

This script does NOT teach. It assumes:
  1. You've read docs/00-quickstart-cloud.md.
  2. You have Anthropic Pro/Max, Google Workspace, Slack, GitHub org accounts.
  3. You're prepared to run interactive prompts for credentials.

For a guided setup with explanations, run instead:
  python3 installer/wizard.py

EOF

read -rp "Proceed with non-interactive cloud install? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 1; }

# v1.0 scaffold — full implementation in v1.x.
cat <<'EOF'

--- v1.0 minimal scaffold ---

Step 1: Bitwarden organisation setup.
  - Create org at https://bitwarden.com/
  - Create canonical collections per governance/SECRETS-POLICY.md:
    founders, all-partners, specialists, advisors, shared-services.

Step 2: GitHub organisation + Brain repo.
  - Create org at https://github.com/
  - Create repo (private or public).
  - Configure 5 repo-level setup pre-requisites per skills/code-qa/SKILL.md §4.0:
    a. Force-push disabled on main.
    b. Deletion disabled on main.
    c. Required signed commits on main.
    d. Required reviewer ≥1 for firm/audit-logs/* paths.
    e. Auto-labeller (already shipped in .github/labeler.yml of this repo —
       copy to your firm Brain repo if applicable).

Step 3: Curator install.
  - Follow docs/01-installing-the-curator.md.
  - Create first domain: 'firm'.

Step 4: Routine install (R5, R6, R1, R2 — the 4 Day-1 Routines).
  - Follow docs/02-installing-routines.md.

Step 5: Onboard first partner.
  - Follow docs/03-onboarding-a-partner.md.
  - Run templates/partner-onboarding/provisioning-script.sh <partner_id>.

For each step's failure handling, see docs/07-troubleshooting.md.

Manual setup time: 2-4 hours across two weekends.
EOF
