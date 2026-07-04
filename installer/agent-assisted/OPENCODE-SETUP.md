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

### Minimal `opencode.json`

Global config lives at `~/.config/opencode/opencode.json`; a per-project `opencode.json` in the repo root overrides it. A minimal config that sets a model looks like this:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "google/gemini-2.5-flash-lite"
}
```

For a local model via LM Studio (OpenAI-compatible endpoint), you configure it as a provider in `opencode.json` — see OpenCode's provider docs at [opencode.ai](https://opencode.ai). For the free built-in models you don't need to set `model` at all; OpenCode prompts you.

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

The Curator installs a **local MCP server** (the my-curator server) so the agent can read and write your Second Brain. OpenCode speaks MCP natively — add the server under the top-level `mcp` key in `opencode.json`. There are two ways the Curator exposes the server; use whichever matches your Curator install:

### Variant 1 — local-HTTP (the Curator's local server at 127.0.0.1:8765)

The Curator runs a local HTTP MCP endpoint at `http://127.0.0.1:8765/mcp`. Bridge it into OpenCode with `mcp-remote` (a small stdio↔HTTP shim via `npx`), the same pattern the cloud install plan uses for Claude Desktop:

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

### Variant 2 — local stdio server directly

If your Curator install exposes the my-curator server as a direct stdio command (rather than the HTTP endpoint), configure it as a `local` server whose `command` array is the server's launch command. Check your Curator app's "MCP" / "integrations" panel for the exact command it wants you to run (it's the same command the Curator prints for the Claude Desktop `mcpServers` block — OpenCode's `command` array takes the executable and its args as list elements):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-curator": {
      "type": "local",
      "command": ["<the-curator-mcp-executable>", "<arg1>", "<arg2>"]
    }
  }
}
```

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

## (h) Honest status

- **Author-verified:** OpenCode installs, loads the my-curator MCP, honours the `"permission": {"*": "ask"}` gate, and follows the install plan's early steps. The naming (`anomalyco/opencode`, formerly `sst/opencode`, npm `opencode-ai`) is confirmed current.
- **QUEUED:** a full **end-to-end community-track install** on the maintainer's test instance — bundled with the Phase 4 privacy-track e2e run, because both need the maintainer's accounts and cannot be run autonomously. Until that lands, the community track is documented-and-author-verified but not e2e-certified. It will be logged in [`docs/internal/agent-compatibility-log.md`](../../docs/internal/agent-compatibility-log.md) when complete.

If you run a community-track install before the maintainer does, please open a PR adding your result to the [agent compatibility log](../../docs/internal/agent-compatibility-log.md) — community-reported compatibility is how the LLM-agnostic claim stays real.
