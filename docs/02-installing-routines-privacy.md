# 02 — Installing Routines (Privacy Track)

**Audience:** Privacy-track founder.
**Time:** ~3 hours for the 4 Day-1 Routines.
**You will end with:** the framework's automation engine running on your always-on machine via cron / launchd / Task Scheduler hitting headless LM Studio.

> 📖 **Reference:** [`routines/README.md`](../routines/README.md) and per-Routine privacy files at `routines/privacy/<R>.md`.

---

## What this is + the first 5 minutes

The privacy track replaces Anthropic's [Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code) with **OS-native scheduling** on the always-on machine. The Routine prompts are functionally identical to the cloud versions; only the execution substrate differs:

- **Cloud:** Claude Code → `/schedule` → Anthropic infrastructure runs the Routine.
- **Privacy:** cron / launchd / Task Scheduler → your always-on machine runs `llmster --skill <pack> --prompt-file <path>` against headless LM Studio.

In both tracks, Excel writeback follows Pattern C (clone Ledger → openpyxl → signed commit → push) per [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](internal/ADR-001-cloud-routine-excel-writeback.md). The privacy track does this against a local Brain-repo clone; the cloud track against a fresh clone created on Anthropic's infrastructure for each Routine fire.

The trade-off: cloud Routines fire while your laptop is closed; privacy-track Routines fire only while the always-on machine is on. **UPS strongly recommended.**

---

## Pre-requisites

- Always-on machine configured (per [docs/00-quickstart-privacy.md](00-quickstart-privacy.md) Weekend One).
- LM Studio installed; Qwen 3 14B (or larger) downloaded.
- `llmster` headless CLI installed at `/usr/local/bin/llmster`.
- LM Studio MCP host running with the required servers (`my-curator`, `excel-mcp`, `desktop-commander`, `github-mcp`).
- Partner Trezors provisioned and 4thtech identities live (per Skill Pack S12).
- Ledger cloned to the always-on machine.

---

## Per-platform scheduler

### macOS — launchd

For each Routine, create a `.plist` file at `~/Library/LaunchAgents/oot.<r>.plist`. The Routine's privacy-track file (`routines/privacy/<R>.md`) ships with the canonical plist content; copy it.

**Install:**
```bash
launchctl load ~/Library/LaunchAgents/oot.r1.plist
```

**Verify:**
```bash
launchctl list | grep oot.r1
```

**Manual test fire:**
```bash
launchctl start oot.r1.daily-output-capture
tail -50 ~/oot-framework/logs/r1.log
```

### Linux — cron

Edit your crontab:
```bash
crontab -e
```

Paste the Routine's cron line from the privacy-track file. Save.

**Verify:**
```bash
crontab -l
```

**Manual test fire:** run the command directly (without cron):
```bash
/usr/local/bin/llmster --model qwen-3-14b-instruct --skill compensation-attribution --skill my-curator --prompt-file ~/oot-framework/routines/privacy/r1.prompt.md
```

### Windows — Task Scheduler

XML templates ship in `examples/task-scheduler/r1.xml` etc.

**Install:**
```powershell
schtasks /create /xml "examples\task-scheduler\r1.xml" /tn "ØØT R1 Daily Output Capture"
```

**Verify:**
```powershell
schtasks /query | findstr "ØØT"
```

**Manual test fire:**
```powershell
schtasks /run /tn "ØØT R1 Daily Output Capture"
```

---

## Step-by-step: the 4 Day-1 Routines

### R5 — Brain Health Check (do first)

[`routines/privacy/R5.md`](../routines/privacy/R5.md) ships the canonical plist + cron + Task Scheduler XML.

**macOS:**
```bash
cp routines/privacy/oot.r5.plist ~/Library/LaunchAgents/   # if pre-built shipped; otherwise compose from R5.md
launchctl load ~/Library/LaunchAgents/oot.r5.plist
launchctl start oot.r5.brain-health   # manual test
```

**Verify:** `firm/brain-health/<this-week>.md` exists; 4thtech dChat `#brain-health` has a summary.

### R6 — EU AI Act Audit Trail (do second)

**Pre-requisite (one-time):**
1. Configure GitHub branch protection on `main`: force-push disabled, deletion disabled, signed commits required, ≥1 reviewer for `firm/audit-logs/*`.
2. Generate GPG signing key for the `oot-bot` user on the always-on machine: `gpg --gen-key` (4096-bit RSA).
3. Upload public key to GitHub: [github.com/settings/keys](https://github.com/settings/keys).
4. Configure `git config --global user.signingkey <key-id>`.
5. Configure `gpg-agent` for 24h passphrase cache: edit `~/.gnupg/gpg-agent.conf`:
   ```
   default-cache-ttl 86400
   max-cache-ttl 86400
   ```

Install R6 per [`routines/privacy/R6.md`](../routines/privacy/R6.md). Manual fire. Verify a **signed** commit lands on `main` (`git log --show-signature` shows "Good signature").

### R1 — Daily Output Capture (do third)

Install per [`routines/privacy/R1.md`](../routines/privacy/R1.md). Manual fire. Verify X1 row + Brain page + dChat post.

### R2 — Weekly BR Prep (do fourth)

Install per [`routines/privacy/R2.md`](../routines/privacy/R2.md). Manual fire. Verify X3 row + Brain pre-meeting page + dChat draft.

---

## Common pitfalls (privacy-specific)

**1. Cron job doesn't fire.**
- Cause 1: machine was off / sleeping. Check `pmset -g log | head` (macOS) or `last reboot` (Linux).
- Cause 2: cron can't find `llmster`. Use the absolute path `/usr/local/bin/llmster`, not `llmster`.
- Cause 3: cron user doesn't have the env vars LM Studio needs. Set `MODELS_DIR` etc. in the crontab itself or wrap in a shell script that sources `~/.bashrc`.

**2. `llmster` errors: "MCP host unreachable".**
- Cause: LM Studio isn't running in headless mode.
- Fix: start LM Studio's headless server: LM Studio → Settings → Local Server → "Start". Add to startup: macOS launchd, Linux systemd unit.

**3. R6 push fails: "secret key not found".**
- Cause: cron's environment doesn't see `gpg-agent`.
- Fix: in the R6 prompt-file's wrapper script, prepend: `eval $(gpg-agent --daemon --enable-ssh-support)` or use `gpg2 --batch --pinentry-mode loopback` patterns.

**4. R6 signed commit succeeds but GitHub rejects: "branch protection blocks push".**
- Cause: branch protection requires ≥1 reviewer for ALL commits, not just human PRs.
- Fix: configure the protection to allow `oot-bot` user to push directly to `firm/audit-logs/*` paths (per the canonical R6 setup).

**5. R3 hangs / produces garbage on Qwen 3 14B.**
- Cause: R3 is high-stakes; smaller models struggle with the multi-partner aggregation logic.
- Fix: switch the R3 plist/cron entry to use Llama 3.3 70B (downloads ~40GB). The framework's authors strongly recommend this.

---

## Long-term reliability

- **UPS health:** check monthly. UPS batteries degrade; replace every 3-5 years.
- **Power-on rule:** configure the always-on machine to wake/start on power restoration: macOS `pmset autorestart 1`; Linux BIOS "Restore on AC Power Loss = On"; Windows BIOS equivalent.
- **Model upgrades:** new model releases get a 1-week dry-run on a parallel directory before cutover. Routine outputs from new models are diffed against old before switching.
- **Disk space:** monitor `~/oot-framework/logs/`; archive logs older than 90 days.

---

## When to escalate

- A Routine missed a day: backfill via `llmster --backfill <YYYY-MM-DD> --skill ... --prompt-file ...`. Document the gap in `firm/privacy-track/troubleshooting/`. Per the framework's discipline, never silently fake a missed day.
- LM Studio crashes repeatedly: check `~/.lmstudio/logs/`; common cause is RAM exhaustion when running multiple models simultaneously.
- 4thtech / PollinationX outage: dChat / dMail are decentralised; outages are rare and usually self-resolve. If persistent, see [wiki.4thtech.io](https://wiki.4thtech.io/).

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. The R6 signed-commit audit-trail discipline addresses EU AI Act Article 12; counsel review is mandatory before relying on the framework's classification.
