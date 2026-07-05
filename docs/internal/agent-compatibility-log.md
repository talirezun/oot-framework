# Agent compatibility log

Community-reported compatibility for agents driving the ØØT install plans at [`installer/agent-assisted/`](../../installer/agent-assisted/). The framework is LLM-agnostic by design — this log tracks which agents have actually been driven to a successful end-to-end install in real-world use.

If you successfully run an install with an agent not listed in [`installer/agent-assisted/AGENT-CAPABILITY-SPEC.md`](../../installer/agent-assisted/AGENT-CAPABILITY-SPEC.md) "Known compatible agents", please open a PR adding a row here.

---

## Tested by the framework's authors

| Date | Agent | Version | LLM backend | Track | Result | Notes |
|---|---|---|---|---|---|---|
| 2026-05-10 | Claude Code | (current) | Claude Sonnet 4.6 | Cloud | ✓ End-to-end | Reference install. Authoritative for the cloud plan. |
| 2026-07-05 | OpenCode | 1.17.9 | opencode/deepseek-v4-flash-free (community) + lmstudio/qwen3.5 (privacy) | Community + Privacy | ✅ VALIDATED | Live e2e 2026-07-05: headless runs, scoped unattended permissions, my-curator MCP (stdio), 4 signed routine cycles + launchd scheduled fire on the test instance (commits e7b6158/4edfe57/314e56b/b527eb2/558e6ed). Findings F1-F11 applied to docs. Community track defined in [ADR-003](ADR-003-community-track-no-subscription.md); harness setup at [`installer/agent-assisted/OPENCODE-SETUP.md`](../../installer/agent-assisted/OPENCODE-SETUP.md). |

(Privacy-track and community-track end-to-end tests were completed 2026-07-05 on the maintainer's test instance — see the VALIDATED row above. The full Path-A install run-through with a non-technical founder remains a v1.x follow-up.)

---

## Community-reported

Open a PR to add a row.

| Date | Agent | Version | LLM backend | Track | Result | Notes |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

---

## How to add an entry

1. Run the install end-to-end (cloud or privacy).
2. Open a PR adding a row to the table above with:
   - **Date** — when you ran it.
   - **Agent + version** — exact version.
   - **LLM backend** — model + provider (or `local: <model>` for LM Studio).
   - **Track** — Cloud / Privacy.
   - **Result** — ✓ End-to-end / ⚠ Partial (note which steps fell back to manual) / ✗ Blocked (note where).
   - **Notes** — anything other founders should know: extra setup, model preferences, time-to-complete, gotchas.
3. The framework's authors review and merge.

---

## What "compatibility" means here

A successful end-to-end install means:

- All 12 steps of the agent-runnable plan completed (`step_*: done` in `~/.oot/install-state.yaml`).
- Install summary written at `~/.oot/install-summary.md`.
- Smoke test passed (R5 fired and produced a signed commit on `main`).
- No silent downgrades (every signed commit was actually signed; no fallbacks taken without the user's explicit approval).

Partial completions are still useful — they tell us where each agent's weak spots are.
