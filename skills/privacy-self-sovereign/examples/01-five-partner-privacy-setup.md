# Example 1 — A 5-partner firm setting up the privacy track from scratch

End-to-end walkthrough of standing up a fully sovereign Gen 1 ØØT instance.

## The setup

- **Firm:** Adriatic Studios. 5 partners (3 full-time + 2 specialists). EU-only customers.
- **Track:** privacy (sovereignty mandate; clients are insurance + finance verticals).
- **Always-on machine choice:** Mac mini M4 Pro 32GB (€1,800).
- **Models:** Qwen 3 14B as default; Llama 3.3 70B for Klarna Test scoring (higher-stakes).

## Day 1 (Saturday) — Hardware + OS

**Morning:**
1. Mac mini arrives. Founder unboxes, sets up macOS Sonoma 15.4.
2. **FileVault enabled.** Login password generated via Bitwarden (32-char). Touch ID **disabled** for boot (OS-only post-boot for convenience).
3. iCloud sync of Documents/Desktop **disabled.**
4. UPS connected (CyberPower 1500VA, ~€140; covers ~30 min of outage at this load).
5. Local user account `oot` created (separate from founder's personal account).

**Afternoon:**
6. **5 Trezor Model One devices** ordered directly from `trezor.io` (one per partner, founder included). Will arrive in 3-5 days.
7. **Bitwarden organisation** set up (firm uses Bitwarden Family + Organisation tier; ~€60/year).
   - Collections: `founders`, `all-partners`, `specialists`, `shared-services`, plus per-partner.
8. **Yubikey 5C NFC** for founder's Bitwarden + GitHub admin (€60).

## Day 2 (Sunday) — Software stack

**Morning:**
1. **LM Studio** downloaded + installed on Mac mini. Models downloaded:
   - `qwen2.5-14b-instruct-q4_k_m.gguf` (~9 GB)
   - `meta-llama-3.3-70b-instruct-q4_k_m.gguf` (~40 GB)
   - `qwen2.5-9b-instruct-q4_k_m.gguf` (~5 GB) — fallback
2. **Headless mode** enabled. `llmster` CLI installed to `/usr/local/bin/llmster`.
3. **MCP host config** in LM Studio:
   ```json
   {
     "mcpServers": {
       "my-curator": { "command": "curator-mcp" },
       "excel-mcp": { "command": "excel-mcp-server", "env": { "EXCEL_MCP_BASE_PATH": "/Users/oot/oot-ledger/firm/excel/" }},
       "desktop-commander": { "command": "desktop-commander-mcp" },
       "github-mcp": { "command": "github-mcp", "env": { "GITHUB_TOKEN_FILE": "/Users/oot/.config/oot/github-token" }}
     }
   }
   ```
4. **Self-test** — open Claude Desktop on founder's laptop (paired to LM Studio over Tailscale), run prompt: *"List my-curator domains."* → returns `[firm]` (the Curator's pre-existing domain on the Mac mini).

**Afternoon:**
5. **The Curator desktop app** installed on Mac mini. Cloud-LLM ingest configured (Gemini Flash Lite — Gen 2 will replace with local LLM ingest).
6. **First Brain ingest:** the firm's existing Notion export (~200 pages). Curator processes overnight.

## Day 3-7 — Trezors arrive; partner provisioning begins

**Day 3 — founder's Trezor:**
1. Verify packaging integrity (tamper seal intact).
2. Initialise offline. 24-word seed phrase written on paper with pencil. Stored in fireproof home safe.
3. PIN set (8-digit). Passphrase enabled; passphrase on separate paper card.
4. `4thtech-wallet` installed; paired with Trezor.
5. Acquire firm's 4thtech dMail domain `adriatic.4thtech` (~€50/year). Configure dChat workspace `adriatic-coop`.
6. Send test dMail to self → received. Identity live.

**Day 4-7 — partner onboardings:**
Each partner physically present for ~2 hours:
1. They unbox their Trezor.
2. Initialise; seed on paper; their fireproof location.
3. PIN; passphrase optional (3 of 4 elect to use it).
4. 4thtech wallet paired to Trezor.
5. Founder sends them an `4thtech invite-dchat --workspace adriatic-coop --wallet <partner-wallet>`.
6. Founder provisions `4thtech grant-dmail --to <partner-wallet> --domain adriatic.4thtech`.
7. Partner receives invites in their 4thtech client.
8. Test dMail roundtrip: partner ↔ founder.

Cost recap: 5 Trezors (€80 each = €400), founder's Yubikey (€60), Mac mini (€1,800), UPS (€140), Bitwarden Org (~€60/year), 4thtech domain (~€50/year). One-time: **~€2,400**. Annual recurring: **~€110/year + Curator pay-as-you-go (~€5-10/month)**.

## Day 8 — PollinationX storage

1. Founder's wallet acquires a 200GB storage NFT on PollinationX (~€20/month equivalent).
2. PollinationX client installed on Mac mini + each partner's machine.
3. Per-partner read access granted: `pollinationx grant-read --nft <storage-nft> --to <partner-wallet>`.
4. Test: founder uploads a 50MB customer-call recording. Receives content address `Qm...x4`. Wikilink in Brain: `[[px:Qm...x4]]`. Partner fetches via wikilink resolution.

## Day 9-10 — Excel MCP + Desktop Commander + GitHub MCP

1. `pip install excel-mcp-server` on Mac mini.
2. `EXCEL_MCP_BASE_PATH` set; restart LM Studio MCP host.
3. Test from Claude Desktop: *"List worksheets in partner-output-ledger.xlsx"* → returns the canonical list.
4. **Desktop Commander** installed; allowed-paths configured per §4.8.
5. **GitHub MCP** installed; PAT generated for `oot-bot` user (the firm's bot account); stored in Bitwarden `shared-services`; written to `~/.config/oot/github-token` on Mac mini.
6. Test: *"Show me the latest commit on the firm Ledger"* → returns the latest signed commit.

## Day 11-12 — Routines (cron + launchd)

Founder + Tomislav (the most technical specialist) install the Day-1 Routines on the Mac mini:

**R1 — daily output capture (launchd):** `~/Library/LaunchAgents/oot.r1.plist` per §4.10 template. `launchctl load`. Verified with manual fire (`launchctl start oot.r1.daily-output-capture`).

**R2 — Friday BR prep (launchd):** trigger Friday 08:00.

**R5 — Sunday Brain health check (launchd):** Sunday 09:00.

**R6 — daily audit log (launchd) — signed commits:**
1. GPG key generated for `oot-bot` (4096-bit).
2. Public key uploaded to GitHub `oot-bot` user.
3. `gpg-agent` configured to cache passphrase for 24h on the Mac mini.
4. Branch protection on `main`: force-push disabled; deletion disabled; required signed commits enabled; required status check `oot/klarna-test`.
5. R6 plist runs daily 23:00; signs each audit-log commit via gpg-agent.

R3, R4, R7, R8 deferred until first partner onboarded + first Klarna trigger fires.

## Day 13 — Smoke tests

1. R1 fires at 18:00. Reads no commits (no firm work yet); writes empty daily log to `firm/output-logs/2026-05-13.md`. ✓
2. R5 dry-run: scans Brain (the 200-page imported wiki); reports 14 broken wikilinks (typo-correctable). Auto-fixes. ✓
3. R6 fires 23:00; appends "no agent activity" entry; signed commit lands on protected `main`. ✓

## Day 14 — Documentation

Founder writes `firm/privacy-track/setup-log.md` summarising the 13 days. Lists partner trezor addresses, model versions installed, Routine schedule, branch protection config, allowed PollinationX content addresses.

The firm is fully Gen 1 operational on the privacy track. No data leaves the partners' wallets or the always-on machine without explicit consent. Curator ingest is the one remaining cloud dependency (resolved when Gen 2 ships local-LLM ingest).

## What this example demonstrates

- **Total setup time:** ~14 days, ~30 hours of founder time + ~10 hours of partner time across the 5 partners.
- **Total cost:** ~€2,400 one-time + ~€110/year + Curator pay-as-you-go.
- **The discipline at every step:** verify packaging integrity, paper seeds, no digital storage of sensitive material, FDE, branch protection, signed commits, dry-run before cutover.
- **Honest deferrals:** R3, R4, R7, R8 not installed Day 1 — they wait until needed (first partner onboarded for R3; first Klarna trigger for R7).
- **Clean Brain audit trail** of the entire setup at `firm/privacy-track/setup-log.md`.
