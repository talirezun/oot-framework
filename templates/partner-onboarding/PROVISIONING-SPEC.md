# Partner Provisioning — SPEC

What `templates/partner-onboarding/provisioning-script.sh` (generated in Phase 4) does, exactly. The script is deliberately shell-only — every step is reproducible by hand if the script breaks.

The provisioning happens during the 90-minute onboarding session. It is the *last* step of the session — the partner has by that point read MANIFESTO.md, signed the Reward Species Declaration, and the Partner Charter. Provisioning is mechanical follow-through.

---

## Pre-requisites (founder-side, one-time)

Before any partner is provisioned, the firm has:

- A Bitwarden organisation (or 1Password Business) with collections per the structure in `governance/SECRETS-POLICY.md`.
- A GitHub organisation with at least one repo (the firm Ledger) and the `Owner` access scoped to the founder's Yubikey-protected admin account.
- A Slack workspace (cloud track) or 4thtech wallet identity for the firm (privacy track).
- A Google Workspace tenant (cloud track) or PollinationX storage allocation (privacy track).
- The Curator desktop app installed on the founder's machine and pointed at the firm Ledger.

All credentials needed by the provisioning script live in Bitwarden under the `founders` collection. The script reads via the `bw` CLI (`bw get item <name>`) — never via plaintext config files.

---

## Required CLI tooling on the provisioner's machine

The script invokes:

| Tool | Source | Purpose |
|---|---|---|
| `bw` | [bitwarden.com/help/cli](https://bitwarden.com/help/cli/) | Manage Bitwarden vault entries and collections |
| `gh` | [cli.github.com](https://cli.github.com/) | GitHub org membership, team assignments, repo access |
| `git` | shipped with macOS / brew | Commit the partner's Brain stub |
| `curl` | shipped | Slack admin API + ad-hoc HTTPS |
| `jq` | brew install jq | Parse JSON responses (Slack admin API, Bitwarden) |
| `op` (optional) | [1password.com/cli](https://1password.com/downloads/command-line/) | If the firm uses 1Password instead of Bitwarden — script auto-detects |

Privacy-track equivalents:

| Tool | Replaces | Privacy-track purpose |
|---|---|---|
| `4thtech` CLI | Slack admin API | Issue dChat invite + dMail address to the partner's wallet |
| `pollinationx` CLI | Drive sharing | Grant the partner read access to firm bulk storage |
| `ssh-keygen` + `gpg` | — | Generate the partner's signing key for the audit-log branch |

The Phase 4 generator selects the correct toolchain per the firm's track.

---

## Inputs

The script takes one argument — the partner's canonical `partner_id` (lowercase-hyphenated, e.g. `jane-doe`). Everything else is read from a config file at `~/.oot/firm.yaml` (committed to the firm's *private* configuration repo, **not** the public framework repo):

```yaml
firm_name: "Acme Cooperative"
github_org: "acme-coop"
brain_repo: "acme-coop/brain"
track: "cloud"  # or "privacy"

bitwarden:
  organization_id: "<uuid>"
  collections:
    founders: "<uuid>"
    all-partners: "<uuid>"
    specialists: "<uuid>"
    advisors: "<uuid>"
    shared-services: "<uuid>"

slack:
  workspace_admin_token_bw_item: "slack-workspace-admin"  # name of the BW item
  default_channels: ["general", "output-log", "business-review", "klarna-test", "compensation"]

google:
  workspace_admin_token_bw_item: "google-workspace-admin"
  shared_drive_id: "0A..."

# Privacy track only:
fourthtech:
  firm_dmail: "acme@4th.tech"
  firm_dchat_workspace: "acme-coop"
pollinationx:
  storage_nft: "0x..."
```

The partner-side input is a small interactive prompt:

```
Partner ID: jane-doe
Cohort (full-time-partner / project-specialist / advisor): full-time-partner
Email (cloud) or wallet address (privacy): jane@example.com
GitHub username: janedoe
Two-worlds-of-code self-id (vibe-coder / agentic-engineer / non-code): agentic-engineer
Jurisdiction (ISO country code): SI
```

The partner enters these once; the script confirms before executing.

---

## Steps the script performs

### Step 1 — Bitwarden vault entry

1. `bw login` (interactive — Yubikey-touched).
2. `bw create org-collection-membership` to add the partner to the appropriate collection per cohort:
   - `full-time-partner` → `all-partners` + a per-partner private collection `partner-<id>`.
   - `project-specialist` → `specialists` + per-partner private collection.
   - `advisor` → `advisors` + per-partner private collection.
3. `bw create item` for the partner's per-partner collection: a stub item named `oot-onboarding-{{partner_id}}` containing the firm's onboarding-resources URL and the partner's reward-species declaration link. Used to verify the partner can actually log in.
4. Print the partner's first-login one-time token (Bitwarden generates this; the partner exchanges it for a personal Master Password on first login).

**Failure modes handled:**
- Bitwarden CLI not authenticated → script aborts, instructs the founder to run `bw login` manually.
- Partner ID collision (already exists) → script aborts; founder must resolve manually (either reactivate the existing entry or use a different ID).

### Step 2 — GitHub org membership and repo access

1. `gh api -X PUT /orgs/{{github_org}}/memberships/{{github_username}} -f role=member` — invites the partner to the org.
2. `gh api -X PUT /orgs/{{github_org}}/teams/<cohort>/memberships/{{github_username}}` — adds to the cohort's team. Teams are pre-configured by the founder per the cohort:
   - `full-time-partners` team → push access to all firm repos.
   - `project-specialists` team → push access to the specific project's repos only.
   - `advisors` team → read-only by default.
3. The partner accepts the invitation in their email; the script polls until membership is `active` (timeout 24 hours; the partner can be reminded by Slack/dMail later).
4. `gh api -X PUT /repos/{{brain_repo}}/collaborators/{{github_username}} -f permission=push` — explicit push access to the Ledger (full-time partners only).

### Step 3 — Slack invite (cloud) or 4thtech onboarding (privacy)

**Cloud:**
1. `curl POST https://slack.com/api/users.admin.invite` with the workspace admin token and the partner's email.
2. The partner receives a Slack invite email.
3. The script subscribes the partner to the firm's default channels via `conversations.invite`.

**Privacy:**
1. `4thtech invite-dchat --workspace {{firm_dchat_workspace}} --wallet {{partner_wallet_address}}` — issues an on-chain invite signed by the firm's wallet.
2. `4thtech grant-dmail --to {{partner_wallet_address}} --domain {{firm_dmail_domain}}` — provisions the partner's `<id>@<firm-domain>` dMail address.
3. The partner receives the invite in their 4thtech client (the partner must already have a Trezor-backed 4thtech wallet — see Skill Pack S12).

### Step 4 — Google Workspace seat (cloud) or PollinationX read access (privacy)

**Cloud:**
1. `gcloud admin directory users insert` (or REST API) — provisions the partner's `<id>@<firm-domain>` email + Drive seat.
2. Adds them to the firm's shared drive.
3. Sends them the welcome email with the standard onboarding doc.

**Privacy:**
1. `pollinationx grant-read --nft {{storage_nft}} --to {{partner_wallet}}`.
2. The partner can now read the firm's bulk storage on PollinationX from their PollinationX client.

### Step 5 — Brain folder stub

1. `git -C {{brain_repo_clone}} checkout -b onboarding/{{partner_id}}`.
2. Create the partner's Brain folder structure per `templates/brain/FIRM-ONTOLOGY.md`:
   ```
   firm/partners/<partner_id>/
   ├── profile.md                  (from templates/brain/partner-profile.md, populated)
   ├── reward-species-declaration.md  (stub linking to the X2 row + signed PDF in firm storage)
   ├── output-specs/.gitkeep
   ├── variable-statements/.gitkeep
   ├── long-tail-statements/.gitkeep
   └── private/.gitkeep
   ```
3. Commit with a signed commit (`git commit -S` — the founder's GPG key is configured pre-onboarding).
4. Push the branch.
5. Open a PR titled `Onboard partner: {{partner_id}}` with the partner as a reviewer (so they see the structure being created on their behalf and can ack it).

### Step 6 — Reward Species Declaration anchoring

1. Open `templates/excel/reward-species-declaration.xlsx` in the firm's instance (cloud: Google Sheets via API; privacy: Excel MCP).
2. Append a new sheet (named `<partner_id>`) populated from the on-screen onboarding answers.
3. Generate a signed PDF from the new sheet (cloud: Google Apps Script; privacy: a small Python script using openpyxl + reportlab in `installer/privacy/`).
4. Upload the PDF to the firm's storage (Drive folder `partners/{{partner_id}}/legal/` or PollinationX equivalent).
5. Update the partner's `reward-species-declaration.md` Brain stub with wikilinks to (a) the X2 sheet row, (b) the signed PDF storage URL.

### Step 7 — Initial Curator self-test (the partner runs this themselves)

The script does *not* execute on the partner's machine. It outputs a one-page checklist the partner runs themselves with the founder watching (the last 15 minutes of the onboarding session):

1. Install the Curator desktop app from `https://github.com/talirezun/the-curator/releases/latest`.
2. Configure cloud-LLM ingest with the firm's API key (founder provides via Bitwarden Send — one-time link, expires after first use).
3. Add the firm Ledger as the Curator's sync target.
4. Run `scan_wiki_health` — should return clean (no broken wikilinks at the partner's freshly created stub).
5. Open `firm/partners/<id>/profile.md` and add one personal note to confirm write access works.
6. Commit, push.

If any step fails, the founder helps debug there and then. The partner is not "onboarded" until step 6 succeeds.

### Step 8 — Notification

The script posts to Slack `#general` (cloud) or 4thtech dChat `#general` (privacy):

> Welcome to the partnership, [[partners/{{partner_id}}]]. Reward species: `{{reward_species}}`. Cohort: `{{cohort}}`. First Output Spec: drafting. First Friday Business Review: this week if before Tuesday, next week otherwise.

And opens an entry in the firm's `firm/partners/index.md` so the partnership has a single roster page that's never out of date.

---

## Acceptance criteria for the generated `provisioning-script.sh`

- POSIX-compatible shell (`#!/usr/bin/env bash`, `set -euo pipefail`).
- Idempotent at every step (re-running with the same `partner_id` short-circuits steps that have already been completed; never silently overwrites).
- Every step logs to `~/.oot/onboarding-logs/{{partner_id}}-{{timestamp}}.log`.
- Every step has a "rollback" sub-command (`./provisioning-script.sh rollback <partner_id>`) that undoes that step and earlier steps, in reverse order. This is the de-onboarding tool when a partner exits.
- Privacy-track and cloud-track variants share the same script with a track switch flag (`--track cloud` or `--track privacy`); the `firm.yaml` sets the default.
- The script does **not** echo any secret to stdout. All secret retrieval is via `bw get item ... --output-format raw` piped directly into the consuming command.
- The script verifies signed-commit configuration before step 5; aborts if the founder's GPG/SSH key is not loaded.

---

## What the script does *not* do

- It does not draft the Output Spec — that's the partner + founder, in the same session, before provisioning.
- It does not auto-set the partner's variable pay parameters — those come from the signed Reward Species Declaration, which is filled in in the same session.
- It does not enrol the partner in any third-party SaaS the firm hasn't pre-paid for. New SaaS subscriptions are governed by the Decision Rights matrix.
- It does not cover the EU AI Act use-case registration — that's S7 (Governance & Compliance), separately, when an AI use case is created.
