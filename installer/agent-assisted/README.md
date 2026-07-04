# Path A — Coding-agent-assisted install + daily ops

The recommended path for ≥80% of founders, for both **install** and **daily operations**.

**Install:** you hand a markdown brief to a coding agent and the agent installs the framework. You answer questions when the agent asks; the agent handles the file edits, JSON config, GPG signing-key generation, GitHub branch protection, MCP wiring, and verification.

**Daily ops:** the same agent reads three short playbooks (DAILY / WEEKLY / MONTHLY) and runs the routine maintenance — sync GitHub to local, surface anomalies, prep BR agenda, poll partner acknowledgements. You paste a one-line prompt and the agent handles the rest.

> 🚀 **Just want to start?** → [`START-HERE.md`](START-HERE.md) gives you a single copy-paste prompt to feed your coding agent for the install.

After install, the daily-driver playbooks live alongside the install plans:

- [`DAILY-OPS.md`](DAILY-OPS.md) — every morning sync + state summary (~2 min)
- [`WEEKLY-OPS.md`](WEEKLY-OPS.md) — Friday BR prep + Sunday brain-health
- [`MONTHLY-OPS.md`](MONTHLY-OPS.md) — 1st-of-month variable pay + acknowledgement polling

This is the primary path because it best matches the framework's own discipline: humans direct, agents implement, and the artefact is the audit trail. The agent reads the install plan, executes against your machine, asks for your decisions, and produces a written summary you can hand to your accountant or your lawyer.

> **Status:** v1.0.1 (May 2026). The install plans are stable and have been tested with Claude Code (cloud track) end-to-end on the framework's authors' own machine. Other compatible agents (Augment Code, Aider, OpenCode, Cline, Continue.dev, Cursor agent mode) work but are less heavily tested. Report issues at [github.com/talirezun/oot-framework/issues](https://github.com/talirezun/oot-framework/issues).

---

## What this path is, in one minute

1. You open a coding agent in your terminal or IDE — Claude Code, Augment Code, Aider against a local LM Studio model, or any agent that meets the [capability spec](AGENT-CAPABILITY-SPEC.md).
2. You point it at the install plan for your track:
   - **Cloud track:** [`installer/agent-assisted/cloud-install-plan.md`](cloud-install-plan.md) — ~60-90 minutes wall-clock, mostly waiting for you to answer questions.
   - **Privacy track:** [`installer/agent-assisted/privacy-install-plan.md`](privacy-install-plan.md) — ~25 hours wall-clock spread across two weekends, plus ~1 week for hardware shipping.
3. The agent reads the plan, walks the steps, and asks you the questions a human installer would have to answer (firm name, partner count, jurisdictions, which optional modules to skip).
4. At the end, the agent produces an install summary at `~/.oot/install-summary.md` you can review, share, or hand to counsel.

You stay in control. Every consequential action (creating a GitHub repo, generating a signing key, configuring branch protection, running a manual test fire of a Routine, anything that costs money) requires your explicit approval before the agent proceeds.

---

## When to use Path A vs. the other paths

| | Path A (agent) | Path B (wizard) | Path C (manual docs) |
|---|---|---|---|
| **Best for** | Most founders, especially less-technical ones | Founders who explicitly avoid agent assistance | Founders who already know what they're doing |
| **Time** | 60-90 min cloud / ~25 hours privacy | similar | longer (you do every step yourself) |
| **You need** | A coding agent (Claude Code, Augment Code, Aider, …) | Just Python 3.13+ | Nothing beyond what the docs reference |
| **Strength** | Agent does the JSON edits, signs commits, runs MCPs, verifies each step | Single Python entry point, no LLM dependency | Most transparent; nothing happens you didn't type |
| **Weakness** | You need an agent that meets the [capability spec](AGENT-CAPABILITY-SPEC.md) | Slightly slower than the agent path; you drive each web-UI step yourself | Steepest learning curve; most error-prone for non-technical founders |

The framework recommends Path A for most founders because the most error-prone step in any install is "edit `claude_desktop_config.json` and paste this snippet" — that's where 60% of failed installs happen, and it's the step a coding agent can do flawlessly without the user touching the editor.

If you're philosophically opposed to handing an agent shell access to your machine — a defensible position — use Path B or Path C. The framework supports all three.

---

## What the agent does on your behalf

The install plan tells the agent how to:

1. **Verify pre-requisites** — git, curl, Python 3.13+, an Anthropic account, a GitHub account, a Slack workspace.
2. **Create the firm Ledger** on GitHub — private by default; configures branch protection (force-push off, deletion off, signed commits required); copies the framework's `templates/excel/*.xlsx` to `firm/excel/*.xlsx` in the new repo; commits the initial state.
3. **Generate signing keys** — GPG key for the bot identity that will run Routines (`oot-bot` by default); upload to GitHub; configure `git config commit.gpgsign true`.
4. **Install the Curator desktop app** — downloads the latest release; runs the post-install verification.
5. **Wire up MCPs in Claude Desktop** — edits `claude_desktop_config.json` to add the my-curator MCP; restarts Claude Desktop; runs the self-test (`use my-curator. list_domains.`) and confirms the green checkmark.
6. **Create the first Curator domain** (`firm`) and ingests a starter set of documents you choose.
7. **Configure the 4 Day-1 Routines** (R5, R6, R1, R2) via the Claude Code `/schedule` interface, attaching the right Skill Packs and connectors per `routines/cloud/<R>.md`.
8. **(Optional) Configure the Klarna gate** — branch-protection-required `oot/klarna-test` status check; `.github/workflows/klarna-gate.yml` ships in the new Ledger; auto-labeller wired up.
9. **Run a smoke test** — manually fires R5 and verifies a brain-health snapshot lands as a signed commit on `main`.
10. **Write the install summary** at `~/.oot/install-summary.md` listing every action taken, every decision deferred, and every open follow-up.

What the agent does *not* do without your explicit approval:

- Sign anything legal (the partner Charter, the Reward Species Declaration). These remain human-signed in v1.0.
- Move money. R3 / R4 produce drafts; founder approves manually; payment runs through the firm's existing payroll process.
- Create accounts on third-party services. The agent walks you to the signup page and waits for you to create the account; it never creates the account itself with your credentials.
- Decide your firm's structure. Partner count, jurisdiction, EU AI Act exposure, sovereignty mandate — those are your calls; the agent surfaces them as questions.

---

## What you need before you start

Whether cloud or privacy track:

- **A coding agent that meets the [capability spec](AGENT-CAPABILITY-SPEC.md).** Claude Code on Anthropic Pro+ is the reference; many alternatives also work.
- **A machine the agent can run on.** macOS, Linux, or WSL. Windows native works for the agent itself but the framework's bash provisioning scripts assume POSIX.
- **An hour (cloud) or a weekend (privacy) of your time** to answer the agent's questions.
- **Read [`MANIFESTO.md`](../../MANIFESTO.md), [`docs/MODULES.md`](../../docs/MODULES.md), and [`docs/00-quickstart-cloud.md`](../../docs/00-quickstart-cloud.md) (or `00-quickstart-privacy.md`) first.** The framework's discipline starts with reading. The agent will not skip this on your behalf.

---

## How to start

### Cloud track

```bash
cd ~/oot-framework  # or wherever you've cloned this repo
# In your coding agent (Claude Code, Augment Code, Aider, …) run:
# "Read installer/agent-assisted/cloud-install-plan.md and execute it.
#  Ask me the questions it tells you to ask. Stop and confirm before
#  any action that costs money or touches a third-party service."
```

The agent will read [`cloud-install-plan.md`](cloud-install-plan.md) and start at Step 0 (preflight).

### Privacy track

```bash
# Same as above, but point at:
# installer/agent-assisted/privacy-install-plan.md
```

The privacy track plan starts with the hardware-acquisition pre-week (you order hardware; the agent waits for it to arrive).

---

## What if my agent doesn't meet the capability spec?

You have two options:

1. **Use Path B (the wizard)** at [`installer/wizard.py`](../wizard.py). It's a complete Python terminal wizard (v1.2.0, steps 0–15) that asks you the same questions and drives the whole install — programmatic where safe, web-UI walkthrough where you must approve a third-party action. It's resumable (`--resume`) and has a `--dry-run`. Start it via the bootstrap one-liner in the [installer README](../README.md).
2. **Use Path C (the manual docs)** at [`docs/00-quickstart-cloud.md`](../../docs/00-quickstart-cloud.md). This is the original Weekend One / Weekend Two path. Slowest, but every step is something you typed yourself, so nothing is opaque.

If your agent meets *most* of the capability spec but fails on one item, the install plans are written defensively: the agent reads the failure, asks you to do that step manually following the linked Path C section, and then resumes from the next step.

---

## Failure modes and recovery

The install plans are **resumable**. If the agent's session ends (network, context limit, you Ctrl-C), the plan tracks state at `~/.oot/install-state.yaml`. Restart the agent, point it at the plan again, and it resumes where it left off.

The plans are **idempotent**. Re-running a step that's already done is a no-op (the agent verifies "is this already configured? yes; skip"). Safe to re-run the whole plan if you're not sure where you left off.

If something goes wrong at a step the agent can't fix, the plan tells the agent to stop and surface the issue with: (a) what was attempted, (b) what failed, (c) the relevant section of [`docs/07-troubleshooting.md`](../../docs/07-troubleshooting.md), (d) a suggested next action. You decide whether to fix manually and continue, or roll back.

Rollback is partial: things the agent did locally (file edits, git commits, key generation) can be undone. Things the agent walked you through on third-party services (creating accounts, configuring Slack) require you to manually undo on those services. The plan's final summary documents exactly what was done where, so rollback is auditable.

---

## What's next

- Read the [agent capability spec](AGENT-CAPABILITY-SPEC.md) to confirm your chosen agent is suitable.
- Read [`cloud-install-plan.md`](cloud-install-plan.md) or [`privacy-install-plan.md`](privacy-install-plan.md) yourself before handing it to the agent — it's a long markdown file, but you'll understand what's about to happen and can adjust in real time.
- When ready, point your agent at the plan and start.
