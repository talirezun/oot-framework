# Skill Pack S3 — Compensation & Attribution: SPEC

**ID:** S3
**Name:** Compensation & Attribution
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

The most distinctive ØØT Skill Pack. Operationalises the seven-layer YOLO compensation model — base, output variable, long-tail outcome, subscription credits, role-weighted bonus, dividends, capital appreciation. v1.0 ships layers 1, 2, 3, and 5 as fully operational; layers 4, 6, 7 are deferred to Generation 2.

Encodes the attribution agent pattern: read commits, specs, reviews, contracts, milestones; produce a daily per-partner output ledger; compute monthly variable; track quarterly long-tail entitlements; surface anomalies for human review.

## Scope

**Covers (Generation 1):**
- Reward Species Declaration onboarding and renegotiation.
- Output Spec drafting and storage in the Brain.
- Daily output capture from GitHub, Slack, Drive, contracts (via Routine R1).
- Variable pay calculation against value-tier multipliers (monthly, via Routine R3).
- Long-tail entitlement tracking (Excel-based, quarterly settlement via Routine R4).
- Annual bonus calculation (third-third-third with role weighting).
- Variable pay dispute initiation (handing off to the dispute resolution playbook in `governance/DECISION-RIGHTS.md`).
- Klarna Test interaction: any Skill that would automate a partner's primary function triggers Routine R7 via the `ai-replaces-human` PR label.

**Deferred (Generation 2):**
- Stablecoin payroll rail integration (Rise / Circle).
- Smart-contract long-tail entitlements (replaces Excel-based quarterly settlement with on-chain auto-payment).
- Subscription credit issuance.
- Internal Unit Fund subscription, dividend payments, capital appreciation tracking.

**Deferred (Generation 3):**
- Per-agent compensation (autonomous business units earning variable).
- Cotrugli Ledger PAC-RO co-signature for compensation events.

**Does NOT cover:**
- Treasury management (that is the Finance & Treasury Skill Pack).
- Tax handling (that is jurisdiction-specific; pointed to `docs/06-when-to-call-a-lawyer.md`).
- Equity / cap-table management for existing investors (that is corporate governance, not compensation).

## Allowed tools / dependencies

- Curator MCP tools (read Brain, write Brain pages for ledger entries and Reward Species Declarations).
- Excel MCP / Google Sheets API (write to `partner-output-ledger.xlsx`, `reward-species-declaration.xlsx`).
- GitHub MCP (read commits, PRs).
- Slack MCP (read configured channels for output signals).
- Filesystem MCP / Desktop Commander (privacy track).

## Section structure

1. **Purpose**
2. **When to invoke**
3. **When NOT to invoke**
4. **Operational instructions:**
   - 4.1 Reward Species Declaration workflow (initial + renegotiation).
   - 4.2 Output Spec drafting (template + Brain commit).
   - 4.3 Daily output capture (Routine R1 invocation pattern).
   - 4.4 Monthly variable pay calculation (Routine R3 invocation pattern).
   - 4.5 Long-tail entitlement entry (manual + Routine R4 settlement).
   - 4.6 Annual bonus calculation.
   - 4.7 Klarna Test interaction (Routine R7 trigger).
   - 4.8 Dispute initiation (handoff to DECISION-RIGHTS).
5. **Brain interaction protocol** — heavy reads/writes; specifies the `partners/` and `outputs/` and `ledger/` slug conventions.
6. **Excel interaction protocol** — writes to X1 (ledger), reads X2 (declarations), writes to X4 (Klarna Test entries when triggered).
7. **Routine integration** — primary owner of R1, R3, R4. Triggered by R7.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts

1. Don't compute variable pay without monthly human sign-off — the calculator is advisory; the founder pays.
2. Don't override a partner's Reward Species Declaration without signed renegotiation — the declaration is contractual.
3. Don't aggregate output across partners in ways that obscure individual attribution.
4. Don't treat AI-generated commits as equivalent to human-written ones for attribution; track AI-vs-human authorship per the YOLO model's "rework within 30 days" principle.
5. Don't bypass the Klarna Test when a Skill rollout would replace a partner's primary function.

## Worked examples concept

**Example 1:** New partner onboards. Walk through Reward Species Declaration (full-time partner, hybrid 70/30 eat-what-you-kill/team-bonus, base €30k, stablecoin upgrade preference: yes when Gen 2 lands). Sign. Commit. The pack triggers R1 to start capturing this partner's outputs from day one.

**Example 2:** End of month. The pack reads the partner output ledger, applies the partner's value-tier multipliers, computes variable for the month, drafts a per-partner statement, sends to each partner for review, escalates to founder for sign-off. Two partners flag attribution errors; the pack walks through the dispute initiation per DECISION-RIGHTS Tier 1.

## References

1. Yolo Investments. *Stop paying for hours. Start paying for output.* (May 2026). The seven-layer compensation framing.
2. Levin, J. & Tadelis, S. *Profit Sharing and the Role of Professional Partnerships* (Stanford GSB).
3. Ressler, C. & Thompson, J. *Why Work Sucks and How to Fix It* (2008). ROWE.
4. MHPR Advisors. *Reward Species Typology* — the seven partnership reward models.
5. Hope, J. & Fraser, R. *Beyond Budgeting* (1998).
6. Weitzman, M. *The Share Economy* (1984).
7. ØØT `MANIFESTO.md`, Thesis 3 — Employees become Partners.
8. ØØT `governance/KLARNA-TEST.md`.

## Acceptance criteria

Standard. Plus:
- The seven-layer compensation picture is explicit in section 4 with Gen 1 / Gen 2 / Gen 3 markings.
- The Klarna Test interaction (R7 trigger) is wired and documented.
- At least 4 worked examples in `examples/` (variable pay, long-tail, dispute, Klarna trigger).