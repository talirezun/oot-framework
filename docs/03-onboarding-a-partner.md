# 03 — Onboarding a Partner

**Audience:** Founder + the partner being onboarded.
**Time:** 90-minute session + 1 week of partner self-onboarding + 30-day check-in.
**You will end with:** a fully onboarded partner with signed Reward Species Declaration, signed Partner Charter, first Output Spec drafted, all tools provisioned, and Brain folder live.

> 📖 **Reference templates:** [`templates/partner-onboarding/`](../templates/partner-onboarding/) — ships the canonical 30-step checklist, the provisioning script, and the first-90-days plan. The Partner Charter template lives at [`templates/partner-charter.md`](../templates/partner-charter.md).

---

## What this is + the first 5 minutes

Onboarding a partner is the framework's most important per-partner ritual. It establishes:

- **Cohort designation:** full-time partner / project specialist / advisor.
- **Reward Species Declaration:** the contractual definition of how the partner is compensated.
- **Output Spec:** the first piece of work the partner is committing to.
- **Partner Charter:** the partnership-style agreement (not an employment contract).
- **Tools provisioning:** Bitwarden, GitHub, Slack/dChat, Drive/PollinationX, Brain folder.

The 30-step checklist at [`templates/partner-onboarding/checklist.md`](../templates/partner-onboarding/checklist.md) is the canonical sequence. Steps 1-15 happen in the 90-minute session; steps 16-25 are the partner's first week; steps 26-30 are the 30-day check-in.

---

## Pre-requisites

- Counsel sign-off on Partner Charter for the partner's jurisdiction (per [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md)).
- Bitwarden organisation set up (per `governance/SECRETS-POLICY.md`).
- GitHub organisation + Brain repo with the 5 setup pre-requisites configured (per Skill Pack S4 §4.0).
- Slack workspace (cloud) or 4thtech firm domain + dChat workspace (privacy).
- The provisioning script at `templates/partner-onboarding/provisioning-script.sh` works — test it with a throwaway `partner_id` like `test-onboard-2026-05-01`.

---

## Pre-onboarding (founder, day before, ~30 min)

Per the checklist steps 1-5:

1. **Verify track readiness.** Confirm budget for cloud or hardware for privacy.
2. **Verify cohort decision.** Founder + (if applicable) managing partner agreed.
3. **Pre-fill X2 first-pass values** (subject to negotiation in the session): reward_species, base_amount, variable weights, bonus splits, output_multiplier.
4. **Verify legal posture.** Counsel sign-off on Partner Charter for the partner's jurisdiction is current.
5. **Send calendar invite** for the 90-min session (both parties present).

---

## The 90-minute session — step-by-step

### 0:00 — 0:30 — Walk through `MANIFESTO.md` together

The partner internalises the five theses, especially **Resistance** and the **Klarna Test**. Questions invited.

If the partner cannot articulate the Klarna Test framing back to you in their own words by the end of this 30-min block, **pause the onboarding**. Schedule a follow-up. Onboarding a partner who hasn't internalised the discipline produces friction in month two.

### 0:30 — 1:00 — Reward Species Declaration

1. Open `templates/excel/reward-species-declaration.xlsx`.
2. Add a sheet for the new partner (or use a per-partner workbook for orgs >20 partners).
3. Walk through every column:
   - **Partner_Profile:** cohort, jurisdiction, base_currency, stablecoin_upgrade_pref (Gen 2), unit_fund_interest (Gen 2), two_worlds_self_id.
   - **Base_Variable_Split:** reward_species (eat-what-you-kill / lockstep / hybrid), base_amount, variable weights summing to 1.0, output_multiplier (default 1.0), bonus splits summing to 1.0.
4. **Negotiate** where the partner wants different values from your pre-fill. The negotiation is real. Pre-fills are a starting point, not a fait accompli.
5. **Validate** the sums (variable weights = 1.0; bonus splits = 1.0 — the spreadsheet's conditional formatting flags violations red).
6. Save the workbook.
7. **Generate signed PDF** (founder + partner sign). Store at `firm/partners/<id>/legal/reward-species-<DATE>.pdf`.
8. **Compile Brain summary** at `firm/partners/<id>/reward-species-declaration.md` per [`templates/brain/reward-species-declaration-summary.md`](../templates/brain/reward-species-declaration-summary.md).
9. Both parties sign the Brain page (signed git commit).

### 1:00 — 1:10 — Two Worlds of Code self-id

Run the 5-question assessment from [`skills/code-qa/SKILL.md`](../skills/code-qa/SKILL.md) §4.9. Record `two_worlds_self_id` in the partner's `firm/partners/<id>/profile.md`.

> 💡 This is **not a value judgement** — it's an operational input to the partner's training plan and Klarna Test triage. Vibe-coder, agentic-engineer, transitional, non-code are all valid.

### 1:10 — 1:25 — First Output Spec

Open [`templates/output-spec.md`](../templates/output-spec.md) (the partner-onboarding tutorial copy with inline guidance).

Together draft:
- Title.
- Value tier (S/M/L/XS — see the rubric in S3 §4.10).
- Expected outcome (one sentence).
- Acceptance criteria (bulleted; specific; testable).
- What's out of scope.
- Risks / dependencies.
- Long-tail entitlement (only if eligible — most outputs aren't).
- Sign-off.

Commit to `firm/partners/<id>/output-specs/<DATE>--<short-slug>.md`.

### 1:25 — 1:30 — Partner Charter signed

Use [`templates/partner-charter.md`](../templates/partner-charter.md). Both parties sign. Counsel signature line filled if required for the partner's jurisdiction. Store at `firm/partners/<id>/legal/partner-charter-<DATE>.pdf`.

### 1:30 — 1:45 — Tools provisioned (provisioning script)

Run the [provisioning script](../templates/partner-onboarding/provisioning-script.sh):

```bash
cd path/to/oot-framework
./templates/partner-onboarding/provisioning-script.sh <partner_id>
```

The script's interactive prompts:
- Cohort, contact email or wallet address, GitHub username, two-worlds self-id, jurisdiction.
- Confirms inputs.
- Then runs steps 1-8 (Bitwarden, GitHub, Slack/dChat, Drive/PollinationX, Brain folder, Reward Species PDF anchoring, Curator self-test).

Each step pauses for confirmation; the partner watches their email/dMail for the resulting invites.

### 1:45 — 2:00 — Curator self-test (the partner runs this on their own machine)

Per the script's step 7, the partner:
1. Installs the Curator desktop app.
2. Configures cloud-LLM ingest with the firm's API key (founder provides via Bitwarden Send — one-time link).
3. Adds the firm Brain repo as the Curator's sync target.
4. Runs `scan_wiki_health` — should return clean (their freshly-created stub has no issues).
5. Opens `firm/partners/<id>/profile.md` and adds one personal note.
6. Commits, pushes.

**The partner is NOT onboarded** until this step succeeds. If anything fails, the founder helps debug there and then.

---

## Post-session

The provisioning script's step 8 posts the welcome announcement to `#general` (cloud) or 4thtech dChat `#general` (privacy). Updates the firm's `firm/partners/index.md` roster.

---

## First week (steps 16-25)

The partner alone:

1. **Read** the foundation kit (`SPEC.md`, `GENERATIONS.md`, all four governance docs, the Skill Packs relevant to their role). 6-8 hours across the week.
2. **Begin work** on the first Output Spec drafted in the session. R1 captures the first commits/contracts/etc. that evening.
3. **Daily check-in** with founder (15 min) for the first 5 days. Friction points surfaced; not problems, just field reports.
4. **Attend the first Friday Business Review.** Listen. Don't speak much. Read the Brain summary after.

---

## 30-day check-in (steps 26-30)

Founder + partner, ~30 min:

1. **Review the first month's outputs** in `partner-output-ledger.xlsx` Output_Log. Discuss: was value-tier classification accurate? Any mis-captured rows?
2. **Review first variable pay statement** at `firm/partners/<id>/variable-statements/<month>.md`. Discuss any disagreements (Tier-1 dispute if needed).
3. **Confirm Reward Species Declaration is still right.** Renegotiate if the first 30 days revealed a mismatch (per S3 §4.1 renegotiation flow). Update X2 + Brain summary if so.
4. **Two Worlds of Code re-check.** Same partner answers the same 5 questions. If the cohort changed (typical: vibe-coder → transitional after 30 days of agentic exposure), update the partner profile.
5. **Tick off the checklist.** Commit `firm/partners/<id>/onboarding/checklist.md` with `status: complete`.

---

## What the founder watches for

Per [`templates/partner-onboarding/first-90-days.md`](../templates/partner-onboarding/first-90-days.md):

- **Week 1:** does the partner ask questions? Silence is a warning sign.
- **Weeks 2-3:** is the output mix consistent with cohort designation?
- **Weeks 4-5:** does the partner engage with their first variable pay statement? Auto-acknowledgement without inspection is a warning sign.
- **Weeks 6-8:** is the partner contributing to the Brain beyond their own outputs?
- **Weeks 9-12:** is the quarterly check-in productive? Does the partner have framework feedback?

---

## Common pitfalls

**1. Skipping the Manifesto walkthrough.**
- Cause: founder thinks "they'll read it later". They won't, or they'll skim.
- Fix: 30 minutes together, in person. Non-negotiable.

**2. Pre-filled X2 values stick because the partner didn't push back.**
- Cause: power dynamic; the partner doesn't want to seem difficult.
- Fix: founder explicitly invites pushback. *"These are starting values; what would you actually want?"*

**3. First Output Spec is too vague.**
- Cause: time pressure at the end of the 90-min session.
- Fix: schedule 30 more minutes if needed. The first Output Spec is the exemplar; rushing it creates a bad pattern.

**4. Curator self-test fails and the partner starts work anyway.**
- Cause: the partner is excited; the founder is tired.
- Fix: don't start work without working tools. The framework's discipline starts here.

**5. 30-day check-in skipped or rushed.**
- Cause: business busy; check-in feels optional.
- Fix: it's not optional. The first month is when adjustments are cheapest.

---

## When to escalate

- **Partner is a poor fit** (mismatch surfacing in week 1-2): the framework is honest — better to release amicably in week 3 than struggle through month 6. Per the Charter §10 exit terms.
- **Reward Species Declaration disputed** at the 30-day check-in: per `governance/DECISION-RIGHTS.md` Tier 1 first; escalate only if Tier 1 fails.
- **Provisioning script fails** repeatedly: open a GitHub issue with the run log. The script is generated per `PROVISIONING-SPEC.md`; v1.0 has TODO(v1.x) markers that may be the cause.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. The Partner Charter is a template; counsel review for the partner's jurisdiction is mandatory before signature. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md).
