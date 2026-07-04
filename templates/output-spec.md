# Output Spec — Partner-Onboarding Tutorial Copy

This is the **annotated tutorial version** of the Output Spec template. New partners use this version during their 90-minute onboarding session to draft their first Output Spec. Once they're comfortable, they switch to the canonical template at `templates/brain/output-spec.md` (which is identical in structure but without the inline guidance).

---

## How to use this template

1. Read the manifesto's Thesis 3 (employees become partners) and the framework's framing of "output, not hours" before drafting.
2. Decide what you're committing to. An Output Spec is **the contract for one piece of work**. It defines what "done" looks like.
3. Fill in the template below. Replace every `{{PLACEHOLDER}}` with your actual value.
4. The founder reviews + accepts (signs off).
5. Commit the Output Spec to the Brain at `firm/partners/<your_id>/output-specs/<DATE>--<SHORT_SLUG>.md`.
6. Begin the work.

The Output Spec is referenced by Routine R1 when it captures your daily output. The Output Spec's **value tier** drives your variable pay.

---

## The template (filled-in example shown after each guidance block)

```yaml
---
title: "Output spec — {{TITLE}}"
slug: partners/{{PARTNER_ID}}/output-specs/{{DATE}}--{{SHORT_SLUG}}
domain: firm
type: output-spec
partner_id: {{YOUR_PARTNER_ID}}
value_tier: {{S | M | L | XS}}
created: {{TODAY}}
updated: {{TODAY}}
authors: [{{YOUR_PARTNER_ID}}]
# attribution_split: OPTIONAL. Only for co-authored outputs where the co-authors
# have agreed a non-even split. Maps partner_id -> fraction (must sum to 1.0).
# R1 writes each co-author's fraction into X1 column N (weight); if omitted, R1
# defaults to an even 1/N split across `authors`. Example:
# attribution_split: {mira-tek: 0.7, davor-krznar: 0.3}
status: drafted
expected_outcome: "{{ONE_SENTENCE_OUTCOME}}"
outcome_review_date: {{REVIEW_DATE}}
linked_pr_or_contract: "TBD"
---
```

> 💡 **Guidance — attribution_split (co-authored outputs only, ADR-005):**
> If two or more partners co-author this output, R1 shares the value envelope across them instead of paying each the full amount. By default the split is even (`1/N`). Only add the optional `attribution_split` field when the co-authors have agreed an *uneven* split — e.g. `attribution_split: {mira-tek: 0.7, davor-krznar: 0.3}`. The fractions must sum to `1.0`. R1 writes each partner's fraction into their `weight` (column N) row in the output ledger. Single-author outputs never need this field.

> 💡 **Guidance — value_tier:**
> - **S** (€8,000 envelope): a flagship piece of work that takes weeks. Major feature, multi-year customer contract, foundational architecture.
> - **M** (€2,000): a significant piece of work that takes days-to-weeks. Substantial feature, standard customer contract, refactor of an existing system.
> - **L** (€500): a typical 1-3 day commit, a routine review, a standard contract execution. The default if no Output Spec exists.
> - **XS** (€100): bug fix, dependency bump, routine touch.
>
> Be honest. Underestimating doesn't help (you'll be paid less than the work warrants); overestimating is dishonest (and the Klarna Test discipline applies to the framework itself — value tiers are never inflated to compensate partners).
>
> The value tier can be **refined as outcomes come in** (see "Long-tail entitlement" section below). The variable-pay tier is set at drafting; long-tail outcome can be S even if variable was M.

```markdown
# Output spec — {{TITLE}}

**Partner:** [[partners/{{YOUR_PARTNER_ID}}]]
**Drafted:** {{TODAY}}
**Value tier:** {{TIER}} (envelope {{ENVELOPE}})
**Expected outcome:** {{EXPECTED_OUTCOME}}
**Outcome review date:** {{REVIEW_DATE}}

## What "done" looks like

{{ACCEPTANCE_CRITERIA}}
```

> 💡 **Guidance — acceptance criteria:**
> - Specific. Testable. Unambiguous.
> - Bullet list. Each bullet is one criterion.
> - "All unit tests pass" — yes. "Code is good" — no.
> - "Customer NPS on the new feature ≥ 70 within 30 days of launch" — yes. "Customers like it" — no.
>
> If you cannot articulate "done" in concrete bullets, the work is not yet ready for an Output Spec. Iterate the spec before starting the work.

```markdown
## What's explicitly out of scope

{{OUT_OF_SCOPE}}
```

> 💡 **Guidance — out of scope:**
> - The clarifying counterpart of "what done looks like".
> - Things that *might* be expected but are NOT part of this output.
> - Example: building OAuth2 PKCE for partner onboarding has out-of-scope: "this does not include OAuth provider selection UI; this does not include email-magic-link flows; those are separate Output Specs."
>
> Out-of-scope is the framework's anti-scope-creep discipline. If a question comes up mid-work that's "should this be in here?", the answer is in the Output Spec.

```markdown
## Risks / dependencies

{{RISKS}}
```

> 💡 **Guidance — risks:**
> - Technical risks: dependencies on external systems, library upgrades, data migration.
> - Business risks: customer-facing changes, contract implications.
> - Schedule risks: critical-path dependencies on other partners.
> - Each risk: brief description + mitigation plan or "accepted risk".

```markdown
## Long-tail entitlement (if applicable)

If this output is eligible for long-tail entitlement:

- **Outcome metric:** {{OUTCOME_METRIC}} (the realised value attributable to this output, measured at quarterly settlement)
- **Partner share %:** {{PARTNER_SHARE}}
- **Settlement period:** quarterly
- **Long-tail end date or "ongoing":** {{LONG_TAIL_END}}
```

> 💡 **Guidance — long-tail eligibility:**
> Most outputs are NOT long-tail eligible. Long-tail is for outputs whose value compounds over time:
> - A multi-year customer contract → revenue per quarter.
> - A foundational architecture choice → cost savings per quarter.
> - A flagship feature → customer-acquisition or retention impact per quarter.
>
> A bug fix is not long-tail eligible. A routine PR is not long-tail eligible.
>
> If the output IS eligible, propose terms here. The founder reviews. Both agree at the next BR (Skill Pack S5). Recorded in your `reward-species-declaration.xlsx` Long_Tail_Schedule sheet.
>
> Typical partner share: 5-15%. Above 25% is rare and the framework's authors find it creates incentive distortions.

```markdown
## Sign-off

- Drafted by: [[partners/{{YOUR_PARTNER_ID}}]] on {{TODAY}}
- Accepted by: [[partners/{{ACCEPTOR_ID}}]] on {{ACCEPTANCE_DATE}}
- Shipped: {{SHIP_DATE | "not yet"}}
```

> 💡 **Guidance — sign-off:**
> The founder (or the partner with relevant authority — typically the founder for Output Specs above L tier; a senior partner for L and XS) accepts the spec. The "accepted by" line records this.
>
> Once accepted, the spec is locked. Material scope changes require an updated spec (or an explicit decision in `firm/decisions/`).

---

## Worked example — a real Output Spec

**Title:** OAuth2 PKCE flow for partner onboarding.
**Partner:** Mira Tek.
**Value tier:** M (€2,000 envelope).
**Drafted:** 2026-05-10.

```markdown
---
title: "Output spec — OAuth2 PKCE flow for partner onboarding"
slug: partners/mira-tek/output-specs/2026-05-10--oauth2-pkce
domain: firm
type: output-spec
partner_id: mira-tek
value_tier: M
created: 2026-05-10
updated: 2026-05-10
authors: [mira-tek]
status: accepted
expected_outcome: "Partner-onboarding flow protected against OAuth2 authorisation-code interception via PKCE; no impact on UX; existing sessions continue to work."
outcome_review_date: 2026-08-10
linked_pr_or_contract: "PR #1502 (TBD)"
---

# Output spec — OAuth2 PKCE flow for partner onboarding

**Partner:** [[partners/mira-tek]]
**Drafted:** 2026-05-10
**Value tier:** M (envelope €2,000)
**Expected outcome:** Partner-onboarding flow protected against OAuth2 authorisation-code interception via PKCE; no impact on UX; existing sessions continue to work.
**Outcome review date:** 2026-08-10

## What "done" looks like

- PKCE protection enabled in NextAuth configuration.
- Client-side PKCE code-verifier generation working in `src/auth/login.tsx`.
- Authorization request sends code-challenge.
- Token exchange validates code-verifier (length + match).
- Existing OAuth tests pass.
- New PKCE-specific tests added: code-verifier mismatch is rejected; code-verifier length validation works; full PKCE round-trip integration test.
- ADR committed at `firm/architecture/ADR-2026-014.md`.
- No regression in onboarding cycle time (measured baseline: 4.2 min average).

## What's explicitly out of scope

- OAuth provider selection UI (this is a separate ongoing piece of work).
- Email-magic-link auth flow (separate Output Spec).
- Mobile app PKCE support (covered by a future Output Spec when mobile launches).
- Changes to the partner-onboarding email content or copy.

## Risks / dependencies

- **Risk:** existing user sessions invalidate on deploy if migration handled incorrectly. **Mitigation:** dual-support during migration window (NextAuth handles both PKCE-protected and pre-PKCE flows for 14 days post-deploy).
- **Risk:** Redis-based PKCE state store has TTL implications. **Mitigation:** explicit 10-min TTL configured.
- **Dependency:** NextAuth v4.24+ required (verified — we are on v4.31).

## Long-tail entitlement

Not applicable. This is security hardening, not value-compounding work.

## Sign-off

- Drafted by: [[partners/mira-tek]] on 2026-05-10
- Accepted by: [[partners/founder-tali]] on 2026-05-10
- Shipped: 2026-05-13
```

---

## What happens next

1. **R1 captures your work** when commits land referencing the Output Spec.
2. **Variable pay calculation (R3)** at month-end uses your Output Spec's value_tier × your `output_multiplier` (from your Reward Species Declaration) to compute your variable.
3. **The Output Spec stays in the Brain** as the canonical record of what you committed to.
4. **At quarterly check-in (S5 §4.6)** the founder reviews your output mix, your value tier accuracy, your output velocity. The Output Spec is the source of truth for these conversations.

The Output Spec is the framework's most important per-partner artefact. Take time on it. The first one is the hardest; subsequent ones flow naturally.
