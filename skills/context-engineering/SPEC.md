# Skill Pack S2 — Context Engineering: SPEC

**ID:** S2
**Name:** Context Engineering
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

---

## Purpose

The foundational meta-skill of ØØT. Every other Skill Pack assumes a partner who knows how to **construct context for an AI agent** — what to include, what to exclude, what shape a prompt should take, how to chain prompts into workflows, and how to evaluate the output. Without this discipline, every other Skill Pack underperforms and the framework's compounding-IP thesis (the Brain) breaks down because the prompts that *produced* the Brain pages are not themselves first-class artefacts.

S2 codifies the ØØT discipline: prompts are intellectual property; the prompt-versioning convention is the same convention as code; the Brain is the version-controlled substrate.

This pack does not teach prompt engineering as a generic discipline. It teaches the **specific operational patterns** an ØØT-native partner uses every working day.

---

## Scope

**Covers:**
- The five-step prompt-construction pattern (Goal / Context / Constraints / Format / Self-Check) — the canonical ØØT prompt skeleton.
- Context-window management: when to include source material, when to summarise, when to off-load to the Brain.
- Skill-invocation patterns: which Skill Pack to invoke first, in what order, with what hand-offs.
- Prompt-chain orchestration (sequential, parallel, conditional patterns).
- Output evaluation rubrics (how to judge whether an AI's output is acceptable).
- Prompt versioning in the Brain (every reusable prompt becomes a versioned `firm/prompts/<slug>.md`).

**Does NOT cover:**
- Domain-specific prompt patterns (those live in the relevant Skill Pack — S3 for compensation prompts, S4 for code prompts, S8 for legal, S11 for sales).
- Model-specific tuning, temperature, sampling parameters (that is platform-side, not partner-side).
- Agent design (developer concern).

---

## Allowed tools / dependencies

- All MCP tools available in the partner's environment (no specific dependency).
- The Curator MCP (`my-curator`) for prompt-artefact reads/writes.
- No specific model dependency — the patterns work on Sonnet, Opus, Qwen 3 (privacy track), or Gemini.
- The pack uses `examples/` heavily; ships with 5 worked examples (more than any other Tier-1 pack).

---

## When to invoke

1. **When constructing any prompt that will be re-used.** A one-off question to Claude does not need S2; a prompt you'll run weekly does.
2. **When debugging an unsatisfactory AI output** — the diagnostic pass goes through S2's Output Evaluation rubric before any other reaction.
3. **When chaining multiple prompts** to produce a single artefact (e.g., research → outline → draft → review → publish).
4. **When a domain-specific Skill Pack invocation is misfiring** — S2 is the meta-skill that diagnoses *whether the input was the problem* before blaming the Skill.
5. **When versioning an existing prompt** that has drifted across uses.

---

## When NOT to invoke

1. When a **domain Skill Pack already covers the case fully** — e.g., monthly variable pay calculation belongs to S3, not S2.
2. When the partner is **just chatting** with Claude about an exploratory topic (no artefact produced).
3. When the prompt is **truly single-use** (a one-off translation, a quick lookup) and won't be re-run.
4. **For privacy-track local LLMs**, when the model does not respect the structured prompt skeleton (some smaller models ignore section headers); fall through to a simpler one-shot prompt and accept the lower quality. Mark the Brain page `quality: experimental` if so.

---

## Operational instructions

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

**Worked example — a partner constructing a customer-call summary prompt:**

```markdown
## Goal
Summarise the attached call transcript into a decision-quality memo for the founder, surfacing every commitment made by either party.

## Context
- Customer profile: [[customers/acme-corp]]
- Prior interaction history: [[customers/acme-corp/interactions]]
- The transcript is below in the user-message section.

## Constraints
- Maximum 250 words.
- Identify each speaker by role, not by name (Customer / Founder).
- Flag any statement that sounds like a verbal contract.
- Do not editorialise; the founder will form their own view.
- All commitments must include: who, what, by when.

## Format
Markdown.
- H2 "Decisions made" — bullet list, each commitment with owner + deadline.
- H2 "Open questions" — bullet list.
- H2 "Customer signals" — three bullets max, surface only meaningful affect or strategic signals.
- Frontmatter: type=customer-summary, customer_slug=acme-corp, call_date=YYYY-MM-DD.

## Self-Check
- Does the output include every commitment made by either party? If unsure, revise.
- Is each commitment ascribed to a specific owner with a specific date?
- Is the word count under 250?
- Is there any editorial language ("the customer was clearly excited...")? If yes, remove.
- Did I respect the "do not name the speakers" rule?
If any check fails, revise once before returning.
```

The five-step skeleton lives at `templates/brain/prompt-artefact.md` as a fillable template. Every prompt that survives more than one use is committed to `firm/prompts/<slug>.md` with semver in the frontmatter (see §4.5).

### 4.2 Context window management

The Curator's Brain is the partner's working *memory*. The partner's chat with Claude is the partner's working *attention*. The discipline is to keep attention focused.

**Decision tree for any input:**

1. Is the source already in the Brain?
   - **Yes** → reference by `[[wikilink]]`, do not paste. Claude (with the my-curator MCP) will fetch the page if needed.
   - **No** → continue to step 2.
2. Is the source ≤2,000 tokens?
   - **Yes** → paste in the Context section.
   - **No** → continue to step 3.
3. Can the partner produce a 2-paragraph summary that's faithful to the source?
   - **Yes** → paste the summary, attach the source as a file reference, instruct the model: *"Use the summary; consult the source only if a contradiction arises."*
   - **No** → ingest the source into the Brain first (using S1 my-curator), then return to step 1.

**Anti-patterns the pack flags and refuses to support:**
- Pasting a 50-page contract into context when the Brain has it indexed.
- Pasting an entire codebase to ask "what does this do?"; instead, use S4's repo-orientation pattern (CLAUDE.md / AGENTS.md, then Plan Mode).
- Pasting a long Slack thread when the Brain's thread-index already has the relevant decisions.

### 4.3 Prompt-chain orchestration patterns

Three canonical patterns. Each has a Brain template and worked examples.

**Sequential (the "researcher's chain"):**

```
[Source ingest] → [Outline] → [Draft] → [Review] → [Polish] → [Publish]
```

Each stage's prompt is its own artefact in `firm/prompts/`. The outputs of stage N are the inputs to stage N+1. The partner runs each stage in a fresh Claude conversation (clean context window) to avoid stage contamination. The Brain page `firm/prompts/researchers-chain.md` provides the chain definition.

**Parallel (the "decompose-and-merge"):**

A complex task is decomposed into independent sub-tasks; each runs in its own conversation; outputs are merged in a final stage. Useful for: comparative analysis (5 vendors, one prompt per vendor, then merge), multi-perspective drafting (founder view, partner view, customer view, then synthesise).

The pack's discipline: parallel chains require an explicit **merge specification** — what fields the sub-tasks must produce, in what schema, so the merge is mechanical. Without the merge spec, parallelism becomes chaos.

**Conditional (the "branch-on-output"):**

Stage A produces a classifier output. Subsequent stages branch on the classification. Used in: customer-tier-routing (premium vs. standard handling), legal-risk-tiering (counsel-required vs. proceed). The pack's discipline: every branch's onward prompt is its own artefact; do not embed branch logic inside one mega-prompt.

### 4.4 Output evaluation rubrics

The partner evaluates AI output against an explicit rubric **before** committing to the Brain or shipping to a customer. The pack provides three tiers of rubric depth.

**Tier 1 — Quick checklist (≤2 minutes, applied to most internal artefacts):**

- Does the output match the requested Format exactly?
- Does it satisfy every Constraint?
- Did it pass the Self-Check the prompt requested?
- Is every fact verifiable (cited, in the Brain, or directly observable)?
- Is there any hallucinated wikilink? (Wikilinks must point to existing slugs.)

**Tier 2 — Quality rubric (10–15 minutes, applied to customer-facing or compensation-affecting artefacts):**

- All of Tier 1.
- Internal consistency (no contradictions between sections).
- Tone matches the firm's voice — no marketing language slipped in.
- Edge cases addressed (the most important customer profile, the regulatory worst-case, the dispute scenario).
- Counterfactual robustness — if the underlying input had been slightly different, would the output meaningfully change in the right direction?

**Tier 3 — Adversarial review (30+ minutes, applied to Klarna Test outputs, EU AI Act submissions, contracts):**

- All of Tier 2.
- A second partner reviews independently (per `governance/DECISION-RIGHTS.md` — non-beneficiary reviewer where applicable).
- A red-team prompt is run against the output: *"Find three ways this output could be misinterpreted, gamed, or wrong in a way that would embarrass the firm in 2 years."*
- The red-team output is itself committed to the Brain alongside the artefact.

The rubric chosen for an artefact is recorded in the artefact's frontmatter (`evaluation_tier: 1|2|3`).

### 4.5 Prompt versioning in the Brain

Every prompt that survives more than one use is a versioned Brain page at `firm/prompts/<slug>.md`. Frontmatter follows `templates/brain/prompt-artefact.md`:

```yaml
---
title: "<human-readable title>"
slug: prompts/<slug>
domain: firm
type: prompt
prompt_id: <slug>
version: <semver — start at 0.1.0; bump major when input/output schema changes; minor when constraints tighten; patch for clarifications>
intended_skill_pack: <S1..S12>
input_signature: "<one-line description of expected inputs>"
output_signature: "<one-line description of expected outputs>"
authors: [<partner_id>]
status: <experimental | active | deprecated>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body sections:

1. **Description** — one paragraph: what this prompt does, when to use it.
2. **The prompt** — fenced markdown block, exact text, the five-step skeleton populated.
3. **Inputs required** — what the partner provides at runtime.
4. **Output schema** — the exact shape the prompt produces.
5. **Worked examples** — at least one input/output pair.
6. **Changelog** — versioned changes, oldest first.

A prompt that has been used to produce three or more Brain pages is **active**. A prompt that has not been invoked in 90 days drops to **deprecated** until renewed.

---

## Brain interaction protocol

**Reads:**
- `firm/prompts/*` — query before constructing a new prompt; the discipline is to look for an existing artefact first.
- Any Brain page the prompt's Context section references.

**Writes:**
- `firm/prompts/<slug>.md` — every reusable prompt.
- The Brain pages produced by the prompt-chain (e.g., a customer summary lands at `customers/<slug>/summaries/<date>.md`).

**Domains:** primarily `firm`. May reference any domain in the prompt's Context. Never writes to `partners/<id>/private/`.

---

## Excel interaction protocol

None.

---

## Routine integration

S2 is **not invoked by any Routine directly**. Every Routine implicitly uses S2's patterns — R1's daily-output-capture prompt is itself a Brain-versioned prompt artefact (`firm/prompts/r1-daily-output-capture.md`), as are the prompts for R2, R3, R5, R6, R7, R8.

When a Routine prompt is updated, the bump is recorded in the prompt artefact's changelog and the Routine version in `firm/routines/changelog.md`.

---

## Don'ts

1. **Don't construct prompts** that ask the model to "do its best" without explicit Format and Constraints sections.
2. **Don't paste large documents** into context if the Brain has them indexed — query the Brain instead.
3. **Don't skip the Self-Check step.** It catches more errors than any other single discipline; every benchmark in the pack's `examples/` folder shows a measurable quality lift from this one step alone.
4. **Don't reuse a prompt without versioning it** in the Brain — prompts are intellectual property; treat them as such.
5. **Don't confuse a prompt-chain failure with a model failure**; debug the prompts first. The pack's troubleshooting doc has a structured diagnostic.
6. **Don't merge prompt-chain stages** to "save tokens" — stage contamination is the most common cause of degraded chain output.
7. **Don't auto-publish** outputs evaluated only at Tier 1 to external surfaces. Tier 2 minimum for anything customer-visible; Tier 3 for anything legal- or compensation-affecting.

---

## Quick reference

| Situation | Action | Output lands at |
|---|---|---|
| Construct a re-usable prompt | Apply the five-step skeleton; commit to `firm/prompts/<slug>.md` v0.1.0 | `firm/prompts/` |
| Diagnose a bad AI output | Run the Tier-1 / Tier-2 / Tier-3 rubric appropriate to the artefact's risk | The Brain page itself, with `evaluation_tier` updated |
| Chain prompts | Pick sequential / parallel / conditional; commit each stage as its own prompt artefact | `firm/prompts/<chain-name>/<stage>.md` |
| Off-load context | Ingest the source via S1 my-curator first; reference by wikilink | A new Brain page in the appropriate domain |
| Update an existing prompt | Bump semver per the rules; append changelog entry; status returns to `active` | The same prompt artefact |
| Deprecate an unused prompt | Set `status: deprecated`; add deprecation note in body | The same prompt artefact |

---

## Worked examples concept

The pack's `examples/` folder ships with **five worked examples** (the most of any Tier-1 pack — context engineering is learned by doing, not by reading definitions):

1. **Customer-call summary prompt** (the example shown above in §4.1, with the actual input transcript and the produced output).
2. **A debugging case study** — a partner is failing to get the AI to refactor a complex codebase consistently. The pack walks through the diagnostic: too much context (the entire codebase pasted in), insufficient constraints (no architectural principles stated), no format spec (asking for "a refactor" instead of "a list of refactor steps with rationale"), no self-check. The reconstructed prompt-chain (discovery → plan → review → execute) and its outputs are shown.
3. **A parallel-chain example** — comparing five SaaS vendors. The decompose-and-merge specification is shown, the per-vendor sub-prompts are shown, the merge prompt is shown, the final comparison memo is shown.
4. **A conditional-chain example** — customer-tier routing for a 30-customer pipeline. The classifier prompt + each branch's onward prompt are shown.
5. **A versioning case study** — a prompt that started at v0.1.0, evolved through five versions, was used to produce 47 Brain pages, and is now at v1.2.3. The full changelog is shown to demonstrate what real prompt evolution looks like.

---

## References

1. Schmid, P. *Prompt Engineering Guide* (2023, ongoing). The taxonomy ØØT's five-step skeleton derives from.
2. Anthropic. *Prompt Engineering documentation* — `https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview`.
3. Karpathy, A. *Software 3.0* (Sequoia AI Ascent 2026). The framing of context as code; the partner-as-context-engineer thesis.
4. Wei, J. et al. *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (NeurIPS, 2022). Foundational for the Self-Check step.
5. Dr. Tali Režun. *Prompts to Precision* (Medium, 2025). The original ØØT five-step formulation.
6. Anthropic. *Constitutional AI* and self-critique research. Underpins the Self-Check rubric.
7. ØØT `MANIFESTO.md` Thesis 5 — Composable Lego (prompts as composable artefacts).

---

## Acceptance criteria for the eventual SKILL.md

Standard structure (all sections 1–10 from `_TEMPLATE_SKILL.md`). Plus:

- The five-step skeleton is reproduced verbatim in §4.1, with at least one populated worked example inline.
- The context-management decision tree is shown as both prose and as an inline flowchart.
- Each chain pattern (sequential / parallel / conditional) has at least one named example.
- The output-evaluation rubric is reproduced in full (all three tiers).
- The prompt-versioning frontmatter schema is reproduced verbatim.
- All 5 worked examples land in `examples/` as separate markdown files.
- All 7 references resolve (URLs check; books cited correctly).
- Frontmatter passes the Phase 8 linter.
