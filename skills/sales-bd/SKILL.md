---
name: sales-bd
description: Use whenever the firm is constructing a sales pipeline from Brain signals, drafting outreach (cold/warm), reviewing or qualifying Lumina widget conversations, recording closed-deal Brain pages, or settling long-tail attribution for sales work. Activates for "build pipeline from this customer-mention search", "draft a cold email to Acme's new CTO", "qualify these Lumina leads from last week", "record the closed deal with Acme MSA", "compute Davor's long-tail share on the Acme contract".
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
  - mcp__email__send
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S11
oot_tier: 2
oot_status: scaffold
oot_dependencies: [S1, S2, S3, S9]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-08
---

# Sales & BD

> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.
> **Klarna Test interaction:** No directly.
> **Brain interaction:** Both — reads customer signals from Brain; writes pipeline pages, deal records, contract Brain pages.

## 1. Purpose

Brain-fed pipeline that writes itself. Outreach skill patterns. **Lumina widget as the front door for inbound.** Sales output is **first-class output** in the partner output ledger — no demoting commercial work to second-class status. The framework's discipline: a closed deal is an `output_type: deal_closed` row in X1, value-tier-rated like any other output.

## 2. When to invoke this pack

1. <!-- TODO: harden — building pipeline from Brain signals (customer mentions in research, contract events, conversation threads, Lumina inbound). -->
2. <!-- TODO: harden — drafting cold outreach (every prompt versioned in `firm/prompts/sales/`). -->
3. <!-- TODO: harden — drafting warm follow-up (post-Lumina or post-customer-meeting). -->
4. <!-- TODO: harden — reviewing Lumina widget conversations weekly and qualifying leads. -->
5. <!-- TODO: harden — recording a closed deal as a `customers/<slug>/contracts/<contract-id>.md` Brain page. -->
6. <!-- TODO: harden — long-tail attribution for sales (per YOLO model — sales output deserves the same compounding entitlement as engineering). -->

## 3. When NOT to invoke this pack

1. **For automated outreach without partner sign-off.** Every cold email/dMail sent on the firm's behalf is principal-authored; the AI assists; the partner is the named sender.
2. **For lead-qualification automation that bypasses the Lumina widget's qualification step.** That step is the framework's escape valve for "this is not a real lead".
3. **For account management of existing customers** — that's the relevant cross-functional pack (depends on the customer relationship's nature; often product partners + S5 BR cadence).
4. **For internal sales-team metrics that aren't real outputs** — the framework does not credit "calls made" or "emails sent"; only `deal_closed` and explicit milestone outputs land in X1.

## 4. Operational instructions

<!-- TODO: harden in v1.x. -->

### 4.1 Pipeline construction from Brain signals

<!-- TODO: harden — query patterns: customer mentions in `research/*`; contract-renewal-due-soon in `customers/*/contracts/*`; Lumina inbound conversations not yet contacted. Output: a `firm/sales/pipeline-<YYYY-MM-DD>.md` Brain page with prioritised contacts. -->

### 4.2 Outreach drafting (cold + warm)

<!-- TODO: harden — every outreach prompt is a versioned artefact in `firm/prompts/sales/<pattern>.md` per S2. Five-step skeleton enforced. Partner reviews + edits before sending; partner is the named sender. -->

### 4.3 Lumina widget integration

<!-- TODO: harden — Lumina is the inbound front door. The pack: (a) syncs the Brain's customer-facing knowledge to Lumina weekly; (b) reviews Lumina conversations every Monday morning; (c) qualifies leads per criteria (BANT — Budget, Authority, Need, Timeline — adapted); (d) escalates qualified leads to the partner-on-pipeline; (e) records dismissed leads with reason for the labeller's improvement. -->

### 4.4 Closed-deal Brain page

<!-- TODO: harden — per `templates/brain/SPEC.md` (no specific deal-record template yet; Phase 4 freeform with required frontmatter: deal_id, customer_slug, value, partner_attribution, contract_link, deal_close_date, long_tail_eligible). The page is the canonical record; X1 row references it. -->

### 4.5 Long-tail attribution for sales

<!-- TODO: harden — per S3 §4.5; sales output is long-tail-eligible; the partner who closed the deal gets a partner_share_pct of the realised revenue. The framework's discipline: sales-driven long-tail is settled quarterly per R4, just like engineering long-tail. The percentage is set at deal-close time per the partner's reward-species declaration; cannot be retroactively reduced. -->

### 4.6 Sales output capture (R1 sub-flow)

<!-- TODO: harden — R1 captures `output_type: contract_signed` and `output_type: deal_closed` from: GitHub PR labels (`contract:<customer>`); calendar events (`Deal closed: <customer>`); explicit `#sales-deal-closed` Slack/dChat tags. Verification: the closed-deal Brain page must exist before R1 lands the row in X1. -->

## 5. Brain interaction protocol

**Reads:** `customers/*/profile.md`, `customers/*/interactions/*`, `research/*`, `firm/sales/pipeline-*.md`.

**Writes:** `firm/sales/pipeline-<date>.md`; `customers/<slug>/contracts/<contract-id>.md`; `customers/<slug>/interactions/<date>.md` for each meaningful touch; `firm/sales/lumina-reviews/<week>.md`.

## 6. Excel interaction protocol

| File | Operation | Trigger |
|---|---|---|
| X1 partner-output-ledger.xlsx | (read-only; R1 writes deal_closed rows) | R1 sub-flow |
| X2 reward-species-declaration.xlsx | (read-only; pack consults Long_Tail_Schedule for sales eligibility) | Manual + R4 |

## 7. Routine integration

- **R1** sub-flow for sales output capture.
- **R4** uses this pack's long-tail attribution for sales-driven entitlements.

## 8. Don'ts (scaffold)

1. **Don't auto-send outreach** without partner sign-off.
2. **Don't omit closed deals from the partner output ledger** — sales is output too.
3. **Don't bypass the Lumina widget's qualification step.**
4. <!-- TODO: harden — don't credit a partner with a deal if the customer was sourced inbound via Lumina without that partner's involvement. The Lumina widget contributes; the partner who closes the deal gets credit; ambiguity goes to the BR for adjudication. -->
5. <!-- TODO: harden — don't auto-respond to inbound Lumina conversations on partner accounts. The Lumina-as-front-door pattern: Lumina handles initial conversation; qualified leads are warm-handed-off to a human partner. -->

## 9. Quick reference

<!-- TODO: harden. -->

## 10. References

1. **Yolo Investments.** *Stop paying for hours.* — sales attribution explicitly addressed.
2. **Lumina AI documentation** — the firm's RAG widget; https://lumina-ai.com/ (or relevant URL).
3. ØØT Skill Pack S3 — Compensation & Attribution (sales output ledger integration; long-tail attribution).
4. ØØT Skill Pack S9 — Marketing (Lumina widget shared dependency).
5. ØØT [`templates/brain/FIRM-ONTOLOGY.md`](../../templates/brain/FIRM-ONTOLOGY.md) — `customers/` domain conventions.

## Acceptance criteria for v1.x hardening

- Sales-as-output framing explicit (every operational instruction reinforces).
- Lumina widget integration spec complete (knowledge sync + conversation review + qualification rubric + escalation flow).
- Long-tail-for-sales worked example included (companion to S3 example #2 which shows engineering long-tail).
- 3+ worked examples in `examples/`.
- Frontmatter `status` → `hardened`.
