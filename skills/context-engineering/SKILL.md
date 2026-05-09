---
name: context-engineering
description: Use whenever the partner is constructing a re-usable prompt, debugging an unsatisfactory AI output, chaining multiple prompts into a workflow, or versioning an existing prompt artefact. Activates for "help me write a better prompt for X", "this AI output is bad — diagnose", "build me a prompt-chain for Y", "I want to reuse this prompt every Friday — how do I version it?". Enforces the five-step prompt skeleton (Goal / Context / Constraints / Format / Self-Check), the context-window decision tree (Brain wikilink first; paste only if ≤2k tokens; ingest first if larger), the three chain patterns (sequential / parallel / conditional), the three-tier output evaluation rubric (Quick / Quality / Adversarial), and the prompt-versioning convention (every reusable prompt becomes a versioned `firm/prompts/<slug>.md` Brain page).
version: 1.0.0
tier: 1
status: hardened
allowed_tools:
  - mcp__my-curator__list_domains
  - mcp__my-curator__get_index
  - mcp__my-curator__search_wiki
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__scan_wiki_health
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S2
oot_tier: 1
oot_status: hardened
oot_dependencies: [S1]
oot_provides_to: [S3, S4, S5, S6, S7, S8, S9, S10, S11, S12]
oot_klarna_test: false
last_updated: 2026-05-08
---

# Context Engineering

> **Generation marker:** This pack ships in v1.0 as **hardened**.
> **Klarna Test interaction:** No.
> **Brain interaction:** Both — reads `firm/prompts/*` before composing; writes versioned prompt artefacts there.

## 1. Purpose

The foundational meta-skill of ØØT. Every other Skill Pack assumes a partner who knows how to construct context for an AI agent — what to include, what to exclude, what shape a prompt should take, how to chain prompts into workflows, and how to evaluate the output. Without this discipline, every other Skill Pack underperforms and the framework's compounding-IP thesis (the Brain) breaks down because the prompts that *produced* the Brain pages are not themselves first-class artefacts.

Prompts are intellectual property. The prompt-versioning convention is the same convention as code. The Brain is the version-controlled substrate.

## 2. When to invoke this pack

1. When the partner is constructing **any prompt that will be re-used** (a one-off question to Claude does not need this skill; a prompt you'll run weekly does).
2. When **debugging an unsatisfactory AI output** — the diagnostic pass goes through the Output Evaluation rubric (§4.4) before any other reaction.
3. When **chaining multiple prompts** to produce a single artefact (e.g. research → outline → draft → review → publish).
4. When a domain-specific Skill Pack invocation is misfiring — this pack diagnoses *whether the input was the problem* before blaming the Skill.
5. When **versioning an existing prompt** that has drifted across uses.

## 3. When NOT to invoke this pack

1. When a domain Skill Pack already covers the case fully — e.g., monthly variable pay belongs to S3, not S2.
2. When the partner is **just chatting** with Claude exploratively (no artefact produced).
3. When the prompt is **truly single-use** and won't be re-run.
4. **Privacy-track local LLMs** that don't respect structured prompt skeletons — fall through to a simpler one-shot prompt and mark the Brain page `quality: experimental`.

## 4. Operational instructions

### 4.1 The five-step prompt construction pattern

Every prompt the partner intends to reuse follows this skeleton. The structure is non-negotiable; the content is filled per use case.

```markdown
## Goal
[One sentence, imperative voice. What the model must produce.]

## Context
[The minimum sufficient information. Reference Brain pages by wikilink rather than pasting. If pasting, no more than ~2,000 tokens of pasted material.]

## Constraints
[A bulleted list of hard rules. Length cap, tone, what to avoid, what must be cited.]

## Format
[Exact output shape. Markdown structure, frontmatter requirements, length, named sections.]

## Self-Check
[A bulleted list of pass/fail criteria the model applies to its own output before returning. The model is instructed to revise if any check fails.]
```

The skeleton template lives at `templates/brain/prompt-artefact.md`. Every prompt that survives more than one use is committed to `firm/prompts/<slug>.md` per §4.5.

### 4.2 Context window management — decision tree

For any input the partner is about to put in context:

1. **Is the source already in the Brain?**
   - **Yes** → reference by `[[wikilink]]`. Do not paste. The my-curator MCP fetches the page if needed.
   - **No** → continue to step 2.
2. **Is the source ≤2,000 tokens?**
   - **Yes** → paste in the Context section.
   - **No** → continue to step 3.
3. **Can the partner produce a faithful 2-paragraph summary?**
   - **Yes** → paste the summary; attach the source as a file reference; instruct the model: *"Use the summary; consult the source only if a contradiction arises."*
   - **No** → ingest the source into the Brain via S1 first, then return to step 1.

**Anti-patterns the pack refuses to support:**
- Pasting a 50-page contract into context when the Brain has it indexed.
- Pasting an entire codebase to ask "what does this do?" — use S4's Plan Mode instead.
- Pasting a long Slack thread when the Brain's thread-index already has the relevant decisions.

### 4.3 Prompt-chain orchestration

Three canonical patterns. Each commits its stages as separate prompt artefacts in `firm/prompts/<chain-name>/<stage>.md`.

**Sequential (the "researcher's chain"):**
```
[Source ingest] → [Outline] → [Draft] → [Review] → [Polish] → [Publish]
```
Each stage runs in a fresh Claude conversation (clean context window) to avoid stage contamination. Stage N's output is stage N+1's input.

**Parallel (the "decompose-and-merge"):**
A complex task decomposed into independent sub-tasks; each runs in its own conversation; outputs are merged in a final stage. Use cases: comparative analysis (5 vendors), multi-perspective drafting.

> ⚠️ Parallel chains require an explicit **merge specification** — what fields the sub-tasks must produce, in what schema. Without the merge spec, parallelism becomes chaos.

**Conditional (the "branch-on-output"):**
Stage A produces a classifier; subsequent stages branch on the classification. Use cases: customer-tier routing, legal-risk tiering. Each branch's onward prompt is its own artefact; do not embed branch logic in one mega-prompt.

### 4.4 Output evaluation rubrics

Before committing AI output to the Brain or shipping to a customer, evaluate against the appropriate tier.

**Tier 1 — Quick checklist (≤2 min, most internal artefacts):**
- Output matches requested Format exactly?
- Every Constraint satisfied?
- Self-Check the prompt requested actually performed?
- Every fact verifiable (cited, in Brain, or directly observable)?
- Any hallucinated wikilink? (Wikilinks must point to existing slugs.)

**Tier 2 — Quality rubric (10–15 min, customer-facing or compensation-affecting):**
- All of Tier 1.
- Internal consistency (no contradictions between sections).
- Tone matches the firm's voice — no marketing language slipped in.
- Edge cases addressed.
- Counterfactual robustness — would slightly different input meaningfully change the output in the right direction?

**Tier 3 — Adversarial review (30+ min, Klarna Test outputs, EU AI Act submissions, contracts):**
- All of Tier 2.
- A second partner reviews independently (per `governance/DECISION-RIGHTS.md` — non-beneficiary where applicable).
- A red-team prompt: *"Find three ways this output could be misinterpreted, gamed, or wrong in a way that would embarrass the firm in 2 years."*
- Red-team output committed alongside the artefact.

The chosen tier is recorded in the artefact's frontmatter (`evaluation_tier: 1|2|3`).

### 4.5 Prompt versioning in the Brain

Every reusable prompt is a versioned Brain page at `firm/prompts/<slug>.md`. Frontmatter follows `templates/brain/prompt-artefact.md`:

```yaml
---
title: "<human-readable title>"
slug: prompts/<slug>
domain: firm
type: prompt
prompt_id: <slug>
version: <semver — start 0.1.0; major when input/output schema changes; minor when constraints tighten; patch for clarifications>
intended_skill_pack: <S1..S12>
input_signature: "<one-line description of expected inputs>"
output_signature: "<one-line description of expected outputs>"
authors: [<partner_id>]
status: <experimental | active | deprecated>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body sections: Description / The prompt (fenced) / Inputs required / Output schema / Worked examples / Changelog.

A prompt used to produce **3 or more** Brain pages is `active`. A prompt unused for **90 days** drops to `deprecated` until renewed.

## 5. Brain interaction protocol

**Reads:**
- `firm/prompts/*` — query before constructing a new prompt.
- Any Brain page the prompt's Context section references.

**Writes:**
- `firm/prompts/<slug>.md` — every reusable prompt.
- The Brain pages the prompt-chain produces (e.g. customer summary at `customers/<slug>/summaries/<date>.md`).

**Domains:** primarily `firm`. References any domain in Context. Never writes to `partners/<id>/private/`.

## 6. Excel interaction protocol

None.

## 7. Routine integration

Not invoked by any Routine directly. Every Routine *implicitly* uses this pack's patterns — the prompts for R1, R2, R3, R5, R6, R7, R8 are themselves versioned prompt artefacts in `firm/prompts/`.

## 8. Don'ts

1. Don't construct prompts that ask the model to "do its best" without explicit Format and Constraints sections.
2. Don't paste large documents if the Brain has them indexed — query the Brain instead.
3. Don't skip the Self-Check step. It catches more errors than any other discipline.
4. Don't reuse a prompt without versioning it in the Brain — prompts are intellectual property.
5. Don't confuse a chain failure with a model failure. Debug the prompts first.
6. Don't merge prompt-chain stages to "save tokens" — stage contamination degrades chains.
7. Don't auto-publish Tier-1-evaluated outputs to external surfaces. Tier 2 minimum customer-visible; Tier 3 for legal/compensation-affecting.

## 9. Quick reference

| Situation | Action | Output lands at |
|---|---|---|
| Construct a re-usable prompt | Apply five-step skeleton; commit at v0.1.0 | `firm/prompts/<slug>.md` |
| Diagnose a bad AI output | Tier-1/2/3 rubric per artefact's risk | The artefact, with `evaluation_tier` updated |
| Chain prompts | Sequential / parallel / conditional; one artefact per stage | `firm/prompts/<chain>/<stage>.md` |
| Off-load context | Ingest via S1 first; reference by wikilink | A new Brain page in the appropriate domain |
| Update a prompt | Bump semver; append changelog entry; status → active | The same artefact |
| Deprecate an unused prompt | `status: deprecated`; deprecation note in body | The same artefact |

## 10. References

1. **Schmid, P.** *Prompt Engineering Guide* (2023, ongoing). The taxonomy the five-step skeleton derives from.
2. **Anthropic.** *Prompt Engineering documentation* — https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview.
3. **Karpathy, A.** *Software 3.0* (Sequoia AI Ascent 2026). The partner-as-context-engineer thesis.
4. **Wei, J. et al.** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (NeurIPS, 2022). Foundational for the Self-Check step.
5. **Dr. Tali Režun.** *Prompts to Precision* (Medium, 2025). The original ØØT five-step formulation.
6. **Anthropic.** *Constitutional AI* and self-critique research. Underpins the Self-Check rubric.
7. ØØT `MANIFESTO.md` Thesis 5 — Composable Lego.
