"""Structural tests for the committed Excel templates + build_excel.py.

These assert against the COMMITTED templates/excel/*.xlsx files. They do NOT run
the generator by default (that would mutate the working tree). One opt-in test
regenerates and restores via git checkout in a finally block.

Contracts checked (see templates/excel/SPEC.md):
  - All 9 workbooks exist and open.
  - X1 (partner-output-ledger) Output_Log has K2/L2 formulas
    (value_envelope VLOOKUP + computed_variable with the rework zero-out).
  - X4 (klarna-test) Klarna_Score L2 == "=SUM(B2:K2)" and the >=14 threshold
    is present (Decision_Log I2 formula + Klarna_Score conditional formatting).
  - X9 (oot-readiness) Scoring dimension SUM formulas exist.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from openpyxl import load_workbook

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCEL_DIR = REPO_ROOT / "templates" / "excel"

EXPECTED_WORKBOOKS = [
    "partner-output-ledger.xlsx",
    "reward-species-declaration.xlsx",
    "business-review.xlsx",
    "klarna-test.xlsx",
    "metr-baseline.xlsx",
    "agent-skill-roi.xlsx",
    "eu-ai-act-mapping.xlsx",
    "treasury-runway.xlsx",
    "oot-readiness.xlsx",
]


def test_build_excel_importable():
    """The generator module must import cleanly (used by CI + oot-build-excel)."""
    import importlib.util

    path = REPO_ROOT / "scripts" / "build_excel.py"
    spec = importlib.util.spec_from_file_location("build_excel", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    assert hasattr(module, "main")
    # It knows where to write.
    assert module.TEMPLATE_DIR.name == "excel"


@pytest.mark.parametrize("name", EXPECTED_WORKBOOKS)
def test_workbook_exists_and_opens(name):
    path = EXCEL_DIR / name
    assert path.exists(), f"{name} missing from templates/excel/"
    wb = load_workbook(path, data_only=False)
    assert "_metadata" in wb.sheetnames, f"{name} missing hidden _metadata sheet"
    assert "README" in wb.sheetnames, f"{name} missing README sheet"


def test_all_nine_present():
    found = sorted(p.name for p in EXCEL_DIR.glob("*.xlsx"))
    for name in EXPECTED_WORKBOOKS:
        assert name in found, f"{name} not found in {found}"
    assert len(found) == 9, f"expected exactly 9 workbooks, found {len(found)}: {found}"


def test_x1_output_log_formulas():
    """X1 Output_Log K2 = value_envelope VLOOKUP; L2 = computed_variable with rework zero-out."""
    wb = load_workbook(EXCEL_DIR / "partner-output-ledger.xlsx", data_only=False)
    ws = wb["Output_Log"]

    k2 = str(ws["K2"].value or "")
    assert k2.startswith("=VLOOKUP("), f"X1 K2 not a VLOOKUP: {k2!r}"
    assert "$O$2:$P$5" in k2, f"X1 K2 does not reference the envelope table: {k2!r}"

    l2 = str(ws["L2"].value or "")
    assert l2.startswith("="), f"X1 L2 not a formula: {l2!r}"
    assert "K2" in l2 and "J2" in l2, f"X1 L2 missing K/J references: {l2!r}"
    # The rework-within-30d zero-out (I2="Yes" => 0).
    assert 'IF(I2="Yes",0,1)' in l2.replace(" ", ""), f"X1 L2 missing rework zero-out: {l2!r}"


def test_x4_klarna_score_total_and_threshold():
    """X4 Klarna_Score L2 == '=SUM(B2:K2)'; the >=14 threshold is present."""
    wb = load_workbook(EXCEL_DIR / "klarna-test.xlsx", data_only=False)
    ks = wb["Klarna_Score"]

    l2 = str(ks["L2"].value or "").replace(" ", "")
    assert l2 == "=SUM(B2:K2)", f"X4 Klarna_Score L2 not =SUM(B2:K2): {l2!r}"

    # data_only must be None (openpyxl writes no cached value) — this is exactly
    # why the klarna-gate workflow needs a recompute fallback.
    wb_cached = load_workbook(EXCEL_DIR / "klarna-test.xlsx", data_only=True)
    assert wb_cached["Klarna_Score"]["L2"].value is None

    # Threshold 14 lives in Decision_Log I2 (PROCEED/HOLD) ...
    dl = wb["Decision_Log"]
    i2 = str(dl["I2"].value or "")
    assert "H2>=14" in i2.replace(" ", ""), f"X4 Decision_Log I2 missing >=14 threshold: {i2!r}"

    # ... and in the Klarna_Score total conditional formatting.
    cf_formulas = []
    for rng, rules in ks.conditional_formatting._cf_rules.items():
        if "L2" in str(rng.sqref):
            for rule in rules:
                cf_formulas.extend(str(f) for f in (rule.formula or []))
    assert any("14" in f for f in cf_formulas), (
        f"X4 Klarna_Score total conditional formatting does not reference 14: {cf_formulas}"
    )


def test_x9_dimension_sums():
    """X9 Scoring sheet has per-dimension SUM formulas + a grand total."""
    wb = load_workbook(EXCEL_DIR / "oot-readiness.xlsx", data_only=False)
    sc = wb["Scoring"]

    # B2..B5 = per-dimension sums over the Questions responses.
    for r in range(2, 6):
        val = str(sc.cell(row=r, column=2).value or "")
        assert val.startswith("=SUM(Questions!"), (
            f"X9 Scoring B{r} not a dimension SUM: {val!r}"
        )
    # B6 = grand total across the four dimensions.
    b6 = str(sc["B6"].value or "").replace(" ", "")
    assert b6 == "=SUM(B2:B5)", f"X9 Scoring B6 not the grand total: {b6!r}"


def test_regenerate_matches_committed_optional():
    """Opt-in: regenerate and confirm no drift, then restore the committed tree.

    Skipped unless OOT_RUN_GENERATOR=1 so the default suite never mutates the
    working tree. Mirrors the excel-validation.yml drift check.
    """
    import os

    if os.environ.get("OOT_RUN_GENERATOR") != "1":
        pytest.skip("set OOT_RUN_GENERATOR=1 to run the mutating drift check")

    import shutil
    import tempfile
    import importlib.util

    backup = Path(tempfile.mkdtemp(prefix="oot-committed-xlsx-"))
    try:
        for p in EXCEL_DIR.glob("*.xlsx"):
            shutil.copy2(p, backup / p.name)

        spec = importlib.util.spec_from_file_location(
            "build_excel", REPO_ROOT / "scripts" / "build_excel.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()

        diffs = []
        for name in EXPECTED_WORKBOOKS:
            a = load_workbook(backup / name, data_only=False)
            b = load_workbook(EXCEL_DIR / name, data_only=False)
            assert a.sheetnames == b.sheetnames, f"{name}: sheet names drifted"
            for sheet in a.sheetnames:
                wsa, wsb = a[sheet], b[sheet]
                mr = max(wsa.max_row, wsb.max_row)
                mc = max(wsa.max_column, wsb.max_column)
                for r in range(1, mr + 1):
                    for c in range(1, mc + 1):
                        if sheet == "_metadata" and r == 3 and c == 2:
                            continue  # generation_date legitimately changes
                        va = wsa.cell(row=r, column=c).value
                        vb = wsb.cell(row=r, column=c).value
                        if va != vb:
                            coord = wsa.cell(row=r, column=c).coordinate
                            diffs.append(f"{name}[{sheet}]!{coord}: {va!r} != {vb!r}")
        assert not diffs, "drift detected:\n" + "\n".join(diffs[:50])
    finally:
        # Restore the committed workbooks so the working tree is left clean.
        subprocess.run(
            ["git", "checkout", "--", "templates/excel/"],
            cwd=REPO_ROOT,
            check=False,
        )
        shutil.rmtree(backup, ignore_errors=True)
