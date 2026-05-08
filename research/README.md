# Research

Research articles, paper summaries, and external-resource pointers relevant to the ØØT framework.

The framework's intellectual foundations rest on peer-reviewed research, industry reports, and practitioner case studies. This folder is the canonical index for those sources, plus the home for original research articles authored by the framework's contributors.

The structure mirrors the Curator project's `/research` folder convention so readers familiar with one can navigate the other.

---

## Structure

```
research/
├── README.md                  ← this file (the index)
├── articles/                  ← original framework articles by contributors
│   └── YYYY-MM-<slug>.md
├── papers/                    ← markdown summaries of cited external papers
│   └── <author>-<short-slug>-YYYY.md
└── external-resources.md      ← curated index of external tools, wikis, projects
```

---

## How to contribute

If you're an ØØT user, founder, or researcher with something to add:

1. **Original article** — drop a markdown file in `research/articles/` named `YYYY-MM-<slug>.md`. Include frontmatter:
   ```yaml
   ---
   title: <full title>
   author: <your name + affiliation>
   date: YYYY-MM-DD
   topic: <which thesis or skill pack the article touches — e.g. "Thesis 3 / S3 Compensation">
   peer_reviewed: <yes | no>
   external_url: <if previously published elsewhere>
   ---
   ```
2. **Paper summary** — if you've read a paper that should anchor a thesis, drop a markdown summary in `research/papers/` named `<lead-author>-<short-slug>-YYYY.md`. Include the citation, a 200-400 word summary, the relevant ØØT cross-reference (which thesis / Skill Pack / governance doc cites it), and a stable link to the source.
3. **External resource** — if a tool, wiki, or project belongs in the ecosystem index, edit `external-resources.md` and submit a PR.

All contributions follow the framework's licence split: original articles are CC BY-SA 4.0 unless the author specifies otherwise compatibly. Code snippets in articles are Apache 2.0.

---

## Articles index

(Populated as articles land. Initial entries are stubs that will be filled in by Phase 7.)

- [`2026-05-prompts-to-precision.md`](articles/2026-05-prompts-to-precision.md) — *(stub)* the framework's five-step prompt skeleton, by Dr. Tali Režun.
- [`2026-04-three-philosophies.md`](articles/2026-04-three-philosophies.md) — *(stub)* Augment Code, Claude Code, Codex CLI — when to use which, by Dr. Tali Režun.

---

## Paper summaries (anchoring the manifesto's theses)

(Populated by Phase 7 as part of the citation-integrity discipline.)

**Thesis 1 — Resistance:**
- [`mit-nanda-genai-divide-2025.md`](papers/mit-nanda-genai-divide-2025.md) — MIT NANDA, *The GenAI Divide* (August 2025).
- [`metr-rct-2025.md`](papers/metr-rct-2025.md) — METR, *RCT on AI tools and developer productivity* (July 2025).
- [`microsoft-frontier-firm-2025.md`](papers/microsoft-frontier-firm-2025.md) — Microsoft, *Work Trend Index 2025: The Frontier Firm*.
- [`klarna-2024-2026.md`](papers/klarna-2024-2026.md) — Klarna headcount trajectory and reversal, 2024–2026.

**Thesis 2 — Centaur work:**
- [`hbs-cybernetic-teammate-2025.md`](papers/hbs-cybernetic-teammate-2025.md) — Dell'Acqua et al., *The Cybernetic Teammate* (HBS WP 25-043, 2025).
- [`karpathy-software-3-2026.md`](papers/karpathy-software-3-2026.md) — Karpathy, *Software 3.0* (Sequoia AI Ascent 2026).
- [`dora-2025.md`](papers/dora-2025.md) — Forsgren et al., *DORA State of AI-Assisted Software Development* (2025).

**Thesis 3 — Partner compensation:**
- [`yolo-investments-output-pay-2026.md`](papers/yolo-investments-output-pay-2026.md) — *Stop paying for hours. Start paying for output* (May 2026). The seven-layer model.
- [`levin-tadelis-partnerships-2005.md`](papers/levin-tadelis-partnerships-2005.md) — Levin & Tadelis on partnership structures.
- [`rowe-2008.md`](papers/rowe-2008.md) — Ressler & Thompson on Results-Only Work Environment.
- [`weitzman-share-economy-1984.md`](papers/weitzman-share-economy-1984.md) — Weitzman, *The Share Economy*.

**Thesis 4 — The Brain:**
- [`nonaka-takeuchi-seci-1995.md`](papers/nonaka-takeuchi-seci-1995.md) — *The Knowledge-Creating Company*. The SECI model.
- [`microsoft-graphrag-2024.md`](papers/microsoft-graphrag-2024.md) — Edge et al., *GraphRAG* (2024).
- [`polanyi-tacit-1966.md`](papers/polanyi-tacit-1966.md) — Polanyi on tacit knowledge.

**Thesis 5 — Composable Lego:**
- *(thesis is more architectural than evidentiary; covered in `external-resources.md`)*

**Governance:**
- [`eu-ai-act-2024.md`](papers/eu-ai-act-2024.md) — Regulation (EU) 2024/1689.
- [`italian-law-132-2025.md`](papers/italian-law-132-2025.md) — Italian Law 132/2025.
- [`mica-2024.md`](papers/mica-2024.md) — EU MiCA stablecoin framework.
- [`genius-act-2025.md`](papers/genius-act-2025.md) — US GENIUS Act.

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
