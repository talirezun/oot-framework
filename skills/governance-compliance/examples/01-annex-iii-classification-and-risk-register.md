# Example 1 — Annex III High-Risk Classification & Risk Register Population

A complete worked example of evaluating a newly proposed agentic capability, classifying it under the EU AI Act (Regulation (EU) 2024/1689), establishing Article 9 risk management mitigations, and logging the evidence trail in `eu-ai-act-mapping.xlsx` (X7).

## The setup

- **Firm:** AdriaTech Solutions (12-partner AI engineering partnership based in Ljubljana, Slovenia).
- **Proposal:** A new agentic pipeline named **Candidate Code Evaluator** (`UC-004`), designed to evaluate incoming partner candidates and specialist contractors by analyzing submitted GitHub repositories, generating a 10-dimension technical score, and ranking applicants.
- **Operating Lead:** Matej K. (`P-003`, Engineering Lead).
- **Target Deadline:** Pre-deployment clearance ahead of the 2 August 2026 EU AI Act high-risk enforcement date.

---

## Phase 1 — Use-case intake and classification (§4.1)

Matej invokes Skill Pack S7: *"We want to deploy Candidate Code Evaluator to screen external partner candidates. Classify this system against the EU AI Act and prepare our compliance entries."*

The pack follows §4.1:

### 1. Article 5 Prohibitions Check
- The agent does not employ subliminal or manipulative techniques.
- The agent does not exploit vulnerabilities of age, disability, or socio-economic situation.
- The agent does not perform biometric categorization or social scoring.
- **Verdict:** Pass (Not an Article 5 prohibited practice).

### 2. Annex III Category Mapping
The pack evaluates the eight categories of Annex III:
- Point 1: Biometrics — *No*.
- Point 2: Critical infrastructure — *No*.
- Point 3: Education and vocational training — *No*.
- **Point 4: Employment, workers management and access to self-employment:**
  - *(a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to screen or filter applications, and to evaluate candidates.*
  - **Verdict:** **Direct Match with Point 4(a)**. Even though ØØT operates on a partner-not-employee model, Annex III explicitly covers "access to self-employment" and selection of natural persons.

### 3. Tier Classification
- **Classification:** **HIGH RISK (Annex III, Point 4(a))**.
- **Mandatory Obligations:** Articles 9 (Risk Management System), 12 (Record-Keeping), 13 (Transparency), 14 (Human Oversight), and GDPR Article 22 (Avoidance of solely automated decisions).

---

## Phase 2 — Article 9 risk management assessment (§4.2)

The pack guides Matej through the four risk dimensions:

| Risk Category | Identified Hazard | Inherent Severity | Mitigation Control | Residual Risk |
|---|---|---|---|---|
| **Technical** | LLM hallucination of syntax errors; bias toward specific coding styles / frameworks | High | Standardized AST parsing; test suite validation; LLM provides diffs rather than raw scores | Low |
| **Governance** | Unconscious demographic bias (proxy data in commit history or repository metadata) | Critical | Automated stripping of author names, emails, university names, and dates prior to LLM ingest | Low |
| **Human Agency** | Automation bias: partners accepting agent candidate rankings without reading the candidate's actual code | High | Mandatory independent code review by two human partners; agent report hidden until human reviews are submitted | Low |
| **Legal** | Candidate challenge under GDPR Article 22 (automated filtering of applicants) | High | Zero candidate is rejected based on automated score alone; every applicant receives human partner review | Controlled |

The detailed assessment is committed to the Ledger at `firm/compliance/risk-assessments/UC-004-candidate-screener.md`.

---

## Phase 3 — Article 13 & 14 governance design (§4.4, §4.5)

### Article 13 Transparency Notice (Instructions for Use)
The pack drafts candidate-facing disclosure copy for the firm's onboarding portal:
> *"AdriaTech Solutions utilizes an AI-assisted evaluation tool (Candidate Code Evaluator) to assist our partners in reviewing technical code samples. The system evaluates automated test coverage, modularity, and documentation clarity. It produces an advisory summary. Final decisions regarding partnership or engagement are made exclusively by our human Partner Selection Committee."*

### Article 14 Human Oversight Mechanism
- The system is architected as **Human-in-the-Loop (HITL)**.
- The agent cannot issue rejection letters, send invitations, or approve contracts.
- Two partners (`P-001` and `P-003`) must sign off on the selection packet in `firm/partners/candidates/CAN-2026-014.md`.

---

## Phase 4 — Spreadsheet updates in `eu-ai-act-mapping.xlsx` (X7)

Using `openpyxl`, S7 appends and updates the four core sheets in X7:

### 1. `Use_Cases` Sheet
- `use_case_id`: `UC-004`
- `name`: Candidate Code Evaluator
- `owner_partner_id`: `P-003`
- `brief_description`: LLM-assisted repository and code sample analysis for prospective partner candidates.
- `deployment_status`: `pilot`
- `affected_population`: prospective partners and contractor candidates
- `brain_link`: `firm/compliance/risk-assessments/UC-004-candidate-screener.md`

### 2. `Annex_III_Risk_Mapping` Sheet
- `use_case_id`: `UC-004`
- `annex_iii_category`: `Point 4(a) Recruitment & Selection`
- `rationale`: Evaluates candidate code submissions to inform partnership admission.
- `conservative_baseline_tier`: `high`
- `counsel_review_status`: `pending`
- `counsel_review_date`: `2026-07-15` (scheduled)

### 3. `Article_Obligations` Sheet
- `use_case_id`: `UC-004`
- `article_9_status`: `compliant`
- `article_12_status`: `compliant` (logged in daily R6)
- `article_13_status`: `compliant` (candidate disclosure active)
- `article_14_status`: `compliant` (dual-partner signoff required)
- `gdpr_article_22_status`: `compliant` (no automated rejection)
- `evidence_refs`: `firm/compliance/risk-assessments/UC-004-candidate-screener.md`

### 4. `Evidence_Trail` Sheet
- Row appended linking requirement "Art 14 Human Oversight" to `firm/partners/candidates/CAN-2026-014.md` and verified date `2026-06-18`.

---

## Phase 5 — Ledger commit & audit verification

The changes are committed to the Ledger repository via signed commit:

```bash
git add firm/compliance/risk-assessments/UC-004-candidate-screener.md firm/excel/eu-ai-act-mapping.xlsx
git commit -S -m "S7: classify UC-004 Candidate Code Evaluator as High-Risk Annex III Point 4(a)"
git push origin main
```

At 23:00 UTC, Routine R6 fires. It detects the commit, extracts the decision metadata, and records in `firm/audit-logs/2026-06-18.md`:

```markdown
### 2026-06-18T14:32:10Z — claude-3-7-sonnet + S7 — UC-004
- **Skill / Routine:** `governance-compliance`
- **Decision context:** Annex III risk classification and Article 9 risk assessment for Candidate Code Evaluator.
- **Output:** Classified as High-Risk Annex III Point 4(a). Risk mitigations, Article 13 notice, and Article 14 dual-partner sign-off controls established.
- **Human reviewer:** Matej K. (`P-003`)
- **Annex III mapping:** Point 4(a) Recruitment/Selection
```

The system is now fully compliant and documented for external counsel review.
