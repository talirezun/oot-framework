# Skill Pack S7 — Governance & Compliance: SPEC

**ID:** S7 | **Tier:** 2 | **Status:** Hardened (v1.3.1)

## Purpose

Operationalises the EU AI Act mapping methodology (`governance/EU-AI-ACT.md`), GDPR compliance disciplines (Articles 17 and 22), Italian Law 132/2025 safeguards, and the legal touchpoints from `docs/06-when-to-call-a-lawyer.md`. Owns the lifecycle of `eu-ai-act-mapping.xlsx` (X7) and the operational standards of the daily EU AI Act Audit Trail Routine (R6).

## Scope

- **EU AI Act Articles 9, 12, 13, 14:** Systematic mapping of all firm AI use cases to Annex III classifications; continuous Article 9 risk management; Article 12 automatic audit trail via Routine R6 with practical immutability on protected git branches; Article 13 deployer instructions and transparency; Article 14 human-above-the-loop oversight mechanisms.
- **GDPR Article 22:** Operational verification that no automated routine executes decisions affecting partner compensation, contract standing, or customer rights without human sign-off.
- **GDPR Article 17 Erasure Runbook:** Two-tier erasure protocol distinguishing the Firm Brain (`<firm>-brain` via Curator Shared Brain admin revoke API) from the Ledger (`<firm>-ledger` statutory retention under Art 17(3)(b) and pseudonymization / git filter-repo).
- **Italian Law 132/2025:** Compliance boundary checks for Italian operations, focusing on Art. 612-quater criminal deepfake provisions and statutory aggravating factors.
- **Risk Register & Compliance Dossier:** Full maintenance of `firm/excel/eu-ai-act-mapping.xlsx` (X7), quarterly compliance review compilation, and preparation of the eleven legal touchpoints for external legal counsel.

## Allowed tools

- `mcp__my-curator__get_node`
- `mcp__my-curator__compile_to_wiki`
- `mcp__my-curator__search_wiki`
- `mcp__excel__read_workbook`
- `mcp__excel__write_cell`
- `mcp__excel__append_row`
- `mcp__github__create_or_update_file`
- Python runtime (`openpyxl`) and Git CLI for signed commits.

## Section structure

Standard canonical 10-section structure:
1. Purpose
2. When to invoke this pack
3. When NOT to invoke this pack
4. Operational instructions (§4.1 Use-case classification, §4.2 Article 9 risk management, §4.3 Article 12 audit trail & R6, §4.4 Article 13 transparency, §4.5 Article 14 human oversight, §4.6 GDPR Article 22 solely-automated avoidance, §4.7 GDPR Article 17 dual-repo erasure runbook, §4.8 Italian Law 132/2025 checks, §4.9 Quarterly reviews & annual counsel preparation)
5. Brain interaction protocol
6. Excel interaction protocol (X7 `eu-ai-act-mapping.xlsx`)
7. Routine integration (R6 daily audit trail owner, R2 BR feed, R7 Klarna coordination)
8. Don'ts (strict operational prohibitions)
9. Quick reference
10. References

## Don'ts

1. Don't treat compliance as a one-time checklist; it is continuous.
2. Don't bypass the daily R6 audit trail.
3. Don't downgrade to unsigned git commits.
4. Don't claim formal EU AI Act or GDPR compliance without qualified local legal counsel review.
5. Don't permit automated payment or disciplinary execution without human-above-the-loop sign-off.
6. Don't update the X7 Risk Register without an audit-trailed git commit.
7. Don't auto-publish Article 13 transparency notices or external filings without founder and counsel approval.
8. Don't execute destructive git history rewriting (`git filter-repo`) without counsel guidance and verified backup isolation.
9. Don't run compliance audit trails on GitHub Free private repositories.

## References

1. Regulation (EU) 2024/1689 (the AI Act).
2. Regulation (EU) 2016/679 (GDPR, Articles 17 and 22).
3. Italian Law No. 132/2025.
4. EDPB Guidelines on Automated Decision-Making and Profiling (WP251rev.01).
5. NIST AI Risk Management Framework (AI RMF 1.0).
6. ISO/IEC 42001:2023 Artificial Intelligence Management System.
7. ØØT `governance/EU-AI-ACT.md`.
8. ØØT `governance/DECISION-RIGHTS.md`.
9. ØØT `docs/06-when-to-call-a-lawyer.md`.
10. ØØT `templates/excel/SPEC.md` (X7).
11. ØØT `routines/SPEC.md` (R6).
12. ØØT `docs/internal/ADR-001` and `ADR-002`.

## Acceptance criteria

- Hardened SKILL.md passes `scripts/validate_skills.py` with zero errors.
- Zero TODO markers anywhere in the pack.
- 3+ worked examples in `examples/`.
- Dedicated references README in `references/README.md`.