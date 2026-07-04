# Weekly operations — agent-runnable playbook

**Audience:** Founder, typically Friday morning before the BR + Sunday morning for brain-health review.
**Read by:** the founder's coding agent.

> 🚀 **One-line prompt to feed your agent:**
>
> ```
> Read installer/agent-assisted/WEEKLY-OPS.md and execute the weekly ops for my firm at <FIRM_FOLDER>. Read ~/.oot/firm-state.yaml for context.
> ```

---

## Agent: what to do, in order

### 1. Run daily-ops first

Execute [`DAILY-OPS.md`](DAILY-OPS.md) Steps 1-4 to sync state and verify health. Then continue below.

### 2. Friday — Business Review prep

R2 fires Friday 08:00 (firm timezone). By the time the founder opens their laptop Friday morning, the BR agenda should be at:

```bash
ls firm/business-reviews/$(date +%Y-%m-%d)-pre.md 2>/dev/null
```

If it exists: open it; summarise to the user; offer to walk them through it before the 14:00 BR meeting.

If it doesn't exist by 10:00 Friday:
- Check `~/oot-framework/logs/r2.log` if privacy track, or the Routine run log on https://claude.ai/code/routines if cloud track.
- Surface the failure to the user with the actual error.
- Offer to run R2 manually (manual fire from the Routines dashboard on cloud track, or on privacy track: `cd ~/<firm-slug> && opencode run --model lmstudio/qwen-3-14b-instruct "$(cat ~/oot-framework/routines/privacy/r2.prompt.md)"`).

After the BR meeting completes (typically signaled by the user editing the page or by the Decisions_Log on X3 getting populated), help the user rename `<date>-pre.md` → `<date>.md` and update the frontmatter `status: active`. This is a small signed commit.

### 3. Sunday — Brain health check

R5 fires Sunday 09:00. Check:

```bash
ls firm/brain-health/$(date +%G-W%V).md 2>/dev/null
```

If present: summarise the report to the user. Focus on:
- Broken wikilinks (and auto-fixes R5 already applied)
- Orphan pages (pages with no incoming links — possible deletion candidates)
- Semantic duplicates (pages that look similar — possible merge candidates)
- Stale pages (>90 days unmodified on pages tagged `active`)

If R5 didn't fire: same diagnostic as R2 above.

### 4. Mid-week — operational review (Tuesday or Wednesday)

Optional weekly task. Ask the founder if they want to run this; not every week needs it.

Pull a quick operational dashboard:

```bash
# Today's commits to X1
git log --since="7 days ago" --pretty=format:'%ai %an: %s' --no-merges -- firm/excel/partner-output-ledger.xlsx

# Routine failure log
ls firm/audit-logs/*.md | tail -7 | xargs grep -l 'FAILED\|ESCALATE\|ERROR' 2>/dev/null
```

If anything's flagged: walk the founder through.

### 5. Update firm-state file

```yaml
last_weekly_sync: <ISO8601>
weekly_observations: |
  - R2 BR agenda: <status>
  - R5 brain health: <status>
  - Anomalies: <list or none>
```

---

## What this playbook does NOT do

- Hold the BR meeting for the user. The agent can prep the agenda; humans still do the meeting.
- Auto-resolve broken wikilinks beyond what R5 already auto-fixed. Manual review for unsafe categories.
- Replace [`docs/walkthroughs/W4-running-the-friday-business-review.md`](../../docs/walkthroughs/W4-running-the-friday-business-review.md), which is the canonical 30-min BR structure.

---

## See also

- [`DAILY-OPS.md`](DAILY-OPS.md) — daily sync
- [`MONTHLY-OPS.md`](MONTHLY-OPS.md) — monthly variable pay flow
- [`routines/cloud/R2.md`](../../routines/cloud/R2.md) — R2 spec
- [`routines/cloud/R5.md`](../../routines/cloud/R5.md) — R5 spec
