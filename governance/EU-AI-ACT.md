# EU AI Act — Mapping Methodology

This document specifies how an ØØT-adopting organisation in EU jurisdiction maps its use of AI to the obligations of the EU Artificial Intelligence Act (Regulation (EU) 2024/1689). It is a methodology, not legal advice. Every EU-operating organisation must engage local counsel; this document tells counsel where to look.

The companion spreadsheet is `templates/excel/eu-ai-act-mapping.xlsx`. The Skill Pack that operationalises the mapping is `skills/governance-compliance/` (Tier 2, scaffolded in v1.0, hardened in v1.x).

---

## Timeline

The EU AI Act applies in stages:

- **1 August 2024.** Act enters into force.
- **2 February 2025.** Prohibitions on unacceptable-risk AI systems and AI literacy obligations apply.
- **2 August 2025.** Obligations for general-purpose AI (GPAI) models apply.
- **2 August 2026.** Most remaining obligations apply, including high-risk AI system obligations under Annex III.
- **2 August 2027.** Full GPAI back-compatibility obligations apply.

ØØT v1.0 ships in 2026 — meaning EU-operating adopters are within one year of the most consequential deadline. The Governance & Compliance Skill Pack and `eu-ai-act-mapping.xlsx` exist primarily to prepare for this.

---

## Risk classification methodology

The EU AI Act assigns AI systems to one of four risk tiers:

1. **Unacceptable risk** (prohibited from 2 February 2025): social scoring by public authorities, real-time biometric identification in public spaces (with narrow exceptions), AI exploiting vulnerabilities of specific groups, etc.
2. **High risk** (full obligations from 2 August 2026): the systems listed in Annex III. Includes AI systems used for: employment / worker management decisions; access to education and vocational training; access to essential private and public services; law enforcement; migration and border control; administration of justice and democratic processes.
3. **Limited risk** (transparency obligations only): chatbots that interact with humans, AI-generated content that could be mistaken for authentic.
4. **Minimal risk** (no specific obligations): everything else.

### ØØT use cases and likely risk classification

The following ØØT components are likely to be classified as **high risk** under Annex III in EU adoption, requiring full Article 9, 12, 13, 14 compliance:

- **Attribution agent + variable pay calculator.** AI used for "decisions affecting access to and terms of employment" (Annex III, point 4). The attribution agent's outputs feed compensation; this falls within scope.
- **Klarna Test gating + Routine R7.** AI used in "decisions on recruitment or selection" or related employment-management decisions, even when AI is in a *gating* role. The mapping is conservative; counsel should confirm.
- **Onboarding Skill (P4).** AI used in partner-onboarding workflows, particularly if it screens or assesses candidates.

The following are likely **limited risk** (transparency obligations only):

- **Lumina AI widget (S11).** Customer-facing chatbot. Article 50 transparency: customers must know they are interacting with AI.
- **Brain query interface.** Internal-facing, not a "decision" system; transparency obligation only if it could be mistaken for human authorship.

The following are likely **minimal risk** (no specific obligations):

- The Brain itself (storage and retrieval of internal knowledge).
- Code & QA assistance (Claude Code, Augment Code). Note: this could change if the assistance is used in safety-critical code domains — counsel.
- Reporting and Business Review automation.

**Important caveat:** classifications depend on the specific use, the population affected, and the consequence of the AI's outputs. The mapping above is the framework's *baseline assumption*; every EU adopter must verify with counsel.

---

## Article-by-article obligations for high-risk systems

The four articles ØØT explicitly maps:

### Article 9 — Risk Management System

**Obligation:** Establish, implement, document, and maintain a risk management system across the AI system's lifecycle. Identify, evaluate, and mitigate foreseeable risks.

**ØØT mapping:**

- The Klarna Test (`governance/KLARNA-TEST.md`) is the framework's primary risk management discipline for the deployment-decision phase.
- The METR baseline (Change Management Skill Pack) is the framework's primary discipline for the operational-quality phase.
- The decision rights matrix (`governance/DECISION-RIGHTS.md`) specifies who is responsible for risk decisions at each tier.
- `eu-ai-act-mapping.xlsx`, sheet "Risk Register," captures identified risks per use case, mitigation status, owner, review date.

**Adopter actions:**
- Populate the Risk Register sheet for each high-risk use case.
- Schedule quarterly review (Routine R6 logs the cadence).
- Document the residual risks accepted by the founder.

### Article 12 — Record-Keeping (Logging)

**Obligation:** High-risk AI systems must automatically log events relevant to risk and oversight. Logs must be retained for an appropriate period (commonly read as 6 months minimum, longer for systems with longer feedback cycles).

**ØØT mapping:**

- Routine R6 (EU AI Act Audit Trail) is the framework's primary logging mechanism. Runs daily at 23:00. Appends to a markdown audit log committed to the Brain.
- The audit log captures: AI system identifier, decision context, input summary (sanitised for PII), output, human reviewer if any, timestamp.
- **Practical immutability is provided by three combined controls** on the Brain repo's audit branch (typically `main`): (a) force-push disabled; (b) deletion disabled; (c) signed commits required (GPG or SSH); (d) audit log paths under `firm/audit-logs/` are append-only by convention. Plain `git history` alone is **not** immutable — force-push can rewrite history — so the controls above must be configured at the GitHub repo level. The cloud installer (Phase 9) and the Code & QA SKILL.md (S4) document the configuration. Generation 2 introduces external anchoring (daily SHA-256 of the audit log committed to a public ledger or service) for adopters who require stronger guarantees.

**Adopter actions:**
- Confirm R6 is configured and running for every high-risk use case.
- Configure branch protection on the audit branch with the three controls above before relying on the Article 12 retention claim.
- Set retention policy (default: indefinite via git; archive older than 12 months to PollinationX cold storage on privacy track).
- Document the logging in the Risk Register.

### Article 13 — Transparency and Provision of Information to Deployers

**Obligation:** High-risk systems must be designed so users (deployers) can interpret outputs and use them appropriately. Instructions for use must specify capabilities, limitations, and required human oversight.

**ØØT mapping:**

- Every Skill Pack (`SKILL.md`) is, in EU AI Act terms, an "instruction for use" of the underlying AI system. The Tier-1 hardened packs include explicit "limitations" sections specifying where the Skill is not to be relied upon.
- The Klarna Test mandatory rubric is the framework's primary transparency-of-limitation mechanism: the test forces the deployer to think through what the AI cannot do.
- The Compensation & Attribution Skill Pack explicitly states the attribution agent's outputs are *advisory* and require monthly human sign-off (per Q5 of the Klarna Test rubric on consultation).

**Adopter actions:**
- For each high-risk Skill Pack, confirm the limitations section is current and accurate.
- Provide every partner with the relevant Skill Pack documentation at onboarding.
- Document transparency provision in the Risk Register.

### Article 14 — Human Oversight

**Obligation:** High-risk AI systems must be designed to enable effective oversight by natural persons during the period in which the system is in use. Oversight measures shall enable humans to: understand capabilities and limitations; remain aware of automation bias; correctly interpret outputs; decide not to use the output; intervene or interrupt operation.

**ØØT mapping:**

- The variable pay calculator's outputs require *monthly human sign-off* before payment per the Compensation & Attribution Skill Pack. The attribution agent does not pay; the founder (or designated human approver) pays.
- The Klarna Test gates any "AI replaces human" decision with a human-scored rubric.
- Routine R7 blocks merges, not just warns — humans must sign off.
- The 90-day post-deployment review (Klarna Test Q9) is the framework's primary mechanism for catching automation bias retroactively.

**Adopter actions:**
- For each high-risk use case, document the specific human oversight mechanism.
- Train designated overseers on the system's known failure modes (the Skill Pack's limitations section).
- Schedule the 90-day reviews in the operational calendar.

---

## GDPR Article 22 — Solely Automated Decisions

**Obligation:** Data subjects (in ØØT context: partners, customers, candidates) have the right not to be subject to a decision based *solely* on automated processing — including profiling — that produces legal or similarly significant effects.

**ØØT mapping:**

The framework's variable pay calculations and Klarna Test gating both have potential Article 22 implications. ØØT's design response:

- **Variable pay decisions are never solely automated.** Routine R3 (Monthly Variable Calc) produces a *draft* that is sent to each partner for review and to the founder for sign-off. The actual payment requires human authorisation. This is a deliberate design choice, not an accident.
- **Klarna Test scoring is human-driven.** The rubric is filled in by humans. Routine R7 *triggers* the scoring; it does not *score*. Score-of-record is human-attested.
- **The audit trail (R6) demonstrates the human-above-the-loop pattern** for any GDPR Article 22 challenge or supervisory authority inquiry.

**Adopter actions:**
- Confirm no Routine in your organisation's deployment makes a final decision affecting partner compensation without human sign-off.
- If you customise R3 to auto-pay, document the legal basis and inform partners.

---

## Italian Law 132/2025 — leading indicator

Italian Law 132/2025, in force from October 2025, created criminal AI offences with fines up to ~€775,000 and corporate disqualification for certain violations. While Italian law applies only in Italy, the framework's authors view it as a leading indicator of EU-wide enforcement seriousness — particularly for organisations operating in multiple EU member states.

**Adopter actions if operating in Italy:**
- Map AI uses against the specific offences defined in Law 132/2025 (with counsel).
- The conservative posture is to assume any high-risk-classified use in Italy will face material liability for Article 12 / 13 / 14 non-compliance, in addition to the standard fines under the EU AI Act itself.

---

## How to use the eu-ai-act-mapping.xlsx

The spreadsheet has six sheets, populated per use case:

1. **Use_Cases.** Every AI system used in the org. Name, owner, brief description, deployment status.
2. **Annex_III_Risk_Mapping.** For each use case, the Annex III category (if any), the rationale, and the conservative-baseline tier (high / limited / minimal).
3. **Article_Obligations.** For each high-risk use case, the specific Article 9/12/13/14 obligations and the ØØT mapping row from this document.
4. **Evidence_Trail.** Per obligation, the evidence reference: Skill Pack section, Routine ID, Brain page, Risk Register row.
5. **Audit_Log_Index.** Pointers into the daily R6 audit log markdown files.
6. **README.** Self-explanatory.

The recommended cadence is: populate at adoption, review monthly with the Governance & Compliance Skill Pack, comprehensive review quarterly, full counsel review annually.

---

## Final note: this document is not enough

This document maps four articles in detail. The EU AI Act has 113 articles. Many other obligations (conformity assessment, post-market monitoring, registration in the EU database for high-risk systems, fundamental rights impact assessment for certain deployers) are not mapped here.

The framework provides the operational scaffolding to *engage* the EU AI Act seriously. It does not provide the legal expertise to *navigate* it comprehensively. EU-operating adopters must engage qualified counsel before, during, and after adoption. This document tells counsel where to start; counsel finishes the job.