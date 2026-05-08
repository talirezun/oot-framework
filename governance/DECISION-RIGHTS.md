# Decision Rights — RACI Matrix Template

Who decides what in an ØØT organisation. The matrix below is a template; every adopting organisation must adapt it to their specific partner roster, jurisdiction, and operational reality.

The matrix uses standard RACI notation: **R**esponsible (does the work), **A**ccountable (signs off and is answerable), **C**onsulted (input solicited before decision), **I**nformed (told after decision).

This is a Generation 1 document. In Generation 2, the matrix integrates with the smart-contract long-tail entitlement system (decisions affecting entitlements require on-chain co-signature). In Generation 3, the matrix incorporates Cotrugli Ledger PAC-RO co-signature requirements for cross-firm decisions.

---

## Template matrix

The columns are roles; substitute your organisation's actual roles. The rows are decision categories. Fill in R / A / C / I per cell.

**Roles in the template:**
- **F** — Founder(s). For multi-founder firms, all founders are jointly Accountable for top-tier decisions.
- **MP** — Managing Partner / operational lead (where designated).
- **P** — Other partners (full-time or specialist, depending on the decision's domain relevance).
- **A** — Advisors (consultative role only by default; no Accountability).
- **AP** — Affected Partner (the partner whose work, compensation, or scope is the decision's primary subject).
- **L** — Local counsel (Consulted on legal-touchpoint decisions; never Responsible or Accountable).

### Strategic decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| Annual operating plan | A | R | C | C | — | I |
| Entry into a new market or product line | A | R | C | C | — | C |
| Significant capital deployment (>10% of treasury) | A | R | C | C | — | I |
| Adoption of Generation 2 (Unit Fund opening) | A | C | C | C | — | C |
| Adoption of Generation 3 (Cotrugli Ledger anchoring) | A | C | C | C | — | C |
| Material change to the Klarna Test threshold | A | R | C | — | — | — |

### Compensation decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| Reward Species Declaration (initial) | A | C | I | — | R | C |
| Reward Species Declaration (renegotiation) | A | C | I | — | R | C |
| Variable pay calculation (monthly) | A | R | I | — | C | — |
| Long-tail entitlement (quarterly settlement) | A | R | I | — | C | — |
| Variable pay dispute resolution (Tier 1) | C | A | — | — | R | — |
| Variable pay dispute resolution (Tier 2) | A | R | C | C | C | C |
| Variable pay dispute resolution (Tier 3) | A | C | — | — | C | C |

### People decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| New partner onboarding (full-time) | A | R | C | — | — | C |
| New partner onboarding (specialist / advisor) | A | R | I | — | — | C |
| Partner exit | A | R | C | — | C | C |
| Cohort designation change | A | R | I | — | R | — |
| Promotion / scope expansion | A | R | C | — | R | — |

### AI rollout decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| New Skill Pack adoption | A | R | C | — | C | — |
| New Routine deployment | A | R | C | — | C | — |
| AI replaces human partner function (Klarna Test required) | A | C | C | C | R | C |
| METR baseline rollout | A | R | C | — | C | — |
| AI Champion designation | A | R | C | — | — | — |

### Vendor / tooling decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| New SaaS subscription / vendor selection | C | A | R | — | — | — |
| Tool replacement affecting daily workflow | A | R | C | — | C | — |
| Privacy track migration (firm-wide) | A | C | C | C | C | C |
| Crypto rail activation (Gen 2) | A | C | C | C | C | C |

### Legal / governance decisions

| Decision | F | MP | P | A | AP | L |
|---|---|---|---|---|---|---|
| Partner Charter template change | A | R | C | C | — | A |
| Variable-pay legal structure modification | A | C | I | C | C | A |
| Long-tail entitlement legal wrapper | A | C | I | C | C | A |
| Unit Fund opening (Gen 2) | A | C | C | C | C | A |
| EU AI Act risk register approval | A | R | C | — | — | A |

---

## How to read the matrix

**Every decision has exactly one A** (Accountable). Even when "the partnership decides," one human is named as Accountable for the decision standing.

**Every decision has at least one R** (Responsible). The R does the work — drafts the option set, runs the analysis, prepares the recommendation. R may be the same person as A in small orgs.

**C (Consulted) means input is solicited before the decision is made.** Not "informed afterward, in case they had thoughts." If C is solicited and the input is rejected, the rejection is recorded.

**I (Informed) means told after the decision.** This is the lightest involvement; it exists to keep the partnership informed of decisions that don't require their input.

**Local counsel (L) is C or A on legal-touchpoint decisions.** Never R alone. Counsel doesn't do the firm's work; counsel reviews and approves.

---

## Three-tier dispute resolution

When a partner disputes a decision (typically: a variable-pay calculation, a long-tail entitlement, a Klarna Test outcome, a cohort designation), the framework provides a three-tier resolution path:

### Tier 1 — Direct discussion

The Affected Partner raises the dispute with the Accountable party (per the matrix). They have a one-on-one discussion within five business days. Outcome documented in writing in the Brain.

If resolved: case closed. If not resolved within ten business days of the original raise, escalate to Tier 2.

### Tier 2 — Partner panel

A panel of three partners (none of whom are the Accountable party for the original decision; at least one must be a non-beneficiary of the disputed outcome) reviews the case, consults the partner, the original decision-maker, and any relevant data.

The panel issues a recommendation within 15 business days. The recommendation is binding unless the original Accountable party formally rejects it in writing with reasons.

If accepted (or unrejected within 5 business days): case closed. If rejected, escalate to Tier 3.

### Tier 3 — Founder + counsel

The Founder reviews the case with local counsel. The Founder issues the final decision in writing, with reasoning. This decision is binding within the partnership.

If the partner disputes the Tier 3 outcome, their remaining recourse is external (mediation, arbitration, or litigation per local jurisdiction). The framework does not provide a Tier 4.

**The honest framing:** Tier 3 is the framework's boundary. ØØT believes most disputes should resolve at Tier 1 (>80%) or Tier 2 (~15%). Tier 3 should be rare. If your organisation finds Tier 3 is being invoked frequently, the cause is upstream — usually unclear reward-species declarations or unclear output specs — and the fix is upstream, not in the resolution mechanism.

---

## Adapting this matrix

Small orgs (3–5 partners) typically collapse MP into F and treat all partners equally on most decisions. The matrix simplifies dramatically; the resolution tiers compress to two (direct + founder).

Medium orgs (6–15 partners) typically need the full MP role and benefit from a partner panel for Tier 2.

Large orgs (16+ partners — outside ØØT's primary v1.0 design target) typically need additional structure not covered here. The framework's authors believe ØØT-native firms above 20 partners are rare in v1.0; the spawning model (Generation 3 autonomous business units) is the planned response to scale.

---

## Commit the matrix

Once adapted, the matrix lives at `governance/DECISION-RIGHTS.md` in the firm's instance of the framework — not in the framework repository. The framework provides the template; the firm provides the realisation.

Review the matrix at every quarterly partner check-in. Decisions categories shift as the firm matures; the matrix should shift with them.