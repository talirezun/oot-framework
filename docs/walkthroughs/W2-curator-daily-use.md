# W2 — The Curator: Daily Use

**Audience:** Any partner who has installed the Curator and wants to use it daily.
**Time:** 30-60 min for the walkthrough; ongoing daily use thereafter.
**You will end with:** comfortable using the five operations every partner does weekly: ingest, query, write, scan, fix.

> 📖 **Concept doc:** [`docs/01-installing-the-curator.md`](../01-installing-the-curator.md). **Skill Pack:** [`skills/my-curator/SKILL.md`](../../skills/my-curator/SKILL.md).

---

## What this is + the first 5 minutes

Five operations. Master these and the Brain compounds:

1. **Ingest** — drop a document into the Curator → it becomes wiki pages.
2. **Query** — ask Claude (with my-curator MCP) about Brain content.
3. **Write** — produce a new Brain page from a conversation.
4. **Scan** — weekly health check + duplicate detection.
5. **Fix** — repair broken wikilinks, dismiss false-positive duplicates.

---

## The Curator desktop app — your daily window

![Curator app main window](../images/W2-1-curator-main.png)

*Three things to know: the **Domains** sidebar (left) shows your knowledge graphs; the **Files** view (centre) shows the markdown pages in the selected domain; the **Ingest** button (top-right) is your daily entry point.*

---

## Operation 1 — Ingest

The most common Curator action. Drop a document → it becomes structured wiki pages.

### Step-by-step (with screenshots)

1. Click **"Ingest"** (top-right).
2. Drag-and-drop a file (PDF, transcript, markdown, image with OCR, etc.).
3. The Curator processes via the configured cloud LLM (Gemini Flash Lite default).
4. **Review the proposed slug + title + frontmatter.** The Curator suggests; you confirm.
5. **Review the proposed wikilinks.** If the Curator proposes `[[some-slug]]` and that slug doesn't exist yet, you can:
   - Create the target stub now.
   - Drop the wikilink (use plain text).
   - Defer (save the page; fix later via `scan_wiki_health`).
6. **Click "Compile to Wiki".** The page lands in the Brain.

![Ingest dialog with proposed slug and wikilinks](../images/W2-2-ingest-dialog.png)

*Watch for the "Wikilink target not found" warning on any proposed `[[slug]]`. The Curator's discipline: never produce broken wikilinks at ingest time.*

### What to ingest

- Customer call transcripts (export from Otter / Fireflies as plain text).
- Contracts (PDF). Use Anthropic Claude as ingest provider for these (higher accuracy).
- Strategic memos / founder notes.
- Pitch decks (export to PDF; the Curator extracts text + slide structure).
- Meeting recordings (export transcript first; recording → PollinationX for storage).

### What NOT to ingest

- Code (use Skill Pack S4 ADRs instead).
- Spreadsheets that are already framework templates (X1-X9).
- Bulk media files (>10MB) — use PollinationX with `[[px:<cid>]]` wikilinks.
- Anything you wouldn't want a future partner reading.

---

## Operation 2 — Query (via Claude Desktop with my-curator MCP)

Claude is your front-door to the Brain. Open a chat in your Claude Desktop project (with my-curator skill loaded).

### Three query patterns

**Pattern 1 — Get the index of a domain:**

```
Use my-curator. Show me the index of the firm domain.
```

Returns the structured tree of pages. Your starting point for navigation.

**Pattern 2 — Search:**

```
Use my-curator. Search the firm domain for "Acme Corp" — return top 10 hits with relevance scores.
```

The Curator runs hybrid retrieval (vector + graph traversal) and returns ranked results.

**Pattern 3 — Drill into a node:**

```
Use my-curator. Get the node at slug partners/mira-tek/profile. Then get the connected nodes (depth 1).
```

Returns the page content + the immediate graph neighbourhood (backlinks, outbound wikilinks).

### Cross-domain search

```
Use my-curator. Search across the firm, customers, and legal domains for "Acme Corp" since 2026-01-01.
```

This is the framework's discipline: cross-domain *reasoning* via `search_cross_domain` is allowed; cross-domain *wikilinks* are not (per `templates/brain/FIRM-ONTOLOGY.md`).

---

## Operation 3 — Write a Brain page

Three patterns for writing pages.

### Pattern A — Direct compile from a conversation

```
Use my-curator. Compile the conversation we just had about the Acme MSA into a Brain page at customers/acme-corp/contracts/acme-msa-2026-04. Use the contract template structure.
```

Claude composes the page; calls `mcp__my-curator__compile_to_wiki`. The page lands.

### Pattern B — From a template

```
Use my-curator. I'm drafting an Output Spec for a new feature. Use templates/brain/output-spec.md. The output is OAuth2 PKCE for partner onboarding. Value tier M. Expected outcome: PKCE protection enabled with no UX impact.
```

Claude fills in the template's placeholders, asks for any missing data, then compiles.

### Pattern C — Update an existing page

```
Use my-curator. Update partners/mira-tek/profile to add a "Recent output specs" section listing the three output specs I drafted this week.
```

Claude reads the current page, modifies, re-compiles.

> ⚠️ **The Curator refuses speculative wikilinks.** If you ask Claude to write a page that references `[[architecture/auth-rewrite-2026]]` and that page doesn't exist, Claude will pause and ask whether to create the stub first.

---

## Operation 4 — Scan (the Sunday discipline)

Routine R5 fires every Sunday 09:00 and does this automatically. But you can run it ad-hoc:

```
Use my-curator. Run scan_wiki_health on the firm domain. Then scan_semantic_duplicates. Report.
```

The output is a report:
- **Broken wikilinks:** N.
- **Orphan pages:** N.
- **Stale pages:** N (>90 days no update on `status: active`).
- **Semantic duplicates:** N clusters.

### What to fix yourself

- **Typo-correctable broken wikilinks:** `Use my-curator. fix_wiki_issue on issue X. Use the suggested slug.`
- **Orphan pages:** typically need a backlink from somewhere. Add one.
- **Stale active pages:** either update them or change `status: active` → `status: archived`.

### What to dismiss

- **Semantic duplicates that aren't actually duplicates** (the Curator can over-flag; e.g. two Output Specs about adjacent features are not duplicates):
  ```
  Use my-curator. dismiss_wiki_issue on cluster X with reason "These are adjacent features, not duplicates".
  ```

---

## Operation 5 — Fix

The `fix_wiki_issue` tool is for single-page repairs. For larger restructures (renaming a slug across the Brain), use the Curator app's UI directly.

### Renaming a slug (the canonical path)

If you need to rename `partners/mira` → `partners/mira-tek`:

1. **Don't just rename.** Backlinks would all break.
2. Open the Curator app's UI.
3. Use the "Rename slug" dialog. The Curator renames the file AND updates every backlink AND records the rename as `status: superseded` with `superseded_by: <new-slug>` on the old (preserves audit trail).
4. Run `scan_wiki_health` to verify no new breakage.

---

## Daily / weekly cadence

- **Daily:** ingest 1-3 documents (whatever you produced or read that day worth keeping).
- **Daily:** query the Brain before any decision (the discipline: ask the Brain before asking a partner; partners are not encyclopaedias).
- **Weekly:** glance at R5's Sunday report; fix anything in the "needs human attention" list.
- **Quarterly:** review the Brain's growth (slug count, page-edit cadence, semantic-duplicate trend) at the partner check-in.

---

## Common pitfalls

**1. Ingesting low-quality sources.**
- Cause: dropping a noisy auto-transcript that the Curator can't parse cleanly.
- Fix: clean up the transcript first (remove timestamps, fix obvious typos), then ingest.

**2. Pasting page content into a chat instead of querying.**
- Cause: forgetting that Claude has my-curator MCP access.
- Fix: always start with `Use my-curator. Get the node at <slug>` — context window stays small; the model fetches what it needs.

**3. Ignoring R5's weekly report.**
- Cause: it feels like a chore.
- Fix: the report should be 10-15 items max if you're using the Brain well. If it's 50+, the Brain is decaying. Address now while it's still cheap.

**4. Speculative wikilinks slipping through.**
- Cause: Claude writes `[[some-slug]]` to a non-existent page; user accepts; broken link enters the Brain.
- Fix: read your own diffs before committing. The Curator's `compile_to_wiki` shows a preview.

**5. Cross-domain wikilinks (which don't resolve).**
- Cause: from `firm/`, writing `[[customers/acme-corp]]` — looks like a wikilink, but cross-domain wikilinks don't resolve via the Curator.
- Fix: cross-domain references are explicit. The convention `[[customers/acme-corp]]` works in human-readable display but `mcp__my-curator__search_cross_domain` is the canonical way to actually find content across domains.

---

## What's next

- **[W3 — Excel Monthly Variable Pay](W3-excel-monthly-variable-pay.md)** — the founder's monthly review ritual.
- **[W4 — Running the Friday BR](W4-running-the-friday-business-review.md)** — the partnership's weekly heartbeat.
