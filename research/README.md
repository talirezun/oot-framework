# Research

Research articles, paper summaries, and external-resource pointers relevant to the ØØT framework.

The framework's intellectual foundations rest on peer-reviewed research, industry reports, and practitioner case studies. This folder is the canonical index for those sources, plus the home for original research articles authored by the framework's contributors.

The structure mirrors the Curator project's `/research` folder convention so readers familiar with one can navigate the other.

---

## Structure

```
research/
├── README.md                  ← this file (the index)
├── articles/                  ← original framework articles + external-article stubs
│   └── YYYY-MM-<slug>.md
├── papers/                    ← markdown summaries of cited external papers
│   └── <author>-<short-slug>-YYYY.md
└── external-resources.md      ← curated index of external tools, wikis, projects
```

---

## Library standards (please read before contributing)

This is a **library**, not a personal note dump. Consistency is the value — readers should be able to scan ten article cards and know exactly where to find the title, author, date, summary, and link to the source. Two things hold that consistency together: a shared **file template** and a shared **library taxonomy**.

### File naming

- **Articles** — `articles/YYYY-MM-<slug>.md`. The date is the **publication date** of the article (where it was first published), not the date you added the file to this repo.
- **Paper summaries** — `papers/<lead-author>-<short-slug>-YYYY.md` (e.g. `mit-nanda-genai-divide-2025.md`).

### Article taxonomy — pick one of two `type:` values

Every file in `articles/` is one of these two shapes:

1. **`type: external-article`** — the article was first published somewhere else (Medium, Substack, the Curator research series, a conference proceeding, etc.). The body of the file in this repo is a **stub** containing: a clearly visible author / date / source block, a 200–400 word summary, a "Why this matters for ØØT" paragraph, cross-references into the framework, and a link back to the full piece. Readers come here to decide whether to click through.
2. **`type: original-article`** — the article is **first-published in this repo** under the licence in `LICENSE-DOCS`. The body contains the full text, the same author / date block, and cross-references. No `external_url`.

The rule of thumb: *if the canonical version lives somewhere else, it is an external-article stub here. If the canonical version lives here, it is an original-article.*

### Required frontmatter

```yaml
---
title: "<full title, in quotes>"
author: "<your full name>"
author_affiliation: "<role + organisation>"
date: YYYY-MM-DD               # publication date (see above)
topic: "<which thesis or skill pack — e.g. Thesis 4 / S1 my-curator>"
peer_reviewed: <yes | no>
type: <external-article | original-article>
external_url: "<canonical URL>"   # required for external-article, omit for original-article
publication: "<where it was first published>"  # required for external-article
---
```

### Required body structure (both types)

The first three lines under the H1 must be the visible author block — frontmatter alone is not enough, because GitHub's markdown view does not render YAML to humans. Use this exactly:

```markdown
# <Title>

**By <Author Name>**
<Author affiliation>
Published: YYYY-MM-DD
Source: [<publication name>](<URL>)

> <one-sentence lede or pull-quote>

---

## Summary

<200–400 words. Reads cleanly on its own. No marketing voice; no spoilers of the full article's "punchline" beyond what makes someone want to read it.>

## Why this matters for ØØT

<one or two paragraphs connecting the article to specific Theses, Skill Packs, Routines, or governance docs.>

## Cross-references

- [`<path>`](<relative-path>) — <one-line note>.
- ...

## Read the full article  ← (external-article only; for original-article, skip this section)

[<short URL>](<URL>)
```

### Paper summary contributions

Drop a markdown summary in `papers/` named `<lead-author>-<short-slug>-YYYY.md`. Include the citation, a 200–400 word summary, the relevant ØØT cross-reference (which thesis / Skill Pack / governance doc cites it), and a stable link to the source.

### External resource contributions

If a tool, wiki, or project belongs in the ecosystem index, edit `external-resources.md` and submit a PR.

### Licence

All contributions follow the framework's licence split: original articles and paper summaries are CC BY-SA 4.0 unless the author specifies otherwise compatibly. External-article stubs reproduce only a short summary under fair use / fair dealing; the full work remains the author's. Code snippets in articles are Apache 2.0.

---

## Articles index

### External-article stubs (canonical version published elsewhere)

These are stubs in this repo; the full text lives at the source link in each file. Summaries here exist so readers can decide whether to click through.

**The Curator series — recommended pre-reading for new ØØT installers.** The Curator is the canonical Brain implementation that S1 imports; understanding how it works is a prerequisite to running the framework. The full series lives at the [Curator research section](https://github.com/talirezun/the-curator/tree/main/research/articles).

- [`2026-04-second-brain-grows-smarter.md`](articles/2026-04-second-brain-grows-smarter.md) — *The Second Brain That Grows Smarter and Lives on Your Computer*, by Dr. Tali Režun (2026-04-15). The compounding-knowledge model behind Thesis 4; Atomic Decomposition (Entity / Concept / Summary); the case against RAG.
- [`2026-04-knowledge-immortality.md`](articles/2026-04-knowledge-immortality.md) — *Building Knowledge Immortality Through the Second Brain Architecture and The Curator App*, by Dr. Tali Režun (2026-04-23). Why the Brain is plain markdown under git, not SaaS; durability across vendor failure and decades.
- [`2026-04-graph-to-intelligence-mcp.md`](articles/2026-04-graph-to-intelligence-mcp.md) — *From Graph to Intelligence: The My Curator MCP and the Art of Querying Your Second Brain*, by Dr. Tali Režun (2026-04-27). The 17-tool MCP surface that lets a frontier model traverse the Brain as a graph; the Skill that disciplines its writes.

**Founder series — by the framework's initiator.**

- [`2026-04-three-philosophies.md`](articles/2026-04-three-philosophies.md) — *Three Philosophies, One Goal: Augment Code, Claude Code, Codex CLI*, by Dr. Tali Režun (2026-04-15). The selection rubric anchoring Skill Pack S4 §4.4. *(Stub — full summary lands in v1.x.)*
- [`2026-05-prompts-to-precision.md`](articles/2026-05-prompts-to-precision.md) — *Prompts to Precision*, by Dr. Tali Režun (2026-05-08). The five-step prompt skeleton anchoring Skill Pack S2. *(Stub — full summary lands in v1.x.)*

### Original articles (first-published here)

*(Empty as of v1.0.0. Open a PR to contribute one — see "Library standards" above.)*

---

## Paper summaries (anchoring the manifesto's theses)

Three paper summaries shipped with v1.0.0; the rest are scheduled for v1.x per [`GENERATIONS.md`](../GENERATIONS.md). Stubs not yet authored are listed below as plain text (no link) so this index doesn't claim files that don't exist.

**Thesis 1 — Resistance:**
- [`mit-nanda-genai-divide-2025.md`](papers/mit-nanda-genai-divide-2025.md) — MIT NANDA, *The GenAI Divide* (August 2025).
- [`metr-rct-2025.md`](papers/metr-rct-2025.md) — METR, *RCT on AI tools and developer productivity* (July 2025).
- `microsoft-frontier-firm-2025.md` *(planned, v1.x)* — Microsoft, *Work Trend Index 2025: The Frontier Firm*.
- [`klarna-2024-2026.md`](papers/klarna-2024-2026.md) — Klarna headcount trajectory and reversal, 2024–2026.

**Thesis 2 — Centaur work:**
- `hbs-cybernetic-teammate-2025.md` *(planned, v1.x)* — Dell'Acqua et al., *The Cybernetic Teammate* (HBS WP 25-043, 2025).
- `karpathy-software-3-2026.md` *(planned, v1.x)* — Karpathy, *Software 3.0* (Sequoia AI Ascent 2026).
- `dora-2025.md` *(planned, v1.x)* — Forsgren et al., *DORA State of AI-Assisted Software Development* (2025).

**Thesis 3 — Partner compensation:**
- `yolo-investments-output-pay-2026.md` *(planned, v1.x)* — *Stop paying for hours. Start paying for output* (May 2026). The seven-layer model.
- `levin-tadelis-partnerships-2005.md` *(planned, v1.x)* — Levin & Tadelis on partnership structures.
- `rowe-2008.md` *(planned, v1.x)* — Ressler & Thompson on Results-Only Work Environment.
- `weitzman-share-economy-1984.md` *(planned, v1.x)* — Weitzman, *The Share Economy*.

**Thesis 4 — The Brain:**
- `nonaka-takeuchi-seci-1995.md` *(planned, v1.x)* — *The Knowledge-Creating Company*. The SECI model.
- `microsoft-graphrag-2024.md` *(planned, v1.x)* — Edge et al., *GraphRAG* (2024).
- `polanyi-tacit-1966.md` *(planned, v1.x)* — Polanyi on tacit knowledge.

**Thesis 5 — Composable Lego:**
- *(thesis is more architectural than evidentiary; covered in [`external-resources.md`](external-resources.md))*

**Governance:**
- `eu-ai-act-2024.md` *(planned, v1.x)* — Regulation (EU) 2024/1689.
- `italian-law-132-2025.md` *(planned, v1.x)* — Italian Law 132/2025.
- `mica-2024.md` *(planned, v1.x)* — EU MiCA stablecoin framework.
- `genius-act-2025.md` *(planned, v1.x)* — US GENIUS Act.

---

## External resources

See [`external-resources.md`](external-resources.md) for the curated index of:

- **Reference Brain** — the Curator project (open-source, MCP-native).
- **Privacy-track stack** — 4thtech, PollinationX, LM Studio, Excel MCP.
- **Cloud-track stack** — Anthropic Claude (Desktop, Code, Routines), Google Workspace, Slack.
- **Governance frameworks** — EU AI Act, GDPR, MiCA, GENIUS Act resources.
- **Standards bodies** — Linux Foundation Agentic AI Foundation, MCP working group.
- **Adjacent open-source frameworks** — for cross-pollination.

---

## A note on citation discipline

The framework's authors run the **Klarna Test** against their own evidence base: any number we cite without a verified source is a Klarna-Test-failing claim about evidence. Phase 0c of the build (citation integrity check) verified the foundation kit's citations. New papers added here go through the same discipline before they are referenced from MANIFESTO.md or any Skill Pack SPEC.

If you spot a stale citation, an inaccurate stat, or a dead link, open an issue or a PR. The framework prefers to update the citation than to leave a vague claim standing.
