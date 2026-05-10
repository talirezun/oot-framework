# Routines — SPEC

The eight ØØT scheduled Routines, in two flavours: cloud track (**Claude Code Routines** — Anthropic's cloud-hosted scheduled-agent product, launched 14 April 2026) and privacy track (OS-native scheduling — cron / launchd / Task Scheduler — hitting headless LM Studio via `llmster`). The substrates differ; the prompts are functionally identical so a firm can switch tracks without rewriting Routine logic.

Claude Code generates 16 markdown files (8 in `routines/cloud/`, 8 in `routines/privacy/`) from this spec.

---

## Operational state lives in the Brain repo (ADR-001)

All `.xlsx` operational state — partner-output-ledger, reward-species-declaration, business-review, klarna-test, agent-skill-roi, eu-ai-act-mapping, treasury-runway, oot-readiness, perception-gap-survey — lives in the **firm's Brain GitHub repo**. Routines mutate these files via **openpyxl in Claude Code's code-execution capability**, then **signed-commit and push** the mutation to the protected `main` branch. No Google Sheets, no native Drive write-in-place, no remote Excel MCP. See [`docs/internal/ADR-001-cloud-routine-excel-writeback.md`](../docs/internal/ADR-001-cloud-routine-excel-writeback.md) for the full decision rationale and alternatives considered.

Track symmetry: cloud and privacy Routines perform the same operation. Privacy Routines run against a local clone; cloud Routines run against a fresh clone created on Anthropic's infrastructure for each Routine run.

**Spreadsheet viewers are user choice.** Microsoft Excel, LibreOffice (free, open-source), Apple Numbers, Excel-for-Web, Google Sheets via "Open with" / import — all open `.xlsx` natively or via auto-conversion. The framework does not require any specific paid app.

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

**Brain-repo access.** Routines that read or write `.xlsx` files require the Brain repo to be cloneable + pushable from the Routine. Configure a deploy key or PAT scoped to the Brain repo, with signing (GPG or SSH) configured per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md). Only the firm's bot identity (e.g. `oot-bot`) commits via Routines; the bot identity is exempted from the `firm/audit-logs/*` reviewer rule per the existing `[skip review]` mechanism (see `skills/code-qa/SKILL.md` §4.0).

**Expected output.** Where the Routine writes — Brain pages, Excel files (mutated in-repo + signed commit), Slack/dChat posts, audit logs.

**Failure handling.** What happens if the Routine errors (e.g., GitHub API rate-limited, MCP unreachable, model error, signing key unavailable).

**Privacy-track delta.** Where the privacy-track equivalent differs from the cloud version. For Excel writes the operation is identical (openpyxl on a local Brain-repo clone) — only the scheduling substrate differs.

---

## R1 — Daily Output Capture

**Trigger:**
- Cloud: Claude Code Routine, daily 18:00 in the firm's primary timezone.
- Privacy: cron `0 18 * * *` (Linux/macOS) or Task Scheduler equivalent (Windows), invoking `llmster --skill compensation-attribution --prompt-file routines/privacy/r1.prompt.md`.

**Allowed Skills:** S3 (Compensation & Attribution), S1 (My Curator).

**MCP servers and tools:**
- Cloud: GitHub connector (Brain-repo clone + signed commit + push). Slack connector (read tracked channels + post `#output-log` and `#ops`). Google Workspace connector (**read-only**, for `{{TRACKED_FOLDERS}}` document discovery). Code execution required (openpyxl writes to X1 in the cloned Brain repo).
- Privacy: same operation locally. GitHub MCP for the commit/push. Local filesystem for the Brain-repo clone. 4thtech CLI/SDK for dChat thread reads (replaces Slack). No Excel MCP needed — openpyxl is a Python library, used directly by `llmster`.

**Prompt body:**

```
You are running the daily output capture for an ØØT organisation. Today is {{TODAY}}.

Your task: read all output signals from the past 24 hours across the following sources, and append rows to partner-output-ledger.xlsx (file X1) per its schema in templates/excel/SPEC.md.

Sources to read:
1. GitHub: all commits across all firm repos in the last 24 hours. Include: commit hash, author (note any Co-authored-by: trailers indicating AI assistance), files changed, lines added/deleted, PR association if applicable.
2. Slack channels listed in {{TRACKED_CHANNELS}} (or 4thtech dChat threads on privacy track): outputs explicitly tagged with #output, contracts mentioned in #commercial, deals closed in #sales.
3. Google Drive (or local filesystem on privacy track): documents created or significantly modified in {{TRACKED_FOLDERS}}.

For each output:
- Generate a log_id following the format OL-YYYYMMDD-NNN.
- Determine the partner_id from the author/owner (consult the partners Brain page if uncertain; if multiple authors, create one row per partner with a fractional output_value note).
- Classify output_type per the X1 schema.
- Reference the output_spec_ref from the Brain if one exists; flag for human review if not.
- Estimate value_tier (S/M/L/XS) based on the output_spec value envelope; default to L if no spec exists.
- Estimate ai_authored_pct from commit trailers and change patterns (best-effort; partner can correct).
- Set `rework_within_30d` to "No" by default. This field is **updated retroactively by R1 on every subsequent run within the next 30 days** using the following deterministic detection rule:

  > A new commit `C_new` marks an earlier commit `C_old` as `rework=Yes` if **all four** conditions hold: (a) same `partner_id` on both commits; (b) `C_new` timestamp is within 30 days after `C_old`; (c) ≥50% file overlap between the two commits' changed-files sets; (d) `C_new`'s commit message OR associated PR title/description matches the regex `\b(fix|revert|hotfix|redo|retry|reapply|backout|rollback)\b` (case-insensitive). When all four hold, R1 **updates the prior X1 row's `rework_within_30d` to "Yes"** (which zeroes out its `computed_variable` via the X1 column-L formula). The Routine logs every retroactive update in the daily Brain summary under a `## Retroactive rework detections` heading.

- Resolve `partner_multiplier` (column J) by **reading X2 directly at write time** — do not rely on a cross-workbook Excel formula (see `templates/excel/SPEC.md` X1). Compute `value_envelope` (column K) per the lookup table embedded in X1.

**Implementation (the canonical Pattern C operation per ADR-001):**

1. Clone the firm's Brain repo to a working directory: `git clone <BRAIN_REPO_URL> /tmp/brain && cd /tmp/brain && git pull`.
2. Open `firm/excel/partner-output-ledger.xlsx` (X1) with openpyxl in code execution.
3. Find the next empty row in Output_Log using **column A (log_id) as the determinant**, NOT `ws.max_row`. The value_envelope_table embedded at O1:P5 makes `max_row` report 5 even when sample data only fills rows 2-4 — using `max_row + 1` would leave a permanent ghost gap. Pseudocode:
   ```python
   r = 2
   while ws.cell(r, 1).value:
       r += 1
   # r is now the first empty row to append at
   ```
4. Append the new rows starting at row `r`. Per row R appended:
   - **Columns A-I:** write the captured values directly to row R (log_id, date, partner_id, output_type, output_ref, output_spec_ref, value_tier, ai_authored_pct, rework_within_30d).
   - **Column J (`partner_multiplier`):** resolve by reading X2 (`firm/excel/reward-species-declaration.xlsx`) at write time per the v1.0 design decision (no cross-workbook formulas). Write the resolved number.
   - **Column K (`value_envelope`):** **MUST write the formula** `=VLOOKUP(G{R}, $O$2:$P$5, 2, FALSE)` (with `{R}` substituted to the row number). Without this formula the cell stays blank and contributes zero to Monthly_Variable's SUMIFS — silent failure mode that R3 will not catch. Do NOT leave K blank.
   - **Column L (`computed_variable`):** **MUST write the formula** `=K{R}*J{R}*IF(I{R}="Yes", 0, 1)` (with `{R}` substituted). Same discipline as K — blank L means zero variable pay for that output until someone manually patches it.
   - **Column M (`notes`):** write any human-readable annotation, optional.
4. For any retroactive rework_within_30d updates, edit the corresponding Output_Log rows in place.
5. Save X1.
6. Write the daily Brain summary as a markdown file at `firm/output-logs/YYYY-MM-DD.md` following the template at `templates/brain/daily-output-log.md`. Include: total outputs captured, breakdown by partner, any anomalies (e.g., a partner with zero outputs for >3 consecutive days), any retroactive rework_within_30d updates.
7. Stage and signed-commit both changes: `git add firm/excel/partner-output-ledger.xlsx firm/output-logs/YYYY-MM-DD.md && git commit -S -m "R1: append <N> outputs for <date>; <K> retroactive rework updates"`.
8. Push to `main`: `git push origin main`. The bot identity is exempted from the `firm/audit-logs/*` reviewer rule per `[skip review]`; for `firm/excel/*` and `firm/output-logs/*` paths, no review is required (these paths are append-mostly Routine output, not audit log).

Post a short summary to Slack #output-log (or 4thtech dChat #output-log on privacy track): "{{TODAY}} captured {{N}} outputs from {{P}} partners. Anomalies: {{LIST_OR_NONE}}."

Failure handling: if any source is unreachable, log the failure to the daily summary, capture from available sources, and post a notice to #ops. If git push fails (signing key unavailable, branch protection rejects, network), retry with exponential backoff up to 3 attempts; if still failing, post to #ops and DO NOT downgrade to an unsigned commit.
```

**Expected outputs:**
- Rows appended to `firm/excel/partner-output-ledger.xlsx` in the Brain repo.
- Brain page at `firm/output-logs/YYYY-MM-DD.md`.
- One signed commit on `main` carrying both changes.
- Slack/dChat summary post.

**Privacy-track delta:**
- Sources: GitHub via GitHub MCP, dChat via 4thtech CLI/SDK, local filesystem via Desktop Commander MCP.
- Excel writes: same openpyxl operation against a local Brain-repo clone — no Excel MCP needed for the Routine path. (Excel MCP remains available as an *optional* tool for ad-hoc human-in-the-loop work, not a Routine dependency.)
- Posting: dChat to a designated channel.
- Cron entry: `0 18 * * * /usr/local/bin/llmster --model qwen-3-14b --skill compensation-attribution --skill my-curator --prompt-file ~/oot/routines/privacy/r1.prompt.md >> ~/oot/logs/r1.log 2>&1`

---

## R2 — Weekly BR Prep

**Trigger:**
- Cloud: Claude Code Routine, Friday 08:00.
- Privacy: cron `0 8 * * 5`.

**Allowed Skills:** S5 (Reporting & Business Review), S1 (My Curator).

**MCP servers and tools:** GitHub connector / GitHub MCP (Brain-repo clone + signed commit + push). Slack / 4thtech connector. Code execution required (openpyxl reads X1, X4, X6 and writes X3 in the cloned Brain repo).

**Prompt body:**

```
You are preparing the Friday Business Review agenda for an ØØT organisation. The BR meeting starts at 14:00 today.

Your task: populate business-review.xlsx (X3) Weekly_Review sheet for the week starting {{MONDAY_DATE}} and ending today.

1. Read partner-output-ledger.xlsx Output_Log for the past 7 days. Identify the top 5 outputs by value_envelope. For each: who shipped it, what tier, brief description from the output_spec_ref. Write to column B (notable_outputs) as a markdown bullet list.

2. Query the Brain for blocker tags raised in the past 7 days that remain open. Write to column C (blockers).

3. Read klarna-test.xlsx Decision_Log for any tests in {{state IN ("scoring", "remediation", "monitoring")}} state. Write to column D (klarna_test_status).

4. Read agent-skill-roi.xlsx for week-over-week deltas on KPIs (customer_count, treasury_runway_months, ai_skill_roi). Write to column E (kpi_movements).

5. Identify decisions due — items in the Brain tagged decision-pending. Write to column F (decisions_due).

Post a draft summary to Slack #business-review (or dChat equivalent) by 09:00:
"BR agenda for {{TODAY}} 14:00 ready. Highlights: {{TOP_3_FROM_NOTABLE}}. Klarna in flight: {{COUNT}}. Decisions due: {{COUNT}}."

After the BR meeting (signaled by manual trigger or by the Decisions_Log getting populated), commit the final summary as a Brain page at firm/business-reviews/YYYY-MM-DD.md.

**Implementation:** clone the Brain repo, read X1 / X4 / X6 via openpyxl, write the new row(s) to X3's Weekly_Review sheet via openpyxl, write the Brain summary markdown, signed-commit both changes, push to `main`. Same Pattern C as R1 (ADR-001).

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

**MCP servers and tools:** GitHub connector / GitHub MCP (Brain-repo clone + signed commit + push). Slack / 4thtech connector for `#compensation` posts. Email / dMail for per-partner statement delivery. Code execution required (openpyxl reads X1, X2 and writes X1's Monthly_Variable sheet in the cloned Brain repo). Polling job to detect partner acknowledgement runs daily as a separate Routine fire (see step 8 below).

**Recommended model:** Cloud — Claude Opus (compensation accuracy is high-stakes). Privacy — largest local model available.

**Prompt body:**

```
You are running the monthly variable pay calculation for an ØØT organisation. The calculation is for {{LAST_MONTH}} (first day to last day inclusive).

Your task: lock the previous month's Output_Log and produce per-partner variable pay drafts.

1. Read partner-output-ledger.xlsx Output_Log filtered to last_month. For each row, verify the rework_within_30d field is current (look forward to today's date and recompute if any output from last_month had rework detected since).

2. Aggregate per partner: total_outputs, total_variable (SUM of computed_variable column).

3. Read reward-species-declaration.xlsx for each partner's base_amount and current reward_species parameters.

4. Populate the Monthly_Variable sheet of partner-output-ledger.xlsx for {{LAST_MONTH}}: one row per partner, with total_outputs, total_variable, base_pay (last_month proportional), total_compensation, sign_off_status='draft'.

5. For each partner, generate a personalised statement at firm/partners/{{partner_id}}/variable-statements/YYYY-MM.md following the template at `templates/brain/variable-statement.md`. Statement includes: month, total outputs (with the top 5 listed by value), variable computation with the multiplier, base pay, total compensation, list of any retroactive rework_within_30d zero-outs from prior months that affected this month's pool. The statement is the partner's official record of their variable for the month. The template ends with an explicit acknowledgement block:

   ```markdown
   ## Acknowledgement

   - [ ] I have reviewed this statement and agree with the calculation.
   - [ ] I dispute the calculation (open Tier 1 dispute per `governance/DECISION-RIGHTS.md`).

   _Sign by editing this page and ticking the appropriate box, then commit._
   ```

6. Send the statement to each partner via email (cloud) or 4thtech dMail (privacy track). Subject: "Variable pay statement for {{LAST_MONTH}} — review by {{REVIEW_DEADLINE}}". Body links to the Brain statement page.

7. Post to Slack/dChat #compensation: "Monthly variable drafts for {{LAST_MONTH}} are ready. {{COUNT}} partners. Total: {{TOTAL_EUR}}. Review window: 5 business days. Founder approval required before payment."

8. **Acknowledgement detection** — the Routine polls each partner's statement page once daily and parses the acknowledgement block. The first checked box wins. Set `sign_off_status` per the table:

   | Detected state in Brain page | sign_off_status |
   |---|---|
   | First box ticked, second unticked | `partner_reviewed` |
   | Second box ticked (dispute), first unticked | `partner_disputed` (escalates to Tier 1 per DECISION-RIGHTS.md; `R3` does not advance the row to `founder_approved`) |
   | Both ticked | `partner_disputed` (the partner's intent is unclear; treat as dispute, ask for clarification) |
   | Neither ticked, ≥5 business days since send | `partner_unresponsive` (escalate to founder; never auto-approve) |
   | Neither ticked, <5 business days since send | `draft` (no change) |

   Slack reactions are **not** the canonical signal; only the Brain checkbox counts. This makes the audit trail self-contained in the Brain (auditable from the firm's git history alone, no third-party messaging dependency).

9. After all partner reviews complete OR after 5 business days (whichever first), compile a founder-approval packet at firm/compensation/YYYY-MM/founder-approval.md. Founder approves; sign_off_status moves to 'founder_approved'. Payment processing then proceeds (manual in Gen 1; automated stablecoin in Gen 2).

Failure handling: if any partner does not respond within the 5-day window, escalate to founder for review. Never auto-approve a contested calculation.
```

**Implementation:** clone Brain repo; read X1 Output_Log (filtered to last_month) and X2 reward-species via openpyxl; write the Monthly_Variable rows + per-partner statement markdown files; signed-commit; push. Same Pattern C as R1 (ADR-001). For the daily acknowledgement polling step, the polling Routine (or a single Routine that handles steps 1-7 on day 1 and step 8 daily through day +5) re-clones the Brain repo, reads each partner's statement page for the checkbox state, updates X1 Monthly_Variable's `sign_off_status` column, signed-commits + pushes. Each polling pass is a separate Routine run; budget for 5–7 R3-polling fires per month in the Anthropic plan calculation.

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

1. Read all reward-species-declaration files (or sheets) for the firm. Extract every Long_Tail_Schedule row where end_date is empty OR > {{LAST_QUARTER_END}}, AND start_date <= {{LAST_QUARTER_END}}.

2. For each such (partner, output) pair, query the Brain or financial system for the realised outcome attributable to the output during {{LAST_QUARTER}}: revenue generated, cost saved, customer impact metric — the metric committed to in the Output Spec.

3. Compute the partner's long-tail payment for the quarter as: outcome_attributable × partner_share_pct.

4. Update the partner's Long_Tail_Schedule sheet: append the quarter to total_settled_to_date.

5. Generate a per-partner long-tail statement at firm/partners/{{partner_id}}/long-tail-statements/YYYY-Q{{N}}.md.

6. Send statement via email/dMail. Founder approval required before payment.

7. Post summary to Slack/dChat #compensation.

Failure handling: if outcome attribution data is missing for an output, flag for founder + affected partner review; do not pay until resolved.
```

**Implementation:** clone Brain repo; read X2 across all partner sheets via openpyxl; compute and write settlement; write per-partner long-tail statement markdown; signed-commit; push. Pattern C as R1.

**Expected outputs:** Per-partner long-tail statements; updated Long_Tail_Schedule sheets; founder-approval packet; signed commit on `main`.

**Privacy-track delta:** Same openpyxl operation locally; dMail instead of email.

---

## R5 — Brain Health Check

**Trigger:**
- Cloud: Claude Code Routine, Sunday 09:00.
- Privacy: cron `0 9 * * 0`.

**Allowed Skills:** S1 (My Curator).

**MCP servers and tools:** my-curator MCP (remote-HTTP for cloud, stdio for privacy). Slack / 4thtech connector. GitHub connector / GitHub MCP for the brain-health snapshot commit. No Excel writes; no code-execution requirement beyond what my-curator needs.

**Prompt body:**

```
You are running the weekly Brain health check for an ØØT organisation.

Your task:
1. Run my-curator's scan_wiki_health on every domain.
2. Compile a summary of issues by type: broken wikilinks, orphan pages, semantic duplicates, stale pages (>90 days no update on pages tagged active).
3. Auto-fix the safe categories (broken wikilinks where the target slug exists with a typo correctable via fix_wiki_issue).
4. For unsafe categories, post a list to Slack #brain-health (or dChat equivalent) for human review and fix-this-week tagging.
5. Run scan_semantic_duplicates and post any new duplicate clusters (clusters not previously dismissed).
6. Update firm/brain-health/YYYY-WW.md with the weekly health snapshot.

Failure handling: if Curator is unreachable, retry hourly until 18:00; if still unreachable, escalate to ops.
```

**Expected outputs:** Brain health snapshot page; Slack/dChat post; auto-fixes applied.

**Privacy-track delta:** dChat instead of Slack.

---

## R6 — EU AI Act Audit Trail

**Trigger:**
- Cloud: Claude Code Routine, daily 23:00.
- Privacy: cron `0 23 * * *`.

**Allowed Skills:** S7 (Governance & Compliance).

**MCP servers and tools:** my-curator MCP (read agent-decision data). GitHub connector / GitHub MCP (signed commit + push of the daily audit log). Code execution required (openpyxl writes X7 Audit_Log_Index after the audit-log markdown is committed).

**Prompt body:**

```
You are appending today's audit trail to the EU AI Act Article 12 record for an ØØT organisation. Today is {{TODAY}}.

Your task:
1. Read all agent decisions logged today across all firm Routines (R1, R2, R3, R4, R5, R7, R8) and any ad-hoc Skill invocations that produced an output affecting partners or customers.
2. For each decision, capture: timestamp, AI system identifier (which model + Skill), decision context (sanitised input summary), output, human reviewer if any, related use_case_id from eu-ai-act-mapping.xlsx.
3. Append to firm/audit-logs/YYYY-MM-DD.md following the template at templates/brain/audit-log-day.md.
4. Update eu-ai-act-mapping.xlsx Audit_Log_Index sheet with today's entry count and any anomalies flagged.
5. Commit the audit log day file via GitHub MCP using a **signed commit** (GPG or SSH). This commit MUST land on the protected `main` branch (or the firm's chosen audit branch) which has the following branch-protection rules configured: (a) force-push disabled; (b) deletion disabled; (c) signed commits required; (d) at least one reviewer for any modification (Routine R6's commits are auto-approved by a designated bot account or use a `[skip review]` exemption only for append-only audit-log paths under `firm/audit-logs/`). These three protections together — append-only path, force-push block, signed commits — provide the practical immutability required by Article 12 record-keeping. (True triple-entry / external anchoring is Generation 2; see `GENERATIONS.md`.)

Failure handling: if any source unreachable, append from available sources and flag the gap. The audit log MUST be appended every day; an empty day is a noted "no agent activity" entry, not a missing day. If the signed-commit step fails (signing key unavailable, branch protection rejects the push), R6 retries hourly; if still failing at 02:00 the next day, escalate to founder via Slack `#ops` — DO NOT downgrade to an unsigned commit silently.
```

**Expected outputs:** Daily audit log Brain page; X7 Audit_Log_Index updated; **signed** git commit on the protected branch.

**Privacy-track delta:** All git operations via GitHub MCP. The audit log discipline is identical. Signing key is stored in a Trezor or YubiKey-backed slot, never in plaintext on the always-on machine.

**Setup pre-requisite (one-time):** The firm must configure GitHub branch protection on `main` (or the audit branch) with: force-push disabled, deletion disabled, "Require signed commits" enabled. The cloud installer (Phase 9) and the Code & QA SKILL.md (S4) document this configuration. Without these protections the Article 12 retention claim does not hold.

---

## R7 — Klarna Test Trigger

**Trigger:**
- Cloud: Claude Code Routine fired by GitHub event (PR labelled `ai-replaces-human`). Optionally also: manual trigger from a partner via Slack slash command.
- Privacy: GitHub webhook polled by a local listener (every 5 minutes) hitting llmster.

**Allowed Skills:** S6 (Change Management), S4 (Code & QA).

**MCP servers and tools:** GitHub connector / GitHub MCP (PR status check, Brain-repo clone + signed commit + push). Slack / 4thtech connector. Email / dMail. Code execution required (openpyxl appends row to X4 Decision_Log).

**Prompt body:**

```
You are launching a Klarna Test scoring for an ØØT organisation. The trigger is PR #{{PR_NUMBER}} in repo {{REPO}} labelled 'ai-replaces-human'.

Your task:
1. Generate a test_id following format KT-YYYY-NNN.
2. Append a row to klarna-test.xlsx Decision_Log with: test_id, today's date, decision_summary (extracted from PR title + description), trigger='pr_label', trigger_ref=PR URL, status='scoring'.
3. Identify the affected partner(s) — partners whose primary function (per their Output Spec history) overlaps with the PR's automated capability.
4. Identify the non-beneficiary reviewer — a partner whose variable pay or long-tail does not increase as a result of the action.
5. Block PR merge by posting a **failing GitHub status check** named `oot/klarna-test` against the PR's head SHA. The status check is implemented by the GitHub Actions workflow at `.github/workflows/klarna-gate.yml` (shipped in Phase 8). The workflow re-runs on every push to the PR and reads the `klarna-test.xlsx` Klarna_Score sheet for the matching `test_id`; it sets the check to **passing** only when **all three** conditions hold simultaneously: `total_score >= 14` AND `scorer_signoff = Yes` AND `non_beneficiary_signoff = Yes`. The firm must have configured branch protection on the merge target to require the `oot/klarna-test` status check; without that protection, the gate is advisory rather than enforcing. Both setup steps (the workflow file and the branch-protection rule) are documented in the Code & QA SKILL.md (S4) and shipped by the cloud installer in Phase 9.
6. Post to Slack/dChat #klarna-test: "{{TEST_ID}}: PR #{{PR_NUMBER}} ({{TITLE}}) requires Klarna Test scoring before merge. Affected partner(s): {{LIST}}. Non-beneficiary reviewer: {{ASSIGNED}}. Scoring window: 5 business days. Reference: governance/KLARNA-TEST.md."
7. Email/dMail the founder + affected partner(s) + non-beneficiary reviewer with the same content.
8. Open a Brain page at firm/klarna-tests/{{test_id}}.md with the full context.
9. Monitor the Klarna_Score sheet for the test_id; on completion, update Decision_Log row status to 'proceeded' (>=14) or 'held' (<14). On 'proceeded', remove the merge block. On 'held', leave the merge blocked and post the remediation list to #klarna-test.
10. Schedule the 90-day review (Q9 of the rubric) — write the date to Decision_Log column K, set a calendar reminder (cloud track) or cron entry (privacy track).

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

Your task:
1. Pull current balances from all firm bank accounts and stablecoin wallets via configured banking/blockchain APIs.
2. Compute total_cash_eur (FX-converted to base currency).
3. Read upcoming Obligations from treasury-runway.xlsx — payroll, variable, long-tail, suppliers, due in next 90 days.
4. Compute monthly_burn_average over rolling 3 months.
5. Update treasury-runway.xlsx Runway_Calc sheet with today's snapshot row: total_cash_eur, monthly_burn_average, runway_months, unit_fund_outstanding_units, implied_redemption_value, reserve_coverage_ratio.
6. If runway_months < threshold (default 9 months) OR reserve_coverage_ratio < 1.0, post alert to Slack #treasury (or dChat) and email founder.

Failure handling: if any banking API is unreachable, flag in alert; never silently skip an account.
```

**Implementation:** clone Brain repo; openpyxl appends snapshot row to `firm/excel/treasury-runway.xlsx`; signed-commit; push. Pattern C as R1.

**Expected outputs:** X8 Runway_Calc updated; alert if thresholds breached; signed commit on `main`.

**Privacy-track delta:** Banking APIs identical (most are HTTP-callable); same openpyxl operation locally; dChat instead of Slack.

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