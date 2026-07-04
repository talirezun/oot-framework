# The Klarna Test

**The signature epistemic check of the ØØT framework.**

Any ØØT recommendation that would have produced the Klarna outcome must be flagged. This document defines what that means, why the test exists, the ten-question scoring rubric, what the score means, and how the test is operationally enforced.

---

## What happened at Klarna (the canonical cautionary tale)

In 2024, Klarna publicly announced it had cut roughly 700 customer-service roles and credited AI for the saving. The announcement received extensive favourable coverage as a leading example of AI-driven workforce transformation. CEO Sebastian Siemiatkowski stated the AI assistant was doing the work of 700 full-time agents.

By 2025–2026, service quality had degraded materially. Customer satisfaction scores dropped. Complaint resolution times lengthened. The company quietly began rehiring, ultimately adopting a hybrid "Uber-style" workforce model with on-demand human agents brought back to handle the work the AI assistant could not credibly do alone.

Total headcount over the period still fell roughly 40% (from ~5,500 to ~3,400). The cost reduction was real. But the headline narrative — *AI replaces customer service* — collapsed publicly and is now widely cited as a leading-edge example of premature automation.

The lesson is not "don't automate." The lesson is: **don't automate before quality bars are proven and reversal plans are real.**

---

## Why ØØT codifies this

Every organisation considering AI-driven workforce changes will believe they are the exception to Klarna. They will believe their AI is better, their workflow is more constrained, their humans were more replaceable. Sometimes they will be right. Often they will be wrong. The cost of being wrong is not just the rehiring; it is the trust loss with remaining staff, the public credibility hit, and the structural difficulty of running a hybrid restoration model after a clean-cut announcement.

ØØT exists in part to make the partner-not-employee operating model real. That mission requires that the framework refuse to recommend, automate, or facilitate any decision that would replicate the Klarna outcome — *even when the framework's own automations could enable it*.

The Klarna Test is the discipline that makes the refusal operational.

---

## Scope of the test

The Klarna Test runs before any decision that:

1. **Replaces a human partner's primary function with an AI agent or Skill.** "Primary function" means: the function that defined the partner's reward-species declaration and output spec.
2. **Reduces the human-agent ratio in a domain by more than 25%** within a single quarter, regardless of the absolute number of partners affected.
3. **Removes a quality gate** that was protecting against AI-generated regressions (in code, content, customer interactions, contractual language, etc.).
4. **Publicly attributes a workforce change to AI** in marketing, investor communications, or public statements.

Each of these is a Klarna trigger. Each requires running the test and clearing it (score ≥14/20) before proceeding.

The test does **not** run for:

- Routine AI-augmentation of existing partner workflows (that is the centaur model; it is *the design*).
- Hiring an AI tool to do work no human partner was doing previously.
- Automating internal back-office processes (logging, audit trails, ledger entries) where no human's primary function is replaced.

---

## The ten-question scoring rubric

Each question is scored 0, 1, or 2. Total possible: 20. The threshold for proceeding is **≥14 / 20 (70%)** (the retired 10-point rubric mapped this to ≥7). A score below 14 blocks the proposed action.

For each question, score:

- **0 — No / Not addressed.** The question reveals a gap or risk that has not been mitigated.
- **1 — Partial.** Some evidence or mitigation exists but is incomplete or untested.
- **2 — Yes / Fully addressed.** Concrete, tested, documented evidence of mitigation.

### The questions

**1. Has the AI's quality been measured against the human baseline on the *actual* task, in the *actual* environment, for at least three months?**

A demo or vendor benchmark does not count. Internal measurements on real production traffic, with the actual user population and the actual edge-case distribution, are required.

**2. Are the metrics that defined human success still being measured after the AI takes over?**

If the previous quality bar was "customer issue resolved on first contact 80% of the time," that exact metric must continue to be measured. Replacing the metric with a different one — "AI confidence score," "response latency" — fails this question.

**3. Is there a defined quality threshold below which the AI's deployment is automatically reversed?**

A pre-committed threshold ("if first-contact resolution drops below 75% for two consecutive weeks, we revert"). With no threshold, there is no reversal trigger; without a reversal trigger, there is no reversal plan.

**4. Is the reversal plan operational, not theoretical?**

Have the displaced humans been retained on standby contracts? Are escalation paths to human review still active? Can the org practically restore the previous staffing within two weeks if the threshold is breached?

**5. Have affected partners been consulted, and have their concerns been addressed in writing?**

Not "informed." Not "managed." Consulted. With a written record of what they said and how it was addressed.

**6. Is there a METR baseline?**

DORA + SPACE + DX Core 4 metrics captured before AI rollout, per the Change Management Skill Pack. Without a baseline, the perception gap (humans report 20% faster while measurably 19% slower) cannot be detected.

**7. Has the decision been reviewed by a partner who is *not* a beneficiary of the cost saving?**

A partner whose variable pay or long-tail entitlement does not increase as a result of the action. This is the conflict-of-interest check.

**8. Is the public-communication posture for this decision specified — even if the chosen posture is "no public communication"?**

The question always applies. There are three valid postures, each scored as follows:

- **Score 2** — Public messaging is drafted and matches operational reality precisely (e.g. "AI handles 60% of X with human escalation for 40%"), or a written decision *not* to communicate publicly exists with an owner and a review date.
- **Score 1** — Posture is decided in principle but the messaging is not yet drafted and reviewed against operational reality, or the no-comms decision is verbal only.
- **Score 0** — No posture decided. This is the Klarna failure mode in its purest form: a workforce change ships without anyone owning what gets said about it.

The previous "n/a" loophole has been removed: there is no decision in scope for the Klarna Test for which silence is automatically defensible. Active decision required.

**9. Has a 90-day post-deployment review been scheduled and resourced?**

A calendar invite, an owner, a budget for the review work, and a pre-committed decision framework for what the review's outputs trigger.

**10. Would the founder be willing to defend this decision publicly, in detail, two years from now?**

The longest-horizon honesty check. If the answer is no, the action fails by definition. If the answer is yes, the founder is putting their reputation behind it; the rest of the framework can support that.

### Scoring template

The `klarna-test.xlsx` template (X4) implements this rubric. The Decision Log sheet captures: decision, date, scorer, the ten question scores with evidence references, total, decision (proceed / hold / abandon), reversal plan reference, 90-day review date.

---

## What "hold" means

A failing score (<14) does not mean "abandon." It means **hold and remediate.**

Specifically:

- Identify which questions scored 0 or 1.
- For each, define the concrete remediation: the missing measurement, the missing reversal plan, the consultation that hasn't happened, the metric that needs reinstatement.
- Re-score after remediation.
- Only proceed when the score is ≥14.

If remediation is not feasible (e.g., the metric cannot be measured without months of new instrumentation; the displaced humans cannot be put on standby without violating local employment law), the answer is **abandon**, not "rationalise to a higher score."

---

## How the test is operationally enforced

**1. Code & QA Skill Pack — pre-merge gate.**

The Code & QA Skill Pack instructs every Claude Code session to flag any pull request that:

- Removes a code path that previously routed work to a human (e.g., removes a "send to manual review" branch).
- Adds a Skill or agent that automates a function previously specified in a partner's output spec.
- Modifies a `partner-output-ledger.xlsx` formula in a way that reduces variable pay attribution to a human partner.

Such PRs are auto-labelled `ai-replaces-human`. The Routine R7 (Klarna Test Trigger) detects the label and:

- Posts a notification to the founder + the affected partner.
- Creates a Klarna Test entry in `klarna-test.xlsx`.
- Blocks merge until the entry shows a score of ≥14 with founder + affected-partner sign-off.

**2. Routine R6 — daily audit trail.**

Every day, the audit trail logs all Klarna Test entries, their current state (open / scored / proceeded / held / abandoned), and any state transitions in the past 24 hours. This is mandatory under EU AI Act Article 12 record-keeping for orgs in EU jurisdiction; it is good practice for everyone else.

**3. Friday Business Review — standing agenda item.**

Every BR includes a "Klarna Test status" item. New tests, tests held, tests resolved. The agenda is auto-populated by Routine R2.

**4. Quarterly partner check-in — explicit topic.**

In the quarterly check-in, every partner is asked whether they have observed any Klarna-test-able decisions in the firm that were *not* tested. The check is for blind spots — situations where the framework's auto-detection failed.

---

## Worked example

*(This is a sketched example for illustration; orgs will accumulate their own.)*

**Decision proposed:** Replace the existing human partner who handles customer-onboarding documentation with an AI Skill that drafts onboarding letters from a customer profile and sends them automatically.

**Klarna Test scoring:**

| # | Question | Score | Evidence |
|---|---|---|---|
| 1 | Quality measured vs. human baseline for ≥3 months? | 1 | A 6-week pilot ran; quality was within 5% of human baseline on 80% of cases, but failure cases were 12% worse. |
| 2 | Original success metrics still measured? | 2 | Customer NPS on onboarding letters and time-to-first-product-use both still tracked. |
| 3 | Defined reversal threshold? | 0 | Not defined. |
| 4 | Reversal plan operational? | 0 | The human partner was not retained on standby. |
| 5 | Affected partner consulted in writing? | 1 | Partner was informed; their feedback was acknowledged but not addressed (they raised concerns about the failure-case pattern). |
| 6 | METR baseline? | 2 | DORA-equivalent metrics for customer-onboarding cycle captured for 90 days pre-rollout. |
| 7 | Reviewed by non-beneficiary partner? | 0 | Reviewed only by the partner championing the change, who would benefit from the cost saving. |
| 8 | Public-communication posture specified? | 0 | No comms posture decided. The team assumed silence was acceptable; nobody owned the question of what would be said if a customer or journalist asked. This is the Klarna failure mode. |
| 9 | 90-day post-deployment review scheduled? | 1 | A review is on the calendar but no owner or framework is defined. |
| 10 | Founder willing to defend this in 2 years? | 1 | Founder is "comfortable" but not "willing to defend in detail." |

**Total: 8 / 20.**

**Decision: Hold.**

**Remediation actions:**

- Q3: Define the reversal threshold ("If onboarding NPS drops below 60 for two weeks, or if the failure-case pattern in pilot recurs, revert").
- Q4: Retain the human partner on a standby contract for 90 days.
- Q5: Address the partner's failure-case concerns in writing; either modify the Skill to handle them or accept their persistence as a risk and plan accordingly.
- Q7: Have a non-beneficiary partner review the decision with full evidence.
- Q8: Decide and write down the public-communication posture (likely: "no proactive comms; if asked, the messaging is X"). Assign an owner. Set a review date.
- Q9: Assign an owner for the 90-day review; pre-commit the decision framework.
- Q10: If the founder cannot honestly say yes, abandon.

After remediation, re-score. Only proceed if score ≥14.

---

## A note on the test's own honesty

The Klarna Test can be gamed. A motivated scorer can rationalise 1s into 2s and 0s into 1s. The framework relies on three guards against this:

1. **The non-beneficiary review (Q7)** — built into the rubric.
2. **The Friday Business Review standing agenda** — every test outcome is visible to the partnership.
3. **The 90-day post-deployment review (Q9)** — every test that proceeded is checked against reality.

These three guards do not eliminate the gaming risk. They reduce it to a level the framework's authors believe is workable. If your organisation finds that Klarna Test scoring is consistently rationalising upward, the problem is cultural; it cannot be fixed by tightening the rubric.

The test is the framework's most important single sentence. Treating it as a checkbox is the framework's most important single failure mode.