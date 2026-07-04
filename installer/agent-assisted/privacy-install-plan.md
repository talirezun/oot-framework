# ØØT Privacy-Track Install Plan (agent-runnable)

**Plan version:** 1.1.0 (2026-05-10) — refined alongside the cloud plan v1.1.0 with the 18 findings recorded in [`docs/internal/install-test-report-2026-05-10.md`](../../docs/internal/install-test-report-2026-05-10.md).

**This is an agent-runnable plan.** A coding agent meeting the [capability spec](AGENT-CAPABILITY-SPEC.md) reads this file end-to-end, executes the steps in order against the user's machine, and asks the user the questions marked **🟡 ASK USER** before proceeding past them.

If you (the human) are reading this directly, see [`START-HERE.md`](START-HERE.md) for how to invoke this with your coding agent. The privacy track has more steps than cloud (~25 hours total across two weekends + 1 week hardware shipping). If you want a faster install and don't have a hard sovereignty mandate, [`cloud-install-plan.md`](cloud-install-plan.md) is the better choice.

---

## Agent: read this preamble first

The privacy-track install differs from cloud in three fundamental ways:

1. **You're installing on an always-on machine, not the user's daily laptop.** "The machine" in this plan means a Mac mini / NUC / Raspberry Pi 5 with FDE + UPS that the user has acquired and set up. Many steps run on the always-on machine; some run on the user's daily laptop (e.g. Claude Desktop's MCP wiring on the laptop talks to Curator running on the always-on machine via Tailscale).
2. **Routines run via OS-native scheduling** (cron / launchd / Task Scheduler) hitting headless LM Studio via `llmster`, not via Claude Code Routines on Anthropic's infrastructure.
3. **Per-partner Trezors are Day-1**, not Gen-2-deferred — they're how 4thtech wallet identities work.

Same ground rules from the [cloud plan preamble](cloud-install-plan.md#agent-read-this-preamble-first) apply: pause and confirm before consequential actions; web-UI primary; never silently downgrade; honest failure reporting; resume from state; don't invent inputs; translate technical for the user; read before write; clipboard sandbox caveat (don't rely on `pbcopy`/`xclip`).

State file: `~/.oot/install-state.yaml` with `track: privacy`. Same format as cloud plan, with these additional fields:

```yaml
firm_profile:
  track: privacy
  always_on_machine_kind: <mac-mini|nuc|pi5|other>
  always_on_machine_specs: <RAM, CPU>
  hardware_in_hand: <yes|no>
  pollinationx_size: <100GB|500GB|1TB+>
  partner_count_for_trezors: <int>
locations:
  framework_repo: "<path on the daily laptop where the framework is cloned>"
  always_on_user: "<username on the always-on machine; e.g. 'oot'>"
  firm_folder: "<absolute path on the always-on machine>"
  curator_vault: "<absolute path; null if Config B>"
  curator_domain: "<domain slug>"
```

---

## Step 0 — Preflight + sovereignty mandate

**What you're about to do (tell the user):** "Privacy track has more reading and more prerequisites than cloud. Let's confirm you have what you need before any hardware arrives."

### 0.1 — Confirm framework reading

🟡 **ASK USER:** "Have you read these files? They're 2-3 hours of reading; the privacy track is unforgiving of skipping it.

- [`MANIFESTO.md`](../../MANIFESTO.md) — five theses
- [`governance/KLARNA-TEST.md`](../../governance/KLARNA-TEST.md) — signature discipline
- [`governance/SECRETS-POLICY.md`](../../governance/SECRETS-POLICY.md) — the seed-on-paper rule
- [`docs/MODULES.md`](../../docs/MODULES.md) — what to install
- [`docs/00-quickstart-privacy.md`](../../docs/00-quickstart-privacy.md) — the manual track for context
- [`skills/privacy-self-sovereign/SKILL.md`](../../skills/privacy-self-sovereign/SKILL.md) — full S12

Type `yes` if read, `wait` if you want to read now."

### 0.2 — Confirm sovereignty mandate

🟡 **ASK USER:** "Why are you choosing the privacy track? Pick one:

1. Regulatory pressure — customers don't allow cloud-LLM ingest of their data
2. Philosophical / political commitment to self-custody
3. Generation 2 readiness — you want Trezor-based identity from Day-1
4. Other (please describe)

If you don't have one of these, the cloud track is materially less work and equally framework-compliant. I'll switch you to `cloud-install-plan.md` if you want."

If user wants to switch: abort this plan and start the cloud plan.

### 0.3 — Verify daily-laptop tools

The agent needs basic tools on the user's daily laptop (where the agent is running):

```bash
git --version
for cmd in python3.13 python3.12 python3.11 python3; do
    command -v "$cmd" >/dev/null 2>&1 && "$cmd" --version && OOT_PYTHON="$cmd" && break
done
curl --version | head -1
gpg --version 2>&1 | head -1 || echo "MISSING: gpg (install via brew install gnupg / apt install gnupg)"
ssh -V 2>&1 || echo "MISSING: ssh"  # needed to connect to the always-on machine later
```

If any required tool is missing: walk user through install (per cloud plan Step 0.1).

### 0.4 — Set up Python venv on daily laptop

```bash
$OOT_PYTHON -m venv ~/.oot/venv
source ~/.oot/venv/bin/activate
pip install openpyxl pyyaml httpx
```

### 0.5 — Mark step done

`step_0_privacy_preflight: done`.

---

## Step 1 — Collect firm profile (privacy-extended)

**What you're about to do (tell the user):** "Same six firm-profile questions as cloud, plus three privacy-specific ones. ~5 minutes."

### 1.1 — Cloud-shared questions

(Same six as `cloud-install-plan.md` Step 1.1: firm name, partner count, jurisdictions, EU AI Act exposure, Klarna gate now/later, Anthropic plan **— note: privacy track Anthropic plan is optional, only needed if Curator's cloud-LLM ingest uses Anthropic Claude. Free tier or Gemini Flash Lite works for ingest**.)

### 1.2 — Privacy-specific questions

🟡 **ASK USER:**

7. **Always-on machine choice.** "Pick one: **Mac mini M4 Pro 32GB** (~€1,800, framework authors' default), **Intel NUC + 32-64GB RAM** (~€1,200), **Raspberry Pi 5 16GB** (~€350, slowest but cheapest). Other options welcome.

   **Important:** R3 monthly variable wants Llama 3.3 70B 4-bit which needs ~32-64GB RAM. Pi 5 16GB will run Qwen 3 14B for R1/R2/R5/R6 only; **R3 will fail** unless you upgrade RAM or use a stronger model on a different machine."

8. **Hardware status.** "Do you have these in hand already, or do we need to wait?

   - Always-on machine
   - Per-partner Trezors (one per partner including founder)
   - UPS (CyberPower / APC, ~€80-150)
   - 2x Yubikey 5C NFC (~€60 each)

   If anything not yet ordered: this is the moment. **Trezor: 3-7 days delivery. Mac mini direct from Apple: 5-10 days. UPS / Yubikey: 1-2 days from Amazon.** Order now and come back when hardware arrives."

9. **PollinationX storage size.** "100GB (small org)? 500GB (medium)? 1TB+ (regulated, large media)? Cost ~€10-80/month equivalent."

### 1.3 — If hardware not yet ordered

If user doesn't have all hardware: pause the plan here.

🟡 **ASK USER:** "I'll wait. When all hardware is in hand, restart this plan and I'll resume from Step 0.5 (locations)."

`step_1_collect_profile: done` once user confirms hardware in hand.

---

## Step 0.5 — Choose locations

**What you're about to do (tell the user):** "Same three location questions as cloud, but the answers refer to the always-on machine, not your daily laptop. ~3 minutes."

(This step runs after Step 1 in the privacy plan because we need the firm profile + hardware-in-hand confirmation first.)

### 0.5.1 — Firm operational repo path on the always-on machine

🟡 **ASK USER:** "On the always-on machine (not your daily laptop), where should the firm operational repo live? Default: `/Users/<oot-user>/<firm-slug>` (macOS) or `/home/<oot-user>/<firm-slug>` (Linux).

Some founders prefer:
- A dedicated path like `/srv/<firm-slug>` on Linux
- An external SSD mount

Type the path, or `default`."

### 0.5.2 — Existing Curator detection (on the always-on machine)

🟡 **ASK USER:** "Do you already have the Curator desktop app installed on the always-on machine?

Most privacy-track founders are setting up the always-on machine fresh, so the answer is usually 'no'. But if you've been a Curator user on this same machine: 'yes'.

(yes / no)"

If yes: ask for the existing vault path.

### 0.5.3 — Curator integration mode

(Same Configuration A vs B as cloud plan Step 0.5.3. For greenfield privacy installs, Configuration B is the more common choice — the always-on machine is dedicated to the firm, no reason to keep a separate second-brain.)

### 0.5.4 — Mark step done

`step_0_5_locations: done`.

---

## Step 2 — Always-on machine OS setup

**What you're about to do (tell the user):** "FDE, dedicated user, network hardening on the always-on machine. About 60-90 minutes. You'll do most of this manually on the always-on machine; I'll guide you with exact commands but I can't run commands on a remote machine over SSH unless you give me access."

### 2.1 — How to run commands on the always-on machine

🟡 **ASK USER:** "Pick one:

A. **You run commands manually** on the always-on machine (open Terminal on it directly), and tell me the output. Slower but doesn't require you to set up SSH access from the agent's machine.

B. **You configure SSH from your daily laptop** to the always-on machine (Tailscale or LAN), and I run commands via SSH. Faster, but requires you to install + configure SSH first.

For most non-technical founders, option A is more accessible. (A / B)"

If A: from this point, the agent's commands are presented as 'paste this in the always-on machine's terminal' rather than executed locally. State file tracks them as `manual` rather than `done`.
If B: walk through SSH setup (key generation on laptop, copy to always-on machine via `ssh-copy-id`, verify with `ssh <oot-user>@<always-on-machine>`).

### 2.2 — OS-specific FDE + dedicated user

(Walk user through OS-specific setup per `docs/00-quickstart-privacy.md` Saturday-morning section. macOS: FileVault + dedicated `oot` user + iCloud sync disabled. Linux: LUKS at install + SSH key auth only + unattended-upgrades. Windows: BitLocker + Yubikey 2FA.)

🟡 **ASK USER:** confirm each sub-step done before continuing.

### 2.3 — UPS

(Per `docs/00-quickstart-privacy.md`. Connect UPS, install drivers, verify OS reports the battery.)

### 2.4 — Network hardening

🟡 **ASK USER:** "The always-on machine should be **outbound-only**. Verify:

- No port-forwarding rules on your router pointing at the always-on machine.
- No public IP exposed.
- Outbound is fine: GitHub, 4thtech RPC nodes, PollinationX gateways, Curator's cloud-LLM ingest provider.
- Tailscale or WireGuard configured if you need remote access from your laptop. (Recommended.)

Tell me `done` when network is configured."

### 2.5 — Mark step done

`step_2_machine_setup: done`.

---

## Step 3 — Per-partner Trezors

**What you're about to do (tell the user):** "Each partner — including you, the founder — needs their own Trezor. ~30-45 min per partner. We do yours now; the rest are done during partner onboarding."

### 3.1 — Verify packaging

🟡 **ASK USER:** "Verify the Trezor packaging tamper-evident seals are intact. **If anything looks tampered with, do NOT use this device — return to the manufacturer.** Confirm intact?"

### 3.2 — Initialise offline

🟡 **ASK USER:** "On the always-on machine, connect the Trezor via USB. Open the Trezor Suite app (https://suite.trezor.io). Initialise as a NEW device (NOT recovery).

The device will display a 24-word seed phrase. **Write it on paper with a pencil.** Store the paper in a fireproof safe **separate** from the Trezor.

**The seed never goes digital — not in Bitwarden, not in iCloud, not in a photo, not in a password manager.** Paper, fireproof safe, separate location.

Set a strong PIN on the device. Tell me `done`."

### 3.3 — (Optional) Passphrase

🟡 **ASK USER:** "Optionally set a passphrase (the '25th word'). Adds another layer of security; adds memorisation requirement. Recommended for founders / high-value Trezors.

If yes, write the passphrase on a SEPARATE paper card from the seed; store separately.

(yes / no / wait — decide later)"

### 3.4 — Pair with 4thtech wallet

🟡 **ASK USER:** "Install the 4thtech wallet client on the always-on machine: https://4thtech.io/. Pair with the Trezor. Send a test dMail to yourself — receipt confirms wallet identity is live. Tell me `done`."

### 3.5 — Record wallet address

🟡 **ASK USER:** "Tell me the founder's 4thtech wallet address. I'll write it to the Brain at Step 9."

`step_3_trezor_founder: done`.

---

## Step 4 — LM Studio + local models

**What you're about to do (tell the user):** "Install LM Studio on the always-on machine + download the local models. About 2 hours (mostly model download time)."

### 4.1 — Install LM Studio

🟡 **ASK USER:** "Download LM Studio for the always-on machine's OS from https://lmstudio.ai/. Install. Tell me `done`."

### 4.2 — Download models

🟡 **ASK USER:** "In LM Studio's Models tab, download these (4-bit quantised unless noted):

- **Qwen 3 14B Instruct** (~9 GB) — default daily driver for R1, R2, R5, R6, R7
- **Qwen 3 9B Instruct** (~5 GB) — fallback for smaller machines
- **Llama 3.3 70B Instruct** (~40 GB) — for R3 monthly variable (high-stakes)
- *(optional)* DeepSeek-V3 (~40 GB) — strong on code if firm ships software heavily

Total: ~55-95 GB. Download time: 1-3 hours depending on connection. Tell me `done`."

### 4.3 — Headless mode + llmster

🟡 **ASK USER:** "In LM Studio, enable headless / server mode. Then install the `llmster` CLI:

- macOS: `brew install llmster` (if available) or per LM Studio docs
- Linux: `pip install llmster` or per LM Studio docs

Verify: `llmster --version`. Tell me what you see."

### 4.4 — Smoke test

🟡 **ASK USER:** "Run: `llmster --model qwen-3-14b --prompt 'Say hello in one word.'`

Tell me what you see. Expected: a one-word response from Qwen."

### 4.5 — MCP host config

🟡 **ASK USER:** "In LM Studio: Settings → MCPs → Add MCP. Add these as we configure them through later steps:

- `my-curator` (configured at Step 9)
- `github-mcp` (configured at Step 8)
- `desktop-commander` for local filesystem (configured at Step 9)
- `4thtech` for dChat / dMail (configured at Step 5)

For now: just confirm the MCPs panel is reachable in LM Studio. Tell me `done`."

`step_4_lm_studio: done`.

---

## Step 5 — 4thtech firm domain

🟡 **ASK USER:** "On the 4thtech dApp, register your firm's dMail domain (e.g. `<firm-slug>.4thtech`). Pay with the founder Trezor's wallet. Confirm purchase complete + tell me the domain."

🟡 **ASK USER:** "Create the firm's dChat workspace. Default channels: `#general`, `#output-log`, `#brain-health`, `#ops`, `#compensation`, `#klarna-test`, `#treasury`. Tell me `done`."

`step_5_4thtech: done`. Persist `firm_4thtech_domain` in state file.

---

## Step 6 — PollinationX storage

🟡 **ASK USER:** "Acquire your PollinationX storage NFT at https://pollinationx.io/ at the size you chose at Step 1.9. Pay with the founder Trezor. Tell me the NFT identifier when complete."

```bash
# Install PollinationX client per upstream docs at https://wiki.pollinationx.io/
pollinationx --version
```

`step_6_pollinationx: done`. Persist `pollinationx_nft` in state file.

---

## Step 7 — GitHub plan-tier choice

(Same as cloud plan Step 3. The privacy track still uses GitHub for **two** repos per [ADR-002](https://github.com/talirezun/oot-framework/blob/main/docs/internal/ADR-002-firm-brain-curator-shared-brain.md): the Ledger — Routines push signed commits — and the Firm Brain — Curator Shared Brain. The plan-tier choice applies to both. Finding 16 applies identically: GitHub Free private = advisory-only branch protection, doesn't enforce.

**Privacy-track-specific note: EU residency.** If your privacy mandate is regulatory (a customer or supervisory authority requires EU storage), GitHub Free / Pro / Team are all US-only. You need **GitHub Enterprise Cloud with the EU data residency option** for the Firm Brain repo (and probably the Ledger too). Curator v3.1's Cloudflare R2 backend will offer a cheaper EU-residency path; for today, Enterprise Cloud is the answer.)

🟡 **ASK USER** the same plan-tier question, extended for privacy track: team / enterprise-eu / public / free.

`step_7_github_plan_choice: done`.

---

## Step 8 — Create GitHub Ledger + Firm Brain repos + initial scaffold

(Same as cloud plan Step 5, which now creates **both** the Ledger and the Firm Brain repos per [ADR-002](https://github.com/talirezun/oot-framework/blob/main/docs/internal/ADR-002-firm-brain-curator-shared-brain.md), with these privacy-track deltas:)

- The local clone of the **Ledger** lives **on the always-on machine**, not the daily laptop. The Firm Brain repo is managed by Curator on the always-on machine — partners' personal Curators on their own laptops Push to it; the admin's Curator on the always-on machine runs weekly Synthesize.
- The clone path for the Ledger is `<FIRM_FOLDER>` from Step 0.5.1.
- The framework repo is cloned on the always-on machine too (at `~/oot-framework` typically) so we have access to `templates/excel/` for the initial copy.
- Persist BOTH `LEDGER_REPO_URL` and `FIRM_BRAIN_REPO_URL` in the privacy-track state file.

```bash
# On the always-on machine:
git clone https://github.com/talirezun/oot-framework.git ~/oot-framework

mkdir -p "<FIRM_FOLDER>"
cd "<FIRM_FOLDER>"
git init -b main
git config user.name "<firm name> Bot"
git config user.email "<BRAIN_REPO_EMAIL>"
git remote add origin "<LEDGER_REPO_URL>"

mkdir -p firm/excel firm/output-logs firm/audit-logs firm/business-reviews firm/klarna-tests firm/compensation firm/brain-health firm/partners
touch firm/output-logs/.gitkeep firm/audit-logs/.gitkeep firm/business-reviews/.gitkeep firm/klarna-tests/.gitkeep firm/compensation/.gitkeep firm/brain-health/.gitkeep firm/partners/.gitkeep

cp ~/oot-framework/templates/excel/*.xlsx firm/excel/

# README same as cloud plan, with track: privacy noted

git add .
git commit -m "scaffold: initial Brain folder + Excel templates from framework v1.0.0"
git push -u origin main
```

🟡 **ASK USER:** before pushing, confirm.

`step_8_brain_repo: done`.

---

## Step 9 — Signing key + branch protection (both repos)

(Same as cloud plan Steps 6 + 7 — runs on the always-on machine. Cloud plan Step 7 now applies branch protection to **both** the Ledger and the Firm Brain repos; do the same here.)

GPG key generation, public-key upload to GitHub via the web UI (https://github.com/settings/gpg/new), branch-protection rule via web UI on **both** `<LEDGER_REPO_URL>/settings/branches` and `<FIRM_BRAIN_REPO_URL>/settings/branches` with identical checkbox configuration (the privacy track also can't escape Finding 16 — same plan-tier caveat applies to both repos).

`step_9_signing: done`. `step_9_5_branch_protection_ledger: done`. `step_9_5_branch_protection_firm_brain: done`.

---

## Step 10 — Curator integration (privacy-track variant)

**What you're about to do (tell the user):** "Install the Curator on the always-on machine + wire my-curator MCP into both Claude Desktop (on your laptop) and LM Studio (on the always-on machine). About 30 minutes."

### 10.1 — Install Curator on the always-on machine

(Per cloud plan Step 8B.1. The Curator runs on the always-on machine.)

🟡 **ASK USER:** "On the always-on machine, in the Curator's first-run wizard:

- **Vault folder:** `<CURATOR_VAULT>` (Configuration A) or `<FIRM_FOLDER>` (Configuration B)
- **Cloud-LLM ingest:** Gemini Flash Lite (https://aistudio.google.com/) — generous free tier; ~€0-10/month for heavy use. **Note:** Gen 2 will replace this with local-LLM ingest. For now, the privacy track still uses cloud-LLM for the Curator's parsing pipeline only — operational queries go to the local LM Studio model, not Anthropic.

Tell me `done` when Curator's main UI is up."

### 10.2 — macOS file permissions (Finding 10)

🟡 **ASK USER:** "macOS may have prompted for filesystem permission. If Curator can't see the firm folder: System Settings → Privacy & Security → Files and Folders → Curator → toggle ON. Restart Curator. Tell me `done`."

### 10.3 — Wire my-curator MCP into LM Studio

🟡 **ASK USER:** "In LM Studio's MCPs panel (set up at Step 4.5), configure `my-curator`:

```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "http://127.0.0.1:8765/mcp"]
}
```

The Curator app exposes its MCP at port 8765 by default. Tell me what LM Studio reports — green check or error."

### 10.4 — Wire my-curator MCP into Claude Desktop on the laptop

(Optional — for the founder to use Claude Desktop on their daily laptop alongside the privacy-track stack. The MCP needs to reach the Curator on the always-on machine — over Tailscale, not localhost.)

🟡 **ASK USER:** "Optional: do you want Claude Desktop on your daily laptop to also be able to query the Curator? If yes:

1. Set up Tailscale on both the daily laptop and the always-on machine (https://tailscale.com/).
2. Note the Tailscale IP of the always-on machine (e.g. `100.x.y.z`).
3. In Claude Desktop's `claude_desktop_config.json`, add my-curator pointing at `http://<tailscale-ip>:8765/mcp` instead of `127.0.0.1`.

Skip for now / configure now? (skip / configure)"

### 10.5 — Self-test

🟡 **ASK USER:** "In LM Studio's chat window, paste:

> Use my-curator. List the available domains.

Tell me what the model responds."

### 10.6 — Add S1 my-curator skill

(Per cloud plan Step 8B.5 — but loaded into LM Studio's persistent system prompt, not Claude Desktop. Or both, if user is using both.)

### 10.7 — Firm Brain admin wizard (Curator Shared Brain initialization)

(Same as cloud plan Step 8.5 — runs on the always-on machine since that's where the admin's Curator lives on the privacy track.)

🟡 **ASK USER:** "On the always-on machine, open Curator → Shared Brain → Admin Setup. Follow the cloud plan Step 8.5 flow:
1. Pick IP mode (`organisational` or `contributor_retains`). For privacy-track firms with sovereignty-aligned partners, `contributor_retains` is often preferred — confirm with the partners before locking.
2. Generate admin token + invite token. Store both in Bitwarden founders collection.
3. Run your own contributor wizard (select your `<curator_domain>` as the opted-in domain).
4. Verify Push → Synthesize → Pull loop end-to-end.

Tell me `done` when the loop is verified."

**Privacy-track-specific caveat surfacing:** during the IP-mode choice, remind the user that Curator's weekly Synthesize step still calls a cloud LLM (Gemini Flash Lite in v3.0.0-beta) — partners' MCP interactions on the privacy track are local (LM Studio + Qwen), but the admin's Synthesize step is cloud. This is the same Gen-1 cloud-LLM gap as personal Curator ingest; Curator v3.1 closes it.

**Privacy-track-specific scheduling:** schedule R9 (the weekly Firm Brain Synthesize) via cron on the always-on machine, not as a Claude Code Routine. Add to crontab:

```
0 19 * * 0 /usr/local/bin/curator sharedbrain synthesize --brain <FIRM_BRAIN_REPO_URL> >> ~/oot/logs/r9.log 2>&1
```

`step_10_7_firm_brain: done`. `step_10_curator: done`.

---

## Step 11 — Initial Brain ingest

(Same as cloud plan Step 9.)

`step_11_brain_first_ingest: done`.

---

## Step 12 — Configure Day-1 Routines (privacy variant)

**What you're about to do (tell the user):** "I'll install the four Day-1 Routines as cron entries / launchd plists / Task Scheduler tasks on the always-on machine. Each Routine fires `llmster` against the local LM Studio model. About 30 minutes."

For each Routine (R5 first, then R6, R1, R2):

1. Place the prompt body at `~/oot-framework/routines/privacy/r<n>.prompt.md` (extracting from the cloud routine's "Prompt body" section in `routines/cloud/R<n>.md`).
2. Install the platform-specific scheduling configuration:

**macOS (launchd):**

```xml
<!-- ~/Library/LaunchAgents/oot.r5.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>oot.r5</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/llmster</string>
        <string>--model</string>
        <string>qwen-3-14b</string>
        <string>--skill</string>
        <string>my-curator</string>
        <string>--prompt-file</string>
        <string>/Users/&lt;oot-user&gt;/oot-framework/routines/privacy/r5.prompt.md</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>  <!-- Sunday -->
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/&lt;oot-user&gt;/oot-framework/logs/r5.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/&lt;oot-user&gt;/oot-framework/logs/r5.err</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/oot.r5.plist
```

**Linux (cron):**

```cron
# ~/oot-framework/routines/privacy/cron.txt
0 9 * * 0 /usr/local/bin/llmster --model qwen-3-14b --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r5.prompt.md >> ~/oot-framework/logs/r5.log 2>&1
0 18 * * * /usr/local/bin/llmster --model qwen-3-14b --skill compensation-attribution --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r1.prompt.md >> ~/oot-framework/logs/r1.log 2>&1
0 23 * * * /usr/local/bin/llmster --model qwen-3-14b --skill governance-compliance --prompt-file ~/oot-framework/routines/privacy/r6.prompt.md >> ~/oot-framework/logs/r6.log 2>&1
0 8 * * 5 /usr/local/bin/llmster --model qwen-3-14b --skill reporting-business-review --prompt-file ~/oot-framework/routines/privacy/r2.prompt.md >> ~/oot-framework/logs/r2.log 2>&1
```

```bash
# ⚠  `crontab <file>` REPLACES the machine's entire crontab — it wipes any
#    existing entries. If the always-on machine already has cron jobs, MERGE
#    instead of overwriting:
crontab -l 2>/dev/null > /tmp/oot-crontab.merged || true
cat ~/oot-framework/routines/privacy/cron.txt >> /tmp/oot-crontab.merged
crontab /tmp/oot-crontab.merged
crontab -l   # verify the ØØT lines AND any pre-existing lines are present
```

If you're certain the crontab is empty (a fresh always-on machine), the direct
`crontab ~/oot-framework/routines/privacy/cron.txt` is fine — but the merge form
above is always safe.

**Windows (Task Scheduler):** XML import — see `routines/privacy/r5-task.xml` template.

### 12.x — Manual test fire + verify

🟡 **ASK USER:** "For each installed Routine, manually fire it once:

- macOS: `launchctl start oot.r5`
- Linux: `bash -c '<the cron line above>'`
- Windows: Run task manually in Task Scheduler

Verify expected outputs:
- R5: `firm/brain-health/<YYYY-WW>.md` exists; signed commit on `main`.
- R6: `firm/audit-logs/<YYYY-MM-DD>.md` exists; signed commit on `main`.
- R1: requires partners — defer until you onboard the first partner.
- R2: requires R1 to have data — defer.

Tell me what you see for R5 and R6."

`step_12_routines: done`.

---

## Step 13 — (Optional) Klarna gate

(Same as cloud plan Step 11 — but the GitHub Actions workflow runs whenever a PR with `ai-replaces-human` label is opened, and the local R7 listener service polls GitHub every 5 minutes. The R7 listener is a separate small Python service launched via launchd / cron alongside the other Routines.)

`step_13_klarna_gate: done` (or skipped).

---

## Step 14 — Smoke test

(Privacy variant of cloud plan Step 12. Same Pattern C openpyxl test, but run on the always-on machine via `llmster` rather than via the agent's Python venv. Plus privacy-specific checks: dChat post arrived; PollinationX read access works; Trezor still recognised by 4thtech; LM Studio is responsive.)

`step_14_smoke_test: done`.

---

## Step 15 — Install summary

(Same as cloud plan Step 13, with privacy-specific entries: hardware inventory, model versions, 4thtech domain, PollinationX NFT, per-partner Trezor IDs, always-on machine kind/specs.)

`step_15_install_summary: done`.

---

## What this plan does NOT install

- Per-partner Trezors beyond the founder's. Done at partner onboarding time.
- The first partner's signed Charter / Reward Species Declaration. Human-signed.
- Long-tail entitlement contracts. Counsel review.
- Cloud track's Routines. If you want both: run cloud first, then privacy as a parallel install — they don't conflict; the privacy machine becomes a redundant runner against the same Ledger.

---

## Resumability + failure handling

Same as cloud plan. Agent reads `~/.oot/install-state.yaml` on startup, resumes from the first non-`done` step. Steps are idempotent.

End of privacy plan v1.1.0.
