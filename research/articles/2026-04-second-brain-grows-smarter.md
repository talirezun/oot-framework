---
title: "The Second Brain That Grows Smarter and Lives on Your Computer"
author: "Dr. Tali Režun"
author_affiliation: "Vice Dean of Frontier Technologies, COTRUGLI Business School"
date: 2026-04-15
topic: "Thesis 4 (the Brain) / S1 my-curator"
peer_reviewed: no
type: external-article
external_url: "https://github.com/talirezun/the-curator/blob/main/research/articles/the-second-brain-that-grows-smarter.md"
publication: "The Curator Research Series"
---

# The Second Brain That Grows Smarter and Lives on Your Computer

**By Dr. Tali Režun**
Vice Dean of Frontier Technologies, COTRUGLI Business School
Published: 2026-04-15
Source: [The Curator Research Series — `the-second-brain-that-grows-smarter.md`](https://github.com/talirezun/the-curator/blob/main/research/articles/the-second-brain-that-grows-smarter.md)

> How a spark from Andrej Karpathy, a free note-taking app called Obsidian, and a locally-hosted tool called The Curator are changing how we think — permanently.

---

## Summary

The article opens with a problem most knowledge workers feel but rarely name: we read voraciously, but the connections between what we read almost never form. Information piles up; synthesis does not. The brain was built to think, not to file.

The piece traces an alternative pattern that originated with **Andrej Karpathy's "LLM Wiki" gist** — instead of using AI to *retrieve* from documents on demand (RAG), use AI to *continuously compile* a personal markdown wiki where every new source is read, decomposed, and integrated into pages that already exist. Knowledge gets compiled once and kept current, rather than re-discovered from scratch each query. The argument against RAG is concrete: chunking and vector retrieval lose the cross-document connections that *are* the value of a knowledge base.

The article then sets out the architecture of the Second Brain in plain markdown:

- **Entities** — the nouns (people, companies, tools, datasets).
- **Concepts** — the ideas (frameworks, techniques, theories).
- **Summaries** — the narratives (one per ingested source, tying Entities and Concepts together).

Pages link to each other with `[[wikilinks]]`, viewable in **Obsidian**'s graph view as a living constellation of your reading life. Adding a new source does not just append a page — it enriches every related page that already exists. The graph reveals patterns in your own thinking that no search bar can.

Manual curation at this scale is impractical. The article introduces **The Curator** — an open-source, local-first desktop app that automates the decomposition and cross-referencing. Drop in a PDF, markdown, or text file; the AI reads it, writes/updates Entity, Concept, and Summary pages, and adds the links. The app is organised into six sections: Domains, Ingest, Chat, Wiki, Sync, Settings.

The piece closes on **knowledge ownership**: plain markdown files on your hard drive cannot be deplatformed, deprecated, or trained on without your consent. A Second Brain built this way is yours — completely, permanently, and technically — and it compounds for years rather than depreciating like a SaaS subscription.

## Why this matters for ØØT

ØØT's Brain (Thesis 4) is built directly on this architecture. Skill Pack **S1 my-curator** imports The Curator's `SKILL.md` verbatim and treats Entity / Concept / Summary as the canonical Brain ontology — see [`templates/brain/FIRM-ONTOLOGY.md`](../../templates/brain/FIRM-ONTOLOGY.md). The compounding-knowledge model in this article is the prerequisite mental model for understanding why every other Skill Pack writes to the Brain rather than to a vendor wiki. Anyone installing ØØT should read this before standing up their firm's Brain.

## Cross-references

- [`skills/my-curator/SKILL.md`](../../skills/my-curator/SKILL.md) — S1 imports The Curator's SKILL.md verbatim.
- [`templates/brain/FIRM-ONTOLOGY.md`](../../templates/brain/FIRM-ONTOLOGY.md) — Entity / Concept / Summary ontology applied to a firm.
- [`templates/brain/SPEC.md`](../../templates/brain/SPEC.md) — Brain page contract (markdown + YAML frontmatter).
- [`MANIFESTO.md`](../../MANIFESTO.md) — Thesis 4 ("the Brain is the substrate").
- [`research/external-resources.md`](../external-resources.md) §"The Curator" — repo, Skill Pack, and ecosystem pointers.

## Read the full article

[github.com/talirezun/the-curator → research/articles/the-second-brain-that-grows-smarter.md](https://github.com/talirezun/the-curator/blob/main/research/articles/the-second-brain-that-grows-smarter.md)
