# Reference Org Examples — SPEC

Specifications for the three reference organisations Phase 9 generates. Each example is a complete, internally consistent ØØT instance — partners with names, signed Reward Species Declarations, two months of populated ledger rows, working business reviews, the appropriate governance posture for the org's profile.

The examples are deliberately *small enough to read end-to-end* (a new founder can absorb each in 30–60 minutes). They are not minimal — they show the framework in operation, including the awkward edges (a dispute, a Klarna Test that was held, a partner who flagged a perception gap).

All names are fictional, all numbers are illustrative. Currency: EUR throughout (matches the framework's EU-leaning audience; founders in other jurisdictions adapt).

---

## Example 1 — `examples/small-org/`

### Profile

- **Firm:** Solunar Studio. A 3-partner generative-software studio. Founded 2026-Q1.
- **Partners:**
  1. **Mira Tek** — founder, full-time partner, agentic-engineer cohort, jurisdiction: SI (Slovenia). Reward species: hybrid 60/30/10 (60% personal output, 30% team contribution, 10% company outcomes).
  2. **Davor Krznar** — full-time partner, agentic-engineer cohort, jurisdiction: SI. Reward species: pure eat-what-you-kill (100% personal).
  3. **Anya Gorska** — project specialist, vibe-coder cohort, jurisdiction: PL (Poland). Reward species: hybrid 80/15/5 (project-bound).
- **Track:** Cloud.
- **Brain status:** Level 4 (Curator + MyCuratorMCP) from day 1.
- **Legal posture:** Slovenian Limited (`d.o.o.`); local counsel engaged; Mira holds 70% / Davor 30% (Anya is contractor, no equity).
- **EU AI Act exposure:** Limited risk. Their AI use is a Lumina-style RAG widget (S11 Sales & BD) and Code & QA tooling (S4). No high-risk Annex III exposure. EU AI Act mapping (X7) is populated but reflects "minimal" / "limited" tier classifications.

### Brain content

- `firm/index.md`: 4-paragraph firm overview.
- `firm/theses.md`: Solunar's adaptation of MANIFESTO.md — drops Thesis 5 (composability) as a explicit operating concern (they assume it; don't articulate it).
- `firm/partners/index.md`: 3-partner roster.
- Per-partner pages: profile, reward-species-declaration link, 4 output specs each (1 per month × 2 months × 2 outputs/partner average).
- 60 days of `firm/output-logs/*.md` (60 daily logs).
- 8 `firm/business-reviews/*.md` (2 months × 4 Fridays).
- 2 `firm/decisions/D-2026-NNN.md` records (one technical, one commercial).
- 1 `firm/architecture/ADR-2026-001.md` (the choice to ship the Lumina widget rather than build a custom front-end).
- 1 `firm/klarna-tests/KT-2026-001.md` — a Klarna Test that *passed* (score 16/20). Decision: replace a manual customer-onboarding email step with an AI-drafted version. The test was triggered by a PR labelled `ai-replaces-human` (R7). Affected partner: Anya. Non-beneficiary reviewer: Davor. The 90-day review entry is scheduled but not yet complete.

### Excel content

- **X1 partner-output-ledger.xlsx**: Two months of populated Output_Log rows (~50 rows), populated Monthly_Variable for both months, Partner_Dashboard auto-computed.
- **X2 reward-species-declaration.xlsx**: Three sheets (one per partner) with full population.
- **X3 business-review.xlsx**: 8 weekly rows; Decisions_Log has 2 entries; Blockers has 3 closed and 1 open.
- **X4 klarna-test.xlsx**: 1 row (KT-2026-001) with full scoring.
- **X5 metr-baseline.xlsx**: Pre-Code-&-QA-rollout metrics captured for Mira and Davor (Anya is project-bound, didn't roll out tools); 4-week pilot results showing the perception gap detected on Davor (he reported +25% productivity; DORA delta was +5%).
- **X6 agent-skill-roi.xlsx**: 60 days of agent-cost data; ~€80/month total Anthropic + Curator spend.
- **X7 eu-ai-act-mapping.xlsx**: Populated with their two AI use cases (Code & QA tooling — minimal; Lumina widget — limited risk per Article 50 transparency). No high-risk obligations.
- **X8**: Not populated (Solunar has not opened the Unit Fund).
- **X9 oot-readiness.xlsx**: Filled in retroactively at month 6 — they scored 78%, with a flag on Q11 (METR baseline willingness — Davor was sceptical at first).

### Awkward edges to include (for realism)

1. **A perception-gap finding** — X5 shows Davor's +25 self-report vs. +5 DORA-measured; the Friday BR for week-of-2026-04-10 has a discussion item where Mira confronts the gap directly, Davor accepts the data, they decide to run a 30-day re-baseline.
2. **A Tier-1 dispute** — Anya disputes a value_tier classification on her output #14 (Mira marked it `M`, Anya argues `S`). Resolved in 4 days. `firm/compensation/2026-04/disputes/D-2026-04-001.md` records the conversation; Anya's variable_statement for April reflects the agreed `S` tier (€2,000 envelope vs. original €500).
3. **A blocker that pushed a deal slip** — week-of-2026-03-27 BR records a blocker that Davor raised about the Lumina widget's qualification step; resolved via an ADR a week later.

### What this example demonstrates

- The framework works at 3 partners.
- The Klarna Test pass-flow is end-to-end (trigger → score → decision → 90-day review scheduled).
- Disputes resolve at Tier 1.
- The Curator-fed Brain is operationally complete after 60 days.

---

## Example 2 — `examples/medium-org/`

### Profile

- **Firm:** Brda Cooperative. A 12-partner studio building AI-augmented analytics tools for the wine industry. Founded 2025-Q2; ØØT-adopted 2026-Q1 after running the readiness assessment (X9 score: 71%).
- **Cohort mix:**
  - 5 full-time partners (founders + senior).
  - 4 project specialists (each tied to one customer engagement).
  - 3 advisors (one industry advisor, one technical advisor, one M&A advisor).
- **Reward species mix:** 3 hybrid, 1 lockstep (the most senior founder, who explicitly chose smoothing), 1 eat-what-you-kill (one of the founders, ROWE-leaning).
- **Track:** Cloud.
- **Brain status:** Level 4. Has 4 Curator domains: `firm`, `customers`, `products`, `legal`.
- **Legal posture:** Slovenian cooperative (`zadruga`) with a sister Croatian d.o.o.; both founders share the legal touchpoint cost. EU operations only.
- **EU AI Act exposure:** Limited + one high-risk use case (an AI-driven supplier-trust scoring system used by their wine-industry customers). They've engaged counsel; the high-risk use case has full Article 9 / 12 / 13 / 14 mapping in X7.

### Brain content

- `firm/`: One full quarter (90 days) of operational data.
  - 12 partner pages with reward-species declarations.
  - Per-partner output specs: 6–10 specs per full-time partner; 2–4 per specialist; 0–1 per advisor.
  - 90 daily output logs.
  - 13 weekly business reviews.
  - 8 monthly variable statements per partner (some have only the most recent given the cohort change in February).
  - 1 quarterly long-tail settlement (R4 ran on 2026-04-01 for Q1 2026).
- `firm/decisions/`: ~12 decision records (the medium-org has a real cadence of decision logging).
- `firm/architecture/`: 4 ADRs.
- `firm/klarna-tests/`: 3 Klarna Tests. KT-2026-001 passed (score 17). KT-2026-002 failed (score 11) — the test held the deployment, the team remediated, re-scored at 15, then proceeded. KT-2026-003 is in scoring as of the snapshot date.
- `firm/change/pilots/`: 2 pilot summaries (Code & QA pack rollout to engineers; Marketing pack rollout to the customer-success team).
- `firm/change/ai-champions/`: 1 (the most-rapid-adopter engineer, Tomislav, recognised after 6 weeks of measurable DORA gains).
- `firm/audit-logs/`: 90 daily files (one per day of the quarter).

### Excel content

- All 9 templates populated for the full quarter.
- X8 Treasury-runway: optional but populated since Brda ran a 9-month Unit Fund pilot in late 2025 and is on the brink of formally opening it. The reserve_coverage_ratio is 1.4 (above 1.0); runway is 14 months.

### Awkward edges to include

1. **Cohort change** — one specialist (Marin) was promoted from project-specialist to full-time-partner mid-quarter. The renegotiation is recorded in his X2 sheet's Renegotiation_Log; the Brain has a `firm/decisions/D-2026-02-005.md` with the rationale; the variable_statement template handled the prorated cohort change correctly.
2. **A Tier-2 dispute** — a specialist disputed her output spec being closed without acceptance; Tier 1 didn't resolve; a partner panel met (3 partners, with one non-beneficiary); they ruled in the specialist's favour; the ruling was documented; the variable was adjusted retroactively. This is the hardest part to make realistic; the example uses a real-feeling disagreement (a deliverable judged "shipped" by the founder but considered "rework requested" by the specialist).
3. **The METR perception gap was caught in a pilot** — the Code & QA pilot's X5 Adoption_Curve shows a 28-point perception gap that the firm caught and remediated *before* full rollout. This is the framework's textbook win condition.
4. **An EU AI Act high-risk use case** — the supplier-trust scoring system. X7 has the full Article 9/12/13/14 mapping. Counsel has reviewed and signed off. The audit trail is appended daily by R6. There is one anomaly in the audit log (a model output that flagged a low-confidence supplier; the human reviewer overrode; the override is recorded and reviewed in the next BR).
5. **A Klarna Test that initially failed** — KT-2026-002. The team wanted to replace human contract review for routine customer agreements. First score: 11. Held. Remediation list (mostly: define reversal threshold, retain the affected partner on standby, get a non-beneficiary review). Re-scored at 15. Proceeded with a 90-day review.

### What this example demonstrates

- The framework works at 12 partners with cohort diversity.
- Tier-2 disputes can resolve without escalation to founder.
- The EU AI Act mapping is operationally workable for a single high-risk use case.
- Klarna Test "fail → remediate → pass" is a normal flow, not an emergency.

---

## Example 3 — `examples/regulated-eu-org/`

### Profile

- **Firm:** AdriaLex AI. A 6-partner regulated-EU AI consultancy serving banking and insurance clients. Founded 2025-Q4 specifically to operate as an ØØT-native firm.
- **Cohort:** 6 full-time partners; no specialists or advisors; all have legal/compliance backgrounds plus AI engineering competence.
- **Track:** Cloud, with privacy-track migration *in progress* (they're in the middle of weekend two of the privacy track at the snapshot date).
- **Legal posture:** Croatian d.o.o.; counsel on retainer (mandatory for their client base); EU AI Act compliance is the *product* — they help clients map their systems, so theirs must be exemplary.
- **EU AI Act exposure:** Six AI use cases, three high-risk (Annex III mappings including employment-decision support and access-to-essential-services classifiers used for clients), two limited-risk, one minimal. Each has full Article 9/12/13/14 mapping.
- **EU MiCA / GDPR exposure:** Active. They handle client data subject to GDPR Article 22 (solely automated decisions). The firm has a designated DPO (one of the partners).

### Brain content

- 60 days of full operation.
- 6 partner pages.
- 4 ADRs.
- 8 Klarna Tests across 60 days (this firm has a higher Klarna Test cadence because they ship AI tooling for clients — every "AI replaces human" decision in client engagements gets the test). Of the 8: 6 proceeded, 1 held + remediated + proceeded, 1 abandoned (the firm refused a client engagement after the Klarna Test scored 6 and remediation was infeasible — this is the example's most important moral).
- 60 daily audit logs, all signed commits, all on the protected `audit/` branch (this firm's audit branch is separate from `main`, with even tighter protection — required reviews from a DPO).
- 1 quarterly long-tail settlement.
- 6 monthly variable statements per partner.

### Excel content

- All 9 templates populated.
- X7 eu-ai-act-mapping.xlsx is the standout — 6 use cases, 3 high-risk with full obligation mapping, 60 days of audit-log-index entries, 4 anomalies flagged across the period (each one investigated, two led to model retraining, two were ruled false-positive). Counsel review signed off at each of: adoption (initial), monthly (recurring), and quarterly (comprehensive).
- X8 not populated (no Unit Fund interest yet).
- X9 was scored at 92% pre-adoption — they were ready.

### Awkward edges to include

1. **The abandoned engagement** — the Klarna Test that scored 6 and could not be remediated. The example contains the full Brain page (`firm/klarna-tests/KT-2026-005.md`) with the score breakdown, the remediation analysis, and the founder's signed-off decision to decline. The decision is also in `firm/decisions/D-2026-03-010.md`. This is the framework's *purpose* in action — the discipline declined a fee.
2. **A GDPR Article 22 escalation** — one of the firm's high-risk use cases (an employment-screening classifier for a banking client) was challenged by a data subject. The audit trail (R6) had the relevant decision logged with a human reviewer; the firm produced the trail to the supervisory authority within 24 hours; no fine. This is captured as a Brain page (`firm/legal/gdpr-escalation-2026-04-12.md` — note: in `legal/` domain, not `firm/`) with the response timeline.
3. **A privacy-track migration mid-stream** — the firm is partway through the cloud→privacy migration. The Brain has `firm/privacy-track/migration-runbook.md` showing weeks 1–3 done, weeks 4–8 pending. This shows what the migration *looks like* during transition (mixed mode is messy; the framework's "don't mix tracks" advice is in tension with reality, and this example doesn't pretend otherwise).
4. **A non-beneficiary reviewer rejection** — one Klarna Test (KT-2026-007) had the non-beneficiary reviewer initially refuse to sign — they thought the affected partner had not been adequately consulted. The test was paused, additional consultation happened, the affected partner's concerns were addressed, the reviewer signed. The Brain has the conversation log.

### What this example demonstrates

- The framework works under EU regulatory pressure.
- The Klarna Test really does decline engagements (not a paper discipline).
- GDPR Article 22 audit trail is operationally robust.
- Privacy-track migration is a multi-week endeavour, not a weekend; the framework is honest about this.

---

## Generation conventions for Phase 9

For each reference org:

1. **Coherence is non-negotiable.** Every wikilink must resolve; every number in the Excel files must match the Brain pages; every decision must reference the underlying ledger entries. The validator from Phase 8 must pass on the example as-shipped.
2. **Names are fictional, jurisdictions are realistic.** Use plausible Slovenian / Croatian / Polish names for the cooperative-leaning examples; the regulated-EU example uses Croatian-leaning names. No real customer names; use composite/anonymous descriptors (e.g. "a mid-sized Slovenian wine producer").
3. **Numbers are realistic but not aspirational.** Variable pay totals in the small-org should be ~€500–€2,500/month per partner. Medium-org full-time partners: €2,000–€6,000/month. Regulated-EU partners: €4,000–€10,000/month (consultancy rates).
4. **The awkward edges must be present.** A reference org without dispute, perception gap, Klarna held, or abandoned engagement is dishonest. Each example has at least three.
5. **README in each example folder** explains the profile, what the example demonstrates, and the recommended reading order.

---

## Acceptance criteria

For each of the three reference orgs:

- Directory matches the structure in `templates/brain/FIRM-ONTOLOGY.md` (path-by-path).
- Every Excel file opens without errors and every formula evaluates against the seeded data.
- Every Brain page passes the Curator's `scan_wiki_health` check.
- Every Klarna Test entry has a corresponding `firm/klarna-tests/KT-...md` page and a corresponding row in `klarna-test.xlsx`, and the two agree on every field.
- The reference org's `firm/README.md` (or top-level README in `examples/<id>/`) explains the awkward edges so a reader can find them quickly.
- The validator from Phase 8 (`scripts/validate_skills.py` and the Excel validation workflow) passes against the example.
