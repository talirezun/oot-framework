# 00 — Quickstart: Cloud Track

**Audience:** Founder. Cloud track. Non-technical to moderately-technical.
**Time:** Two weekends (~16 hours total). Most of it sequential, not parallelisable.
**You will end with:** a fully-operational ØØT instance with one partner onboarded.

> 📖 **Read first:** [`MANIFESTO.md`](../MANIFESTO.md) (15 min), [`SPEC.md`](../SPEC.md) (30 min), [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md) (10 min). The framework's discipline starts with reading.

---

## What this is + the first 5 minutes

ØØT runs on a stack of well-known UI tools: **Claude Desktop** (your daily driver), **Google Drive / Sheets** (or Microsoft Excel via the Claude extension), **Slack** (comms), **GitHub** (Brain sync + version control), the **Curator desktop app** (knowledge graph), and **Anthropic Remote Routines** (cloud automation that runs while your laptop is closed).

By the end of weekend one, you will have:
- Installed the stack.
- Created your firm's first Curator domain.
- Configured 4 Day-1 Routines (R1, R2, R5, R6).
- Set up Bitwarden + Trezor + Yubikey per the secrets policy.

By the end of weekend two, you will have:
- Onboarded your first partner end-to-end.
- Held the first Friday Business Review.
- Confirmed daily output capture is working.

If at any step a screenshot doesn't match what you see (Anthropic / Google / Slack UIs evolve), trust the UI's labels over the screenshot and let us know via PR.

---

## Before you start

Decide:

- **Cloud track or privacy track?** This guide is the **cloud** path. If you need sovereignty (4thtech + PollinationX + LM Studio), start with [`00-quickstart-privacy.md`](00-quickstart-privacy.md) instead.
- **Are you in the EU?** If yes, the EU AI Act (full obligations from 2 August 2026) and GDPR materially affect your build. [`governance/EU-AI-ACT.md`](../governance/EU-AI-ACT.md) and Skill Pack S7 are mandatory reading.
- **What jurisdiction will the entity operate in?** Worker classification, variable-pay legality, securities law (long-tail entitlements, Unit Fund), and crypto-payroll regulation all vary. [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md) lists the eleven legal touchpoints.

Open the ØØT-readiness diagnostic at `templates/excel/oot-readiness.xlsx`. Score yourself honestly. **Below 60% suggests adoption is premature** — address the lowest-scoring dimension first.

---

## Weekend One — Saturday

### Saturday morning (3-4 hours): accounts + credentials

1. **Bitwarden organisation account.** [bitwarden.com](https://bitwarden.com/). Create the org, add the canonical collections (`founders`, `all-partners`, `specialists`, `advisors`, `shared-services`). Per [`governance/SECRETS-POLICY.md`](../governance/SECRETS-POLICY.md).
2. **Trezor hardware wallet.** Order from [trezor.io](https://trezor.io/) (only direct from manufacturer). For now, just initialise it; you'll use it later (Gen 2 stablecoin payroll, or privacy-track migration if you switch tracks).
3. **Yubikey 5C NFC** (or two). For org-admin 2FA. Set it up for GitHub admin, Anthropic admin, Google admin, Bitwarden organisation owner.
4. **Anthropic account.** [claude.com](https://claude.com/). Pro or Max plan — Remote Routines require Pro+.
5. **GitHub organisation.** Apply Apache 2.0 default for code repos and CC BY-SA 4.0 for documentation repos.
6. **Google Workspace.** [workspace.google.com](https://workspace.google.com/). Configure 2FA with the Yubikey on the admin account.
7. **Slack workspace.** With the [Claude Slack integration](https://slack.com/apps/A0848GFRZ54-claude) enabled.

> 💡 **Tip:** Don't save any password to your browser's password manager during this setup. Use Bitwarden from the start. Browser autofill is the leak point that destroys the secrets policy six months later.

### Saturday afternoon (2-3 hours): install the stack

1. **Claude Desktop.** Download from [claude.com](https://claude.com/). Sign in. Connect Google Drive, Calendar, Gmail (the official Anthropic connectors).
2. **Claude Code.** [Install per Anthropic docs](https://docs.claude.com/en/docs/claude-code). Enable Max plan if you have it.
3. **The Curator desktop app.** Download from [github.com/talirezun/the-curator/releases/latest](https://github.com/talirezun/the-curator/releases/latest). Install. Run the onboarding wizard. Configure cloud-LLM ingest (Gemini Flash Lite recommended for cost; Anthropic Claude for quality on important docs). Pay-as-you-go pricing — heavy usage typically stays under €10/month.
4. **MyCuratorMCP.** Configure per the Curator's wizard — copy the snippet, paste into `claude_desktop_config.json`, restart Claude Desktop. Run the self-test.
5. **The My Curator skill.** From the Curator GitHub repo's `claude-skills/my-curator/SKILL.md` (or use ØØT's pre-imported version at `skills/my-curator/SKILL.md`). Add it to Claude Desktop as a Project Document.
6. **Obsidian** (optional but recommended). Point it at your Brain's markdown folder. This is your human-readable view.

> 💡 **Verification:** open Claude Desktop, ask: *"Use my-curator. List the firm domains."* You should see a green checkmark on the my-curator MCP and Claude should respond with the available domains.

---

## Weekend One — Sunday

### Sunday morning (2-3 hours): scaffold the Brain

1. **Create the Brain repository on GitHub.** Private or public per your preference. The Curator syncs to it.
2. **Create the first Curator domain.** Use the Curator app's UI; create a domain called `firm` for company-internal knowledge. Optionally add `customers`, `products`, `legal`, `research`. Per [`templates/brain/FIRM-ONTOLOGY.md`](../templates/brain/FIRM-ONTOLOGY.md).
3. **First ingest.** Pick five existing documents (a recent contract, a strategic memo, a product spec, a pitch deck, a meeting transcript). Ingest them via the Curator. Verify the resulting wiki pages, fix any wikilink issues with `fix_wiki_issue`.
4. **Run the health check.** `scan_wiki_health` from Claude Desktop. Address any structural issues.
5. **Bookmark the entry points.** The Curator's `get_index` for each domain. The MyCurator skill's quick-reference.

### Sunday afternoon (3-4 hours): configure the 4 Day-1 Routines

> 📖 **Reference:** [`routines/README.md`](../routines/README.md) for the recommended install order. Each Routine has a per-file install checklist at `routines/cloud/<R>.md`.

1. **Routine R5 — Brain Health Check.** Trigger: Sunday 09:00. No dependencies. [`routines/cloud/R5.md`](../routines/cloud/R5.md).
2. **Routine R6 — EU AI Act Audit Trail** (mandatory for EU founders; recommended for everyone). Trigger: daily 23:00. **Pre-requisite:** configure GitHub branch protection on `main` with force-push disabled, signed commits required, ≥1 reviewer for `firm/audit-logs/*`. [`routines/cloud/R6.md`](../routines/cloud/R6.md).
3. **Routine R1 — Daily Output Capture.** Trigger: daily 18:00. **Pre-requisite:** at least one partner onboarded (you, the founder). [`routines/cloud/R1.md`](../routines/cloud/R1.md).
4. **Routine R2 — Weekly BR Prep.** Trigger: Friday 08:00. **Pre-requisite:** R1 has 7+ days of data (so don't expect this one to produce useful output until next Friday). [`routines/cloud/R2.md`](../routines/cloud/R2.md).

> ⚠️ Hold off on R3 (Monthly Variable Calc), R4 (Long-Tail Settlement), R7 (Klarna Test trigger), and R8 (Treasury Runway) until Phase 8's CI workflows ship and you have the relevant Skill Packs + Excel files configured.

---

## Weekend Two — Saturday: onboard the first partner

> 📖 **Reference:** [`templates/partner-onboarding/checklist.md`](../templates/partner-onboarding/checklist.md) — the canonical 30-step checklist. Steps 1-15 happen in the 90-min onboarding session.

1. **Schedule a 90-minute onboarding session.** Both founder and partner present.
2. **Walk through `MANIFESTO.md` together.** 30 min. The partner internalises the five theses, especially Resistance and the Klarna Test.
3. **Reward Species Declaration.** Open `templates/excel/reward-species-declaration.xlsx`. The partner fills in their sheet. Both sign. Generate signed PDF; commit to Brain at `firm/partners/<id>/legal/reward-species-<DATE>.pdf`.
4. **Two Worlds of Code self-identification.** [`skills/code-qa/SKILL.md`](../skills/code-qa/SKILL.md) §4.9 has the 5-question assessment.
5. **Output Spec for the first piece of work.** Together, draft using [`templates/output-spec.md`](../templates/output-spec.md). Commit to `firm/partners/<id>/output-specs/<DATE>--<slug>.md`.
6. **Partner Charter signed.** Use [`templates/partner-charter.md`](../templates/partner-charter.md). Both parties sign.
7. **Tools provisioned.** Run [`templates/partner-onboarding/provisioning-script.sh <partner_id>`](../templates/partner-onboarding/provisioning-script.sh). The script handles Bitwarden, GitHub, Slack, Drive, Brain folder.

---

## Weekend Two — Sunday: first full operational week begins

1. **Daily ledger updates** start (Routine R1). Verify the partner's output appears in `templates/excel/partner-output-ledger.xlsx` Output_Log.
2. **Friday Business Review** (Routine R2 generates the agenda; meeting is 30 minutes; recorded as a markdown summary committed to the Brain). Use [`docs/walkthroughs/W4-running-the-friday-business-review.md`](walkthroughs/W4-running-the-friday-business-review.md) for the 30-minute structure.
3. **First Klarna Test** (when relevant — typically not week one). Walk through [`governance/KLARNA-TEST.md`](../governance/KLARNA-TEST.md) together so the team knows the process before they need it. The walkthrough is at [`docs/walkthroughs/W5-running-a-klarna-test.md`](walkthroughs/W5-running-a-klarna-test.md).

By end of weekend two, you have a running ØØT instance with one partner onboarded, daily output capture, weekly review cadence, and the Brain compounding.

---

## What success looks like

- The Brain has 10–30 ingested documents, no broken wikilinks, weekly health check running.
- One partner onboarded with signed Reward Species Declaration, signed Partner Charter, first Output Spec drafted.
- Daily output capture writing to `partner-output-ledger.xlsx`.
- Friday Business Review held; agenda was generated by R2; outcomes committed to the Brain.
- Bitwarden + Trezor + Yubikey configured per `governance/SECRETS-POLICY.md`.
- (EU founders) `eu-ai-act-mapping.xlsx` started; daily audit trail running.

You are now operating ØØT Generation 1.

---

## Common pitfalls (what to watch for)

1. **Setting up everything before onboarding anyone.** Don't. Onboard the first partner against a minimum-viable stack (Brain + Charter + Output Spec + ledger Routine). Add the rest of the Routines and Excel templates as the operational rhythm requires them. Founders who scaffold the entire stack before any partner work waste two weeks on tools nobody is using yet.
2. **Skipping the METR baseline.** Mandatory before any major Skill rollout (per Skill Pack S6). Without baseline metrics, you cannot detect the perception gap (the +20% self-reported / -19% measured swing METR found in 2025).
3. **Treating the Klarna Test as a checkbox.** It is not. The test is the framework's signature epistemic discipline. If you score 13 and rationalise to 14, you are doing it wrong. Either honestly score at or above the threshold (≥14/20) or don't proceed.
4. **Adopting Gen 2 features before Gen 1 is stable.** Stablecoin payroll, smart-contract long-tail, Unit Fund — wait. The YOLO model recommends 6–9 months of pilot before opening the Unit Fund.
5. **Storing API keys or secrets in `claude_desktop_config.json` committed to git.** Use environment-variable references (`"env": {"API_KEY": "${BITWARDEN_API_KEY}"}`) instead.

---

## When to escalate

- **Brain ingest failing** repeatedly: see [`docs/01-installing-the-curator.md`](01-installing-the-curator.md) troubleshooting section, or open an issue on the Curator's GitHub.
- **Routine not firing** at scheduled time: see [`docs/02-installing-routines.md`](02-installing-routines.md).
- **Klarna Test triggering on a PR you don't think it should**: see [`docs/05-using-the-klarna-test.md`](05-using-the-klarna-test.md) for the gaming-and-anti-gaming patterns.
- **Legal-touchpoint question**: see [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md). Counsel is mandatory before adoption in any jurisdiction.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**. Adapt to your jurisdiction with qualified counsel. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md) for the eleven legal touchpoints.
