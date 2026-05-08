# ØØT Quickstart

A weekend setup path for both the Cloud track and the Privacy track. Follow one or the other; do not mix tracks until you understand both.

This guide assumes a single founder doing initial setup, with one to four other partners coming in shortly afterward. Adapt as needed.

**Time budget.** Weekend One: install the stack, set up the Brain, configure scheduled jobs. Weekend Two: onboard one partner end-to-end, run a full week of operations, hold the first Friday Business Review.

---

## Before you start (both tracks)

Read in order:

1. `MANIFESTO.md` — understand the five theses.
2. `SPEC.md` — understand the eight-layer architecture.
3. `GENERATIONS.md` — understand what's deferred.
4. `governance/KLARNA-TEST.md` — understand the discipline.
5. This file.

Decide:

- **Cloud track or Privacy track?** Cloud is faster, easier, has Anthropic Remote Routines (laptop closed). Privacy is sovereign, requires an always-on machine, uses 4thtech + PollinationX + LM Studio + local cron. Most founders should start cloud unless they have a clear sovereignty mandate.
- **Are you in the EU?** If yes, the EU AI Act (full obligations from 2 August 2026) and GDPR materially affect your build. The Governance & Compliance Skill Pack and `governance/EU-AI-ACT.md` are mandatory reading, not optional.
- **What jurisdiction will the entity operate in?** Worker classification, variable-pay legality, securities law, and crypto-payroll regulation all vary. `docs/06-when-to-call-a-lawyer.md` lists the eleven touchpoints requiring local counsel. Engage counsel before you ship the first Partner Charter.

Open the ØØT-readiness assessment (`templates/excel/oot-readiness.xlsx`). It is a 20-question diagnostic across People, Tech, Culture, Risk. Score yourself honestly. A score below 60% suggests Gen 1 adoption is premature; address gaps first.

---

## Cloud track — weekend one

### Saturday morning: accounts and credentials

1. **Create a Bitwarden account** (or open 1Password if you prefer commercial). This is where all software credentials will live. Do not use a browser password manager; the secrets policy requires a sharable vault.
2. **Acquire a Trezor hardware wallet.** Required for crypto signing in the privacy-comms layer (4thtech wallet identity) and for Gen 2 readiness (stablecoin payroll wallet). Initialise it offline; record the seed phrase per Trezor's instructions; store the seed in a fire-safe location separate from the device itself.
3. **Acquire a Yubikey** (or two). Used for org-level admin accounts. Set it up for GitHub, Anthropic, Google admin.
4. **Anthropic account.** Pro or Max plan. Needed for Claude Desktop, Claude Code, and Remote Routines. Note: Remote Routines require Pro or higher.
5. **GitHub organisation.** Create one for your firm. Apply Apache 2.0 default for code repos and CC BY-SA 4.0 for documentation repos.
6. **Google Workspace.** Drive, Sheets, Docs, Calendar. Needed for the Claude connector. Configure 2FA with the Yubikey on the admin account.
7. **Slack workspace.** With the Claude integration enabled.

Store all credentials in Bitwarden. Configure shared vaults per partner role: founder (full access), partner (their working credentials), advisor (narrow scope).

### Saturday afternoon: install the stack

1. **Claude Desktop.** Download from claude.ai. Sign in. Connect Google Drive, Calendar, Gmail (the official connectors).
2. **Claude Code.** Install per Anthropic's instructions. Enable Max plan if you have it.
3. **The Curator desktop app.** Download from `talirezun/the-curator`. Install. Run the onboarding wizard. Configure cloud-LLM ingest (Gemini Flash Lite recommended for cost; Anthropic Claude for quality on important docs). Pay-as-you-go pricing — heavy usage typically stays under €10/month.
4. **MyCuratorMCP.** Configure per the Curator's wizard — copy the snippet, paste into `claude_desktop_config.json`, restart Claude Desktop. Run the self-test.
5. **The My Curator skill.** Download `claude-skills/my-curator/SKILL.md` from the Curator GitHub repo. Add it to Claude Desktop as a Project Document.
6. **Obsidian** (optional but recommended). Point it at your Brain's markdown folder. This is the human-readable view of the Brain.

### Sunday morning: scaffold the Brain

1. **Create the Brain repository on GitHub.** Private or public per your preference. The Curator syncs to it.
2. **Create the first domain.** Use the Curator's `list_domains` tool first; create a domain called `firm` for company-internal knowledge. Optionally also `customers`, `products`, `legal`, `research`.
3. **First ingest.** Pick five existing documents (a recent contract, a strategic memo, a product spec, a pitch deck, a meeting transcript). Ingest them via the Curator. Verify the resulting wiki pages, fix any wikilink issues with `fix_wiki_issue`.
4. **Run the health check.** `scan_wiki_health`. Address any structural issues.
5. **Bookmark the entry points.** The Curator's `get_index` for each domain. The MyCurator skill's quick-reference.

### Sunday afternoon: configure Routines

1. **Routine R1 — Daily Output Capture.** Trigger: daily 18:00 local. Reads GitHub commits, Slack threads (specific channels), Drive activity since 18:00 yesterday. Writes rows to `partner-output-ledger.xlsx`. Use the prompt in `routines/SPEC.md`.
2. **Routine R2 — Weekly BR Prep.** Trigger: Friday 08:00. Builds agenda from ledger; populates `business-review.xlsx`.
3. **Routine R5 — Brain Health Check.** Trigger: Sunday 09:00. Runs Curator `scan_wiki_health`; posts to Slack `#brain-health`.
4. **Routine R6 — EU AI Act Audit Trail** (EU founders only). Trigger: daily 23:00. Appends to audit log.

Hold off on R3 (Monthly Variable Calc), R4 (Long-Tail Settlement), R7 (Klarna Test trigger), and R8 (Treasury Runway) until you have the relevant Skill Packs and Excel files configured.

---

## Cloud track — weekend two

### Saturday: onboard the first partner

1. **Schedule a 90-minute onboarding session.** Both founder and partner present.
2. **Walk through `MANIFESTO.md` together.** 30 minutes. The partner needs to internalise the five theses, especially the Resistance thesis and the Klarna Test.
3. **Reward Species Declaration.** Open `reward-species-declaration.xlsx`. The partner fills it in: full-time partner / project specialist / advisor; eat-what-you-kill / lockstep / hybrid with weights; base salary level; cohort designation; preferences for Gen 2 (stablecoin upgrade, Unit Fund interest). Both parties sign. Commit to the partner's own folder in the firm Brain.
4. **Two Worlds of Code self-identification.** The partner reads the section in the Onboarding Skill, declares which world they identify with, and the cohort is recorded.
5. **Output Spec for the first piece of work.** Together, draft the spec. Commit to the Brain.
6. **Partner Charter signed.** Markdown template + signed PDF. Stored in the partner's Brain folder.
7. **Tools provisioned.** Bitwarden vault for the partner; Slack invite; GitHub access (read-only initially); Claude Desktop seat; Curator client install; Obsidian setup pointing at their assigned Brain domain.

### Sunday: first full operational week begins

1. **Daily ledger updates** start (Routine R1). Verify the partner's output appears.
2. **Friday Business Review** (Routine R2 generates the agenda; meeting is 30 minutes; recorded as a markdown summary committed to the Brain).
3. **First Klarna Test** (when relevant — typically not week one). Walk through `governance/KLARNA-TEST.md` together so the team knows the process before they need it.

By end of weekend two, you have a running ØØT instance with one partner onboarded, daily output capture, weekly review cadence, and the Brain compounding.

---

## Privacy track — weekend one

The privacy track is operationally complete in Gen 1 but takes longer to set up than the cloud track. The trade-off is sovereignty: no data leaves your machines or your wallets except by your explicit choice.

### Saturday morning: hardware

1. **An always-on machine.** Mac mini, NUC, or Raspberry Pi 5 with at least 16GB RAM (32GB recommended for larger local models). This is what runs the local LLM and the cron equivalents of cloud Routines.
2. **A Trezor hardware wallet.** Mandatory for the privacy track — wallet identity is how 4thtech authenticates you. Set up per Trezor's instructions.
3. **Bitwarden account, Yubikey** as in cloud track.

### Saturday afternoon: install the stack

1. **LM Studio** (or Ollama, or Open WebUI). Install on the always-on machine. Download a capable local model: Qwen 3 (≥9B), Llama 3.x, or DeepSeek-V3. The Curator confirms Qwen 3 9B running on 12GB RAM is operationally usable.
2. **MCP support in LM Studio.** Configure the MCP host (LM Studio 0.3.17+ supports MCP servers natively). Add MyCuratorMCP and the Excel MCP (`haris-musa/excel-mcp-server`).
3. **Desktop Commander MCP.** Install. Point it at the relevant local folders.
4. **The Curator desktop app.** Install. Cloud-LLM ingest is currently the only option (Gemini Flash Lite or Anthropic). Local-LLM ingest lands in Gen 2.
5. **GitHub MCP.** Install. Configure with a personal access token stored in Bitwarden.
6. **4thtech.** Install dMail and dChat. Authenticate with your Trezor-controlled wallet. Test by sending a message to yourself across two devices.
7. **PollinationX.** Acquire decentralised storage capacity (NFT-based). Install the client. Configure encrypted storage of the Brain's larger files (videos, recordings, large PDFs).

### Sunday morning: scaffold the Brain

Same as cloud track, except:

- The Brain folder lives on the always-on machine (or a partner's machine, synced via GitHub MCP).
- Bulk files (recordings, videos, large attachments) live on PollinationX, not in the Brain repo. Wikilinks in the Brain reference the PollinationX content addresses.
- Comms in the Brain (decisions referenced from chat threads) reference 4thtech dChat addresses, not Slack URLs.

### Sunday afternoon: configure cron equivalents

The privacy track runs the same eight Routines as the cloud track but on local cron / launchd / Task Scheduler hitting headless LM Studio.

1. **Headless LM Studio (`llmster`).** Install on the always-on machine. Test the REST API.
2. **Local cron job for R1 (Daily Output Capture).** Edit your crontab: `0 18 * * * /usr/local/bin/llmster --skill compensation-attribution --prompt "..."`. Full prompt template in `routines/SPEC.md`.
3. **Repeat for R2, R5, R6.** R3, R4, R7, R8 wait until the Skill Packs and Excel are in place.

The trade-off vs. cloud track: the always-on machine has to be on. If it sleeps or shuts down, jobs miss. Use a UPS for critical machines.

---

## Privacy track — weekend two

Same as cloud track. The onboarding flow is identical; only the tools differ.

Differences:

- Comms training: the partner needs to learn dMail and dChat, not Gmail and Slack.
- Wallet setup: the partner gets their own Trezor (firm should provide as a partner-onboarding cost) and creates their own 4thtech wallet identity.
- Storage training: PollinationX for bulk; Brain repo (synced via GitHub MCP) for everything else.

---

## What success looks like at the end of weekend two

- The Brain has 10–30 ingested documents, no broken wikilinks, weekly health check running.
- One partner onboarded with signed Reward Species Declaration, signed Partner Charter, first Output Spec drafted.
- Daily output capture writing to `partner-output-ledger.xlsx`.
- Friday Business Review held; agenda was generated by R2; outcomes committed to the Brain.
- Bitwarden + Trezor + Yubikey configured per `governance/SECRETS-POLICY.md`.
- (EU founders) `eu-ai-act-mapping.xlsx` started; daily audit trail running.

You are now operating ØØT Generation 1.

---

## Common pitfalls

**Setting up everything before onboarding anyone.** Don't. Onboard the first partner against a minimum-viable stack (Brain + Charter + Output Spec + ledger Routine). Add the rest of the Routines and Excel templates as the operational rhythm requires them. Founders who scaffold the entire stack before any partner work waste two weeks on tools nobody is using yet.

**Skipping the METR baseline.** Mandatory before any major Skill rollout. Without baseline metrics, you cannot detect the perception gap. The Skill Pack will tell you to do it; do it.

**Treating the Klarna Test as a checkbox.** It is not. The test is the framework's signature epistemic discipline. If you score 6.5 and rationalise to 7, you are doing it wrong. Either honestly score above the threshold or don't proceed.

**Mixing cloud and privacy tracks.** Pick one for v1.0. You can transition later, but mixing produces tooling chaos and partner confusion.

**Adopting Gen 2 features before Gen 1 is stable.** Stablecoin payroll, smart-contract long-tail, Unit Fund — wait. The YOLO model recommends 6–9 months of pilot before opening the Unit Fund. Trust the timing; the framework's authors learned it the hard way.