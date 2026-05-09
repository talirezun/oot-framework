# W5 — Running a Klarna Test

**Audience:** Any partner assigned as scorer or non-beneficiary reviewer for a Klarna Test.
**Time:** 30-60 minutes per test (do it well, not fast).
**You will end with:** a scored Klarna Test in `klarna-test.xlsx` + a Brain page at `firm/klarna-tests/<test_id>.md`, with a clear PROCEED or HOLD decision.

> 📖 **Concept doc:** [`docs/05-using-the-klarna-test.md`](../05-using-the-klarna-test.md). **Authoritative reference:** [`governance/KLARNA-TEST.md`](../../governance/KLARNA-TEST.md).

---

## What this is + the first 5 minutes

A PR was labelled `ai-replaces-human` (auto-labeller per S4 §4.8). Routine R7 fired. You received Slack/dChat + email:

> KT-2026-014: PR #1502 (replace manual customer-onboarding email with AI drafter) requires Klarna Test scoring before merge. Affected partner: [[partners/anya-gorska]]. Non-beneficiary reviewer: [[partners/mira-tek]]. Scoring window: 5 business days.

You're either the **scorer** (the proposer / accountable) or the **non-beneficiary reviewer** (someone whose comp does not increase as a result of the action).

---

## Step 1 — Read the underlying decision (NOT score yet)

### Open the PR

In GitHub: navigate to the PR. Read description fully. Note:
- What the PR removes (the human-routing code path).
- What the PR adds (the AI Skill / automation).
- Linked design docs / ADRs.

### Open the Brain page

R7 created `firm/klarna-tests/KT-2026-014.md` automatically. Open it.

![Klarna test Brain page](../images/W5-1-klarna-brain-page.png)

*The page has the test_id, decision summary, affected partner(s), non-beneficiary reviewer, full context, and 10 empty score rows.*

### Open the affected partner's Output Spec history

Navigate to `firm/partners/anya-gorska/output-specs/`. Skim recent specs. The framework's discipline: **the affected partner's primary function is what's being automated.** You need to understand it.

### Read `governance/KLARNA-TEST.md`

If you haven't recently. The 10-question rubric definitions are there. Each question has guidance for what 0/1/2 means.

---

## Step 2 — Open `klarna-test.xlsx`

In Excel or Google Sheets, open `templates/excel/klarna-test.xlsx`.

Two sheets matter:

1. **Decision_Log** — has the test's metadata (test_id, date, decision_summary, scorer, non-beneficiary reviewer, total_score (auto-computed), decision (auto-computed), 90-day review date).
2. **Klarna_Score** — where you enter the 10 question scores.

![klarna-test.xlsx Klarna_Score sheet](../images/W5-2-klarna-score-sheet.png)

*Find your test_id row. Q1-Q10 are columns B-K. L (total) auto-computes. M is evidence_links. N is scorer_signoff (Yes/No). O is non_beneficiary_signoff.*

---

## Step 3 — Score Q1: Quality measured vs. human baseline ≥3 months?

The framework's test of evidence:

- **0:** vendor demos / theoretical claims only. No production measurement.
- **1:** some measurement, but <3 months OR not on production traffic OR not on the actual user population.
- **2:** ≥3 months of measurement on real production traffic, with the actual edge-case distribution.

For the Acme onboarding email PR: a 6-week pilot ran on 50 real customers; quality matched human on 80% of cases; failure-cases were 12% worse.

→ Score: **1**. (Pilot ran on production traffic but only 6 weeks, not 3 months; and the failure-case gap is substantive.)

In M (evidence_links), enter: `[[firm/klarna-tests/KT-2026-014/pilot-results]]` (the wikilink to the pilot data Brain page).

---

## Step 4 — Score Q2 through Q10

Continue. For each question:
- Read the question and the rubric (per `governance/KLARNA-TEST.md`).
- Score 0 / 1 / 2.
- Record evidence wikilink in M (column for evidence).

**The framework's discipline: if you're between 1 and 2, score 1.** Conservative bias is correct. Better to remediate one question than ship a 14 that should have been 13.

After Q10:
- L (total) auto-computes via `=SUM(B:K)`.

![Klarna_Score row populated, total auto-computed](../images/W5-3-score-populated.png)

*The total cell turns red if <14, green if ≥14, per the spreadsheet's conditional formatting.*

---

## Step 5 — Sign off

If you're the **scorer**:
- Tick column N (`scorer_signoff = Yes`).

If you're the **non-beneficiary reviewer**:
- Re-read the scorer's work with one specific question: *"Does each score reflect actual evidence, or has the scorer rationalised upward?"*
- Tick column O (`non_beneficiary_signoff = Yes`) only if you actually agree.
- If you disagree on a specific question's score: do NOT sign off. Open a 3-way conversation with the scorer + affected partner.

---

## Step 6 — Auto-decision

The Decision_Log sheet's column I auto-computes:

```
=IF(H2>=14, "PROCEED", "HOLD")
```

If **PROCEED**:
- The `oot/klarna-test` GitHub status check on the PR re-runs and turns green.
- The PR's merge button activates.
- The affected partner can merge.

If **HOLD**:
- Status check stays red. PR cannot merge.
- R7 posts the remediation list to `#klarna-test` automatically.
- The test_id row stays open in scoring; re-score after remediation (do NOT create a new test_id).

![GitHub PR with oot/klarna-test status check passed](../images/W5-4-status-check-green.png)

*Look for the green "oot/klarna-test" check in the PR's status checks list. If still red, the workflow is polling Klarna_Score; allow up to 5 minutes.*

---

## Step 7 — If HOLD: remediate

The remediation list R7 posts is per-question. For our example (total 10/20):

```
KT-2026-014 held. Score: 10/20. Remediation required:
- Q3 (0): Define the reversal threshold. e.g. "If onboarding NPS drops below 60 for 2 weeks, revert."
- Q4 (0): Retain Anya on standby contract for 90 days post-rollout.
- Q5 (1): Address Anya's failure-case concerns in writing. Either modify the AI Skill to handle them, or accept their persistence as risk and plan accordingly.
- Q7 (0): Get Mira's non-beneficiary review.
- Q8 (0): Decide and write down the public-comms posture (likely: "no proactive comms; if asked, the messaging is X"). Assign owner. Set review date.
- Q9 (1): Assign owner for the 90-day review; pre-commit decision framework.
- Q10 (1): Founder must commit in writing to defending in 2 years.
```

Address each. Update the test row's scores. Re-score. The same `test_id` row is updated; do NOT create a new test_id.

---

## Step 8 — The 90-day review

Q9 of the rubric — Klarna's anti-rationalisation mechanism.

When the test PROCEEDS, R7 schedules the 90-day review. The review is NOT theatre:
- Re-measure the metrics from Q1 + Q2.
- Verify the reversal threshold from Q3 has not been breached.
- Verify the standby plan from Q4 hasn't been quietly retired.
- Confirm the 90-day review owner has actually run the review.

If any reveals a problem: the **decision flips back**. The test's PROCEED was conditional; conditions can fail.

The review is recorded as `firm/klarna-tests/KT-YYYY-NNN-90day.md` (a separate page that wikilinks back to the original test page).

---

## Common pitfalls

**1. Scoring fast.**
- 30-60 minutes minimum. Anything less is rubber-stamping.
- The framework's authors find that fast scoring correlates with future remediation costs.

**2. Letting the affected partner score.**
- Q7 explicitly forbids this. The affected partner is consulted via Q5; they don't score.

**3. "We don't need a non-beneficiary because we're aligned."**
- Q7 is non-negotiable. If your partnership cannot produce a non-beneficiary, that is itself a finding (the firm's incentives are too tightly aligned).

**4. Q8 "we won't say anything publicly so n/a."**
- The Q8 correction (B4) closed this loophole. "No public comms" must be a written, owned posture to score 2.

**5. Score is exactly 14 and you're uncertain.**
- The framework's discipline: if uncertain, score 13 (= HOLD). Better to remediate one item than ship a 14 that should have been 13.

**6. The 90-day review reminder is ignored.**
- The reminder is on the calendar for a reason. The test is incomplete without it.

---

## What's next

- **[W6 — Monitoring the Routines Dashboard](W6-monitoring-routines-dashboard.md)** — your daily ops health check ensures R7 fires when it should.
- After the test PROCEEDS: confirm the reversal threshold is in `Quality_Gates` sheet of X4. Confirm the 90-day review is on the founder's calendar. Confirm the affected partner has the standby contract documented.
