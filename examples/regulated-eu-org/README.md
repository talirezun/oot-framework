# Reference Org: AdriaLex AI (6-partner regulated-EU consultancy)

## Profile

- **Firm:** AdriaLex AI. Regulated-EU AI consultancy serving banking and insurance clients. Founded 2025-Q4 specifically to operate as ØØT-native.
- **Cohort:** 6 full-time partners; no specialists or advisors; all have legal/compliance backgrounds + AI engineering competence.
- **Track:** cloud, with privacy-track migration **in progress** (mid-stream at the snapshot date — week 3 of 4).
- **Brain status:** Each partner runs their own Curator with `firm`, `customers`, `products`, `legal`, `personal` domains. `firm` is opted-in to the Firm Brain. **Firm Brain** is a Curator Shared Brain instance per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md).
- **GitHub repos:** two — `adrialex-ledger` + `adrialex-brain`. **GitHub Enterprise Cloud with EU data residency option** for both (mandatory — clients are EU-regulated banks/insurers; data residency is a contractual requirement). Cost: ~€126/mo for 6 seats. Curator v3.1's Cloudflare R2 with `jurisdiction = "eu"` will let them drop to GitHub Team + R2 (~€80/mo savings).
- **Firm Brain IP mode:** `organisational` for all 6 partners (binding via the Partner Charter §8.1 IP-assignment clause — non-negotiable for AdriaLex given the regulated client base and the firm's IP being the substantive deliverable). The DPO partner additionally maintains a documented Article 17 erasure runbook for partner exits and for any client-data-subject erasure requests that cascade into the Firm Brain.
- **Attribution flags:** UUID-pseudonymous baseline. NO partners enable name attribution on Firm Brain pages — the firm's posture is that synthesized firm IP is a collective work product, attribution by name would compromise both the collective framing and the GDPR-minimisation discipline.
- **Synthesize cadence:** weekly. Cadence varies during the privacy-track migration (week 3-4) — admin alternates between cloud Curator on a laptop and the always-on machine. Post-migration: Sunday evening cron on the always-on machine.
- **Article 17 readiness:** the DPO partner has run the revoke endpoint end-to-end against a test contributor UUID during onboarding (`firm/compliance/erasure-rehearsal-2026-03-15.md`). This is mandatory rehearsal for any EU-regulated firm; documented in the firm's compliance manual.
- **Legal posture:** Croatian d.o.o.; counsel on retainer (mandatory for client base); EU AI Act compliance is the *product*.
- **EU AI Act exposure:** 6 AI use cases, 3 high-risk (Annex III mappings including employment-decision support and access-to-essential-services classifiers used for clients), 2 limited-risk, 1 minimal. Full Article 9/12/13/14 mapping per high-risk use case.
- **GDPR exposure:** Active. Handles client data subject to Article 22. Designated DPO (one of the partners).

## Awkward edges to find

1. **The abandoned engagement** — see `firm/klarna-tests/KT-2026-005.md`. Klarna Test scored 6/20; remediation infeasible; founder declined the client engagement. Decision recorded at `firm/decisions/D-2026-03-010.md`. **The framework's purpose in action — refusing a fee.**
2. **A GDPR Article 22 escalation** — see `firm/compliance/gdpr-escalations/2026-04-12.md`. Employment-screening classifier challenged by data subject. R6 audit trail had the relevant decision logged with human reviewer; firm produced trail to supervisory authority within 24 hours; no fine.
3. **Privacy-track migration mid-stream** — see `firm/privacy-track/migration-runbook.md`. Week 1-3 done; week 4 pending. **Honest framing:** mixed mode is messy in week 2-3.
4. **A non-beneficiary reviewer rejection** — see `firm/klarna-tests/KT-2026-007.md`. Non-beneficiary reviewer initially refused to sign — thought affected partner had not been adequately consulted. Test paused; additional consultation; affected partner's concerns addressed; reviewer signed. The conversation log is in the Brain page.

## What this example demonstrates

- The framework works under EU regulatory pressure.
- The Klarna Test really declines engagements (not a paper discipline).
- GDPR Article 22 audit trail is operationally robust.
- Privacy-track migration is a multi-week endeavour, not a weekend.

## v1.0 scaffold status

This reference org ships as a scaffold in v1.0. Directory structure complete; representative Brain pages in place. The 60-day operational dataset (60 daily audit logs, 8 Klarna tests, 4 ADRs, full X7 mapping) lands in v1.x.

The **abandoned engagement** is the most important single artefact in this reference org — it shows the framework declining a client when the Klarna Test cannot be cleared. New founders should read this first.
