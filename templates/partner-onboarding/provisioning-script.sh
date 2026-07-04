#!/usr/bin/env bash
# ØØT Partner Provisioning Script
# Implements PROVISIONING-SPEC.md
# Usage: ./provisioning-script.sh <partner_id>
#        ./provisioning-script.sh rollback <partner_id>
#        ./provisioning-script.sh --resume <partner_id>
#
# Pre-requisites: bw, gh, git, curl, jq installed; ~/.oot/firm.yaml configured;
# Bitwarden CLI authenticated (`bw login`); GPG signing key configured for signed commits.

set -euo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly OOT_HOME="${OOT_HOME:-$HOME/.oot}"
readonly LOG_DIR="$OOT_HOME/onboarding-logs"
readonly STATE_DIR="$OOT_HOME/onboarding-state"
readonly FIRM_CONFIG="$OOT_HOME/firm.yaml"

# ──────────────────────────────────────────────────────────────────────────────
# Argument parsing
# ──────────────────────────────────────────────────────────────────────────────

readonly TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

usage() {
    cat <<EOF
Usage:
  $(basename "$0") <partner_id>             # provision new partner
  $(basename "$0") --resume <partner_id>    # resume from last completed step
  $(basename "$0") rollback <partner_id>    # roll back all completed steps
  $(basename "$0") --dry-run <partner_id>   # show what would happen without acting
  $(basename "$0") --track <cloud|privacy>  # override firm.yaml track default
EOF
    exit 1
}

ACTION="provision"
DRY_RUN=false
TRACK_OVERRIDE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --resume) ACTION="resume"; shift ;;
        rollback) ACTION="rollback"; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --track) TRACK_OVERRIDE="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) PARTNER_ID="$1"; shift ;;
    esac
done

[[ -z "${PARTNER_ID:-}" ]] && usage

readonly LOG_FILE="$LOG_DIR/${PARTNER_ID}-${TIMESTAMP}.log"
readonly STATE_FILE="$STATE_DIR/${PARTNER_ID}.state"

mkdir -p "$LOG_DIR" "$STATE_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

log() { echo "[$(date +'%H:%M:%S')] $*"; }
fatal() { log "FATAL: $*"; exit 1; }

# ──────────────────────────────────────────────────────────────────────────────
# Pre-flight checks
# ──────────────────────────────────────────────────────────────────────────────

preflight() {
    log "Pre-flight checks..."
    for cmd in bw gh git curl jq; do
        command -v "$cmd" >/dev/null 2>&1 || fatal "$cmd not installed (see PROVISIONING-SPEC.md §Required CLI tooling)"
    done
    [[ -f "$FIRM_CONFIG" ]] || fatal "$FIRM_CONFIG not found (see PROVISIONING-SPEC.md §Inputs)"

    # Verify Bitwarden CLI is unlocked.
    bw status | jq -e '.status == "unlocked"' >/dev/null 2>&1 || fatal "Bitwarden CLI is locked. Run 'bw login' or 'bw unlock' first."

    # Verify GPG signing key.
    git config --get user.signingkey >/dev/null 2>&1 || fatal "Git signing key not configured. See governance/SECRETS-POLICY.md."

    log "Pre-flight checks passed."
}

# ──────────────────────────────────────────────────────────────────────────────
# Configuration loading (yq required for full YAML parsing; falls back to grep)
# ──────────────────────────────────────────────────────────────────────────────

readonly FIRM_NAME="$(grep '^firm_name:' "$FIRM_CONFIG" | cut -d'"' -f2)"
readonly GITHUB_ORG="$(grep '^github_org:' "$FIRM_CONFIG" | cut -d'"' -f2)"
readonly BRAIN_REPO="$(grep '^brain_repo:' "$FIRM_CONFIG" | cut -d'"' -f2)"
readonly TRACK_DEFAULT="$(grep '^track:' "$FIRM_CONFIG" | cut -d'"' -f2)"
readonly TRACK="${TRACK_OVERRIDE:-$TRACK_DEFAULT}"

# Firm slug (used for the default Ledger clone path <firm-slug>-ledger); falls back
# to the GitHub org name if firm_slug isn't set in firm.yaml.
FIRM_SLUG="$(grep '^firm_slug:' "$FIRM_CONFIG" | cut -d'"' -f2)"
[[ -n "$FIRM_SLUG" ]] || FIRM_SLUG="$GITHUB_ORG"
readonly FIRM_SLUG

[[ "$TRACK" =~ ^(cloud|privacy)$ ]] || fatal "Invalid track: $TRACK"

log "Provisioning partner '$PARTNER_ID' for firm '$FIRM_NAME' (track: $TRACK)"

# ──────────────────────────────────────────────────────────────────────────────
# State management (idempotency)
# ──────────────────────────────────────────────────────────────────────────────

step_completed() { grep -q "^step_$1:done$" "$STATE_FILE" 2>/dev/null; }
mark_step_done() { echo "step_$1:done" >> "$STATE_FILE"; }
clear_step() { sed -i.bak "/^step_$1:done$/d" "$STATE_FILE" 2>/dev/null || true; }

# ──────────────────────────────────────────────────────────────────────────────
# Interactive partner inputs
# ──────────────────────────────────────────────────────────────────────────────

collect_partner_inputs() {
    echo
    echo "Partner inputs (will be confirmed before any action):"
    read -rp "  Cohort (full-time-partner / project-specialist / advisor): " COHORT
    read -rp "  Email (cloud) or wallet address (privacy): " CONTACT
    read -rp "  GitHub username: " GITHUB_USERNAME
    read -rp "  Two-worlds-of-code (vibe-coder / agentic-engineer / non-code): " TWO_WORLDS
    read -rp "  Jurisdiction (ISO country code): " JURISDICTION
    echo
    echo "Confirming inputs:"
    echo "  Partner ID:       $PARTNER_ID"
    echo "  Cohort:           $COHORT"
    echo "  Contact:          $CONTACT"
    echo "  GitHub:           $GITHUB_USERNAME"
    echo "  Two-worlds:       $TWO_WORLDS"
    echo "  Jurisdiction:     $JURISDICTION"
    echo
    read -rp "Proceed? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Cancelled by operator."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 1 — Bitwarden vault entry
# ──────────────────────────────────────────────────────────────────────────────

step_1_bitwarden() {
    log "Step 1 — Bitwarden vault entry"
    if step_completed 1; then log "Step 1 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would create Bitwarden collection 'partner-$PARTNER_ID' and onboarding stub item."; mark_step_done 1; return; fi

    # Determine cohort collection.
    case "$COHORT" in
        full-time-partner) COHORT_COLLECTION="all-partners" ;;
        project-specialist) COHORT_COLLECTION="specialists" ;;
        advisor) COHORT_COLLECTION="advisors" ;;
        *) fatal "Unknown cohort: $COHORT" ;;
    esac

    # The Bitwarden CLI for organisation collection management is project-specific.
    # In a real implementation, this section uses `bw create org-collection-membership`.
    # The exact invocation depends on the firm's Bitwarden organisation_id from firm.yaml.
    log "  Adding partner to '$COHORT_COLLECTION' collection (manual via Bitwarden web UI in v1.0; programmatic in v1.x)..."
    log "  Creating per-partner collection 'partner-$PARTNER_ID'..."
    log "  TODO(v1.x): replace this manual prompt with full programmatic Bitwarden CLI invocation."
    read -rp "  Confirm Bitwarden steps completed manually [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 1 not completed."

    mark_step_done 1
    log "Step 1 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 2 — GitHub org membership and repo access
# ──────────────────────────────────────────────────────────────────────────────

step_2_github() {
    log "Step 2 — GitHub org membership"
    if step_completed 2; then log "Step 2 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would invite $GITHUB_USERNAME to $GITHUB_ORG and assign cohort team."; mark_step_done 2; return; fi

    case "$COHORT" in
        full-time-partner) TEAM_SLUG="full-time-partners" ;;
        project-specialist) TEAM_SLUG="project-specialists" ;;
        advisor) TEAM_SLUG="advisors" ;;
    esac

    log "  Inviting $GITHUB_USERNAME to $GITHUB_ORG..."
    gh api -X PUT "/orgs/$GITHUB_ORG/memberships/$GITHUB_USERNAME" -f role=member

    log "  Assigning to team '$TEAM_SLUG'..."
    gh api -X PUT "/orgs/$GITHUB_ORG/teams/$TEAM_SLUG/memberships/$GITHUB_USERNAME"

    if [[ "$COHORT" == "full-time-partner" ]]; then
        log "  Granting Ledger push access..."
        gh api -X PUT "/repos/$BRAIN_REPO/collaborators/$GITHUB_USERNAME" -f permission=push
    fi

    mark_step_done 2
    log "Step 2 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 3 — Slack invite (cloud) or 4thtech onboarding (privacy)
# ──────────────────────────────────────────────────────────────────────────────

step_3_comms() {
    log "Step 3 — Comms invite (track: $TRACK)"
    if step_completed 3; then log "Step 3 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would issue $TRACK comms invite to $CONTACT."; mark_step_done 3; return; fi

    if [[ "$TRACK" == "cloud" ]]; then
        SLACK_TOKEN="$(bw get item slack-workspace-admin | jq -r '.notes')"
        log "  Sending Slack invite to $CONTACT..."
        curl -sf -X POST "https://slack.com/api/users.admin.invite" \
            -H "Authorization: Bearer $SLACK_TOKEN" \
            --data-urlencode "email=$CONTACT" >/dev/null
        log "  Adding to default channels..."
        # TODO: programmatic invite to default channels via slack admin API
    else
        log "  4thtech onboarding (privacy track):"
        log "    1. Run: 4thtech invite-dchat --workspace <firm-workspace> --wallet $CONTACT"
        log "    2. Run: 4thtech grant-dmail --to $CONTACT --domain <firm-domain>"
        read -rp "  Confirm 4thtech invitations sent [y/N] " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 3 not completed."
    fi

    mark_step_done 3
    log "Step 3 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 4 — Google Workspace seat (cloud) or PollinationX read access (privacy)
# ──────────────────────────────────────────────────────────────────────────────

step_4_storage() {
    log "Step 4 — Storage / workspace (track: $TRACK)"
    if step_completed 4; then log "Step 4 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would provision $TRACK storage/workspace for $CONTACT."; mark_step_done 4; return; fi

    if [[ "$TRACK" == "cloud" ]]; then
        log "  Google Workspace: provision seat via Admin Console."
        log "  TODO(v1.x): programmatic via Google Admin SDK."
        read -rp "  Confirm seat provisioned + welcome email sent [y/N] " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 4 not completed."
    else
        log "  PollinationX: grant read access:"
        log "    Run: pollinationx grant-read --nft <storage-nft> --to $CONTACT"
        read -rp "  Confirm PollinationX access granted [y/N] " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 4 not completed."
    fi

    mark_step_done 4
    log "Step 4 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 5 — Brain folder stub (signed commit + PR)
# ──────────────────────────────────────────────────────────────────────────────

step_5_brain() {
    log "Step 5 — Brain folder stub"
    if step_completed 5; then log "Step 5 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would create Brain folder stub for $PARTNER_ID."; mark_step_done 5; return; fi

    # The partner's firm/partners/<id>/ tree is operational state — it lives in the
    # Ledger repo (<firm-slug>-ledger), not the Firm Brain. Default clone path derived
    # from the firm slug; override with LEDGER_REPO_PATH.
    LEDGER_REPO_PATH="${LEDGER_REPO_PATH:-$HOME/${FIRM_SLUG:-firm}-ledger}"
    [[ -d "$LEDGER_REPO_PATH" ]] || fatal "Ledger not found at $LEDGER_REPO_PATH (set LEDGER_REPO_PATH env var)"

    cd "$LEDGER_REPO_PATH"
    git checkout -b "onboarding/$PARTNER_ID"

    mkdir -p "firm/partners/$PARTNER_ID"/{output-specs,variable-statements,long-tail-statements,private,legal,onboarding}
    touch "firm/partners/$PARTNER_ID/output-specs/.gitkeep"
    touch "firm/partners/$PARTNER_ID/variable-statements/.gitkeep"
    touch "firm/partners/$PARTNER_ID/long-tail-statements/.gitkeep"
    touch "firm/partners/$PARTNER_ID/private/.gitkeep"

    # Create profile stub
    cat > "firm/partners/$PARTNER_ID/profile.md" <<EOF
---
title: "$PARTNER_ID"
slug: partners/$PARTNER_ID/profile
domain: firm
type: partner-profile
partner_id: $PARTNER_ID
cohort: $COHORT
start_date: $(date +%Y-%m-%d)
jurisdiction: $JURISDICTION
two_worlds_self_id: $TWO_WORLDS
created: $(date +%Y-%m-%d)
updated: $(date +%Y-%m-%d)
authors: [founder, $PARTNER_ID]
status: active
---

# $PARTNER_ID

Stub created at onboarding. Partner edits this page to fill in details.

(See \`templates/brain/partner-profile.md\` for the full template.)
EOF

    # Create reward-species stub (will be filled in by step 6)
    cat > "firm/partners/$PARTNER_ID/reward-species-declaration.md" <<EOF
---
title: "Reward Species Declaration — $PARTNER_ID"
slug: partners/$PARTNER_ID/reward-species-declaration
domain: firm
type: reward-species-declaration
partner_id: $PARTNER_ID
status: stub
---

# Reward Species Declaration — $PARTNER_ID

**Status:** stub. Step 6 of provisioning fills this in after the X2 sheet is populated and the PDF is signed.
EOF

    git add "firm/partners/$PARTNER_ID/"
    git commit -S -m "Onboard partner: $PARTNER_ID

Brain folder stub created per templates/partner-onboarding/PROVISIONING-SPEC.md step 5.
Cohort: $COHORT. Jurisdiction: $JURISDICTION. Two-worlds: $TWO_WORLDS.

The reward-species-declaration is a stub; step 6 will fill it in after the X2 sheet
and signed PDF land."
    git push origin "onboarding/$PARTNER_ID"

    log "  Opening PR..."
    gh pr create \
        --title "Onboard partner: $PARTNER_ID" \
        --body "Provisioning script step 5: Brain folder stub. Reviewer: $GITHUB_USERNAME (the partner being onboarded)." \
        --reviewer "$GITHUB_USERNAME"

    cd - >/dev/null
    mark_step_done 5
    log "Step 5 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 6 — Reward Species Declaration anchoring
# ──────────────────────────────────────────────────────────────────────────────

step_6_reward_species() {
    log "Step 6 — Reward Species Declaration anchoring"
    if step_completed 6; then log "Step 6 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would populate X2 + generate signed PDF."; mark_step_done 6; return; fi

    log "  Manual steps required (Gen 1):"
    log "    1. Open the firm's Ledger copy firm/excel/reward-species-declaration.xlsx (X2) in your spreadsheet viewer."
    log "    2. Add a sheet named '$PARTNER_ID' (or per-partner workbook for >20 partners)."
    log "    3. Populate Partner_Profile + Base_Variable_Split per the on-screen agreement."
    log "    4. Validate: variable weights sum to 1.0; bonus splits sum to 1.0."
    log "    5. Generate signed PDF (founder + partner sign)."
    log "    6. Commit signed PDF to Brain at firm/partners/$PARTNER_ID/legal/reward-species-$(date +%Y-%m-%d).pdf"
    log "    7. Update reward-species-declaration.md to reference the X2 row + PDF."
    read -rp "  Confirm Reward Species Declaration completed [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 6 not completed."

    mark_step_done 6
    log "Step 6 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 7 — Curator self-test (partner runs this)
# ──────────────────────────────────────────────────────────────────────────────

step_7_curator_self_test() {
    log "Step 7 — Curator self-test (partner runs)"
    if step_completed 7; then log "Step 7 already completed; skipping."; return; fi

    cat <<EOF

Partner runs the following on their own machine:
  1. Install the Curator desktop app from https://github.com/talirezun/the-curator/releases/latest
  2. Configure cloud-LLM ingest with the firm's API key (founder provides via Bitwarden Send).
  3. Add the firm Ledger as the Curator's sync target.
  4. Run \`scan_wiki_health\` — should return clean.
  5. Open firm/partners/$PARTNER_ID/profile.md and add one personal note.
  6. Commit, push.

Founder watches; if any step fails, debug there and then.

EOF
    read -rp "Confirm partner has completed the Curator self-test [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Step 7 not completed. Partner is NOT onboarded until this succeeds."

    mark_step_done 7
    log "Step 7 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Step 8 — Notification + roster update
# ──────────────────────────────────────────────────────────────────────────────

step_8_notification() {
    log "Step 8 — Notification + roster update"
    if step_completed 8; then log "Step 8 already completed; skipping."; return; fi
    if $DRY_RUN; then log "[dry-run] Would post welcome message + update partners/index.md."; mark_step_done 8; return; fi

    if [[ "$TRACK" == "cloud" ]]; then
        SLACK_TOKEN="$(bw get item slack-workspace-admin | jq -r '.notes')"
        MESSAGE="Welcome to the partnership, [[partners/$PARTNER_ID]]. Cohort: \`$COHORT\`. First Output Spec: drafting."
        curl -sf -X POST "https://slack.com/api/chat.postMessage" \
            -H "Authorization: Bearer $SLACK_TOKEN" \
            --data-urlencode "channel=general" \
            --data-urlencode "text=$MESSAGE" >/dev/null
    else
        log "  Privacy track: post welcome to 4thtech dChat #general manually."
        log "  Suggested message: 'Welcome to the partnership, [[partners/$PARTNER_ID]]. Cohort: $COHORT. First Output Spec: drafting.'"
    fi

    log "  TODO: programmatic update of firm/partners/index.md (manual in v1.0)."
    mark_step_done 8
    log "Step 8 done."
}

# ──────────────────────────────────────────────────────────────────────────────
# Rollback (de-onboarding)
# ──────────────────────────────────────────────────────────────────────────────

rollback() {
    log "Rolling back onboarding for partner '$PARTNER_ID'..."
    log "  This is a destructive operation. It will:"
    log "    - Remove $PARTNER_ID from GitHub org and teams."
    log "    - Revoke Slack/dChat access."
    log "    - Revoke Google Workspace seat / PollinationX access."
    log "    - Mark the Brain folder \`firm/partners/$PARTNER_ID/\` with status: archived."
    log "    - Remove Bitwarden collection memberships."
    log "  It will NOT delete the Brain folder (history is preserved)."
    log "  It will NOT recover paid variable pay (per framework discipline)."
    read -rp "Proceed with rollback? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || fatal "Rollback cancelled."

    log "TODO: implement rollback step-by-step (v1.x). Manual rollback procedure documented in PROVISIONING-SPEC.md §rollback."
    rm -f "$STATE_FILE"
}

# ──────────────────────────────────────────────────────────────────────────────
# Main flow
# ──────────────────────────────────────────────────────────────────────────────

main() {
    case "$ACTION" in
        rollback)
            rollback
            ;;
        provision|resume)
            preflight
            collect_partner_inputs
            step_1_bitwarden
            step_2_github
            step_3_comms
            step_4_storage
            step_5_brain
            step_6_reward_species
            step_7_curator_self_test
            step_8_notification
            log ""
            log "✓ Onboarding complete for $PARTNER_ID."
            log "  State file: $STATE_FILE"
            log "  Log file: $LOG_FILE"
            log "  Next: complete the partner-onboarding checklist (templates/partner-onboarding/checklist.md) week 1 onwards."
            ;;
    esac
}

main
