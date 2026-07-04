# START HERE — copy-paste this into your coding agent

You're about to install the ØØT framework on your machine. This page gives you a single block of text to paste into your coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, Continue, or any agent that meets the [capability spec](AGENT-CAPABILITY-SPEC.md)). The agent will read the install plan, walk through the steps, and ask you the questions when needed.

If you don't yet have a coding agent installed, see the [README](README.md) → "When to use Path A vs. the other paths" — for less-technical founders who don't want to use any agent, the manual track at [`docs/00-quickstart-cloud.md`](../../docs/00-quickstart-cloud.md) covers the same ground in plain English.

---

## What to do

1. Open your coding agent in your terminal or IDE.
2. **Make sure your working directory is the cloned ØØT framework repo** (or the agent has access to the install plan files).
   - If you used the one-line bootstrap (the `curl ... | bash` in the [installer README](../README.md)), the repo is already cloned at `~/.oot/oot-framework` — `cd ~/.oot/oot-framework`.
   - Otherwise, clone it yourself:
   ```bash
   git clone https://github.com/talirezun/oot-framework.git ~/oot-framework
   cd ~/oot-framework
   ```
3. Copy the prompt below verbatim into your agent.
4. Answer the agent's questions. The whole install takes ~60-90 minutes for cloud track, mostly waiting for you to type answers.

---

## The prompt — copy this verbatim

```
I'm installing the ØØT framework on my machine for the cloud track. Please drive
the install end-to-end by following the agent-runnable plan at:

  installer/agent-assisted/cloud-install-plan.md

Ground rules I want you to follow:

1. Read the plan from the top before starting. It defines the install state file
   (~/.oot/install-state.yaml), the resumability protocol, the pause-and-confirm
   gates, and the failure handling. Don't skip the preamble.

2. Pause and confirm with me before any action that costs money, sends a message
   to a third party, creates an account, generates a cryptographic key, pushes
   to a remote repository, or configures branch protection. The plan flags these
   with the "🟡 ASK USER" marker — when you hit one, surface it to me clearly
   and wait for my "yes" or "no".

3. If a step requires me to do something on a third-party service (GitHub.com,
   Anthropic's website, the Curator app), tell me the exact button-by-button
   sequence and wait for my "done" before continuing.

4. If you can't do a step (a tool is missing, a permission is denied, an API
   call fails), surface the exact error to me, propose a fix, and wait for me
   to decide whether to retry, fix manually, or skip.

5. Don't downgrade silently. If signed-commit fails, retry with backoff; if it
   keeps failing, stop and tell me — never push an unsigned commit without my
   explicit "yes, push unsigned".

6. Translate technical for me. I'm not a developer. When you ask me to do
   something, frame it for someone who has never opened a JSON file. Show me
   what's happening before it happens.

7. After every step, update ~/.oot/install-state.yaml so we can resume if your
   session ends.

When the install is complete, write a summary at ~/.oot/install-summary.md that
I can review and hand to my accountant or counsel.

Start with Step 0 of the plan.
```

---

## Notes

- **Privacy track:** if you're installing on the privacy track instead, replace the path in the prompt with `installer/agent-assisted/privacy-install-plan.md`. Everything else stays the same.
- **If your agent doesn't fully meet the [capability spec](AGENT-CAPABILITY-SPEC.md):** the plan has fallbacks — when the agent can't do a step (e.g. no native MCP support), it'll ask you to do that step manually following the linked manual-track section in `docs/00-quickstart-cloud.md`.
- **Cost expectations:** the install itself is free. Anthropic's plan (Pro at ~€20/month or Max at ~€100/month) is what powers Claude Desktop + Claude Code Routines after the install. GitHub Free private repos work for solo / 2-person firms but **don't enforce branch protection** — see Step 3 of the install plan for the GitHub plan-tier trade-off.
- **What you keep:** at the end of the install you have a working ØØT instance with a Ledger GitHub repo (yours), a signing key (yours), the Curator integration wired (yours), and a written install summary. Nothing the agent did is locked behind the framework's authors — everything is in your accounts and your filesystem.
