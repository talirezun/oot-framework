#!/usr/bin/env bash
# ØØT privacy-track installer — thin pointer.
#
# The step-by-step v1.0 scaffold that used to live here is retired: it hard-coded
# a stale order (and named a `llmster` CLI that does not exist as an agent). The
# real, maintained install paths are below. This script just preflights a few
# tools and points you at them.

set -euo pipefail

cat <<'EOF'
ØØT — Privacy Track
===================

Pick one of the three maintained install paths:

  Path A — Agent-assisted (recommended). An AI agent drives the install with you,
           pausing to confirm each consequential step:
             installer/agent-assisted/START-HERE.md
             installer/agent-assisted/privacy-install-plan.md

  Path B — Guided wizard (interactive, self-serve):
             bash installer/bootstrap.sh --track=privacy
           (or: python3 installer/wizard.py)

  Path C — Do-it-yourself from the quickstart docs:
             docs/00-quickstart-privacy.md
             docs/02-installing-routines-privacy.md

Privacy-track model + automation stack (what the docs set up):
  * LM Studio >= 0.3.5 run headless by the `llmster` daemon = the local MODEL SERVER
    (OpenAI-compatible endpoint at http://127.0.0.1:1234/v1), managed with the
    `lms` CLI (`lms server start`, `lms load <model> --ttl 3600`).
  * OpenCode (`opencode run`) = the AGENT that loads skills, clones the Ledger,
    runs openpyxl, and calls MCP servers. See installer/agent-assisted/OPENCODE-SETUP.md.
  * `llmster` is only the model host — it does NOT run skills or agentic work.
  * Scheduled Routines = cron / launchd / Task Scheduler firing `opencode run`
    from the firm runner directory (which carries a scoped opencode.json).

EOF

echo "Preflight (privacy track needs an always-on machine; these are the local tools):"
for tool in git python3 gpg; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '  [ok]      %s\n' "$tool"
  else
    printf '  [missing] %s — install it before continuing\n' "$tool"
  fi
done
for tool in opencode lms; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '  [ok]      %s\n' "$tool"
  else
    printf '  [todo]    %s — installed later per OPENCODE-SETUP.md / lmstudio.ai\n' "$tool"
  fi
done

echo
echo "Then follow Path A, B, or C above. This script performs no install steps itself."
