# ADR-001 — Cloud Routines mutate Excel files in the Ledger via openpyxl and signed commits

**Status:** Accepted
**Date:** 2026-05-10
**Decision-makers:** Dr. Tali Režun (initiator), Claude Code (drafting)
**Supersedes:** the implicit pattern in v1.0 routines/cloud/* prompts that suggested Google Sheets / Drive as the writeback substrate.

---

## Context

The framework defines eight scheduled Routines (R1–R8). Several of them write to Excel-shaped state — partner output ledger (X1), monthly variable (X1 sheet 2), reward species declaration (X2), business review agenda (X3), Klarna decision log + scores (X4), perception-gap survey (X5), agent skill ROI (X6), audit-log index (X7), treasury runway (X8), readiness diagnostic (X9). The privacy track resolves writes via [`haris-musa/excel-mcp-server`](https://github.com/haris-musa/excel-mcp-server) running locally on the always-on machine — clean and unambiguous.

The cloud track was ambiguous. v1.0 routines listed `mcp_servers: [google-drive]` for R1 and `[excel, slack, email]` for R3 / R4 / R8 without specifying *how* writes actually happen. Three plausible interpretations existed:

- **Pattern A** — native Google Drive connector writes to a Google Sheet in place.
- **Pattern B** — Google Sheets via a remote-HTTP MCP that the firm hosts.
- **Pattern C** — Routine clones the Ledger GitHub repo, opens the `.xlsx` with openpyxl in code execution, mutates in place, signed-commits, pushes.
- **Pattern D** — Excel MCP exposed remote-HTTP writing to a hosted `.xlsx`.

The decision needed an authoritative answer before less-technical founders are told "your routines will write to your Excel ledger."

## Verification of Anthropic's product surface (May 2026)

1. **Claude Code Routines** is the actual product name (launched 14 April 2026). The framework's older "Anthropic Remote Routines" naming should be updated. Per-day run limits are 5 (Pro), 15 (Max / Team), 25 (Enterprise). Routines run on Anthropic's infrastructure with **the same toolset as an interactive Claude Code session** — file reads/writes, code execution, git operations including signed commits, MCP tools, and integrations with connected services.

2. **Anthropic's native Google Workspace connector is read-mostly for Sheets.** Per the [official help-centre page](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors): the connector reads Sheets, Slides, PDFs, MS Office files; uploads new files; creates folders; saves Claude-generated files. **It cannot append a row to an existing Sheet in place.** Writes are upload-replacements, not in-place mutations. This rules out Pattern A.

3. **Stdio MCP servers cannot run in cloud Routines.** A stdio MCP runs as a subprocess of the agent host; cloud Routines have no local machine. To use an MCP in a Routine it must be remote-HTTP / SSE and reachable from Anthropic's infrastructure. This means Patterns B and D require the firm to deploy and maintain a remote MCP server.

## Decision

**Adopt Pattern C as canonical for both tracks.**

- **All `.xlsx` operational state lives in the firm's Ledger GitHub repo.** During a fresh install the framework's `templates/excel/*.xlsx` files are *copied* (not symlinked, not referenced) into the firm Ledger at `firm/excel/<file>.xlsx` (or whatever path the firm chooses). The framework repo's templates remain pristine generated artefacts; the firm's copies become stateful as Routines mutate them.
- **Cloud Routines mutate Excel files via Claude Code's code-execution capability**, using openpyxl, against a fresh clone of the Ledger for each run. Each mutation is committed with a signed commit (`R1: append <N> rows for <date>`, etc.) and pushed to the protected `main` branch.
- **Privacy Routines do the same operation locally** via openpyxl against a local clone — no Excel MCP needed. (The Excel MCP becomes an *optional* tool for ad-hoc human-in-the-loop work, not a Routine dependency.)
- **The native Google Workspace connector is used for reads only** — pulling Drive documents that R1 should classify as outputs, for example.
- **Spreadsheet viewers are user choice.** Microsoft Excel, LibreOffice (free, open-source), Apple Numbers, Excel for Web, Google Sheets via "Open with" — all open `.xlsx` natively or via auto-conversion. The framework does not require any specific paid app.

## Consequences

### Positive

1. **Track symmetry.** R1-cloud and R1-privacy do the same thing against the same repo. No code-path divergence.
2. **Native `.xlsx` preserved.** All openpyxl-generated formulas (X1 column-L `computed_variable`, X3 KPI rolls, X8 runway calc, X9 readiness scoring) stay intact because the file never leaves `.xlsx`. Conditional formatting, named ranges, data validation all survive.
3. **R6 audit trail collapses into the same artefact.** Every `.xlsx` mutation is a signed commit on `main`. Article 12 retention, branch protection, append-only history — all inherited. No separate audit substrate for Excel writes.
4. **No new hosted infrastructure.** The firm already has GitHub. No remote MCP to deploy, monitor, or pay for.
5. **Idempotency natural.** R1 keyed on `log_id` produces a no-op commit when re-run on the same day with the same inputs.
6. **Concurrency clean.** Standard git pull-merge-push handles routines and humans editing the same workbook simultaneously.
7. **Office-app-independent.** Founders are not pushed onto Microsoft 365 or Google Workspace just to view their state. LibreOffice and Numbers are first-class.

### Negative / cost

1. **Founders who want the state in a hosted Sheet for live multi-user collaboration are not served by this pattern.** They can adopt a one-way export (Routine writes to Ledger, separate sync job pushes a flattened CSV to a Sheet for collaborative pivoting) — but the canonical store remains `.xlsx` in git.
2. **Routines need GitHub write access with signing.** The bot account or per-Routine identity needs a GPG/SSH signing key uploaded to GitHub. This is a one-time setup, but it is one-time setup the manual-track docs must cover.
3. **R6 must be aware of Routine commits.** The `firm/audit-logs/*` reviewer-required rule must allow R-prefixed commits from the bot identity to land without human review (per skills/code-qa/SKILL.md §4.0 the existing `[skip review]` exemption mechanism covers this; it is now load-bearing).

### Plan-tier implication

Steady-state daily-routine cost on the v1.0 schedule:
- R1 daily ≈ 1.0/day · R6 daily ≈ 1.0/day · R2 weekly ≈ 0.14/day · R5 weekly ≈ 0.14/day · R7 event-driven · R3 monthly · R4 quarterly · R8 weekly.
- **Steady state ≈ 2.3 runs/day**, peak ≈ 4–5 on Monday/Friday with active R7.

Recommendation:

- **Pro plan (5 runs/day) — sufficient for solo or 2-partner firms with no R7 activity.** Monitor the daily counter; if you hit 5/day twice in a week, upgrade.
- **Max plan (15 runs/day) — recommended for 3+ partner firms or any firm with active R7 / Klarna gate enforcement.**
- **Team / Enterprise (25 runs/day) — for >10 partners or firms running R8 + extended R7 plus discretionary ad-hoc Routines.**

## Alternatives considered

### Pattern A — native Google Drive connector writes Sheets in place
**Rejected.** The connector is read-only for Sheets in place; replacement-via-upload loses formulas, validation, and is non-idempotent. Functionally insufficient.

### Pattern B — remote Google Sheets MCP (e.g. `xing5/mcp-google-sheets`, `ringo380/claude-google-sheets-mcp`)
**Rejected.** Workable, but the firm now hosts an MCP server (operational load) and the source of truth is Google Sheets (vendor lock, no native `.xlsx` formulas, no LibreOffice/Numbers fallback, conflicts with the framework's "everything-in-markdown-and-git" philosophy). Pattern C achieves the same goal with one less moving part and better philosophical alignment.

### Pattern D — remote-HTTP `haris-musa/excel-mcp-server`
**Rejected.** The Excel MCP supports streamable-HTTP transport, so it could be deployed remotely. But the `.xlsx` file still has to live on the MCP server's filesystem, which means the firm hosts a small VM with the Ledger cloned and pulled around routine runs — equivalent to Pattern C with extra moving parts. Pattern C accomplishes the same outcome by giving the writer (the Routine itself) the file, not by hosting a separate writer.

## What this changes in the codebase

1. Rename "Anthropic Remote Routines" → "Claude Code Routines" repo-wide.
2. Update `routines/SPEC.md` and `routines/cloud/R{1,2,3,4,5,6,7,8}.md` `mcp_servers:` lists and prompt bodies to spell out Pattern C.
3. Add a new section in `templates/excel/SPEC.md` titled *"Excel files in operation: where they live and who writes them"*.
4. Update `docs/00-quickstart-cloud.md` and `docs/02-installing-routines.md` to teach Pattern C and Pro vs Max plan guidance.
5. Update `CLAUDE.md` "Key design decisions" with this as #11.
6. Document supported spreadsheet viewers (Excel / LibreOffice / Numbers / Excel-for-Web / Sheets-via-import) in the user docs.

## References

- [Introducing routines in Claude Code (Anthropic, April 2026)](https://claude.com/blog/introducing-routines-in-claude-code)
- [Use Google Workspace connectors (Anthropic Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Connect Claude Code to tools via MCP (Anthropic docs)](https://code.claude.com/docs/en/mcp)
- [haris-musa/excel-mcp-server (GitHub)](https://github.com/haris-musa/excel-mcp-server)
- [`templates/excel/SPEC.md`](../../templates/excel/SPEC.md) — the Excel templates spec.
- [`routines/SPEC.md`](../../routines/SPEC.md) — the eight Routines spec.
- [`CLAUDE.md`](../../CLAUDE.md) — repository orientation, including decision-of-record list.
