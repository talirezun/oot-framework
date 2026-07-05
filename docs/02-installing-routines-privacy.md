# 02 — Installing Routines (Privacy Track)

**Audience:** Privacy-track founder.
**Time:** ~3 hours for the 4 Day-1 Routines.
**You will end with:** the framework's automation engine running on your always-on machine via cron / launchd / Task Scheduler, each schedule firing **OpenCode headless** (`opencode run`) against a **local LM Studio server**.

> 📖 **Reference:** [`routines/README.md`](../routines/README.md) and per-Routine privacy files at `routines/privacy/<R>.md`.

---

## What this is + the first 5 minutes

The privacy track replaces Anthropic's [Claude Code Routines](https://claude.com/blog/introducing-routines-in-claude-code) with **OS-native scheduling** on the always-on machine. The Routine prompts are functionally identical to the cloud versions; only the execution substrate differs:

- **Cloud:** Claude Code → `/schedule` → Anthropic infrastructure runs the Routine.
- **Privacy:** cron / launchd / Task Scheduler → your always-on machine runs `opencode run --model lmstudio/<model> "$(cat <prompt-file>)"` against a **local LM Studio server**.

The agent that clones the Ledger, runs openpyxl, and calls the MCP servers is **OpenCode** (open-source terminal agent, non-interactive `opencode run` mode). The **model** it uses is served locally by **LM Studio** on its OpenAI-compatible server (`http://127.0.0.1:1234/v1`). How you run that server headless depends on the machine: **on macOS with the LM Studio desktop app, the app itself is the server** (`lms server start`) — there is no separate `llmster` binary; on a **headless Linux box** with no GUI app, the standalone **`llmster` daemon** fills that role. Either way, LM Studio is *only* the model server — it does not run skills, clone repos, or call MCP tools; OpenCode does all of that.

### How the pieces fit

```
cron / launchd / Task Scheduler   (the schedule — fires on time, only while the machine is on)
        │
        ▼
opencode run --model lmstudio/<model> "$(cat r<N>.prompt.md)"
   run from the firm's runner dir (~/<firm-slug>) so it picks up the scoped opencode.json
        │
        ├─▶ LM Studio server  ─── the model (served headless: the LM Studio app on macOS, or the llmster daemon on headless Linux; kept warm via `lms load … --context-length 32768 --ttl`)
        ├─▶ MCP servers       ─── github-mcp, desktop-commander, 4thtech, my-curator (declared in opencode.json → mcp)
        └─▶ code execution    ─── git clone + openpyxl + signed commit (ADR-001 Pattern C)
                                        │
                                        ▼
                                  the firm's Ledger repo on GitHub
```

In both tracks, Excel writeback follows Pattern C (clone Ledger → openpyxl → signed commit → push) per [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](internal/ADR-001-cloud-routine-excel-writeback.md). The privacy track does this against a local Ledger-repo clone; the cloud track against a fresh clone created on Anthropic's infrastructure for each Routine fire.

The trade-off: cloud Routines fire while your laptop is closed; privacy-track Routines fire only while the always-on machine is on. **UPS strongly recommended.**

---

## Pre-requisites

The privacy track's scheduled Routines run on a **three-piece stack**. Install all three before wiring any Routine:

1. **LM Studio ≥0.3.5, run headless** — the model server. Download Qwen 3 14B (or larger) inside LM Studio, then run it headless per [lmstudio.ai/docs/developer/core/headless](https://lmstudio.ai/docs/developer/core/headless). **On macOS with the desktop app, the app itself is the headless server** (`lms server start`); on a **headless Linux box** it's the standalone **`llmster` daemon**. Either way it serves an OpenAI-compatible endpoint at `http://127.0.0.1:1234/v1`.
2. **The `lms` CLI** — LM Studio's own command-line tool (ships with LM Studio). Use it to manage the server and keep a model warm: `lms server start`, then `lms load qwen-3-14b-instruct --context-length 32768 --ttl 3600`. The `--context-length 32768` is required — LM Studio's default 4096-token context can't even hold the agent's system prompt, so a default-loaded model fails with `n_keep >= n_ctx`. The `--ttl` keeps the model resident so a cron fire doesn't pay a cold-load every run.
3. **OpenCode** — the agent harness (`opencode run`). Install per [`../installer/agent-assisted/OPENCODE-SETUP.md`](../installer/agent-assisted/OPENCODE-SETUP.md), configure an OpenAI-compatible provider named `lmstudio` pointing at `http://127.0.0.1:1234/v1`, wire the MCP servers (`my-curator`, `desktop-commander`, `github-mcp`, `4thtech`) in `opencode.json` → `mcp`, and drop the **scoped unattended `opencode.json`** into the firm's runner directory (see OPENCODE-SETUP.md → "Scheduled / unattended runs").

Plus:

- Always-on machine configured (per [docs/00-quickstart-privacy.md](00-quickstart-privacy.md) Weekend One).
- Partner Trezors provisioned and 4thtech identities live (per Skill Pack S12).
- Ledger cloned to the always-on machine, under the firm's runner directory `~/<firm-slug>`.

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

**Manual test fire:** run the command directly (without cron), from the firm runner directory so the scoped `opencode.json` applies:
```bash
cd ~/<firm-slug> && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)"
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
- Cause 2: cron can't find `opencode`. Use the absolute path `/usr/local/bin/opencode` (or wherever `which opencode` reports), not bare `opencode` — cron's `PATH` is minimal.
- Cause 3: the fire runs but OpenCode can't find its config. The cron line must `cd ~/<firm-slug>` first so OpenCode loads that directory's project-level `opencode.json` (provider + MCP + the scoped allow-list). A fire from the wrong directory falls back to global config and will hit permission prompts it can't answer.
- Cause 4: cron user doesn't have the env vars the tools need. Set them in the crontab itself, or wrap the command in `/bin/bash -lc '…'` so a login shell sources your profile (this is also why the launchd plists use `/bin/bash -lc`).

**2. OpenCode hangs or errors: model / MCP unreachable.**
- Cause A — model server down: OpenCode's `lmstudio` provider can't reach `http://127.0.0.1:1234/v1`. Fix: start the LM Studio server (the desktop app's own server on macOS, or the `llmster` daemon on a headless Linux box) and load a model — `lms server start && lms load qwen-3-14b-instruct --context-length 32768 --ttl 3600` (the `--context-length` is required; the default 4096 can't hold the agent's system prompt). Add the server to startup (macOS launchd, Linux systemd unit). LM Studio here is **only** the model server.
- Cause B — MCP server missing: the MCP servers now live in the runner directory's `opencode.json` `mcp` block, **not** in LM Studio. If a Routine reports a missing tool (e.g. `github-mcp`), check that block and that the server's binary/command is installed. Tip: use `opencode serve` + `--attach` (see OPENCODE-SETUP.md) to keep MCP servers warm and avoid a cold-boot on every fire.

**3. R6 push fails: "secret key not found".**
- Cause: cron's environment doesn't see `gpg-agent`.
- Fix: in the R6 prompt-file's wrapper script, prepend: `eval $(gpg-agent --daemon --enable-ssh-support)` or use `gpg2 --batch --pinentry-mode loopback` patterns.

**4. R6 signed commit succeeds but GitHub rejects: "branch protection blocks push".**
- Cause: branch protection requires ≥1 reviewer for ALL commits, not just human PRs.
- Fix: configure the protection to allow `oot-bot` user to push directly to `firm/audit-logs/*` paths (per the canonical R6 setup).

**5. R3 hangs / produces garbage on Qwen 3 14B.**
- Cause: R3 is high-stakes; smaller models struggle with the multi-partner aggregation logic.
- Fix: switch the R3 plist/cron entry to use Llama 3.3 70B (downloads ~40GB). The framework's authors strongly recommend this.

**6. Small models make cosmetic formatting slips.**
- Observed live: a small model (≤9-10B) completes the routine cycles correctly but produces minor markdown-formatting slips — e.g. a wikilink written with a `.md` suffix that prior rows lacked, and a dropped closing `---` on a page's YAML frontmatter. The numbers and logic were right; only the formatting drifted.
- Fix: when your hardware allows, run an **MoE-class local model** (e.g. `qwen3.5-35b-a3b`) for the daily routines — it's far more formatting-consistent than a small dense model while staying fast. Either way, the **founder-review step is what catches these slips** — a small model plus review is a workable floor.

---

## Long-term reliability

- **UPS health:** check monthly. UPS batteries degrade; replace every 3-5 years.
- **Power-on rule:** configure the always-on machine to wake/start on power restoration: macOS `pmset autorestart 1`; Linux BIOS "Restore on AC Power Loss = On"; Windows BIOS equivalent.
- **Model upgrades:** new model releases get a 1-week dry-run on a parallel directory before cutover. Routine outputs from new models are diffed against old before switching.
- **Disk space:** monitor `~/oot-framework/logs/`; archive logs older than 90 days.

---

## When to escalate

- A Routine missed a day: **there is no `--backfill` flag** — you catch up by re-running the prompt. For **R1**, just run it again: R1 dedupes and scans from its last recorded `log_id` (fixed 2026-07-04), so the next fire automatically captures whatever it missed, never double-paying. For the **other Routines**, re-run the prompt with the target date stated inline — e.g. `cd ~/<firm-slug> && opencode run --model lmstudio/qwen-3-14b-instruct "Process the R6 audit trail for 2026-04-12. $(cat ~/oot-framework/routines/privacy/r6.prompt.md)"`. Document the gap in `firm/privacy-track/troubleshooting/`. Per the framework's discipline, never silently fake a missed day.
- LM Studio crashes repeatedly: check `~/.lmstudio/logs/`; common cause is RAM exhaustion when running multiple models simultaneously.
- 4thtech / PollinationX outage: dChat / dMail are decentralised; outages are rare and usually self-resolve. If persistent, see [wiki.4thtech.io](https://wiki.4thtech.io/).

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. The R6 signed-commit audit-trail discipline addresses EU AI Act Article 12; counsel review is mandatory before relying on the framework's classification.
