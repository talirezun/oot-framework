# Agent Capability Spec — what your coding agent must be able to do

This is the formal spec for "is my coding agent good enough to drive an ØØT install?" The framework's install plans assume an agent meeting all the *required* capabilities below. *Recommended* capabilities make the install smoother but aren't strictly necessary.

The spec is **LLM-agnostic where possible**. The framework doesn't require Claude or any specific LLM — it requires a coding-agent harness that meets the behaviour spec. What model the harness runs is up to you (and your privacy/cost preferences).

If your agent fails one of the required items, you can still run the install plans with manual fallback at the failed step (see [`README.md`](README.md) "What if my agent doesn't meet the capability spec").

---

## Required capabilities

### R1 — File reads and writes on the user's machine

The agent must be able to read arbitrary files in the working directory and write/edit files (typically via Read/Write/Edit-style tools). Without this it cannot edit `claude_desktop_config.json`, copy `.xlsx` templates into the firm's Brain repo, or scaffold the `firm/` namespace.

### R2 — Shell command execution

The agent must be able to run arbitrary shell commands (typically via a Bash-style tool) and observe their output. The plans use `git`, `curl`, `gpg`, `jq`, `python3`, and platform-specific package managers. Required for: cloning the framework repo, generating signing keys, signing commits, running `python3 scripts/build_excel.py` and `python3 scripts/validate_skills.py`, manually firing test Routines.

### R3 — Markdown comprehension at the install-plan scale

The install plans are 1500-2500 line markdown files with H1/H2/H3 structure. The agent must follow them sequentially without losing track between steps. As a rough proxy: an agent that reliably handles a 50-step task list across one session has enough context discipline.

### R4 — Pause-and-confirm before consequential actions

The agent must stop and ask the user before any action that:
- Costs money (paying for a service, a stripe upgrade, an API call against a metered key the user hasn't pre-approved).
- Sends a message to a third party (Slack post, email, GitHub issue, GitHub PR comment).
- Creates an account on a third-party service.
- Generates a cryptographic key (signing key, API key, OAuth token).
- Pushes to a remote git repository.
- Configures branch protection or any other GitHub repo-level setting.

If the agent can be configured to require approval for *all* tool uses, that's overkill but acceptable. If the agent has no approval-requirement mechanism at all, it fails this requirement and is unsafe to drive the install.

### R5 — Honest failure reporting

When a step fails, the agent must tell the user: what was attempted, what failed (with the actual error output, not a paraphrase), and what it tried as a remedy. The plans assume the agent surfaces failures honestly rather than masking them.

This is a tested-by-the-author bar. Agents that have a tendency to produce optimistic summaries that don't match reality ("the install completed successfully" when it didn't) fail this requirement. Trust-but-verify: the install summary at the end is something the user reads and spot-checks.

---

## Recommended capabilities

### A1 — Native MCP support

The plans configure MCP servers (my-curator, possibly GitHub MCP, possibly Excel MCP). An agent that natively speaks MCP can verify the configuration by calling the MCP tools directly — `use my-curator. list_domains.` — and confirm the green checkmark before moving on.

Agents without MCP support can still drive the install, but verification falls back to "ask the user to open Claude Desktop and confirm the green checkmark" — slower and more error-prone.

### A2 — Long context window (≥200k tokens)

The install plans plus the framework's foundation kit they reference total ~80-120k tokens. An agent with a 200k+ context window holds the whole picture without dropping things. Smaller-context agents work but may need the user to remind them of earlier decisions ("we're on cloud track, EU jurisdiction, 3 partners — keep going from Step 7").

If your agent has a 100k context window, prefer to break the install into 2-3 sessions, keeping the install state file (`~/.oot/install-state.yaml`) as the bridge.

### A3 — Web fetch / browse

The agent occasionally needs to fetch a current URL (Curator's latest release, Anthropic's pricing page, the Bitwarden CLI download). Agents without web access can still drive the install but need the user to fetch URLs manually.

### A4 — Git workflow understanding

The agent needs to understand that signed commits are different from unsigned commits, that branch protection rejects unsigned pushes, and that Routines that fail to push must retry rather than silently downgrade. This is mostly captured by the plan's prompts, but an agent that already understands the git mental model will navigate it better.

### A5 — Plan / TODO tracking

The agent should track which install steps are complete vs. pending, ideally in a way the user can inspect. Most modern coding agents have a TodoWrite-style or task-tracker mechanism; using it is recommended but not required.

---

## Known compatible agents

This list is current as of v1.0.1 (May 2026). It's not exhaustive — the framework is LLM-agnostic — and we update as new agents launch and we test them.

### Tested end-to-end (cloud track)

- **Claude Code** — the reference. Anthropic's own CLI agent. Works on Pro / Max / Team. Native MCP, signed commits, web fetch, TodoWrite, long context. The framework's authors test against Claude Code first.
  - Cloud-track install: Claude Sonnet 4.6+ (Sonnet recommended; Opus for the few high-stakes steps).
  - Privacy-track install: same agent, but with `claude.com/settings/api-keys` revoked and Claude Code pointed at a local LM Studio Anthropic-API-compatible endpoint. **Privacy-track install with Claude Code is possible but unconventional**; OpenCode or Aider against LM Studio is the cleaner path.

### Tested cloud track

- **Augment Code** — strong on multi-file builds; excellent context handling. Works against Anthropic / OpenAI / others. MCP support varies by version. https://www.augmentcode.com/
- **Aider** — minimalist; works against any OpenAI-compatible API including LM Studio's local server endpoint. No native MCP yet (May 2026); manual fallback for MCP verification steps. https://aider.chat/
- **OpenCode (opencode-ai)** — open-source Claude Code competitor. Native MCP. https://github.com/sst/opencode
- **Cline (formerly Claude Dev)** — VSCode extension, broad model support including local. https://github.com/cline/cline
- **Continue.dev** — VSCode/JetBrains extension, broad model support. https://www.continue.dev/

### Tested privacy track

- **OpenCode against LM Studio** — Qwen 3 32B+ recommended for sustained 50-step tasks; Llama 3.3 70B for the high-stakes config-file edits. Tested by the framework's authors on a Mac mini M4 Pro 32GB.
- **Aider against LM Studio** — same model recommendations. Aider is more terse in its outputs which suits the privacy track's "no chatter, just do" preference.
- **Cline against LM Studio** — works; UI is friendlier than Aider for non-technical privacy-track founders.

### NOT recommended

- **Cursor agent mode** — works but is IDE-bound, which makes the install plan's "open the terminal and run X" steps awkward. Use Cline instead if you want a VSCode-resident agent.
- **ChatGPT plain (no agent harness)** — does not meet R1, R2, R4. Not a coding agent in the sense the plans require.
- **Any agent that doesn't pause-and-confirm before consequential actions.** R4 is non-negotiable.

---

## Plan choice and what your agent's underlying LLM should be capable of

The install plans don't require a frontier reasoning model. They require a model strong enough to:

- Read a 1500-line markdown plan and follow its sequential structure.
- Recognise template-variable substitutions (`{{FIRM_NAME}}` → the value the user gave at Step 3).
- Write idiomatic shell commands and explain them before running.
- Edit JSON config files without breaking syntax.
- Recognise when a tool result contains an error (red text from `git push` rejected) and surface it to the user.

In practice: any model that handles "Software 3.0" tasks well — Claude Sonnet 4.6+, Claude Opus 4.7, GPT-5, Gemini 2.5 Pro, Qwen 3 32B+, Llama 3.3 70B+, DeepSeek-V3 — handles the install. Smaller models (7B, 13B) typically lose track around step 30 and are not recommended.

For the **R3 monthly variable calc** specifically — the highest-stakes Routine in the framework — the docs recommend the strongest available model regardless of agent: Claude Opus 4.7 on cloud track, Llama 3.3 70B 4-bit on privacy track. This is independent of the install: the install configures R3 to *call* that model regardless of what model your install-time agent is using.

---

## How to validate your agent before running the install

Before pointing your agent at `cloud-install-plan.md`, run this 3-question pre-flight in your agent session. If it fails any of them, switch to a different agent or fall back to Path B / Path C.

1. **"Read `installer/agent-assisted/AGENT-CAPABILITY-SPEC.md` and tell me which sections apply to you."** A well-behaved agent will read this file and either (a) confirm it meets all required capabilities or (b) honestly flag the items it can't do.

2. **"Show me what `claude_desktop_config.json` looks like on this machine without modifying it. If it doesn't exist, tell me where it should live."** Tests R1 (file reads), R5 (honest reporting). Should produce either the file's content or "this file does not exist at the expected path".

3. **"Write a one-paragraph summary of what `python3 scripts/validate_skills.py` does in this repo, then run it and report the result."** Tests R1, R2, R3, R5 in sequence. Should produce: a paragraph, then run the script, then surface the output. If the agent skips reading the file and runs the script blindly, R3 (markdown comprehension) is failing.

If the agent passes all three, point it at `cloud-install-plan.md` (or `privacy-install-plan.md`) and start.

---

## Reporting agent compatibility

We track which agents work well at [`docs/internal/agent-compatibility-log.md`](../../docs/internal/agent-compatibility-log.md) (v1.x — currently a stub). If you successfully run the install with an agent not in the "Known compatible" list above, please open a PR adding it to the log with:

- Agent name + version
- LLM backend used
- Track (cloud / privacy)
- Issues encountered + workarounds
- Time-to-complete

Community-reported compatibility is how the LLM-agnostic claim stays real.
