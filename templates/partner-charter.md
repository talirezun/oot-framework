# Partner Charter — {{FIRM_NAME}}

**Between:** {{FIRM_LEGAL_ENTITY}} ("the Firm")
**And:** {{PARTNER_FULL_NAME}} ("the Partner")
**Effective from:** {{START_DATE}}

This Partner Charter is the foundational agreement between the Firm and the Partner. It is **not an employment contract**; it is a partnership-style agreement defining how the Partner contributes output and how the Firm compensates that output. Both parties read, understand, and sign this document together.

> ⚠️ **This is a template, not legal advice.** Adapt to your jurisdiction with qualified counsel. Specifically: worker-classification law, variable-pay legality, and (Generation 2) securities-law implications of long-tail entitlements vary materially by jurisdiction. See `docs/06-when-to-call-a-lawyer.md` for the eleven legal touchpoints. Local counsel review before any signature.

---

## 1. Cohort designation

The Partner is engaged as a **{{COHORT}}**:

- **Full-time partner** — full output participation, monthly variable, long-tail entitlement, eligible for Unit Fund (Gen 2).
- **Project specialist** — defined project, defined deliverable, defined amount, exit at project end.
- **Advisor** — continuous engagement, narrow scope, smaller stake.

Cohort changes require a signed renegotiation per §6.

## 2. Reward Species Declaration

The Partner has signed a Reward Species Declaration recorded in `templates/excel/reward-species-declaration.xlsx` sheet `{{PARTNER_ID}}` and mirrored in the Brain at `firm/partners/{{PARTNER_ID}}/reward-species-declaration.md`. The declaration specifies:

- Reward species: `{{eat-what-you-kill | lockstep | hybrid}}`.
- Annual base amount: {{BASE}} {{CURRENCY}}.
- Variable weights (personal / team / company): summing to 1.0.
- Output multiplier (default 1.0).
- Bonus splits (personal / team / company): summing to 1.0.
- Stablecoin upgrade preference (Gen 2 readiness).
- Unit Fund interest (Gen 2 readiness).

The Reward Species Declaration is the contractual definition of how the Partner is compensated. It cannot be modified without the signed renegotiation flow per §6.

## 3. Output, not hours

The Partner is engaged to **produce output**, not to work hours. The Firm does not track time. Output is:

- A merged code commit, a signed contract, a closed deal, a published article, a delivered design, a substantive code review, a drafted Output Spec — anything that lands and ships.

Output is captured daily by Routine R1 to `templates/excel/partner-output-ledger.xlsx`. Each output is classified by value tier (S/M/L/XS) per §4.10 of Skill Pack S3. Variable pay is calculated monthly (Routine R3); long-tail entitlements settle quarterly (Routine R4).

## 4. The seven-layer compensation picture

The Partner's compensation has up to seven layers. Generation 1 ships layers 1, 2, 3, and 5; layers 4, 6, 7 ship in Generation 2.

1. **Guaranteed base** (monthly). Per §2.
2. **Output variable** (monthly). Computed from the daily ledger × value-tier × multiplier × rework-flag.
3. **Long-tail entitlement** (quarterly). Percentage entitlement against the realised outcome of qualifying outputs, per §2's Long_Tail_Schedule.
4. **Subscription credits** (Gen 2). Locked in Gen 1.
5. **Role-weighted annual bonus** (annual). Computed per §2's bonus splits.
6. **Dividends on units held** (Gen 2). Locked in Gen 1.
7. **Capital appreciation** (Gen 2). Locked in Gen 1.

The Partner agrees to the Gen 1 layers as defined and acknowledges the Gen 2 layers as deferred features that activate per a future signed amendment.

## 5. Klarna Test discipline

The Partner agrees that any decision to replace a partner's primary function with AI is subject to the Klarna Test per `governance/KLARNA-TEST.md`. The Partner specifically agrees:

- Their work is subject to the framework's discipline; it is not exempt.
- If the Partner's primary function is the subject of a Klarna Test, they will be the **affected partner** and consulted in writing per question 5 of the rubric.
- The Partner respects the non-beneficiary review (question 7): they will not score a test where their compensation is at stake.
- The 90-day post-deployment review (question 9) is real and they will participate.

## 6. Renegotiation

Either the Partner or the Firm may initiate a renegotiation of the Reward Species Declaration:

- **Quarterly check-in** is the natural point (per `routines/SPEC.md` and Skill Pack S5 §4.6).
- **Ad-hoc** at any time with written notice.

A renegotiation flow (per Skill Pack S3 §4.1):
1. Append a row to the Renegotiation_Log in `reward-species-declaration.xlsx`.
2. Apply field changes; update `start_date` of new terms (no retroactive changes to closed periods).
3. Re-sign signed PDF.
4. Update the Brain summary page.
5. Record the renegotiation as `firm/decisions/D-YYYY-NNN.md`.

The prior period's compensation never recomputes. Mid-month renegotiation produces a split-month statement showing both periods.

## 7. Disputes

If the Partner disputes any compensation calculation or framework decision, the three-tier resolution flow per `governance/DECISION-RIGHTS.md` applies:

- **Tier 1 — Direct discussion** (5 business days).
- **Tier 2 — Partner panel** (15 business days; binding unless rejected in writing by the original Accountable party).
- **Tier 3 — Founder + counsel** (binding within the partnership).

External recourse (mediation, arbitration, litigation) is the Partner's remaining option after Tier 3 per local jurisdiction.

## 8. Confidentiality and IP

The Partner agrees:

- All work product produced for the Firm — code, contracts, designs, content, prompts, ADRs — is the Firm's IP, with the licence-split applying for any externally-published content (Apache 2.0 for code; CC BY-SA 4.0 for documentation, where the Firm's IP is published openly).
- Customer information, partner-private information, and the Firm's trade secrets are confidential.
- The Brain is the Firm's IP; the Partner contributes to it; the Partner does not retain a personal copy upon exit beyond what was authored as their attributable contribution.

## 9. Two Worlds of Code self-identification

The Partner declares their Two Worlds of Code self-id (per Karpathy / Skill Pack S4 §4.9): `{{vibe-coder | agentic-engineer | transitional | non-code}}`. This is not a value judgement; it is an operational input to the Firm's training plan and Klarna Test triage.

## 10. Exit

The Partner may exit the partnership with **30 days' written notice** (Gen 1 default; jurisdiction may require longer). On exit:

- All variable pay through exit date is calculated and paid per the standard R3 cycle.
- Long-tail entitlements continue per the Long_Tail_Schedule (Gen 1: until end_date specified at output sign-off; Gen 2: per smart-contract terms).
- Bitwarden access revoked within 24 hours per `governance/SECRETS-POLICY.md`.
- 4thtech wallet (privacy track) remains the Partner's; the Firm updates routing.
- The Partner's contributions to the Brain remain in the Brain, attributed to them.

The Firm may exit the partnership with the Partner only:

- For cause (per the dispute-resolution flow's Tier 3 with counsel involvement).
- For business necessity, with the same 30-days notice and a documented decision in `firm/decisions/`.
- Subject to local jurisdictional requirements which may exceed the 30-day default.

## 11. Acknowledgements

The Partner acknowledges:

- They have read `MANIFESTO.md` (the framework's intellectual core).
- They have read `governance/KLARNA-TEST.md` and accepted the discipline.
- They have read `governance/DECISION-RIGHTS.md` and accepted the three-tier dispute path.
- They have signed the Reward Species Declaration in `templates/excel/reward-species-declaration.xlsx`.
- They have a personal device to access the Firm's tools and have completed onboarding per `docs/03-onboarding-a-partner.md`.

The Firm acknowledges:

- The Partner is engaged as `{{COHORT}}`, not as an employee.
- The Firm will pay all compensation per the Reward Species Declaration on the cadence specified.
- The Firm will not retroactively modify the Reward Species Declaration without signed renegotiation per §6.
- The Firm has obtained local counsel review of this Charter for the Partner's jurisdiction (`{{JURISDICTION}}`).

---

## Signatures

**Firm:** `_______________________________________`  ([[partners/{{FOUNDER_ID}}]], on behalf of {{FIRM_LEGAL_ENTITY}})

Date: `_____________`

**Partner:** `_______________________________________`  ([[partners/{{PARTNER_ID}}]])

Date: `_____________`

**Counsel reviewed:** `Yes / No.` Counsel: `_______________________________________`. Date: `_____________`.

---

*This Charter is generated from `templates/partner-charter.md` v1.0 ({{LAST_UPDATED}}). Modifications by the Firm are tracked in `firm/decisions/`.*
