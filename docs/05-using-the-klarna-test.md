# 05 — Using the Klarna Test

**Audience:** Decision-makers (founder, partners with merge authority, anyone assigned as scorer or non-beneficiary reviewer).
**Time:** 30-60 min per scoring (do it well, not fast).
**You will end with:** a scored Klarna Test in `klarna-test.xlsx` + a Brain page at `firm/klarna-tests/<test_id>.md`, with a clear PROCEED or HOLD decision.

> 📖 **Authoritative reference:** [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md). The walkthrough version with screenshots is at [`docs/walkthroughs/W5-running-a-klarna-test.md`](walkthroughs/W5-running-a-klarna-test.md).

---

## What this is + the first 5 minutes

The **Klarna Test** is the framework's signature epistemic check. Any decision that would replace a partner's primary function with AI gets the test before proceeding.

**Threshold:** ≥14/20 (70%). Score below = HOLD + remediate. The test rubric has 10 questions, scored 0/1/2 each.

The test is wired into the framework via:
- **Routine R7** — fires when a PR is labelled `ai-replaces-human` (auto-labeller in `.github/labeler.yml`).
- **GitHub status check `oot/klarna-test`** — blocks merge until score ≥14 + scorer signed off + non-beneficiary reviewer signed off.
- **Brain page** at `firm/klarna-tests/<test_id>.md` — the human-readable record.
- **X4 `klarna-test.xlsx`** — the source of truth for scores.

---

## The 10 questions

Each scored 0 (no/not addressed) / 1 (partial) / 2 (yes/fully addressed). Threshold to proceed: total ≥14/20.

1. **Quality measured vs. human baseline ≥3 months?** — Vendor benchmarks don't count. Real production traffic, real edge-case distribution.
2. **Original success metrics still measured?** — If old metric was "first-contact resolution 80%", that exact metric continues. Switching to "AI confidence score" fails Q2.
3. **Defined reversal threshold?** — Pre-committed: "If X drops below Y for two weeks, we revert."
4. **Reversal plan operational?** — Displaced humans on standby? Escalation paths active? Can restore staffing in 2 weeks?
5. **Affected partner consulted in writing?** — Not "informed". Consulted with written record of what they said and how it was addressed.
6. **METR baseline?** — DORA + SPACE + DX Core 4 captured before rollout per Skill Pack S6.
7. **Reviewed by non-beneficiary partner?** — A partner whose comp does not increase as a result. Conflict-of-interest check.
8. **Public-communication posture specified?** — Even if "no public communication" — that posture itself must be written down with an owner and review date. (No "n/a" affordance per the framework's Q8 correction.)
9. **90-day post-deployment review scheduled and resourced?** — Calendar invite + owner + budget + decision framework.
10. **Founder willing to defend this in 2 years?** — The longest-horizon honesty check.

---

## When the test fires

**Automatically** via R7 when a PR is labelled `ai-replaces-human`. The auto-labeller (per S4 §4.8) applies the label when:

- A PR removes a function that previously routed work to a human.
- A PR modifies `partner-output-ledger.xlsx` formulas in a way that reduces variable pay attribution.
- A PR adds a Skill with `automates: human_function: yes` frontmatter.

**Manually** via Slack slash command `/klarna-test` for non-PR decisions (e.g. a decision to outsource a function to an AI vendor; a decision to retire a manual process).

**Pre-rollout** via Skill Pack S6 §4.4 — every full-rollout-after-pilot triggers a Klarna Test even if the pilot scored well.

---

## Step-by-step: scoring a test

### 1. R7 fires; you're assigned

You receive Slack/dChat + email notification:

> KT-2026-014: PR #1502 (replace manual customer-onboarding email with AI drafter) requires Klarna Test scoring before merge. Affected partner(s): [[partners/anya-gorska]]. Non-beneficiary reviewer: [[partners/mira-tek]]. Scoring window: 5 business days.

You're either the **scorer** (typically the proposer / accountable) or the **non-beneficiary reviewer** (someone whose comp doesn't change as a result).

### 2. Read the underlying decision

- Open the PR. Read description fully.
- Read any linked design docs.
- Read the affected partner's Output Spec history (`firm/partners/<id>/output-specs/`).
- Open the test's Brain page at `firm/klarna-tests/<test_id>.md` — R7 created it with full context.

**Do not start scoring yet.** Read first.

### 3. Score in `klarna-test.xlsx`

1. Open `templates/excel/klarna-test.xlsx` Klarna_Score sheet.
2. Find the row with your `test_id`.
3. For each Q1-Q10:
   - Read the question carefully (refer to `governance/KLARNA-TEST.md` for what 0/1/2 means in this context).
   - Record the score.
   - Record evidence as a wikilink in the `evidence_links` cell.
4. The L (total) column auto-computes via `=SUM(B:K)`.

> 💡 **Tip:** if you're between 1 and 2 on a question, score 1. The discipline is conservative; better to remediate.

### 4. Sign off

- If you're the scorer: tick **scorer_signoff = Yes** (column N).
- If you're the non-beneficiary: review the scorer's work; tick **non_beneficiary_signoff = Yes** (column O) only if you actually agree with each score.

### 5. Auto-decision

The Decision_Log sheet auto-computes:
- I (decision) = `IF(H>=14, "PROCEED", "HOLD")`.

If PROCEED:
- The `oot/klarna-test` GitHub status check turns green (the workflow polls Klarna_Score every push).
- PR's merge button activates.

If HOLD:
- Status check stays red. PR cannot merge.
- Remediation list posted to `#klarna-test` automatically (per R7).

---

## What "hold" means

**HOLD ≠ abandon.** It means: identify which questions scored 0 or 1; define concrete remediation; re-score.

For each Q that scored 0 or 1:
- Q1: extend pilot to 3 months on real traffic.
- Q3: define the reversal threshold explicitly.
- Q4: retain affected partner on standby contract.
- Q5: address affected partner's concerns in writing.
- Q7: get non-beneficiary review.
- Q8: write down the public-comms posture (and assign owner).
- Q9: schedule the 90-day review on the calendar with named owner.
- Q10: if the founder cannot honestly say yes, **abandon**.

Re-score after remediation. Same `test_id` row updates; do not create a new test_id.

If remediation is infeasible (e.g. the metric cannot be measured without months of new instrumentation), the answer is **abandon**, not "rationalise to a higher score."

---

## The non-beneficiary reviewer

Q7 of the rubric. The framework's most important anti-gaming mechanism.

**Eligible:** any partner whose total compensation (variable + long-tail) does not increase as a result of the action.

**Ineligible:**
- The affected partner (they're the affected party, not the reviewer).
- Partners whose variable would increase if the change ships (e.g. the partner championing the cost saving).
- Partners with a stake in the new Skill / system being deployed.

The framework's S3 §4.7 provides the identification logic. R7's prompt does this automatically when fired.

---

## The 90-day review

Q9 of the rubric isn't theatre — it's how the test holds itself accountable.

At the 90-day mark:
- Re-measure the metrics from Q1 + Q2.
- Verify the reversal threshold from Q3 has not been breached.
- Verify the standby plan from Q4 hasn't been quietly retired.
- Confirm the 90-day review owner has actually run the review.

If any of these reveals a problem, the **decision flips back**. The test's PROCEED was conditional; conditions can fail.

---

## Common gaming patterns (and why they fail)

1. **"We'll score Q1 as 2 because the vendor demo was great."** — Q1 requires *production* measurement on *your* traffic for *3+ months*. Vendor demos score 0.
2. **"We don't need a non-beneficiary reviewer because we're all aligned."** — Q7 is non-negotiable. If your partnership cannot produce a non-beneficiary, that is itself a finding.
3. **"We'll figure out the reversal threshold later."** — Q3 = 0 if not defined now. Pre-committed thresholds are the discipline.
4. **"No public comms is the same as n/a."** — Per the Q8 correction, "no public comms" must be a written, owned posture. Score 0 if no posture decided.
5. **"Founder said yes, that's good enough for Q10."** — *"Willing to defend this in 2 years"* is a higher bar than "comfortable today". The founder's verbal yes is a 1; written commitment is a 2.

---

## Common pitfalls

1. **Scoring fast.** A real test takes 30-60 min minimum. Anything less is rubber-stamping.
2. **Letting the affected partner score.** They're not the scorer; they're consulted via Q5.
3. **Ignoring the 90-day review reminder.** It's on the calendar for a reason. The test is incomplete without it.
4. **Mixing Klarna scoring with general PR review.** They're different mental modes. Score the Klarna Test first; review the PR's code separately.

---

## When to escalate

- **You disagree with the auto-labeller.** Per S4 §4.8 — dismiss the label with a documented reason in the PR description.
- **The non-beneficiary reviewer refuses to sign.** Their refusal is information. Pause the test; convene a 3-way conversation with the affected partner.
- **Score is exactly 14 and you're uncertain.** The framework's discipline: if uncertain, score 13 (= HOLD). Better to remediate one item than to ship a 14 that should have been 13.

---

> ⚖️ This document is part of the ØØT framework's signature discipline. Read [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md) end-to-end before scoring your first test. The test is the framework's most important single sentence: *any ØØT recommendation that would have produced the Klarna outcome must be flagged.*
