# Example 2 — A long-tail entitlement that compounds + a retroactive rework zero-out

A compound example covering two of S3's harder workflows: long-tail entitlement settlement across multiple quarters, and the retroactive `rework_within_30d` zero-out detection.

## Part A — Long-tail that compounds

### The output

Partner Davor lands a contract with a customer worth **€120,000 ARR over 3 years** in 2026-Q1. The Output Spec at `firm/partners/davor-krznar/output-specs/2026-02-12--acme-contract.md` includes a long-tail section:

```yaml
long_tail:
  outcome_metric: "Realised revenue from this contract per quarter"
  partner_share_pct: 8
  settlement_period: quarterly
  start_date: 2026-04-01
  end_date: 2029-03-31  # 3 years
```

At the next BR (2026-03-22), founder + Davor agree the terms. The pack appends a row to X2 Long_Tail_Schedule for `davor-krznar`:

| output_id | description | partner_share_pct | settlement_period | start_date | end_date | total_settled |
|---|---|---|---|---|---|---|
| OL-20260212-014 | Acme contract — 3yr ARR | 8 | quarterly | 2026-04-01 | 2029-03-31 | 0 |

Cross-link added to the Output Spec.

### Quarter-by-quarter settlements (R4)

**2026-Q2 settlement (R4 fires 2026-07-01):**

1. Read all Long_Tail_Schedule rows where `start_date ≤ 2026-06-30` AND (`end_date` empty OR > 2026-06-30). The Acme row qualifies.
2. Query: realised revenue from Acme during 2026-Q2 = €30,000 (one quarter of the €120k ARR).
3. Compute: payment = 30,000 × 0.08 = **€2,400**.
4. Update X2: `total_settled_to_date = 2,400`.
5. Generate Davor's Q2 statement at `firm/partners/davor-krznar/long-tail-statements/2026-Q2.md`.
6. Email/dMail; founder approves; payment processes.

**2026-Q3 (R4 fires 2026-10-01):**

Same flow. Realised revenue: €30,000 (still on plan). Payment: €2,400. `total_settled_to_date = 4,800`.

**2026-Q4 (R4 fires 2027-01-01):**

The customer reduced usage by ~30% in November (an internal restructuring). Realised revenue for Q4: €21,000.

The pack flags this as an **anomaly** because the realised outcome diverged from plan. The Brain anomaly page surfaces it for the next BR. The compute is unchanged: payment = 21,000 × 0.08 = **€1,680**. `total_settled_to_date = 6,480`.

Davor's Q4 statement explicitly notes the divergence in the `## Outcome attribution` section so he sees it before signing.

**2027-Q1 (R4 fires 2027-04-01):**

The customer's usage stabilises at the new lower level. Q1 revenue: €21,000. Payment: €1,680. Cumulative: **€8,160**.

### After 4 quarters

Davor has earned **€8,160** on long-tail from this single output. The arrangement continues for 8 more quarters (through 2029-Q1).

The Output Spec page in the Brain shows the cumulative settlement history — every settlement row is a wikilink to the relevant Long-tail statement page. Davor can see his 3-year compounding payout at a glance.

> **Honest framing:** if the contract terminates before 2029-03-31, the Long_Tail_Schedule's `end_date` updates to the actual termination date, and the row stops generating settlements. If usage spikes (the customer expands the contract), the realised outcome rises and so does the settlement. The long-tail mechanism pays the partner for the value the artefact actually generates over time, not for a fixed estimate at sign-time.

---

## Part B — Retroactive rework zero-out

### The setup

On 2026-04-08, partner Anya merges PR `gh:1452` — a refactor of the customer-onboarding flow. R1 captures it:

| log_id | date | partner | output_type | output_ref | value_tier | rework? | computed_variable |
|---|---|---|---|---|---|---|---|
| OL-20260408-002 | 2026-04-08 | anya-gorska | pr_merged | gh:1452 | M | No | €2,000 |

April variable statement closes on 2026-05-01 with this row contributing €2,000 to Anya's pool. She acknowledges; founder approves; payment processes on 2026-05-05.

### The rework detection

On 2026-04-30 (within the 30-day window), Anya merges `gh:1467` with this commit message:

> **fix: revert onboarding refactor — customer reports session loss**
>
> The 2026-04-08 refactor (gh:1452) introduced a regression where session tokens were not invalidated on logout. Reverting and reapplying with the fix.

R1 fires that evening (2026-04-30 18:00). The detection rule (per `routines/SPEC.md` R1) checks:

- **Same partner_id?** Yes (both Anya).
- **C_new timestamp within 30 days of C_old?** Yes (22 days later).
- **≥50% file overlap?** Yes (both touch `src/auth/onboarding.ts`, `src/auth/session.ts`).
- **Commit message regex match `\b(fix|revert|hotfix|redo|retry|reapply|backout|rollback)\b`?** Yes — both `fix:` and `revert`.

All four conditions hold. R1 **flips OL-20260408-002's `rework_within_30d` from No to Yes**. The X1 column-L formula re-evaluates: `value_envelope × multiplier × IF(I="Yes", 0, 1)` = 0. Anya's April variable retroactively drops by €2,000.

The daily summary at `firm/output-logs/2026-04-30.md` includes the `## Retroactive rework detections` block:

```markdown
## Retroactive rework detections

- OL-20260408-002 (originally captured 2026-04-08) — flipped to `rework_within_30d=Yes`. Trigger: commit gh:1467 (`fix: revert onboarding refactor — customer reports session loss`). Affected partner: [[partners/anya-gorska]].
```

### What happens to the already-paid April variable?

April was already paid on 2026-05-05. The framework's discipline: **closed-month variable does not retroactively recompute.** The April row stays paid.

But the ~~€2,000~~ doesn't disappear from accountability. It shows up as a **prior-month zero-out line item** in Anya's May variable statement, in the `## Retroactive zero-outs from prior months affecting this month's pool` section:

```markdown
## Retroactive zero-outs from prior months affecting this month's pool

- OL-20260408-002 (originally 2026-04-08, originally €2,000) → flipped to rework=Yes by R1 on 2026-04-30. Net effect on this month: €0 (the prior month's variable was already paid; the framework's locked-month discipline does not retroactively recover paid amounts. This entry is the audit record.)
```

This is honest: the partner sees that the rework happened; the retrospective is in the Brain audit trail; future variable calculations *are* affected (her R1 detection rate is one signal in §4.9 anomaly checks).

### What happens long-term?

If Anya's `rework_within_30d=Yes` rate exceeds 25% over a rolling 30-day window, §4.9 fires the rework-spike anomaly. The next BR surfaces it. The conversation at the BR is not punitive — it's diagnostic. The framework's authors find the most common cause is environment problems (test infra is unreliable, leading to merging-then-reverting); the rework-spike anomaly is the signal to fix the environment.

## What both parts of this example demonstrate

- Long-tail entitlement is a real Gen 1 capability — Excel-tracked, quarterly-settled, honest about outcome divergence.
- The rework-within-30d mechanism is the framework's correction discipline (not an `ai_authored_pct` discount).
- The audit trail is in the Brain at every step — Output Spec, daily logs, statements, anomalies, Long_Tail_Schedule updates.
- The framework is honest about edge cases (locked-month discipline, contract termination, outcome divergence).
