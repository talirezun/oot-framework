# Install test report — 2026-05-10 (cloud-track Path A)

**Tester:** Claude Code (Opus 4.7) driving its own `installer/agent-assisted/cloud-install-plan.md` against a sandbox on the framework's authors' machine.
**Sandbox:** `/tmp/oot-test-install/` with a bare local git remote at `/tmp/oot-test-install/oot-brain-remote/` simulating GitHub. Cleaned up after the test.
**Outcome:** Path A is structurally sound. Pattern C works mechanically. **8 findings**, of which 1 is a real bug in the framework (formula-write gap in R1) and 7 are docs / install-plan refinements that would have tripped a less-technical founder running the plan against a fresh machine.

---

## What was tested

- Step 0.1 preflight (tool checks)
- Step 4.4-4.6 Brain folder scaffold + Excel template copy + initial commit
- Step 8 (proxy) — **Pattern C end-to-end**: open X1 with openpyxl, resolve partner_multiplier from X2 at write time, append a row to Output_Log, save, re-open, verify named ranges + conditional formatting + row count
- Step 10.1 smoke test — open all 9 `.xlsx` files via openpyxl

## What was NOT tested (requires real third-party access)

- Real GitHub repo creation (`gh repo create`)
- Real branch protection API call
- Real `gpg --quick-generate-key` (gpg not installed on this machine)
- Real `gh gpg-key add`
- Curator desktop app install (cloud-LLM ingest API key required)
- Claude Desktop MCP wiring (would need Claude Desktop already running)
- Claude Code Routine creation via `/schedule` (would consume the user's daily Routine quota)
- Slack channel creation / Claude integration

These are the steps that need a "live install on a fresh machine" to surface their rough edges. Recommended for the next iteration of the install-path overhaul.

---

## Findings

### Finding 1 — `python3` resolves to system Python 3.9.6 on macOS, but 3.13 is installed under `/opt/homebrew/bin/python3.13`

Step 0.1 of the cloud install plan currently says "if `python3 --version` is < 3.13, abort." On a typical macOS machine where the user installed Python 3.13 via Homebrew, `python3` still resolves to the system 3.9.6, so the plan would falsely abort.

**Fix:** Step 0.1 should try `python3.13`, `python3.12`, `python3.11`, `python3` in that order and use whichever first satisfies `requires-python`. **Severity:** medium — would not produce a wrong install but produces an unnecessary error.

### Finding 2 — `pyproject.toml` says `requires-python = ">=3.11"` but CLAUDE.md and the install plan say `>=3.13`

Inconsistency. Either CLAUDE.md is stricter than the actual code requires, or `pyproject.toml` is laxer than the framework's standard. The framework's tooling (`ruff`, `black`, `mypy`) is configured for `py313`, suggesting 3.13 is the target.

**Fix:** Decide canonically. Recommend updating `pyproject.toml` to `requires-python = ">=3.13"` to match CLAUDE.md and the install plan. Or relax the install plan to `>=3.11` if 3.11 is genuinely sufficient. **Severity:** low — currently no observable failure.

### Finding 3 — `gpg`, `gh`, `jq` not installed by default on macOS; install plan doesn't tell user how to install them

On a clean macOS install, none of these CLIs are present. The install plan's Step 0.1 detects this but its remediation message is generic ("install per upstream docs"). For less-technical founders, surfacing the per-OS install command saves several minutes of confusion.

**Fix:** Step 0.1 should inline:
- macOS: `brew install gnupg gh jq` (after `brew install` itself if Homebrew missing)
- Linux: `sudo apt install gnupg gh jq` (or `dnf` per distro)
- Windows / WSL: `winget install` or per official upstream

**Severity:** medium — common first-day friction.

### Finding 4 — `openpyxl` is not pre-installed for Python 3.13; install plan doesn't have a "install dependencies" step

Pattern C requires openpyxl. The plan currently assumes it's available but never installs it. On Homebrew Python 3.13, `pip install --user openpyxl` is also rejected by PEP 668.

**Fix:** Add a Step 0.4 to the install plan:
```
0.4 — Set up Python virtual environment for the framework
- python3.13 -m venv ~/.oot/venv
- source ~/.oot/venv/bin/activate
- pip install -e <FRAMEWORK_REPO>     # or: pip install openpyxl pyyaml
```
Or use `uv venv` if `uv` is installed (faster).

The Routines themselves run on Anthropic infrastructure (cloud track) or against `llmster` (privacy track) — Anthropic's runtime has openpyxl available; `llmster` users need to ensure their always-on machine has it. So the venv requirement is for the *install-time agent's* code-execution sandbox + for any local human-in-the-loop work.

**Severity:** medium — install would otherwise stop at the first `python` invocation that imports openpyxl.

### Finding 5 — Homebrew Python 3.13 enforces PEP 668; `pip install --user` fails

Related to Finding 4. The install plan must use a venv or `uv` rather than `pip install --user`.

**Fix:** see Finding 4. Plus a brief explainer: "Python 3.13 from Homebrew enforces PEP 668 — you can't `pip install --user` directly. We use a venv at `~/.oot/venv` for the framework's Python deps."

**Severity:** medium — same impact as Finding 4.

### Finding 6 — CRITICAL: R1's appended X1 rows do NOT have K (`value_envelope`) or L (`computed_variable`) formulas populated

Pattern C is structurally sound. openpyxl mutates the `.xlsx` cleanly, named ranges and conditional formatting survive, the file re-opens correctly. **But** the test revealed that when R1 appends a new row to Output_Log, only the columns it writes explicitly (A-J, M) get values — **K and L stay blank**.

The X1 spec (`templates/excel/SPEC.md` X1 §Formulas in Output_Log) says K and L are formulas referencing the row in question (`=VLOOKUP(G2, value_envelope_table, 2, FALSE)`, `=K2 * J2 * IF(I2="Yes", 0, 1)`). These formulas were generated by `build_excel.py` for sample-data rows 2-4. Newly appended rows from R1 have blank K and L.

**Consequence:** Monthly_Variable's `total_variable` column sums L:L. Blank cells sum as zero. **Every output R1 captures contributes zero to the variable pay until someone manually pastes the formula in.** This is a silent failure mode: the Routine reports "appended N rows" but the partner gets no variable pay for those rows.

**Fix (three coordinated edits):**

1. `templates/excel/SPEC.md` X1 §Formulas in Output_Log — add explicit note: "K and L formulas are written by R1 (and any other Routine that appends rows) per row, with row numbers adjusted to the appended row. The build script seeds rows 2-N with formulas for sample data, but operational Routines must re-write K and L on every appended row."
2. `routines/SPEC.md` R1 implementation step — add: "When appending row R, also write `K{R} = =VLOOKUP(G{R}, $O$2:$P$5, 2, FALSE)` and `L{R} = =K{R}*J{R}*IF(I{R}="Yes", 0, 1)`. Without this, the appended row contributes 0 to Monthly_Variable's SUMIFS."
3. `routines/cloud/R1.md` and `routines/privacy/R1.md` prompt body — same explicit instruction.

**Severity:** CRITICAL. This is the kind of silent-zero-pay bug that takes 30 days to discover (when partners look at their first variable statement and see the row is missing). Live install would have surfaced it immediately when the founder ran a manual R1 fire and looked at X1.

### Finding 7 — Output_Log's `max_row` is misleading: the value_envelope_table embedded in O1:P5 makes `ws.max_row = 5` even though sample data only fills rows 2-4

This was initially mis-diagnosed as an off-by-one in `build_excel.py`. Closer inspection: the lookup table at O1:P5 has data, so openpyxl reports `max_row=5`. Sample data (A-M) only fills rows 2-4. So `ws.append()` or any `max_row + 1` strategy lands at row 6, leaving row 5 blank in columns A-M — a "ghost row" between sample data and the first R1 append.

This is more subtle than a bug: the row is technically valid (openable, no broken formulas), and the gap doesn't break Monthly_Variable's SUMIFS (the SUMIFS skip the blank row). But it's ugly and means R1's append cadence doesn't produce a contiguous Output_Log.

**Fix (two options, do both):**

1. **Routine-side (immediate):** R1's prompt body / openpyxl operation must find the next empty row using **column A (log_id) as the determinant**, not `max_row`. Concretely:
   ```python
   r = 2
   while ws.cell(r, 1).value:  # while log_id column has a value
       r += 1
   # r is now the first empty row in Output_Log
   ```
2. **Schema-side (v1.x candidate):** Move the value_envelope_table out of Output_Log (e.g. into a new `_lookups` hidden sheet, or extend `_metadata`). Update the K formula to use a cross-sheet reference. Then `max_row` would correctly reflect Output_Log content only. Defer this to v1.x — too disruptive for an in-flight install.

**Severity:** medium. The Routine-side fix is mandatory for clean operation; without it every X1 has a permanent ghost row 5.

### Finding 8 — Install plan Step 10.1 references `python3 build_excel.py --check` which doesn't exist

I imagined a `--check` flag that isn't in `scripts/build_excel.py`. The plan's smoke test invocation would error out: "unrecognized arguments: --check".

**Fix:** Replace Step 10.1's smoke-test invocation with an inline openpyxl check that opens each `.xlsx` and counts sheets, OR add the `--check` flag to `build_excel.py`. Recommend the inline approach — keep `build_excel.py` as a single-purpose generator; smoke-test logic belongs in a separate script (`scripts/smoke_test.py`?) or inline in the plan.

**Severity:** low-medium — the plan's smoke test would fail; agent would surface the failure and the user would catch it. But the plan reads as if it should "just work."

---

## What worked well

- Pattern C (the keystone of ADR-001) is **structurally sound**. openpyxl mutates `.xlsx` cleanly. Named ranges, conditional formatting, formulas on existing rows all survive a save/load cycle. The track-symmetric design holds.
- The Brain folder structure scaffolds cleanly (`firm/excel`, `firm/output-logs`, etc.).
- All 9 framework Excel templates open via openpyxl on Python 3.13 without errors.
- The install plan's pause-and-confirm gate structure (🟡 ASK USER) reads cleanly when the agent narrates what it's about to do — exactly the "surface decisions, don't decide silently" behavior the plan was meant to encode.
- The state-file pattern (`~/.oot/install-state.yaml`) is defensible — every step logs its outcome; agent can resume.

## Recommended next steps

In priority order:

1. **Fix Finding 6 immediately.** This is the only blocker for Path A's correctness. Three edits to coordinate (X1 SPEC, R1 SPEC implementation step, R1 cloud + privacy prompt bodies). Should land as a `fix-routines-r1-formulas` commit before any live install.
2. **Apply Findings 1, 3, 4, 5 to the install plan.** Step 0.1 needs Python-version fallback + per-OS install one-liners + a venv setup substep. These are all in `installer/agent-assisted/cloud-install-plan.md` Step 0.
3. **Apply Finding 8 to Step 10.1.** Replace the imaginary `--check` invocation with an inline openpyxl check.
4. **Fix Finding 2.** Decide canonically on Python ≥3.11 vs ≥3.13 and align `pyproject.toml`, CLAUDE.md, the install plan, the wizard, and the docs.
5. **Fix Finding 7.** Patch `build_excel.py` sample-data loop to populate all sample rows fully. Pre-existing v1.0 bug, low-priority.
6. **Run the live install on a real machine end-to-end.** This test was sandbox-only; it didn't exercise GitHub repo creation, branch protection, real signed commits, Curator install, Claude Desktop MCP wiring, or actual Claude Code Routines. Those are the next class of findings the live install will surface.

## Appendix — sandbox layout used for this test

```
/tmp/oot-test-install/
├── .venv/                         (Python 3.13 venv with openpyxl)
├── oot-brain-remote/              (bare git repo simulating GitHub)
├── oot-brain/                     (working clone)
│   └── firm/
│       ├── excel/                 (9 .xlsx copied from framework)
│       ├── output-logs/
│       ├── audit-logs/
│       ├── business-reviews/
│       ├── klarna-tests/
│       ├── compensation/
│       ├── brain-health/
│       └── partners/
└── test_pattern_c.py              (the smoke-test script)
```

This sandbox was deleted after the test. To re-run the same test, the script `test_pattern_c.py` is preserved in this report's git history — recover with `git log --all -p docs/internal/install-test-report-2026-05-10.md` if needed.
