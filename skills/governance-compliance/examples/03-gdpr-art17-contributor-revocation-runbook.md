# Example 3 — GDPR Article 17 Contributor Revocation in Dual-Repo Architecture

A complete worked example of executing a GDPR Article 17 ("Right to Erasure") request for a departing contributor, managing the boundary between the Firm Brain (Curator Shared Brain) and the Ledger (`<firm>-ledger`) under ADR-002, and maintaining statutory accounting records under GDPR Article 17(3)(b).

## The setup

- **Firm:** Apex Vanguard (8-partner advisory firm operating between Munich, Germany and Zagreb, Croatia).
- **Data Subject:** Dr. Aris V. (external specialist advisor, partner identifier `P-007`, Curator contributor UUID `contrib-8841-f92e`).
- **Trigger:** On 2026-07-10, Dr. Aris concludes his advisory engagement and delivers a formal legal notice requesting the complete erasure of all personal data, wiki contributions, notes, and profile documents under GDPR Article 17.
- **Statutory Deadline:** 30 days (10 August 2026).

---

## Phase 1 — Legal scoping & architectural separation (§4.7)

The firm's Compliance Lead (Mirjana S., `P-002`) invokes S7: *"Dr. Aris V. has exercised his GDPR Article 17 right to erasure. Run the dual-repo scoping and execution protocol."*

S7 analyzes the request against the firm's architecture:

### 1. Firm Brain Scoping (`<firm>-brain` via Curator Shared Brain)
- **Data Held:** 14 technical research summaries, 6 architecture proposals, and personal contribution notes authored by `contrib-8841-f92e`.
- **Legal Assessment:** Purely collaborative intellectual property and working notes. No statutory corporate retention requirement applies.
- **Action:** Full immediate revocation via Curator Shared Brain API.

### 2. Ledger Repository Scoping (`<firm>-ledger`)
- **Data Held:**
  - `firm/partners/advisors/aris-v.md` (Contact information, biographical details, private bank IBAN).
  - `firm/excel/partner-output-ledger.xlsx` (X1) Output_Log (8 approved advisory outputs with compensation vouchers totaling €18,400).
  - `firm/excel/reward-species-declaration.xlsx` (X2) Base_Variable_Split (`partner_id: P-007`).
- **Legal Assessment (GDPR Article 17(3)(b)):**
  - Personal contact info and bios: **Must be erased**.
  - Financial, tax, and compensation vouchers: **Exempt from erasure**. German Commercial Code (HGB §257) and Slovenian Tax Procedure Act (ZDavP-2) require retention of accounting records and vouchers for 10 years.
- **Action:** Pseudonymize personal records; replace personal identifiers with `P-007 (Archived Advisor)`; preserve accounting numbers.

---

## Phase 2 — Firm Brain revocation execution

Mirjana follows the S7 §4.7.1 runbook:

1. **Retrieve Admin Token:** Mirjana accesses the firm's founders' Bitwarden vault and retrieves the Curator `admin_token`.
2. **Execute Curator Admin Revoke:**
   ```bash
   curl -X POST "https://brain.apex-vanguard.internal/api/sharedbrain/apex-shared-v1/revoke" \
     -H "Authorization: Bearer ${CURATOR_ADMIN_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "contributor_id": "contrib-8841-f92e",
       "confirmation": "REVOKE-contrib-8841-f92e"
     }'
   ```
3. **Verify Execution Response:**
   ```json
   {
     "status": "success",
     "revoked_contributor_id": "contrib-8841-f92e",
     "purged_payloads": 14,
     "resynthesis_triggered": true,
     "timestamp": "2026-07-11T09:14:22Z"
   }
   ```
4. **Audit Log Inspection:**
   Mirjana inspects `state/revocation-log.json` in the Firm Brain repo. The entry confirms:
   ```json
   {
     "action": "revoke_contributor",
     "contributor_id": "contrib-8841-f92e",
     "timestamp": "2026-07-11T09:14:22Z",
     "admin_auth": "token-hash-e8f1"
   }
   ```
   No personal names or identifiable text are retained in the log.
5. **Partner Cache Invalidation Advisory:**
   Mirjana posts to the firm's internal comms channel:
   > 📢 **Notice:** Contributor `contrib-8841-f92e` has concluded their term. Please run `curator pull` in your terminal today to refresh your local collective domain.

---

## Phase 3 — Ledger repository redaction & pseudonymization

Mirjana executes the statutory redaction protocol in the Ledger repository:

1. **Redact Advisor Profile:**
   - File `firm/partners/advisors/aris-v.md` is deleted.
   - A redacted placeholder is created at `firm/partners/archived/P-007.md`:
     ```markdown
     ---
     partner_id: P-007
     role: former-technical-advisor
     tenure: 2025-11-01 to 2026-06-30
     status: departed
     gdpr_status: erased-redacted-2026-07-11
     ---
     # Partner P-007 (Archived)
     Personal details and contact identifiers erased per GDPR Article 17 request REQ-2026-012.
     Statutory compensation and tax records preserved pursuant to GDPR Article 17(3)(b) and HGB §257.
     ```
2. **Preserve Accounting Ledger Integrity:**
   - In `partner-output-ledger.xlsx` (X1), row entries for `P-007` remain unchanged. The `partner_id` `P-007` serves as a synthetic foreign key, preserving financial totals without displaying Aris's personal name.
3. **Commit Redaction:**
   ```bash
   git add firm/partners/ firm/compliance/
   git commit -S -m "S7: execute GDPR Article 17 redaction for former advisor P-007 per REQ-2026-012"
   git push origin main
   ```

---

## Phase 4 — Compliance certificate and data subject closure

1. S7 drafts the formal compliance certificate at `firm/compliance/erasure-requests/REQ-2026-012.md`:
   - Request ID: `REQ-2026-012`
   - Data Subject: Dr. Aris V.
   - Date Received: 2026-07-10
   - Date Executed: 2026-07-11 (within 24 hours of receipt)
   - Firm Brain Action: Complete revocation via Curator API; 14 payload documents purged; re-synthesis verified.
   - Ledger Action: Contact details erased; biographical files scrubbed; statutory tax vouchers preserved under Art. 17(3)(b).
2. S7 generates the formal response letter sent via secure PDF to Dr. Aris V. explaining the dual-repo procedure, confirming the purge of the Firm Brain, and citing the statutory retention requirement for financial records.
3. In `eu-ai-act-mapping.xlsx` (X7), sheet `Evidence_Trail` is updated with row pointing to `REQ-2026-012.md`.

---

## The outcome

- Complete compliance with GDPR Article 17 accomplished in 24 hours.
- Zero risk of criminal or civil tax penalties for premature destruction of financial records.
- The Firm Brain collective knowledge graph was immediately scrubbed and regenerated without broken wikilinks or orphaned payload fragments.
- When Routine R6 runs at 23:00 UTC, it records the compliance operation in `firm/audit-logs/2026-07-11.md`, completing the defensible Article 12 paper trail.
