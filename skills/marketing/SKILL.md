---
name: marketing
description: Use whenever the firm is generating marketing content (emails, social posts, landing pages, blog articles), running a content pipeline (technical source → outline → draft → review → publish), integrating the Lumina AI widget for inbound capture, or managing brand voice. Activates for "draft this newsletter", "turn this engineering blog into a customer-facing post", "review the Lumina widget responses for last week's new leads", "we need a launch sequence for the new feature".
version: 1.0.0
tier: 2
status: scaffold
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__search_wiki
  - mcp__my-curator__search_cross_domain
  - mcp__lumina__list_conversations
  - mcp__lumina__qualify_lead
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S9
oot_tier: 2
oot_status: scaffold
oot_dependencies: [S1, S2, S3, S6, S11]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-08
---

# Marketing

> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.
> **Klarna Test interaction:** No directly (a marketing-pack rollout that displaces a content partner's primary function is a Klarna trigger via S6).
> **Brain interaction:** Both — reads research, customer signals, prior content; writes content drafts and brand-voice notes.

## 1. Purpose

The AI marketing team workflow — content generation from technical sources to publishable formats, with the **Lumina-as-front-door** pattern for external-facing surfaces. This pack is what the marketing pilot in S6 example 02 ran (and abandoned for full rollout); the pack still exists for the narrow use cases where AI marketing produces real value (internal newsletters, routine status emails) and serves as a starting point for firms whose marketing function is differently-shaped.

## 2. When to invoke this pack

1. **TODO (v1.x):** drafting a customer-facing email / newsletter / social post.
2. **TODO (v1.x):** running the content pipeline (technical-source → outline → draft → review → publish).
3. **TODO (v1.x):** Lumina widget conversation review (qualifying leads, escalating to sales).
4. **TODO (v1.x):** brand-voice management (the firm's voice document; voice-tuning prompts).
5. **TODO (v1.x):** publishing automation (with mandatory human editorial sign-off).

## 3. When NOT to invoke this pack

1. **Without human editorial sign-off** for any externally-published content.
2. **For customer-facing content** when the engagement-rate baseline shows AI drafts underperform (per S6 marketing example).
3. **For sales follow-up** — that's S11.
4. **For legal-sensitive content** (terms of service, privacy policy updates) — that's S8 + counsel.

## 4. Operational instructions

> **TODO (v1.x):**

### 4.1 Content pipeline (technical source → publishable)

> **TODO (v1.x):** sequential chain pattern (per S2): ingest source → extract key points → outline → draft → human review → polish → publish. Each stage as its own prompt artefact in `firm/prompts/marketing/`.

### 4.2 Lumina widget integration

> **TODO (v1.x):** Lumina is the firm's front-door RAG chatbot for inbound. The pack manages: knowledge-base sync from Brain → Lumina; conversation review (R8-style weekly review of conversations); lead qualification; escalation to S11.

### 4.3 Brand voice management

> **TODO (v1.x):** the firm's voice document at `firm/marketing/brand-voice.md`. Voice-tuning prompts at `firm/prompts/marketing/voice-tuning.md`. Every drafted piece passes through the voice-tuning pass.

### 4.4 Memes-to-technical-content workflow

> **TODO (v1.x):** the framework's authors' practice (per Dr. Tali Režun's *How I Built an AI Marketing Team* article): start with a meme/visual idea, expand to technical depth via the Brain, polish to the firm's voice.

### 4.5 Publishing automation

> **TODO (v1.x):** every externally-published piece passes through human editorial sign-off (frontmatter `editorial_signoff: <partner_id>`). Auto-publishing is **not allowed** in Gen 1.

### 4.6 Content performance review

> **TODO (v1.x):** weekly review of email open rates, social engagement, landing conversion; surface to BR's KPI block via S5.

## 5. Brain interaction protocol

**Reads:** `firm/architecture/*`, `firm/products/*`, `customers/*/profile.md`, `research/*` (for technical-source ingest).

**Writes:** `firm/marketing/brand-voice.md`, `firm/marketing/published/<date>-<slug>.md`, `firm/marketing/drafts/<date>-<slug>.md`.

## 6. Excel interaction protocol

None directly.

## 7. Routine integration

None directly. The pack contributes to S5's KPI block (content performance metrics).

## 8. Don'ts (scaffold)

1. **Don't publish AI-generated content without human editorial sign-off.**
2. **Don't claim AI authorship as human authorship.** Bylines reflect the principal partner; AI assistance is `Co-authored-by:` in the commit, not the byline.
3. **Don't bypass the brand voice guidelines.**
4. **TODO (v1.x):** don't auto-respond on social media without the partner's explicit per-post sign-off.
5. **TODO (v1.x):** don't forward Lumina widget conversations to sales without consent (the conversation may have privacy implications).

## 9. Quick reference

> **TODO (v1.x):**

## 10. References

1. **Dr. Tali Režun.** *How I Built an AI Marketing Team That Actually Works* (Medium, 2026).
2. **Microsoft.** *Work Trend Index 2025: The Frontier Firm* — 73% Frontier-firm AI marketing adoption.
3. ØØT Skill Pack S11 — Sales & BD (Lumina widget shared dependency).
4. ØØT [`research/external-resources.md`](../../research/external-resources.md) — Lumina AI references.

## Acceptance criteria for v1.x hardening

- All `<!-- TODO -->` markers replaced.
- Lumina widget integration points explicit (read knowledge-base sync flow + conversation-review flow).
- Brand voice document template lives at `firm/marketing/brand-voice.md` and the pack provides the authoring guide.
- 3+ worked examples in `examples/`.
- Frontmatter `status` → `hardened`.
