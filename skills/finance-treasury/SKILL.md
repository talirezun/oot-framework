---
name: finance-treasury
description: Use whenever the firm is coordinating FIAT payroll (Gen 1), tracking agent costs vs. outputs (X6), running R8 treasury runway updates (X8 — only orgs adopting Unit Fund), preparing for Gen 2 stablecoin upgrade (per-partner jurisdiction verification), managing the monthly financial close, or forecasting treasury runway. Activates for "compute April payroll", "what's our agent-cost ROI?", "check runway for Q3", "verify Mira's stablecoin upgrade is legal in SI", "prepare the founder-approval packet".
version: 1.0.0
tier: 2
status: scaffold
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__excel__append_row
  - mcp__banking-api__list_accounts
  - mcp__banking-api__get_balance
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S10
oot_tier: 2
oot_status: scaffold
oot_dependencies: [S1, S2, S3, S5, S8]
oot_provides_to: []
oot_klarna_test: false
last_updated: 2026-05-08
---

# Finance & Treasury

> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.
> **Klarna Test interaction:** No directly.
> **Brain interaction:** Both — reads X1/X2 for compensation data; writes treasury snapshots, runway alerts, agent-cost ROI summaries.

## 1. Purpose

FIAT-default in v1.0; documents the **stablecoin upgrade path for Gen 2**. Owns:
- Treasury management coordination.
- **Agent-cost attribution** (Prefactor / Bifrost-style per-agent token accounting; X6 agent-skill-roi.xlsx).
- Monthly financial close coordination.
- Treasury runway tracker (X8 — **optional** in v1.0; mandatory only for orgs adopting Unit Fund Gen 2).
- Forecasting basics.

The pack does **not** execute payroll directly; it produces the founder-approval packet that authorises payroll execution via the firm's banking partners (Gen 1) or Rise/Circle stablecoin rails (Gen 2).

## 2. When to invoke this pack

1. <!-- TODO: harden — monthly payroll preparation (post R3 founder-approval packet → bank execution). -->
2. <!-- TODO: harden — quarterly long-tail settlement (post R4 → bank/stablecoin execution). -->
3. <!-- TODO: harden — agent-cost ROI weekly tracking (R8 sub-flow). -->
4. <!-- TODO: harden — treasury runway snapshot weekly (R8 main flow; optional). -->
5. <!-- TODO: harden — Gen 2 stablecoin upgrade verification (per-partner jurisdictional). -->
6. <!-- TODO: harden — annual financial close (year-end ledger lock + tax-prep handoff). -->
7. <!-- TODO: harden — Unit Fund opening prep (Gen 2; legal scoping + treasury reserve discipline). -->

## 3. When NOT to invoke this pack

1. **For variable pay calculation itself** — that's S3.
2. **For tax filing** — counsel/tax-advisor territory.
3. **For Unit Fund operations in Gen 1** — locked; pack returns "Not available in Gen 1".
4. **For currency hedging or derivatives** — out of scope; firm's external treasury advisor.

## 4. Operational instructions

<!-- TODO: harden in v1.x. -->

### 4.1 Monthly FIAT payroll execution (Gen 1)

<!-- TODO: harden — read R3 founder-approval packet at `firm/compensation/<month>/founder-approval.md`; produce a structured payment list (per-partner: amount, currency, IBAN, reference); execute via SEPA/wire from firm's banking partner; record `payment_date` in X1 Monthly_Variable. -->

### 4.2 Agent-cost attribution (X6 agent-skill-roi.xlsx)

<!-- TODO: harden — daily/weekly capture of token costs per Skill / Routine / use case. Sources: Anthropic API usage dashboard, Curator Gemini Flash Lite usage, LM Studio local inference (privacy track — electricity-attributed). Per-Skill ROI computed at month-end. -->

### 4.3 Treasury runway tracker (X8 — optional)

<!-- TODO: harden — R8 weekly sub-flow: pull bank balances + obligations → update X8 Cash_Position + Obligations + Runway_Calc. Alert if `runway_months < 9` OR `reserve_coverage_ratio < 1.0`. -->

### 4.4 Monthly financial close

<!-- TODO: harden — coordinate with bookkeeping (firm's accountant); ensure X1 month-locked status before close; deliver tax-prep packet to tax advisor. -->

### 4.5 Gen 2 stablecoin upgrade preparation

<!-- TODO: harden — per-partner jurisdictional check (S8 + counsel); verify USDC/EURC legal status; Rise (Circle partner) integration; per-partner wallet provisioning. -->

### 4.6 Smart-contract long-tail entitlement (Gen 2)

<!-- TODO: harden — replaces Excel-tracked Long_Tail_Schedule with on-chain percentage entitlements; counsel review per jurisdiction; quarterly auto-payment via smart contract. -->

### 4.7 Internal Unit Fund (Gen 2)

<!-- TODO: harden — opening procedure after 6-9 months of pilot data; treasury reserve discipline (X8 mandatory); subscription-credit issuance; bid/ask liquidity; quarterly dividend payments. -->

## 5. Brain interaction protocol

**Reads:** `firm/compensation/*`, `firm/partners/<id>/variable-statements/*`, `firm/partners/<id>/long-tail-statements/*`.

**Writes:** `firm/finance/treasury-snapshots/<date>.md`, `firm/finance/agent-cost-monthly/<month>.md`, `firm/finance/financial-close/<month>.md`.

## 6. Excel interaction protocol

| File | Sheet | Operation | Trigger |
|---|---|---|---|
| X6 agent-skill-roi.xlsx | Agent_Costs, Skill_Outputs, Human_Agent_Ratio, ROI_Calc | Write | Daily (R1+R8 inputs) + monthly rollup |
| X8 treasury-runway.xlsx (optional) | Cash_Position, Obligations, Runway_Calc | Write | R8 weekly |
| X1 partner-output-ledger.xlsx | Monthly_Variable col I (payment_date) | Update post-payment | Per execution |

## 7. Routine integration

- **R8** (Treasury Runway Update — OPTIONAL) — owned by this pack.
- Contributes to **R3** (post-approval payment execution) and **R4** (post-approval long-tail execution).

## 8. Don'ts (scaffold)

1. **Don't activate stablecoin payroll** without counsel review for the partner's jurisdiction.
2. **Don't open the Unit Fund** without ≥6–9 months of attribution accuracy data + treasury reserve coverage ≥1.0.
3. **Don't bypass treasury runway discipline** if the Unit Fund is open.
4. <!-- TODO: harden — don't run payroll without an explicit founder-approved packet matching the X1 Monthly_Variable. -->
5. <!-- TODO: harden — don't change X6 cost-attribution methodology without a Brain ADR (changes affect ROI calculations partners can see). -->

## 9. Quick reference

<!-- TODO: harden. -->

## 10. References

1. **Yolo Investments.** *Stop paying for hours.* — treasury reserve discipline.
2. **Rise (Circle partner)** — stablecoin payroll. https://riseworks.io/. Q1 2026 lifetime volume: $1.37B.
3. **EU MiCA** + **US GENIUS Act** — regulatory frameworks.
4. **Prefactor, Bifrost** — per-agent cost attribution patterns.
5. ØØT Skill Pack S3 — Compensation & Attribution (upstream dependency).
6. ØØT Skill Pack S8 — Legal Operations (jurisdictional verification).
7. ØØT [`templates/excel/SPEC.md`](../../templates/excel/SPEC.md) — X6, X8 schemas.

## Acceptance criteria for v1.x hardening

- Gen 1 vs. Gen 2 boundary explicit at every operational instruction.
- Bank-API integration patterns documented (jurisdiction-specific).
- Stablecoin upgrade procedure (Gen 2) walked through end-to-end with counsel handoff points.
- 3+ worked examples in `examples/`.
- Frontmatter `status` → `hardened`.
