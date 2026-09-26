# References — Skill Pack S7 (Governance & Compliance)

The statutory, regulatory, and technical foundations of the framework's governance, AI risk management, and compliance disciplines.

## Primary statutory & regulatory instruments

1. **European Union.** *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).* Official Journal of the European Union, L 2024/1689, 12 July 2024. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689.
   - *Key provisions:* Article 5 (Prohibited AI practices), Article 6 & Annex III (Classification rules for high-risk AI systems), Article 9 (Risk management system), Article 11 (Technical documentation), Article 12 (Record-keeping / automatic logging), Article 13 (Transparency and provision of information to deployers), Article 14 (Human oversight), Article 50 (Transparency obligations for providers and deployers of certain AI systems), and Article 71 (Penalties).

2. **European Union.** *Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation — GDPR).* Official Journal of the European Union, L 119, 4 May 2016. https://eur-lex.europa.eu/eli/reg/2016/679/oj.
   - *Key provisions:* Article 17 (Right to erasure / "right to be forgotten"), Article 17(3)(b) (Exemptions for compliance with a legal obligation), and Article 22 (Automated individual decision-making, including profiling).

3. **Italian Republic.** *Legge 23 settembre 2025, n. 132 — Disposizioni in materia di intelligenza artificiale.* Gazzetta Ufficiale della Repubblica Italiana, Serie Generale n. 224, 25 settembre 2025 (in force 10 October 2025).
   - *Key provisions:* Article 612-quater Codice Penale (Illicit dissemination of content generated or manipulated with AI systems) and statutory aggravating circumstances for computer fraud and intellectual property infringement committed using AI.

## Regulatory guidance & international standards

4. **European Data Protection Board (EDPB).** *Guidelines on Automated individual decision-making and Profiling for the purposes of Regulation 2016/679* (WP251rev.01, adopted 3 October 2017, as last revised and adopted on 6 February 2018). https://edpb.europa.eu/.
   - Establishes the authoritative European interpretation of "meaningful human intervention" under Article 22, confirming that superficial rubber-stamping of automated recommendations fails the human-in-the-loop requirement.

5. **National Institute of Standards and Technology (NIST).** *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1, U.S. Department of Commerce, January 2023. https://doi.org/10.6028/NIST.AI.100-1.
   - Core functions: Govern, Map, Measure, Manage. Informs S7's Article 9 four-dimension risk taxonomy (technical, governance, operational, human agency).

6. **International Organization for Standardization (ISO) / International Electrotechnical Commission (IEC).** *ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system.* Geneva, Switzerland: ISO/IEC, December 2023. https://www.iso.org/standard/81230.html.
   - Requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organisations.

7. **High-Level Expert Group on Artificial Intelligence (AI HLEG).** *Ethics Guidelines for Trustworthy AI.* European Commission, B-1049 Brussels, 8 April 2019. https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai.
   - Informs the foundational requirements of technical robustness, human agency, privacy governance, and non-discrimination.

## Cross-references inside ØØT

- ØØT [`governance/EU-AI-ACT.md`](../../../governance/EU-AI-ACT.md) — The framework's core mapping methodology, compliance timeline, and Annex III conservative baselines.
- ØØT [`governance/DECISION-RIGHTS.md`](../../../governance/DECISION-RIGHTS.md) — Three-tier authority matrix, human decision rights, and partner dispute escalation paths.
- ØØT [`governance/KLARNA-TEST.md`](../../../governance/KLARNA-TEST.md) — The 20-point risk and justification gate for AI-assisted human substitution.
- ØØT [`docs/06-when-to-call-a-lawyer.md`](../../../docs/06-when-to-call-a-lawyer.md) — The eleven jurisdiction-specific legal touchpoints requiring qualified local counsel.
- ØØT [`templates/excel/SPEC.md`](../../../templates/excel/SPEC.md) — Specification for workbook X7 (`eu-ai-act-mapping.xlsx`), sheets `Use_Cases`, `Annex_III_Risk_Mapping`, `Article_Obligations`, `Evidence_Trail`, and `Audit_Log_Index`.
- ØØT [`routines/SPEC.md`](../../../routines/SPEC.md) — Operational requirements for Routine R6 (EU AI Act Audit Trail) and R7 (Klarna Test Trigger).
- ØØT [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../../../docs/internal/ADR-001-cloud-routine-excel-writeback.md) — Architectural decision establishing openpyxl execution on git clones rather than hosted spreadsheet APIs.
- ØØT [`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](../../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md) — Architectural decision separating the Ledger (`<firm>-ledger`) from the Firm Brain (`<firm>-brain`).
