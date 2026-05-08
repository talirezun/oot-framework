# Documentation — SPEC

Specifications for the twelve plain-language user guides Claude Code generates in Phase 7 of `BUILD-INSTRUCTIONS.md`. Each doc is for a specific audience, with a specific purpose, with copy-pasteable commands and screenshot placeholders where applicable.

The foundation kit deliberately does not write these docs itself; Claude Code generates them from this SPEC plus the rest of the foundation kit, with full repo context (it has just generated the Skills, Excel templates, and Routines, so it can reference them concretely).

---

## Universal conventions

**Audience tone.** Plain language. No jargon without definition. No assumed technical background beyond "I can edit a config file and run a shell command from a terminal."

**Format.** Markdown. H1 title. H2 sections. Numbered steps within sections. Screenshots placeholders as `![Description](images/<doc-id>-<step-number>.png)` — the actual screenshots are added separately.

**Length.** Most docs are 2,000–3,500 words. The quickstart docs are longer (~5,000) because they cover the full setup. The FAQ is open-ended and grows over time.

**Cross-references.** Every doc links to the relevant SPEC files, Skill Packs, governance documents, and other docs. Use relative links from the doc's own location (e.g., `../governance/KLARNA-TEST.md`).

**Commands.** All shell commands are copy-pasteable. macOS / Linux primary; Windows variants where relevant. Privacy-track docs include cron / launchd / Task Scheduler examples.

**The legal disclaimer block.** Every doc that touches legal or financial topics ends with a standard disclaimer block: *"This document is part of the ØØT framework and is not legal or financial advice. Adapt to your jurisdiction with qualified counsel. See `docs/06-when-to-call-a-lawyer.md` for the eleven legal touchpoints."*

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

## Acceptance criteria

For all 12 docs:

- All links resolve.
- All commands are tested where possible (cloud-track in a sandbox; privacy-track on a clean test machine).
- All screenshot placeholders are present (with descriptive alt text); actual images come in a follow-up PR.
- The legal disclaimer is present in every doc that touches legal/financial topics.
- No assumed knowledge beyond the level stated in this SPEC.
- Tone is plain, direct, opinionated where the framework has earned the opinion. No marketing language.

If a doc cannot be plain-language because the underlying topic is technical (e.g., the privacy-track scheduling), the doc should include a "for technical partners" subsection where complexity is acceptable, with a "for everyone else" summary at the top.