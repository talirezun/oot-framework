---
name: legal-operations
description: Use whenever the firm is drafting or reviewing a contract (customer agreement, partner agreement, vendor agreement), running due diligence on a customer or partner, managing the Partner Charter template, preparing for a counsel engagement, or coordinating a Tier-3 dispute escalation per `governance/DECISION-RIGHTS.md`. Activates for "draft this customer MSA", "review this NDA before signing", "prepare due-diligence pack for new partner Mira", "handoff package for counsel review of the long-tail entitlement structure".
version: 1.0.0
tier: 2
status: scaffold
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__github__create_or_update_file
  - mcp__pdf-tools__extract_text
  - mcp__docx-tools__draft_document
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S8
oot_tier: 2
oot_status: scaffold
oot_dependencies: [S1, S2, S3, S7]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-08
---

# Legal Operations

> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.
> **Klarna Test interaction:** No.
> **Brain interaction:** Both — reads contracts, writes drafts and counsel-handoff packets to `legal/` domain.

## 1. Purpose

Harvey-style patterns for in-house legal work in an ØØT-native firm. Contract review, due diligence, partner agreement template management, dispute resolution coordination. **Designed to augment a counsel-engaged firm, not replace counsel.** The framework is unambiguous: every contract, every Tier-3 dispute, and every legal-touchpoint decision (per `docs/06-when-to-call-a-lawyer.md`) requires a qualified human lawyer.

## 2. When to invoke this pack

1. **TODO (v1.x):** drafting a customer MSA / SOW / NDA / DPA.
2. **TODO (v1.x):** reviewing a counterparty's draft before signature.
3. **TODO (v1.x):** preparing a due-diligence pack for a new partner.
4. **TODO (v1.x):** preparing a counsel-handoff packet for a complex matter.
5. **TODO (v1.x):** Tier-3 dispute escalation packet.
6. **TODO (v1.x):** Partner Charter template renegotiation.
7. **TODO (v1.x):** variable-pay-structure legal verification (Gen 1 FIAT; Gen 2 stablecoin upgrade).
8. **TODO (v1.x):** long-tail entitlement legal-wrapper preparation.

## 3. When NOT to invoke this pack

1. **For final legal advice.** The pack drafts and surfaces; counsel decides.
2. **For criminal-law matters** (any potential criminal exposure goes straight to counsel; the pack does not draft).
3. **For Italy-specific Law 132/2025 questions** without local Italian counsel co-engaged.
4. **For tax filings** — a tax-advisor engagement, not this pack.

## 4. Operational instructions

> **TODO (v1.x):** The pack's depth requires real engagement with the eleven legal touchpoints from `docs/06-when-to-call-a-lawyer.md`; v1.0 is a scaffold with structural placeholders.

### 4.1 Contract drafting workflow

> **TODO (v1.x):** Plan-Mode-style chain: (1) discovery (read prior similar contracts in `legal/contracts/*`); (2) draft per template; (3) counsel-handoff packet; (4) revisions; (5) signature; (6) commit to `legal/`.

### 4.2 Contract review (counterparty's draft)

> **TODO (v1.x):** read; flag risks per categorised list (data residency, IP assignment, liability cap, indemnity, termination); draft redline; counsel review.

### 4.3 Due-diligence pack for a new partner

> **TODO (v1.x):** identity verification; jurisdictional check; conflict-of-interest scan against firm's customer/competitor list.

### 4.4 Counsel-handoff packet

> **TODO (v1.x):** standardised structure: question, context, prior firm decisions, draft language, deadline.

### 4.5 Tier-3 dispute escalation

> **TODO (v1.x):** per `governance/DECISION-RIGHTS.md` Tier 3; counsel + founder; binding decision documented.

### 4.6 Partner Charter management

> **TODO (v1.x):** version-controlled template; renegotiation flow; per-partner customisations stored in `firm/partners/<id>/legal/`.

### 4.7 Variable-pay legal verification

> **TODO (v1.x):** jurisdictional verification of variable-pay structure compatibility; Gen 1 FIAT only; Gen 2 stablecoin requires re-verification per partner's jurisdiction.

### 4.8 Long-tail entitlement legal wrapper

> **TODO (v1.x):** securities-law analysis per jurisdiction; partnership-agreement provisions; Gen 1 = Excel-tracked + signed addendum; Gen 2 = on-chain smart contract requiring fresh counsel review.

## 5. Brain interaction protocol

**Reads:** `legal/*`, `firm/partners/<id>/legal/*`, `customers/*/contracts/*`.

**Writes:** `legal/contracts/<contract-id>.md`, `legal/counsel-handoffs/<date>-<topic>.md`, `firm/partners/<id>/legal/*` for partner-specific documents.

## 6. Excel interaction protocol

None directly. (X2 reward-species-declaration is owned by S3; this pack reviews the legal structure but does not modify the spreadsheet.)

## 7. Routine integration

None directly. The pack is invoked manually or via S3 / S6 cross-references.

## 8. Don'ts (scaffold)

1. **Don't replace counsel with Skills.** The pack augments; counsel decides.
2. **Don't auto-execute contract changes** without counsel review.
3. **Don't bypass the eleven legal touchpoints** from `docs/06-when-to-call-a-lawyer.md`.
4. **TODO (v1.x):** don't sign on the firm's behalf without explicit founder-level authorisation.
5. **TODO (v1.x):** don't redline a counterparty's draft without explicit principal direction (the partner authoring the redline is the named author, not the AI).

## 9. Quick reference

> **TODO (v1.x):** standard quick reference table.

## 10. References

1. **Harvey AI** — industry coverage 2024–2026 of AI-assisted legal practice.
2. ØØT [`docs/06-when-to-call-a-lawyer.md`](../../docs/06-when-to-call-a-lawyer.md) — the eleven legal touchpoints.
3. ØØT [`governance/DECISION-RIGHTS.md`](../../governance/DECISION-RIGHTS.md) — three-tier dispute resolution.
4. ØØT [`governance/EU-AI-ACT.md`](../../governance/EU-AI-ACT.md).
5. ØØT [`MANIFESTO.md`](../../MANIFESTO.md) "What ØØT is not" — the legal-not-legal-advice framing.

## Acceptance criteria for v1.x hardening

- All `<!-- TODO -->` markers replaced with substantive content.
- Counsel-handoff points explicit at each operational instruction.
- Contract templates referenced live in `legal/templates/` (separate from this Skill Pack).
- 3+ worked examples in `examples/`.
- Frontmatter `status` flips from `scaffold` to `hardened`.
