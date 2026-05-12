# 07 — Troubleshooting

**Audience:** All. Anyone running into a sharp edge.

This is a **living document.** Add to it as your firm encounters new failure modes; submit additions via PR.

---

## Index by symptom

| Symptom | Section |
|---|---|
| Claude Desktop says "MCP server failed to start" for MyCuratorMCP | [§MCP-1](#mcp-1) |
| The Curator self-test fails on macOS Sonoma+ | [§Curator-1](#curator-1) |
| A Routine runs but produces no output | [§Routine-1](#routine-1) |
| A Routine produces an error message I don't understand | [§Routine-2](#routine-2) |
| Excel formulas show #REF! after I edit X1 | [§Excel-1](#excel-1) |
| A partner reports their variable pay calculation is wrong | [§Comp-1](#comp-1) |
| The PR auto-label `ai-replaces-human` isn't firing | [§Klarna-1](#klarna-1) |
| The Brain's wikilinks are breaking en masse | [§Brain-1](#brain-1) |
| LM Studio crashes when I run the daily Routine | [§Privacy-1](#privacy-1) |
| 4thtech dMail says "wallet not authorised" | [§Privacy-2](#privacy-2) |
| PollinationX storage NFT not recognised | [§Privacy-3](#privacy-3) |
| The Trezor doesn't connect to 4thtech | [§Privacy-4](#privacy-4) |
| I lost my Trezor seed — what happens to my 4thtech identity? | [§Privacy-5](#privacy-5) |
| Bitwarden CLI auth keeps timing out | [§Secrets-1](#secrets-1) |
| GitHub branch protection blocks R6 audit-log push | [§Audit-1](#audit-1) |

---

## MCP

### §MCP-1 — Claude Desktop says "MCP server failed to start" for MyCuratorMCP

**Probable causes:**
1. Claude Desktop wasn't fully restarted after editing config.
2. The Curator app isn't running.
3. The MCP config snippet has a typo.

**Fix:**
1. Quit Claude Desktop completely (Cmd+Q on macOS, not just close window).
2. Verify the Curator app is running.
3. Open `claude_desktop_config.json` (Settings → Developer → Edit Config). Confirm the `my-curator` block has correct `command` path and `args`.
4. Reopen Claude Desktop. Wait 5 seconds. Check the MCP servers panel.

**Escalation:** [github.com/talirezun/the-curator/issues](https://github.com/talirezun/the-curator/issues).

---

## Curator

### §Curator-1 — Self-test fails on macOS Sonoma+

**Probable cause:** known issue with Curator builds < v1.2 and macOS Sonoma+.

**Fix:** download the latest release from [github.com/talirezun/the-curator/releases/latest](https://github.com/talirezun/the-curator/releases/latest). The issue is fixed in v1.2+.

---

## Routines

### §Routine-1 — A Routine runs but produces no output

**Probable causes:**
1. The Routine's MCP host can't reach your Curator (cloud track: Curator must be on a network-reachable machine).
2. The connector permissions are insufficient.
3. The prompt's data sources are empty (e.g. R1 on a day with no commits).

**Fix:**
1. Check the Routine's run log in the Anthropic dashboard (cloud) or `~/oot-framework/logs/<r>.log` (privacy).
2. Verify Curator is reachable. If running on your laptop, the Routine on Anthropic infra cannot reach it; consider Anthropic's Curator-as-a-service (Q3 2026 launch) or a small always-on Pi.
3. Verify connector permissions match what the prompt requires.
4. For empty days: this is correct. R1 writes a "no outputs captured" Brain page.

### §Routine-2 — A Routine produces an error I don't understand

**Common errors:**

- `"openai.RateLimitError"` — quota exhausted or rate-limited. Check Anthropic billing or wait 60 seconds.
- `"connection refused: localhost:1234"` (privacy) — LM Studio isn't running in headless mode.
- `"git push rejected: signature required"` (R6) — branch protection requires signed commits; configure GPG/SSH signing.
- `"VLOOKUP error in cell K5"` — X1 formula failure; usually a corrupted value_envelope_table; restore from backup.

**Fix:** the routine's per-file file (`routines/cloud/<R>.md` or `routines/privacy/<R>.md`) has a "Failure handling" section describing the prompt's own escalation path.

---

## Excel

### §Excel-1 — Formulas show #REF! after I edit X1

**Probable cause:** you deleted a row that another row's formula referenced, OR you renamed a sheet.

**Fix:**
1. Undo immediately (Ctrl+Z / Cmd+Z) if you can.
2. If past undo: restore from the previous git commit. The Ledger's git history is your backup.
3. If formulas are persistently broken: re-generate the Excel file from `scripts/build_excel.py` (you'll lose live data — only do this on a fresh template).

**Prevention:** never delete rows from `Output_Log` once they've been included in a paid `Monthly_Variable`. Use the renegotiation flow per S3 §4.1.

---

## Compensation

### §Comp-1 — A partner reports their variable pay calculation is wrong

**Probable causes:**
1. Value tier mis-classification (most common).
2. `partner_multiplier` (X1.J) doesn't match X2's `output_multiplier`.
3. A retroactive `rework_within_30d` flip happened that the partner didn't expect.

**Fix:**
1. Open `templates/excel/partner-output-ledger.xlsx` Output_Log.
2. Filter to the disputed month + the partner.
3. Walk through each row with the partner. The discipline: facts (which output, what tier, what envelope) before judgement.
4. If genuine error: open a Tier-1 dispute (partner ticks the dispute box on their variable statement). Per `governance/DECISION-RIGHTS.md` Tier 1 flow.
5. If the dispute resolves: backfill X1 with corrections; regenerate the variable statement; partner re-acks.

**Anti-pattern:** retroactively recomputing closed-month variable. Don't. The framework's discipline: closed months stay closed; corrections apply forward.

---

## Klarna

### §Klarna-1 — The PR auto-label `ai-replaces-human` isn't firing

**Probable causes:**
1. The auto-labeller workflow (`.github/labeler.yml` or equivalent) isn't installed.
2. The PR's diff doesn't match the §4.8 signatures.
3. The labeller has a config error.

**Fix:**
1. Check `.github/labeler.yml` exists in the repo's default branch.
2. Open the PR's "Checks" tab; look for the labeller workflow run.
3. Review the PR's diff against S4 §4.8 signatures: code path removal, ledger formula change, autonomous Skill addition. The labeller is heuristic; it can miss.
4. If the PR should have been labelled but wasn't: apply the label manually. R7 will fire either way.
5. Update the labeller's config via PR to catch the missed pattern next time.

---

## Brain

### §Brain-1 — Wikilinks are breaking en masse

**Probable causes:**
1. A page was renamed (slug changed) and backlinks weren't updated.
2. A Curator ingest produced wikilinks to slugs that don't exist.
3. The Ledger's git history was force-pushed (this should be impossible if branch protection is configured).

**Fix:**
1. Run `mcp__my-curator__scan_wiki_health` immediately. It identifies every broken link.
2. For typo-correctable: use `fix_wiki_issue`.
3. For renamed slugs: per `templates/brain/FIRM-ONTOLOGY.md` discipline — mark old slug `status: superseded` with `superseded_by: <new-slug>`; never just delete.
4. For force-push damage: restore from a healthy fork or local clone. Configure branch protection (per S4 §4.0) to prevent recurrence.

---

## Privacy track

### §Privacy-1 — LM Studio crashes when I run the daily Routine

**Probable causes:**
1. RAM exhaustion (multiple models loaded).
2. macOS / Linux killed the process due to memory pressure.

**Fix:**
1. `~/.lmstudio/logs/` for the crash log.
2. Unload unused models in LM Studio's UI.
3. For Routines that need the larger model (R3 with Llama 3.3 70B), ensure ≥48GB free RAM at runtime.
4. Consider upgrading the always-on machine if you're running multiple models simultaneously.

### §Privacy-2 — 4thtech dMail says "wallet not authorised"

**Probable cause:** the wallet's permissions on the firm's dMail domain expired or weren't granted.

**Fix:** founder runs `4thtech grant-dmail --to <partner-wallet> --domain <firm-domain>` again. The grant has a TTL that may need renewal.

### §Privacy-3 — PollinationX storage NFT not recognised

**Probable cause:** the NFT isn't in the wallet that the PollinationX client is connecting from.

**Fix:**
1. Verify the NFT is held in the firm's treasury wallet (Trezor-backed).
2. The PollinationX client must be paired with that specific wallet.
3. Per-partner read access: `pollinationx grant-read --nft <id> --to <partner-wallet>`.

### §Privacy-4 — Trezor doesn't connect to 4thtech

**Probable cause:** Trezor Bridge isn't running, or the device is in bootloader mode.

**Fix:**
1. Verify Trezor Bridge: `ps aux | grep trezor` (macOS/Linux); should show running process.
2. If absent: install from [trezor.io/start](https://trezor.io/start).
3. Disconnect + reconnect the Trezor; tap to wake.

### §Privacy-5 — I lost my Trezor seed. What happens to my 4thtech identity?

**Honest answer:** your 4thtech identity is **gone**. The wallet's contents are unrecoverable. This is a feature of self-custody, not a bug.

**Recovery:**
1. Acquire a new Trezor.
2. Generate a new seed; new 4thtech wallet identity.
3. The firm updates routing: `4thtech invite-dchat` for the new wallet; `4thtech grant-dmail` for the new wallet's dMail.
4. The lost identity's history (sent/received dMail; dChat messages) is gone unless you exported it locally.

**Prevention:** seed on paper, fireproof safe, separate from device. Optionally: split-seed (Shamir backups) per Trezor docs.

---

## Secrets

### §Secrets-1 — Bitwarden CLI auth keeps timing out

**Probable cause:** the session token has a default 30-min TTL.

**Fix:** set `BW_SESSION` env var with the token from `bw unlock`. For the provisioning script, the script handles this; for ad-hoc use, run `export BW_SESSION="$(bw unlock --raw)"` before the next command.

---

## Audit trail

### §Audit-1 — GitHub branch protection blocks R6 audit-log push

**Probable cause:** the branch protection rule requires reviews for ALL commits, but R6's `oot-bot` user is committing directly.

**Fix (canonical setup):** the branch protection should be configured with an exception for the `oot-bot` user pushing to `firm/audit-logs/*` paths. If your protection doesn't allow this:
1. Add the exception via repo Settings → Branches → Edit rule.
2. Or: create a separate `audit/main` branch with R6 pushing there; main branch unaffected.

---

## When to escalate

- **Issues you can't diagnose:** open a GitHub issue on this repo with the run log + reproduction steps.
- **Curator-specific issues:** [github.com/talirezun/the-curator/issues](https://github.com/talirezun/the-curator/issues).
- **4thtech / PollinationX issues:** their respective wikis ([wiki.4thtech.io](https://wiki.4thtech.io/), [wiki.pollinationx.io](https://wiki.pollinationx.io/)).
- **Legal-touchpoint questions:** [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md). Counsel is mandatory.

---

> ⚖️ This document is part of the ØØT framework. As a living document, it grows with the partnership's experience. Submit additions via PR.
