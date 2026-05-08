# Skill Pack S5 — Reporting & Business Review: SPEC

**ID:** S5
**Name:** Reporting & Business Review
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

The operational heartbeat of an ØØT firm. Replaces status meetings with a Brain-generated agenda for the Friday Business Review. Encodes the daily / weekly / monthly / quarterly cadences, the rolling-forecast principle from Beyond Budgeting, and the per-partner check-in structure.

## Scope

**Covers:**
- Daily ledger update (Routine R1 ownership).
- Friday Business Review agenda generation (Routine R2 ownership).
- Monthly KPI rollup.
- Quarterly partner check-in structure.
- Decision logging in the Brain (every BR decision becomes a versioned Brain page).
- Blocker surfacing (the BR's standing "what's stuck" agenda item).
- Klarna Test status as a standing BR agenda item.

**Does NOT cover:**
- The variable pay calculation itself (that is S3).
- Treasury reporting (that is S10 — Tier 2).
- Long-cycle strategic planning (that is founder-level work, not BR work).

## Allowed tools / dependencies

- Curator MCP tools (read ledger, write BR summaries to Brain).
- Excel MCP / Google Sheets (read X1, write X3).
- Slack / 4thtech (read configured channels for blockers and decisions).
- Calendar MCP (Google Calendar or equivalent — invite the BR meeting).

## Section structure

1. **Purpose**
2. **When to invoke**
3. **When NOT to invoke**
4. **Operational instructions:**
   - 4.1 Daily ledger update (R1 invocation pattern).
   - 4.2 Friday BR agenda generation (R2 invocation; what to include, what to exclude).
   - 4.3 Running the BR (30-minute structure: outputs, blockers, decisions, Klarna Test status, KPI movements).
   - 4.4 BR summary commit to Brain.
   - 4.5 Monthly rollup.
   - 4.6 Quarterly partner check-in structure.
5. **Brain interaction protocol** — writes BR summaries to `firm/business-reviews/<YYYY-MM-DD>.md`; links to ledger, decisions, blockers.
6. **Excel interaction protocol** — reads X1 (ledger) for source data; writes X3 (BR sheet).
7. **Routine integration** — owns R2; reads from R1 output.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts

1. Don't run a status meeting outside the BR — if it's a status update, it goes in the ledger or the BR.
2. Don't extend a BR past 30 minutes — if it's running long, the agenda is wrong.
3. Don't use the BR for personnel discussions — those go in the quarterly check-in.
4. Don't auto-publish BR summaries externally — they may contain sensitive partner-level data.

## Worked examples concept

**Example 1:** Friday morning. R2 fires at 08:00. The pack reads the past week's ledger, surfaces three notable outputs, two blockers, one Klarna Test in progress, KPI movement on customer NPS. Writes the agenda to `business-review.xlsx`, posts a draft summary to Slack `#business-review`. The 14:00 BR meeting works through it. Outcomes are committed to the Brain.

**Example 2:** End of quarter. The pack rolls up 13 BR summaries into a quarterly digest. Founder uses it as input for partner check-ins.

## References

1. Hope, J. & Fraser, R. *Beyond Budgeting: How Managers Can Break Free from the Annual Performance Trap* (2003).
2. Microsoft. *Work Trend Index 2025: The Frontier Firm*.
3. ØØT `MANIFESTO.md`, Thesis 1 — Resistance.
4. ØØT `templates/excel/SPEC.md` (X1, X3 schemas).

## Acceptance criteria

Standard. Plus: 2+ worked examples; sample BR summary template in `examples/`.