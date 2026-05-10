# ØØT Privacy-Track Install Plan (agent-runnable)

**This is an agent-runnable plan.** A coding agent meeting the [capability spec](AGENT-CAPABILITY-SPEC.md) reads this file end-to-end, executes the steps in order against the user's machine, and asks the user the questions marked **🟡 ASK USER** before proceeding past them.

If you (the human) are reading this directly, see [`README.md`](README.md). The privacy track is materially more setup work than cloud track — total ~25 hours across two weekends + 1 week of hardware shipping. If you want a faster install and don't have a hard sovereignty mandate, [`cloud-install-plan.md`](cloud-install-plan.md) is the better choice.

---

## Agent: read this preamble first

The privacy-track install differs from cloud in three fundamental ways:

1. **You're installing on an always-on machine, not the user's daily laptop.** The "machine" in this plan refers to a Mac mini / NUC / Raspberry Pi 5 with FDE + UPS that the user has acquired and set up.
2. **Routines run via OS-native scheduling** (cron / launchd / Task Scheduler) hitting headless LM Studio via `llmster`, not via Claude Code Routines on Anthropic infrastructure.
3. **Per-partner Trezors are Day-1**, not Gen-2-deferred — they're how 4thtech wallet identities work.

The same ground rules from `cloud-install-plan.md` apply: pause and confirm before consequential actions; never silently downgrade; honest failure reporting; resume from state; don't invent inputs; translate technical for the user; read before write.

State file: `~/.oot/install-state.yaml` (same format as cloud plan, with `track: privacy`).

---

## Step 0 — Preflight + reading

**What you're about to do (tell the user):** "Privacy track has more reading and more prerequisites than cloud. Let's confirm you have what you need before any hardware arrives."

### 0.1 — Confirm reading

🟡 **ASK USER:** "Have you read these files? They're 2-3 hours of reading; the privacy track is unforgiving of skipping it.
- [`MANIFESTO.md`](../../MANIFESTO.md) — five theses
- [`governance/KLARNA-TEST.md`](../../governance/KLARNA-TEST.md) — signature discipline
- [`governance/SECRETS-POLICY.md`](../../governance/SECRETS-POLICY.md) — the seed-on-paper rule
- [`docs/MODULES.md`](../../docs/MODULES.md) — what to install
- [`docs/00-quickstart-privacy.md`](../../docs/00-quickstart-privacy.md) — the manual track for context
- [`skills/privacy-self-sovereign/SKILL.md`](../../skills/privacy-self-sovereign/SKILL.md) — full S12 (the privacy track's owner skill)

Type `yes` if you've read them, `wait` if you want to read now."

### 0.2 — Confirm sovereignty mandate

🟡 **ASK USER:** "Why are you choosing the privacy track? Pick one:
1. Regulatory pressure (e.g. customers don't allow cloud-LLM ingest of their data)
2. Philosophical / political commitment to self-custody
3. Generation 2 readiness (you want Trezor-based identity from Day-1)
4. Other (please describe)

If you don't have one of these, the cloud track is materially less work and equally framework-compliant. I'll switch you to `cloud-install-plan.md` if you want."

If user wants to switch to cloud, abort this plan and start the cloud one.

### 0.3 — Mark step done

`step_0_privacy_preflight: done`.

---

## Step 1 — Collect firm profile

(Same as cloud plan Step 1, plus three privacy-specific questions:)

🟡 **ASK USER:**

7. **Always-on machine choice.** "Mac mini M4 Pro 32GB (~€1,800, the framework's authors' default)? Intel NUC + 32-64GB RAM (~€1,200)? Raspberry Pi 5 16GB (~€350, slowest but cheapest)? Other? Note: R3 monthly variable wants Llama 3.3 70B which needs 32-64GB RAM — Pi 5 16GB will run Qwen 3 14B for R1/R2/R5/R6 only and will fail R3."

8. **Hardware status.** "Have you ordered the always-on machine, per-partner Trezors, UPS, and Yubikeys yet? (Trezor delivery: 3-7 days. Mac mini direct: 5-10 days. UPS / Yubikey: 1-2 days.) If not, this is the moment — order now and come back when hardware arrives."

9. **PollinationX storage size.** "100GB (small org)? 500GB (medium)? 1TB+ (regulated, large media)? You can resize later but pick a starting tier. Cost ~€10-80/month equivalent."

Persist as `firm_profile.always_on_machine`, `firm_profile.hardware_ordered`, `firm_profile.pollinationx_size`.

### 1.x — If hardware not yet ordered

If user hasn't ordered hardware: pause the plan here. Tell user: "I'll wait. When all hardware is in hand, restart this plan and I'll resume from Step 2."

`step_1_collect_profile: done` once user confirms hardware is in hand.

---

## Step 2 — Always-on machine setup

**What you're about to do (tell the user):** "The always-on machine needs FDE, a dedicated user, and network hardening. About 60 minutes."

### 2.1 — OS choice

Detect what the user has running on the always-on machine. Walk through the per-OS setup:

**macOS:**
```bash
# On the always-on machine:
sudo fdesetup status     # confirm FileVault is on (if off: System Settings → Privacy & Security → FileVault → Turn On)
# Create dedicated `oot` user via System Settings → Users & Groups
# Disable iCloud sync of Documents/Desktop in iCloud settings
# Touch ID for boot: disable (unsafe for unattended machine)
```

**Linux (NUC/Pi):**
```bash
# LUKS FDE was set during install; verify:
sudo cryptsetup status /dev/mapper/<your_volume>
# SSH key auth only:
sudo sed -i 's/#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
# Unattended upgrades:
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

**Windows:**
```powershell
# BitLocker
manage-bde -on C:
# Disable RDP unless VPN'd
```

🟡 **ASK USER** at each step: confirm done before moving on.

### 2.2 — UPS

🟡 **ASK USER:** "Connect the UPS: machine plugged into UPS, UPS plugged into wall. Install UPS drivers if needed (CyberPower / APC have macOS / Linux daemons). Verify the UPS battery is charged and the OS reports it. Type `done` when wired up."

### 2.3 — Network

🟡 **ASK USER:** "The always-on machine should be **outbound-only**: no port-forwarding, no public IP, no exposed services. If you want to access it from your laptop remotely, install Tailscale (https://tailscale.com/) or WireGuard. Type `done | skip` when done."

### 2.4 — Mark step done

`step_2_machine_setup: done`.

---

## Step 3 — LM Studio + local models

**What you're about to do (tell the user):** "I'll install LM Studio on the always-on machine and download the local models the framework's Routines will run against. About 2 hours (mostly model download time)."

### 3.1 — Install LM Studio

Walk user to https://lmstudio.ai/, download for the platform, install.

### 3.2 — Download models

🟡 **ASK USER:** "In LM Studio's Models tab, download these (all 4-bit quantised unless noted):
- **Qwen 3 14B Instruct** (~9 GB) — default daily driver for R1, R2, R5, R6, R7
- **Qwen 3 9B Instruct** (~5 GB) — fallback for smaller machines
- **Llama 3.3 70B Instruct** (~40 GB) — for R3 monthly variable (high-stakes)
- **DeepSeek-V3** (~40 GB) — for code work if your firm ships software heavily

Download time: 1-3 hours total depending on connection. Tell me when complete."

### 3.3 — Enable headless mode + llmster

```bash
# Enable LM Studio headless mode (per LM Studio docs)
# Install llmster CLI:
brew install llmster   # macOS via Homebrew (if available)
# Or: pip install llmster (if Python package is the install path your version uses)

llmster --version
```

🟡 **ASK USER:** "Verify with: `llmster --model qwen-3-14b --prompt 'Say hello.'`. Tell me what you see."

If error: walk through troubleshooting; surface the actual error.

### 3.4 — Configure MCP host

LM Studio has an MCP host built into the desktop app. Walk user through adding the MCPs:

🟡 **ASK USER:** "In LM Studio: Settings → MCPs → Add MCP. We need:
- `my-curator` — the Brain interface
- `github-mcp` — for the Brain repo signed-commit workflow
- `desktop-commander` — for local filesystem ops
- `4thtech` — for dChat / dMail (only on privacy track)

I'll show you the config for each. Tell me when ready."

(Walk through each MCP config one at a time, similar to cloud plan Step 6.)

### 3.5 — Mark step done

`step_3_lm_studio: done`.

---

## Step 4 — Per-partner Trezors

**What you're about to do (tell the user):** "Each partner — including you, the founder — needs their own Trezor. ~30-45 min per partner. We'll do yours now; the rest are done during partner onboarding."

### 4.1 — Verify Trezor packaging

🟡 **ASK USER:** "Verify the Trezor packaging: tamper-evident seals must be intact. **If anything looks tampered with, do NOT use this device — return to the manufacturer.** Confirm seals are intact?"

### 4.2 — Initialise the Trezor offline

🟡 **ASK USER:** "Connect the Trezor via USB to the always-on machine. Open the Trezor Suite app. Initialise as a NEW device (NOT recovery). The device will display a 24-word seed phrase. Write it on paper with a pencil. **The seed never goes digital — not in Bitwarden, not in iCloud, not in a photo, not in a password manager.** Store the paper in a fireproof safe separate from the Trezor itself.

When the seed is recorded on paper and the Trezor is set up with a strong PIN, type `done`."

### 4.3 — (Optional) Passphrase ("25th word")

🟡 **ASK USER:** "Optionally set a passphrase (the '25th word'). Adds another layer of security but adds a memorisation requirement. Recommended for founders / high-value Trezors. If yes, write the passphrase on a SEPARATE paper card from the seed and store separately. Type `yes` (configured), `no` (skip), or `wait` (decide later)."

### 4.4 — Pair with 4thtech

🟡 **ASK USER:** "Install the 4thtech wallet client (https://4thtech.io/). Pair with the Trezor. Send a test dMail to yourself — receipt confirms the wallet identity is live. Type `done`."

### 4.5 — Record wallet address

```bash
# Capture the wallet address; write to firm/partners/<your-id>/profile.md when we get there
echo "<wallet-address>" > /tmp/founder-wallet.txt
```

### 4.6 — Mark step done

`step_4_trezor_founder: done`. (Per-partner Trezor setup happens at partner onboarding time.)

---

## Step 5 — 4thtech firm domain

**What you're about to do (tell the user):** "Acquire the firm's 4thtech dMail domain (~€50/year). Configure dChat workspace. About 30 minutes."

### 5.1 — Acquire firm domain

🟡 **ASK USER:** "On the 4thtech dApp, register your firm's dMail domain (e.g. `<firm-slug>.4thtech`). Pay with the founder Trezor's wallet. Confirm purchase complete."

### 5.2 — Configure dChat workspace

🟡 **ASK USER:** "Create the firm's dChat workspace. Default channels: `#general`, `#output-log`, `#brain-health`, `#ops`, `#compensation`, `#klarna-test`, `#treasury`. Confirm done."

### 5.3 — Mark step done

`step_5_4thtech: done`.

---

## Step 6 — PollinationX storage

🟡 **ASK USER:** "Acquire your PollinationX storage NFT at https://pollinationx.io/ at the size from Step 1.9. Pay with the founder Trezor. Confirm purchase complete + write the storage NFT identifier to me."

```bash
# Install PollinationX client:
# (Per upstream docs at https://wiki.pollinationx.io/ )
pollinationx --version
```

`step_6_pollinationx: done`.

---

## Step 7 — GitHub Brain repo + signing

(Same as cloud plan Steps 4 + 5: create the Brain repo, generate signing key, configure branch protection. The bot identity needs push access to the Brain repo from the always-on machine.)

`step_7_brain_repo: done`. `step_8_signing: done`.

---

## Step 8 — Curator on the always-on machine

(Same as cloud plan Step 6, but installed on the always-on machine, not the user's daily laptop.)

🟡 **ASK USER:** "Install the Curator on the always-on machine. Configure cloud-LLM ingest with Gemini Flash Lite (or Anthropic Claude). Note: Gen-2 will replace this with local-LLM ingest; for now, the privacy track still uses cloud-LLM for the Curator's parsing pipeline only — the firm's actual queries are answered by the local LM Studio model. Confirm Curator is running."

`step_9_curator: done`.

---

## Step 9 — First Curator domain + initial ingest

(Same as cloud plan Step 7, run from Claude Desktop on the user's laptop, but pointed at the always-on machine's Curator via Tailscale or local network. Or run from the always-on machine directly.)

`step_10_brain_first_ingest: done`.

---

## Step 10 — Configure Day-1 Routines (privacy track)

**What you're about to do (tell the user):** "I'll install the four Day-1 Routines as cron entries / launchd plists / Task Scheduler tasks on the always-on machine. Each Routine fires `llmster` against the local LM Studio model. About 30 minutes."

For each Routine:

1. Place the prompt body at `~/oot-framework/routines/privacy/r<n>.prompt.md` (separate file with the prompt text from the cloud routine's "Prompt body" section).
2. Install the platform-specific scheduling configuration:
   - **macOS:** `~/Library/LaunchAgents/oot.r<n>.plist`; `launchctl load`.
   - **Linux:** `crontab -e` with the cron line from `routines/privacy/R<n>.md`.
   - **Windows:** Task Scheduler XML import.
3. Manually fire to test.
4. Verify expected outputs (signed commit on `main` for state-mutating Routines; markdown Brain page for all).

**Privacy-track Excel writeback** is the same Pattern C as cloud: the Routine clones the Brain repo, openpyxl mutates `firm/excel/<file>.xlsx`, signed-commits, pushes. The local clone is at `~/oot-brain/`. **Excel MCP is NOT required** for the Routine path — the Routine uses openpyxl directly. (Excel MCP remains an *optional* tool for ad-hoc human-in-the-loop work.)

`step_11_routines: done`.

---

## Step 11 — Smoke test

(Same as cloud plan Step 10, plus privacy-specific checks: dChat post arrived; PollinationX read access works; Trezor still recognised by 4thtech; LM Studio is responsive.)

`step_12_smoke: done`.

---

## Step 12 — Install summary

(Same as cloud plan Step 11, with privacy-specific entries: hardware inventory, model versions, 4thtech domain, PollinationX NFT, per-partner Trezor IDs.)

`step_13_summary: done`.

---

## What this plan does NOT install

- Per-partner Trezors beyond the founder's. Done at partner onboarding.
- The first partner's signed Charter / Reward Species Declaration. Human-signed.
- Long-tail entitlement contracts. Counsel review.
- Cloud track's Routines. If you need both, run cloud first, then privacy as a parallel install — they don't conflict; the privacy machine becomes a redundant runner against the same Brain repo.

End of plan.
