---
name: governance-compliance
description: Use whenever the firm is mapping AI use cases to the EU AI Act, populating the eu-ai-act-mapping.xlsx, running the daily R6 audit trail Routine, conducting a quarterly compliance review, preparing for counsel review, or responding to a GDPR Article 22 escalation. Activates for "map this use case against Annex III", "is our R6 audit trail compliant?", "draft the Article 13 transparency notes for our supplier-trust scoring system", "respond to this data-subject GDPR access request".
version: 1.0.0
tier: 2
status: scaffold
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__github__create_or_update_file
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S7
oot_tier: 2
oot_status: scaffold
oot_dependencies: [S1, S2, S3, S6]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-15
---

# Governance & Compliance

> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x. Substantive content lands in v1.x; this file currently provides structure and TODOs.
> **Klarna Test interaction:** No (the pack supports the Klarna Test via Article 13 transparency mapping, but does not score).
> **Brain interaction:** Both — reads use-case register, writes audit-trail entries.

## 1. Purpose

Operationalises the EU AI Act mapping methodology (`governance/EU-AI-ACT.md`) and GDPR Article 22 patterns. Owns the `eu-ai-act-mapping.xlsx` (X7) and the daily audit trail Routine (R6). Coordinates with counsel on the eleven legal touchpoints from `docs/06-when-to-call-a-lawyer.md`.

This pack is **mandatory for EU-operating organisations** before 2 August 2026 (full high-risk obligations). Non-EU adopters should still follow the audit-log discipline as a hygiene practice.

## 2. When to invoke this pack

1. <!-- TODO: harden in v1.x — when a new AI use case is identified and needs Annex III risk mapping. -->
2. <!-- TODO: harden in v1.x — when R6 produces an audit-trail anomaly that needs investigation. -->
3. <!-- TODO: harden in v1.x — quarterly compliance review preparation. -->
4. <!-- TODO: harden in v1.x — counsel review preparation (annual or per-engagement). -->
5. <!-- TODO: harden in v1.x — GDPR Article 22 data-subject escalation response. -->
6. <!-- TODO: harden in v1.x — Italian Law 132/2025 compliance check (for orgs operating in Italy). -->

## 3. When NOT to invoke this pack

1. <!-- TODO: harden — for routine ledger entries that don't touch high-risk use cases. -->
2. <!-- TODO: harden — for non-AI-driven decisions (e.g., a purely human-judgement contract clause). -->

## 4. Operational instructions

<!-- TODO: harden in v1.x — full operational instructions per the canonical SKILL.md structure. The Tier-1 packs in v1.0 (S1–S6, S12) provide the template; this pack will follow the same structure. -->

### 4.1 Use-case classification (Annex III mapping)

<!-- TODO: harden — step-by-step procedure for classifying a use case against the EU AI Act's risk tiers. References the conservative-baseline tier table from `governance/EU-AI-ACT.md`. -->

### 4.2 Article 9 risk-management system

<!-- TODO: harden — populate X7 Risk Register; quarterly review; founder sign-off on residual risks. -->

### 4.3 Article 12 audit-trail (R6 invocation)

<!-- TODO: harden — daily 23:00 R6 audit log writes; signed commits; branch protection; retention. -->

### 4.4 Article 13 transparency

<!-- TODO: harden — every Skill Pack's "limitations" section is the Article 13 mechanism; pack ensures coverage per use case. -->

### 4.5 Article 14 human oversight

<!-- TODO: harden — every high-risk use case has a documented human-oversight mechanism; pack ensures coverage. -->

### 4.6 GDPR Article 22

<!-- TODO: harden — verify no Routine makes a final decision affecting partners/customers without human sign-off. -->

### 4.6.5 GDPR Article 17 — Right to Erasure (Firm Brain)

The Firm Brain (Curator Shared Brain, per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md)) ships a **first-class Article 17 mechanism**: the admin revoke endpoint with typed-confirmation safety gate. See [`governance/EU-AI-ACT.md`](../../governance/EU-AI-ACT.md) §"GDPR Article 17" for the runbook.

**S7 responsibilities for revocation:**
1. **Maintain the `admin_token`** (founders Bitwarden collection per [`governance/SECRETS-POLICY.md`](../../governance/SECRETS-POLICY.md)). Rotate annually and on suspected compromise.
2. **Verify the revoke audit log** quarterly: confirm `state/revocation-log.json` entries match the firm's records of contributor exits.
3. **Coordinate absolute erasure when required** (`git filter-repo` + force-push + backup purge for both the Firm Brain and the Ledger if the data subject's request goes beyond Curator's built-in revoke). This is counsel-coordinated; document the procedure outcome in `firm/compliance/erasure-requests/<request_id>.md` in the Ledger.
4. **For EU firms,** confirm Firm Brain storage residency: GitHub Enterprise Cloud EU option until Curator v3.1 ships Cloudflare R2 with `jurisdiction = "eu"`.

### 4.7 Italian Law 132/2025 (for orgs operating in Italy)

<!-- TODO: harden — Art. 612-quater mapping; aggravating-circumstances awareness; counsel coordination. -->

## 5. Brain interaction protocol

Per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), compliance evidence lives in the **Ledger** (signed-commit audit trail) and compliance *knowledge* (decision rationales, ADRs on compliance posture) lives in the **Firm Brain**.

**Reads (Ledger):** `firm/audit-logs/*`, `firm/klarna-tests/*` (operational evidence).

**Reads (Firm Brain — synthesized mirror or git clone):** `entities/decisions/*` (compliance-relevant decisions), `entities/architecture/*` (ADRs touching compliance — e.g., audit-trail anchoring).

**Writes (Ledger only):** `firm/audit-logs/<date>.md` (via R6); `firm/compliance/quarterly-reviews/<quarter>.md`; `firm/compliance/counsel-reviews/<date>.md`; `firm/compliance/erasure-requests/<request_id>.md` (Article 17 absolute-erasure records).

**No Firm Brain writes from S7.** Compliance ADRs and decision rationales are authored by the accountable partner in their personal Curator and pushed via Curator Shared Brain — that's an authorship flow, not an S7 Routine flow.

## 6. Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X7 eu-ai-act-mapping.xlsx | Use_Cases | Append per new use case | Manual |
| X7 | Annex_III_Risk_Mapping | Write | Manual + counsel review |
| X7 | Article_Obligations | Write | Per high-risk use case |
| X7 | Evidence_Trail | Append | Per evidence reference |
| X7 | Audit_Log_Index | Append | R6 daily |

## 7. Routine integration

- **R6** — owned by this pack.
- **R2** — contributes Klarna status block (mirrored from S5).

## 8. Don'ts (scaffold)

1. Don't treat compliance as a one-time exercise; it is continuous.
2. Don't bypass the daily R6 audit trail.
3. Don't claim EU AI Act compliance without counsel review.
4. <!-- TODO: harden — don't update the Risk Register without an audit trail of who updated and why. -->
5. <!-- TODO: harden — don't auto-publish Article 13 transparency notes externally without legal review. -->

## 9. Quick reference

<!-- TODO: harden — the standard 6-row Quick Reference table. -->

## 10. References

1. **Regulation (EU) 2024/1689** — the AI Act.
2. **GDPR** — General Data Protection Regulation, Article 22.
3. **Italian Law 132/2025** — first national EU AI law.
4. ØØT [`governance/EU-AI-ACT.md`](../../governance/EU-AI-ACT.md) — the mapping methodology.
5. ØØT [`templates/excel/SPEC.md`](../../templates/excel/SPEC.md) (X7) — the mapping spreadsheet.
6. ØØT [`routines/SPEC.md`](../../routines/SPEC.md) R6 — the audit trail.

## Acceptance criteria for v1.x hardening

- All `<!-- TODO -->` markers replaced with substantive content.
- Each §4.x section is operational (concrete steps with tool calls).
- 3+ worked examples in `examples/`.
- Frontmatter `status` flips from `scaffold` to `hardened`.
- All references include URLs where applicable.
