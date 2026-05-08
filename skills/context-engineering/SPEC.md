# Skill Pack S2 — Context Engineering: SPEC

**ID:** S2
**Name:** Context Engineering
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

The foundational meta-skill of ØØT. Every other Skill Pack assumes a partner who knows how to construct context for an AI agent — what to include, what to exclude, what shape a prompt should take, how to chain prompts into workflows, how to evaluate the output. Without this discipline, every other Skill Pack underperforms.

This pack codifies the ØØT discipline of context engineering: the practice of constructing, refining, and re-using prompts and prompt-chains as first-class artefacts of the firm's intellectual property.

## Scope

**Covers:**
- Prompt construction (the "Prompts to Precision" pattern, Schmid's prompt-engineering taxonomy adapted for ØØT).
- Prompt-chain orchestration (multi-step workflows, hand-off between agents).
- Context window management (what to include, when to summarise, when to off-load to the Brain).
- Skill invocation patterns (when to invoke which Skill Pack, in which order).
- Output evaluation (how to judge whether an AI's output is acceptable; explicit rubrics).
- Prompt versioning (treating prompts as versioned artefacts in the Brain).

**Does NOT cover:**
- Domain-specific prompt patterns (those live in the relevant Skill Pack — S4 for code, S8 for legal, etc.).
- Model-specific tuning (this is platform-side, not partner-side).
- Agent design (that is a developer concern; partners use agents, designers build them).

## Allowed tools / dependencies

- All MCP tools available in the partner's environment.
- No specific Curator tools required (this is a meta-skill).
- Optional: the Skill Pack uses `examples/` heavily.

## Section structure

The eventual `SKILL.md` follows the canonical template with these specific sections:

1. **Purpose**
2. **When to invoke** — when a partner is constructing a prompt, when a partner is failing to get a useful AI response, when a partner is building a prompt-chain.
3. **When NOT to invoke** — when a domain-specific Skill Pack already covers the use case (defer to that).
4. **Operational instructions:**
   - 4.1 The five-step prompt construction pattern (Goal, Context, Constraints, Format, Self-Check).
   - 4.2 Context window management (what stays, what summarises, what offloads).
   - 4.3 Prompt-chain orchestration (sequential, parallel, conditional patterns).
   - 4.4 Output evaluation rubrics.
   - 4.5 Prompt versioning in the Brain (every reusable prompt becomes a Brain page).
5. **Brain interaction protocol** — writes prompt artefacts to the `firm` domain under `prompts/` slug; reads existing prompts before constructing new ones.
6. **Excel interaction protocol** — none.
7. **Routine integration** — none directly; every other Routine implicitly uses this Skill Pack's patterns.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts (specific to this pack)

1. Don't construct prompts that ask the model to "do its best" without explicit Format and Constraints sections.
2. Don't paste large documents into context if the Brain has them indexed — query the Brain instead.
3. Don't skip the Self-Check step; it catches more errors than any other single discipline.
4. Don't reuse a prompt without versioning it in the Brain — prompts are intellectual property, treat them as such.
5. Don't confuse a prompt-chain failure with a model failure; debug the prompts first.

## Worked examples concept

**Example 1:** A partner needs to summarise a customer call. The pack walks them through the five-step construction: Goal (decision-quality summary, not transcript), Context (customer profile from Brain, prior interactions), Constraints (max 200 words, includes named action items with owners), Format (markdown with H2 headings), Self-Check ("Does this summary include every commitment made by either party?"). The resulting prompt is committed to the Brain as a versioned reusable artefact.

**Example 2:** A partner is failing to get the AI to refactor a complex codebase consistently. The pack diagnoses: too much context (the entire codebase pasted in), insufficient constraints (no architectural principles stated), no format spec (asking for "a refactor" instead of "a list of refactor steps with rationale"), no self-check. The pack walks them through reconstructing the prompt as a chain: discovery → plan → review → execute, each stage with its own constraints.

## References

1. Schmid, P. *Prompt Engineering Guide* (2023, ongoing).
2. Anthropic. *Prompt Engineering documentation* (`docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview`).
3. Karpathy, A. *Software 3.0* talk, Sequoia AI Ascent 2026 — context as code.
4. Wei, J. et al. *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (2022).
5. ØØT `MANIFESTO.md`, Thesis 5 — Composable Lego.
6. Dr. Tali Režun, *Prompts to Precision* (Medium, 2025).

## Acceptance criteria

Standard. Plus: at least 5 worked examples in `examples/` (this pack benefits from many examples — context engineering is learned by doing, not by reading definitions).