# Documentation — SPEC

Specifications for the user-guide layer Claude Code generates in Phase 7 of `BUILD-INSTRUCTIONS.md`. Two tiers, **18 documents total**:

- **Tier 1 — Concept + Setup guides (12 docs in `docs/`):** the original twelve plain-language guides. Each doc is for a specific audience, with a specific purpose, with copy-pasteable commands and screenshot placeholders where applicable.
- **Tier 2 — UI walkthroughs (6 docs in `docs/walkthroughs/`):** the day-by-day operational guides for the non-technical partner who is using the framework via Claude Desktop, Excel/Sheets, the Curator desktop app, and the Routines dashboard. Each walkthrough is screenshot-rich, sequential, and assumes nothing about file paths or shell commands.

The foundation kit deliberately does not write these docs itself; Claude Code generates them from this SPEC plus the rest of the foundation kit, with full repo context (it has just generated the Skills, Excel templates, and Routines, so it can reference them concretely).

---

## Documentation philosophy — write for the non-technical partner first

ØØT runs on UI-based tools that the user actually clicks: Claude Desktop, Microsoft Excel or Google Sheets, the Curator desktop app, the Anthropic Remote Routines dashboard, Slack. The framework's most important user is **the founder or partner who can edit a spreadsheet and follow a screenshot, but does not write code, does not use a terminal, and does not want to**.

Every Tier-1 doc that involves a UI tool follows the **three-layer pattern**:

1. **What this is + the first 5 minutes** (≤300 words). What the tool is for, what it does for the user, what success looks like at the end of the doc. Written for someone who has never opened the application.
2. **Step-by-step walkthrough** (≤2,000 words, with screenshots). Click-by-click, screenshot-anchored, no implicit knowledge. Every numbered step says exactly which button to click, what to type, and what to look for as confirmation.
3. **Common pitfalls + when to escalate** (≤500 words). The 3–5 things that go wrong most often, with screenshot examples of the wrong-state UI and the correction.

**Tier-2 walkthroughs** are pure layer-2 — they assume the user has already read the concept doc and just need to *do the thing*. Each Tier-2 walkthrough is one specific operational task, screenshot-rich, end-to-end.

**Audience tone (Tier 1 and Tier 2):**
- Plain language. No jargon without definition. The Glossary is a living reference; every first use of a glossary term wikilinks to it.
- The reader has read MANIFESTO.md and at least one of QUICKSTART.md, but no other technical material.
- "Open Excel and click the cell at row 3, column F" is *better* than "set `A3` to a literal `=SUM(...)` formula" when the audience is non-technical.
- Where a step diverges between Microsoft Excel and Google Sheets, both are shown.
- Where a step diverges between cloud track and privacy track, both are shown.
- Shell commands appear *only* in Tier-1 docs that explicitly target a technical audience (the Curator install for the founder, the Phase 8 CI doc for an engineer). Even there, the doc explains what the command will do in plain terms before showing it.

**Format conventions:**
- Markdown. H1 title. H2 sections. Numbered steps within sections.
- Screenshots placeholders as `![Description](images/<doc-id>-<step-number>.png)` with descriptive alt-text. Phase 7 generates the placeholders; the screenshots are captured by the framework's authors and added in a follow-up PR (one PR per doc to keep image binaries reviewable).
- Every screenshot has a caption underneath in italics describing what to look for ("*Look for the green checkmark next to 'Connected'. If you see a red X, see Common pitfalls below.*").
- "Tip" callouts use `> 💡 **Tip:** ...`. "Warning" callouts use `> ⚠️ **Warning:** ...`.
- Cross-references use relative paths (e.g., `../governance/KLARNA-TEST.md`).

**Length envelope:**
- Tier-1 quickstart docs: ~5,000 words (full weekend setup).
- Tier-1 concept docs: 2,000–3,500 words.
- Tier-1 troubleshooting / FAQ: open-ended.
- Tier-2 walkthroughs: 1,500–3,000 words each, screenshot-dense.

**Commands.** All shell commands are copy-pasteable. macOS / Linux primary; Windows variants where relevant. Privacy-track docs include cron / launchd / Task Scheduler examples. Cloud-track docs minimise shell usage outside the founder's initial install.

**The legal disclaimer block.** Every doc that touches legal or financial topics ends with a standard disclaimer block: *"This document is part of the ØØT framework and is not legal or financial advice. Adapt to your jurisdiction with qualified counsel. See `docs/06-when-to-call-a-lawyer.md` for the eleven legal touchpoints."*

---

## Tier-1 — the 12 plain-language guides

---

## The 12 documents

### `docs/00-quickstart-cloud.md`

**Audience:** Non-technical founder. Cloud track.

**Purpose:** Walk through the weekend setup path from the cloud track in `QUICKSTART.md`, with screenshots, copy-pasteable commands, and explicit "what success looks like" checkpoints at each stage.

**Required sections:**

1. **Before you start.** Decisions to make. Materials to acquire. Reading order.
2. **Saturday morning — accounts and credentials.** Bitwarden setup. Trezor unboxing and initialisation. Yubikey setup. Anthropic, GitHub, Google Workspace, Slack accounts.
3. **Saturday afternoon — install the stack.** Claude Desktop, Claude Code, the Curator, Obsidian.
4. **Sunday morning — scaffold the Brain.** First Curator domains. First ingest. Health check.
5. **Sunday afternoon — configure first Routines.** R1, R2, R5, R6 setup. (R3, R4, R7, R8 deferred to weekend two.)
6. **Weekend two preview.** What you'll do.
7. **Common pitfalls.** Same as in `QUICKSTART.md` plus cloud-track-specific gotchas.
8. **What success looks like.** End-of-weekend-one checklist.

**References:** `QUICKSTART.md` (canonical source for the path), Skill Pack S1 (My Curator), `governance/SECRETS-POLICY.md`.

---

### `docs/00-quickstart-privacy.md`

**Audience:** Sovereignty-focused founder. Privacy track.

**Purpose:** Same as cloud-quickstart, for the privacy track.

**Required sections:** Mirror cloud, but substitute:

- **Hardware.** Always-on machine selection (Mac mini / NUC / Pi 5). Disk encryption setup.
- **Models.** LM Studio install. Qwen 3 14B download. MCP host configuration.
- **Wallets.** Trezor setup for 4thtech wallet identity (per partner — emphasise this is per-person, not per-firm).
- **Comms migration.** dMail, dChat instead of email, Slack.
- **Storage.** PollinationX NFT acquisition; bulk storage; encrypted Brain attachments.
- **Scheduling.** cron / launchd / Task Scheduler equivalents of cloud Routines, with exact crontab lines.

**References:** `QUICKSTART.md`, Skill Pack S12 (Privacy / Self-Sovereign Stack), `governance/SECRETS-POLICY.md`.

---

### `docs/01-installing-the-curator.md`

**Audience:** All. Step-by-step Curator install.

**Purpose:** Detailed walkthrough of the Curator desktop app install, MyCuratorMCP configuration, the My Curator Skill installation, and first-domain setup. Both tracks use the same Curator (cloud-LLM ingest in v1.0; local-LLM ingest = Gen 2).

**Required sections:**

1. Why the Brain matters — link to `MANIFESTO.md` Thesis 4.
2. Pre-requisites.
3. Install the Curator desktop app.
4. Configure cloud-LLM ingest (Gemini Flash Lite vs. Anthropic; cost estimates).
5. Install MyCuratorMCP into Claude Desktop.
6. Install the My Curator Skill.
7. Run the self-test.
8. Create your first domain.
9. First ingest — five sample documents.
10. First health check.
11. What's next.

**References:** Skill Pack S1, `https://github.com/talirezun/the-curator`.

---

### `docs/02-installing-routines.md`

**Audience:** Cloud-track founder.

**Purpose:** Detailed walkthrough of installing each of the 8 cloud Routines via Anthropic's Remote Routines feature.

**Required sections:**

For each of R1–R8 (with R8 marked optional):

- What this Routine does (one paragraph).
- Pre-requisites (other Routines, Skill Packs, or Excel files this Routine depends on).
- Step-by-step setup (where in the Anthropic dashboard, what trigger to configure, what prompt file to upload, what Skills to attach).
- Verifying the Routine works (manual test trigger; what success output looks like).
- Common errors (rate limits, permission errors, missing connectors).

Recommended install order: R5 first (no dependencies), then R6, R1, R2, R3, R7, R4, R8.

**References:** `routines/SPEC.md`, the 8 generated Routine files in `routines/cloud/`.

---

### `docs/02-installing-routines-privacy.md`

**Audience:** Privacy-track founder.

**Purpose:** Privacy-track equivalents — cron / launchd / Task Scheduler invocations hitting headless LM Studio (`llmster`).

**Required sections:** Mirror cloud with platform-specific instructions:

- **macOS:** launchd plist examples; install via `launchctl load`.
- **Linux:** crontab examples; install via `crontab -e`.
- **Windows:** Task Scheduler XML; install via `schtasks` or GUI.

For each Routine, the exact line of cron/launchd configuration, the prompt file path, and the verification procedure.

**References:** `routines/SPEC.md`, the 8 generated files in `routines/privacy/`.

---

### `docs/03-onboarding-a-partner.md`

**Audience:** Founder.

**Purpose:** End-to-end walkthrough of onboarding a new partner using the templates in `templates/partner-onboarding/`.

**Required sections:**

1. Pre-onboarding decisions.
2. The 90-minute onboarding session — script.
3. Walking through the Manifesto together.
4. Filling in the Reward Species Declaration.
5. Two Worlds of Code self-identification.
6. Drafting the first Output Spec.
7. Signing the Partner Charter.
8. Provisioning tools — the checklist + the script.
9. Day-1 Brain orientation.
10. Week-1 expectations.
11. The 30-day check-in.

**References:** `templates/partner-onboarding/`, `MANIFESTO.md`, `templates/partner-charter.md`.

---

### `docs/04-running-the-business-review.md`

**Audience:** Founder + partners.

**Purpose:** How to run a Friday Business Review meeting that actually works.

**Required sections:**

1. The principle — replaces all status meetings.
2. The 30-minute structure: outputs (10 min) → blockers (5 min) → decisions (10 min) → Klarna status (3 min) → KPI snapshot (2 min).
3. Roles: facilitator, scribe, decision-recorder.
4. The pre-meeting (R2 generates agenda; participants pre-read).
5. The meeting itself — common patterns and anti-patterns.
6. Post-meeting — committing the summary to the Brain.
7. When the BR runs long — the agenda is wrong, here's why.
8. Quarterly rhythm — where the BR fits.

**References:** Skill Pack S5, `routines/cloud/R2.md`.

---

### `docs/05-using-the-klarna-test.md`

**Audience:** Decision-makers (founder, partners with merge authority).

**Purpose:** Concrete walkthrough of running the Klarna Test on a real decision.

**Required sections:**

1. The Klarna case — short version (1 paragraph).
2. When the test triggers — automatically (R7) and manually.
3. Reading the rubric — each of the 10 questions, with examples of 0/1/2 scores.
4. The non-beneficiary reviewer — how to choose, why it matters.
5. Filling in `klarna-test.xlsx` step by step.
6. The proceed / hold decision.
7. What "hold" means in practice — remediation, not abandonment.
8. The 90-day review.
9. Common gaming patterns (and why they fail).
10. The worked example.

**References:** `governance/KLARNA-TEST.md`, `templates/excel/klarna-test.xlsx`, Routine R7.

---

### `docs/06-when-to-call-a-lawyer.md`

**Audience:** All.

**Purpose:** The eleven jurisdiction-specific legal touchpoints where local counsel is mandatory. The framework's most important "what we don't pretend to do" document.

**Required sections:**

Disclaimer at the top. Then: for each of the eleven touchpoints, a section with:

1. **The touchpoint name.**
2. **Why it matters.** What can go wrong.
3. **What ØØT provides.** Templates, Skill Packs, governance docs that touch this.
4. **What ØØT does not provide.** Legal interpretation, jurisdiction-specific clauses, advocacy.
5. **Trigger questions for counsel.** What to ask when you hire a lawyer.
6. **Indicative cost.** Rough order-of-magnitude for legal scoping.

The eleven touchpoints (per `MANIFESTO.md` "What ØØT is not" section):

1. **Worker classification** (partner vs. employee). Highly variable across EU/US/UK/Asia.
2. **Variable pay legality.** Some jurisdictions require minimum guaranteed wage; others disallow output-only pay structures.
3. **Profit-share structures.** Entity choice (LLC, GmbH, S.r.l., d.o.o., etc.).
4. **Crypto payroll.** Most jurisdictions allow as supplement, not primary; AML/KYC implications.
5. **Long-tail entitlements.** Securities-law implications when tied to revenue percentages.
6. **Internal Unit Fund.** Securities offering registration; jurisdiction-specific.
7. **EU AI Act Articles 9, 12, 13, 14** (from 2 August 2026, high-risk obligations).
8. **GDPR Article 22** (right against solely-automated decisions).
9. **Data residency** — where the Brain physically lives. EU vs. US implications.
10. **Italian Law 132/2025** (criminal AI offences; leading indicator of EU enforcement seriousness).
11. **IP ownership of Brain content** (employer vs. partner work-for-hire; jurisdiction-specific).

**References:** `governance/EU-AI-ACT.md`, `MANIFESTO.md` (closing section).

**This doc must end with the strongest version of the disclaimer:** *"ØØT is a framework. It points at landmines; it does not defuse them. Local counsel is mandatory before adoption in any jurisdiction. The framework's authors take no responsibility for outcomes of adoption without counsel."*

---

### `docs/07-troubleshooting.md`

**Audience:** All.

**Purpose:** Common issues by symptom. Living document — additions welcome.

**Structure:** Two-column index at top (Symptom → Section). Then per-symptom section: cause analysis, remediation steps, when to escalate.

**Initial symptom set (Claude Code populates with concrete remediations):**

- Claude Desktop says "MCP server failed to start" for MyCuratorMCP.
- The Curator self-test fails on macOS Sonoma+.
- A Routine runs but produces no output.
- A Routine produces an error message I don't understand.
- Excel formulas show #REF! after I edit X1.
- A partner reports their variable pay calculation is wrong.
- The PR auto-label `ai-replaces-human` isn't firing.
- The Brain's wikilinks are breaking en masse.
- LM Studio crashes when I run the daily Routine.
- 4thtech dMail says "wallet not authorised."
- PollinationX storage NFT not recognised.
- The Trezor doesn't connect to 4thtech.
- I lost my Trezor seed — what happens to my 4thtech identity?

For the last item especially: the answer is "your 4thtech identity is gone; create a new one; the firm has to update routing." Be honest.

---

### `docs/08-faq.md`

**Audience:** All.

**Purpose:** Living FAQ. Claude Code populates with the canonical questions; partners and founders add as new questions surface.

**Initial canonical questions:**

- Is ØØT a methodology, a tool, or a framework? *Answer: a framework — markdown specs + tools + Skill Packs + templates + Routines + governance.*
- Do I have to use Claude? *Answer: no. The framework's reference implementation uses Claude, but Skill Packs are markdown and load into any MCP-compatible client.*
- Can I adopt ØØT without crypto? *Answer: yes. Generation 1 is FIAT-default; crypto rails are an opt-in upgrade in Generation 2.*
- What if I'm in the US? *Answer: jurisdictional adaptations required, especially around worker classification and variable pay. EU is more demanding; US is more permissive on some axes, less on others. Counsel mandatory.*
- Can I run ØØT solo? *Answer: technically yes for the Brain and Skills, but the framework is designed for ≥3 partners. Solo use captures maybe 30% of the value.*
- How much does this cost? *Answer: for a 10-partner cloud-track firm, roughly €100–€200/month in tool subscriptions (Anthropic seats, Curator pay-as-you-go, GitHub, Bitwarden). Privacy track adds hardware cost (~€600 for the always-on machine, ~€80 per Trezor for partners).*
- Why "ØØT"? *Answer: pronounced "out". The two crossed-out circles negate legacy headcount and empty hours; the T is Tomorrow.*
- How is this different from Holacracy / Teal / OKRs? *Answer: ØØT is operational and file-based, not philosophical. The other frameworks publish opinions; ØØT publishes Skill Packs, Excel templates, scheduled Routines, and a GitHub repo.*
- Can I fork the framework? *Answer: yes — Apache 2.0 + CC BY-SA 4.0. Forking is encouraged. Send PRs back if you find improvements.*
- What if Anthropic changes? *Answer: the framework is markdown + open standards. Skill Packs work in Cursor, LM Studio, ChatGPT, Claude Desktop, and any future MCP-compatible client. ØØT survives any single vendor change.*
- Is the Klarna Test really mandatory? *Answer: yes. It is the framework's signature epistemic discipline. Treating it as optional is the framework's most important single failure mode.*

---

### `docs/glossary.md`

**Audience:** All.

**Purpose:** Alias of `/GLOSSARY.md` for discoverability from the docs folder.

**Generation note:** This is a one-line file: `See [/GLOSSARY.md](../GLOSSARY.md).` Or, if Claude Code prefers, it can be a literal copy of `/GLOSSARY.md` (kept in sync via CI). The framework's authors prefer the alias to reduce duplication.

---

## Generation order

Recommended order for Claude Code:

1. `glossary.md` (trivial; do first to confirm cross-reference patterns).
2. `00-quickstart-cloud.md` and `00-quickstart-privacy.md` (reference all other docs heavily; do these next so subsequent docs can reference back).
3. `01-installing-the-curator.md`.
4. `02-installing-routines.md` and `02-installing-routines-privacy.md`.
5. `03-onboarding-a-partner.md`.
6. `04-running-the-business-review.md`.
7. `05-using-the-klarna-test.md`.
8. `06-when-to-call-a-lawyer.md`.
9. `07-troubleshooting.md`.
10. `08-faq.md`.

After all 12 docs, run a cross-reference validation pass: every link resolves; every referenced Skill Pack and Excel file exists.

---

---

## Tier-2 — UI walkthroughs (six docs in `docs/walkthroughs/`)

The day-by-day operational guides. Each one is a single end-to-end task, screenshot-rich, paced for a non-technical reader, with no shell-command dependency. Each walkthrough has a Cloud version and a Privacy version where the underlying tools differ.

### `docs/walkthroughs/W1-claude-desktop-tour.md`

**Audience:** Any partner on day 1.
**Purpose:** Tour Claude Desktop end-to-end so the partner is comfortable using it as their daily driver.

**Required sections:**

1. **What Claude Desktop is** (the first 5 minutes). Where you download it, how to sign in, what the main UI shows.
2. **The conversation pane** — starting a chat, what model is selected, switching models (Sonnet for daily, Opus for high-stakes).
3. **Project Documents** — what they are, how to add a SKILL.md, how the model uses them.
4. **MCP Connectors** — what an MCP is in plain language ("a way for Claude to use external tools"), how to install MyCuratorMCP via the wizard, the green-check vs. red-X states.
5. **Connectors for Drive / Gmail / Calendar / Slack** (cloud track) — install + first-use confirmation. Privacy track: the equivalent local connectors (Desktop Commander, 4thtech).
6. **Loading a Skill Pack** — drag-and-drop a SKILL.md into the project; how to verify the model can see it; first invocation pattern.
7. **The first conversation that produces a Brain page** — walk through asking Claude to help you draft an Output Spec; watch the wikilink discipline live; commit it via the Curator MCP.
8. **Common pitfalls** — MCP server stuck on red X (instructions to fix), Connector authorisation failed, Skill Pack not loading.

**Length:** ~2,500 words + 15–20 screenshots.
**Cross-references:** Skill Pack S1, S2, the Curator install doc (01).

---

### `docs/walkthroughs/W2-curator-daily-use.md`

**Audience:** Any partner who has installed the Curator and wants to use it daily.
**Purpose:** Walk through the five operations every partner does at least weekly: ingest, query, write, scan, fix.

**Required sections:**

1. **What the Curator looks like every day** (5 min). The desktop app's main window, the domain selector, the search bar.
2. **Ingest** — dropping a PDF, a transcript, or a markdown file into the Curator. Watch it parse, see the resulting wiki pages, fix any broken wikilinks immediately.
3. **Query via Claude Desktop** — using the MCP tools (`get_index`, `search_wiki`, `get_node`). How to phrase queries that produce useful results vs. the queries that don't (concrete before/after examples).
4. **Write a Brain page** — the SKILL.md-driven write flow. The Curator's "no speculative wikilink" rule visualised: when Claude proposes a wikilink to a slug that doesn't exist, the user sees the warning and either creates the slug or rephrases the link.
5. **Scan** — running `scan_wiki_health` and `scan_semantic_duplicates` weekly. What the report looks like, what to fix yourself, what to dismiss.
6. **Fix** — the `fix_wiki_issue` flow for typos and broken links. Concrete worked example with screenshots.
7. **When the Curator surprises you** — a small troubleshooting section.

**Length:** ~2,500 words + 15–20 screenshots.

---

### `docs/walkthroughs/W3-excel-monthly-variable-pay.md`

**Audience:** Founder doing the monthly variable-pay sign-off (R3's human side).
**Purpose:** Walk through end-of-month variable-pay review and approval, in Excel/Sheets, without touching any code.

**Required sections:**

1. **What's about to happen** (5 min). On the 1st of the month, R3 (Monthly Variable Calc) ran at 09:00. It populated three things you need to inspect: the Monthly_Variable sheet in `partner-output-ledger.xlsx`, a per-partner Brain statement, and a founder-approval packet. Your job: verify and approve.
2. **Open `partner-output-ledger.xlsx` in Excel** (or in Google Sheets — both shown). The sheet you want is **Monthly_Variable**. Look for the row for the month that just closed.
3. **The four columns to inspect**:
   - `total_outputs` — does it match what you remember the team shipping?
   - `total_variable` — is it consistent with the team's recent average?
   - `base_pay` — is the partner's base correct (matches their X2)?
   - `total_compensation` — the sum.
4. **Drill into each partner's outputs** — open the Output_Log sheet, filter to last month + the partner. Spot-check: are there outputs with `value_tier=S` that look like XS jobs? Any rows with `rework_within_30d=Yes` (which zero out the variable)?
5. **Read the partner's Brain statement** — open the partner's `firm/partners/<id>/variable-statements/YYYY-MM.md` page in any markdown viewer (or in Obsidian if installed). Verify the statement matches the spreadsheet.
6. **Read the partner's acknowledgement** — has the partner ticked the first box (agree) or the second (dispute)? If unresponsive after 5 business days, the founder makes a call: pay anyway with a note, or hold and escalate.
7. **Approve in the spreadsheet** — change the partner's `sign_off_status` from `partner_reviewed` to `founder_approved`. Date it. Save.
8. **Trigger payment** — Gen 1 is FIAT manual. The walkthrough shows: opening the firm's banking portal, copying the payment list from the founder-approval packet, executing the SEPA / wire transfers, recording the `payment_date` in the spreadsheet.
9. **Common pitfalls** — a partner whose Reward Species Declaration has changed mid-month (proration); a retroactive rework zero-out from a prior month showing up in the current calc; a dispute that wasn't escalated cleanly.

**Length:** ~3,000 words + 25 screenshots (Excel and Google Sheets variants both shown for steps 2–7).
**Cross-references:** Skill Pack S3, X1 schema, R3 prompt, DECISION-RIGHTS.md Tier 1.

---

### `docs/walkthroughs/W4-running-the-friday-business-review.md`

**Audience:** The week's BR facilitator (rotates among partners) plus all attendees.
**Purpose:** Run the Friday BR meeting end-to-end.

**Required sections:**

1. **What the BR is** (5 min). 30 minutes. Replaces all status meetings. Agenda is generated by R2 at 08:00 Friday.
2. **Pre-read** — at 09:00 the facilitator opens `business-review.xlsx` Weekly_Review sheet and Slack `#business-review`. Reviews R2's draft. Confirms with the founder if anything looks off.
3. **The 30-minute meeting structure** (with an annotated example agenda):
   - Outputs (10 min) — read the top 5; congratulate quickly, ask sharp questions only on outliers.
   - Blockers (5 min) — owner, ETA, what help is needed.
   - Decisions (10 min) — work through Decisions_Due. Each decision recorded by the scribe in `firm/decisions/D-YYYY-NNN.md`.
   - Klarna status (3 min) — open tests, test outcomes since last week.
   - KPI snapshot (2 min) — 30-second look at the agent-skill-roi dashboard and treasury runway.
4. **The post-meeting commit** — the scribe finalises the Brain page (`firm/business-reviews/YYYY-MM-DD.md`) within 30 minutes of the meeting ending. R2 detects the post-meeting commit and updates the X3 status.
5. **When the BR runs long** — diagnose: usually one of (a) too many decisions queued, (b) a decision that needs more context than the BR can give, (c) a personnel matter that should have gone to the quarterly check-in. Each has a different fix.
6. **Common pitfalls** — facilitator skipping the Klarna status (it's the standing agenda item; never skip), founder dominating the discussion (the BR is for the partnership, not the founder), no scribe (always assign one).

**Length:** ~2,500 words + 8–10 screenshots.

---

### `docs/walkthroughs/W5-running-a-klarna-test.md`

**Audience:** Any partner who needs to score a Klarna Test.
**Purpose:** End-to-end walkthrough of scoring a real Klarna Test in `klarna-test.xlsx`, with the rubric, the evidence, the non-beneficiary review, and the decision.

**Required sections:**

1. **The 5-minute orientation.** What just happened: a PR labelled `ai-replaces-human` triggered R7. You've been assigned as scorer or non-beneficiary reviewer.
2. **Open the Klarna Test in the spreadsheet.** Find the row with your `test_id`. The Klarna_Score sheet has 10 question columns; the Decision_Log shows the trigger and decision.
3. **Read the underlying decision.** Open the PR. Read the description. Read any linked design docs in the Brain. **Do not start scoring yet.**
4. **Score each of the 10 questions, in order.** For each: read the question carefully; reference `governance/KLARNA-TEST.md` for what 0/1/2 means in this context; capture the evidence as a wikilink in the `evidence_links` cell.
5. **The non-beneficiary review.** If you are the non-beneficiary reviewer (assigned by R7 because your variable pay does not increase as a result of the action), your job is to check the scorer's work, not score independently. Look especially for: scoring 1 where evidence supports 0, missing evidence on questions that scored 2, ducked questions (especially Q7 and Q8).
6. **The decision** — total ≥14 → proceed; total <14 → hold + remediate. The spreadsheet auto-computes; your job is to sign the decision (column N for scorer, column O for non-beneficiary).
7. **The remediation flow** — if held, read the per-question remediation list in `governance/KLARNA-TEST.md`. Take action. Re-score. The same `test_id` row gets updated; do not create a new test_id for a re-score.
8. **The 90-day review reminder** — Q9's whole purpose. Confirm the calendar invite landed; confirm the owner is named; confirm the decision framework for the review is pre-committed.
9. **Common pitfalls** — scoring fast (the test takes 30–60 minutes minimum to do well), gaming Q8 ("we won't say anything publicly so it doesn't apply" — the rephrased Q8 closes that loophole; see KLARNA-TEST.md), letting the affected partner score (it's the non-beneficiary's role).

**Length:** ~2,500 words + 12–15 screenshots.

---

### `docs/walkthroughs/W6-monitoring-routines-dashboard.md`

**Audience:** Founder or designated ops partner.
**Purpose:** Day-to-day monitoring of the Routines (cloud or privacy) so the framework's automation stays healthy.

**Required sections:**

1. **What you're monitoring** (5 min). Eight Routines run on schedule. Each one writes a Brain page; each one posts to Slack/dChat. Failures should not be silent.
2. **Cloud track — the Anthropic Routines dashboard.** Where it is, what to look at: the runs panel, the success/failure markers, the daily token spend.
3. **Privacy track — the always-on machine + cron logs.** Where the logs live, how to tail them, what a successful run looks like, what a failed run looks like.
4. **Daily check-in** (60 seconds) — open Slack/dChat `#output-log` and `#brain-health`. Confirm yesterday's R1 ran; this week's R5 ran on Sunday; today's R6 will run at 23:00.
5. **Weekly check-in** (5 minutes) — open `business-review.xlsx` and confirm R2 populated it; open `agent-skill-roi.xlsx` and check the week's spend.
6. **Monthly check-in** (15 minutes) — confirm R3 ran on the 1st; the founder-approval packet exists; partner statements were sent.
7. **What "broken" looks like** — the four most common failure modes (R1 missed a day; R6 audit log gap; R7 didn't catch a PR label; R3 partner statements not delivered) — with screenshots of the symptoms and the recovery procedure for each.
8. **Escalation path** — when ops can't fix it, who to call.

**Length:** ~2,500 words + 15 screenshots (cloud-track dashboard and privacy-track terminal both shown).

---

## Generation order — Phase 7 sequencing

Recommended order (extends the prior 1–10):

1. `glossary.md` (trivial; do first to confirm cross-reference patterns).
2. Tier-1 quickstarts: `00-quickstart-cloud.md` and `00-quickstart-privacy.md`.
3. Tier-1 concept docs: `01` through `08` in order.
4. Tier-2 walkthroughs: `W1` (Claude Desktop tour), `W2` (Curator daily use), `W3` (monthly variable pay), `W4` (Friday BR), `W5` (Klarna Test), `W6` (Routines monitoring).

After all 18 docs, run a cross-reference validation pass: every link resolves; every referenced Skill Pack and Excel file exists.

---

## Acceptance criteria

For all 18 docs:

- All links resolve.
- All commands are tested where possible (cloud-track in a sandbox; privacy-track on a clean test machine).
- All screenshot placeholders are present (with descriptive alt text); actual images come in a follow-up PR.
- The legal disclaimer is present in every doc that touches legal/financial topics.
- No assumed knowledge beyond the level stated in this SPEC.
- Tone is plain, direct, opinionated where the framework has earned the opinion. No marketing language.
- **Tier-1 docs** that involve a UI tool follow the three-layer pattern (orientation → walkthrough → pitfalls).
- **Tier-2 walkthroughs** include both Microsoft Excel and Google Sheets variants for any spreadsheet-touching step, and include both cloud-track and privacy-track variants where the underlying tool differs.

If a doc cannot be plain-language because the underlying topic is technical (e.g., the privacy-track scheduling), the doc should include a "for technical partners" subsection where complexity is acceptable, with a "for everyone else" summary at the top.