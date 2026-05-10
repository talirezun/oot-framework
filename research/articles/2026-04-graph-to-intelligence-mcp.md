---
title: "From Graph to Intelligence: The My Curator MCP and the Art of Querying Your Second Brain"
author: "Dr. Tali Režun"
author_affiliation: "Vice Dean of Frontier Technologies, COTRUGLI Business School"
date: 2026-04-27
topic: "Thesis 4 (the Brain) / Thesis 5 (composable Lego) / S1 my-curator"
peer_reviewed: no
type: external-article
external_url: "https://github.com/talirezun/the-curator/blob/main/research/articles/from-graph-to-intelligence-my-curator-mcp.md"
publication: "The Curator Research Series — Article 3"
---

# From Graph to Intelligence: The My Curator MCP and the Art of Querying Your Second Brain

**By Dr. Tali Režun**
Vice Dean of Frontier Technologies, COTRUGLI Business School
Published: 2026-04-27
Source: [The Curator Research Series — `from-graph-to-intelligence-my-curator-mcp.md`](https://github.com/talirezun/the-curator/blob/main/research/articles/from-graph-to-intelligence-my-curator-mcp.md)

> How My Curator MCP turns your Second Brain into a frontier-AI research partner — a private bridge between the knowledge you have built and the reasoning models that can finally read it as a graph, not a folder.

---

## Summary

The third article in The Curator series argues that the Second Brain only becomes fully useful once a frontier reasoning model can interrogate it **as a graph**, not as a flat folder of files. Most users get stuck at the wrong loop: the Brain is structured beautifully in Obsidian, but every time they want to ask a real question they fall back into a generic chat window that has no idea their graph exists. The mismatch wastes the whole architecture.

**My Curator MCP** is the standalone bridge that closes that gap. It is a Model Context Protocol server, distinct from The Curator desktop app (which handles ingest), that exposes the user's Brain to any MCP-capable client (Claude Desktop, Claude Code, etc.) over **17 carefully designed tools**. The article walks through what each tool does, grouped roughly into:

- **Read** — `get_index`, `get_node`, `get_summary`, `search_wiki`, `search_cross_domain`, `get_backlinks`, `get_connected_nodes`, `get_graph_overview`, `get_tags`, `list_domains`.
- **Maintain** — `scan_wiki_health`, `scan_semantic_duplicates`, `fix_wiki_issue`, `dismiss_wiki_issue`, `undismiss_wiki_issue`, `get_health_dismissed`.
- **Write** — `compile_to_wiki` (the privileged write tool that respects the Atomic Decomposition contract).

The MCP is not just a tool surface — it ships with a **Skill** (instruction manual) that teaches the model how to behave inside the graph: orient on the wiki via `list_domains` and `get_index` before composing any write, ground every wikilink in an existing slug, refuse speculative links on fresh domains, compound knowledge into existing pages instead of creating duplicates, and respect per-domain siloing. The Skill is what turns a blunt frontier model into a disciplined librarian.

The article includes three use cases — academic research synthesis, executive intelligence, and personal-pattern recognition — showing what "deep Second Brain research" actually looks like when the model can traverse the graph rather than retrieve chunks. It closes with installation instructions, privacy-track options (cloud frontier vs. local LLM), and best practices for getting the most out of the surface.

## Why this matters for ØØT

My Curator MCP is the **common protocol surface** every ØØT Skill Pack uses to read from and write to the Brain. It is what makes the Skill Packs composable across the cloud track (Claude Desktop / Claude Code) and the privacy track (local frontier or LM Studio). [`AGENTS.md`](../../AGENTS.md) documents how cross-vendor agents orient on the Brain via this same surface; [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md) places it in the cloud and privacy stacks. Anyone running ØØT for real should understand the 17-tool inventory before configuring an agent against the firm's Brain — this article is the canonical reference.

## Cross-references

- [`skills/my-curator/SKILL.md`](../../skills/my-curator/SKILL.md) — S1 imports The Curator's SKILL.md verbatim, including the MCP tool inventory and Skill behaviour.
- [`AGENTS.md`](../../AGENTS.md) — cross-vendor orientation; My Curator MCP is the common Brain interface across vendors.
- [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md) — where My Curator MCP sits in the cloud and privacy stacks.
- [`templates/brain/FIRM-ONTOLOGY.md`](../../templates/brain/FIRM-ONTOLOGY.md) — the Entity / Concept / Summary contract the MCP enforces.
- [`MANIFESTO.md`](../../MANIFESTO.md) — Theses 4 and 5.

## Read the full article

[github.com/talirezun/the-curator → research/articles/from-graph-to-intelligence-my-curator-mcp.md](https://github.com/talirezun/the-curator/blob/main/research/articles/from-graph-to-intelligence-my-curator-mcp.md)
