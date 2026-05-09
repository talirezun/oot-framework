# References — Skill Pack S1 (My Curator)

The intellectual and technical foundations of the canonical Brain Skill Pack.

## Primary source

- **The Curator project.** Open-source desktop app + MyCuratorMCP server (17 tools). The canonical SKILL.md this pack imports verbatim.
  - Repository: https://github.com/talirezun/the-curator
  - Wiki + research: https://github.com/talirezun/the-curator/tree/main/research
  - Licence: open-source (see repo).

## Intellectual foundations

- **Karpathy, A.** *The second brain* (Twitter thread / blog, 2023). The original framing of the personal-knowledge-graph as a working artefact alongside an AI assistant.

- **Nonaka, I. & Takeuchi, H.** *The Knowledge-Creating Company* (Oxford University Press, 1995). The SECI model — Socialisation → Externalisation → Combination → Internalisation. The Brain operationalises the externalisation and combination phases at firm scale.

- **Polanyi, M.** *The Tacit Dimension* (Doubleday, 1966). The distinction between explicit and tacit knowledge that the framework's manifesto Thesis 4 cites as a caveat: not all tacit knowledge externalises cleanly, which is why the firm preserves synchronous rituals (the BR, the quarterly check-in) alongside the file-based Brain.

## Retrieval and graph architecture

- **Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Larson, J.** *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* (Microsoft Research, 2024). The GraphRAG pattern the Curator's hybrid retrieval is built on. Available at https://arxiv.org/abs/2404.16130.

- **Lewis, P. et al.** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS, 2020). The foundational RAG paper.

## Standards

- **Model Context Protocol (MCP).** Open standard for agent ↔ tool communication. Governed by the Linux Foundation Agentic AI Foundation as of December 2025.
  - Spec: https://modelcontextprotocol.io/
  - Servers index: https://github.com/modelcontextprotocol/servers

- **Anthropic Agent Skills (SKILL.md format).** The canonical skill format the framework adopts.
  - Documentation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview

## Cross-references inside ØØT

- ØØT [`MANIFESTO.md`](../../../MANIFESTO.md), Thesis 4 — The Collecting Brain.
- ØØT [`SPEC.md`](../../../SPEC.md), Layer 2 (Tech), T1 — The Curator + MyCuratorMCP.
- ØØT [`templates/brain/FIRM-ONTOLOGY.md`](../../../templates/brain/FIRM-ONTOLOGY.md) — the canonical `firm/` namespace this Skill Pack writes to.
- ØØT [`templates/brain/SPEC.md`](../../../templates/brain/SPEC.md) — the 14 Brain page templates this Skill Pack uses.
