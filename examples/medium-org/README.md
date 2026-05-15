# Reference Org: Brda Cooperative (12-partner medium org)

## Profile

- **Firm:** Brda Cooperative. AI-augmented analytics for the wine industry. Founded 2025-Q2; ØØT-adopted 2026-Q1 after readiness assessment (X9 score: 71%).
- **Cohort mix:**
  - 5 full-time partners (founders + senior).
  - 4 project specialists (each tied to one customer engagement).
  - 3 advisors (industry, technical, M&A).
- **Reward species mix:** 3 hybrid, 1 lockstep (most senior founder), 1 eat-what-you-kill.
- **Track:** cloud.
- **Brain status:** Level 4. Each partner runs their own Curator with 4 personal domains: `firm`, `customers`, `products`, `legal`. The `firm` domain is opted-in to the Firm Brain. **Firm Brain** is a Curator Shared Brain instance per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md).
- **GitHub repos:** two — `brda-coop-ledger` (operational state) + `brda-coop-brain` (Firm Brain). EU-residency requirement (one customer is a regulated EU supervisor) means **GitHub Enterprise Cloud with EU residency option** for both repos (5 seats = ~€105/mo).
- **Firm Brain IP mode:** `organisational` (binding via the cooperative's IP-assignment policy in each Partner Charter §8.1). The 3 advisors signed side-letters explicitly affirming `organisational` for the brain even though they are paid as advisors — the cooperative's policy is that all firm-IP contributions go to the cooperative regardless of cohort. Specialists' Output Specs (one per customer engagement) remain in the Ledger as operational artefacts; only firm-level theses, decisions, ADRs go to the Firm Brain.
- **Attribution flags:** UUID-pseudonymous baseline. Three founders enable `attribute_by_name` selectively on customer-facing thought-leadership pages (signed firm theses, market analyses) that go to the firm's external blog after synthesis.
- **Synthesize cadence:** weekly, Sunday evening, alternates between the founders (rotation logged in `firm/routines/changelog.md`). Cost ~$0.04/week (heavier than small-org because of higher contribution volume).
- **Legal posture:** Slovenian cooperative (`zadruga`) + Croatian d.o.o. sister entity. EU-only operations.
- **EU AI Act exposure:** Limited + ONE high-risk use case (AI-driven supplier-trust scoring used by wine-industry customers). Counsel engaged; full Article 9/12/13/14 mapping in X7.

## Awkward edges to find

1. **Cohort change** — see `firm/decisions/D-2026-02-005.md`. Specialist Marin promoted to full-time partner mid-quarter. Renegotiation in his X2 Renegotiation_Log; prorated cohort change handled correctly.
2. **A Tier-2 dispute** — see `firm/compensation/2026-02/disputes/D-2026-02-003.md`. A specialist disputed her Output Spec being closed without acceptance; Tier 1 didn't resolve; partner panel met (3 partners, one non-beneficiary); ruled in specialist's favour; variable adjusted retroactively.
3. **A METR perception gap caught in pilot** — see `firm/change/pilots/code-qa-2026-q1.md`. 28-point perception gap at week 4 of Code & QA pilot; remediated *before* full rollout.
4. **An EU AI Act high-risk use case** — see `firm/compliance/use-cases/UC-001-supplier-trust-scoring.md`. Full Article 9/12/13/14 mapping. Counsel reviewed and signed off. Daily R6 audit trail. One anomaly in audit log (low-confidence supplier override; recorded; reviewed in next BR).
5. **A Klarna Test that initially failed** — see `firm/klarna-tests/KT-2026-002.md`. Replace human contract review for routine customer agreements. First score: 11. Held. Remediation. Re-scored at 15. Proceeded with 90-day review.

## What this example demonstrates

- Cohort diversity is operationally workable.
- Tier-2 disputes can resolve without escalation to founder.
- EU AI Act mapping is functional for a single high-risk use case.
- Klarna Test "fail → remediate → pass" is a normal flow, not an emergency.

## v1.0 scaffold status

This reference org ships as a scaffold in v1.0. Directory structure complete; representative Brain pages in place. Full-quarter operational data lands in v1.x.
