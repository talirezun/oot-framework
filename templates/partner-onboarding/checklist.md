# Partner Onboarding Checklist (30 steps)

Use this checklist when onboarding a new partner. The 90-minute onboarding session covers steps 1-15; steps 16-17 complete end-of-day, right after the session (Curator self-test + welcome announcement); the partner's first week covers steps 18-25; the 30-day check-in covers steps 26-30.

Tick boxes as you complete each step. Commit the completed checklist to `firm/partners/<partner_id>/onboarding/checklist.md`.

---

## Pre-onboarding (founder, 30 min, day before)

- [ ] **1. Verify track readiness.** Cloud track: confirm Anthropic seat budget, GitHub org admin, Slack workspace. Privacy track: confirm always-on machine running, Trezor stock available.
- [ ] **2. Verify cohort decision.** Founder + (if applicable) managing partner agreed on cohort (`full-time-partner | project-specialist | advisor`).
- [ ] **3. Verify initial reward-species fields.** Founder pre-fills (subject to partner negotiation) the X2 row's first-pass: `reward_species`, `base_amount`, `variable_weight_*`, `output_multiplier`, `bonus_split_*`. Partner negotiates within the session.
- [ ] **4. Verify legal posture.** Confirm Partner Charter template is current; counsel sign-off recorded for the partner's jurisdiction (per `governance/DECISION-RIGHTS.md` matrix).
- [ ] **5. Calendar invite sent.** 90 min onboarding session, both parties present.

## The 90-min onboarding session

- [ ] **6. Walk through MANIFESTO.md together.** 30 min. The partner internalises the five theses. Questions invited.
- [ ] **7. Reward Species Declaration.** Open the firm's Ledger copy `firm/excel/reward-species-declaration.xlsx` (X2) — the framework's `templates/excel/` copy is a pristine master; the firm works on its own copy in the Ledger. Add the partner's sheet. Walk through every column. Negotiate where the partner wants different values. Validate sums (variable weights + bonus splits both = 1.0). Save.
- [ ] **8. Two Worlds of Code self-id.** Run the 5-question assessment from S4 §4.9. Record `two_worlds_self_id`.
- [ ] **9. Output Spec for first piece of work.** Open `templates/output-spec.md` (the tutorial copy). Draft together. Commit to `firm/partners/<partner_id>/output-specs/<DATE>--<SHORT_SLUG>.md`.
- [ ] **10. Partner Charter signed.** Print signed PDF from `templates/partner-charter.md`. Both sign. Counsel signature line filled if applicable. Store at `firm/partners/<partner_id>/legal/partner-charter-<DATE>.pdf`.
- [ ] **11. Bitwarden vault provisioned (optional in Gen 1).** Recommended once the firm has a Bitwarden organisation (2+ admins sharing credentials); skip if solo/2-admin — see `governance/SECRETS-POLICY.md` Gen-1 tiering. If provisioning: founder runs `provisioning-script.sh <partner_id>` step 1 (or completes manually per `PROVISIONING-SPEC.md`). Partner receives one-time login token.
- [ ] **12. GitHub access provisioned.** Step 2 of provisioning script. Partner accepts org invite from their email.
- [ ] **13. Slack invite (cloud) / 4thtech onboarding (privacy).** Step 3 of provisioning script.
- [ ] **14. Google Workspace seat (cloud — optional) / PollinationX read access (privacy).** Step 4 of provisioning script. Google Workspace is optional in Gen 1 (read-only Drive connector only; never a state store — see `governance/SECRETS-POLICY.md` and ADR-001) — skip if the firm doesn't use it. PollinationX read access is required on the privacy track.
- [ ] **15. Brain folder stub.** Step 5 of provisioning script. PR opened titled `Onboard partner: <partner_id>`. Partner reviews + acks.

## End of onboarding session

- [ ] **16. Partner runs Curator self-test.** Step 7 of provisioning script. Founder watches. If any step fails, debug there and then. Partner is **not** onboarded until this succeeds.
- [ ] **17. Welcome announcement.** Step 8 of provisioning script. Posted to `#general` (cloud) or 4thtech dChat (privacy). Roster updated.

## First week (partner alone)

- [ ] **18. Read SPEC.md** (~30 min). Technical architecture; the eight-layer model.
- [ ] **19. Read GENERATIONS.md** (~10 min). What's deferred; what's coming.
- [ ] **20. Read governance/KLARNA-TEST.md** (~10 min). The framework's signature discipline.
- [ ] **21. Read governance/DECISION-RIGHTS.md** (~10 min). The three-tier dispute path.
- [ ] **22. Read governance/SECRETS-POLICY.md** (~15 min). Bitwarden + Trezor + Yubikey.
- [ ] **23. Read the relevant Skill Packs.** Whichever Skill Packs the partner's role requires (typically S1 my-curator + S2 context-engineering + S3 compensation-attribution as universal; plus S4 if engineering, S11 if sales, etc.).
- [ ] **24. Attend first Friday Business Review.** Listen. Don't speak much. Watch the structure. Read the Ledger summary after.
- [ ] **25. Begin work on the first Output Spec.** R1 will capture the first commits/contracts/etc. that evening.

## 30-day check-in (founder + partner, 30 min)

- [ ] **26. Review first 30 days of output.** Open the firm's Ledger copy `firm/excel/partner-output-ledger.xlsx` (X1) Output_Log filtered to the partner. Discuss: was the value-tier classification accurate? Anything mis-captured?
- [ ] **27. Review first variable pay statement.** Open the first month's `firm/partners/<partner_id>/variable-statements/<month>.md`. Discuss any disagreements (Tier-1 dispute if needed).
- [ ] **28. Confirm Reward Species Declaration is still right.** Renegotiate if the first 30 days revealed a mismatch. Update X2 + Brain summary if so.
- [ ] **29. Two Worlds of Code self-id check.** Same partner answers the same 5 questions again. If the cohort changed (typical: vibe-coder → transitional after 30 days of agentic-engineer exposure), update the partner profile.
- [ ] **30. Check off this checklist.** Commit to `firm/partners/<partner_id>/onboarding/checklist.md` with `status: complete`.

---

## What happens if a step fails

Each step has an explicit failure mode in `PROVISIONING-SPEC.md`. The framework's discipline: **the partner is not 'onboarded' until step 17 succeeds.** Steps 18-25 (first week) and 26-30 (30-day) are post-onboarding rituals that confirm the partnership is working.

If step 16 or 17 fails repeatedly, the founder pauses the onboarding and investigates. The partner does not start work until they have a working Curator + Brain access + Output Spec for their first piece of work.

---

## Per-cohort variations

- **Full-time partner:** all 30 steps.
- **Project specialist:** steps 1-17 + 25 (first work begins). Steps 26-30 substituted with project-end review.
- **Advisor:** steps 1-15 only. No Brain provisioning beyond a profile page; no Output Specs unless the engagement requires them.
