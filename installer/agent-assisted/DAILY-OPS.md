# Daily operations — agent-runnable playbook

**Audience:** Founder, every day they open their laptop. The framework's daily-driver assistant.
**Read by:** the founder's coding agent (Claude Code, Augment Code, Aider, OpenCode, Cline, Continue, ChatGPT in code-execution mode — any agent meeting the [capability spec](AGENT-CAPABILITY-SPEC.md)).
**You will end with:** local clone synced from GitHub, today's state summarised, any anomalies flagged.

> 🚀 **One-line prompt to feed your agent:**
>
> ```
> Read installer/agent-assisted/DAILY-OPS.md and execute the daily sync for my firm at <FIRM_FOLDER>. Read ~/.oot/firm-state.yaml for context.
> ```
>
> *(Replace `<FIRM_FOLDER>` with your actual path, e.g. `/Users/talirezun/00T-test-company`.)*

---

## Agent: what to do, in order

### 1. Pull latest state from GitHub

```bash
cd <FIRM_FOLDER>
git fetch origin main
git status
```

If `git status` shows any local uncommitted changes:
- Ask the user: "You have local changes to `<files>`. Do you want me to (a) commit and push them, (b) stash for later, or (c) discard?"
- Default to (b) stash if the user is unsure.

Then:
```bash
git pull origin main --rebase
```

Capture the **last-sync commit SHA** from `~/.oot/firm-state.yaml` (if it exists) so you know what's new.

### 2. Summarise what changed since the last sync

```bash
# What landed since last sync
git log <LAST_SYNC_SHA>..HEAD --pretty=format:'%h %ai %s' --no-merges
```

Read the new commits. Categorise them:

- **Routine commits** — typically authored by the bot identity (e.g. `oot-bot` or `<firm-name> Bot`) with subjects like `R1: append <N> outputs`, `R6: audit log YYYY-MM-DD`. Summarise: "R1 captured <N> outputs across <K> partners. R6 audit log for <date> contains <X> agent decisions."
- **Human commits** — partner-authored. Summarise per-partner.
- **Anomalies** — any commit subject mentioning "FAILED", "ESCALATE", "ERROR", or any retroactive `rework_within_30d` flips. Surface these prominently.

### 3. Surface today's operational state

For each of these, check and report:

#### 3a. Today's output log

```bash
ls -la firm/output-logs/$(date +%Y-%m-%d).md 2>/dev/null
```

If it exists: open it and summarise to the user (3-5 bullet points of what R1 captured yesterday).
If it doesn't: say "No R1 output log for today yet. If R1 fires daily 18:00 (firm timezone), this is expected if you're opening your laptop before then."

#### 3b. Today's audit log

```bash
ls -la firm/audit-logs/$(date +%Y-%m-%d).md 2>/dev/null
```

Same pattern as 3a. R6 fires daily 23:00; if it's morning the log is from yesterday.

#### 3c. Pending partner acknowledgements (only relevant after R3 fires on the 1st of the month)

```bash
ls -la firm/partners/*/variable-statements/$(date +%Y-%m).md 2>/dev/null
```

For each statement that exists this month: check the acknowledgement block. If the partner hasn't yet ticked either checkbox, count days since the statement was committed:

```bash
git log -1 --format='%cd' --date=short firm/partners/<id>/variable-statements/$(date +%Y-%m).md
```

If >5 business days have passed and neither box is ticked, flag for founder review.

#### 3d. R5 weekly Brain health (only relevant Sundays)

```bash
ls -la firm/brain-health/$(date +%G-W%V).md 2>/dev/null
```

If it's Sunday and the current week's health file doesn't exist by 10:00, surface that R5 may have failed.

#### 3e. Klarna tests in flight

```bash
ls firm/klarna-tests/*.md 2>/dev/null | xargs grep -l 'status: scoring' 2>/dev/null
```

For each test in `scoring` state, count days since it was opened. If >5 business days, flag.

### 4. Verify signing key + GitHub auth are healthy

```bash
# Most recent commit signature
git log --show-signature -1 2>&1 | grep -E 'gpg: Good signature|gpg: Bad signature|signature error' | head -1

# GitHub auth (a quick remote check)
git ls-remote origin HEAD 2>&1 | head -1
```

If either fails: surface to the user with the exact error. Don't try to fix silently; signing/auth failures are diagnostic.

### 5. Update the firm-state file

Persist the new last-sync info at `~/.oot/firm-state.yaml`:

```yaml
firm: <firm name>
firm_folder: <FIRM_FOLDER>
ledger_repo_url: <URL>
last_sync: <ISO8601 timestamp>
last_sync_sha: <commit SHA after pull>
notes: |
  Any flagged anomalies or follow-ups from today's sync.
```

### 6. Present the summary to the user

Format the output to the user as a brief morning brief:

```
🟢 Ledger synced (was at <old SHA>, now at <new SHA>).

What's new since last sync:
  - R1 (daily 18:00): captured <N> outputs across <K> partners
  - R6 (daily 23:00): <X> agent decisions logged
  - <human commit by partner-X>: <subject>

Today's state:
  ✓ R1 output log present
  ✓ R6 audit log present
  ⏳ R5 brain-health: scheduled for Sunday 09:00
  📋 1 partner statement pending acknowledgement (3 of 5 days remaining)

Health:
  ✓ Signing key works (last commit verified)
  ✓ GitHub auth OK

Anything you want to dig into?
```

If you have access to my-curator MCP and the firm uses Configuration B (firm repo is the Curator vault), offer to run `scan_wiki_health` or surface recent Brain pages. If Configuration A (separate vault), skip — my-curator queries against the firm operational folder won't work.

---

## What this playbook does NOT do

- It does not configure Routines. That's install-time, not daily-ops.
- It does not approve compensation. R3's monthly variable calc produces drafts; founder approval is human-only.
- It does not sign anything legal. Partner Charter, Reward Species Declaration, Klarna Test sign-offs — human-signed.
- It does not edit `.xlsx` files. The agent reads them via openpyxl for verification but doesn't mutate. Mutations are Routines' job (Pattern C — see [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md)) or human's job via the spreadsheet app.

---

## Failure handling

If any step fails:

1. Tell the user exactly what failed (paste the error).
2. Propose a fix (link to `docs/07-troubleshooting.md` for the matching pitfall).
3. Wait for the user to decide whether to retry, fix manually, or skip.

Do not retry silently. Do not pretend the step succeeded when it didn't.

---

## Why this exists

`git pull` is a one-line command, but for a non-technical founder it's the kind of one-line command that doesn't get done. The framework's architecture (Pattern C) means **GitHub is the source of truth** and **the user's local clone is one of several working copies**. The two need to stay in sync, but the sync is manual.

A coding agent — which the founder probably already has installed for the framework's Path A install — closes the loop. They paste a short prompt every morning; the agent handles the git operations + surfaces what changed. Two minutes of attention per day, no terminal commands the founder has to remember.

Long-term, an ØØT desktop application (Gen 2 candidate, see [`GENERATIONS.md`](../../GENERATIONS.md)) will wrap this in a graphical UI. For Gen 1, the agent-as-daily-UI pattern is the right interim.

---

## See also

- [`WEEKLY-OPS.md`](WEEKLY-OPS.md) — Friday BR prep + Sunday brain-health review
- [`MONTHLY-OPS.md`](MONTHLY-OPS.md) — 1st-of-month variable-pay walkthrough + partner-acknowledgement polling
- [`docs/AUTOMATION-PIPELINE.md`](../../docs/AUTOMATION-PIPELINE.md) — how Routines + the local clone fit together
- [`docs/MODULES.md`](../../docs/MODULES.md) — what to add to the daily ops as the firm scales
