# W1 — Claude Desktop Tour

**Audience:** Any partner on day 1.
**Time:** 60-90 minutes.
**You will end with:** comfortable using Claude Desktop as your daily driver, with MyCuratorMCP green-checked, the My Curator skill loaded, and your first Brain page produced.

> 📖 The concept doc for installing Claude Desktop + the Curator is [`docs/01-installing-the-curator.md`](../01-installing-the-curator.md). This walkthrough is the day-by-day operational version with screenshots.

---

## What this is + the first 5 minutes

Claude Desktop is the framework's **daily driver** for the cloud track. It's a desktop application (macOS / Windows / Linux) that gives Claude conversational access to your tools via MCP servers, your project documents, and external connectors (Drive, Slack, Gmail, Calendar).

By the end of this walkthrough you will have:
- Installed Claude Desktop and signed in.
- Configured the first MCP connector (MyCuratorMCP) with a green checkmark.
- Loaded the My Curator skill (S1) as a Project Document.
- Connected Drive, Calendar, and Slack via the official Anthropic connectors.
- Run your first conversation that produces a Brain page.

---

## Step 1 — Download and sign in

1. Visit [claude.com/download](https://claude.com/download).
2. Pick your platform (macOS / Windows / Linux).
3. Install. macOS: drag to Applications. Windows: run installer. Linux: package manager or AppImage.
4. Launch. Sign in with your Anthropic account.

![Claude Desktop main window after first launch](../images/W1-1-claude-desktop-main.png)

*Look for the conversation pane on the left, the input area at the bottom, and the model selector in the top-right (typically "Claude Sonnet" by default).*

> 💡 **Plan choice:** Pro plan unlocks Claude Code Routines (5 runs/day — enough for solo or 2-partner firms with no Klarna gate). **Max plan (15 runs/day) is the recommended default** for 3+ partner firms or any firm with active R7. The framework's authors recommend Max for partners who do engineering daily.

---

## Step 2 — The conversation pane

The main area is the conversation pane. Three things to know:

1. **Model selector** (top-right). Claude Sonnet for daily; Claude Opus for high-stakes (Klarna scoring, complex code).
2. **New chat button** (top-left). Each chat is a separate conversation with its own context window.
3. **Project selector** (left sidebar). Projects bundle related chats with a shared set of Project Documents (your Skill Packs).

![Model selector showing Sonnet and Opus options](../images/W1-2-model-selector.png)

*The model selector dropdown shows your available models. ØØT's default is Sonnet for daily Routines and Opus for R3 (Monthly Variable Calc) per the framework's S3 §4.4 recommendation.*

---

## Step 3 — Create your first project

A Project is the framework's unit of organisation in Claude Desktop. Each firm typically has one Project per role-context (e.g. "Founder", "Engineering", "Sales") with the relevant Skill Packs loaded.

1. Click **"+ New Project"** in the left sidebar.
2. Name: `<Your-Firm-Name> — Founder` (or similar).
3. Click **"Create"**.

![New Project dialog](../images/W1-3-new-project.png)

*The Project dialog asks for a name and an optional description. Keep the name short — it shows up in the sidebar.*

---

## Step 4 — Install MyCuratorMCP

The MyCuratorMCP server is what lets Claude Desktop query and write to your Brain.

1. Open the Curator desktop app (per [`docs/01-installing-the-curator.md`](../01-installing-the-curator.md) Step 1).
2. In Curator's wizard's "MCP Setup" step, click **"Copy snippet"**.
3. Back in Claude Desktop, **Settings → Developer → "Edit Config"**. This opens `claude_desktop_config.json`.
4. Paste the snippet inside the `mcpServers` block.
5. Save the file.
6. **Quit Claude Desktop completely** (Cmd+Q on macOS, not just close the window).
7. Reopen.
8. Open the **MCP servers panel** (bottom-left tools icon).

![my-curator MCP green checkmark](../images/W1-4-mcp-green.png)

*Look for `my-curator` in the list with a green checkmark on the left. Red X = config issue; see [`docs/07-troubleshooting.md`](../07-troubleshooting.md) §MCP-1.*

> ⚠️ **The single most common pitfall:** not fully quitting Claude Desktop after editing config. Cmd+Q (macOS) or right-click tray icon → Quit (Windows). Just closing the window doesn't reload the MCP servers.

---

## Step 5 — Connect Drive / Calendar / Slack (cloud track)

The official Anthropic connectors give Claude scoped access to your cloud-track tools.

1. **Settings → Connectors** (in Claude Desktop).
2. For each: Drive, Calendar, Gmail, Slack — click **"Connect"**.
3. OAuth flow opens in browser. Sign in. Approve the requested scopes.
4. Back in Claude Desktop, the connector shows a green checkmark.

![Connectors panel with Drive, Calendar, Gmail, Slack all green-checked](../images/W1-5-connectors.png)

*All four green checkmarks = your cloud-track stack is fully wired into Claude Desktop.*

> 💡 **Privacy track:** skip Drive / Gmail. Use Desktop Commander MCP (filesystem) and 4thtech (comms) instead. See [`docs/00-quickstart-privacy.md`](../00-quickstart-privacy.md).

---

## Step 6 — Load the My Curator skill

1. Open your Project.
2. Click **"Add Project Document"**.
3. Drag-and-drop `skills/my-curator/SKILL.md` (from this repo).
4. Drop. The Skill appears in the Project Documents sidebar.

![SKILL.md loaded as a Project Document](../images/W1-6-skill-loaded.png)

*The S1 SKILL.md is now part of every chat in this project. Claude has the 17 my-curator MCP tools' instructions.*

---

## Step 7 — First conversation that produces a Brain page

In a new chat in your Project:

```
Use my-curator. List the firm domains. Then create a partner profile page for me at firm/partners/<your_id>/profile based on the partner-profile template at templates/brain/partner-profile.md. My details:
- Name: Mira Tek
- Cohort: full-time-partner
- Start date: 2026-05-08
- Jurisdiction: SI
- Two-worlds self-id: agentic-engineer
```

Watch Claude:
1. Call `mcp__my-curator__list_domains` → returns `[firm]`.
2. Call `mcp__my-curator__get_node` on the template (or read the template path you referenced).
3. Compose the page.
4. Call `mcp__my-curator__compile_to_wiki` with the new page content.

In the Curator app, your Brain now has a new page at `firm/partners/mira-tek/profile.md`.

---

## Common pitfalls

**1. MCP server stuck on red X.**
- Quit Claude Desktop fully + reopen (per Step 4 warning).
- Verify the Curator desktop app is actually running.

**2. Connector authorisation failed.**
- Re-run the OAuth flow.
- Check that your Google / Slack admin allows the Anthropic Connectors (some IT-managed accounts block OAuth apps by default).

**3. Skill Pack not loading.**
- Ensure the SKILL.md is in the Project Documents (not just in a chat).
- Drag the SKILL.md to the **top** of the Project Documents list.
- Open a *new* chat after loading (existing chats may not see new documents).

**4. "Out of context" errors mid-conversation.**
- The conversation grew too long. Start a new chat in the same project.
- Or: switch to Opus (longer context window).

**5. Connectors dropping randomly.**
- OAuth tokens expire. Re-authorise via Settings → Connectors.

---

## What's next

- **[W2 — The Curator Daily Use](W2-curator-daily-use.md)** — five operations every partner does at least weekly.
- **[W3 — Excel Monthly Variable Pay](W3-excel-monthly-variable-pay.md)** — when R3 fires on the 1st of next month.
- **[W4 — Running the Friday BR](W4-running-the-friday-business-review.md)** — your first Friday in the framework.
