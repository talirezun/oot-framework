# Install test report — 2026-05-10 (cloud-track Path A)

**Tester:** Claude Code (Opus 4.7) driving its own `installer/agent-assisted/cloud-install-plan.md` against a sandbox on the framework's authors' machine.
**Sandbox:** `/tmp/oot-test-install/` with a bare local git remote at `/tmp/oot-test-install/oot-brain-remote/` simulating GitHub. Cleaned up after the test.
**Outcome:** Path A is structurally sound. Pattern C works mechanically. **8 findings**, of which 1 is a real bug in the framework (formula-write gap in R1) and 7 are docs / install-plan refinements that would have tripped a less-technical founder running the plan against a fresh machine.

> **Editorial note (2026-07-04):** this historical report references `llmster` as the privacy-track Routine runner. That invocation pattern was later corrected — `llmster` is LM Studio's headless **daemon** (the local model server), **not** an agent CLI; the agent that runs privacy-track Routines is **OpenCode headless** (`opencode run`). Findings below are preserved as originally written; see [`docs/02-installing-routines-privacy.md`](../02-installing-routines-privacy.md) for the corrected stack.

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

## Live install findings (2026-05-10, post-sandbox)

### Finding 9 — Install plan didn't handle "user already has Curator + second-brain" case

The cloud install plan's Step 6 assumes greenfield Curator install ("install Curator desktop app, create first domain"). Tali already had a populated second-brain at `/Users/talirezun/second-brain/` with my-curator MCP wired into Claude Desktop AND LM Studio. The plan should ask: *"Do you already have a Curator second-brain? If yes, where, and which domain do you want to use for this firm?"* — and skip the wizard portion when the answer is yes.

This is probably the more common case for any experienced ØØT adopter. **Severity: medium.** Fix in next install-plan revision.

### Finding 10 — macOS filesystem permissions for the Curator + MCP path

Not yet exercised in this test (Tali's MCP was already authorised), but install plan should explicitly walk through System Settings → Privacy & Security → Files and Folders for first-time MCP installs. **Severity: medium for new installs.**

### Finding 11 — Node.js preflight missing from the install plan

`mcp-remote` (the standard wrapper for plumbing remote MCP servers into Claude Desktop) needs Node ≥18. Tali had Node 22.14.0 already, but the plan's Step 0.1 didn't check. **Fix:** add `node --version` to preflight; if missing, surface `brew install node` (macOS) / `apt install nodejs` (Linux).

### Finding 12 — `noreply.github.com` email vs. real-email mismatch for signed commits

Tali's global git config used `61226945+talirezun@users.noreply.github.com` (GitHub's privacy email). The GPG key generated for the test uses `blocklabstech@gmail.com`. For GitHub to mark commits "Verified", the commit author's email must match the GPG key UID's email. **Fix:** install plan must set `user.email` *locally* in the Ledger to match the GPG key's email — not change global config.

### Finding 13 — Install plan over-relies on `gh` CLI; web-UI path must be canonical fallback

A non-technical founder is more likely to know the GitHub web UI than the `gh` CLI. The install plan currently assumes `gh repo create` / `gh api -X PUT /repos/.../branches/main/protection` / `gh gpg-key add`. Each of those needs a web-UI alternative documented. **Fix:** rewrite the plan's Steps 4, 5, 6 to offer "via gh CLI (faster)" or "via GitHub.com (more accessible)" forks. Default to web UI; agent can switch to gh if user opts in.

### Finding 14 — `gh gpg-key add` requires `gh auth`, which most non-technical founders don't have

Same as #13 but specifically for GPG key upload. Web-UI path: paste the key block at https://github.com/settings/gpg/new. **Fix:** plan documents this as the primary path.

### Finding 15 — `pbcopy` from agent shell doesn't reach user's real clipboard

When I tried `cat /tmp/oot-test-gpg-public.asc | pbcopy`, the key didn't land on Tali's clipboard — agent shell sandbox clipboard ≠ user clipboard. **Fix:** install plan must use a method the user can actually access. Two acceptable options: (a) print the key inline in the chat for the user to copy, (b) use `open <file>` on macOS to launch the user's default text editor showing the key. **Severity: high** — mid-install blocker for any agent shell that doesn't share clipboard with the user session.

### Finding 16 — CRITICAL: GitHub Free private repos don't enforce branch protection rules

Tali's screenshot showed the explicit warning: *"Your protected branch rules for your branch won't be enforced on this private repository until you move to a GitHub Team or Enterprise organization account."* This means **R6's audit-trail-immutability claim does not hold on GitHub Free + private repo** — anyone with push access can force-push or push unsigned commits, even with the rule "set."

**Implications for the framework:**

1. ADR-001's audit-trail discipline requires *enforced* branch protection. Three valid configurations:
   - **GitHub Team** ($4/user/month) — branch protection enforces on private repos. Recommended for any firm taking R6 seriously.
   - **GitHub Public repo** — branch protection enforces on personal Free, but firm operational data (X1, X2, salaries, customer info) is publicly readable. Workable only for fully-open-source orgs.
   - **GitHub Free + private + procedural discipline** — branch protection rule is advisory; rely on internal trust + Klarna Test review. Acceptable for solo founders / 2-person shops.

2. **The install plan must surface this trade-off explicitly before the user creates the repo**, including the cost implication.

3. **Routine R6 should detect the unenforced state** at install time and warn. Possibly via a smoke-test that tries `git push --force` and verifies it gets rejected; if accepted, surface "branch protection is not enforced — your audit trail does not have the immutability the framework's docs assume."

**Severity: CRITICAL.** This affects the framework's correctness claims for every firm on GitHub Free. **Fix:** new section in install plan + new section in `governance/SECRETS-POLICY.md` about repo-hosting plan choice.

### Finding 18 — Curator vault location vs. firm operational repo location is unspecified

The framework has two valid configurations and hasn't been explicit about which is canonical:

- **Configuration A (separate roots, used by Tali's existing setup):** Curator vault at one path (`/Users/talirezun/second-brain/`), firm operational repo at another (`/Users/talirezun/00T-test-company/`). The firm repo holds `.xlsx` + Routine-written markdown (`firm/output-logs/`, etc.). The Curator vault holds the knowledge graph, with the firm as one domain. They link via wikilinks but my-curator MCP queries don't see operational data — operational reads happen via direct git access.
- **Configuration B (unified root, greenfield):** firm operational repo IS the Curator vault. `firm/` is a domain. my-curator queries see everything: `.xlsx` state, output logs, audit logs, partner profiles.

Configuration A suits an experienced Curator user with a multi-firm or general second-brain. Configuration B suits a new founder building a single-firm Curator setup from scratch. Both are valid; the framework needs to surface the choice in the install plan and explain the trade-off.

**Fix:** new install-plan step at the top of Step 6 ("the Curator integration choice") that asks the user which config they want. Document trade-offs. Default to B for greenfield, A for users who already have a Curator vault with content.

**Severity: medium.** Affects discoverability of operational data via Curator MCP queries. Doesn't block Pattern C or basic Routines; does affect whether founders can ask Claude "show me the most recent output specs" via my-curator.

### Finding 17 — Install plan's branch protection instructions were unclear

Quoting my own writing: "☑ **Allow force pushes — disabled** (so it stays off)" — internally contradictory. The checkbox label is "Allow force pushes" — checking it ALLOWS force pushes; unchecking it DISALLOWS them. I wrote it in a way that confused Tali.

**Fix:** rewrite as a clean table:

| Checkbox | State | Why |
|---|---|---|
| Require signed commits | ☑ CHECKED | Reject unsigned commits (ADR-001 keystone) |
| Allow force pushes | ☐ UNCHECKED | Force-push rewrites history; we want history immutable |
| Allow deletions | ☐ UNCHECKED | Branch deletion erases audit trail |

**Severity: medium.** Real install-time confusion; user did the wrong thing because of my unclear writing.

---

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
