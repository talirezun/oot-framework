# ØØT Cloud-Track Install Plan (agent-runnable)

**Plan version:** 1.1.0 (2026-05-10) — refined from 1.0.0 based on findings from sandbox + live install tests recorded in [`docs/internal/install-test-report-2026-05-10.md`](../../docs/internal/install-test-report-2026-05-10.md).

**This is an agent-runnable plan.** A coding agent meeting the [capability spec](AGENT-CAPABILITY-SPEC.md) reads this file end-to-end, executes the steps in order against the user's machine, and asks the user the questions marked **🟡 ASK USER** before proceeding past them.

If you (the human) are reading this directly, see [`START-HERE.md`](START-HERE.md) for how to invoke this with your coding agent. You don't need to read the whole plan yourself — but skimming it before handing it to the agent gives you a sense of what's coming.

---

## Agent: read this preamble first

You are about to install the ØØT framework on the user's machine for the cloud track. Before you start, internalise these ground rules. They override any default behaviour you have.

### Identity and scope

- You're acting as the framework's installer. You're not free-styling; you're following this plan.
- Your output is a working ØØT Gen-1 cloud install plus a written install summary the user can hand to their accountant or counsel.
- You are NOT a substitute for the user's judgement on firm structure, jurisdiction, partner count, EU AI Act exposure, or anything else this plan asks them about. When in doubt, surface the question; don't decide it.

### Ground rules — non-negotiable

1. **Pause and confirm before any consequential action.** Specifically: creating a GitHub repo, configuring branch protection, generating a cryptographic key, pushing a commit, posting to Slack, sending email, paying for a service, or running `python3 scripts/build_excel.py` against any path other than the framework templates. Surface what you're about to do, why, and the exact command — then wait for the user to type "yes" or equivalent.
2. **Web UI is the canonical user-facing path.** A non-technical founder is more likely to know github.com than `gh` CLI. For every action that has a web UI alternative (repo creation, GPG key upload, branch protection), present the web UI as the primary path. The `gh` CLI is an optional accelerator if the user has it set up.
3. **Never silently downgrade.** If signed-commit fails, retry with backoff; if still failing, surface the failure and stop. Never push an unsigned commit without the user's explicit "yes, push unsigned".
4. **Honest failure reporting.** If a step fails, tell the user: what you tried, what the actual error was (paste the error text — do not paraphrase), and what you tried as a remedy. Don't summarise success when the action didn't succeed.
5. **Resume from state.** This plan is resumable. After every completed step, update `~/.oot/install-state.yaml` with `step_<N>: done`. On startup, read the state file and skip steps already marked done.
6. **Don't invent inputs.** If the user has not given you their firm name, do not make one up. Ask. The same applies to every template variable in this plan.
7. **Translate technical for the user.** When asking the user a question, frame it for someone who has never opened a JSON file. Don't say "edit `claude_desktop_config.json`'s `mcpServers` block"; say "I'm going to add the my-curator brain interface to Claude Desktop. This means editing one config file. I'll show you the change before I make it. OK to proceed?"
8. **Read before write.** Always read a file before editing it. Always confirm git working-tree state before committing.
9. **Clipboard caveat.** Most agent shell sandboxes can't reach the user's actual clipboard. Don't rely on `pbcopy`/`xclip`. To give the user a long string of text (a GPG public key, a config snippet), either (a) print it inline in the chat for the user to copy, or (b) write it to a file and tell the user `open /path/to/file` (macOS) / `xdg-open /path/to/file` (Linux) which opens their default text editor.

### Decision boundary — what you do vs. what the user does

- **You do:** read/write files locally, run shell commands, edit config files, run `git`, generate keys, configure MCPs, run validators, write the install summary.
- **You walk-the-user-through:** creating accounts on third-party services (Anthropic, GitHub, Slack), signing legal documents (Partner Charter, Reward Species Declaration), making firm-structure decisions, **clicking buttons in their browser** (creating GitHub repo, uploading GPG key, configuring branch protection — all primarily web-UI, not CLI).
- **You never:** create third-party accounts on the user's behalf using their credentials, sign anything legal, move money, or commit to the user's repo without their explicit approval.

### State file format

Maintain `~/.oot/install-state.yaml`:

```yaml
plan: cloud-install-plan.md
plan_version: 1.1.0
started_at: <ISO8601>
last_updated: <ISO8601>
firm_profile:
  name: "<firm name>"
  partner_count: <int>
  jurisdictions: ["<ISO codes>"]
  eu_high_risk: <yes|no>
  track: cloud
  github_plan_tier: <free|team|enterprise>
  curator_config: <A_separate|B_unified>
  existing_curator: <yes|no>
locations:
  framework_repo: "<path to cloned framework repo>"
  firm_folder: "<absolute path>"
  curator_vault: "<absolute path; null if Config B>"
  curator_domain: "<domain slug>"
modules_chosen:
  required: [anthropic, github, curator, my_curator_mcp, R5, spreadsheet_app]
  recommended: [...]
  deferred: [...]
steps_completed:
  step_0_preflight: done | failed | skipped
  step_0_5_locations: done | failed | skipped
  step_1_collect_profile: done | failed | skipped
  step_2_module_selection: done | failed | skipped
  step_3_github_plan_choice: done | failed | skipped
  step_4_anthropic_check: done | failed | skipped
  step_5_brain_repo: done | failed | skipped
  step_6_signing_key: done | failed | skipped
  step_7_branch_protection: done | failed | skipped
  step_8_curator: done | failed | skipped
  step_9_brain_first_ingest: done | failed | skipped
  step_10_routines: done | failed | skipped
  step_11_klarna_gate: done | failed | skipped
  step_12_smoke_test: done | failed | skipped
  step_13_install_summary: done | failed | skipped
notes: |
  Any agent observations, things the user manually did,
  fallback paths taken when something failed.
```

---

## Step 0 — Preflight

**What you're about to do (tell the user):** "Before we start the install, I need to check that your machine has the tools I'll need (`git`, `python3.13`, `curl`, `gpg`, `node`), and confirm you've read the framework's intellectual core. About 5 minutes."

### 0.1 — Verify tools

Run, in order, and capture each result:

```bash
git --version
# Python: try 3.13 / 3.12 / 3.11 / system python3 in order; use whichever first satisfies ≥3.11
for cmd in python3.13 python3.12 python3.11 python3; do
    command -v "$cmd" >/dev/null 2>&1 && "$cmd" --version && OOT_PYTHON="$cmd" && break
done
echo "Will use: $OOT_PYTHON"
curl --version | head -1
gpg --version 2>&1 | head -1 || echo "MISSING: gpg"
node --version 2>&1 || echo "MISSING: node"
jq --version 2>&1 || echo "MISSING: jq (nice-to-have, not required)"
gh --version 2>&1 | head -1 || echo "MISSING: gh (optional accelerator; not required)"
```

If `OOT_PYTHON` is unset (no Python ≥3.11 found):

🟡 **ASK USER:** "ØØT requires Python 3.11 or newer. Please install Python 3.13 from https://www.python.org/downloads/ (or via Homebrew on macOS: `brew install python@3.13`). Tell me when done."

If `gpg` or `node` is missing, walk the user through:

- **macOS:** `brew install gnupg node` (run `brew install` itself first if Homebrew missing — get from https://brew.sh).
- **Linux:** `sudo apt install gnupg nodejs` (Debian/Ubuntu) or `sudo dnf install gnupg nodejs` (Fedora).
- **Windows:** install Gpg4win from https://www.gpg4win.org/ and Node.js from https://nodejs.org/, or use WSL.

`gh` and `jq` are optional. `gh` accelerates a couple of steps if installed and authenticated; the plan's web-UI primary path doesn't need it. `jq` is convenient for inspecting JSON; not required.

After install, re-run the checks. Capture the absolute path of `OOT_PYTHON` (e.g. `/opt/homebrew/bin/python3.13`) — it'll be used in subsequent steps and persisted in the state file.

### 0.2 — Confirm framework reading

🟡 **ASK USER:** "Have you read these files in the framework repo? They're 60 minutes of reading total but they're the framework's intellectual core — installing without reading them tends to produce installs that miss the point.

- `MANIFESTO.md` — the five theses with citations
- `governance/KLARNA-TEST.md` — the framework's signature epistemic discipline
- `docs/MODULES.md` — what we're about to install and what's optional

If yes, type `yes`. If you want to read them now, type `wait` and I'll wait. If you want to skip them and risk it, type `skip` (not recommended)."

If `wait`, pause until the user says they've read them.
If `skip`, log this in the state file's `notes` and continue.

### 0.3 — Set up Python virtual environment

The framework's scripts use `openpyxl`, `pyyaml`, and others. macOS Homebrew Python 3.13 enforces PEP 668 — `pip install --user` is rejected. Use a venv at `~/.oot/venv/`:

```bash
$OOT_PYTHON -m venv ~/.oot/venv
source ~/.oot/venv/bin/activate
pip install openpyxl pyyaml httpx
```

Verify:
```bash
python -c "import openpyxl; print(f'openpyxl {openpyxl.__version__} OK')"
```

The venv is the install-time agent's code-execution sandbox. Routines themselves (cloud track) run on Anthropic infrastructure where the dependencies are already available; the venv is for the local install + any human-in-the-loop work.

Persist `~/.oot/venv` path in the state file.

### 0.4 — Mark step done

`step_0_preflight: done`. Persist `OOT_PYTHON` (absolute path) and the venv path.

---

## Step 0.5 — Choose locations

**What you're about to do (tell the user):** "Three folder questions. Where the firm's operational stuff lives, where your knowledge graph (Curator) lives, and how the two relate. About 3 minutes."

### 0.5.1 — Firm operational repo path

🟡 **ASK USER:** "Where should the firm's operational repo live on your local machine? This is the folder that will hold the `.xlsx` state files (X1...X9), the markdown Brain pages that Routines write (output logs, audit logs, partner profiles), and that gets pushed to GitHub for backup + Routine access.

Default: `~/<firm-slug>` (e.g. `~/acme-studio` if your firm is 'Acme Studio').

You can pick anywhere. Some founders prefer:
- `~/firms/<firm-slug>` if you might run multiple firms
- `/Users/<you>/<firm-slug>` (full path)
- Anywhere else with read/write access

Type the path, or 'default' for `~/<firm-slug>`."

Capture as `FIRM_FOLDER`. Verify the parent exists and is writable. Don't create the folder yet — that happens at Step 5.

### 0.5.2 — Existing Curator detection

🟡 **ASK USER:** "Do you already have the Curator desktop app installed and a 'second-brain' folder set up?

If yes: I'll integrate this firm install with your existing Curator (faster, no reinstall, you keep your existing knowledge graph).

If no / not sure: I'll walk you through installing the Curator from scratch.

(yes / no)"

If yes:

🟡 **ASK USER:** "Where is your Curator vault folder? On a default Curator install this is typically `~/second-brain/` or whatever you chose during the Curator's first-run wizard.

Type the absolute path, or `find` and I'll try to locate it for you."

If `find`:
```bash
ls -d ~/second-brain ~/Documents/second-brain ~/Library/Containers/io.curator/Data/second-brain 2>/dev/null
```

Capture as `CURATOR_VAULT`. Verify the path exists and is a directory.

### 0.5.3 — Curator integration mode (Configuration A vs B)

🟡 **ASK USER:** "There are two valid ways the firm operational repo and the Curator vault can relate:

**Configuration A — Separate (recommended for existing Curator users):**
- Firm operational repo at `<FIRM_FOLDER>` holds `.xlsx` state + Routine-written markdown.
- Curator vault at `<CURATOR_VAULT>` holds your knowledge graph, with this firm as one domain.
- They link via wikilinks but my-curator MCP queries see only Curator vault content. Operational data (output logs, audit logs) is read via direct file/git access.
- This is what the framework's authors use because they had pre-existing second-brains.

**Configuration B — Unified (recommended for greenfield):**
- The firm operational repo IS the Curator vault root.
- `firm/` is a domain inside it.
- my-curator MCP queries see everything — both `.xlsx` state context and Routine-written markdown.
- Cleaner for someone starting fresh; harder to retrofit if you already have a multi-firm Curator.

Which config? (A / B)"

Default: A if `existing_curator == yes`, B otherwise.

If A: ask the user for the existing domain slug they want to use for this firm, OR confirm a new domain will be created. Default: `<firm-slug>`.
If B: the firm folder will become the Curator vault root after Step 8.

### 0.5.4 — Mark step done

Persist `firm_folder`, `curator_vault`, `curator_config` (A/B), `curator_domain` in state file.

`step_0_5_locations: done`.

---

## Step 1 — Collect firm profile

**What you're about to do (tell the user):** "Six questions about the firm. ~3 minutes."

### 1.1 — The questions

🟡 **ASK USER**, one at a time, recording each answer in `firm_profile`:

1. **Firm name.** "What's your firm's full name? (e.g. 'Acme Studio'.) Goes in the Ledger, the partner charter, the Excel templates."
2. **Partner count.** "How many partners do you expect in the next 12 months? Solo? 2-5? 5+? Map to: solo / small / medium / large."
3. **Jurisdictions.** "Where will partners operate? ISO 2-letter country codes, comma-separated (e.g. `SI,HR`)."
4. **EU AI Act exposure.** "Are any of your firm's AI use cases likely to be 'high-risk Annex III' under the EU AI Act — AI used in employment decisions, essential public services, biometric ID, etc.? (yes / no / not-sure)"
   - If `not-sure`: log as `yes` (cautious default) and add to `notes` that user should review `governance/EU-AI-ACT.md` with counsel.
5. **Klarna gate now or later?** "The Klarna Test is the framework's signature pre-merge discipline. Configure today (yes), or defer until the first AI-replaces-human PR comes in (later)? Most defer."
6. **Anthropic plan.** "Pro / Max / Team / Enterprise? Pro is fine for solo / 2-partner with no R7. Max is recommended default for 3+ partners or active Klarna gate. (See [`docs/02-installing-routines.md`](../../docs/02-installing-routines.md) plan-tier guidance.)"

### 1.2 — Confirm + persist

Show collected profile, ask user to confirm or edit.

`step_1_collect_profile: done`.

---

## Step 2 — Module selection

**What you're about to do (tell the user):** "Based on your firm profile, I'll recommend a Day-1 module set. Read [`docs/MODULES.md`](../../docs/MODULES.md) for the full picture."

Apply this logic to recommend the module set:

- **Always required:** Anthropic + GitHub Ledger + Curator + my-curator MCP + S1 + R5 + spreadsheet app
- If `eu_high_risk == yes`: add **R6 + branch protection + signing key + S7 + X7** (Day-1 mandatory for EU)
- If user is in EU jurisdictions and `eu_high_risk == no`: still recommend R6 + branch protection + signing key
- If `klarna_gate_choice == now`: add **R7 + Klarna gate workflow + auto-labeller + branch-protection-required `oot/klarna-test` status check + S4 + S6 + X4**
- If `partner_count_estimate ≥ small`: surface that R1 + first partner onboarding (Charter + X2 + Output Spec) is Day-7 work
- Always: ask whether user wants Bitwarden (recommended any firm) and Yubikey (recommended once 2+ admins). Do NOT recommend Trezor unless privacy track.

🟡 **ASK USER:** "Recommended Day-1 module set: <list>. Anything to add or skip?"

`step_2_module_selection: done`.

---

## Step 3 — GitHub plan-tier choice (CRITICAL)

**What you're about to do (tell the user):** "The framework's audit-trail discipline requires GitHub branch protection to actually be *enforced*. On GitHub Free + private repos, branch protection rules are advisory only — anyone with push access can force-push or push unsigned commits. This affects how robust your firm's audit trail is. ~3 minutes to choose."

### 3.1 — Explain the trade-off

🟡 **ASK USER:** "Three valid configurations:

1. **GitHub Team plan** ($4/user/month) — branch protection enforces on private repos. Recommended for any firm taking R6 (EU AI Act audit trail) seriously, or that holds customer data. Cost: $48/year/user.

2. **GitHub Public repo + Free plan** — branch protection enforces on personal Free, but your firm's operational data (X1 partner output, X2 reward species declarations including salaries, customer references in Output Specs) is publicly visible to anyone on the internet. Acceptable only for fully-open-source orgs. Cost: free, but typically wrong fit.

3. **GitHub Free + private repo + procedural discipline** — branch protection rule is created but advisory only; honour-system enforcement. Acceptable for solo founders or 2-person shops who trust each other; not acceptable once you have 3+ committers or hold customer data. Cost: free.

Which? (team / public / free)"

Capture as `firm_profile.github_plan_tier`. If `team`: surface that the user needs to upgrade their GitHub plan (https://github.com/settings/billing/plans) before Step 7 (branch protection configuration).

### 3.2 — Mark step done

`step_3_github_plan_choice: done`.

---

## Step 4 — Anthropic account check

**What you're about to do (tell the user):** "I'll verify your Anthropic account is on the right plan and Claude Desktop / Claude Code are installed. ~5 minutes."

### 4.1 — Check Claude Desktop

```bash
ls /Applications/Claude.app 2>/dev/null && echo "macOS Claude Desktop found"
ls "$HOME/AppData/Local/AnthropicClaude" 2>/dev/null && echo "Windows Claude Desktop found"
which claude 2>/dev/null && echo "Claude Code CLI found"
```

If neither installed:

🟡 **ASK USER:** "Claude Desktop is not installed. Open https://claude.com/download in your browser, install for your platform, and sign in with your Anthropic account. Type `done` when running."

### 4.2 — Check Claude Code (recommended)

If `claude` CLI missing:

🟡 **ASK USER:** "Claude Code CLI isn't installed. It's the most common way to configure Day-1 Routines (`/schedule` command). Install it: https://docs.claude.com/en/docs/claude-code. Type `done` when installed, or `skip` to use the web dashboard at https://claude.ai/code/routines instead. Either path works — Routines run on Anthropic's cloud regardless."

`step_4_anthropic_check: done`.

---

## Step 5 — Create GitHub Ledger + initial scaffold

**What you're about to do (tell the user):** "I'll create the firm's Ledger GitHub repo, scaffold the local folder structure, and copy the framework's Excel templates as the initial state. The repo will be private. About 10 minutes."

### 5.1 — Create the repo on GitHub.com (web UI — primary path)

🟡 **ASK USER:** "Open https://github.com/new in your browser and create the repo. I'll give you exact settings:

- **Repository name:** `<firm-slug>-brain` (e.g. `acme-studio-brain`). Or whatever you'd prefer — but keep it descriptive.
- **Description:** `ØØT framework Ledger for <firm name>`
- **Visibility:** **Private** (or Public if you chose Configuration `public` at Step 3)
- **Initialize this repository with:** ☐ DO NOT add a README, .gitignore, or licence — leave all three checkboxes UNCHECKED. We need an empty repo to push our scaffold into.

Click **Create repository**. Tell me the URL of the new repo (looks like `https://github.com/<you>/<repo-name>.git`)."

**(Optional accelerator if user has `gh auth status` working):**
```bash
gh repo create <user>/<repo-name> --private --description "ØØT Ledger for <firm>" 2>&1
```

Persist as `LEDGER_REPO_URL`. If user provided HTTPS URL, that's what we'll use for cloning.

### 5.2 — Create the local firm folder

```bash
mkdir -p "<FIRM_FOLDER>"
cd "<FIRM_FOLDER>"
git init -b main
git config user.name "<user's name; ask if not in global config>"
git config user.email "<user's email — see 5.3 below>"
git remote add origin "<LEDGER_REPO_URL>"
```

### 5.3 — Email matters for signed commits

🟡 **ASK USER:** "GitHub marks commits as 'Verified' (green badge) only when the commit's author email matches the GPG key's email. Two questions:

1. What email should we use for commit authorship in this repo? Options:
   - Your real email (cleanest; signed commits show as Verified)
   - GitHub's `noreply` address (e.g. `<id>+<user>@users.noreply.github.com`) — keeps your real email private but signed commits won't get Verified badge until you also add this address as a UID on the GPG key

2. Same email for the GPG key we'll generate at Step 6? (Default yes)

For test installs: a real email works fine and avoids the Verified-badge complication. For founders who want privacy: stick with the noreply address but plan to add it as a GPG key UID at Step 6."

Persist as `BRAIN_REPO_EMAIL` (local to this repo only — never modify global git config).

```bash
git config --local user.email "<BRAIN_REPO_EMAIL>"
```

### 5.4 — Scaffold folder structure

```bash
mkdir -p firm/excel firm/output-logs firm/audit-logs firm/business-reviews firm/klarna-tests firm/compensation firm/brain-health firm/partners
touch firm/output-logs/.gitkeep firm/audit-logs/.gitkeep firm/business-reviews/.gitkeep firm/klarna-tests/.gitkeep firm/compensation/.gitkeep firm/brain-health/.gitkeep firm/partners/.gitkeep
```

### 5.5 — Copy framework Excel templates

```bash
cp <FRAMEWORK_REPO>/templates/excel/*.xlsx firm/excel/
ls firm/excel/   # should show 9 files
```

### 5.6 — Write the firm Ledger README

Generate a `README.md` at the firm folder root:

```markdown
# <firm name> — operational Ledger

ØØT framework cloud-track install. Holds the firm's `.xlsx` operational state (`firm/excel/`) and Routine-written markdown (`firm/output-logs/`, `firm/audit-logs/`, etc.). Mutated by Routines via openpyxl + signed commits per [ADR-001](https://github.com/talirezun/oot-framework/blob/main/docs/internal/ADR-001-cloud-routine-excel-writeback.md).

Curator integration: <Configuration A: separate vault at <CURATOR_VAULT> / Configuration B: this folder IS the Curator vault>.

Created: <ISO date>. Plan version: 1.1.0.
```

### 5.7 — Initial commit (unsigned — signing key not yet generated)

```bash
git add .
git commit -m "scaffold: initial Brain folder + Excel templates from framework v1.0.0"
```

🟡 **ASK USER:** "I'm about to push the initial scaffold to your new GitHub repo at <LEDGER_REPO_URL>. The first commit is unsigned (we generate the signing key in the next step). Confirm? (yes / no)"

```bash
git push -u origin main
```

### 5.8 — Verify

🟡 **ASK USER:** "Open <LEDGER_REPO_URL> in your browser. You should see the README + the `firm/` folder with 9 .xlsx files. Confirm?"

`step_5_brain_repo: done`. Persist `LEDGER_REPO_URL`, `BRAIN_REPO_PATH` in state file.

---

## Step 6 — Generate signing key + upload to GitHub

**What you're about to do (tell the user):** "I'll generate a GPG signing key (so your commits get the green Verified badge on GitHub) and walk you through uploading the public part to your GitHub account. ~5 minutes."

### 6.1 — Generate the key (no passphrase for ease; production keys SHOULD have a passphrase)

```bash
cat > /tmp/oot-gpg-batch.txt <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: <firm name> Bot
Name-Comment: ØØT installation - <ISO date>
Name-Email: <BRAIN_REPO_EMAIL>
Expire-Date: 1y
%commit
EOF
gpg --batch --gen-key /tmp/oot-gpg-batch.txt 2>&1
rm /tmp/oot-gpg-batch.txt
gpg --list-secret-keys --keyid-format LONG | head -10
```

Capture the **key ID** (the 16-character hex string after `rsa4096/` on the `sec` line).

🟡 **ASK USER:** "Generated GPG signing key with ID `<KEY_ID>`. This is a 1-year-expiry test/scaffolding key with no passphrase — convenient for the install. **For production, you should generate a separate key with a passphrase + pinentry.** Acknowledge and proceed? (yes / no)"

### 6.2 — Export the public key + give it to the user

The agent's shell can't reach the user's clipboard reliably. Two options to give the user the key block:

**Option A — print inline in chat:**
```bash
gpg --armor --export <KEY_ID>
```

Print the output directly in the chat for the user to select-and-copy.

**Option B — open the user's text editor:**
```bash
gpg --armor --export <KEY_ID> > /tmp/oot-gpg-public.asc
# macOS:
open /tmp/oot-gpg-public.asc
# Linux:
xdg-open /tmp/oot-gpg-public.asc
```

Tell the user the file is now open in TextEdit / their default text editor; they can Cmd+A, Cmd+C to copy.

🟡 **ASK USER:** "I'll print the public key block in the chat. Select it (everything from `-----BEGIN PGP PUBLIC KEY BLOCK-----` through `-----END PGP PUBLIC KEY BLOCK-----` inclusive) and copy. Then:

1. Open https://github.com/settings/gpg/new in your browser.
2. **Title:** `<firm name> Bot — ØØT signing key`
3. **Key:** paste the block.
4. Click **Add GPG key** and confirm with your password.

Tell me `done` when uploaded. If GitHub rejects the key (rare, but happens with non-ASCII characters in UID), let me know and I'll regenerate with ASCII-only fields."

### 6.3 — Configure git to sign commits in this repo

```bash
cd "<FIRM_FOLDER>"
git config --local user.signingkey <KEY_ID>
git config --local commit.gpgsign true
git config --local gpg.program $(which gpg)
```

### 6.4 — Verify with a real signed commit

```bash
echo "Signed-commit verification at $(date -u +%FT%TZ)" > firm/.signing-test
git add firm/.signing-test
git commit -S -m "verify: signing key works on this repo"
git log --show-signature -1 | head -6
```

Look for `gpg: Good signature` in the output. If yes, push:

```bash
git push origin main
```

### 6.5 — Verify on GitHub

🟡 **ASK USER:** "Open `<LEDGER_REPO_URL>/commits/main`. The latest commit (`verify: signing key works on this repo`) should have a green `Verified` badge. Confirm?

If you see a yellow `Unverified` or no badge: the email on the GPG key doesn't match the email on the commit author. Tell me what email is on the GPG key and what email is on the commit and I'll reconcile."

### 6.6 — Mark step done

`step_6_signing_key: done`. Persist `signing_key_id` in state file.

---

## Step 7 — Branch protection (web UI)

**What you're about to do (tell the user):** "I'll walk you through configuring branch protection on the Ledger. This is what enforces 'no unsigned commits, no force-pushes, no branch deletion' — the discipline R6's audit-trail relies on. About 5 minutes."

### 7.1 — Surface the GitHub-Free caveat (Finding 16)

If `firm_profile.github_plan_tier == free`:

🟡 **ASK USER:** "**Important:** GitHub Free private repos do *not* enforce branch protection rules — the rule is advisory only, and force-pushes / unsigned commits will still be accepted by the server. We'll create the rule anyway (it's structurally correct for the day you upgrade), but R6's audit-trail-immutability claim doesn't hold until you upgrade to GitHub Team or move the repo to a public state.

Acknowledge and proceed? (yes — I understand the limitation / no — I'll upgrade now)"

If user wants to upgrade, walk them to https://github.com/settings/billing/plans and wait for `done`.

### 7.2 — Create the branch protection rule (web UI)

🟡 **ASK USER:** "Open `<LEDGER_REPO_URL>/settings/branches` in your browser. Click **Add classic branch protection rule** (or **Add ruleset** in the newer UI — either works for our needs).

**Branch name pattern:** `main`

Configure these checkboxes EXACTLY as below:

| Checkbox | State | Why |
|---|---|---|
| Require pull request before merging | ☐ unchecked | Allow direct commits during install + Routine fires |
| Require linear history | ☐ unchecked | Routines may need merge commits |
| Require deployments to succeed before merging | ☐ unchecked | Not relevant for ØØT |
| Lock branch | ☐ unchecked | Allow Routine writes |
| **Require signed commits** | ☑ **CHECKED** | Reject unsigned commits — ADR-001 keystone |
| Do not allow bypassing the above settings | ☐ unchecked | Admins can bypass in emergencies |
| **Allow force pushes** | ☐ **UNCHECKED** | Force-push rewrites history; we want immutable history |
| **Allow deletions** | ☐ **UNCHECKED** | Branch deletion would erase audit trail |

Click **Create**. Tell me `done` when saved."

### 7.3 — Verify (only meaningful on Team+ plans)

If `github_plan_tier == team` or higher:

```bash
cd "<FIRM_FOLDER>"
# Try to push an unsigned commit; should be rejected.
echo "should be rejected" > /tmp/unsigned-test.txt
git config --local commit.gpgsign false
echo "test unsigned" > firm/.unsigned-test
git add firm/.unsigned-test
git commit -m "test: should be rejected by branch protection"
git push origin main 2>&1 | tail -5
```

If push is rejected with "GH006: Protected branch update failed for refs/heads/main" or "Required signed commit": branch protection is enforced. Roll back the test:

```bash
git reset HEAD~1
rm firm/.unsigned-test
git config --local commit.gpgsign true
```

If push is accepted: surface to user that branch protection is NOT enforcing, even though the rule is set. Possible cause: GitHub Free private. Repeat Finding 16 caveat.

### 7.4 — Mark step done

`step_7_branch_protection: done`. Persist `branch_protection_enforced: <yes|no>` in state file.

---

## Step 8 — Curator integration

**What you're about to do (tell the user):** "I'll wire up the my-curator MCP and configure the Curator app for this firm. The exact steps depend on whether you already have Curator (Step 0.5.2) and which configuration you chose (Step 0.5.3). About 15 minutes."

### Branch 8A — Existing Curator + Configuration A (separate roots)

User already has Curator + second-brain at `<CURATOR_VAULT>`. We add a new domain for this firm but don't touch the firm operational repo's MCP wiring (because in Config A, my-curator MCP only sees the Curator vault).

#### 8A.1 — Verify my-curator MCP is wired in Claude Desktop

🟡 **ASK USER:** "In Claude Desktop, open a new chat and paste this:

> Use my-curator. List the available domains.

Tell me what Claude responds — does it list your existing domains?"

If yes: my-curator MCP is configured. Continue.
If no: walk through MCP installation (skip to Branch 8B's MCP setup).

#### 8A.2 — Create the new firm domain

If the user-chosen `curator_domain` doesn't already exist:

🟡 **ASK USER:** "I'll create a new domain `<curator_domain>` in your Curator vault at `<CURATOR_VAULT>/domains/<curator_domain>/`. In the Curator app, navigate to Domains → Create domain → name `<curator_domain>` → Description `<firm name>`. Tell me `done`."

#### 8A.3 — Verify the domain is visible from my-curator MCP

🟡 **ASK USER:** "In Claude Desktop, paste:

> Use my-curator. List the available domains. Then call get_index for the domain `<curator_domain>`.

Tell me what Claude responds. The new domain should be in the list, and `get_index` should return an empty domain (no entities/concepts/summaries yet)."

### Branch 8B — Greenfield + Configuration B (unified root)

User has no existing Curator. Install Curator and use the firm operational repo as the Curator vault root.

#### 8B.1 — Install Curator

```bash
# macOS
curl -L https://github.com/talirezun/the-curator/releases/latest/download/Curator.dmg -o /tmp/Curator.dmg
hdiutil attach /tmp/Curator.dmg
cp -R /Volumes/Curator/Curator.app /Applications/
hdiutil detach /Volumes/Curator
# Linux: download .deb or .AppImage; install per platform
# Windows: walk user through installer
```

🟡 **ASK USER:** "Open the Curator desktop app. In the first-run wizard, when it asks for the vault folder, choose `<FIRM_FOLDER>`. Configure cloud-LLM ingest with Gemini Flash Lite (https://aistudio.google.com/ for the API key — generous free tier). Tell me `done` when the Curator's main UI is showing."

#### 8B.2 — macOS filesystem permissions (Finding 10)

🟡 **ASK USER:** "macOS may have prompted for filesystem permission when the Curator first accessed `<FIRM_FOLDER>`. If you see the Curator's main UI but can't see your firm folder's contents in the domains list:

1. System Settings → Privacy & Security → Files and Folders
2. Find Curator in the list
3. Toggle access for the relevant folders ON
4. Restart the Curator

Tell me `done` once you can see the firm folder in the Curator's domains list."

#### 8B.3 — Wire my-curator MCP into Claude Desktop

In the Curator app's first-run wizard, copy the MCP config snippet shown. Open Claude Desktop's config file:

```bash
# macOS
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
# Linux
CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
# Windows
CLAUDE_CONFIG="$APPDATA/Claude/claude_desktop_config.json"
```

Backup first:
```bash
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.bak.$(date +%s)"
```

Read existing config; add the `my-curator` block to `mcpServers`; write back.

If the config file doesn't exist, create it:
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

🟡 **ASK USER:** "Quit Claude Desktop fully (Cmd+Q on macOS — closing the window isn't enough). Reopen. Open a new chat. Click the bottom-left tools icon and look for `my-curator` in the MCP servers list with a green checkmark. Tell me what you see."

If green check: continue. If red X: walk through troubleshooting per [`docs/01-installing-the-curator.md`](../../docs/01-installing-the-curator.md).

#### 8B.4 — Self-test

🟡 **ASK USER:** "In Claude Desktop, paste:

> Use my-curator. List the available domains.

Tell me what Claude responds."

#### 8B.5 — Add S1 my-curator skill to Claude Desktop project

🟡 **ASK USER:** "Create a Claude Desktop project for `<firm name>` (top-left → New project). Drag-and-drop `<FRAMEWORK_REPO>/skills/my-curator/SKILL.md` into the project's documents pane. Tell me `done`."

### 8.x — Mark step done

`step_8_curator: done`. Persist `curator_config` and `curator_domain` if not already set.

---

## Step 9 — Initial Brain ingest

**What you're about to do (tell the user):** "Pick five existing documents that represent your firm's knowledge. The Curator ingests them into your domain. About 20 minutes."

(Same content as Step 7 of the v1.0 plan — unchanged.)

🟡 **ASK USER:** "Pick:
1. A recent customer contract
2. A strategic memo (your recent thinking)
3. A product spec or technical document
4. A pitch deck (export to PDF)
5. A meeting transcript (export to text)

In the Curator app: Ingest → drag-and-drop. Tell me when ingestion is complete."

Then health check:

🟡 **ASK USER:** "In Claude Desktop:

> Use my-curator. scan_wiki_health on domain=<curator_domain>. scan_semantic_duplicates on domain=<curator_domain>. Report.

Expected: clean report. Walk through `fix_wiki_issue` for any broken wikilinks."

`step_9_brain_first_ingest: done`.

---

## Step 10 — Configure Day-1 Routines

**What you're about to do (tell the user):** "I'll walk you through configuring R5 (and optionally R6, R1, R2) in Claude Code Routines. About 20-30 minutes."

For each Routine, follow the per-Routine setup checklist at `routines/cloud/<R>.md`. Pause-and-confirm at each.

R5 first (no dependencies):

🟡 **ASK USER:** "Open Claude Code → run `/schedule`. Or visit https://claude.ai/code/routines. Or use the Claude Code desktop app's 'New Remote Task' feature. Configure R5 per the checklist at `routines/cloud/R5.md`. Use the prompt body from that file. Attach the `my-curator` Skill Pack. Configure the GitHub connector pointing at `<LEDGER_REPO_URL>` (with the bot identity's signing key). Manual fire to test. Verify a signed commit lands on `main` adding `firm/brain-health/<YYYY-WW>.md`. Tell me `done`."

Repeat for R6, R1, R2 if user opted in at Step 2.

`step_10_routines: done`. Log which Routines configured vs. deferred.

---

## Step 11 — (Optional) Klarna gate

If `klarna_gate_choice == now` at Step 1:

```bash
cd "<FIRM_FOLDER>"
cp <FRAMEWORK_REPO>/.github/workflows/klarna-gate.yml .github/workflows/
cp <FRAMEWORK_REPO>/.github/labeler.yml .github/
git add .github/
git commit -S -m "config: Klarna gate workflow + auto-labeller"
git push origin main
```

Update branch protection in the web UI to require `oot/klarna-test` status check (`<LEDGER_REPO_URL>/settings/branches` → edit rule → add required status check).

Configure R7 per `routines/cloud/R7.md`.

`step_11_klarna_gate: done` (or `skipped`).

---

## Step 12 — Smoke test

**What you're about to do (tell the user):** "Final end-to-end check: every module reachable, signed commits flowing, Pattern C verified."

```bash
cd "<FIRM_FOLDER>"
source ~/.oot/venv/bin/activate

# 1. Ledger accessible
git ls-remote "<LEDGER_REPO_URL>" | head -3

# 2. Signed commit working
git log --show-signature -1 | grep "gpg: Good signature" && echo "✓ signing works"

# 3. All 9 Excel templates open via openpyxl
python -c "
import openpyxl
from pathlib import Path
brain = Path('<FIRM_FOLDER>') / 'firm' / 'excel'
ok = 0
fail = 0
for f in sorted(brain.glob('*.xlsx')):
    try:
        wb = openpyxl.load_workbook(f)
        sheets = len(wb.sheetnames)
        wb.close()
        ok += 1
        print(f'  ✓ {f.name} — {sheets} sheets')
    except Exception as e:
        fail += 1
        print(f'  ✗ {f.name} — {e}')
print(f'Result: {ok} ok, {fail} fail')
exit(0 if fail == 0 else 1)
"

# 4. Pattern C live test (R1's actual operation)
python -c "
import openpyxl
from datetime import date
from pathlib import Path
X1 = Path('<FIRM_FOLDER>') / 'firm' / 'excel' / 'partner-output-ledger.xlsx'
wb = openpyxl.load_workbook(X1)
ws = wb['Output_Log']
r = 2
while ws.cell(r, 1).value:
    r += 1
ws.cell(r, 1, f'OL-{date.today().strftime(\"%Y%m%d\")}-SMOKE')
ws.cell(r, 2, date.today())
ws.cell(r, 3, '[SAMPLE]-smoke-test')
ws.cell(r, 4, 'commit')
ws.cell(r, 5, 'install-smoke')
ws.cell(r, 6, '[[outputs/install-smoke-test]]')
ws.cell(r, 7, 'L')
ws.cell(r, 8, 0)
ws.cell(r, 9, 'No')
ws.cell(r, 10, 1.0)
ws.cell(r, 11, f'=VLOOKUP(G{r},\$O\$2:\$P\$5,2,FALSE)')
ws.cell(r, 12, f'=K{r}*J{r}*IF(I{r}=\"Yes\",0,1)')
wb.save(X1)
print(f'✓ Pattern C: appended row {r} to X1 with K and L formulas')
"

git add firm/excel/partner-output-ledger.xlsx
git commit -S -m "smoke: Pattern C live test row appended"
git push origin main && echo "✓ smoke commit pushed"
```

🟡 **ASK USER:** "Smoke results: <list each step's outcome>. Open `<LEDGER_REPO_URL>/commits/main` and verify the latest commit has the green Verified badge. Confirm?"

🟡 **ASK USER:** "In Claude Desktop, paste:

> Use my-curator. List domains.

Verify `<curator_domain>` is in the list. Confirm?"

`step_12_smoke_test: done`.

---

## Step 13 — Write the install summary

(Same as v1.0 plan Step 11 — extends the summary template with `github_plan_tier`, `curator_config`, and any deferred steps logged in `notes`.)

`step_13_install_summary: done`.

---

## Resumability + failure handling

Same as v1.0 — agent reads `~/.oot/install-state.yaml` on startup, resumes from the first non-`done` step. Steps are idempotent.

End of plan v1.1.0.
