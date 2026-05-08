# Skill Pack S12 — Privacy / Self-Sovereign Stack: SPEC

**ID:** S12
**Name:** Privacy / Self-Sovereign Stack
**Tier:** 1
**Status:** Hardened in v1.0 (build now)
**Maintainer:** Dr. Tali Režun

## Purpose

Orchestrates the privacy track's tools — 4thtech (on-chain communication), PollinationX (decentralised storage), LM Studio (local LLM), Excel MCP (privacy-track spreadsheet automation), Desktop Commander (local filesystem), GitHub MCP (cross-machine sync), OS-native scheduling — into a coherent operating mode. Without this pack, founders adopting the privacy track have a list of tools and no clear "how to wire them together" guide.

## Scope

**Covers:**
- Architectural overview of the privacy track (cloud-track equivalents and what differs).
- LM Studio installation and local model selection (Qwen 3 ≥9B, Llama 3.x, DeepSeek-V3).
- 4thtech setup: dMail, dChat, file transfer, wallet identity on Trezor.
- PollinationX setup: NFT storage acquisition, encrypted bulk file storage, content-addressing in the Brain.
- Excel MCP (`haris-musa/excel-mcp-server`) installation and configuration in LM Studio.
- Desktop Commander MCP for local filesystem.
- GitHub MCP for cross-machine Brain sync.
- OS-native scheduling (cron / launchd / Task Scheduler) hitting headless LM Studio (`llmster`).
- The trade-off vs. cloud track (laptop must be on; addressed via always-on machine — Mac mini / NUC / Pi).
- Privacy-track secret management additions (4thtech keys on Trezor; never in Bitwarden).

**Does NOT cover:**
- The cloud-track equivalents (those live in their respective tool sections of QUICKSTART and the relevant Skill Packs).
- Crypto operations beyond identity and storage (that is S10 — Finance & Treasury, Gen 2+).
- The legal landscape of self-custodial communication (counsel territory).

## Allowed tools / dependencies

- LM Studio MCP host.
- 4thtech CLIs and SDKs.
- PollinationX client.
- Excel MCP server.
- Desktop Commander MCP.
- GitHub MCP.
- Trezor (hardware wallet — for 4thtech wallet identity per partner).

## Section structure

1. **Purpose**
2. **When to invoke** — when a partner is setting up the privacy track, when a partner is migrating to privacy track from cloud, when troubleshooting a privacy-track-specific issue.
3. **When NOT to invoke** — cloud-track operations.
4. **Operational instructions:**
   - 4.1 Privacy track architecture overview (the parity table from `SPEC.md`).
   - 4.2 Always-on machine setup (hardware sizing, OS, full-disk encryption).
   - 4.3 LM Studio installation; local model selection and download; MCP host configuration.
   - 4.4 Trezor setup for 4thtech wallet identity (per partner).
   - 4.5 4thtech installation: dMail, dChat, file transfer; first message test across two machines.
   - 4.6 PollinationX: NFT acquisition; encrypted storage; Brain wikilinks to PollinationX content addresses.
   - 4.7 Excel MCP installation and configuration; integration with LM Studio.
   - 4.8 Desktop Commander setup; folder permissioning.
   - 4.9 GitHub MCP setup; cross-machine Brain sync.
   - 4.10 OS-native scheduling: cron jobs / launchd plists / Task Scheduler tasks; headless LM Studio (`llmster`) integration; equivalents of cloud Routines R1, R2, R5, R6.
   - 4.11 Migration workflow (cloud track → privacy track).
5. **Brain interaction protocol** — writes setup logs and configuration documentation to `firm/privacy-track/`.
6. **Excel interaction protocol** — provides the privacy-track equivalent of cloud Excel automation; reads/writes all 9 templates via Excel MCP.
7. **Routine integration** — provides the privacy-track equivalents of all 8 cloud Routines. The execution substrate differs (cron vs. Anthropic infrastructure); the prompts are identical.
8. **Don'ts**
9. **Quick reference**
10. **References**

## Don'ts

1. Don't store 4thtech wallet seed phrases in Bitwarden, or any digital store. Trezor only.
2. Don't run the privacy track without an always-on machine. Routines that miss because the laptop slept = data loss.
3. Don't mix cloud and privacy track for the same firm without explicit migration plan.
4. Don't skip full-disk encryption on the always-on machine. The privacy thesis collapses without it.
5. Don't trust local LLM outputs at the same threshold as Claude Opus — quality varies; the Klarna Test still applies.

## Worked examples concept

**Example 1:** A founder is setting up a 5-partner firm in privacy track. Walk through: provision the always-on Mac mini; install LM Studio with Qwen 3 14B; provision 5 Trezors (one per partner); set up 4thtech for each partner; install PollinationX; configure Excel MCP; install Desktop Commander; GitHub MCP; cron jobs for R1, R2, R5, R6. End-state: complete privacy-track ØØT operation with no cloud dependency.

**Example 2:** An existing cloud-track firm decides to migrate to privacy track for sovereignty reasons. Walk through: Brain export from Curator; re-ingest on local LLM; comms migration (Slack → 4thtech dChat); storage migration (Drive → PollinationX); Routine substrate switch (Anthropic → cron). 4-week migration plan.

## References

1. 4thtech project: `https://github.com/4thtech` and `https://wiki.4thtech.io/quickstart/index`.
2. PollinationX project: `https://wiki.pollinationx.io/introduction/start-here`.
3. The Curator project (cloud-LLM ingest currently; local-LLM ingest = Gen 2 roadmap): `https://github.com/talirezun/the-curator`.
4. LM Studio MCP support documentation.
5. `haris-musa/excel-mcp-server` (MIT licensed).
6. ØØT `MANIFESTO.md`, Thesis 5 — Composable Lego.
7. ØØT `governance/SECRETS-POLICY.md`.

## Acceptance criteria

Standard. Plus: cross-machine Brain sync example; full migration example; the privacy-track Routine equivalents are explicit (cron expressions or launchd plists shown).