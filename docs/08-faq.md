# 08 — FAQ

A living FAQ. Submit additions via PR. Initial canonical questions:

---

**Is ØØT a methodology, a tool, or a framework?**

A framework — markdown specs + tools + Skill Packs + templates + Routines + governance. Not a methodology (it doesn't tell you what to *do*; it gives you the operational discipline). Not a tool (it doesn't replace your existing stack; it composes around it).

---

**Do I have to use Claude?**

**Mostly no — with one honest caveat.** The framework's two most valuable, portable assets are vendor-neutral: the **Skill Packs** are plain markdown that load into any MCP-compatible client (Cursor, LM Studio, OpenCode, Cody, future agents), and the **Ledger** is a GitHub repo of markdown + `.xlsx` — no Anthropic lock-in.

The caveat is the **cloud track's scheduled automation**. The Routines (R1–R8) run on **Claude Code Routines**, which today requires an Anthropic Pro-or-higher plan. If you don't want an Anthropic subscription, your alternative *today* is the **privacy track**: run the identical Routine prompts on your own always-on hardware against a local model (LM Studio), scheduled with cron / launchd / Task Scheduler. That's real sovereignty, but it costs hardware and setup time.

A **third, no-subscription-no-hardware path is now documented**: the **community track** ([ADR-003](internal/ADR-003-community-track-no-subscription.md)). Substrate-neutral routine prompts are driven by a free open-source agent (**OpenCode**) on free/local models — no Anthropic plan, no dedicated hardware — with scheduled automation via a 3-rung ladder (manual playbook runs → laptop cron → GitHub Actions). Setup is in [`installer/agent-assisted/OPENCODE-SETUP.md`](../installer/agent-assisted/OPENCODE-SETUP.md); the module map is in [`docs/MODULES.md`](MODULES.md#community-track). So there are now **three** supported answers: "Anthropic plan (cloud track)", "own hardware + local model (privacy track)", or "OpenCode + free models (community track)". The reference implementation is Claude by design (per Thesis 5), but the framework is built to outlive any single vendor. *(Honest status: the community track is documented and author-verified for basic operation; a full end-to-end community-track install is queued alongside the privacy-track e2e test.)*

---

**Can I adopt ØØT without crypto?**

Yes. **Generation 1 is FIAT-default.** Crypto rails (stablecoin payroll, smart-contract long-tail) are an opt-in upgrade in Generation 2. The privacy track uses 4thtech for *communication* (dMail, dChat) but that does not require crypto pay; it only requires per-partner Trezor for wallet identity. Many firms operate the privacy track entirely in FIAT.

---

**What if I'm in the US?**

Jurisdictional adaptations required, especially around worker classification (W-2 vs. 1099) and variable pay. EU is more demanding on AI Act and GDPR; US is more permissive on some axes, less on others (especially securities law for the long-tail entitlements). Counsel mandatory. See [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md).

---

**Can I run ØØT solo?**

Technically yes for the Brain and Skills, but the framework is designed for ≥3 partners. Solo use captures maybe 30% of the value — you get the Curator + the Skill Packs but lose the partnership-cadence (BR, quarterly check-ins, three-tier disputes are all multi-partner constructs).

---

**How much does this cost?**

Tooling costs live in one canonical place: the **[Cost summary in `docs/ECOSYSTEM.md`](ECOSYSTEM.md#cost-summary)** — cloud vs. privacy, solo vs. 3-partner vs. 10-partner, one-time hardware, and per-year recurring. It's kept current there so the numbers don't drift across the docs.

Counsel costs are separate (not a tooling cost): budget for an initial readiness review across the eleven legal touchpoints — see [`docs/06-when-to-call-a-lawyer.md`](06-when-to-call-a-lawyer.md).

---

**Why "ØØT"?**

Pronounced "out". The two crossed-out circles negate legacy headcount and empty hours; the T is Tomorrow / Threshold / the new vector. Search-friendly, ownable, non-conflicting with existing brand names. ASCII contexts use `oot`; the branded mark is ØØT.

---

**How is this different from Holacracy / Teal / OKRs / OBM?**

- **Holacracy / Teal:** philosophical frameworks with implicit operational guidance. ØØT is operational and file-based. The other frameworks publish opinions; ØØT publishes Skill Packs, Excel templates, scheduled Routines, and a GitHub repo.
- **OKRs:** a goal-setting methodology. ØØT incorporates goal-setting via Output Specs but is a much wider framework.
- **OBM (Open-Book Management):** transparency around financials. ØØT shares the transparency commitment but is centred on output-based partner compensation, not financial transparency per se.

---

**Can I fork the framework?**

Yes. License: Apache 2.0 for code + CC BY-SA 4.0 for docs/Skills. Forking is encouraged. Send PRs back if you find improvements.

---

**What if Anthropic changes?**

The framework is markdown + open standards. Skill Packs work in Cursor, LM Studio, ChatGPT, Claude Desktop, and any future MCP-compatible client. ØØT survives any single vendor change. If Anthropic's API costs spike or their model quality regresses, the privacy track is the framework's escape valve (local models, OS-native scheduling).

---

**Is the Klarna Test really mandatory?**

**Yes.** It is the framework's signature epistemic discipline. Treating it as optional is the framework's most important single failure mode. The X4 spreadsheet's data validation prevents partial scoring; the GitHub status check enforces ≥14/20 on labelled PRs; the 90-day review keeps the framework honest with itself.

If your firm finds the Klarna Test consistently rationalising upward, the cause is cultural, not procedural. The test is the framework's canary.

---

**What about Generation 2 / Generation 3?**

- **Generation 2 (6–12 months from v1.0):** stablecoin payroll, smart-contract long-tail, Internal Unit Fund, Curator local-LLM ingest, Tier-2 Skill Pack hardening.
- **Generation 3 (12–24 months, theoretical):** Cotrugli Ledger anchoring (PAC-RO receipts), Kelly-style autonomous business units, per-agent compensation.

See [`GENERATIONS.md`](../GENERATIONS.md). Adopting Gen 1 does not commit you to Gen 2 or 3.

---

**Can I run ØØT for a non-software firm?**

Yes. The framework is industry-agnostic. The S4 (Code & QA) Skill Pack is engineering-specific, but the other 11 Skill Packs apply to any knowledge-work firm. A consulting firm, a design studio, a research collective, a marketing agency — all viable adopters. The framework's authors operate it across software, hardware, content, and research.

---

**What if my partners don't want to use the framework?**

Then don't adopt it. The framework's discipline starts with partnership-wide buy-in. Per [`X9 oot-readiness.xlsx`](../templates/excel/oot-readiness.xlsx) Q05: "Have all founding partners read DECISION-RIGHTS.md and accepted the three-tier dispute path?" If the answer is no, adoption is premature.

---

**How do I contribute?**

See [`CONTRIBUTING.md`](../CONTRIBUTING.md). The framework welcomes documentation, Skill Pack improvements, governance refinements, citations, reference org examples, and bug reports. The framework's licence split (Apache 2.0 for code; CC BY-SA 4.0 for docs/Skills) governs contributions.

---

**Where do I file bugs?**

GitHub Issues on this repo. Include reproduction steps and your environment (cloud or privacy; OS; tool versions).

---

**What's the framework's update cadence?**

v1.x patch releases as needed. v2.0 (Generation 2) targeted for late 2026 / early 2027 depending on Curator local-LLM ingest landing + counsel completing stablecoin / Unit Fund scoping in target jurisdictions. v3.0 (Generation 3) is research-stage; no committed timeline.

---

**Who is "the framework's authors"?**

- **Initiator:** Dr. Tali Režun.
- **Founding contributors:** Dražen Kapusta (Cotrugli Ledger), COTRUGLI Business School.
- **Future contributors:** added as named contributors as they join the project.

---

> ⚖️ This document is part of the ØØT framework and is **not legal or financial advice**.
