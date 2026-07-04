#!/usr/bin/env bash
# ØØT cloud-track installer — thin pointer.
#
# The step-by-step v1.0 scaffold that used to live here is retired: it hard-coded
# a stale order (Bitwarden-first, Google Workspace as a hard requirement) that
# contradicts current guidance (secrets tooling is recommended-but-optional at
# start; Workspace is one option among several). The real, maintained install
# paths are below. This script just preflights a few tools and points you at them.

set -euo pipefail

cat <<'EOF'
ØØT — Cloud Track
=================

Pick one of the three maintained install paths:

  Path A — Agent-assisted (recommended). An AI agent drives the install with you,
           pausing to confirm each consequential step:
             installer/agent-assisted/START-HERE.md
             installer/agent-assisted/cloud-install-plan.md

  Path B — Guided wizard (interactive, self-serve):
             bash installer/bootstrap.sh
           (or: python3 installer/wizard.py)

  Path C — Do-it-yourself from the quickstart docs:
             docs/00-quickstart-cloud.md
             docs/02-installing-routines.md

Notes:
  * Bitwarden / Trezor / YubiKey are recommended-but-optional at the start; a
    founder can begin without them and add them as the firm matures.
  * The Ledger + Firm Brain are two GitHub repos (see ADR-002). Slack/email and
    a spreadsheet viewer are your choice.
  * Scheduled automation on the cloud track is Claude Code Routines (Pro+).
    No subscription? See the community track in docs/ and ADR-003.

EOF

echo "Preflight (local tools the cloud path uses):"
for tool in git python3 gpg; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '  [ok]      %s\n' "$tool"
  else
    printf '  [missing] %s — install it before continuing\n' "$tool"
  fi
done

echo
echo "Then follow Path A, B, or C above. This script performs no install steps itself."
