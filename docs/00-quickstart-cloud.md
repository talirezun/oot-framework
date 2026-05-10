# 00 — Quickstart: Cloud Track

**Audience:** Founder. Cloud track. Non-technical to moderately-technical.
**Time:** Two weekends (~16 hours) for the manual path. Path A (agent-assisted) cuts this to ~60-90 minutes.
**You will end with:** a fully-operational ØØT instance with one partner onboarded, a real GitHub-hosted Brain repo with signed commits, four scheduled Routines running on Anthropic's infrastructure, and an audit trail you can hand to your accountant or counsel.

> 📖 **Read first:** [`MANIFESTO.md`](../MANIFESTO.md) (15 min), [`docs/MODULES.md`](MODULES.md) (10 min — what to install and what's optional), [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md) (10 min). The framework's discipline starts with reading.

> 🤖 **Faster install path:** if you have a coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, etc.), use [Path A — Coding-agent-assisted install](../installer/agent-assisted/START-HERE.md). The agent reads the install plan and executes it, asking you the questions a human installer would have to answer. ~60-90 minutes wall-clock. **Recommended for ≥80% of founders, especially less-technical ones.** This document (Path C) is for founders who want to type every step themselves or who don't have a coding agent set up.

---

## The non-technical primer

If you've never opened a JSON file, never used a terminal, and don't know what a "signed commit" is — you're in the right place. The framework's whole user story is the founder who knows their craft but doesn't write code. Here's the vocabulary you need, in plain English:

- **Terminal / shell**: an app where you type commands instead of clicking buttons. On macOS it's "Terminal" (Cmd+Space → "Terminal" → Enter). On Windows you'd typically use WSL ("Windows Subsystem for Linux"). You'll use the terminal a few times in this guide; everything else is in your browser or a desktop app.
- **JSON file**: a text file with a specific structure (curly braces, quotes, commas) that apps use for configuration. You'll edit one — `claude_desktop_config.json` — once, and the Curator app gives you the exact text to paste. If you accidentally delete a comma or a quote and the file breaks, the app will tell you and you can fix it.
- **GitHub**: a website (github.com) where files live in version-controlled folders called "repositories" or "repos". Your firm's Brain repo will be private and only you (and partners you invite) can see it. Think of it like Dropbox with full history of every change forever.
- **Git**: the underlying tool that talks to GitHub. You'll run a few git commands; each one is a single line you copy-paste.
- **MCP** (Model Context Protocol): a way for Claude to talk to outside tools — your Brain (via my-curator MCP), GitHub, Slack, etc. The Curator app installs one for you; you wire it into Claude Desktop with one config-file edit.
- **Signed commit**: every change you make to your Brain repo gets a cryptographic signature so anyone can verify it actually came from you (or a partner) and wasn't tampered with. You generate a "signing key" once, upload its public half to GitHub, and from that point every change is signed automatically.
- **Branch protection**: a setting on your GitHub repo that says "no force-pushes, no deletions, only signed commits accepted". This is what makes your audit trail **immutable** — it can't be silently rewritten.
- **Routine**: a Claude Code task that runs automatically on a schedule (daily 18:00, Friday 08:00, etc.). The framework ships eight; you'll set up four on Day-1.

You don't need to memorise any of this. Just refer back when a term shows up in a step.

---

## What this is + the first 5 minutes

ØØT runs on a stack of well-known UI tools:

- **Claude Desktop** — your daily driver, the chat interface
- **Claude Code** — the developer-y version of Claude that runs Routines
- **GitHub** — your firm's Brain repo holds markdown pages and `.xlsx` operational state
- **Slack** — comms (or any chat tool you're already using; framework supports Slack natively)
- **The Curator desktop app** — your knowledge-graph engine
- **A spreadsheet app** of your choice — Microsoft Excel, **LibreOffice (free, open-source)**, Apple Numbers (built into macOS), Excel for Web. The framework writes native `.xlsx` and is app-agnostic; **you don't need Microsoft 365**.

By the end of weekend one: stack installed, Brain repo created with signed commits and branch protection, first Curator domain populated with five sample documents, four Day-1 Routines (R1, R2, R5, R6) configured on Claude Code Routines.

By the end of weekend two: first partner onboarded, first Friday Business Review held, daily output capture flowing into your Brain repo.

If at any step a screenshot doesn't match what you see (Anthropic / GitHub / Slack UIs evolve), trust the UI's labels over the screenshot and let us know via PR.

---

## Before you start — decisions to make first

Don't skip this section. Each decision here affects later steps; making them now saves backtracking.

### 1. Cloud or privacy track?

This guide is the **cloud** path. If you need full sovereignty (4thtech + PollinationX + LM Studio + always-on machine), use [`00-quickstart-privacy.md`](00-quickstart-privacy.md) instead. Most founders should start cloud.

### 2. EU AI Act exposure

Are any of your firm's AI use cases likely to be "high-risk Annex III" (employment decisions, essential public services, biometric ID, etc.)? If yes — or if you're unsure — read [`governance/EU-AI-ACT.md`](../governance/EU-AI-ACT.md) and Skill Pack S7 before any partner ships AI-augmented work. This is also why R6 (daily audit trail) is mandatory for EU founders.

### 3. Where will the firm folder live on your machine?

Your firm's Brain repo gets cloned to a folder on your local machine. Where? Default: `~/<firm-slug>` (e.g. `~/acme-studio` if your firm is "Acme Studio"). Some founders prefer `~/firms/<firm-slug>` if they might run multiple firms, or `~/Documents/<firm-slug>`.

Pick a path now; you'll use it in the install steps. **Anywhere you have read+write access works.**

### 4. Do you already have the Curator second-brain installed?

The Curator desktop app might already be on your machine if you're an existing user.

- **If yes**: you'll add a new domain for this firm to your existing second-brain. No reinstall. (Faster path.)
- **If no**: you'll install the Curator from scratch and the firm folder becomes the Curator's vault.

### 5. Curator integration mode (Configuration A vs B)

Two valid ways the firm operational repo and the Curator vault can relate:

- **Configuration A — Separate** (recommended if you already have a Curator + second-brain): firm operational repo at `~/<firm-slug>/` holds `.xlsx` state and Routine-written markdown. Curator vault stays where it is. They link via wikilinks but don't share a root.
- **Configuration B — Unified** (recommended for greenfield): the firm operational repo IS the Curator's vault root. `firm/` is a domain inside it. my-curator MCP queries see everything.

Pick A if you have an existing second-brain; B otherwise.

### 6. GitHub plan-tier — CRITICAL DECISION ⚠️

**This is the most important structural decision in this whole guide.** GitHub Free private repos do *not* enforce branch protection rules. The rule shows in the UI but it's advisory only — anyone with push access can force-push or push unsigned commits, even with the rule "set."

Three valid configurations:

| Config | Cost | Branch protection enforced? | Suitable for |
|---|---|---|---|
| **GitHub Team** | $4/user/month | ✓ YES | Any firm taking R6 audit trail seriously, or 3+ committers, or holding customer data. **Recommended default.** |
| **GitHub Public repo** | Free | ✓ YES | Fully-open-source orgs only. Your firm's operational data (X1 partner output, X2 reward species declarations including salaries, customer references in Output Specs) becomes publicly readable. **Almost never the right choice for a real firm.** |
| **GitHub Free + private** | Free | ✗ NO (advisory only) | Solo founders or 2-person shops who trust each other. **Acceptable for v1 pilot.** Upgrade to Team before adding the 3rd committer. |

If you're a solo founder doing a pilot: Free is fine for now. Plan to upgrade to Team within 90 days or before adding a third committer, whichever comes first.

### 7. Anthropic plan — Pro vs Max

| Plan | Routine runs/day | Suitable for |
|---|---|---|
| **Pro** (~€20/mo) | 5 | Solo founder or 2-partner firm with no R7 (Klarna gate) activity |
| **Max** (~€100/mo) | 15 | **Recommended default** for 3+ partner firms or any firm with active R7 |
| **Team** | 25 | 5+ partner firms with discretionary ad-hoc Routines |

Steady-state Day-1 daily-routine cost: R1 daily + R6 daily + R2/R5 weekly ≈ 2.3 runs/day average. Pro plan handles this. The moment R3 month-end firing + acknowledgement polling kicks in (5–7 fires per month) or R7 fires on a real PR, you exceed Pro's 5/day. Upgrade to Max before that happens.

### 8. Spreadsheet app

Microsoft Excel (desktop or web), **LibreOffice** (free, open-source, https://www.libreoffice.org/), Apple Numbers (preinstalled on macOS), WPS Office, OnlyOffice — all read native `.xlsx` and work with the framework. Pick one you're comfortable with. **Do not use Google Sheets** as the canonical store — round-trips lose openpyxl-generated formulas and the framework's design (ADR-001) treats `.xlsx` in your GitHub repo as the source of truth.

### Now run the readiness diagnostic

Open `templates/excel/oot-readiness.xlsx` in your spreadsheet app. Score yourself honestly. **Below 60% suggests adoption is premature** — address the lowest-scoring dimension first before continuing.

---

## Weekend One — Saturday morning (2-3 hours): minimum-viable accounts

The Day-1 minimum to operate ØØT cloud track is **three accounts**:

### 1. Anthropic account

Go to https://claude.com/. Sign up. Pick the plan you decided in §7 above. **Pro for solo / 2-partner with no R7; Max for everyone else.**

### 2. GitHub account or organisation

Go to https://github.com/. If you already have a personal GitHub account, fine. If you want a separate org for the firm: https://github.com/account/organizations/new (organisations are free for unlimited public repos and unlimited private repos within plan limits). Apply Apache 2.0 for code repos and CC BY-SA 4.0 for documentation repos by default.

If you chose **Team** in §6 above: upgrade now at https://github.com/settings/billing/plans (or for an org: `https://github.com/organizations/<org>/settings/billing/plans`).

### 3. Slack workspace + Claude integration

Create a Slack workspace at https://slack.com/get-started if you don't have one. Free tier is fine for ≤10 people / 90-day history; upgrade to Pro (€7/user/month) when the firm scales. Install the [Claude Slack integration](https://slack.com/apps/A0848GFRZ54-claude).

That's the minimum. The next three are **recommended-but-optional in Gen 1** — add them later as the firm matures (per CLAUDE.md decision #13):

### 4. Bitwarden organisation account *(recommended; optional in Gen 1)*

[bitwarden.com](https://bitwarden.com/). Best practice for any firm; not gating for solo or 2-partner founders. Beginning founders can use the Bitwarden personal free tier or any password manager that lets them store credentials securely off the browser autofill path. When you do adopt the org tier, create the canonical collections (`founders`, `all-partners`, `specialists`, `advisors`, `shared-services`) per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md).

### 5. Yubikey 5C NFC *(recommended; optional in Gen 1)*

For org-admin 2FA. ~€60. Strongly recommended once the firm has its second admin or holds customer data; not required for a solo founder on Day-1.

### 6. Trezor hardware wallet *(deferred to Gen 2)*

Trezors store crypto keys for the Generation-2 stablecoin payroll path. You don't need one to operate Gen 1 unless you're already on the privacy track. **Beginning founders skip this entirely until v2.0.**

> 💡 **Tip:** Don't save any password to your browser's password manager during this setup. Use a real password manager from the start. Browser autofill is the leak point that destroys the secrets policy six months later.

---

## Weekend One — Saturday afternoon (2-3 hours): install the stack

### 1. Install missing command-line tools

Open Terminal (Cmd+Space → "Terminal" on macOS). Check what's already installed:

```bash
git --version              # should print "git version 2.x"
python3.13 --version       # should print "Python 3.13.x"
gpg --version              # if "command not found", install below
node --version             # if "command not found", install below
curl --version             # already installed on macOS / Linux
```

If `gpg` or `node` are missing:

- **macOS:** Install Homebrew first if you don't have it: https://brew.sh/. Then:
  ```bash
  brew install gnupg node
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt install gnupg nodejs
  ```
- **Linux (Fedora):**
  ```bash
  sudo dnf install gnupg nodejs
  ```
- **Windows / WSL:** install Gpg4win from https://www.gpg4win.org/, Node from https://nodejs.org/, or run all of this inside WSL on Linux.

If `python3.13` is missing:

- **macOS:** `brew install python@3.13`
- **Linux:** install Python 3.13 from your distro's package manager or https://www.python.org/downloads/
- **Windows:** install from https://www.python.org/downloads/

### 2. Set up the framework's Python environment

Homebrew Python 3.13 enforces PEP 668 — you can't `pip install` system-wide. We use a virtual environment (venv) so the framework's Python tools don't conflict with anything else:

```bash
python3.13 -m venv ~/.oot/venv
source ~/.oot/venv/bin/activate     # this activates the venv for your current terminal session
pip install openpyxl pyyaml httpx   # the framework's Python deps
python -c "import openpyxl; print(f'openpyxl {openpyxl.__version__} OK')"
```

You'll need to re-run `source ~/.oot/venv/bin/activate` each time you open a new terminal (or add it to your `~/.zshrc` / `~/.bashrc` to do it automatically).

### 3. Claude Desktop

Download from https://claude.com/download. Install. Sign in with your Anthropic account.

If you use Google Workspace and want the read-only Drive / Calendar / Gmail integration: connect via Settings → Connectors. **Note:** these are read-only; the framework's state lives in GitHub, not Google.

### 4. Claude Code

[Install per Anthropic docs](https://docs.claude.com/en/docs/claude-code). On Max plan you get higher rate limits and unlock the Routines daily quota described above.

### 5. The Curator desktop app

If you decided in §4 of "decisions" that you have an existing Curator: skip ahead to §6 below.

If greenfield: download from https://github.com/talirezun/the-curator/releases/latest. Install. Run the onboarding wizard. **Important — when it asks for the vault folder:**

- **Configuration A (separate):** point at a fresh folder like `~/second-brain/` (or wherever you want your knowledge graph to live, separate from the firm folder).
- **Configuration B (unified):** point at `~/<firm-slug>/` (the firm folder you decided in §3 of "decisions"). Click through the wizard to create it.

Configure cloud-LLM ingest (Gemini Flash Lite recommended for cost; get a free API key at https://aistudio.google.com/). Pay-as-you-go pricing — heavy usage typically stays under €10/month.

#### macOS file permissions (important!)

If macOS asks you to grant the Curator access to your folders, say **yes**. If you accidentally said no: System Settings → Privacy & Security → Files and Folders → Curator → toggle access ON. Then quit and reopen the Curator. Symptom: Curator can't see folders / shows empty domains list when files are clearly there.

### 6. Wire the my-curator MCP into Claude Desktop

In the Curator's wizard (or Settings → Sync), there's an "MCP Setup" step that shows a JSON snippet. **Copy it.** Then:

- **Open Claude Desktop → Settings → Developer → "Edit Config"**. This opens `claude_desktop_config.json` in your default text editor.
- The file might be empty `{}` or have other config already. Find or create the `mcpServers` section. Paste the my-curator block inside it.
- **Save the file.**
- **Quit Claude Desktop completely** (Cmd+Q on macOS — closing the window isn't enough). Reopen.
- In a new chat, click the bottom-left tools icon. You should see `my-curator` in the MCP servers list with a **green checkmark**. If you see a red X, see [`docs/01-installing-the-curator.md`](01-installing-the-curator.md) "Common pitfalls".

### 7. Add the my-curator skill (S1) to Claude Desktop

Locate `skills/my-curator/SKILL.md` in this framework repo. In Claude Desktop, create or open a Project for your firm (top-left → New project). Drag-and-drop SKILL.md into the project documents pane.

Verify: in a new chat in the project, ask:

> Use my-curator. List the available domains.

Expected: Claude calls `list_domains` MCP tool and returns a list (might be empty if you haven't created any domains yet — that's fine).

### 8. (Optional) Obsidian

[obsidian.md](https://obsidian.md/). Free. Point it at your Curator vault folder for a human-readable view. Some founders prefer it; others find Claude Desktop sufficient.

---

## Weekend One — Sunday morning (3-4 hours): scaffold the Brain

This is the most procedural part of the install. Take your time; nothing here is reversible without effort.

### Step 1 — Create the Brain repo on GitHub.com (web UI)

1. Open https://github.com/new in your browser.
2. **Repository name**: `<firm-slug>-brain` (e.g. `acme-studio-brain`).
3. **Description**: `ØØT framework Brain repo for <firm name>`.
4. **Visibility**: **Private** (or Public if you chose `public` in §6 of "decisions").
5. **Initialize this repository with**: ☐ DO NOT add a README, .gitignore, or licence — leave all three checkboxes UNCHECKED. We need an empty repo so we can push our scaffold without a merge conflict.
6. Click **Create repository**.

Note the URL — looks like `https://github.com/<you>/<firm-slug>-brain.git`. You'll use it in Step 2.

### Step 2 — Create the local firm folder + initial scaffold

Open Terminal. **Replace** `<FIRM_FOLDER>` and `<BRAIN_REPO_URL>` with your actual values:

```bash
mkdir -p <FIRM_FOLDER>
cd <FIRM_FOLDER>
git init -b main
git remote add origin <BRAIN_REPO_URL>

# Set local git identity. Use a real email for signed commits to be marked Verified by GitHub.
git config user.name "<Your Name>"
git config user.email "<your-real-email@example.com>"   # match this to the GPG key email in Step 4
```

> **Why local config?** This sets `user.email` only inside this repo, not globally. Your other git work isn't affected. Per Finding 12 of `docs/internal/install-test-report-2026-05-10.md`.

### Step 3 — Scaffold the firm folder structure + copy Excel templates

Still in your Terminal, in the `<FIRM_FOLDER>`:

```bash
mkdir -p firm/excel firm/output-logs firm/audit-logs firm/business-reviews firm/klarna-tests firm/compensation firm/brain-health firm/partners
touch firm/output-logs/.gitkeep firm/audit-logs/.gitkeep firm/business-reviews/.gitkeep firm/klarna-tests/.gitkeep firm/compensation/.gitkeep firm/brain-health/.gitkeep firm/partners/.gitkeep

# Replace ~/oot-framework with wherever you cloned the framework repo
cp ~/oot-framework/templates/excel/*.xlsx firm/excel/
ls firm/excel/   # should show 9 .xlsx files
```

Write a README at the firm folder root:

```bash
cat > README.md <<EOF
# <firm name> — operational Brain repo

ØØT framework cloud-track install. Holds the firm's \`.xlsx\` operational state (\`firm/excel/\`) and Routine-written markdown (\`firm/output-logs/\`, \`firm/audit-logs/\`, etc.). Mutated by Routines via openpyxl + signed commits per [ADR-001](https://github.com/talirezun/oot-framework/blob/main/docs/internal/ADR-001-cloud-routine-excel-writeback.md).

Curator integration: <Configuration A: separate vault / Configuration B: this folder IS the Curator vault>.

Created: $(date +%Y-%m-%d).
EOF
```

Then commit and push (this first commit is unsigned — signing key comes next):

```bash
git add .
git commit -m "scaffold: initial Brain folder + Excel templates from framework v1.0.0"
git push -u origin main
```

If git asks for your GitHub credentials: paste your GitHub username + a Personal Access Token (PAT) from https://github.com/settings/tokens (create one with `repo` scope; macOS will cache it via the `osxkeychain` credential helper).

### Step 4 — Generate a GPG signing key

In Terminal:

```bash
cat > /tmp/oot-gpg-batch.txt <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: <Your Name> (ØØT Bot)
Name-Comment: ØØT installation $(date +%Y-%m-%d)
Name-Email: <your-real-email@example.com>
Expire-Date: 1y
%commit
EOF

gpg --batch --gen-key /tmp/oot-gpg-batch.txt
rm /tmp/oot-gpg-batch.txt
gpg --list-secret-keys --keyid-format LONG
```

The output ends with a 16-character hex string after `rsa4096/` on the `sec` line — that's your **key ID**. Note it.

> **Production note:** the `%no-protection` line above means the key has NO passphrase. Convenient for the install; **for a production key you'd add a passphrase** (replace `%no-protection` with `Passphrase: <your-passphrase>` in the batch file). The framework's authors generated their test key with no passphrase to make the install smoother.

### Step 5 — Upload the public key to GitHub (web UI)

```bash
gpg --armor --export <KEY_ID> > /tmp/oot-gpg-public.asc
open /tmp/oot-gpg-public.asc      # macOS — opens in TextEdit
# Linux: xdg-open /tmp/oot-gpg-public.asc
# Windows: start /tmp/oot-gpg-public.asc
```

Your text editor opens with the public key block. **Cmd+A** to select all, **Cmd+C** to copy.

Then:

1. Open https://github.com/settings/gpg/new in your browser.
2. **Title**: `<firm name> — ØØT signing key`.
3. **Key**: paste with **Cmd+V**.
4. Click **Add GPG key**. GitHub asks for your password; enter it.

If GitHub rejects the key (rare; happens if there are non-ASCII characters in the UID): regenerate the key with ASCII-only fields.

### Step 6 — Configure git to sign commits in this repo

```bash
cd <FIRM_FOLDER>
git config --local user.signingkey <KEY_ID>
git config --local commit.gpgsign true
git config --local gpg.program $(which gpg)
```

Verify with a test signed commit:

```bash
echo "Signed-commit verification at $(date -u +%FT%TZ)" > firm/.signing-test
git add firm/.signing-test
git commit -S -m "verify: signing key works"
git log --show-signature -1
```

You should see `gpg: Good signature from "<Your Name> (ØØT Bot)..."` in the output. Push:

```bash
git push origin main
```

Open `<BRAIN_REPO_URL>/commits/main` in your browser. The latest commit should have a green **Verified** badge. **If you see Unverified or no badge:** the email on the GPG key doesn't match the email on the commit author. Check both with `git log -1 --pretty=format:"%ae"` (commit email) and `gpg --list-keys --keyid-format LONG <KEY_ID>` (key email). They must match.

### Step 7 — Configure branch protection (web UI)

Go to `<BRAIN_REPO_URL>/settings/branches`. Click **Add classic branch protection rule** (or "Add ruleset" in the newer UI — either works).

**Branch name pattern:** `main`

**Configure these checkboxes EXACTLY as below:**

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

Click **Create**.

> ⚠️ **Free-plan caveat (Finding 16):** if you're on GitHub Free and the repo is private, you'll see a yellow banner: *"Your protected branch rules for your branch won't be enforced on this private repository until you move to a GitHub Team or Enterprise organization account."* The rule is structurally correct but **not enforced** — anyone with push access can still push unsigned commits or force-push. This is acceptable for solo / 2-person Day-1 pilot; upgrade to Team ($4/user/month) before adding a third committer or before R6's audit-trail claim is load-bearing.

### Step 8 — Set up the Curator domain

If you chose **Configuration A** in §5 of decisions (existing Curator + separate vault):

- In the Curator app, navigate to Domains → Create domain.
- **Name**: `<firm-slug>` (e.g. `acme-studio`).
- **Description**: `<firm name> — operational Brain`.
- Click **Create**. The Curator scaffolds a folder under your existing vault.
- Verify in Claude Desktop:
  > Use my-curator. List domains.

  The new domain should appear.

If you chose **Configuration B** (firm folder IS the vault root) — already done in Saturday afternoon Step 5; skip ahead.

### Step 9 — First ingest

Pick five existing documents that represent your firm's knowledge:

1. A recent customer contract
2. A strategic memo (your recent thinking)
3. A product spec or technical document
4. A pitch deck (export to PDF)
5. A meeting transcript (Otter, Fireflies, or similar — export to plain text)

In the Curator app: **Ingest → drag-and-drop** the five files. The Curator processes each via Gemini Flash Lite (or whichever provider you configured). Each document becomes one or more wiki pages.

### Step 10 — Health check

In Claude Desktop:

> Use my-curator. scan_wiki_health on domain=<firm-slug>. scan_semantic_duplicates on domain=<firm-slug>. Report.

Expected: a clean report. Walk through `fix_wiki_issue` for any broken wikilinks the Curator's first-pass extraction proposed (it sometimes guesses slugs that don't exist; you confirm or rephrase).

---

## Weekend One — Sunday afternoon (2-3 hours): configure the 4 Day-1 Routines

> 📖 **Reference:** [`routines/README.md`](../routines/README.md) for the recommended install order. Each Routine has a per-file install checklist at `routines/cloud/<R>.md`.

For each Routine, the workflow is:

1. Open Claude Code → run `/schedule`. Or visit the web dashboard at https://claude.ai/code/routines, or use the Claude Code desktop app's "New Remote Task" feature. **Routines run on Anthropic's cloud, not on your local machine** — your laptop can be closed once they're scheduled. The three interfaces are just management UIs for the same cloud-hosted feature. (Note: this is the **Claude Code** desktop app, not the Claude Desktop chat app — they're different products.)
2. Click **New Routine**.
3. Configure trigger per the routine's frontmatter (e.g. R5 = Sunday 09:00).
4. Upload the prompt body from `routines/cloud/<R>.md` (everything inside the `## Prompt body` fenced block).
5. Attach the Skill Packs listed in the routine's frontmatter.
6. Configure connectors (GitHub with the Brain repo + signing, Slack, Drive read-only as needed).
7. **Confirm code execution is enabled** (default for Pro+).
8. Manual test fire.
9. Verify expected outputs (Brain page lands as signed commit on `main`; Slack post visible).

Install order:

1. **R5 — Brain Health Check** (Sunday 09:00; no dependencies). Do this first — if R5 fires successfully, your stack is wired correctly. [`routines/cloud/R5.md`](../routines/cloud/R5.md).
2. **R6 — EU AI Act Audit Trail** (daily 23:00; mandatory for EU founders, recommended for everyone). **Pre-requisite:** branch protection configured at Step 7 above. [`routines/cloud/R6.md`](../routines/cloud/R6.md).
3. **R1 — Daily Output Capture** (daily 18:00). **Pre-requisite:** at least one partner onboarded (you, the founder, count). [`routines/cloud/R1.md`](../routines/cloud/R1.md).
4. **R2 — Weekly BR Prep** (Friday 08:00). **Pre-requisite:** R1 has 7+ days of data. [`routines/cloud/R2.md`](../routines/cloud/R2.md).

> ⚠️ Hold off on R3 (Monthly Variable Calc), R4 (Long-Tail Settlement), R7 (Klarna Test trigger), and R8 (Treasury Runway) until you have the relevant Skill Packs + Excel files configured and the firm is producing real output data.

---

## Weekend Two — Saturday: onboard the first partner

> 📖 **Reference:** [`templates/partner-onboarding/checklist.md`](../templates/partner-onboarding/checklist.md) — the canonical 30-step checklist. Steps 1-15 happen in the 90-min onboarding session.

1. **Schedule a 90-minute onboarding session.** Both founder and partner present.
2. **Walk through `MANIFESTO.md` together.** 30 min. The partner internalises the five theses, especially Resistance and the Klarna Test.
3. **Reward Species Declaration.** Open `firm/excel/reward-species-declaration.xlsx` in your spreadsheet app. The partner fills in their sheet. Both sign. Generate signed PDF; commit to Brain at `firm/partners/<id>/legal/reward-species-<DATE>.pdf`.
4. **Two Worlds of Code self-identification.** [`skills/code-qa/SKILL.md`](../skills/code-qa/SKILL.md) §4.9 has the 5-question assessment.
5. **Output Spec for the first piece of work.** Together, draft using [`templates/output-spec.md`](../templates/output-spec.md). Commit to `firm/partners/<id>/output-specs/<DATE>--<slug>.md`.
6. **Partner Charter signed.** Use [`templates/partner-charter.md`](../templates/partner-charter.md). Both parties sign.
7. **Tools provisioned.** Run [`templates/partner-onboarding/provisioning-script.sh <partner_id>`](../templates/partner-onboarding/provisioning-script.sh).

---

## Weekend Two — Sunday: first full operational week begins

1. **Daily ledger updates** start (Routine R1). Verify the partner's output appears in `firm/excel/partner-output-ledger.xlsx` Output_Log via signed commits on `main`.
2. **Friday Business Review** (Routine R2 generates the agenda; meeting is 30 minutes; recorded as a markdown summary committed to the Brain). Use [`docs/walkthroughs/W4-running-the-friday-business-review.md`](walkthroughs/W4-running-the-friday-business-review.md) for the 30-minute structure.
3. **First Klarna Test** (when relevant — typically not week one). Walk through [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md) together so the team knows the process before they need it.

By end of weekend two: a running ØØT instance with one partner onboarded, daily output capture writing to your Brain repo as signed commits, weekly review cadence, and the Brain compounding.

---

## What success looks like

- The Brain has 10–30 ingested documents, no broken wikilinks, weekly health check running.
- One partner onboarded with signed Reward Species Declaration, signed Partner Charter, first Output Spec drafted.
- Daily output capture writing to `firm/excel/partner-output-ledger.xlsx` via signed commits on `main`.
- Friday Business Review held; agenda was generated by R2; outcomes committed to the Brain.
- (EU founders) `firm/excel/eu-ai-act-mapping.xlsx` started; daily R6 audit trail running with green Verified badges on every commit.
- Branch protection enforced (or, if on Free private, advisory but you have a plan to upgrade to Team within 90 days).

You are now operating ØØT Generation 1.

---

## Common pitfalls (what to watch for)

1. **Setting up everything before onboarding anyone.** Don't. Onboard the first partner against a minimum-viable stack (Brain + Charter + Output Spec + ledger Routine). Add the rest of the Routines and Excel templates as the operational rhythm requires them.
2. **Skipping the GitHub plan-tier decision.** Default-clicking through GitHub Free + private and expecting branch protection to enforce will silently fail Finding 16. Re-read decision §6.
3. **Skipping the METR baseline.** Mandatory before any major Skill rollout (per Skill Pack S6). Without baseline metrics, you cannot detect the perception gap (the +20% self-reported / -19% measured swing METR found in 2025).
4. **Treating the Klarna Test as a checkbox.** It is not. The test is the framework's signature epistemic discipline. If you score 13 and rationalise to 14, you are doing it wrong. Either honestly score at or above the threshold (≥14/20) or don't proceed.
5. **Adopting Gen 2 features before Gen 1 is stable.** Stablecoin payroll, smart-contract long-tail, Unit Fund — wait. The YOLO model recommends 6–9 months of pilot before opening the Unit Fund.
6. **Storing API keys or secrets in `claude_desktop_config.json` committed to git.** Use environment-variable references (`"env": {"API_KEY": "${BITWARDEN_API_KEY}"}`) instead.
7. **Pasting the GPG private key anywhere.** Only the **public** key (the block starting `-----BEGIN PGP PUBLIC KEY BLOCK-----`) goes to GitHub. The **private** key stays on your machine in `~/.gnupg/` and never leaves it.
8. **Ignoring the email-mismatch between commit author and GPG key UID.** If your commits show "Unverified" instead of green "Verified" on GitHub, the most common cause is `git config user.email` doesn't match the email on the GPG key. Fix by either updating one to match the other.

---

## When to escalate

- **Brain ingest failing** repeatedly: see [`docs/01-installing-the-curator.md`](01-installing-the-curator.md) troubleshooting section, or open an issue on the Curator's GitHub.
- **Routine not firing** at scheduled time: see [`docs/02-installing-routines.md`](02-installing-routines.md).
- **Klarna Test triggering on a PR you don't think it should**: see [`docs/05-using-the-klarna-test.md`](05-using-the-klarna-test.md) for the gaming-and-anti-gaming patterns.
- **Legal-touchpoint question**: see [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md). Counsel is mandatory before adoption in any jurisdiction.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md) for the eleven legal touchpoints.
