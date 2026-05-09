# 01 — Installing the Curator

**Audience:** All. Step-by-step Curator install for both cloud and privacy tracks.
**Time:** ~90 minutes including the first ingest.
**You will end with:** Curator desktop app running, MyCuratorMCP wired into Claude Desktop, your first domain populated with five sample documents.

> 📖 The Curator is the framework's **Brain implementation**. Skill Pack S1 imports the Curator's canonical `SKILL.md` verbatim — every other Skill Pack writes into the Brain via S1's discipline. Read `MANIFESTO.md` Thesis 4 (the Collecting Brain) first.

---

## What this is + the first 5 minutes

The Curator is an **open-source desktop app + MCP server** that turns your firm's markdown files into a queryable knowledge graph. It exposes 17 tools through the MyCuratorMCP server: 10 read tools (`list_domains`, `get_index`, `search_wiki`, `get_node`, etc.) and 7 write tools (`compile_to_wiki`, `fix_wiki_issue`, `scan_wiki_health`, etc.).

The Brain you build with the Curator is the framework's **most important compounding asset**. Six months in, the Brain is the firm's most valuable IP, by construction.

**By the end of this doc:**
- Curator desktop app installed.
- Cloud-LLM ingest configured (Gemini Flash Lite — the framework's recommended cost-effective default).
- MyCuratorMCP installed in Claude Desktop.
- The My Curator skill (S1) loaded as a Project Document.
- Self-test passed.
- First Curator domain created (`firm`).
- First 5 documents ingested.
- First health check run.

---

## Why the Brain matters

Three reasons in one paragraph: **(1)** Every conversation, decision, contract, and customer interaction is candidate knowledge that compounds. **(2)** AI agents need structured context to be useful at firm scale; the Brain *is* the context. **(3)** The framework's compensation system (Skill Pack S3) reads the Brain to produce daily output ledgers, monthly variable statements, and quarterly long-tail entitlements. Without the Brain, the framework cannot operate.

See `MANIFESTO.md` Thesis 4 for the long version.

---

## Pre-requisites

- A machine to run the Curator on. **Cloud track:** your daily-driver laptop. **Privacy track:** the always-on machine (Mac mini / NUC / Pi 5).
- Claude Desktop installed (per [docs/00-quickstart-cloud.md](00-quickstart-cloud.md) §"Saturday afternoon").
- A Google AI Studio account (for Gemini Flash Lite ingest) OR an Anthropic API key (for Claude ingest).
- ~10 GB free disk space.

---

## Step 1 — Install the Curator desktop app

1. Visit [github.com/talirezun/the-curator/releases/latest](https://github.com/talirezun/the-curator/releases/latest).
2. Download the platform-appropriate installer (`.dmg` for macOS, `.deb` / `.AppImage` for Linux, `.exe` for Windows).
3. Install. macOS: drag to Applications. Linux: `sudo apt install ./curator.deb` or run the AppImage directly. Windows: run the installer.
4. Launch. The first-launch wizard appears.

![Curator first-launch wizard](images/01-1-curator-first-launch.png)

*Look for the "Welcome to the Curator" screen with three setup steps shown in the wizard sidebar.*

---

## Step 2 — Configure cloud-LLM ingest

The Curator's ingest pipeline parses raw documents (PDFs, transcripts, markdown, etc.) into the structured wiki format the Brain uses. Gen 1 uses cloud LLMs for this; Gen 2 will land local-LLM ingest.

**Recommended provider:** **Gemini Flash Lite** for routine ingest, **Anthropic Claude** for high-stakes documents (contracts, board memos).

**Cost:** typically <€10/month for heavy usage on Gemini Flash Lite. ~€20-30/month if you switch to Claude for everything.

1. In the wizard's "Ingest provider" step, select **Gemini Flash Lite**.
2. Paste your Google AI Studio API key (get one at [aistudio.google.com](https://aistudio.google.com/)).
3. Click "Test connection". You should see a green checkmark.
4. Optionally, configure a fallback to Anthropic Claude for important documents.

> ⚠️ **The API key is stored in your OS keychain by the Curator** — not in a config file on disk. This is the right behaviour. Per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md), credentials live in keychains or Bitwarden, never in plaintext.

---

## Step 3 — Configure MyCuratorMCP in Claude Desktop

The MyCuratorMCP server is what lets Claude Desktop (and any other MCP-compatible client) query and write to your Brain.

1. In the Curator's wizard, the **"MCP Setup"** step shows a config snippet. Click **"Copy snippet"**.
2. Open Claude Desktop. Settings → Developer → "Edit Config". This opens `claude_desktop_config.json` in your default editor.
3. Paste the snippet inside the `mcpServers` block. Save.
4. **Restart Claude Desktop** (fully quit + reopen).
5. In Claude Desktop, open the MCP servers panel (bottom-left tools icon). You should see `my-curator` listed with a green checkmark.

![my-curator MCP green checkmark](images/01-3-mcp-green.png)

*Look for the green checkmark next to "my-curator". Red X indicates a config issue — see Common pitfalls below.*

---

## Step 4 — Install the My Curator skill (S1)

The S1 SKILL.md tells Claude how to use the my-curator MCP tools well, in the order that produces the best results.

1. Locate `skills/my-curator/SKILL.md` in this repo (the Curator's canonical SKILL.md, with ØØT preamble).
2. In Claude Desktop, open or create the **Project** for your firm. Click "Add Project Document".
3. Drag-and-drop `SKILL.md` into the project documents pane.
4. Verify Claude can see it: open a new chat in the project, ask: *"Do you have the my-curator skill loaded? Summarise its main sections."* Claude should respond with the skill's purpose and the 17 MCP tools.

---

## Step 5 — Run the self-test

In Claude Desktop, in the project with my-curator skill loaded, run:

```
Use my-curator. List the available domains. Then run scan_wiki_health on whatever domain exists. Report back.
```

Expected behaviour:
- Claude calls `list_domains` → returns either `[]` (no domains yet) or `[firm]` (if the wizard created a default).
- Claude calls `scan_wiki_health` → returns a clean report (no broken wikilinks, no orphans — because the Brain is empty).

If both calls succeed, the Curator + MCP + skill are working end-to-end. Move to Step 6.

If a call fails, see [Common pitfalls](#common-pitfalls) below.

---

## Step 6 — Create your first domain

Domains are siloed knowledge graphs (per `templates/brain/FIRM-ONTOLOGY.md`). Most firms start with `firm` (internal company knowledge) and add others as scale demands.

In the Curator app's UI:

1. Click "Domains" → "Create domain".
2. Name: `firm`. Description: "Internal company knowledge".
3. Click "Create".
4. The Curator scaffolds the folder structure under `domains/firm/wiki/`.

Now in Claude Desktop:

```
Use my-curator. Create the firm/index.md page with a 4-paragraph firm overview based on the following: <paste a brief description of your firm>.
```

Claude composes the page using the canonical structure, calls `compile_to_wiki`, and the page lands in your Brain.

---

## Step 7 — First ingest (5 sample documents)

Pick five existing documents that represent your firm's knowledge:

- A recent customer contract.
- A strategic memo (founder's recent thinking).
- A product spec or technical document.
- A pitch deck (export to PDF).
- A meeting transcript (Otter, Fireflies, or similar — export to plain text).

In the Curator app:

1. Click "Ingest" → drag-and-drop the five files.
2. The Curator processes them via Gemini Flash Lite (or your configured provider).
3. Each document becomes one or more wiki pages. The Curator suggests slugs and wikilinks; review and accept.
4. **Fix any broken wikilinks** the Curator's `scan_wiki_health` flags. Use `fix_wiki_issue` from Claude Desktop, or edit manually.

> 💡 **Tip:** the first ingest is when you discover your firm's implicit ontology. Don't rush it. Spend the time to get the slug structure right; future-you will thank present-you.

---

## Step 8 — First health check + bookmarks

```
Use my-curator. scan_wiki_health on domain=firm. scan_semantic_duplicates on domain=firm. Report.
```

Expected: no broken wikilinks (you fixed them in Step 7); no orphan pages; no semantic duplicates (you only have 5 pages).

Bookmark in Claude Desktop:
- The project with the my-curator skill.
- A frequently-used MCP query: `mcp__my-curator__get_index domain=firm`.

You're done. The Brain is operational.

---

## What's next

- Install Routine R5 (Brain Health Check) so `scan_wiki_health` runs every Sunday automatically. See [`docs/02-installing-routines.md`](02-installing-routines.md) (cloud) or [`docs/02-installing-routines-privacy.md`](02-installing-routines-privacy.md) (privacy).
- Onboard your first partner. They'll create their `firm/partners/<id>/profile.md` page during onboarding. See [`docs/03-onboarding-a-partner.md`](03-onboarding-a-partner.md).

---

## Common pitfalls

**1. MyCuratorMCP shows red X in Claude Desktop.**
- Cause: Claude Desktop wasn't fully restarted after pasting the config.
- Fix: quit Claude Desktop completely (Cmd+Q on macOS, not just close window), reopen.

**2. "Provider authentication failed" during ingest.**
- Cause: API key invalid or quota exhausted.
- Fix: re-paste API key in the Curator's settings; verify quota on [aistudio.google.com](https://aistudio.google.com/).

**3. `scan_wiki_health` reports many broken wikilinks after ingest.**
- Cause: the Curator's first-pass extraction sometimes proposes wikilinks to slugs that don't exist yet.
- Fix: run `fix_wiki_issue` — for each broken link, accept the suggested fix or rephrase. The Brain is iteratively refined; first-ingest hygiene is normal.

**4. The S1 skill is loaded but Claude doesn't seem to call my-curator tools.**
- Cause: the project document order matters. SKILL.md should be at the top.
- Fix: in Claude Desktop project settings, drag the SKILL.md to the top of the project documents.

**5. Curator app crashes on macOS Sonoma+.**
- Cause: known issue with older Curator builds and recent macOS versions.
- Fix: download the latest release; the issue is fixed in v1.2+.

---

## When to escalate

- The Curator's GitHub issues: [github.com/talirezun/the-curator/issues](https://github.com/talirezun/the-curator/issues).
- The Curator's wiki: [github.com/talirezun/the-curator/blob/main/README.md](https://github.com/talirezun/the-curator/blob/main/README.md).
- ØØT-specific Brain ontology questions: see [`templates/brain/FIRM-ONTOLOGY.md`](../templates/brain/FIRM-ONTOLOGY.md).

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. The Curator handles your firm's knowledge graph; data residency and processing implications vary by jurisdiction. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md).
