# Routines — SPEC

The eight ØØT scheduled Routines, in two flavours: cloud track (**Claude Code Routines** — Anthropic's cloud-hosted scheduled-agent product, launched 14 April 2026) and privacy track (OS-native scheduling — cron / launchd / Task Scheduler — invoking OpenCode headless against a local LM Studio server, hosted by the `llmster` daemon). The substrates differ; the prompts are functionally identical so a firm can switch tracks without rewriting Routine logic.

Claude Code generates 16 markdown files (8 in `routines/cloud/`, 8 in `routines/privacy/`) from this spec.

---

## Operational state lives in the Ledger (ADR-001)

All `.xlsx` operational state — partner-output-ledger, reward-species-declaration, business-review, klarna-test, agent-skill-roi, eu-ai-act-mapping, treasury-runway, oot-readiness, perception-gap-survey — lives in the **firm's Ledger GitHub repo**. Routines mutate these files via **openpyxl in Claude Code's code-execution capability**, then **signed-commit and push** the mutation to the protected `main` branch. No Google Sheets, no native Drive write-in-place, no remote Excel MCP. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../docs/internal/ADR-001-cloud-routine-excel-writeback.md) for the full decision rationale and alternatives considered.

Track symmetry: cloud and privacy Routines perform the same operation. Privacy Routines run against a local clone; cloud Routines run against a fresh clone created on Anthropic's infrastructure for each Routine run.

**Spreadsheet viewers are user choice.** Microsoft Excel, LibreOffice (free, open-source), Apple Numbers, Excel-for-Web, Google Sheets via "Open with" / import — all open `.xlsx` natively or via auto-conversion. The framework does not require any specific paid app.

---

## Routine write authority: Ledger only (ADR-002)

**Routines write only to the Ledger.** They never push to the Firm Brain (Curator Shared Brain). Per [ADR-002](../docs/internal/ADR-002-firm-brain-curator-shared-brain.md):

- **Ledger** (`<firm>-ledger`) — Routine-writable, openpyxl + signed commits per ADR-001. Holds all `.xlsx` files plus Routine-authored operational markdown: `firm/output-logs/`, `firm/audit-logs/`, `firm/business-reviews/`, `firm/klarna-tests/`, `firm/partners/<id>/variable-statements/`, `firm/partners/<id>/long-tail-statements/`, `firm/compensation/`, `firm/brain-health/`, `firm/treasury/` (R8 daily snapshot per ADR-004).
- **Firm Brain** (`<firm>-brain`) — partner-writable only, via Curator Shared Brain Push. **No Routine pushes here.** Holds partner-authored firm IP: theses, decisions, ADRs, partner profiles, prompts, change-management artefacts. Routines may **read** the Firm Brain (via git clone of the `<firm>-brain` repo, scoped to `collective/<firm-domain>/wiki/`) when they need firm context — see the per-Routine "Firm Brain reads" column below.

### Per-Routine repo access matrix

| Routine | Ledger read | Ledger write | Firm Brain read | Firm Brain write |
|---|---|---|---|---|
| **R1** Daily Output Capture | ✓ | ✓ (X1, output-logs) | optional (output-spec lookup) | **✗** |
| **R2** Weekly BR Prep | ✓ | ✓ (X3, business-reviews) | ✓ (decisions, ADRs, partner profiles for context) | **✗** |
| **R3** Monthly Variable Calc | ✓ | ✓ (X1, X2, variable-statements, compensation) | optional (reward-species summary, partner profile) | **✗** |
| **R4** Quarterly Long-Tail | ✓ | ✓ (X1, long-tail-statements, compensation) | optional (output-specs for outcome attribution) | **✗** |
| **R5** Brain Health Check | ✓ | ✓ (X9, brain-health) | ✓ (synthesized firm IP — scans for orphans, broken links) | **✗** |
| **R6** EU AI Act Audit Trail | ✓ | ✓ (X7, audit-logs) | ✗ | **✗** |
| **R7** Klarna Test Trigger | ✓ | ✓ (X4, klarna-tests) | ✓ (decisions, ADRs touching the gated change) | **✗** |
| **R8** Treasury Runway (opt) | ✓ | ✓ (X8) | ✗ | **✗** |
| **R9** Firm Brain Synthesize | ✗ | ✗ | (admin-run; mutates `<firm>-brain` via Curator's API, not as a normal Routine commit) | ✓ — but via **Curator's Synthesize endpoint**, not via openpyxl + signed-commit |

Firm Brain reads from cloud Routines use a fresh `git clone <firm>-brain` at the start of each run. Privacy-track Routines read from a local clone maintained on the always-on machine, refreshed via `git pull` before each run.

---

## Plan-tier guidance (cloud track)

Anthropic plan limits drive what's affordable for a firm:

| Plan | Routine runs/day | Suitable for |
|---|---|---|
| **Pro** | 5 | Solo founders or 2-partner firms **without** R7 (Klarna gate) activity |
| **Max** | 15 | 3+ partner firms; any firm with active R7; recommended default |
| **Team** | 25 | 5+ partner firms with discretionary ad-hoc Routines |
| **Enterprise** | 25 | >10 partners; firms running R8 + extended R7 |

Steady-state daily-routine cost on the v1.0 schedule: R1 daily + R6 daily + R2/R5/R8 weekly + R3 monthly + R4 quarterly + R7 event-driven ≈ 2.3 runs/day average, peak ≈ 4–5. Pro is sufficient until R7 starts firing; from there, upgrade.

---

## Conventions for all Routines

**Trigger.** The schedule or event that fires the Routine.

**Prompt body.** The full prompt the Routine sends to its model. Cloud track sends to Claude (Sonnet by default; Opus for R3 due to compensation sensitivity). Privacy track sends to the local model loaded in LM Studio (Qwen 3 ≥9B recommended, larger preferred for R3).

**Allowed Skills.** Skill Packs the Routine loads at runtime. The Routine inherits the Skill Pack's discipline.

**MCP servers.** MCP tools the Routine uses. **Cloud Routines support remote-HTTP / SSE MCPs only** (no stdio MCP — there is no local machine for cloud Routines). Stdio MCPs (e.g. `haris-musa/excel-mcp-server` in default mode, Desktop Commander) are privacy-track-only. The Excel writeback canonical pattern uses **no Excel MCP** — it uses Claude Code's built-in code execution + GitHub repo operations.

**Code-execution requirement.** Routines that mutate `.xlsx` files require code execution to be enabled in their Claude Code Routine config. This is the default for Pro+ accounts.

**Brain-repo access.** Routines that read or write `.xlsx` files require the Ledger to be cloneable + pushable from the Routine. Configure a deploy key or PAT scoped to the Ledger, with signing (GPG or SSH) configured per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md). Only the firm's bot identity (e.g. `oot-bot`) commits via Routines; the bot identity is exempted from the `firm/audit-logs/*` reviewer rule per the existing `[skip review]` mechanism (see `skills/code-qa/SKILL.md` §4.0).

**Expected output.** Where the Routine writes — Brain pages, Excel files (mutated in-repo + signed commit), Slack/dChat posts, audit logs.

**Failure handling.** What happens if the Routine errors (e.g., GitHub API rate-limited, MCP unreachable, model error, signing key unavailable).

**Privacy-track delta.** Where the privacy-track equivalent differs from the cloud version. For Excel writes the operation is identical (openpyxl on a local Brain-repo clone) — only the scheduling substrate differs.

---

## R1 — Daily Output Capture

**Trigger:**
- Cloud: Claude Code Routine, daily 18:00 in the firm's primary timezone.
- Privacy: cron `0 18 * * *` (Linux/macOS) or Task Scheduler equivalent (Windows), invoking `opencode run --model lmstudio/<model> "$(cat routines/privacy/r1.prompt.md)"` (the prompt file's read-first line loads the compensation-attribution skill).

**Allowed Skills:** S3 (Compensation & Attribution), S1 (My Curator).

**MCP servers and tools:**
- Cloud: GitHub connector (Brain-repo clone + signed commit + push). Slack connector (read tracked channels + post `#output-log` and `#ops`). Google Workspace connector (**read-only**, for `{{TRACKED_FOLDERS}}` document discovery). Code execution required (openpyxl writes to X1 in the cloned Ledger).
- Privacy: same operation locally. GitHub MCP for the commit/push. Local filesystem for the Ledger clone. 4thtech CLI/SDK for dChat thread reads (replaces Slack). No Excel MCP needed — openpyxl is a Python library, run directly by OpenCode's code execution (against the LM Studio server hosted by the `llmster` daemon).

**Prompt body:**

```
You are running the daily output capture for an ØØT organisation. Today is {{TODAY}}.

Your task: read all output signals from the past 24 hours across the following sources, and append rows to partner-output-ledger.xlsx (file X1) per its schema in templates/excel/SPEC.md.

Sources to read:
1. GitHub: all commits across all firm repos in the last 24 hours. Include: commit hash, author (note any Co-authored-by: trailers indicating AI assistance), files changed, lines added/deleted, PR association if applicable. **EXCLUDE the routines' own writebacks:** skip any commit authored by the firm's routine-bot identity (e.g. `oot-bot`) AND any commit whose subject line starts with a routine prefix (`R1:`, `R2:`, … `R9:`, or `migration:`). Routine writebacks (R6's audit commit, R5's brain-health snapshot, R1's own append, etc.) are audit events — captured by R6, never counted as partner output.
2. Slack channels listed in {{TRACKED_CHANNELS}} (or 4thtech dChat threads on privacy track): outputs explicitly tagged with #output, contracts mentioned in #commercial, deals closed in #sales.
3. Google Drive (or local filesystem on privacy track): documents created or significantly modified in {{TRACKED_FOLDERS}}.

For each output:
- Generate a log_id following the format OL-YYYYMMDD-NNN.
- Determine the partner_id from the author/owner (consult the partners Brain page if uncertain). **For a co-authored output, create one row per co-author and set each row's `weight` (column N) to `1/count`** — or to the explicit fractions in the output spec's `attribution_split` field when the partners have agreed a split (ADR-005). The column-L formula (`=K*J*N*IF(rework…)`) then *shares* the value envelope across co-authors instead of paying each the full amount. Do NOT record the split as a free-text note; `weight` is the load-bearing field.
- Classify output_type per the X1 schema.
- Reference the output_spec_ref from the Ledger if one exists; flag for human review if not.
- Estimate value_tier (S/M/L/XS) based on the output_spec value envelope; default to L if no spec exists.
- Estimate ai_authored_pct from commit trailers and change patterns (best-effort; partner can correct).
- Set `rework_within_30d` to "No" by default. This field is **updated retroactively by R1 on every subsequent run within the next 30 days** using the following deterministic detection rule:

  > A new commit `C_new` marks an earlier commit `C_old` as `rework=Yes` if **all four** conditions hold: (a) same `partner_id` on both commits; (b) `C_new` timestamp is within 30 days after `C_old`; (c) ≥50% file overlap between the two commits' changed-files sets; (d) `C_new`'s commit message OR associated PR title/description matches the regex `\b(fix|revert|hotfix|redo|retry|reapply|backout|rollback)\b` (case-insensitive). When all four hold, R1 **updates the prior X1 row's `rework_within_30d` to "Yes"** (which zeroes out its `computed_variable` via the X1 column-L formula). The Routine logs every retroactive update in the daily Brain summary under a `## Retroactive rework detections` heading.

- Resolve `partner_multiplier` (column J) by **reading X2 directly at write time** — do not rely on a cross-workbook Excel formula (see `templates/excel/SPEC.md` X1). Compute `value_envelope` (column K) per the lookup table embedded in X1.

**Implementation (the canonical Pattern C operation per ADR-001):**

1. Clone the firm's Ledger to a fresh per-run working directory: `WORKDIR=$(mktemp -d) && git clone <LEDGER_REPO_URL> "$WORKDIR/ledger" && cd "$WORKDIR/ledger"`. Use a unique dir per run (not a fixed `/tmp/brain`) so concurrent or same-day re-runs never collide on a stale clone. A fresh clone is already current — no `git pull` needed after it.
2. Open `firm/excel/partner-output-ledger.xlsx` (X1) with openpyxl in code execution.
3. Find the next empty row in Output_Log using **column A (log_id) as the determinant**, NOT `ws.max_row`. The value_envelope_table embedded at O1:P5 makes `max_row` report 5 even when sample data only fills rows 2-4 — using `max_row + 1` would leave a permanent ghost gap. Pseudocode:

        r = 2
        while ws.cell(r, 1).value:
            r += 1
        # r is now the first empty row to append at

3a. **Dedupe against already-logged outputs (makes re-runs idempotent).** Before appending any candidate, read the existing Output_Log rows and collect the set of `output_ref` values (column E) from every row whose `date` (column B) is within the last 45 days. **Skip any candidate whose `output_ref` already appears in that set** — it was captured on a prior run. Running R1 twice on the same day (e.g. after an Anthropic-infra retry) must therefore append zero duplicate rows and pay nobody twice. Only genuinely new outputs get appended. Log the count of skipped-as-duplicate candidates in the daily Brain summary.
4. Append the new rows starting at row `r`. Per row R appended (the appended-row contract, ADR-004 §3):
   - **Columns A-I:** write the captured values directly to row R (log_id, date, partner_id, output_type, output_ref, output_spec_ref, value_tier, ai_authored_pct, rework_within_30d). The `partner_id` (C) joins X2 Partner_Profile column A (ADR-005).
   - **Column J (`partner_multiplier`):** resolve by reading X2 (`firm/excel/reward-species-declaration.xlsx`) at write time per the v1.0 design decision (no cross-workbook formulas). Match the partner by `partner_id` in `Base_Variable_Split` column A (ADR-005 join key), read `output_multiplier` (column G), write the resolved number.
   - **Column K (`value_envelope`):** **MUST write the formula** `=VLOOKUP(G{R}, $O$2:$P$5, 2, FALSE)` (with `{R}` substituted to the row number). Without this formula the cell stays blank and contributes zero to Monthly_Variable's SUMIFS — silent failure mode that R3 will not catch. Do NOT leave K blank.
   - **Column L (`computed_variable`):** **MUST write the formula** `=K{R}*J{R}*N{R}*IF(I{R}="Yes", 0, 1)` (with `{R}` substituted). Same discipline as K — blank L means zero variable pay for that output until someone manually patches it. The `N{R}` factor shares the envelope across co-authors (ADR-005).
   - **Column M (`notes`):** write any human-readable annotation, optional.
   - **Column N (`weight`):** write `1.0` for a single-author output; write `1/count` (or the output spec's `attribution_split` fraction) for each co-author row of a co-authored output (ADR-005).
5. For any retroactive rework_within_30d updates, edit the corresponding Output_Log rows in place.
6. Save X1.
7. Write the daily Brain summary as a markdown file at `firm/output-logs/YYYY-MM-DD.md` following the template at `templates/brain/daily-output-log.md`. Include: total outputs captured, breakdown by partner, count skipped as duplicates, any anomalies (e.g., a partner with zero outputs for >3 consecutive days), any retroactive rework_within_30d updates.
8. Stage and signed-commit both changes: `git add firm/excel/partner-output-ledger.xlsx firm/output-logs/YYYY-MM-DD.md && git commit -S -m "R1: append <N> outputs for <date>; <K> retroactive rework updates"`.
9. Push to `main`: `git push origin main`. The bot identity is exempted from the `firm/audit-logs/*` reviewer rule per `[skip review]`; for `firm/excel/*` and `firm/output-logs/*` paths, no review is required (these paths are append-mostly Routine output, not audit log).

Post a short summary to Slack #output-log (or 4thtech dChat #output-log on privacy track): "{{TODAY}} captured {{N}} outputs from {{P}} partners. Anomalies: {{LIST_OR_NONE}}."

Failure handling: if any source is unreachable, log the failure to the daily summary, capture from available sources, and post a notice to #ops. If git push fails (signing key unavailable, branch protection rejects, network), retry with exponential backoff up to 3 attempts; if still failing, post to #ops and DO NOT downgrade to an unsigned commit.
```

**Expected outputs:**
- Rows appended to `firm/excel/partner-output-ledger.xlsx` in the Ledger.
- Brain page at `firm/output-logs/YYYY-MM-DD.md`.
- One signed commit on `main` carrying both changes.
- Slack/dChat summary post.

**Privacy-track delta:**
- Sources: GitHub via GitHub MCP, dChat via 4thtech CLI/SDK, local filesystem via Desktop Commander MCP.
- Excel writes: same openpyxl operation against a local Brain-repo clone — no Excel MCP needed for the Routine path. (Excel MCP remains available as an *optional* tool for ad-hoc human-in-the-loop work, not a Routine dependency.)
- Posting: dChat to a designated channel.
- Cron entry: `0 18 * * * cd ~/<firm-slug> && /usr/local/bin/opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r1.prompt.md)" >> ~/oot-framework/logs/r1.log 2>&1` (the prompt file's read-first line loads compensation-attribution + my-curator).

---

## R2 — Weekly BR Prep

**Trigger:**
- Cloud: Claude Code Routine, Friday 08:00.
- Privacy: cron `0 8 * * 5`.

**Allowed Skills:** S5 (Reporting & Business Review), S1 (My Curator).

**MCP servers and tools:** GitHub connector / GitHub MCP (Brain-repo clone + signed commit + push). Slack / 4thtech connector. Code execution required (openpyxl reads X1, X4, X6, X2, and X8-if-adopted, and reads + writes X3 in the cloned Ledger).

**Prompt body:**

```
You are preparing the Friday Business Review agenda for an ØØT organisation. The BR meeting starts at 14:00 today.

Your task: populate business-review.xlsx (X3) Weekly_Review sheet for the week starting {{MONDAY_DATE}} and ending today.

1. Read partner-output-ledger.xlsx Output_Log for the past 7 days. Identify the top 5 outputs by computed_variable (column L = value_envelope × partner_multiplier × rework_flag). For each: who shipped it, what tier, brief description from the output_spec_ref. Write to column B (notable_outputs) as a markdown bullet list.

2. Query the Ledger (firm/output-logs/) for blocker tags raised in the past 7 days that remain open. Write to column C (blockers).

3. Read klarna-test.xlsx Decision_Log column M (`status`) for any tests with M ∈ {`scoring`, `remediation`, `monitoring`} (ADR-004). Write to column D (klarna_test_status). Post-meeting, R2 may write M back to Decision_Log (e.g. a test the BR agreed to close moves `monitoring`→`proceeded`, or a re-score decision moves `remediation`→`scoring`) — the writeback is a signed commit like any other Routine mutation.

4. Read the KPI sources for week-over-week deltas and write to column E (kpi_movements). Each KPI has a specific home: `ai_skill_roi` from X6 ROI_Calc (`roi_multiple`); `agent_human_ratio` from X6 Human_Agent_Ratio (`agent_human_ratio`); `treasury_runway_months` from X8 Runway_Calc (`runway_months`) — or "n/a" if X8 not adopted; `partner_count` from X2 Partner_Profile (row count); `customer_count` from X3 Monthly_BR (`customer_count_delta`).

5. Identify decisions due — items in the Ledger tagged decision-pending. Write to column F (decisions_due).

Post a draft summary to Slack #business-review (or dChat equivalent) by 09:00:
"BR agenda for {{TODAY}} 14:00 ready. Highlights: {{TOP_3_FROM_NOTABLE}}. Klarna in flight: {{COUNT}}. Decisions due: {{COUNT}}."

After the BR meeting (signaled by manual trigger or by the Decisions_Log getting populated), commit the final summary as a Ledger page at firm/business-reviews/YYYY-MM-DD.md.

**Implementation:** clone the Ledger, read X1 / X4 / X6 / X2 / X8(if adopted) via openpyxl, write the new row(s) to X3's Weekly_Review sheet via openpyxl, write the Ledger summary markdown, signed-commit both changes, push to `main`. Same Pattern C as R1 (ADR-001).

Failure handling: if any data source is unreachable, populate from what's available and clearly mark the gap in column G (meeting_notes) for the BR participants to address.
```

**Expected outputs:**
- `firm/excel/business-review.xlsx` Weekly_Review sheet populated.
- Slack/dChat draft summary.
- Post-BR Brain page (after meeting).
- Signed commit on `main`.

**Privacy-track delta:** Same openpyxl operation against a local Brain-repo clone; dChat via 4thtech.

---

## R3 — Monthly Variable Calc

**Trigger:**
- Cloud: Claude Code Routine, 1st of month, 09:00.
- Privacy: cron `0 9 1 * *`.

**Allowed Skills:** S3 (Compensation & Attribution).

**MCP servers and tools:** GitHub connector / GitHub MCP (Brain-repo clone + signed commit + push). Slack / 4thtech connector for `#compensation` posts. Email / dMail for per-partner statement delivery. Code execution required (openpyxl reads X1, X2 and writes X1's Monthly_Variable sheet in the cloned Ledger). Polling job to detect partner acknowledgement runs daily as a separate Routine fire (see step 8 below).

**Recommended model:** Cloud — Claude Opus (compensation accuracy is high-stakes). Privacy — largest local model available.

**Prompt body:**

```
You are running the monthly variable pay calculation for an ØØT organisation. The calculation is for {{LAST_MONTH}} (first day to last day inclusive).

Your task: lock the previous month's Output_Log and produce per-partner variable pay drafts.

1. Read partner-output-ledger.xlsx Output_Log filtered to last_month. For each row, verify the rework_within_30d field is current (look forward to today's date and recompute if any output from last_month had rework detected since).

2. Aggregate per partner: total_outputs, total_variable (SUM of computed_variable column).

3. Read reward-species-declaration.xlsx for each partner's base_amount and current reward_species parameters. Join on `partner_id` — filter `Base_Variable_Split` to the row where column A (`partner_id`, ADR-005) matches the partner, then read `base_amount` (column C) and `output_multiplier` (column G).

4. Populate the Monthly_Variable sheet of partner-output-ledger.xlsx for {{LAST_MONTH}}: one row per partner, with total_outputs, total_variable, base_pay (last_month proportional), total_compensation, sign_off_status='draft'. **total_outputs (C) and total_variable (D) are written as resolved literals** (aggregate in Python), not Excel formulas — the pseudo-COUNTIFS/SUMIFS in the SPEC is a definition, not valid Excel. total_variable already reflects co-authorship weight because it sums Output_Log column L (which folds in column N).

5. For each partner, generate a personalised statement at firm/partners/{{partner_id}}/variable-statements/YYYY-MM.md following the template at `templates/brain/variable-statement.md`. Statement includes: month, total outputs (with the top 5 listed by value), variable computation with the multiplier, base pay, total compensation, list of any retroactive rework_within_30d zero-outs from prior months that affected this month's pool. The statement is the partner's official record of their variable for the month. The template ends with an explicit acknowledgement block:

        ## Acknowledgement

        - [ ] I have reviewed this statement and agree with the calculation.
        - [ ] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).

        _Sign by editing this page and ticking the appropriate box, then commit._

6. Send the statement to each partner via email (cloud) or 4thtech dMail (privacy track). Subject: "Variable pay statement for {{LAST_MONTH}} — review by {{REVIEW_DEADLINE}}". Body links to the Ledger statement page.

7. Post to Slack/dChat #compensation: "Monthly variable drafts for {{LAST_MONTH}} are ready. {{COUNT}} partners. Total: {{TOTAL_EUR}}. Review window: 5 business days. Founder approval required before payment."

8. **Acknowledgement detection** — the Routine polls each partner's statement page once daily and parses the acknowledgement block. The first checked box wins. Set `sign_off_status` per the table:

   | Detected state in Brain page | sign_off_status |
   |---|---|
   | First box ticked, second unticked | `partner_reviewed` |
   | Second box ticked (dispute), first unticked | `partner_disputed` (escalates to Tier 1 per DECISION-RIGHTS.md; `R3` does not advance the row to `founder_approved`) |
   | Both ticked | `partner_disputed` (the partner's intent is unclear; treat as dispute, ask for clarification) |
   | Neither ticked, ≥5 business days since send | `partner_unresponsive` (escalate to founder; never auto-approve) |
   | Neither ticked, <5 business days since send | `draft` (no change) |

   Slack reactions are **not** the canonical signal; only the Ledger checkbox counts. This makes the audit trail self-contained in the Ledger (auditable from the firm's git history alone, no third-party messaging dependency).

9. After all partner reviews complete OR after 5 business days (whichever first), compile a founder-approval packet at firm/compensation/YYYY-MM/founder-approval.md. Founder approves; sign_off_status moves to 'founder_approved'. Payment processing then proceeds (manual in Gen 1; automated stablecoin in Gen 2).

Failure handling: if any partner does not respond within the 5-day window, escalate to founder for review. Never auto-approve a contested calculation.
```

**Implementation:** clone Ledger; read X1 Output_Log (filtered to last_month) and X2 reward-species via openpyxl; write the Monthly_Variable rows + per-partner statement markdown files; signed-commit; push. Same Pattern C as R1 (ADR-001). For the daily acknowledgement polling step, the polling Routine (or a single Routine that handles steps 1-7 on day 1 and step 8 daily through day +5) re-clones the Ledger, reads each partner's statement page for the checkbox state, updates X1 Monthly_Variable's `sign_off_status` column, signed-commits + pushes. Each polling pass is a separate Routine run; budget for 5–7 R3-polling fires per month in the Anthropic plan calculation.

**Expected outputs:**
- `firm/excel/partner-output-ledger.xlsx` Monthly_Variable sheet populated.
- Per-partner statement Brain pages.
- Email/dMail to each partner.
- Founder-approval packet.
- One signed commit per Routine fire (initial + daily polling).

**Privacy-track delta:** dMail instead of email; same openpyxl operation locally.

---

## R4 — Quarterly Long-Tail Settlement

**Trigger:**
- Cloud: Claude Code Routine, 1st of quarter (1 Jan, 1 Apr, 1 Jul, 1 Oct), 09:00.
- Privacy: cron `0 9 1 1,4,7,10 *`.

**Allowed Skills:** S3, S10 (Finance & Treasury).

**MCP servers and tools:** GitHub connector / GitHub MCP. Email / dMail. Code execution required (openpyxl reads X2 Long_Tail_Schedule across all partner sheets, writes settlement rows and per-partner statement markdown). Pattern C as in R1 (ADR-001).

**Prompt body:**

```
You are running the quarterly long-tail entitlement settlement for an ØØT organisation. The quarter just ended is {{LAST_QUARTER}}.

Your task: for every output that has an entry in any partner's reward-species-declaration.xlsx Long_Tail_Schedule with settlement_period='quarterly', compute the partner's long-tail payment for the quarter.

1. Read the firm's single reward-species-declaration.xlsx. In `Long_Tail_Schedule` (one shared sheet, keyed by leading `partner_id` in column A — ADR-005), extract every row where end_date is empty OR > {{LAST_QUARTER_END}}, AND start_date <= {{LAST_QUARTER_END}}. Settle "per partner" by grouping on column A (`partner_id`), NOT by assuming per-partner sheets.

2. For each such (partner, output) pair, query the Ledger or financial system for the realised outcome attributable to the output during {{LAST_QUARTER}}: revenue generated, cost saved, customer impact metric — the metric committed to in the Output Spec.

3. Compute the partner's long-tail payment for the quarter as: outcome_attributable × partner_share_pct / 100 (partner_share_pct is column D after the ADR-005 shift).

4. Update the partner's Long_Tail_Schedule row: add the quarter's settlement to total_settled_to_date (column H after the ADR-005 shift).

5. Generate a per-partner long-tail statement at firm/partners/{{partner_id}}/long-tail-statements/YYYY-Q{{N}}.md.

6. Send statement via email/dMail. Founder approval required before payment.

7. Post summary to Slack/dChat #compensation.

Failure handling: if outcome attribution data is missing for an output, flag for founder + affected partner review; do not pay until resolved.
```

**Implementation:** clone Ledger; read X2 across all partner sheets via openpyxl; compute and write settlement; write per-partner long-tail statement markdown; signed-commit; push. Pattern C as R1.

**Expected outputs:** Per-partner long-tail statements; updated Long_Tail_Schedule sheets; founder-approval packet; signed commit on `main`.

**Privacy-track delta:** Same openpyxl operation locally; dMail instead of email.

---

## R5 — Brain Health Check

**Trigger:**
- Cloud: Claude Code Routine, Sunday 09:00.
- Privacy: cron `0 9 * * 0`.

**Allowed Skills:** S1 (My Curator).

**Two structurally-different variants (the full prompt bodies live in the per-track files, which are authoritative):**

- **Cloud — the bridge** ([`routines/cloud/R5.md`](cloud/R5.md), authoritative). Cloud Routines run on Anthropic's infrastructure and cannot reach a local stdio MCP, so there is **no my-curator MCP** on the cloud track. R5 clones **two repos** at runtime (the Ledger read-write + the Curator-synced brain repo read-only), does a **file-level** scan of the synced markdown (parse frontmatter, walk `[[wikilinks]]`, git-mtime), and detects broken wikilinks / orphans / stale pages. It **cannot auto-fix** (read-only on the brain repo — it LISTS typo-correctable links) and **cannot run semantic-duplicate detection** (needs the MCP). Report written to `firm/brain-health/YYYY-WW.md` in the Ledger via signed commit; summary posted to Slack `#brain-health`.

- **Privacy — direct MCP** ([`routines/privacy/R5.md`](privacy/R5.md), authoritative). The Routine runs on the **same always-on machine** as the my-curator MCP server, so it reaches the Curator's full 17-tool set directly (stdio). It calls `scan_wiki_health`, **auto-fixes** the narrowly-safe class via `fix_wiki_issue` (a broken wikilink with exactly one existing slug within Levenshtein ≤ 2 — same safe/unsafe decision as cloud, but privacy can act on it), and runs `scan_semantic_duplicates` to surface same-concept-different-slug pages (listed for human review, never auto-merged — merges are destructive). Report written to the same `firm/brain-health/YYYY-WW.md` template in the Ledger via signed commit; the privacy report additionally carries a semantic-duplicates section and an auto-fixed count. Summary posted to 4thtech dChat `#brain-health`.

**MCP servers and tools:** cloud — GitHub connector only (no my-curator); code execution for the two-repo clone + scan + snapshot commit. Privacy — my-curator MCP (local stdio) + GitHub MCP for the snapshot commit; code execution for the signed commit. Neither variant mutates any `.xlsx` file.

**Expected outputs:** Brain health snapshot page at `firm/brain-health/YYYY-WW.md` (Ledger, signed commit); Slack/dChat post if any metric is non-zero. Privacy additionally: single-candidate typo links auto-fixed in the Curator.

**Failure handling:** Curator/brain-repo unreachable → retry once, then write a flagged "unreachable" report (so the gap is audit-trailed), commit it, escalate to `#ops`. Ledger push failure → retry, escalate to `#ops`, never downgrade to an unsigned commit.

---

## R6 — EU AI Act Audit Trail

**Trigger:**
- Cloud: Claude Code Routine, daily 23:00.
- Privacy: cron `0 23 * * *`.

**Allowed Skills:** S7 (Governance & Compliance).

**MCP servers and tools:** GitHub connector / GitHub MCP (Ledger clone + signed commit + push of the daily audit log). **No my-curator MCP** — R6 reads other Routines' decisions from their **Ledger writebacks** (the markdown pages under `firm/output-logs/`, `firm/business-reviews/`, etc.), not from the Curator graph; the Second Brain bridge is not used here (matches cloud R6 v1.1.1's frontmatter). Code execution required (openpyxl writes X7 Audit_Log_Index; both artifacts land in one commit).

**Prompt body:**

```
You are appending today's audit trail to the EU AI Act Article 12 record for an ØØT organisation. Today is {{TODAY}}.

Your task:
1. Clone {{LEDGER_REPO_URL}} and read all agent decisions logged today across all firm Routines (R1, R2, R3, R4, R5, R7, R8) and any ad-hoc Skill invocations that produced an output affecting partners or customers. Each Routine writes its decisions as markdown in the Ledger — read today's files under `firm/output-logs/` (R1), `firm/business-reviews/` (R2), `firm/partners/*/variable-statements/` (R3), `firm/partners/*/long-tail-statements/` (R4), `firm/compensation/` (R3/R4 founder-approval packets), `firm/brain-health/` (R5), `firm/klarna-tests/` (R7), `firm/treasury/` (R8), and `firm/audit-logs/` itself (yesterday's entries, for continuity). R6's source-of-truth is the Ledger, not the Curator graph.
2. For each decision, capture: timestamp, AI system identifier (which model + Skill), decision context (sanitised input summary), output, human reviewer if any, related use_case_id from eu-ai-act-mapping.xlsx.
3. Append to firm/audit-logs/YYYY-MM-DD.md following the template at templates/brain/audit-log-day.md.
4. Update eu-ai-act-mapping.xlsx Audit_Log_Index sheet with today's entry count and any anomalies flagged.
5. Stage and signed-commit **both artifacts in one commit** via the git CLI in code execution (Pattern C, ADR-001): `git add firm/audit-logs/YYYY-MM-DD.md firm/excel/eu-ai-act-mapping.xlsx && git commit -S -m "R6: audit trail for <date>" && git push origin main`. One commit carries both the audit-log markdown and the X7 Audit_Log_Index update. This commit MUST land on the protected `main` branch (or the firm's chosen audit branch) which has the following branch-protection rules configured: (a) force-push disabled; (b) deletion disabled; (c) signed commits required; (d) at least one reviewer for any modification (Routine R6's commits are auto-approved by a designated bot account or use a `[skip review]` exemption only for append-only audit-log paths under `firm/audit-logs/`). These three protections together — append-only path, force-push block, signed commits — provide the practical immutability required by Article 12 record-keeping. (True triple-entry / external anchoring is Generation 2; see `GENERATIONS.md`.)

Failure handling: if any source unreachable, append from available sources and flag the gap. The audit log MUST be appended every day; an empty day is a noted "no agent activity" entry, not a missing day. If the signed-commit step fails (signing key unavailable, branch protection rejects the push), R6 retries hourly; if still failing at 02:00 the next day, escalate to founder via Slack `#ops` — DO NOT downgrade to an unsigned commit silently.
```

**Expected outputs:** Daily audit log Brain page; X7 Audit_Log_Index updated; **signed** git commit on the protected branch.

**Privacy-track delta:** The prompt body is identical (same Pattern-C git-CLI single signed-commit carrying both the audit-log markdown and the X7 update; same Ledger-writeback source, no my-curator). The audit-log discipline is identical. The signing key is stored in a Trezor or YubiKey-backed slot on the always-on machine, never in plaintext.

**Setup pre-requisite (one-time):** The firm must configure GitHub branch protection on `main` (or the audit branch) with: force-push disabled, deletion disabled, "Require signed commits" enabled. The cloud installer (Phase 9) and the Code & QA SKILL.md (S4) document this configuration. Without these protections the Article 12 retention claim does not hold.

---

## R7 — Klarna Test Trigger

**Trigger:**
- Cloud: Claude Code Routine fired by GitHub event (PR labelled `ai-replaces-human`). Optionally also: manual trigger from a partner via Slack slash command.
- Privacy: GitHub webhook polled by a local listener (every 5 minutes) that invokes OpenCode (`opencode run`) against the local LM Studio server.

**Allowed Skills:** S6 (Change Management), S4 (Code & QA).

**MCP servers and tools:** GitHub connector / GitHub MCP (PR status check, Brain-repo clone + signed commit + push). Slack / 4thtech connector. Email / dMail. Code execution required (openpyxl appends row to X4 Decision_Log).

**Schema (ADR-004).** Decision_Log column **M `status`** is the Excel home for the lifecycle state machine (literal enum `scoring | remediation | monitoring | proceeded | held`; data-validated; never a formula). It is distinct from column I `decision`, which is the formula-driven threshold verdict (`=IF(H>=14,"PROCEED","HOLD")`). The two may disagree transiently. R7 writes and updates M directly; it does NOT track state in the `firm/klarna-tests/{{test_id}}.md` frontmatter as a schema workaround (that page remains the human-readable context record). See ADR-004 for the full contract.

**Prompt body:**

```
You are launching a Klarna Test scoring for an ØØT organisation. The trigger is PR #{{PR_NUMBER}} in repo {{REPO}} labelled 'ai-replaces-human'.

Your task:
1. Generate a test_id following format KT-YYYY-NNN.
2. Append a row to klarna-test.xlsx Decision_Log per the appended-row contract (ADR-004, `templates/excel/SPEC.md`):
   - **Columns A-G literals:** test_id (A), today's date (B), decision_summary from PR title + description (C), trigger='pr_label' (D), trigger_ref=PR URL (E), scorer=the assigned scorer partner_id (F), non_beneficiary_reviewer partner_id (G).
   - **Column H (total_score) MUST write the formula** `=IFERROR(VLOOKUP(A{R},Klarna_Score!A:L,12,FALSE),"")`.
   - **Column I (decision) MUST write the formula** `=IF(ISBLANK(H{R}),"",IF(H{R}>=14,"PROCEED","HOLD"))`. Do NOT write a literal — I is formula-driven.
   - **Column K (review_date_90d) MUST write** the 90-day review date as a real date cell (see step 10).
   - **Column M (status) literal = `scoring`.**
3. Identify the affected partner(s) — partners whose primary function (per their Output Spec history) overlaps with the PR's automated capability.
4. Identify the non-beneficiary reviewer — a partner whose variable pay or long-tail does not increase as a result of the action.
5. Block PR merge by posting a **failing GitHub status check** named `oot/klarna-test` against the PR's head SHA. The status check is implemented by the GitHub Actions workflow at `.github/workflows/klarna-gate.yml` (shipped in Phase 8). The workflow re-runs on every push to the PR and reads the `klarna-test.xlsx` Klarna_Score sheet for the matching `test_id`; it sets the check to **passing** only when **all three** conditions hold simultaneously: `total_score >= 14` AND `scorer_signoff = Yes` AND `non_beneficiary_signoff = Yes`. The gate reads Klarna_Score directly and never consults the `status` column. The firm must have configured branch protection on the merge target to require the `oot/klarna-test` status check; without that protection, the gate is advisory rather than enforcing. Both setup steps (the workflow file and the branch-protection rule) are documented in the Code & QA SKILL.md (S4) and shipped by the cloud installer in Phase 9.
6. Post to Slack/dChat #klarna-test: "{{TEST_ID}}: PR #{{PR_NUMBER}} ({{TITLE}}) requires Klarna Test scoring before merge. Affected partner(s): {{LIST}}. Non-beneficiary reviewer: {{ASSIGNED}}. Scoring window: 5 business days. Reference: governance/KLARNA-TEST.md."
7. Email/dMail the founder + affected partner(s) + non-beneficiary reviewer with the same content.
8. Open a Ledger page at firm/klarna-tests/{{test_id}}.md with the full context.
9. Monitor the Klarna_Score sheet for the test_id; on completion, update Decision_Log column M `status` per the ADR-004 lifecycle: `proceeded` (I=PROCEED, work ships → remove the merge block) or, if I=HOLD, either `remediation` (gaps being fixed for a re-score) or `held` (decision stands). On `held`/`remediation`, leave the merge blocked and post the remediation list to #klarna-test. Once a `proceeded` row enters its 90-day review window, set M=`monitoring`; when the column-K review date passes and the outcome is recorded, close M back to `proceeded`.
10. Schedule the 90-day review (Q9 of the rubric) — write the date to Decision_Log column K (as a real date cell, per step 2), set a calendar reminder (cloud track) or cron entry (privacy track).

Failure handling: if scoring isn't complete in 5 business days, escalate to founder for direct decision; never auto-proceed without a complete score.
```

**Expected outputs:** Klarna Test entry; PR merge block; Slack/email notifications; Brain page; 90-day review scheduled.

**Privacy-track delta:** Webhook polling instead of push; dMail instead of email; dChat instead of Slack.

---

## R8 — Treasury Runway Update (OPTIONAL — only orgs adopting Unit Fund)

**Trigger:**
- Cloud: Claude Code Routine, Monday 08:00.
- Privacy: cron `0 8 * * 1`.

**Allowed Skills:** S10 (Finance & Treasury).

**MCP servers and tools:** Banking integrations (jurisdiction-specific HTTP APIs — most banks expose REST). GitHub connector / GitHub MCP (Brain-repo clone + signed commit + push). Code execution required (openpyxl appends today's snapshot row to X8 Runway_Calc).

**Prompt body:**

```
You are running the weekly treasury runway update for an ØØT organisation. Today is {{TODAY}}.

Your task (appended-row contract, ADR-004 §3 — order matters):
1. Pull current balances from all firm bank accounts and stablecoin wallets via configured banking/blockchain APIs.
2. **Append the day's Cash_Position rows FIRST** (one per account: date, account_label, balance, currency, balance_eur_equivalent — all literals). Burn is a delta over the just-appended history, so these rows must exist before you compute burn.
3. Compute total_cash_eur (FX-converted to base currency) by summing the day's Cash_Position rows in Python.
4. Read upcoming Obligations from treasury-runway.xlsx — payroll, variable, long-tail, suppliers, due in next 90 days (for context only; NOT the burn source).
5. Compute monthly_burn_average over rolling 3 months from historical Cash_Position deltas (realised outflow, NOT Obligations).
6. **Append one Runway_Calc snapshot row.** Write literals for snapshot_date (A), total_cash_eur (B), monthly_burn_average (C), unit_fund_outstanding_units (E), implied_redemption_value (F). **MUST write the D formula** `=IFERROR(B{R}/C{R},0)` and **the G formula** `=IFERROR(B{R}/IF(F{R}=0,1,F{R}),0)` on the appended row.
7. Write a one-paragraph markdown snapshot to `firm/treasury/{{TODAY}}.md` in the Ledger (runway_months, reserve_coverage_ratio, any breach) so R6's audit trail — which scans Ledger markdown — sees treasury activity (ADR-004 §4). Commit it in the SAME commit as the X8 mutation.
8. If runway_months < threshold (default 9 months) OR reserve_coverage_ratio < 1.0, post alert to Slack #treasury (or dChat) and email founder.

Failure handling: if any banking API is unreachable, flag in alert; never silently skip an account.
```

**Implementation:** clone Ledger; openpyxl appends the Cash_Position rows then the Runway_Calc snapshot row (with D/G formulas) to `firm/excel/treasury-runway.xlsx`; write `firm/treasury/{{TODAY}}.md`; `git add firm/excel/treasury-runway.xlsx firm/treasury/{{TODAY}}.md && git commit -S && git push`. Pattern C as R1.

**Expected outputs:** X8 Cash_Position + Runway_Calc updated; `firm/treasury/{{TODAY}}.md` snapshot; alert if thresholds breached; one signed commit on `main` carrying both.

**Privacy-track delta:** Banking APIs identical (most are HTTP-callable); same openpyxl operation locally; dChat instead of Slack.

---

## R9 — Firm Brain Synthesize (admin-run)

**Trigger:**
- Cloud and privacy: **weekly, admin-run.** Not a typical Claude Code Routine — runs on the admin's laptop (or always-on machine on the privacy track) via Curator's Shared Brain admin wizard or `curator sharedbrain synthesize` CLI. **Recommended cadence: every Sunday evening, before the new week opens.**

**Why this isn't a normal Routine.** R9 does not write to the Ledger; it mutates the Firm Brain via Curator's Shared Brain protocol (read `contributions/`, merge into `collective/<firm-domain>/wiki/`, append Provenance, commit + push to `<firm>-brain`'s main branch). Curator handles the writes — the framework's only responsibility is **ensuring it runs on the agreed cadence**.

**Allowed Skills:** S1 (My Curator). No others — synthesis is bounded to Curator's own logic.

**MCP servers and tools:** Curator desktop app or `curator` CLI on the admin's machine. Curator manages its own access to the `<firm>-brain` GitHub repo via the admin's PAT (held in the admin's Bitwarden, founders collection, per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md)).

**Operation (what happens during R9):**

1. Curator reads all contributions in `<firm>-brain/contributions/<fellow_id>/*.json` newer than `state/last-synthesis.json`.
2. For each affected page slug, Curator unions the new facts with the existing `collective/<firm-domain>/wiki/...` page.
3. **Jaccard similarity ≥ 0.5 + < 1.0** between candidate facts → Curator calls the configured LLM (Gemini Flash Lite in v3.0.0-beta) to resolve. Unresolved contradictions are written as `⚠️ CONFLICTING SOURCES — review needed` markers.
4. Provenance is appended: UUID by default; real names only when both `allow_name_attribution` (org-side) and `attribute_by_name` (contributor-side) flags are true.
5. `collective/<firm-domain>/wiki/index.md` is rebuilt.
6. `state/last-synthesis.json` is updated.
7. The whole change is signed-committed and pushed to `<firm>-brain` main (branch protection enforces signed commits).

**Expected outputs:**
- Updated `collective/<firm-domain>/wiki/**/*.md` in the Firm Brain repo.
- One signed commit on `main` from the admin's signing identity (NOT a Routine bot identity).
- Cost: typically under $0.01 per weekly run for a 100-page brain with 5 contributors (per Curator's own measurement).

**Admin checklist (each Sunday):**
1. `git pull` the latest contributions (the admin's local Curator does this automatically via the Pull button).
2. Run Curator's Synthesize via the wizard / CLI.
3. Scan the output for `⚠️ CONFLICTING SOURCES` markers; if present, work with the conflicting partners to resolve in their personal Curator domains, then re-run.
4. Confirm the push lands on `<firm>-brain` main with a Verified signature.
5. Post a brief summary to firm comms ("Firm Brain synthesized for week of YYYY-MM-DD; N contributions merged, M conflicts open"); partners run Pull at their leisure.

**Failure handling:**
- LLM API unavailable: defer synthesis; rerun next day. The conflict-resolution step is the only LLM-dependent part — union-merge runs without LLM.
- Branch protection rejects the push: investigate (signed-commit configuration, force-push attempt, etc.). Do NOT bypass protection.
- A specific contribution payload is malformed: Curator logs the failure and skips that payload; the affected contributor is notified to re-Push.

**Privacy-track delta:**
- Runs on the always-on machine instead of the admin's daily laptop.
- The synthesis LLM is the **only remaining cloud-LLM dependency** in the Gen 1 privacy stack. Curator v3.1's local-LLM synthesis support will remove this; tracked in [`GENERATIONS.md`](../GENERATIONS.md).
- Cron entry on the always-on machine (admin's machine if dedicated): `0 19 * * 0 /usr/local/bin/curator sharedbrain synthesize --brain <firm>-brain >> ~/oot/logs/r9.log 2>&1`.

**Plan-tier note:** R9 runs on the admin's machine via Curator's local CLI; it does NOT count against Claude Code Routine per-day limits.

---

## Cross-cutting concerns

**Privacy-track scheduling reliability.** The privacy track requires the always-on machine to be running. Recommended hardware: Mac mini, Intel NUC, or Raspberry Pi 5 with at least 16GB RAM (32GB for R3 with larger models). Recommended UPS for unattended operation.

**Cloud-track concurrency.** Claude Code Routines run on Anthropic infrastructure; they tolerate the partner's laptop being closed. They do not tolerate Anthropic infrastructure being down — design for this with idempotent prompts (running a Routine twice on the same day produces the same output; Pattern C makes this natural via git's content-addressed commits).

**Routines and the Klarna Test.** Routines are themselves subject to the Klarna Test. Any new Routine that automates a function previously performed by a partner triggers R7. The framework's authors run R7 against R7 — circular, but the discipline holds.

**Auditability.** Every Routine writes to the daily audit log (R6). For EU-operating firms, this is a Article 12 obligation. For others, it is good hygiene that costs almost nothing and prevents many disputes.

**Cost containment (cloud track).** Estimate Routine costs monthly via X6 (agent-skill-roi.xlsx). Cloud Routines for a 10-partner firm running all 8 daily/weekly/monthly typically cost €30–€80/month in Anthropic API fees. Privacy-track marginal cost is electricity for the always-on machine.

**Versioning.** Each Routine prompt should be versioned. Update the prompt → bump the version (semver in the file frontmatter) → log the change in firm/routines/changelog.md. Old prompt outputs remain valid; new outputs use the new prompt.

---

## Generation acceptance criteria

For each of the 16 generated Routine files (8 cloud + 8 privacy):

- File has YAML frontmatter with: routine_id, version, track (cloud/privacy), trigger_spec, allowed_skills, mcp_servers, recommended_model, last_updated.
- The prompt body matches this SPEC.
- Privacy-track files include the exact cron / launchd / Task Scheduler invocation line.
- Each file ends with a "Setup checklist" — 3–7 steps to install the Routine the first time.
- The `routines/README.md` summarises all 16 files with a setup-order recommendation: cloud track install order is R5 first (no dependencies), then R6, then R1, then R2, then R3, then R7, then R4, then R8 (optional). Privacy-track order is identical.