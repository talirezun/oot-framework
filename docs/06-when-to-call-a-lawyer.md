# 06 — When to Call a Lawyer

**Audience:** Every founder. Every partner. Especially everyone who is about to sign anything.
**Time:** 20 minutes to read; weeks/months to actually engage counsel for the matters identified.
**You will end with:** a clear map of the eleven jurisdiction-specific legal touchpoints where local counsel is mandatory.

---

> ⚠️ **The framework's strongest disclaimer applies to this document.** ØØT is a framework. It points at landmines; it does not defuse them. **Local counsel is mandatory before adoption in any jurisdiction.** The framework's authors take no responsibility for outcomes of adoption without counsel.

---

## What this is + the first 5 minutes

ØØT operates at the intersection of partnership law, employment law, securities law, AI regulation, and (Generation 2) crypto regulation. **All of these vary materially by jurisdiction.** The framework deliberately does not provide legal advice; it provides a structured map of where legal advice is mandatory.

This document lists **eleven legal touchpoints** the framework cannot defuse. Engage counsel **before** signing the first Partner Charter; engage counsel **continuously** as the framework's generations advance.

If your firm operates in multiple jurisdictions (e.g. an EU-based firm with US customers, or a Slovenian d.o.o. with a Croatian sister entity), each jurisdiction's counsel is required separately.

---

## The eleven touchpoints

### 1. Worker classification — partner vs. employee

**Why it matters:** the framework's defining choice (partners not employees) is enforceable only if local law recognises the partnership-style structure. Misclassification can expose the firm to retroactive employment liability, social charges, and tax penalties.

**What ØØT provides:**
- Partner Charter template (per-cohort variations: full-time partner, project specialist, advisor).
- Reward Species Declaration with cohort designation field.
- Decision Rights matrix (`governance/DECISION-RIGHTS.md`) defining authority structure consistent with partnership.

**What ØØT does NOT provide:**
- Jurisdictional analysis of worker-classification factors.
- Defence against re-classification challenge.
- Adaptation of Partner Charter to local language requirements.

**Trigger questions for counsel:**
- Does this jurisdiction recognise our partner-not-employee classification?
- What factors does the local court / authority weight in re-classification disputes?
- What's our specific risk profile?

**Indicative cost:** €2-5k for initial review; €1-2k per partner for ongoing risk monitoring.

---

### 2. Variable pay legality

**Why it matters:** some jurisdictions require minimum guaranteed wage; others disallow output-only pay structures. The framework's seven-layer compensation (base + variable + long-tail + bonus + Gen 2 layers) intersects local wage laws.

**What ØØT provides:** the structure (base_amount + variable_weights + bonus_splits in the Reward Species Declaration).

**What ØØT does NOT provide:** verification that the structure is compliant in the partner's jurisdiction.

**Trigger questions:**
- Is our base_amount above the local minimum guarantee?
- Is the variable structure compatible with local wage-protection law?
- Are there mandatory thirteenth-month / vacation-pay rules that affect our calculations?

**Indicative cost:** €1-3k initial review; renegotiation costs separately.

---

### 3. Profit-share structures + entity choice

**Why it matters:** how the firm is incorporated (LLC, GmbH, S.r.l., d.o.o., LLP, etc.) determines what compensation forms are legally available, what tax treatment applies, and what governance is required.

**What ØØT provides:** the operational discipline assuming the entity exists.

**What ØØT does NOT provide:** entity formation, governance documents (operating agreement, articles), registration.

**Trigger questions:**
- What entity type best fits our partner-distribution model?
- What governance requirements does our entity type impose (board, audit committee, etc.)?
- What's the tax treatment of partner distributions vs. salary?

**Indicative cost:** €5-15k for entity formation; ongoing compliance varies.

---

### 4. Crypto payroll (Generation 2 readiness)

**Why it matters:** most jurisdictions allow stablecoin payroll as a *supplement* to FIAT (per partner consent), not as a *replacement*. AML/KYC implications. Tax treatment of crypto receipts.

**What ØØT provides:** the Gen 2 stablecoin upgrade path; per-partner preference field in X2.

**What ØØT does NOT provide:** the legal verification that the upgrade is compliant for the partner's jurisdiction.

**Trigger questions:**
- Can we pay partner X in USDC/EURC under local law?
- What AML/KYC checks are required?
- How is crypto receipt taxed for the partner?

**Indicative cost:** €2-4k per jurisdiction for initial verification.

---

### 5. Long-tail entitlements (securities-law implications)

**Why it matters:** when long-tail entitlement is "a percentage of revenue from a specific output", many jurisdictions classify this as a security or revenue-share arrangement requiring registration / disclosure.

**What ØØT provides:** the Long_Tail_Schedule sheet in X2; the Ledger page convention; quarterly settlement via R4.

**What ØØT does NOT provide:** securities-law analysis. **This is the most legally-fraught compensation layer.**

**Trigger questions:**
- Does our long-tail structure constitute a security under local law?
- What disclosure / registration is required?
- What's the tax treatment for the partner and the firm?

**Indicative cost:** €5-10k for initial structuring; ongoing for material changes.

---

### 6. Internal Unit Fund (Gen 2 securities offering)

**Why it matters:** the Unit Fund — the firm's internal open-ended fund of units, dividend-paying, with bid/ask liquidity — is **explicitly a securities offering** in most jurisdictions. Registration with local securities regulator likely required.

**What ØØT provides:** the model + the X8 treasury-runway tracker + the YOLO model's reserve discipline.

**What ØØT does NOT provide:** any of the legal infrastructure.

**Trigger questions:**
- What's our jurisdiction's registration requirement?
- What's the cost of compliance (annual)?
- Is the Fund's structure compatible with our entity type?

**Indicative cost:** €15-50k+ for initial structuring depending on jurisdiction. **Do not open the Unit Fund without this engagement.** Per Gen 2 readiness; Gen 1 firms skip this.

---

### 7. EU AI Act Articles 9, 12, 13, 14

**Why it matters:** EU adopters face full high-risk obligations from 2 August 2026. Non-compliance penalty: up to €35M / 7% of worldwide turnover.

**What ØØT provides:** `governance/EU-AI-ACT.md` mapping methodology + X7 register + R6 audit trail + Skill Pack S7.

**What ØØT does NOT provide:** confirmation that your specific use cases are correctly classified; conformity assessment; technical documentation per Art. 11.

**Trigger questions:**
- Are our high-risk use case classifications correct?
- What conformity assessment do we need?
- What's our notified-body engagement timeline?

**Indicative cost:** €10-30k for initial compliance; €5-15k/year ongoing.

---

### 8. GDPR Article 22 — solely automated decisions

**Why it matters:** data subjects (your partners, your customers, anyone) have the right not to be subject to decisions based solely on automated processing. The framework's variable pay calculations and Klarna Test gating both potentially trigger Article 22.

**What ØØT provides:** the framework's design response — R3 produces drafts, founder approves; R7 triggers tests, humans score.

**What ØØT does NOT provide:** confirmation that your specific implementation is GDPR-compliant.

**Trigger questions:**
- Are any of our Routines making final decisions without human sign-off?
- What's our DPIA (Data Protection Impact Assessment) for the variable pay system?
- Do we have a designated DPO?

**Indicative cost:** €3-8k initial DPIA; ongoing DPO cost varies.

---

### 9. Data residency

**Why it matters:** where your Brain physically lives matters for GDPR, US export controls, China data-localisation laws, etc. Cloud-track Brains live where your Curator's storage backend lives; privacy-track Brains live on your always-on machine.

**What ØØT provides:** the tracking via the firm config (`firm.yaml`).

**What ØØT does NOT provide:** the verification that your data residency is compliant.

**Trigger questions:**
- Where does our Brain data physically live?
- Are cross-border transfers (e.g. Brain on US-based GitHub, customers in EU) compliant?
- Do we need EU-only Curator storage?

**Indicative cost:** €2-5k for initial review.

---

### 10. Italian Law 132/2025 (leading indicator)

**Why it matters:** if you operate in Italy, Law 132/2025 introduces criminal AI offences (Art. 612-quater of the Italian Criminal Code: 1-5 years imprisonment for AI-deepfake harm) and aggravating circumstances. **Even if you don't operate in Italy**, this is a leading indicator of EU enforcement seriousness.

**What ØØT provides:** the framework's Klarna Test discipline + audit trail discipline reduces exposure.

**What ØØT does NOT provide:** Italian counsel.

**Trigger questions (if operating in Italy):**
- Do any of our AI use cases potentially trigger Art. 612-quater?
- What's our risk profile under the aggravating-circumstances framework?
- Are administrative penalties (still pending decree) material to our compliance budget?

**Indicative cost:** €5-15k for Italian-counsel engagement.

---

### 11. IP ownership of Brain content

**Why it matters:** in employer/work-for-hire jurisdictions (US default), the firm owns partner-authored content automatically. In other jurisdictions, IP ownership requires explicit assignment. The Brain is the firm's compounding IP; ambiguous ownership at exit time is a real risk.

**What ØØT provides:** the Charter §8 (Confidentiality + IP) defines the firm's IP claim.

**What ØØT does NOT provide:** local-law verification that the Charter's IP assignment is enforceable.

**Trigger questions:**
- Is our IP assignment language enforceable in the partner's jurisdiction?
- What happens to the partner's contributions on exit?
- How does the long-tail entitlement structure interact with IP assignment?

**Indicative cost:** €1-3k per jurisdiction for review.

---

## How to engage counsel (the framework's recommendation)

1. **Find counsel familiar with both employment law AND tech transactions** in your primary jurisdiction. The framework's discipline crosses both; a pure-employment lawyer or pure-corporate lawyer will miss things.
2. **Engage early.** Before the first Partner Charter is signed, not after the first dispute.
3. **Fixed-fee initial review.** ~€5-10k for a comprehensive readiness review covering most of the eleven touchpoints. Avoid hourly billing for the initial scope.
4. **Annual ongoing review.** ~€3-8k/year. Material changes (new jurisdiction, Gen 2 activation, Unit Fund opening) trigger ad-hoc engagements.
5. **Counsel of record on the firm's `governance/DECISION-RIGHTS.md`.** Per the matrix, counsel is **C** (Consulted) or **A** (Accountable) on legal-touchpoint decisions; never **R** (Responsible) — counsel reviews; the firm acts.

---

## What ØØT's authors do (transparency)

The framework's authors operate Slovenian d.o.o.s with engaged Slovenian counsel + Croatian sister-entity counsel. Long-tail entitlements have been structured per signed addenda, not on-chain (Gen 1). The Unit Fund has not been opened (Gen 2 deferred until counsel completes structuring). EU AI Act mapping is being prepared with counsel for the 2 August 2026 deadline.

This is one possible posture among many. The framework does not prescribe a specific entity type or counsel arrangement — it prescribes that the conversation must happen.

---

> ⚠️ **ØØT is a framework. It points at landmines; it does not defuse them. Local counsel is mandatory before adoption in any jurisdiction. The framework's authors take no responsibility for outcomes of adoption without counsel.**

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel.
