# Example 2 — A BR where the agenda was wrong

A worked example of the §4.7 "BR ran long" diagnostic in action.

## The setup

Same 8-partner firm. Friday 14:00. R2 has populated X3 with **8 decisions due**.

| # | Decision | Pre-read state |
|---|---|---|
| 1 | Unit Fund pilot Q3 launch | Pre-read in Brain ≥24h prior ✓ |
| 2 | Stripe → Adyen | Pre-read partial; ADR not yet drafted |
| 3 | Office space lease renewal | Pre-read absent (Tali surfaced it 2h ago) |
| 4 | New customer-success specialist hire | Pre-read absent |
| 5 | EU AI Act risk register Q1 review | Pre-read in Brain ✓ |
| 6 | Code review tool replacement | Pre-read partial |
| 7 | Conference attendance budget | Pre-read absent |
| 8 | Customer-tier pricing change | Pre-read in Brain ✓ |

## What goes wrong

Mira (facilitator) starts on time. The 10-min outputs block runs to 12 (Tali asks questions about the Acme MSA). Blockers: 6 min. Decisions block opens at 14:18 — already 4 min over.

**Decision #1 (Unit Fund):** takes **22 minutes**. Real questions, deep discussion, no clean conclusion. Decision deferred to next week.

It's now 14:40. The remaining 7 decisions are stacked. 3 of them have no pre-read.

Mira makes the call: **stop the meeting**.

> "We're at 40 minutes. The Unit Fund discussion was valuable but the agenda was wrong. I'm closing the meeting now and we'll diagnose at the start of next week's BR."

She closes. The remaining 7 decisions are tabled.

## Friday 14:45 — Mira opens the post-meeting Brain page

She writes the summary as normal, then adds a `## Diagnostic note` section:

```markdown
## Diagnostic note

This BR ran 40 min (10 over). §4.7 diagnostic:

- **Was the agenda overstuffed?** YES. 8 decisions in a 10-min block is impossible (~1 min each is unrealistic for any non-trivial decision).
- **Was a decision under-prepared?** YES. Decisions 3, 4, 7 had no pre-read in Brain ≥24h prior; should not have been on the agenda.
- **Was one partner dominating?** No — the Unit Fund discussion was genuinely 5-way.
- **Was the BR being used as a 1-1 substitute?** No.

**Root cause:** the firm's "decision queue" hit 8 simultaneously this week without triage. The pre-read discipline (decisions on BR agenda only after Brain pre-read committed ≥24h prior) was not enforced for 3 of them.

**Remediation for next BR (2026-04-24):**
1. Triage the 7 tabled decisions before next BR. Owner: founder-tali. Deadline: 2026-04-22.
2. Apply the pre-read rule strictly: any decision without ≥24h Brain pre-read does not appear on the agenda. Tali and Mira both enforce.
3. Working session for the Unit Fund discussion separately from BR (longer format, dedicated). Owner: founder-tali. Date: 2026-04-23 14:00.
```

Signed commit: `phase-br: 2026-04-17 BR summary + ran-long diagnostic; 7 decisions tabled`.

## Friday 17:00 — Tali responds

Tali reads the Brain page. Sees the diagnostic. Posts to `#business-review`:

> Mira's call to stop today's BR was correct. Acknowledging the agenda was overstuffed because I let the decision queue accumulate without triage. Working session on Unit Fund 2026-04-23 14:00 (calendar invite landing today). Will triage the remaining 6 by Tuesday so next Friday's BR is clean. Sorry team.

## The next week's BR (2026-04-24)

R2 fires at 08:00. The Decisions_Due block has **3** items (Tali's triage decided 4 of the prior week's 7 didn't actually need BR-level discussion; one was Tier-2 dispute material; one was already accepted-in-principle pending an ADR; one needed counsel input first). The Unit Fund had its own working session on 2026-04-23 — a Brain decision page now exists, and the BR-level item is "approve the working session's outcome", which is a 2-minute confirmation.

The 2026-04-24 BR runs 26 minutes. Clean. The diagnostic from the prior week is referenced in passing during Mira's facilitator-opening: *"Last week we ran long; today's agenda has 3 decisions, all pre-read. Let's see how it goes."*

## What this example demonstrates

- **The 30-minute discipline is enforced by stopping the meeting**, not by accelerating through the agenda.
- **The diagnostic is a Brain artefact**, not a verbal acknowledgement that disappears.
- **Founder accountability** — Tali surfaces in `#business-review` that the decision queue mismanagement was on him; the partnership sees the correction.
- **Discrete remediations** — triage, working session for the long discussion, pre-read enforcement going forward.
- **Most decisions don't actually need a BR.** The triage step revealed 4 of 7 weren't BR-level. The framework's discipline pushes the partnership toward asynchronous, Brain-anchored decisions where possible.
- **The next week is clean.** The diagnostic worked.
