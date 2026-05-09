# References — Skill Pack S2 (Context Engineering)

The intellectual foundations for the framework's prompt-engineering discipline.

## Primary sources

1. **Schmid, P.** *Prompt Engineering Guide* (2023, ongoing). The taxonomy ØØT's five-step skeleton derives from. https://www.promptingguide.ai/

2. **Anthropic.** *Prompt Engineering documentation* — https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview. The canonical Anthropic guidance on system prompts, examples, chain-of-thought, and structured outputs.

3. **Karpathy, A.** *Software 3.0* (Sequoia AI Ascent 2026). The framing of the partner-as-context-engineer — humans contribute spec, taste, judgement; AI contributes implementation; the prompt is the spec. Talk summary at https://karpathy.bearblog.dev/sequoia-ascent-2026/

## Foundational research

4. **Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E. H., Le, Q. V., Zhou, D.** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (NeurIPS, 2022). https://arxiv.org/abs/2201.11903 — the foundational paper for the Self-Check step.

5. **Bai, Y. et al.** *Constitutional AI: Harmlessness from AI Feedback* (Anthropic, 2022). https://arxiv.org/abs/2212.08073 — the self-critique research that underpins the Self-Check rubric.

6. **Wang, X. et al.** *Self-Consistency Improves Chain of Thought Reasoning in Language Models* (ICLR, 2023). https://arxiv.org/abs/2203.11171 — the basis for the parallel-chain pattern's "decompose-and-merge" discipline.

## Practitioner literature

7. **Dr. Tali Režun.** *Prompts to Precision* (Medium, 2025). The original ØØT five-step formulation.

8. **Anthropic.** *Tool use overview and best practices* — https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview. Relevant for the chain orchestration pattern when MCP tools are in scope.

9. **OpenAI.** *Prompt engineering best practices* — https://platform.openai.com/docs/guides/prompt-engineering. Cross-vendor reference; the ØØT five-step is portable across both Anthropic and OpenAI APIs.

## Cross-references inside ØØT

- ØØT [`MANIFESTO.md`](../../../MANIFESTO.md), Thesis 5 — Composable Lego (prompts as composable artefacts).
- ØØT [`templates/brain/SPEC.md`](../../../templates/brain/SPEC.md) `prompt-artefact.md` — the canonical Brain page schema this pack writes to.
- ØØT [`templates/brain/FIRM-ONTOLOGY.md`](../../../templates/brain/FIRM-ONTOLOGY.md) — the `firm/prompts/` slug convention.
- ØØT Skill Pack S1 (My Curator) — the Brain substrate this pack depends on.
- ØØT Skill Pack S4 (Code & QA) — the Plan Mode workflow that uses this pack's chain pattern.
