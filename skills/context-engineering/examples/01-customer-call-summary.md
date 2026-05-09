# Example 1 — Customer-call summary prompt (the canonical worked example)

A complete worked example of the five-step prompt skeleton applied to one of the most common partner tasks: turning a customer-call transcript into a decision-quality summary.

## The starting state

A partner just finished an hour-long call with a customer. They have a transcript (~6,000 words). They need a summary to send to the founder this afternoon.

## The constructed prompt (v0.2.1, lives at `firm/prompts/customer-call-summary.md`)

```markdown
## Goal
Summarise the attached call transcript into a decision-quality memo for the founder, surfacing every commitment made by either party.

## Context
- Customer profile: [[customers/acme-corp]]
- Prior interaction history: [[customers/acme-corp/interactions]]
- The transcript is below in the user-message section.

## Constraints
- Maximum 250 words.
- Identify each speaker by role, not by name (Customer / Founder).
- Flag any statement that sounds like a verbal contract.
- Do not editorialise; the founder will form their own view.
- All commitments must include: who, what, by when.

## Format
Markdown.
- H2 "Decisions made" — bullet list, each commitment with owner + deadline.
- H2 "Open questions" — bullet list.
- H2 "Customer signals" — three bullets max, surface only meaningful affect or strategic signals.
- Frontmatter: `type=customer-summary, customer_slug=acme-corp, call_date=YYYY-MM-DD`.

## Self-Check
- Does the output include every commitment made by either party? If unsure, revise.
- Is each commitment ascribed to a specific owner with a specific date?
- Is the word count under 250?
- Is there any editorial language ("the customer was clearly excited...")? If yes, remove.
- Did I respect the "do not name the speakers" rule?
If any check fails, revise once before returning.
```

## The produced output (a typical good run)

```markdown
---
type: customer-summary
customer_slug: acme-corp
call_date: 2026-04-22
authors: [partner-mira-tek]
evaluation_tier: 1
---

## Decisions made

- **Customer:** will sign the renewal at the existing tier by 2026-05-15.
- **Founder:** will deliver an updated technical proposal for the additional API quotas by 2026-05-08.
- **Both parties:** agreed to a 30-minute scoping call for the new analytics module on 2026-05-12 at 14:00 CEST.

## Open questions

- The customer's data-residency requirements are unclear; need clarification before proposal.
- The integration timeline is implicitly Q3 2026 but not committed.

## Customer signals

- Procurement is unusually slow this cycle; finance review is bottleneck.
- New CTO mentioned twice, in evaluative tone — relationship inheritance worth confirming.
- Renewed interest in the privacy-track features post-DORA-2025 reading.
```

## What the prompt's authors got right

- **Goal is one sentence in imperative voice.** Easy for the model to anchor on.
- **Context references the Brain rather than pasting.** The prompt assumes the customer page is in the Brain (it is); the model uses the wikilink at runtime.
- **Constraints are concrete and testable.** "Max 250 words" not "concise"; "no editorial language" with examples.
- **Format is exact.** Frontmatter schema specified; H2 sections named.
- **Self-Check is the most powerful section.** The model performs the check before returning; if any item fails, it revises once.

## What went wrong in v0.1.0 (changelog excerpt)

The original prompt didn't have the "do not name the speakers" rule. The model named the customer's procurement officer in the summary; that summary went to the founder; the founder forwarded it (without the partner's review) to a third party who knew the procurement officer; awkward conversation followed. v0.2.0 added the rule. v0.2.1 added the explicit Self-Check item to enforce it.

## Pre-commit evaluation

- **Tier:** 1 (internal artefact; no customer-facing redistribution).
- **Pass:** all five Self-Check items satisfied; format matches; word count 178; no broken wikilinks.
- **Brain commit:** `customers/acme-corp/summaries/2026-04-22.md`.
