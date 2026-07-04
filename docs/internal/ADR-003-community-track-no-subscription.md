# ADR-003 — The community track: operating ØØT without an Anthropic subscription

**Status:** Accepted 2026-07-04.
**Deciders:** Dr. Tali Režun (initiator) + framework maintainers.
**Supersedes:** nothing. **Related:** ADR-001 (Excel writeback), ADR-002 (Firm Brain).

---

## Context

Gen 1 ships two operating configurations:

1. **Cloud track** — daily driver + automation on Anthropic products. The automation layer (all 8 scheduled Routines) is **Claude Code Routines**, a Pro+-gated Anthropic product. Minimum real cost: ~€20-100/month per active seat.
2. **Privacy track** — sovereignty-first: always-on machine (~€1,800), per-partner Trezors, 4thtech, PollinationX. One-time cost ~€2,460.

That leaves a gap the audit of 2026-07-03 made explicit: **a founder who simply doesn't have a subscription budget** — not a sovereignty mandate — currently has no documented path. The FAQ's old answer ("Do I have to use Claude? No.") was true for Skill Packs and false for automation. Routing a budget-constrained founder into buying a Mac mini and hardware wallets is not an answer.

Meanwhile the pieces for a third configuration already exist:

- **OpenCode** ([opencode.ai](https://opencode.ai), repo `anomalyco/opencode`, formerly `sst/opencode`; npm package `opencode-ai`) — an open-source terminal coding agent with 75+ providers, **free built-in models**, local-model support (Ollama / LM Studio), native MCP support (`opencode.json` → `mcp`), a permission system (`"permission": {"*": "ask"}`) that satisfies the capability spec's R4 pause-and-confirm requirement, and a non-interactive `opencode run` mode.
- The Ledger is plain GitHub — vendor-neutral already.
- Curator ingest already supports Gemini Flash Lite pay-as-you-go (well under €10/month).
- The Routine prompt bodies are substrate-neutral markdown (the privacy track already proves prompts run outside Anthropic's cloud).
- The ops playbooks (DAILY/WEEKLY/MONTHLY-OPS) already prove the agent-runs-a-playbook pattern.
- R7's enforcement half (the Klarna gate) is a **GitHub Actions workflow** — free on any track.

## Decision

**ØØT documents a third operating configuration: the community track.** Free-to-start, no Anthropic subscription, no dedicated hardware, no sovereignty claims.

| Layer | Community track choice |
|---|---|
| Install harness + daily-ops agent | **OpenCode** (free built-in models, or the founder's own API keys, or local models) |
| Ledger + Firm Brain | GitHub (unchanged; ADR-001/ADR-002 apply verbatim) |
| Brain ingest | Curator + Gemini Flash Lite pay-as-you-go (~€5-10/month at heavy use) |
| Spreadsheet viewer | LibreOffice / any (unchanged) |
| Comms | Slack free tier or email (unchanged) |
| Klarna gate (R7 enforcement) | GitHub Actions — identical to the other tracks, free |
| Scheduled Routines | **Three-rung ladder, below** |

### The automation ladder (the substantive decision)

Cloud Routines' laptop-closed scheduling has no free equivalent; the community track is honest about that and offers three rungs, each an upgrade of the last:

1. **Rung 1 — manual playbook runs (the floor, zero setup).** The founder runs the DAILY/WEEKLY/MONTHLY-OPS playbooks by pasting the pre-prepared prompt into OpenCode. R1's dedupe + last-run catch-up semantics (fixed 2026-07-04) make irregular cadence safe: a missed day is captured on the next run, never double-paid.
2. **Rung 2 — laptop cron (recommended default once the firm is real).** OS scheduling (cron / launchd / Task Scheduler) invokes `opencode run` non-interactively with the routine prompt body. Runs only while the laptop is on — the same gap semantics as the privacy track's always-on caveat, minus the hardware. Missed fires are absorbed by the same catch-up semantics as Rung 1.
3. **Rung 3 — GitHub Actions scheduled workflows (laptop-closed, still no subscription).** A `schedule:`-triggered workflow runs the routine prompt against a model API using a repo-secret key (Gemini Flash / any OpenAI-compatible endpoint; typically cents per month at ØØT's ~2.3 runs/day). This restores laptop-closed automation. Trade-off: the firm's Ledger content transits the chosen model provider — same class of disclosure as the cloud track, so EU founders apply the same S7 assessment.

### Non-goals

- The community track makes **no sovereignty claims**. Founders with a privacy mandate use the privacy track.
- It is **not a separate prompt set**. Routines, Skill Packs, Excel templates, governance are byte-identical across tracks; only the harness and scheduler differ. Any divergence is a bug (same rule as cloud/privacy parity).
- It does not remove the recommendation that firms who can afford it use the cloud track — Claude Code Routines remain the best-supported automation substrate, and frontier-model quality matters for R3's high-stakes monthly calc (mitigated on the community track by the founder-approval step R3 already requires).

## Consequences

- `installer/agent-assisted/OPENCODE-SETUP.md` becomes the harness appendix (install, provider/permission config, my-curator MCP wiring, START-HERE variant).
- MODULES / quickstart decision blocks / FAQ / ECOSYSTEM gain the third-track row; the capability spec's OpenCode entry gets the resolved naming and the R4 permission mapping.
- The agent-compatibility log gains an OpenCode row: **end-to-end install test queued** (live-testing session with the maintainer's test instance; same queue as the privacy-track e2e).
- Rung-3 reference workflow ships as a template in v1.3 (`templates/ci/routine-runner.yml` candidate); until then Rung 3 is documented conceptually with the gate workflow as the pattern to copy.
- Gen-2's ØØT desktop app (T27) should treat the community track as a first-class citizen (its dashboard reads the Ledger, which is track-agnostic).

## Alternatives considered

- **"Just use the privacy track without the privacy parts"** — rejected: its docs entangle hardware, Trezor and 4thtech steps that a budget founder doesn't need; untangling in-place would damage the sovereignty narrative.
- **Hosted ØØT runner service** — rejected for Gen 1: introduces a vendor (us) and contradicts Thesis 5 (composable Lego, no vendor between you and the framework).
- **Ollama-only fully-local free stack** — folded in rather than rejected: OpenCode supports local models, so a founder with a strong machine gets this for free within the community track; it is not required.
