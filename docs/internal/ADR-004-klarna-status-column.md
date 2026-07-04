# ADR-004 — X4 gains a `status` lifecycle column; the appended-row contract becomes explicit

**Status:** Accepted 2026-07-04.
**Deciders:** Dr. Tali Režun (initiator) + framework maintainers.
**Related:** ADR-001 (Excel writeback). Resolves the "Known schema gap" TODOs placed 2026-07-04 in `routines/SPEC.md`, `routines/cloud/R7.md`, `routines/cloud/R2.md`.

## Context

R7's prompt appends a Decision_Log row "with status='scoring'" and later "updates status to proceeded/held"; R2 reads X4 "for tests in scoring | remediation | monitoring state". But `klarna-test.xlsx` Decision_Log has columns A–L only — **no status column exists**, and the nearest candidate, column I (`decision`), is a formula cell (`=IF(H≥14,"PROCEED","HOLD")`) that a literal write would clobber. The Klarna lifecycle state machine has no Excel home. Separately, R7 replicated the Finding-6 bug class: it never wrote the H/I/K formulas or the F/G reviewer columns on rows it appends.

## Decision

1. **X4 Decision_Log gains column M — `status`.** Literal enum, never a formula: `scoring | remediation | monitoring | proceeded | held`. Data validation enforces the enum. `decision` (column I) remains formula-driven and answers a different question: I is the *threshold verdict* (what the score says); M is the *lifecycle state* (where the process is). They are allowed to disagree transiently (e.g. I=PROCEED while M=monitoring during the 90-day review window).
2. **State semantics:** R7 writes `scoring` on row creation → the scoring session's outcome moves it to `proceeded` (I=PROCEED, work ships), `remediation` (I=HOLD, gaps being fixed for a re-score), or `held` (I=HOLD, decision stands) → `proceeded` rows become `monitoring` until the column-K review date passes, then close back to `proceeded`. R2's weekly read surfaces every row with M ∈ {scoring, remediation, monitoring}. Post-meeting M updates are made by R2's writeback or by a human in the sheet — both legitimate per ADR-001 (spreadsheets are review-and-edit surfaces).
3. **The appended-row contract is now a required SPEC section per workbook.** Every workbook whose rows are appended by a Routine gets an explicit "Appended-row contract" block in `templates/excel/SPEC.md` listing, per column: literal-written-by-routine / formula-the-routine-MUST-write / human-only. First consumers: X1 (R1 — the original Finding-6 fix, now generalised), X4 (R7 — writes A–G literals incl. `scorer` and `non_beneficiary_reviewer`, H/I/K formulas, M=`scoring`), X8 (R8 — MUST append the day's Cash_Position row before computing burn, and write the D/G formulas on the appended Runway_Calc row).
4. **R8 becomes visible to the Article-12 audit trail:** R8 additionally writes a one-paragraph markdown snapshot to `firm/treasury/<YYYY-MM-DD>.md` in the Ledger (same commit), so R6's audit capture — which scans Ledger markdown paths — sees treasury activity. R6's path list gains `firm/treasury/` plus the R3/R4 statement paths it was missing.
5. **The `oot/klarna-test` gate workflow is unaffected** — it reads Klarna_Score directly and never consults `status`.

## Consequences

`templates/excel/SPEC.md` (column M + contract sections), `scripts/build_excel.py` (column, validation, sample row), regenerated X4, `routines/SPEC.md` + `cloud/R7.md` + `cloud/R2.md` + `cloud/R8.md` + `cloud/R6.md` contract updates, S3/S4 references where they describe the R7 flow, and `tests/test_build_excel.py` assertions. Existing firm workbooks: add column M manually or via the one-liner in the migration note (new column at M, header `status`, validation list; no formula changes needed).
