# ØØT Cloud-Track Install Plan (agent-runnable)

**This is an agent-runnable plan.** A coding agent meeting the [capability spec](AGENT-CAPABILITY-SPEC.md) reads this file end-to-end, executes the steps in order against the user's machine, and asks the user the questions marked **🟡 ASK USER** before proceeding past them.

If you (the human) are reading this directly, see [`README.md`](README.md) for context. You don't need to read this whole file — the agent does.

---

## Agent: read this preamble first

You are about to install the ØØT framework on the user's machine for the cloud track. Before you start, internalise these ground rules. They override any default behaviour you have.

### Identity and scope

- You're acting as the framework's installer. You're not free-styling; you're following this plan.
- Your output is a working ØØT Gen-1 cloud install plus a written install summary the user can hand to their accountant or counsel.
- You are NOT a substitute for the user's judgement on firm structure, jurisdiction, partner count, EU AI Act exposure, or anything else this plan asks them about. When in doubt, surface the question; don't decide it.

### Ground rules — non-negotiable

1. **Pause and confirm before any consequential action.** Specifically: creating a GitHub repo, configuring branch protection, generating a cryptographic key, pushing a commit, posting to Slack, sending email, paying for a service, or running `python3 scripts/build_excel.py` against any path other than the framework templates. Surface what you're about to do, why, and the exact command — then wait for the user to type "yes" or equivalent.
2. **Never silently downgrade.** If signed-commit fails, retry with backoff; if still failing, surface the failure and stop. Never push an unsigned commit without the user's explicit "yes, push unsigned".
3. **Honest failure reporting.** If a step fails, tell the user: what you tried, what the actual error was (paste the error text — do not paraphrase), and what you tried as a remedy. Don't summarise success when the action didn't succeed.
4. **Resume from state.** This plan is resumable. After every completed step, update `~/.oot/install-state.yaml` with `step_<N>: done`. On startup, read the state file and skip steps already marked done.
5. **Don't invent inputs.** If the user has not given you their firm name, do not make one up. Ask. The same applies to every template variable in this plan.
6. **Translate technical for the user.** When asking the user a question, frame it for someone who has never opened a JSON file. Don't say "edit `claude_desktop_config.json`'s `mcpServers` block"; say "I'm going to add the my-curator brain interface to Claude Desktop. This means editing one config file. I'll show you the change before I make it. OK to proceed?"
7. **Read before write.** Always read a file before editing it. Always confirm git working-tree state before committing.

### Decision boundary — what you do vs. what the user does

- **You do:** read/write files locally, run shell commands, edit config files, run `git`, generate keys, configure MCPs, run validators, write the install summary.
- **You walk-the-user-through:** creating accounts on third-party services (Anthropic, GitHub, Slack), signing legal documents (Partner Charter, Reward Species Declaration), making firm-structure decisions.
- **You never:** create third-party accounts on the user's behalf using their credentials, sign anything legal, move money, or commit to the user's repo without their explicit approval.

### State file format

Maintain `~/.oot/install-state.yaml`:

```yaml
plan: cloud-install-plan.md
plan_version: 1.0.1
started_at: <ISO8601>
last_updated: <ISO8601>
firm_profile:
  name: "<firm name>"
  partner_count: <int>
  jurisdictions: ["<ISO codes>"]
  eu_high_risk: <yes|no>
  track: cloud
modules_chosen:
  required: [anthropic, github, curator, my_curator_mcp, R5, spreadsheet_app]
  recommended: [...]    # what the user opted into
  deferred: [...]       # what the user opted out of for now
steps_completed:
  step_0_preflight: done | failed | skipped
  step_1_collect_profile: done | failed | skipped
  ...
notes: |
  Any agent observations, things the user manually did,
  fallback paths taken when something failed.
```

After every step, append to `notes` a one-line summary of what was done in that step. The notes field becomes the basis for the install summary at Step 12.

---

## Step 0 — Preflight

**What you're about to do (tell the user):** "Before we start the install, I need to check that your machine has the tools I'll need (`git`, `python3`, `curl`, `gpg`), and confirm you've read the framework's intellectual core. About 5 minutes."

### 0.1 — Verify tools

Run, in order, and capture each result:

```bash
git --version
python3 --version    # must be ≥3.13
curl --version
gpg --version
jq --version || true # nice-to-have, not required
which gh || true     # GitHub CLI; if missing, walk user through install
```

If any required tool is missing, walk the user through installation (macOS: `brew install <tool>`; Linux: `apt install <tool>`; Windows / WSL: per official docs).

If `python3 --version` is < 3.13, surface this clearly: "ØØT requires Python 3.13 or newer. You have <X>. Please install Python 3.13 from https://www.python.org/ before continuing." Stop the plan and wait.

### 0.2 — Confirm framework reading

🟡 **ASK USER:** "Have you read these files in the framework repo? They're 60 minutes of reading total but they're the framework's intellectual core — installing without reading them tends to produce installs that miss the point.
- `MANIFESTO.md` — the five theses with citations
- `governance/KLARNA-TEST.md` — the framework's signature epistemic discipline
- `docs/MODULES.md` — what we're about to install and what's optional

If yes, type `yes`. If you want to read them now, type `wait` and I'll wait. If you want to skip them and risk it, type `skip` (not recommended)."

If `wait`, pause until the user says they've read them.
If `skip`, log this in the state file's `notes` and continue.

### 0.3 — Mark step done

Update state file: `step_0_preflight: done`.

---

## Step 1 — Collect firm profile

**What you're about to do (tell the user):** "I need a few facts about your firm to tailor the install. Six questions, ~3 minutes."

### 1.1 — Ask the questions

🟡 **ASK USER**, one at a time, recording each answer in `firm_profile`:

1. **Firm name.** "What's your firm's name? (e.g. 'Acme Studio'.) This goes in the Brain repo, the partner charter, the Excel templates, and elsewhere. You can change it later but it's a chore."
2. **Partner count.** "How many partners (people who'll be paid via the framework's Output Spec / Reward Species discipline) do you expect in the next 12 months? Solo founder? 2-5? 5+?" Map to `partner_count_estimate: solo | small | medium | large`.
3. **Jurisdictions.** "Where will partners operate? Give me ISO 2-letter country codes, comma-separated. (e.g. `SI,HR` for Slovenia + Croatia, or `US,GB` for US + UK.)"
4. **EU AI Act exposure.** "Are any of your firm's AI use cases likely to be 'high-risk Annex III' under the EU AI Act — meaning AI used in employment decisions, essential public services, biometric ID, etc.? (yes / no / not-sure)"
   - If `not-sure`: "I'll mark this as 'yes, treat as high-risk' until you've reviewed `governance/EU-AI-ACT.md` with counsel. That's the cautious default."
5. **Klarna gate now or later?** "The Klarna Test is the framework's signature pre-merge discipline. The cloud track ships a GitHub Actions workflow (`.github/workflows/klarna-gate.yml`) that blocks PRs labelled `ai-replaces-human` until they pass a 14/20 score. Do you want me to wire this up today (yes), or defer it until you have your first AI-replaces-human PR (later)? Most founders defer it; the workflow ships in the new Brain repo either way."
6. **Anthropic plan.** "What Anthropic plan are you on — Pro (~€20/month, 5 Routine runs/day), Max (~€100/month, 15 runs/day), Team, or Enterprise? Pro is fine for solo or 2-partner firms. **Max is recommended** if you have 3+ partners, plan to use the Klarna gate actively (R7), or run R3 monthly variable + acknowledgement polling fires." If user says Pro and `partner_count_estimate ≥ small`, flag: "Pro plan caps at 5 Routine runs/day. Once R3's monthly polling fires kick in (5-7 fires per month) plus your daily Day-1 Routines, you'll exceed Pro's limit. Consider Max."

### 1.2 — Confirm and write

Show the user the collected profile and confirm before proceeding:

```
Firm: <name>
Partner count: <count> (~<estimate>)
Jurisdictions: <list>
EU high-risk: <yes|no>
Klarna gate: <now|later>
Anthropic plan: <plan>
```

🟡 **ASK USER:** "Is this correct? (yes / edit)"

If `edit`, re-ask the relevant questions.

### 1.3 — Mark step done + persist

Update state file with `firm_profile` populated and `step_1_collect_profile: done`.

---

## Step 2 — Module selection

**What you're about to do (tell the user):** "Based on your firm profile, I'll recommend a Day-1 module set. You can override any of it. Read [`docs/MODULES.md`](../../docs/MODULES.md) if you want the full picture; or trust the recommendation and confirm."

### 2.1 — Recommend the module set

Apply this logic and present the recommendation:

**Required (always):** Anthropic + GitHub Brain repo + Curator + my-curator MCP + S1 skill + R5 + spreadsheet app (user choice)

**Recommended on top, based on profile:**

- If `eu_high_risk == yes`: add **R6 + branch protection + signing key + S7 + X7** (Day-1 mandatory for EU founders)
- If `eu_high_risk == no` AND user is in EU jurisdictions: still add **R6 + branch protection + signing key** (recommended; cheap once configured)
- If `klarna_gate_choice == now`: add **R7 + Klarna gate workflow + auto-labeller + branch-protection-required `oot/klarna-test` status check + S4 + S6 + X4**
- If `partner_count_estimate ≥ small`: surface that **R1 + first partner onboarding (Charter + X2 + first Output Spec)** is Day-7 work and confirm the user wants Day-1 to include the partner-onboarding scaffold
- Always: ask whether user wants **Bitwarden** (recommended for any firm) and **Yubikey** (recommended once user has 2+ admins). Do NOT recommend Trezor unless the user is on the privacy track.

🟡 **ASK USER:** "Here's the Day-1 module set I recommend for your profile. Anything you want to add or skip? (Trezor is intentionally not in this list — it's only needed for Generation 2 stablecoin payroll. Bitwarden / Yubikey are recommended but optional in Gen 1.)"

### 2.2 — Persist the choice

Update state file with `modules_chosen.required`, `modules_chosen.recommended`, `modules_chosen.deferred` populated, and `step_2_module_selection: done`.

---

## Step 3 — Anthropic account check

**What you're about to do (tell the user):** "I'll verify your Anthropic account is on the right plan and Claude Desktop is installed. If not, I'll walk you through the signup."

### 3.1 — Check Claude Desktop

Run:
```bash
ls /Applications/Claude.app 2>/dev/null && echo "macOS Claude Desktop found"
ls ~/AppData/Local/AnthropicClaude 2>/dev/null && echo "Windows Claude Desktop found"
which claude 2>/dev/null && echo "Claude Code CLI found"
```

If neither Claude Desktop nor Claude Code is installed:

🟡 **ASK USER:** "Claude Desktop is not installed. Open https://claude.com/download and install it for your platform. Sign in with your Anthropic account (the plan from Step 1). When done, type `done`."

Wait until user types `done`. Re-run the checks.

### 3.2 — Check Claude Code (optional but recommended)

If Claude Code CLI is missing:

🟡 **ASK USER:** "Claude Code CLI isn't installed. It's how the Day-1 Routines will be configured (`/schedule` command). I recommend installing it: https://docs.claude.com/en/docs/claude-code. Type `done` when installed, or `skip` to defer."

If `done`, verify with `claude --version`. If `skip`, log it and continue (the user can configure Routines via the web dashboard at `claude.com/routines` instead).

### 3.3 — Mark step done

`step_3_anthropic: done`.

---

## Step 4 — GitHub Brain repo creation

**What you're about to do (tell the user):** "I'll create a private GitHub repo for your firm's Brain. This is where the markdown wiki AND the .xlsx state files live (per ADR-001). I'll configure branch protection and copy the framework's Excel templates as the initial state. About 10 minutes."

### 4.1 — Verify GitHub CLI auth

Run:
```bash
gh auth status
```

If not authenticated:

🟡 **ASK USER:** "GitHub CLI is not authenticated. Run `gh auth login` and choose your account. Tell me when done."

### 4.2 — Pick repo name

🟡 **ASK USER:** "What should I name the Brain repo? Suggestion: `<firm-slug>-brain` (lowercase, hyphenated). For example, if your firm is 'Acme Studio', I'll suggest `acme-studio-brain`. Type a name or `accept` for the suggestion."

Capture as `BRAIN_REPO_NAME`. Verify it doesn't already exist:

```bash
gh repo view <user>/<BRAIN_REPO_NAME> 2>/dev/null && echo "EXISTS" || echo "OK to create"
```

If it exists, ask the user whether to use the existing repo or pick a different name.

### 4.3 — Create the repo

🟡 **ASK USER:** "I'm about to create a **private** GitHub repo at `<user>/<BRAIN_REPO_NAME>`. Confirm? (yes / no)"

On `yes`:
```bash
gh repo create <user>/<BRAIN_REPO_NAME> --private --description "ØØT firm Brain repo for <firm name>" --add-readme
gh repo clone <user>/<BRAIN_REPO_NAME> ~/oot-brain
cd ~/oot-brain
```

### 4.4 — Scaffold the Brain folder structure

Create:
```bash
mkdir -p firm/excel firm/output-logs firm/audit-logs firm/business-reviews firm/klarna-tests firm/compensation firm/brain-health firm/partners
```

### 4.5 — Copy framework Excel templates

```bash
cp <FRAMEWORK_REPO>/templates/excel/*.xlsx firm/excel/
```

Replace `<FRAMEWORK_REPO>` with the path the user has the framework cloned at (typically `~/oot-framework`). If unclear, ask.

### 4.6 — Initial commit

🟡 **ASK USER:** "I'm about to commit the initial Brain folder structure + the framework's 9 Excel templates as the firm's starting state. The first commit will be unsigned (the signing key isn't generated yet — that's the next step). Confirm? (yes / no)"

On `yes`:
```bash
git add firm/
git commit -m "scaffold: initial Brain folder structure + Excel templates from framework v1.0.0"
git push origin main
```

### 4.7 — Mark step done

`step_4_brain_repo: done`. Persist `BRAIN_REPO_NAME` and `BRAIN_REPO_PATH` in state file.

---

## Step 5 — Signing key + branch protection

**What you're about to do (tell the user):** "I'll generate a GPG signing key, upload it to GitHub, and configure branch protection on the Brain repo's main branch (force-push off, deletion off, signed commits required). This makes every future commit auditable. About 10 minutes."

### 5.1 — Decide identity

🟡 **ASK USER:** "Should the signing key be tied to your personal GitHub identity, or to a dedicated `oot-bot` GitHub user? Bot identity is recommended (cleaner audit trail; Routines run as the bot, not as you). If bot: you'll need to create the bot account on GitHub and invite it to your firm — I'll walk you through it. Choose: `personal` or `bot`."

If `bot`: walk the user through creating the GitHub bot account (open https://github.com/signup in a fresh browser; pick a name like `<firm-slug>-bot`; verify email; invite to the firm's GitHub org as a member). Wait for confirmation.

### 5.2 — Generate the signing key

```bash
gpg --batch --quick-generate-key "ØØT bot <oot-bot@<firm-domain>>" rsa4096 cert,sign 0
gpg --list-secret-keys --keyid-format LONG <bot email>
```

Capture the key ID.

### 5.3 — Upload to GitHub

```bash
gpg --armor --export <key id>
```

🟡 **ASK USER:** "I'll paste this GPG public key block to your GitHub account at https://github.com/settings/gpg/new. Confirm? (yes / no)"

On `yes`:
```bash
gh gpg-key add - <<< "$(gpg --armor --export <key id>)"
```

### 5.4 — Configure git for signed commits

```bash
git config --global user.signingkey <key id>
git config --global commit.gpgsign true
```

### 5.5 — Configure branch protection

🟡 **ASK USER:** "I'll now set branch protection on `main`: force-push disabled, deletion disabled, signed commits required, ≥1 reviewer required for `firm/audit-logs/*` paths. Confirm? (yes / no)"

On `yes`:
```bash
gh api -X PUT "/repos/<user>/<BRAIN_REPO_NAME>/branches/main/protection" --input - <<EOF
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_signatures": true
}
EOF
```

### 5.6 — Verify with a signed commit

```bash
cd ~/oot-brain
echo "Signed-commit verification at $(date -u +%FT%TZ)" > firm/.signing-test
git add firm/.signing-test
git commit -S -m "verify: signing key + branch protection configured"
git push origin main
git log --show-signature -1
```

If `git log --show-signature` shows `gpg: Good signature`, the setup is correct.

If push is rejected: surface the actual error to the user. Common causes: signing key not yet propagated (wait 30s, retry); GPG agent not running (`gpg-agent --daemon`); user's git identity doesn't match the GPG key's email (run `git config user.email <bot email>`).

### 5.7 — Mark step done

`step_5_signing: done`. Persist `signing_key_id`, `bot_identity` in state file.

---

## Step 6 — Curator + my-curator MCP

**What you're about to do (tell the user):** "I'll install the Curator desktop app and wire up the my-curator MCP in Claude Desktop. This is the Brain interface — the 17 tools that let Claude read and write your knowledge graph. About 15 minutes."

### 6.1 — Install Curator

```bash
# macOS
curl -L https://github.com/talirezun/the-curator/releases/latest/download/Curator.dmg -o /tmp/Curator.dmg
hdiutil attach /tmp/Curator.dmg
cp -R /Volumes/Curator/Curator.app /Applications/
hdiutil detach /Volumes/Curator
# Linux: download .deb or .AppImage; install per platform
# Windows: walk user through installer
```

🟡 **ASK USER:** "Open the Curator desktop app. Sign in / set up the cloud-LLM ingest provider. Recommended: Gemini Flash Lite (https://aistudio.google.com/ for the API key — generous free tier, ~€0-10/month for heavy use). When the Curator is running and you see the main UI, type `done`."

### 6.2 — Wire my-curator MCP into Claude Desktop

Locate Claude Desktop's config file:

```bash
# macOS
CLAUDE_CONFIG=~/Library/Application\ Support/Claude/claude_desktop_config.json
# Windows
CLAUDE_CONFIG=$APPDATA/Claude/claude_desktop_config.json
# Linux
CLAUDE_CONFIG=~/.config/Claude/claude_desktop_config.json
```

🟡 **ASK USER:** "I'm about to add the my-curator MCP to Claude Desktop's config. I'll show you the exact change before making it. The Curator's onboarding wizard should have shown you a snippet to copy — do you have it, or should I use the default localhost configuration?"

If user has snippet, paste it into the config. Otherwise, use the default:

```json
{
  "mcpServers": {
    "my-curator": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://127.0.0.1:8765/mcp"]
    }
  }
}
```

Read the existing config, add the `my-curator` block, write back. Always backup first:

```bash
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.bak.$(date +%s)"
```

### 6.3 — Restart Claude Desktop

🟡 **ASK USER:** "Quit Claude Desktop fully (Cmd+Q on macOS — closing the window isn't enough), then reopen it. Open a new chat. Click the bottom-left tools icon and look for `my-curator` in the MCP servers list with a green checkmark. Tell me what you see."

If green check: continue.
If red X: surface the failure. Likely cause: Curator app not running, or wrong port. Walk through troubleshooting per [`docs/01-installing-the-curator.md`](../../docs/01-installing-the-curator.md) "Common pitfalls".

### 6.4 — Self-test

🟡 **ASK USER:** "In Claude Desktop, in a fresh chat, paste this and send it:

> Use my-curator. List the available domains.

Tell me what Claude responds."

Expected: Claude calls `list_domains` MCP tool and returns something (empty list `[]` is fine — no domains yet).

If the call fails: troubleshoot per [`docs/01-installing-the-curator.md`](../../docs/01-installing-the-curator.md).

### 6.5 — Add S1 my-curator skill to Claude Desktop project

🟡 **ASK USER:** "Create a Claude Desktop project for your firm (top-left → New project). Name it after your firm. Then drag-and-drop `<FRAMEWORK_REPO>/skills/my-curator/SKILL.md` into the project's documents pane. Tell me when done."

### 6.6 — Mark step done

`step_6_curator: done`.

---

## Step 7 — First Curator domain + initial ingest

**What you're about to do (tell the user):** "I'll create the `firm` domain in Curator and walk you through ingesting your first 5 documents (a contract, a strategic memo, a product spec, a pitch deck, a meeting transcript). About 20 minutes."

### 7.1 — Create the `firm` domain

🟡 **ASK USER:** "In the Curator app: Domains → Create domain. Name: `firm`. Description: `Internal company knowledge`. Click Create. Tell me when done."

### 7.2 — Configure the Curator's GitHub sync

🟡 **ASK USER:** "In the Curator app: Sync → Configure. Point sync at the Brain repo we created (`<user>/<BRAIN_REPO_NAME>`). The Curator will then write its generated wiki pages directly into your Brain repo. Tell me when configured."

### 7.3 — First ingest

🟡 **ASK USER:** "Pick five documents that represent your firm's knowledge. Ideal mix:
1. A recent customer contract
2. A strategic memo (your recent thinking)
3. A product spec or technical document
4. A pitch deck (export to PDF)
5. A meeting transcript (export to text)

In the Curator app: Ingest → drag-and-drop the five files. The Curator will process each via the configured LLM (Gemini Flash Lite or whatever you chose). Tell me when ingestion is complete."

### 7.4 — Health check

In Claude Desktop:

> Use my-curator. scan_wiki_health on domain=firm. scan_semantic_duplicates on domain=firm. Report.

Expected: clean report. If broken wikilinks: walk user through `fix_wiki_issue` for each.

### 7.5 — Mark step done

`step_7_brain_first_ingest: done`.

---

## Step 8 — Configure Day-1 Routines

**What you're about to do (tell the user):** "I'll configure the four Day-1 Routines (R5, R6, R1, R2) in Claude Code. The Routines run on Anthropic's infrastructure on schedule (R5 Sunday 09:00, R6 daily 23:00, R1 daily 18:00, R2 Friday 08:00). About 20 minutes — most of it filling in connector details."

For each Routine, the per-Routine setup checklist is at `routines/cloud/<R>.md`. Walk the user through each one.

### 8.1 — R5 Brain Health Check (do first; no dependencies)

🟡 **ASK USER:** "Open Claude Code in your terminal and run `/schedule`. Or visit https://claude.com/routines. I'll walk you through configuring R5 step by step. Ready?"

Walk through the steps from `routines/cloud/R5.md` setup checklist. The Routine prompt body is at `routines/cloud/R5.md` "## Prompt body".

After the user has saved R5 and manually fired it once, verify:
- Brain repo `firm/brain-health/<YYYY-WW>.md` exists (signed commit on `main`)
- Slack `#brain-health` has a message

If both: R5 is operational.

### 8.2 — R6 EU AI Act Audit Trail

If `eu_high_risk == yes` OR user opted in at Step 2: walk through `routines/cloud/R6.md`. Branch protection is already configured at Step 5; now configure the Routine itself with the bot identity's signing key.

### 8.3 — R1 Daily Output Capture

🟡 **ASK USER:** "R1 captures your firm's daily outputs (commits, PRs, contracts, deals) and appends rows to X1. It needs at least one partner with a populated X2 reward-species sheet. Do you want to: (a) configure R1 now and onboard the first partner today (you, the founder), or (b) defer R1 to Day-7 when you've drafted the first Output Spec?"

If `now`: walk through the partner-onboarding scaffold (Charter + first X2 + first Output Spec) before configuring R1. This adds ~60 minutes to the install.
If `later`: log the deferred step; provide the `routines/cloud/R1.md` setup checklist to the user for when they're ready.

### 8.4 — R2 Weekly BR Prep

R2 needs R1 to have ≥7 days of data. If R1 was just configured, R2 won't produce useful output until the following Friday — but configuring R2 now is fine; it just runs against thin data initially.

🟡 **ASK USER:** "Configure R2 now or defer? If you configured R1, configure R2 now — it'll fire its first useful BR a week from today."

### 8.5 — Mark step done

`step_8_routines: done`. Log which Routines were configured vs. deferred.

---

## Step 9 — (Optional) Klarna gate setup

If the user opted into the Klarna gate at Step 1:

**What you're about to do (tell the user):** "I'll configure the Klarna gate: the GitHub Actions workflow + auto-labeller + branch-protection-required `oot/klarna-test` status check. About 10 minutes."

### 9.1 — Copy the Klarna workflow files

```bash
cd ~/oot-brain
cp <FRAMEWORK_REPO>/.github/workflows/klarna-gate.yml .github/workflows/
cp <FRAMEWORK_REPO>/.github/labeler.yml .github/
git add .github/
git commit -S -m "config: Klarna gate workflow + auto-labeller"
git push origin main
```

### 9.2 — Update branch protection to require the status check

```bash
gh api -X PATCH "/repos/<user>/<BRAIN_REPO_NAME>/branches/main/protection" --input - <<EOF
{
  "required_status_checks": {
    "strict": false,
    "contexts": ["oot/klarna-test"]
  }
}
EOF
```

### 9.3 — Configure R7

Walk through `routines/cloud/R7.md` setup checklist.

### 9.4 — Mark step done

`step_9_klarna: done` (or `skipped` if user deferred).

---

## Step 10 — Smoke test

**What you're about to do (tell the user):** "I'll run a final smoke test that exercises the whole stack end-to-end."

### 10.1 — Verify each module

Run, in order, and report results to the user:

```bash
# Brain repo accessible
git ls-remote git@github.com:<user>/<BRAIN_REPO_NAME>.git | head -3

# Signed commit working
cd ~/oot-brain
git log --show-signature -1 | grep "gpg: Good signature" && echo "✓ signing works"

# Excel templates intact
python3 <FRAMEWORK_REPO>/scripts/build_excel.py --check ~/oot-brain/firm/excel/ 2>&1 || echo "(skip if --check unsupported)"

# my-curator MCP reachable
# (User runs in Claude Desktop: "Use my-curator. list_domains.")

# R5 has fired at least once (or has been manually fired)
ls ~/oot-brain/firm/brain-health/ 2>/dev/null
```

### 10.2 — Final user check

🟡 **ASK USER:** "Do you see Brain pages in `firm/brain-health/`? Do you see commits on `main` signed by the bot identity? Does `my-curator. list_domains` in Claude Desktop return `[firm]`? Report any 'no'."

Address any failures.

### 10.3 — Mark step done

`step_10_smoke_test: done`.

---

## Step 11 — Write the install summary

**What you're about to do (tell the user):** "I'll write a summary of what we did, what's deferred, and what to do next."

Generate `~/.oot/install-summary.md` with the following structure:

```markdown
# ØØT Install Summary — <firm name>

**Track:** cloud
**Installed:** <ISO date>
**By:** agent-assisted install plan v1.0.1
**Driver agent:** <agent name + version>

## Firm profile

- Firm: <name>
- Partner count estimate: <count>
- Jurisdictions: <list>
- EU high-risk: <yes|no>
- Anthropic plan: <plan>

## Modules installed

- ✓ Anthropic <plan>
- ✓ GitHub Brain repo: <user>/<repo>
- ✓ Branch protection: force-push off, deletion off, signed commits required
- ✓ Signing key: <key id> on GitHub identity <bot identity>
- ✓ Curator desktop app + my-curator MCP wired into Claude Desktop
- ✓ S1 my-curator skill loaded in Claude Desktop project
- ✓ First Curator domain `firm` populated with <N> ingested documents
- ✓ Excel templates copied to `firm/excel/` (X1...X9)
- ✓ Routines configured: <list>
  - R5 Brain Health (Sunday 09:00) — fired and verified
  - R6 EU AI Act Audit (daily 23:00) — fired and verified
  - R1 Daily Output (daily 18:00) — configured / deferred
  - R2 Weekly BR Prep (Friday 08:00) — configured / deferred
- <if Klarna>: ✓ Klarna gate workflow + auto-labeller + status-check required
- <if R7>: ✓ R7 Klarna Test trigger configured
- <recommended-but-deferred>: <list>

## What's deferred

- <each deferred module with the doc reference for completing it later>
- E.g.: "First partner onboarding (Charter + X2 + Output Spec) — see `templates/partner-onboarding/checklist.md`. Do this before R1's first useful fire."

## What to do next (in priority order)

1. **<top deferred>** — <when, why>
2. **Read [`docs/03-onboarding-a-partner.md`](docs/03-onboarding-a-partner.md)** if you haven't. Onboard your second partner within 30 days.
3. **Subscribe to [`research/articles/`](research/articles/)** for monthly framework updates.
4. **Check the install for drift weekly** — re-run R5 manually; verify `firm/brain-health/` has a fresh page every Sunday.

## Open follow-ups (the agent flagged these)

<anything from state file's `notes` that surfaced during install>

## Repository

[github.com/<user>/<BRAIN_REPO_NAME>](https://github.com/<user>/<BRAIN_REPO_NAME>) — your firm's Brain.
```

🟡 **ASK USER:** "I've written your install summary at `~/.oot/install-summary.md`. Take 5 minutes to read it, then tell me anything that's wrong or missing."

Edit per user feedback.

### 11.1 — Mark complete

`step_11_summary: done`. Mark the entire plan as complete.

---

## Resumability

If the agent's session ends partway through, the next session reads `~/.oot/install-state.yaml` and resumes at the first non-`done` step. Each step is idempotent: re-running it should be a no-op if already complete.

To restart from scratch: delete `~/.oot/install-state.yaml` and `~/.oot/install-summary.md`. The agent will start at Step 0.

---

## Failure handling — what to do if a step fails

1. The agent surfaces the failure with the actual error text.
2. The agent suggests a fix (consults `docs/07-troubleshooting.md`).
3. The user decides: (a) try the suggested fix, (b) fix it manually then continue, (c) skip the step (with consequences explained), or (d) abort.
4. The agent updates the state file with the outcome.
5. If aborted, the install summary at Step 11 still gets written, listing what was done and what's outstanding.

---

## What this plan does NOT install

- The first partner's signed Charter + signed Reward Species Declaration. These are human-signed legal documents; the agent cannot sign on the user's behalf.
- Long-tail entitlement contracts. These need counsel review (per [`docs/06-when-to-call-a-lawyer.md`](../../docs/06-when-to-call-a-lawyer.md)).
- The firm's OAuth tokens for any third-party service. The user grants OAuth themselves.
- Tier-2 Skill Pack hardening (S7-S11). These remain scaffolds in v1.0; v1.x will harden.
- Trezor + 4thtech + PollinationX. Cloud track does not need them; privacy track is a separate plan at [`privacy-install-plan.md`](privacy-install-plan.md).

End of plan.
