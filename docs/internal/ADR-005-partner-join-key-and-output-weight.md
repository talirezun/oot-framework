# ADR-005 — X2 gains a partner join key; X1 gains an output weight (multi-author fix)

**Status:** Accepted 2026-07-04.
**Deciders:** Dr. Tali Režun (initiator) + framework maintainers.
**Related:** ADR-001 (Excel writeback), ADR-004 (appended-row contract).

## Context

Two schema ambiguities become real defects the day a firm has its second partner:

1. **No partner join key.** R1/R3 must read "X2's `output_multiplier` for *that partner*" and R4 must settle long-tail "per partner" — but `Base_Variable_Split` and `Long_Tail_Schedule` have no partner column. With one partner (the shipped sample) the lookup is degenerate-unambiguous; with two it is undefined. No per-partner sheet-naming convention exists either.
2. **Co-authored outputs double-pay.** R1 writes "one row per partner with a fractional output_value note" — but the fraction lives in the free-text `notes` column while the K formula grants each co-author the **full** value envelope. Two co-authors on one Large output each receive 100% of €2,000.

## Decision

1. **`partner_id` becomes the universal join key.** `Partner_Profile` column A (`partner_id`, format `P-NNN`) is canonical. `Base_Variable_Split` and `Long_Tail_Schedule` each gain a **leading `partner_id` column**; both stay **single shared sheets** with one row per partner (Base_Variable_Split) / per partner-artifact (Long_Tail_Schedule). Per-partner *sheets* are explicitly rejected: openpyxl append logic, named ranges, and cross-sheet formulas all get simpler with row-wise partitioning, and the sheet already is a review surface filtered by column. R1/R3/R4 lookups join on `partner_id`; X1's column B (`partner_id`) already exists and now resolves against X2 unambiguously.
2. **X1 Output_Log gains column N — `weight`.** Number in (0, 1], default `1.0`. For a co-authored output R1 writes one row per co-author with `weight = 1/N` (or explicit fractions when the partners have agreed a split in the output spec — the output spec template gains an optional `attribution_split` field). The computed-variable formula L becomes `=K·J·N-weight·IF(rework…)` so the envelope is *shared*, not duplicated. The appended-row contract (ADR-004) covers N: literal, routine-written, defaults 1.0. Column N is free in the current layout (data ends at M; the envelope lookup table sits at O1:P5).
3. **Migration for existing Gen-1 workbooks** (few, early): insert column N in Output_Log with `1.0` for all existing rows and update the L formula fill; insert the `partner_id` column at A in the two X2 sheets and backfill from Partner_Profile (single-partner firms: every row gets `P-001`). A migration note ships in the Excel SPEC; no automated migrator in Gen 1.

## Consequences

`templates/excel/SPEC.md` (schemas + contracts + migration note), `scripts/build_excel.py` (columns, L-formula, validation, CF ranges that shift with the new leading column, sample data), regenerated X1/X2, `routines/SPEC.md` + `cloud/R1.md`/`R3.md`/`R4.md` (join + weight semantics; the "fractional note" instruction replaced), `templates/output-spec.md` (optional `attribution_split`), S3 SKILL §4.3 (weight discipline; the multi-author double-pay warning becomes a resolved rule), and `tests/test_build_excel.py`. The X5 perception survey and other workbooks are untouched.
