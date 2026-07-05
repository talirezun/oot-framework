# OpenCode setup — the community-track harness

This is the harness appendix for the **community track** (per [`docs/internal/ADR-003-community-track-no-subscription.md`](../../docs/internal/ADR-003-community-track-no-subscription.md)): operating ØØT with **no Anthropic subscription and no dedicated hardware**. It tells you how to install [OpenCode](https://opencode.ai), point it at a free (or your-own-key, or local) model, configure it so it satisfies the framework's pause-and-confirm safety bar, wire the my-curator MCP, and drive the ØØT install with it.

> **Status (2026-07-04): author-verified basic operation; end-to-end community-track install test QUEUED.** OpenCode has been verified to install, load the my-curator MCP, and follow the install plan's early steps. A full end-to-end community-track install (bundled with the Phase 4 privacy-track live test on the maintainer's test instance) has **not yet been run**. Do not treat the community track as e2e-tested until that lands; report issues at [github.com/talirezun/oot-framework/issues](https://github.com/talirezun/oot-framework/issues).

---

## (a) What OpenCode is + the naming note

**OpenCode** is an open-source terminal coding agent — a Claude-Code-style harness that runs in your terminal, reads and writes files, runs shell commands, speaks MCP natively, and drives an install plan the same way Claude Code does. It supports 75+ model providers, ships **free built-in models**, runs local models via Ollama / LM Studio, and has a permission system that satisfies the framework's [capability spec](AGENT-CAPABILITY-SPEC.md) R4 (pause-and-confirm).

**Naming note.** OpenCode's repository is now **`anomalyco/opencode`** — it was **formerly `sst/opencode`**. The npm package is **`opencode-ai`**. The project site is [opencode.ai](https://opencode.ai). If you find older docs (including earlier ØØT drafts) referencing `sst/opencode`, that's the same project under its previous name.

- Site: [opencode.ai](https://opencode.ai)
- Repo: [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) (formerly `sst/opencode`)
- npm package: `opencode-ai`

---

## (b) Install

macOS / Linux — pick one:

```bash
# Option 1 — the install script
curl -fsSL https://opencode.ai/install | bash

# Option 2 — npm (needs Node 18+)
npm i -g opencode-ai@latest

# Option 3 — Homebrew (macOS / Linux)
brew install anomalyco/tap/opencode
```

Verify:

```bash
opencode --version
```

**Windows.** Install under **WSL** (Windows Subsystem for Linux), same as the rest of the framework. ØØT's provisioning steps assume a POSIX shell (`git`, `curl`, `gpg`, `jq`, `python3`); native-Windows PowerShell is not a supported install environment. This matches the wizard's stance — run the whole install inside WSL.

---

## (c) Model / provider setup

OpenCode needs a model to run. Three options, cheapest-first:

### Option 1 — free built-in models (default for trying it out)

OpenCode ships free built-in models. This is the zero-cost, zero-config way to try the install: launch `opencode`, pick a free model when prompted, and go. Good enough to read the plan and drive the file/shell steps. For the framework's **one** genuinely high-stakes step — the R3 monthly variable-pay calculation — the docs recommend the strongest model you can point at (see the capability spec's note on R3); a free model is fine for the *install*, and R3 runs later against whatever model you configure for it.

### Option 2 — your own API key (recommended once the firm is real)

Point OpenCode at your own provider key. **Gemini Flash Lite is the recommended default** — it's cheap (well under €10/month at ØØT's ~2.3 runs/day), strong enough for the install and for daily-ops playbook runs, and it's **the same provider key the Curator already uses for ingest** (see §e below), so you're not adding a new vendor relationship. Any OpenAI-compatible or first-party provider OpenCode supports also works.

### Option 3 — local models via LM Studio / Ollama (fully offline)

If you have a capable machine, run a local model — no API key, no data leaving your machine for the agent's own reasoning. This is the community-track path that most resembles the privacy track without buying dedicated hardware. Qwen 3 32B+ or Llama 3.3 70B are the models the framework recommends for sustained 50-step install tasks (per [`AGENT-CAPABILITY-SPEC.md`](AGENT-CAPABILITY-SPEC.md) "Tested privacy track"). Smaller models (7B/13B) tend to lose track around step 30.

**Model fidelity, from live testing.** Small models (≤9-10B) complete the routine cycles but make cosmetic formatting slips — in a live run a qwen3.5-9b wrote an X7 wikilink with a `.md` suffix that prior rows lacked, and dropped the closing `---` of a page's YAML frontmatter. When the hardware allows, prefer an **MoE-class local model** (e.g. `qwen3.5-35b-a3b`, which activates only a few billion parameters per token so it runs far faster than a dense 35B) for daily routines. Either way, the founder-review step is what catches these cosmetic slips — a small model plus review is a workable floor.

### Minimal `opencode.json`

Global config lives at `~/.config/opencode/opencode.json`; a per-project `opencode.json` in the repo root overrides it. A minimal config that sets a model looks like this:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "google/gemini-2.5-flash-lite"
}
```

For a local model via LM Studio (OpenAI-compatible endpoint), the `lmstudio/` model prefix used everywhere in this doc only exists if you **define the `lmstudio` provider**. Add this live-validated block to your global config at `~/.config/opencode/opencode.jsonc` (it merges with any project-level `opencode.json` in the runner directory — the two are layered, not exclusive):

```json
"provider": {
  "lmstudio": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "LM Studio (local)",
    "options": { "baseURL": "http://127.0.0.1:1234/v1" },
    "models": { "qwen/qwen3.5-9b": { "name": "Qwen 3.5 9B (local)" } }
  }
}
```

The model IDs under `models` must match LM Studio's own identifiers **exactly** — run `lms ls` to see them. The `--model` flag is then `lmstudio/<that id>` (e.g. `--model lmstudio/qwen/qwen3.5-9b`); multi-slash IDs are fine because OpenCode only splits on the *first* `/` — the leading segment is the provider, the rest is the model ID verbatim.

For the free built-in models you don't need to set `model` at all; OpenCode prompts you.

---

## (d) Permissions for the install (non-negotiable)

The framework's [capability spec R4](AGENT-CAPABILITY-SPEC.md) requires the agent to **pause and confirm before any consequential action** — anything that costs money, sends a message to a third party, creates an account, generates a cryptographic key, pushes to a remote repo, or configures branch protection. OpenCode satisfies R4 through its `permission` config.

**Set every tool to `ask` for the duration of the install.** Add this to your `opencode.json` (project-level is cleanest — put it in the ØØT repo root so it only applies here):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "*": "ask"
  }
}
```

This makes OpenCode stop and ask you before **every** tool call. That is deliberately more than R4 strictly requires (R4 only mandates confirmation on *consequential* actions), but "ask on everything" is the safe default for a founder driving a real install against real accounts and a real signing key. You can relax it to per-tool rules (`allow` / `ask` / `deny`, with pattern-based bash rules) once you're comfortable and the install is done.

**Explicitly do NOT use `--auto` / TUI auto-approve during the install.** OpenCode has an `--auto` flag (and a TUI auto-approve toggle) that approves tool calls without asking. **Auto-approve violates R4** and defeats the whole pause-and-confirm discipline — it could generate your GPG signing key, push to your Ledger, or configure branch protection without you seeing it happen. Leave auto-approve **off** for the entire install. This is the single most important line on this page.

---

## (e) Wiring the my-curator MCP

The Curator installs a **local MCP server** (the my-curator server) so the agent can read and write your Second Brain. OpenCode speaks MCP natively — add the server under the top-level `mcp` key in `opencode.json`. There are two ways the Curator exposes the server; **Variant 2 (stdio) is the recommended default** — it's the form validated on the live-test instance and it needs no shim.

### Variant 1 — local-HTTP (127.0.0.1:8765)

Some Curator installs run a local HTTP MCP endpoint at `http://127.0.0.1:8765/mcp`, bridged into OpenCode with `mcp-remote` (a small stdio↔HTTP shim via `npx`), the same pattern the cloud install plan uses for Claude Desktop:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-curator": {
      "type": "local",
      "command": ["npx", "-y", "mcp-remote", "http://127.0.0.1:8765/mcp"]
    }
  }
}
```

> **Caveat (from live testing):** many Curator installs expose the MCP as **stdio ONLY** — the local-HTTP endpoint may be absent or disabled. Verify with `curl -s http://127.0.0.1:8765/mcp` before committing to this variant; if it's unreachable, use **Variant 2 (stdio)** below.

### Variant 2 — local stdio server directly (recommended default)

The stdio form is the validated default. Configure the my-curator server as a `local` server whose `command` array is the server's launch command — this is the **same command the Curator prints for the Claude Desktop `mcpServers` block**; find it in your `claude_desktop_config.json` under `mcpServers.my-curator` (OpenCode's `command` array takes the executable and its args as list elements). The live-validated form is:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-curator": {
      "type": "local",
      "command": ["/usr/local/bin/node", "<path>/mcp/server.js", "--domains-path", "<path>/domains"]
    }
  }
}
```

Validated live as: `node ~/second-brain/mcp/server.js --domains-path ~/second-brain/domains` (use the absolute `node` path — e.g. `/usr/local/bin/node` — in the config's first array element).

> `"type": "local"` is for stdio servers running on your machine (both variants above are local — the HTTP endpoint is bridged through a local `npx` process). `"type": "remote"` with a `url` is for genuinely remote HTTP MCP servers, which the my-curator server is not.

**Verify** the wiring inside OpenCode by asking it to call the MCP:

```
Use my-curator. List the available domains.
```

You should get back your Curator domains. If it errors, the Curator app probably isn't running (start it) or the endpoint/command is wrong (recheck against the Curator's MCP panel).

---

## (f) The START-HERE prompt — OpenCode variant

This is the community-track equivalent of [`START-HERE.md`](START-HERE.md). Same install plan, same ground rules; the only differences are the cost note and the automation note. Copy this verbatim into OpenCode (working directory = the cloned ØØT repo), after you've set the `permission` block from §d.

```
I'm installing the ØØT framework on my machine for the cloud track's file/
GitHub/Curator layer, on the COMMUNITY TRACK — I have no Anthropic subscription
and I'm driving this install with you (OpenCode) on a free/local model. Please
drive the install end-to-end by following the agent-runnable plan at:

  installer/agent-assisted/cloud-install-plan.md

Ground rules I want you to follow:

1. Read the plan from the top before starting. It defines the install state file
   (~/.oot/install-state.yaml), the resumability protocol, the pause-and-confirm
   gates, and the failure handling. Don't skip the preamble.

2. Pause and confirm with me before any action that costs money, sends a message
   to a third party, creates an account, generates a cryptographic key, pushes to
   a remote repository, or configures branch protection. The plan flags these
   with the "🟡 ASK USER" marker. (My OpenCode permission config is set to
   "ask" on everything, so you'll be prompting me anyway — good.)

3. If a step requires me to do something on a third-party service (GitHub.com,
   the Curator app), tell me the exact button-by-button sequence and wait for my
   "done" before continuing.

4. If you can't do a step, surface the exact error to me, propose a fix, and wait
   for me to decide whether to retry, fix manually, or skip.

5. Don't downgrade silently. If a signed commit fails, retry; if it keeps failing,
   stop and tell me — never push an unsigned commit without my explicit "yes".

6. Translate technical for me. I'm not a developer. Frame each action for someone
   who has never opened a JSON file, and show me what's happening before it happens.

7. After every step, update ~/.oot/install-state.yaml so we can resume if your
   session ends.

IMPORTANT for the community track: any step in the plan that assumes Claude Code
Routines (the scheduled cloud automation) does NOT apply to me — I have no
Anthropic plan. When you reach the Routine-scheduling steps, STOP and tell me,
and point me at the automation ladder in
docs/internal/ADR-003-community-track-no-subscription.md so I can pick a rung
(manual playbook runs / laptop cron / GitHub Actions) instead. Everything else in
the plan — the Ledger repo, signing key, branch protection, Curator wiring, Excel
scaffold, Klarna gate workflow — applies to me unchanged.

When the install is complete, write a summary at ~/.oot/install-summary.md.

Start with Step 0 of the plan.
```

**Cost note (community track).** The install itself is **free** — OpenCode is free and you can drive it on a free built-in model. You need **no Anthropic subscription** for the install *or* for daily operation on the community track. The only running cost is the Curator's Gemini Flash Lite ingest (~€5-10/month at heavy use) plus your GitHub plan (Free works for a solo/2-partner firm, though Free private repos don't enforce branch protection — GitHub Team at ~€4/user/month buys enforcement; see the install plan's plan-tier step). Canonical numbers live in [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md#cost-summary).

**What needs what.** The Skill Packs, the Ledger, the Firm Brain, the Excel templates, the Klarna gate (a free GitHub Actions workflow), and the governance discipline all run on the community track unchanged. The **only** part that assumes Anthropic is the scheduled-automation layer (Claude Code Routines). The community track replaces that with the automation ladder below.

---

## (g) The automation ladder (from ADR-003)

Cloud Routines' laptop-closed scheduling has no free equivalent, so the community track offers three rungs, each an upgrade of the last. Pick the lowest rung that meets your needs and climb when you're ready. Full detail in [`docs/internal/ADR-003-community-track-no-subscription.md`](../../docs/internal/ADR-003-community-track-no-subscription.md) § "The automation ladder".

1. **Rung 1 — manual playbook runs (the floor, zero setup).** Paste the DAILY / WEEKLY / MONTHLY ops-playbook prompt into OpenCode when you sit down. R1's dedupe + last-run catch-up semantics (fixed 2026-07-04) make irregular cadence safe — a missed day is captured on the next run, never double-paid. This is where every community-track firm starts.
2. **Rung 2 — laptop cron (recommended default once the firm is real).** OS scheduling (cron / launchd / Task Scheduler) invokes `opencode run` non-interactively with a routine prompt body. Runs only while your laptop is on — same gap semantics as the privacy track's always-on caveat, minus the hardware. Missed fires are absorbed by the same catch-up semantics as Rung 1.
3. **Rung 3 — GitHub Actions scheduled workflows (laptop-closed, still no subscription).** A `schedule:`-triggered workflow runs the routine prompt against a model API using a repo-secret key (Gemini Flash / any OpenAI-compatible endpoint; typically cents per month at ØØT's ~2.3 runs/day). This restores laptop-closed automation. Trade-off: the firm's Ledger content transits the chosen model provider — the same class of disclosure as the cloud track, so **EU founders apply the same S7 assessment** they would on cloud. A reference `templates/ci/routine-runner.yml` ships in v1.3; until then, copy the pattern from the shipped Klarna-gate workflow.

> **Rungs 1 and 2 do NOT give you laptop-closed automation.** Only Rung 3 runs when your machine is off. Don't promise yourself hands-off operation on Rung 1 or 2 — they run when *you* run OpenCode (Rung 1) or when your laptop is awake (Rung 2).

---

## (h) Scheduled / unattended runs (privacy track + community Rung 2)

The **privacy track** and the community track's **Rung 2** run OpenCode from a scheduler with no human present. That changes two things: the invocation form, and the permission model.

### The canonical scheduled invocation

The scheduler (cron / launchd / Task Scheduler) runs `opencode run` non-interactively with the routine prompt piped in from its `r*.prompt.md` file:

```bash
# cron line (R1 example, daily 18:00). Replace <firm-slug> and the model per routine.
# The `lms unload --all; lms load …` prefix is load-bearing on a scheduled fire — see the TTL/JIT note below.
0 18 * * * cd ~/<firm-slug> && lms unload --all; lms load qwen-3-14b-instruct --context-length 32768 --ttl 900 -y && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)" >> ~/oot-framework/logs/r1.log 2>&1
```

- `cd ~/<firm-slug>` first — this is the firm's **runner directory**, where the scoped `opencode.json` lives (below). OpenCode loads the project-level config from its working directory.
- `lms unload --all; lms load … --ttl 900 -y &&` — chain the model reload into the cron line itself (see the TTL/JIT note directly below for why). `-y` skips the interactive confirm so it runs unattended.
- `--model lmstudio/<model>` — on the privacy track the provider is `lmstudio` (a local LM Studio server); on community Rung 2 it can be any provider you've configured (e.g. `google/gemini-2.5-flash-lite`). On a non-LM-Studio provider (Rung 2 with an API model) drop the `lms unload/load` prefix — it's LM-Studio-specific.
- `"$(cat …)"` — the prompt body. It begins with an instruction to read the routine's owner SKILL.md file(s) first (this replaces any per-invocation skill flags; the prompt loads its own skills).
- One-time on the always-on machine: `mkdir -p ~/oot-framework/logs`. **The `--context-length 32768` is not optional:** LM Studio's default 4096-token context cannot even hold an agent's system prompt, so a run against a default-loaded model fails immediately with `n_keep >= n_ctx`.

> **⚠️ TTL/JIT trap — why the cron line chains `lms unload --all; lms load …` instead of relying on a keep-warm TTL (from live testing).** A `lms load --ttl <seconds>` keep-warm always expires long before the *next* daily fire (a 3600s TTL is dead 23 hours before an every-24h routine runs). When the model has expired and a run arrives, LM Studio **JIT-reloads it at the default 4096 context** — which breaks the run (`n_keep >= n_ctx`) exactly as an un-`--context-length`'d load would. Worse, a plain re-`lms load` of an already-loaded model creates a **DUPLICATE instance** (identifier `<model>:2`) while the stale instance keeps serving — so you end up with two copies and requests hitting the wrong one. The robust scheduled-fire pattern is therefore to **unload everything, then load fresh at the right context, then run**, all in the cron line: `lms unload --all; lms load <model> --context-length 32768 --ttl 900 -y && opencode run …`. The short `--ttl 900` is just a safety margin for the run's own duration; it is *not* relied on to survive to the next fire. (A long keep-warm TTL still makes sense for an **always-loaded server you drive interactively** — it's only the *scheduled* fire that needs the unload+load prefix.)

**launchd (macOS)** can't do the `$(cat …)` shell substitution itself, so wrap the whole command in a login shell — this is the simplest correct form for a plist. The same `lms unload --all; lms load …` prefix belongs here too (a scheduled launchd fire hits the identical TTL/JIT trap):

```xml
<key>ProgramArguments</key>
<array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>cd ~/&lt;firm-slug&gt; &amp;&amp; lms unload --all; lms load qwen-3-14b-instruct --context-length 32768 --ttl 900 -y &amp;&amp; /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)"</string>
</array>
```

### The unattended permission exception (scoped `opencode.json`)

§d told you to set `"permission": {"*": "ask"}` for the whole install. **Scheduled runs are the documented exception:** cron and launchd cannot answer an interactive "ask" prompt, so an all-`ask` config would deadlock every fire. Instead, the firm's runner directory carries a **scoped** project-level `opencode.json` that pre-authorises exactly the operations a Routine needs and asks for everything else:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "python3 *": "allow",
      "mktemp *": "allow",
      "ls *": "allow",
      "cat *": "allow",
      "echo *": "allow",
      "head *": "allow",
      "tail *": "allow",
      "grep *": "allow",
      "find *": "allow",
      "wc *": "allow",
      "date": "allow",
      "date *": "allow",
      "mkdir *": "allow"
    },
    "edit": "allow",
    "external_directory": "allow",
    "webfetch": "ask"
  },
  "mcp": {
    "github-mcp": { "type": "local", "command": ["<github-mcp launch command>"] },
    "desktop-commander": { "type": "local", "command": ["<desktop-commander launch command>"] },
    "my-curator": { "type": "local", "command": ["<my-curator launch command>"] }
  }
}
```

> ⚠️ **Rule order matters — OpenCode permission rules are LAST-MATCH-WINS.** The `"*": "ask"` catch-all must be the **first** key in the `bash` object. If you put it last, it matches every command *after* the allow rules and overrides them all — every unattended fire then auto-rejects and the Routine deadlocks. (Validated live both ways: catch-all first = allow rules honoured; catch-all last = everything asks and fails.)

- The `bash` allow-list covers the ADR-001 write path (git clone + `python3`/openpyxl + `git commit -S`) **plus the read-only helpers real models actually reach for**: models emit compound commands (`ls … || echo "not found"`), and every segment must independently match an allow rule or the whole command falls to the catch-all. `echo`/`head`/`tail`/`grep`/`find`/`wc`/`date`/`mkdir` are the segments observed in live runs — everything still unlisted stays `ask` (which, unattended, means it fails loudly rather than running silently).
- `"external_directory": "allow"` lets the agent read files outside the firm folder — needed when a Routine prompt reads a `SKILL.md` from the framework clone (e.g. `~/oot-framework/skills/…`) that lives outside `~/<firm-slug>`. The alternative, if you'd rather not grant it, is to **copy the needed `SKILL.md` files into the firm folder at install time** and drop this line.
- `edit` is scoped to the working directory by virtue of the runner dir being the project root.
- Add `4thtech` (privacy) or drop MCP servers you don't use.

> The validated reference config from the live test instance is at `~/<firm-slug>/opencode.json` after install — reproduce its structure exactly (catch-all first, read-only helpers listed, `external_directory` at the permission top level).

> ⚠️ **`--auto` is NOT the way to make a scheduled run non-interactive.** Global auto-approve removes the pause on *every* action, machine-wide — the exact thing §d forbids. The scoped allow-list above is the correct, auditable form of the unattended exception: it authorises a known-small set of operations and refuses the rest. Never reach for `--auto` to "just make cron work".

### Prompt-authoring rules for unattended runs

Two OpenCode permission behaviours bite silently in unattended mode; the routine **prompts** must be authored around them (this is a constraint on how you write the `r*.prompt.md` bodies, not on the config):

1. **The permission glob does not span newlines.** A multiline `python3 -c "…"` command does **not** match the `python3 *` allow rule (the glob stops at the first newline) — so it drops to the catch-all and is **auto-rejected**, even though single-line `python3` is allowed. **Rule:** never emit multiline inline Python. Instead, instruct the agent to **write the Python to a script file with the edit tool, then run it as a single-line command** (`python3 firm/tmp/r1_writeback.py`). Single-line invocations match the glob; multiline `-c` blobs don't.
2. **`rm` is (correctly) not allow-listed**, so any deletion prompts — and unattended that means it fails. **Rule:** prompts must **never instruct deletion.** Leave temp files unstaged (they simply don't enter the commit) rather than cleaning them up.
3. **Stop on errors — but order cleanup last.** Instruct the agent to STOP on any error, **with one exception:** a permission-rejection of a *cleanup* step must not abort the *commit* step. So either put any optional cleanup **after** the signed commit, or skip cleanup entirely. Never let a rejected `rm` (or a rejected multiline command) leave the run without its commit.

### Keeping MCP servers warm (`opencode serve` + `--attach`)

Each `opencode run` that cold-boots its MCP servers pays a startup cost every fire. To avoid that, run a persistent server and attach to it:

```bash
opencode serve   # long-running; hosts the MCP servers once
# then each scheduled fire attaches instead of cold-booting:
opencode run --attach --model lmstudio/<model> "$(cat …/r<N>.prompt.md)"
```

On an always-on privacy-track machine, running `opencode serve` as a launchd/systemd unit and having the cron lines `--attach` is the low-latency setup. For a laptop (Rung 2) it's optional — the cold-boot cost is usually fine at ØØT's ~2.3 runs/day.

### Troubleshooting headless runs

Two failure modes surfaced repeatedly in live testing of `opencode run`:

- **"Unexpected server error" on every fire.** Two causes, check both:
  1. **The OpenCode DESKTOP app is running.** The CLI attaches to a running desktop app if it finds one, and the two fight over the same session — quit the OpenCode desktop app and re-run. (The desktop app's data lives separately from the CLI's, so quitting it costs you nothing.)
  2. **A corrupt CLI state database.** Run `opencode run --print-logs` and look for `SQLiteError` (e.g. `no such column`). If you see it, the CLI's state DB is corrupt — back it up so OpenCode rebuilds a fresh one:
     ```bash
     mv ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.bak
     ```
     OpenCode recreates the DB on the next run. This touches only the CLI's state — the desktop app's data is a separate store and is unaffected.
- **`opencode upgrade` hangs silently.** The in-place upgrade command can stall with no output. Don't wait on it — the curl installer is the reliable re-install path and upgrades in place:
  ```bash
  curl -fsSL https://opencode.ai/install | bash
  ```

---

## (i) Honest status

- **Author-verified:** OpenCode installs, loads the my-curator MCP, honours the `"permission": {"*": "ask"}` gate, and follows the install plan's early steps. The naming (`anomalyco/opencode`, formerly `sst/opencode`, npm `opencode-ai`) is confirmed current.
- **QUEUED:** a full **end-to-end community-track install** on the maintainer's test instance — bundled with the Phase 4 privacy-track e2e run, because both need the maintainer's accounts and cannot be run autonomously. Until that lands, the community track is documented-and-author-verified but not e2e-certified. It will be logged in [`docs/internal/agent-compatibility-log.md`](../../docs/internal/agent-compatibility-log.md) when complete.

If you run a community-track install before the maintainer does, please open a PR adding your result to the [agent compatibility log](../../docs/internal/agent-compatibility-log.md) — community-reported compatibility is how the LLM-agnostic claim stays real.
