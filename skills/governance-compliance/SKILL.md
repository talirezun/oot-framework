---
name: governance-compliance
description: Use whenever the firm is mapping AI use cases to the EU AI Act, populating or updating eu-ai-act-mapping.xlsx (X7), executing or auditing the daily R6 audit trail Routine, conducting a quarterly compliance review, preparing for external counsel review, handling GDPR Article 17 contributor erasure requests across the dual-repo architecture, responding to GDPR Article 22 solely-automated-decision inquiries, or evaluating Italian Law 132/2025 compliance. Activates for "map this use case against Annex III", "is our R6 audit trail compliant?", "draft the Article 13 transparency notes for our supplier-trust scoring system", "respond to this data-subject GDPR access request", "execute contributor revocation under Article 17", "prepare compliance dossier for counsel review".
version: 1.0.0
tier: 2
status: hardened
allowed_tools:
  - mcp__my-curator__get_node
  - mcp__my-curator__compile_to_wiki
  - mcp__my-curator__search_wiki
  - mcp__excel__read_workbook
  - mcp__excel__write_cell
  - mcp__excel__append_row
  - mcp__github__create_or_update_file
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
oot_pack_id: S7
oot_tier: 2
oot_status: hardened
oot_dependencies: [S1, S2, S3, S6]
oot_provides_to: [S4, S5, S8]
oot_klarna_test: false
last_updated: 2026-09-26
---

# Governance & Compliance

> **Generation marker:** Hardened in v1.3.1 (Tier-2). Operationalises EU AI Act (Regulation (EU) 2024/1689) Articles 9, 12, 13, 14, GDPR Articles 17 and 22, and Italian Law 132/2025.
> **Klarna Test interaction:** No directly (the pack supports the Klarna Test via Article 13 transparency mapping and Article 9 risk management, but does not score).
> **Brain interaction:** Both — reads use-case register, risk register, decision logs; writes compliance reviews, audit trail summaries, erasure documentation.

## 1. Purpose

Operationalises the EU AI Act mapping methodology (`governance/EU-AI-ACT.md`), GDPR compliance disciplines (Articles 17 and 22), Italian Law 132/2025 safeguards, and the legal escalation touchpoints from `docs/06-when-to-call-a-lawyer.md`. Owns the lifecycle of `eu-ai-act-mapping.xlsx` (X7) and the operational standards of the daily EU AI Act Audit Trail Routine (R6).

For organisations operating in the European Union or deploying AI systems affecting EU citizens, adherence to the EU AI Act (Regulation (EU) 2024/1689) is mandatory. As of 2 August 2026, full obligations for Annex III high-risk AI systems apply, with substantial administrative penalties (up to €35 million or 7% of worldwide annual turnover). Non-EU adopting firms also adopt this pack to enforce verifiable operational transparency, tamper-evident audit trails, and defensible human-above-the-loop oversight.

This pack provides concrete procedures for classifying AI systems, maintaining the Article 9 risk register, verifying Article 12 audit-trail immutability, ensuring Article 13 deployer transparency, guaranteeing Article 14 human oversight, enforcing the GDPR Article 17 dual-repo erasure runbook, and preparing audit dossiers for external legal counsel.

## 2. When to invoke this pack

1. **Classifying a new AI system or Skill Pack:** When an AI capability, agent workflow, or Routine is proposed, piloted, or deployed, to map against Annex III risk classifications.
2. **Maintaining the Article 9 Risk Register:** When updating risks, mitigation controls, residual risk acceptance, or owner assignments in X7 (`eu-ai-act-mapping.xlsx`).
3. **Auditing the Daily R6 Routine:** When validating the 23:00 UTC Article 12 audit trail, investigating missing runs, resolving push or cryptographic signing failures, or inspecting logged anomalies.
4. **Conducting a Quarterly Compliance Review:** Every quarter, prior to the end-of-quarter Business Review, synthesizing compliance posture across all active AI use cases into `firm/compliance/quarterly-reviews/YYYY-QX.md`.
5. **Preparing for External Counsel Review:** Compiling the eleven legal touchpoints dossier (`docs/06-when-to-call-a-lawyer.md`) for annual or transaction-specific review by qualified local counsel.
6. **Processing a GDPR Article 17 Erasure Request:** When a departing partner, contractor, or customer requests data deletion, requiring execution of the Curator Shared Brain admin revoke API or Ledger `git filter-repo` protocol.
7. **Responding to a GDPR Article 22 Challenge:** When an affected party inquiries whether a decision (e.g., variable pay calculation or partner selection) was solely automated, requiring extraction of human-signoff evidence.
8. **Conducting an Italian Law 132/2025 Verification:** For firms operating or delivering services in Italy, verifying criminal liability boundaries (Art. 612-quater) and aggravating factor mitigations.

## 3. When NOT to invoke this pack

1. **For day-to-day code review and CI/CD quality gates:** Use **S4 (Code & QA)**; S7 specifies compliance standards for audit trails and gates, but S4 runs the technical testing machinery.
2. **For technical legal drafting of partner operating agreements or customer contracts:** Use **S8 (Legal Operations)**; S7 flags regulatory exposure and coordinates touchpoints, while S8 handles transactional legal operations.
3. **For change-management resistance diagnostics or perception-gap tracking:** Use **S6 (Change Management)**; S7 verifies that human oversight mechanisms exist, while S6 runs the 90-day METR baseline and pilot cohorts.
4. **For scoring or executing the Klarna Test:** Use the Klarna Test workflow (`governance/KLARNA-TEST.md`) and Routine R7; S7 ensures the resulting decisions are logged in the Article 12 trail, but does not calculate Klarna scores.
5. **As a substitute for certified legal counsel:** S7 enforces operational compliance methodology; it never issues formal legal opinions or dispenses jurisdictional legal advice.

## 4. Operational instructions

### 4.1 Use-case classification (Annex III mapping procedure)

Every AI capability (whether an internal routine, agentic skill, customer-facing chatbot, or decision support tool) must be classified prior to production deployment.

```
+-----------------------------------------------------------------------+
| Step 1: Query Use-Case Definition                                     |
| Retrieve name, owner partner_id, affected population, input/output    |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| Step 2: Test Against Prohibited Practices (Article 5)                 |
| Social scoring, biometric categorization, subconscious manipulation?   |
| IF YES: REJECT DEPLOYMENT IMMEDIATELY                                 |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| Step 3: Test Against Annex III High-Risk Categories                   |
| 1. Biometrics  2. Critical infra  3. Education/vocational             |
| 4. Employment, worker management, access to self-employment           |
| 5. Essential private/public services  6. Law enforcement              |
| 7. Migration/asylum  8. Administration of justice/democracy           |
+-----------------------------------------------------------------------+
        |                                               |
  Matched Annex III                               No Annex III Match
        |                                               |
        v                                               v
+--------------------------------+              +-------------------------------+
| Tier: HIGH RISK                |              | Step 4: Test Transparency     |
| Mandatory: Articles 9, 12, 13, |              | Interacts with humans?        |
| 14, and X7 full documentation. |              | Generates synthetic media?    |
+--------------------------------+              +-------------------------------+
                                                        |               |
                                                      YES               NO
                                                        |               |
                                                        v               v
                                                +---------------+ +------------+
                                                | Tier: LIMITED | | Tier:      |
                                                | Mandatory:    | | MINIMAL    |
                                                | Art. 50 /     | | General    |
                                                | disclosures.  | | hygiene.   |
                                                +---------------+ +------------+
```

1. **Execute Step 1 (Intake):** Inspect the proposal or Output Spec. Identify:
   - Unique identifier (`UC-NNN`).
   - System name and description.
   - Operating Partner ID.
   - Affected population (internal partners, candidates, customers, public).
2. **Execute Step 2 (Article 5 Prohibitions Check):** Verify the system does NOT engage in cognitive behavioural manipulation, social scoring, biometric categorization for sensitive attributes, or predictive policing. If any match, flag as **PROHIBITED** and halt adoption.
3. **Execute Step 3 (Annex III Risk Evaluation):** Evaluate against Annex III categories. Note the framework's conservative baseline:
   - **Attribution Agent & Variable Pay Calculator (S3, R1, R3):** Classified as **HIGH RISK** (Annex III, Point 4(b) — AI systems used to make decisions affecting terms of work-related relationships, task allocation, and compensation).
   - **Recruitment & Partner Onboarding Screening (S6, R7, Onboarding kits):** Classified as **HIGH RISK** (Annex III, Point 4(a) — AI systems used for recruitment or selection).
   - **Customer-Facing Autonomous Chatbots / Sales Agents (S9, S11):** Classified as **LIMITED RISK** under Article 50 (transparency required; must disclose AI nature to users).
   - **Internal Knowledge Retrieval & Synthesizer (S1, S2, Curator):** Classified as **MINIMAL RISK** unless piped directly into high-risk decision pipelines without human triage.
   - **Code & QA Assistance (S4):** Classified as **MINIMAL RISK** unless deployed in safety-critical cyber-physical domains.
4. **Record Classification in X7:**
   - In `templates/excel/eu-ai-act-mapping.xlsx` (or firm clone `firm/excel/eu-ai-act-mapping.xlsx`), open sheet `Use_Cases` and append a row with `use_case_id`, `name`, `owner_partner_id`, `brief_description`, `deployment_status`, `affected_population`, and `brain_link`.
   - Open sheet `Annex_III_Risk_Mapping` and write: `annex_iii_category`, `rationale`, `conservative_baseline_tier` (`high`, `limited`, `minimal`, `prohibited`), `counsel_review_status` (`pending`, `reviewed`, `exempt`), `counsel_review_date`.
5. **Commit the Record:** Commit the updated X7 workbook with message `S7: classify use-case UC-NNN (<tier>)`.

### 4.2 Article 9 risk-management system

For every system classified as **HIGH RISK**, the firm must maintain a continuous risk management system running through its entire lifecycle.

1. **Identify Risks:** Identify foreseeable risks across four dimensions:
   - *Technical Risks:* Hallucination, model drift, prompt injection, tool execution failure.
   - *Governance & Legal Risks:* Bias, discrimination, non-compliance with local wage/partner laws, worker misclassification challenge.
   - *Operational Risks:* Shadow refusal, partner alienation, data leakage, single point of failure in signing keys.
   - *Human Agency Risks:* Automation bias, rubber-stamping by overseers, erosion of core partner competencies.
2. **Populate X7 `Article_Obligations` & `Evidence_Trail`:**
   - In `Article_Obligations`, map `use_case_id` against `article_9_status` (`compliant`, `partial`, `not-started`).
   - In `Evidence_Trail`, record:
     - Requirement: "Continuous risk identification and mitigation".
     - `evidence_type`: `brain_page` or `risk_register_row`.
     - `evidence_link`: Path to the system's risk assessment document (e.g., `firm/compliance/risk-assessments/UC-NNN.md`).
     - `last_verified_date`: Current date.
3. **Conduct Quarterly Risk Review:**
   - Review all open high-risk use cases every 90 days.
   - Evaluate whether mitigation controls remain effective.
   - Require written sign-off by the Lead Partner / Founder on all accepted residual risks.
   - File the completed review in the Ledger at `firm/compliance/quarterly-reviews/YYYY-QX.md`.

### 4.3 Article 12 record-keeping and audit trail (R6 invocation)

Article 12 mandates automatic event logging over the entire operational lifecycle for high-risk AI systems. ØØT implements this through **Routine R6 (EU AI Act Audit Trail)** running daily at 23:00 UTC.

1. **Verify R6 Configuration & Prerequisites:**
   - Ensure the firm's Ledger repository enforces the **four immutability controls**:
     - (a) Force-push disabled on default branch (`main`).
     - (b) Branch deletion disabled.
     - (c) Signed commits required (`git commit -S` with GPG or SSH).
     - (d) Path `firm/audit-logs/` treated as append-only.
   - Ensure repository plan-tier meets Article 12 standards: **GitHub Team** minimum (GitHub Free private repos do not enforce branch protection). For EU firms requiring verified GDPR data residency, **GitHub Enterprise Cloud (EU Region)** is required.
2. **Execute or Verify the Daily R6 Run:**
   - Scan all Routine writeback outputs produced in the preceding 24 hours:
     - `firm/output-logs/` (R1 Daily Output Verification)
     - `firm/business-reviews/` (R2 Weekly Business Review agenda)
     - `firm/partners/*/variable-statements/` (R3 Monthly Variable Calc)
     - `firm/partners/*/long-tail-statements/` (R4 Long-Tail Settlement)
     - `firm/compensation/` (R3/R4 founder approvals)
     - `firm/brain-health/` (R5 Weekly Brain Health)
     - `firm/klarna-tests/` (R7 Klarna Test trigger and scoring)
     - `firm/treasury/` (R8 Treasury Runway updates)
   - For each logged decision, compile:
     - `timestamp` (ISO-8601 UTC).
     - `ai_system` (model ID + Skill Pack, e.g., `claude-3-7-sonnet-20250219 + S3`).
     - `use_case_id` (from X7, e.g., `UC-001`).
     - `context_summary` (sanitised prompt / task context with PII redacted).
     - `output_summary` (decision summary, e.g., variable pay recommendation).
     - `human_reviewer` (Partner ID or "Pending sign-off").
     - `annex_iii_category` (e.g., "Point 4(b) Employment/Compensation").
     - `anomaly_flagged` (boolean; `true` if unexpected tool failure, missing sign-off, or unauthorized override).
3. **Format and Commit Audit Trail:**
   - Format entries into `firm/audit-logs/YYYY-MM-DD.md` following `templates/brain/audit-log-day.md`.
   - Update `firm/excel/eu-ai-act-mapping.xlsx` sheet `Audit_Log_Index` with date, path, entry count, and anomalies count.
   - Stage and commit both files in a **single signed commit**:
     ```bash
     git add firm/audit-logs/YYYY-MM-DD.md firm/excel/eu-ai-act-mapping.xlsx
     git commit -S -m "R6: audit trail for YYYY-MM-DD [skip ci]"
     git push origin main
     ```
   - *Never split this commit or commit without cryptographic signing.* An empty day must be recorded as "No agent activity today", never omitted.

### 4.4 Article 13 transparency & instructions for use

Deployers of high-risk AI systems must be provided with clear, accessible instructions for use detailing system capabilities, technical limitations, and required oversight.

1. **Enforce Skill Pack Limitations Section:**
   - In ØØT, every `SKILL.md` serves as the official "instructions for use" for that agentic subsystem.
   - For every high-risk use case, verify that the associated Skill Pack contains an explicit, un-bypassable **Section 8 (Don'ts)** and **Section 3 (When NOT to invoke this pack)**.
2. **Partner Onboarding Transparency Disclosure:**
   - Every partner entering the organisation must receive written documentation during Day 1-30 of onboarding (`templates/partner-onboarding/first-90-days.md`) explaining:
     - How AI agents evaluate and attribute outputs.
     - What model endpoints are utilised.
     - How variable pay calculations are generated.
     - How to inspect the partner's own logged entries in `firm/output-logs/`.
3. **External and Customer Disclosures (Article 50):**
   - For customer-facing interfaces (e.g., Lumina AI web widgets, automated email responders, marketing bots):
     - Ensure prominent notice: *"You are interacting with an AI system deployed by [Firm Name]."*
     - Provide a clear mechanism for escalating to a human partner upon request.

### 4.5 Article 14 human oversight & anti-automation bias

High-risk AI systems must be subject to effective oversight by natural persons. Automated systems are strictly advisory tools; they do not hold legal authority to commit the organisation.

1. **Human-Above-the-Loop Architecture:**
   - Enforce the non-negotiable ØØT principle: **Agents propose, humans decide and authorise.**
   - In Routine R1: Output verification recommends value envelopes; the partner and reviewing partner affirm.
   - In Routine R3: The variable pay script generates *draft statements*; the founding partner must explicitly sign off before treasury funds are released.
   - In Routine R7: The Klarna gate workflow blocks PR merges; human scorers must complete the rubric and attest the score.
2. **Mitigating Automation Bias:**
   - Implement the **mandatory 90-day post-deployment review** (Klarna Test Q9):
     - 90 days after any AI-driven restructuring or deployment, re-measure baseline operational metrics (via S6 METR discipline).
     - Compare self-reported partner productivity against measured throughput. If perception gap > 20 points, trigger a formal review.
   - Check overseer behaviour: If a human approver approves 100% of AI recommendations in under 30 seconds without opening reference files, flag for "oversight complacency / automation bias" in the quarterly compliance review.

### 4.6 GDPR Article 22 solely automated decision avoidance

Article 22 of Regulation (EU) 2016/679 grants individuals the right not to be subject to decisions based solely on automated processing producing legal or similarly significant effects.

1. **Audit Compensation and Disciplinary Decisions:**
   - Review all routines and scripts touching partner compensation, task assignment, or membership standing.
   - Verify that no automated script has write access to banking rails, payment gateways, or equity/token distribution contracts without human multi-signature sign-off.
2. **Establish the Article 22 Defense Dossier:**
   - If a partner or contractor questions an allocation, generate an extract from `firm/audit-logs/` demonstrating:
     - The AI output was advisory.
     - The human reviewer received the draft on date $T_1$.
     - The human reviewer attested and approved the payment on date $T_2$.
     - The partner had access to the Tier-1 dispute resolution mechanism (`governance/DECISION-RIGHTS.md`).
3. **Record Findings in X7:**
   - In sheet `Article_Obligations`, set `gdpr_article_22_status` to `compliant` for all high-risk use cases, linking to the relevant human approval packets in `firm/compensation/`.

### 4.7 GDPR Article 17 right to erasure in dual-repo architecture

Under [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), the firm operates two distinct repositories: the **Ledger** (`<firm>-ledger`) and the **Firm Brain** (`<firm>-brain` via Curator Shared Brain). When a partner, contributor, or customer exercises the right to erasure, execute this two-tier runbook:

```
                          Article 17 Erasure Request
                                      |
              +-----------------------+-----------------------+
              |                                               |
              v                                               v
    [Firm Brain Repository]                         [Ledger Repository]
    (Curator Shared Brain)                           (GitHub Git Tree)
              |                                               |
              v                                               v
  1. Retrieve admin_token from                   1. Evaluate legal retention
     Bitwarden (Founders vault).                    obligations (tax/corporate).
  2. Invoke Curator API:                         2. Redact PII in active files:
     POST /api/sharedbrain/:id/revoke               contracts, customer logs.
     Token: "REVOKE-<fellow_id>"                 3. If absolute erasure ordered
  3. Curator deletes contributions,                 by counsel:
     triggers clean re-synthesis.                   - Run git filter-repo
  4. Verify state/revocation-log.json               - Lift branch protection
  5. Issue Pull advisory to partners                - Force-push signed commit
     to update local mirrors.                       - Re-enable branch protection
              |                                               |
              +-----------------------+-----------------------+
                                      |
                                      v
                  Document Execution in Ledger:
                  firm/compliance/erasure-requests/REQ-YYYY-NNN.md
```

#### Procedure A: Firm Brain Contributor Revocation (Curator Shared Brain)
1. Retrieve the Curator Shared Brain `admin_token` from the founders' Bitwarden vault (per `governance/SECRETS-POLICY.md`).
2. Dispatch an authenticated API request:
   ```bash
   curl -X POST "https://brain.firm-domain.internal/api/sharedbrain/${SHARED_BRAIN_ID}/revoke" \
     -H "Authorization: Bearer ${ADMIN_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "contributor_id": "'"${FELLOW_UUID}"'",
       "confirmation": "REVOKE-'"${FELLOW_UUID}"'"
     }'
   ```
3. Verify that the response returns `HTTP 200 OK` and inspect `state/revocation-log.json` in the Firm Brain repo to confirm the entry is recorded with timestamp and contributor UUID (no personal names).
4. Verify that Curator has triggered a re-synthesis excluding all pages authored by `${FELLOW_UUID}`.
5. Notify all active partners via Slack `#announcements` or 4thtech dChat to execute a `curator pull` to purge cached local copies.

#### Procedure B: Ledger Repository Redaction / Erasure
1. Determine legal retention exemptions: Under GDPR Article 17(3)(b), data necessary for compliance with a legal obligation (e.g., tax, corporate accounting records, invoices) is exempt from immediate destruction. Tax/compensation records in X1 and X2 are preserved for the statutory period (typically 5–10 years depending on EU member state).
2. For personal data not subject to statutory retention (e.g., candidate assessment notes, draft biographies, contact details):
   - Update active files to redact personal identifiers, replacing names with UUID pseudonyms.
3. If complete historical purge is legally required by supervisory authority or court order:
   - Coordinate with legal counsel.
   - Clone a bare copy of the Ledger.
   - Run `git-filter-repo` to scrub the target PII strings or files from git history:
     ```bash
     git-filter-repo --replace-text expressions.txt
     ```
   - Temporarily disable branch protection on `main`.
   - Force push the scrubbed history.
   - Immediately re-enable branch protection, force-push block, and signed commit requirements.
   - Purge secondary backups on PollinationX or cold storage.
4. File the compliance completion certificate in `firm/compliance/erasure-requests/REQ-YYYY-NNN.md`.

### 4.8 Italian Law 132/2025 compliance checks

For organisations operating in Italy or providing services to Italian citizens, Italian Law 132/2025 introduces specific criminal and administrative liabilities for AI utilization.

1. **Verify Criminal Boundaries (Art. 612-quater Codice Penale):**
   - Strictly prohibit the generation, modification, or dissemination of synthetic audio/video or images depicting real individuals without explicit, written, verifiable consent.
   - Any synthetic media used in marketing (S9) or client comms (S11) must carry permanent, conspicuous digital watermarking and clear textual warnings.
2. **Aggravating Circumstances Awareness:**
   - Under Law 132/2025, offenses committed through the intentional use of AI systems carry statutory sentence enhancements.
   - Audit all automated sales, marketing, and market-intelligence workflows to guarantee no deceptive practices, unauthorized data harvesting, or automated defamatory assertions occur.
3. **Document Italian Jurisdiction Status:**
   - In X7 `Annex_III_Risk_Mapping`, flag any use case operating in Italy with a special compliance tag `IT_LAW_132_APPLIES`.

### 4.9 Quarterly compliance review & annual counsel preparation

Compliance is an ongoing discipline, not a one-time audit. S7 coordinates the preparation of compliance reviews and external legal dossiers.

1. **Quarterly Review Workflow (End of Q1, Q2, Q3, Q4):**
   - Run openpyxl query on X7: inspect `Use_Cases`, `Annex_III_Risk_Mapping`, `Article_Obligations`, and `Audit_Log_Index`.
   - Check total AI decisions logged in R6 for the quarter.
   - Check total anomalies flagged and verify every anomaly was resolved.
   - Draft `firm/compliance/quarterly-reviews/YYYY-QX.md` containing:
     - Active high-risk use cases and their Article 9/12/13/14 status.
     - Review of human oversight logs and sign-off timestamps.
     - Status of GDPR Article 17 revocation requests.
     - Identified regulatory changes in EU or national legislation.
   - Submit quarterly report to the Friday Business Review (R2).
2. **Annual Counsel Review Dossier (The Eleven Legal Touchpoints):**
   - Compile the formal dossier referencing `docs/06-when-to-call-a-lawyer.md`:
     - *Touchpoint 1:* Worker classification evidence (Partner Charters, decision rights).
     - *Touchpoint 2:* Variable pay legality (X1/X2 base vs variable split).
     - *Touchpoint 3:* Profit-share & entity governance.
     - *Touchpoint 4:* Stablecoin payroll compliance (Gen 2 readiness).
     - *Touchpoint 5:* Long-tail revenue entitlement classification (securities analysis).
     - *Touchpoint 6:* Internal Unit Fund status (mandatory if Gen 2 Unit Fund is active).
     - *Touchpoint 7:* EU AI Act Articles 9, 12, 13, 14 conformance evidence.
     - *Touchpoint 8:* GDPR Article 22 human-above-the-loop audit trail.
     - *Touchpoint 9:* GDPR Article 17 erasure runbook verification.
     - *Touchpoint 10:* Italian Law 132/2025 checks (if applicable).
     - *Touchpoint 11:* Cross-border tax and VAT handling on autonomous outputs.
   - Commit the signed counsel opinion letter to `firm/compliance/counsel-reviews/YYYY-MM-DD.md`.

## 5. Brain interaction protocol

Per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md), compliance evidence and regulatory records live in the **Ledger** (signed-commit audit trail), whereas high-level compliance *knowledge*, architectural choices, and institutional policies live in the **Firm Brain**.

### Reads (Ledger)
- `firm/audit-logs/*.md`: Daily R6 Article 12 records.
- `firm/klarna-tests/*.md`: Klarna Test records and human attestation logs.
- `firm/output-logs/*.md`: Output logs for attribution and rework tracking.
- `firm/compensation/*.md`: Monthly variable pay founder approval packets.
- `firm/excel/eu-ai-act-mapping.xlsx`: The X7 compliance workbook.

### Reads (Firm Brain — Shared Brain mirror)
- `entities/decisions/*`: Architectural Decision Records and governance policies touching compliance.
- `entities/policies/*`: Firm-level policies on data protection, acceptable AI use, and secrets management.

### Writes (Ledger only)
- `firm/audit-logs/YYYY-MM-DD.md`: Daily audit trail generated by R6.
- `firm/compliance/quarterly-reviews/YYYY-QX.md`: Formal quarterly compliance reviews.
- `firm/compliance/risk-assessments/UC-NNN.md`: In-depth Article 9 risk management evaluations.
- `firm/compliance/counsel-reviews/YYYY-MM-DD.md`: Counsel review documentation and legal opinions.
- `firm/compliance/erasure-requests/REQ-YYYY-NNN.md`: GDPR Article 17 execution records.

### Wikilink Discipline
- When writing markdown pages in the Ledger or proposing pages for the Firm Brain, only link to verified existing slugs.
- Never invent speculative links.
- Cross-references to spreadsheets use relative repo paths (e.g., `[[../excel/eu-ai-act-mapping.xlsx]]` or explicit markdown links `[eu-ai-act-mapping.xlsx](../excel/eu-ai-act-mapping.xlsx)`).

## 6. Excel interaction protocol

Per [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md), Excel workbook mutations by Routines occur via **openpyxl execution inside code execution on the local Ledger clone on BOTH cloud and privacy tracks**. There is no Google Sheets or hosted cloud spreadsheet API in the Routine write path. The `mcp__excel__*` tools listed in frontmatter are strictly for human-in-the-loop interactive inspection and patching at a partner's workstation.

### X7 `eu-ai-act-mapping.xlsx` Sheet Architecture

| Sheet | Purpose | Operation | Trigger | Write Mechanism |
|---|---|---|---|---|
| `Use_Cases` | Inventory of all firm AI systems | Append / Update | New AI system proposal or tier change | Python `openpyxl` / Manual |
| `Annex_III_Risk_Mapping` | Annex III classification & counsel sign-off | Write / Update | Classification review or counsel review | Python `openpyxl` / Counsel review |
| `Article_Obligations` | Status of Art 9, 12, 13, 14, and GDPR Art 22 | Write / Update | Quarterly review or system hardening | Python `openpyxl` / S7 audit |
| `Evidence_Trail` | Granular pointers to files, routines, and pages | Append / Update | Evidence generation | Python `openpyxl` / S7 audit |
| `Audit_Log_Index` | Index of daily R6 audit logs and anomalies | Append daily | Daily R6 routine run at 23:00 UTC | Routine R6 via `openpyxl` |
| `README` | Governance disclaimer and operating instructions | Read-only | Initial template generation | Locked |

### Appended-Row Contract — `Audit_Log_Index` (R6)
When Routine R6 appends to sheet `Audit_Log_Index`, it MUST write literal values for:
- Column A: `date` (`YYYY-MM-DD`).
- Column B: `audit_log_path` (relative repo path, e.g., `firm/audit-logs/2026-09-26.md`).
- Column C: `entries_count` (integer $\ge 0$).
- Column D: `anomalies_flagged` (integer $\ge 0$).

Both the markdown page `firm/audit-logs/YYYY-MM-DD.md` and the updated `eu-ai-act-mapping.xlsx` must be committed together in a single signed git commit.

## 7. Routine integration

- **R6 (EU AI Act Audit Trail):** Primary routine owned by S7. Fires daily at 23:00 UTC (cloud: Claude Code Routine; privacy: local cron `0 23 * * *`). Inspects all daily Ledger writebacks, writes `firm/audit-logs/YYYY-MM-DD.md`, updates X7 `Audit_Log_Index`, and pushes a signed commit to `main`.
- **R2 (Weekly Business Review):** S7 contributes the quarterly compliance posture and any open audit anomalies to the Friday Business Review agenda.
- **R7 (Klarna Test Trigger):** Coordinates with S7 to ensure that every high-risk automation PR triggering the Klarna gate is recorded in X7 `Use_Cases` and properly captured in the Article 12 audit trail.

## 8. Don'ts

1. **Don't treat compliance as a one-time checklist;** it is a continuous, living operational discipline requiring daily audit logging and quarterly reviews.
2. **Don't bypass the daily R6 audit trail;** an unlogged day constitutes a regulatory non-compliance event under Article 12. If no decisions occurred, log "No agent activity today".
3. **Don't downgrade to unsigned git commits;** if cryptographic signing keys are unavailable or branch protection fails, retry and escalate to the founder; never push an unsigned audit log.
4. **Don't claim formal EU AI Act or GDPR compliance without qualified local legal counsel review;** S7 provides the operational scaffolding, not legal certification.
5. **Don't permit automated payment or disciplinary execution without human-above-the-loop sign-off;** fully automated execution violates GDPR Article 22 and EU AI Act Article 14.
6. **Don't update the X7 Risk Register without an audit-trailed git commit;** every change to risk status, owner, or mitigation must identify who updated it and why.
7. **Don't auto-publish Article 13 transparency notices or external regulatory filings without founder and counsel approval.**
8. **Don't execute destructive git history rewriting (`git filter-repo`) for Article 17 requests without counsel guidance and verified backup isolation.**
9. **Don't run compliance audit trails on GitHub Free private repositories;** Article 12 immutability guarantees require branch protection, which is only enforced on GitHub Team or Enterprise.

## 9. Quick reference

| Situation | Immediate Action | Primary Tool / Routine | Output Artifact |
|---|---|---|---|
| New AI system proposed | Map against Article 5 and Annex III; classify tier | S7 §4.1 + openpyxl | X7 `Use_Cases` & `Annex_III_Risk_Mapping` |
| Daily 23:00 UTC audit run | Collect daily decisions; redact PII; verify sign-offs | Routine R6 | `firm/audit-logs/YYYY-MM-DD.md` + X7 update |
| R6 signing failure | Stop; do not push unsigned; alert `#ops`; retry key | Git CLI + GPG/SSH | GPG signed commit on `main` |
| Audit anomaly flagged | Investigate root cause; review prompt/code; log remediation | S7 §4.3 + S4 | `firm/compliance/incidents/INC-YYYY-NNN.md` |
| End-of-quarter review | Audit all open use cases; evaluate Article 9 mitigations | S7 §4.9 + openpyxl | `firm/compliance/quarterly-reviews/YYYY-QX.md` |
| Annual counsel prep | Compile the 11 touchpoints dossier from docs/06 | S7 §4.9 + S8 | `firm/compliance/counsel-reviews/YYYY-MM-DD.md` |
| Departing partner Article 17 | Invoke Curator Shared Brain admin revoke API | `POST /api/sharedbrain/:id/revoke` | `state/revocation-log.json` + clean synthesis |
| Ledger PII erasure ordered | Run `git filter-repo` under counsel direction; force push | Git CLI + filter-repo | `firm/compliance/erasure-requests/REQ-NNN.md` |

## 10. References

1. **Regulation (EU) 2024/1689 of the European Parliament and of the Council (EU Artificial Intelligence Act).** Official Journal of the European Union, L 2024/1689, 12 July 2024. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689. (Mandatory obligations for Annex III high-risk AI systems, Articles 9, 12, 13, 14, and Article 50 transparency).
2. **Regulation (EU) 2016/679 (General Data Protection Regulation — GDPR).** Official Journal of the European Union, L 119, 4 May 2016. Articles 17 (Right to Erasure) and 22 (Automated Individual Decision-Making, including Profiling). https://eur-lex.europa.eu/eli/reg/2016/679/oj.
3. **Italian Republic, Law No. 132/2025 on Artificial Intelligence.** Gazzetta Ufficiale della Repubblica Italiana, 23 September 2025 (in force 10 October 2025). Introduces Art. 612-quater Codice Penale regarding illicit diffusion of AI-generated synthetic content and aggravating criminal factors.
4. **European Data Protection Board (EDPB).** *Guidelines on Automated individual decision-making and Profiling for the purposes of Regulation 2016/679* (WP251rev.01). https://edpb.europa.eu/.
5. **National Institute of Standards and Technology (NIST).** *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* (NIST AI 100-1, January 2023). https://doi.org/10.6028/NIST.AI.100-1.
6. **International Organization for Standardization (ISO) / International Electrotechnical Commission (IEC).** *ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system.* https://www.iso.org/standard/81230.html.
7. ØØT [`governance/EU-AI-ACT.md`](../../governance/EU-AI-ACT.md) — The canonical mapping methodology for the framework.
8. ØØT [`governance/DECISION-RIGHTS.md`](../../governance/DECISION-RIGHTS.md) — Three-tier governance and human authority matrices.
9. ØØT [`docs/06-when-to-call-a-lawyer.md`](../../docs/06-when-to-call-a-lawyer.md) — The eleven legal touchpoints requiring qualified local counsel.
10. ØØT [`templates/excel/SPEC.md`](../../templates/excel/SPEC.md) — Canonical specification for `eu-ai-act-mapping.xlsx` (X7).
11. ØØT [`routines/SPEC.md`](../../routines/SPEC.md) — Operational specifications for Routine R6 (EU AI Act Audit Trail) and R7 (Klarna Test Trigger).
12. ØØT [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md) and [`docs/internal/ADR-002-firm-brain-curator-shared-brain.md`](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md) — Architectural decisions establishing the dual-repo model and openpyxl writeback discipline.

## Acceptance criteria for this SKILL.md

- All sections 1–10 present and fully articulated with concrete operational guidance.
- Frontmatter passes `scripts/validate_skills.py` with zero errors or warnings (`tier: 2`, `status: hardened`, `oot_status: hardened`).
- Zero incomplete or placeholder markers present in the text.
- Every tool referenced in operational instructions is present in `allowed_tools` or belongs to the standard git/Python execution runtime.
- Exact operational protocols provided for EU AI Act Articles 9, 12, 13, 14, GDPR Articles 17 and 22, and Italian Law 132/2025.
- At least 3 detailed worked examples located in `examples/`.
- Dedicated references README located in `references/README.md`.
