# The ØØT Manifesto

**Five theses for the organisation of tomorrow.**

This document states what ØØT believes and why. The technical specification (`SPEC.md`) translates these theses into Skill Packs, Routines, Excel templates, and governance documents. The two should be read in this order: Manifesto first to understand what we are building toward; Spec second to understand how.

The theses are presented in the order of evidentiary weight — strongest empirical base first — not narrative drama. The framework leads with **Resistance** because that is the central problem, the place where every comparable framework fails, and the place where the practitioner contribution of this framework's authors is sharpest. Compensation, technology, knowledge, and composability follow.

Each thesis carries an explicit honesty clause: what is well-evidenced, what is directional, what is speculative. We do this because the field is full of confident futurism, and confident futurism is the most reliable indicator of an organisation that will fail to adopt AI well.

---

## Thesis 1 — Resistance is the central problem

The technology is ready. The organisations are not.

This is not a slogan. It is the most consistent finding in the 2025 enterprise-AI literature, and it is the place where the gap between what the tools can do and what organisations actually capture is widest.

**The evidence:**

- **MIT NANDA, *The GenAI Divide* (August 2025).** 95% of enterprise GenAI pilots produce no measurable P&L impact. Only 5% achieve rapid revenue acceleration. The root cause of failure is a *learning gap* — organisational and process-level, not model quality. Externally purchased or partnered tools succeed roughly twice as often as internal builds (~67% vs. ~33%). 90% of workers use shadow AI tools daily; only 40% of companies have official LLM subscriptions.

- **METR, *RCT on AI tools and developer productivity* (July 2025).** In a controlled study of experienced open-source developers using **early-2025 AI coding tools** on real OSS tasks, participants were measured **19% slower** while self-reporting they were **20% faster** — a 39-point perception swing. METR's February 2026 follow-up shows similar but wider-CI results; the structural finding (humans cannot reliably self-assess AI-assisted productivity without an external baseline) holds across both studies.

- **Microsoft, *Work Trend Index 2025: The Frontier Firm*.** 82% of leaders call 2025 "pivotal" for rethinking strategy and operations. 81% expect agents to be moderately-to-extensively integrated within 12–18 months. Only 46% are actually automating workflows with agents today. The gap between expectation and execution is the resistance problem in numerical form.

- **Klarna (2024–2026).** The canonical cautionary tale. Klarna publicly cut roughly 700 customer-service roles in 2024 and credited AI for the saving. By 2025–2026 service quality had degraded materially and the company was rehiring on a hybrid "Uber-style" workforce model. Headcount still fell ~40% over the period (5,500 → 3,400) but the headline replacement narrative collapsed. The lesson is not "don't automate" — it is "don't automate before quality bars are proven and reversal plans are real."

**The six findings the framework's Change Management Skill Pack encodes:**

1. **Mandates fail at trust=33%.** License-only rollouts produce shadow refusal. Use structured 6–8 week pilots with 15–20% of the team.
2. **The METR perception gap is the central risk.** Adopt rigorous baseline metrics (DORA, SPACE, DX Core 4) *before* AI rollout, not after. The `metr-baseline.xlsx` template exists for this reason.
3. **AI Champions must be earned, not appointed.** Tecknoworks and Caplaz case studies show artificial champions backfire. The Skill Pack specifies the criteria.
4. **Code review and quality gates are the political battleground.** Stack Overflow remains the preferred verification source for 84% of developers. Skill Packs that bypass this lose adoption.
5. **The "Two Worlds of Code" (Karpathy) is real and time-bound.** By the Software 3.0 transition (~2026–2028), legacy developers face a forced cohort transition. Partner onboarding helps the partner self-identify which world they're entering.
6. **Plan for a 12–24 month resistance plateau.** MIT NANDA's 95% failure rate is largely composed of teams that quit after pilot disappointment. Persistence at the workflow-redesign level is the key correlate of high performance.

**The signature epistemic check:** the **Klarna Test**. Any ØØT recommendation that would have produced the Klarna outcome must be flagged. The full scoring rubric is in `governance/KLARNA-TEST.md`. The test is wired into the Code & QA Skill Pack as a pre-merge gate on any pull request labelled `ai-replaces-human`. Each of the ten questions is scored 0, 1, or 2; the threshold to proceed is **≥14/20 (70%)**. A score below 14 blocks merge.

**Honesty clause:** Resistance is the strongest thesis empirically. It is also the most uncomfortable, because it implies that the bottleneck on AI value capture is the organisation, not the model. We lead with it anyway because the alternative is unserious.

---

## Thesis 2 — Human work in the AI era is centaur work

The human contributes spec, taste, judgement, and the parts of the work that depend on context the model has not seen. The AI contributes implementation at speed. Neither is sufficient alone. This is the **centaur model**, and it has thirty years of literature behind it.

**The evidence:**

- **Harvard Business School, *The Cybernetic Teammate* (Dell'Acqua et al., Working Paper 25-043, 2025).** A controlled field experiment with Procter & Gamble (n=776) showing that **individuals working with AI matched the performance of two-person teams without AI**, that **teams with AI produced more top-tier solutions**, and that AI broke down functional silos between R&D and commercial roles. The effect persists after controlling for individual skill.
- **DORA Report 2025.** Teams using AI assistance show measurable lifts in deployment frequency and lead time, but only when paired with mature CI/CD, code review, and observability practices. Without those, AI assistance accelerates the production of bugs.
- **Karpathy, *Software 3.0* (Sequoia AI Ascent 2026).** The most articulate framing of the new division of labour: spec is human, implementation is AI, review is human. "Agents are like intern entities" — they need taste, aesthetics, and judgement from humans.
- **HBS Cybernetic Teammate** + **MIT NANDA** + **DORA 2025** + **Microsoft Frontier Firm 2025** all converge on the same finding: the highest-performing teams in 2025 are neither the AI-skeptical nor the AI-maximalist; they are the ones who redesigned workflows around the centaur pattern.

**Domain-specific augmentation patterns the framework's Skill Packs encode:**

- **Software development.** Karpathy's pattern: spec / test / review human, implementation AI. Tools: Claude Code, Cursor, Augment Code, Codex CLI, GitHub Copilot. Adoption: 75% of professional developers; 41–46% of code AI-written. Skill Pack: Code & QA.
- **Legal.** Document review, due diligence, contract drafting AI; lawyer = judgement + strategy. Reference platform: Harvey ($11B valuation, $190M ARR, 700+ firms, 42% of AmLaw 100). Skill Pack: Legal Operations (Tier 2 in v1.0).
- **Marketing.** Content generation, segmentation, A/B at scale. 73% of Frontier Firm leaders/workers report using AI for marketing (Microsoft Work Trend Index 2025). Skill Pack: Marketing (Tier 2 in v1.0).
- **Customer service.** AI for routine, human escalation. The Klarna lesson: prove the quality bar before reducing headcount. Reference platforms: Sierra, Decagon, Beam.
- **Sales.** Lead enrichment, outreach, deal-room support. The Lumina AI widget pattern (RAG chatbot as front-door) is the framework's reference.

**The honest framing of the 5/95 ratio.** The "Tim/YOLO Investments thesis" of 5% humans guiding 95% agentic operations is a **design hypothesis**, not a measured outcome. Microsoft's Frontier Firm work explicitly avoids committing to a numerical ratio, framing the human-agent ratio as a task-specific design parameter. Sam Altman's "one-person unicorn" thesis is similarly directional. WhatsApp at acquisition was $345M of value per employee; Nvidia is roughly $100M per employee at $3T market cap. The direction is well-evidenced; the median outcome by 2030 is not. ØØT presents 5/95 as the **limit case** — a useful design star — not the median enterprise outcome.

**Honesty clause:** Centaur work is the most empirically supported thesis after Resistance. The risk is that "centaur" gets watered down in adoption — used as a slogan to keep humans in roles where they no longer add value, or used as a rhetorical fig leaf for full automation. The Klarna Test exists to discipline both directions.

---

## Thesis 3 — Employees become Partners

The salary system was the answer to a 20th-century question: how do you compensate someone for showing up to a factory or an office, when output is hard to measure, attribution is harder, and payment infrastructure is slow?

The infrastructure that produced that question is gone. AI attribution agents now read commits, reviews, contracts, and milestones in real time. Stablecoin payroll settles in seconds. Long-tail entitlements can be encoded in smart contracts. Tokenised internal unit funds can be continuously priced and dividend-paying.

The pieces exist. ØØT puts them on paper and into running code.

**The intellectual lineage:**

Weitzman (1984, profit-sharing macroeconomics) → Levin & Tadelis (Stanford, *Profit Sharing and the Role of Professional Partnerships*) → ROWE (Cali Ressler & Jody Thompson, Best Buy 2003) → Beyond Budgeting (Hope & Fraser, 1998) → DAO contributor models (Dework, Coordinape, SourceCred, Cabin, 2021–2025) → stablecoin payroll (Rise, Circle, USDC/EURC, 2024–2026).

**The evidence each layer adds:**

- **ROWE** reports up to ~35% productivity gains in adopting departments and **52–90% reductions in voluntary turnover** depending on department, in Best Buy, Gap, and IBM case studies (Kelly, Moen et al. research base). Cortisol studies show physiological stress reduction.
- **Performance-based pay** (WorldatWork research): **88% of organisations report it improves engagement; 65% report performance gains in year one**. IZA World of Labor synthesis finds collective performance-related-pay schemes produce roughly **5–15% productivity gains** depending on scheme design. Specific firm case studies (e.g. Salesforce) report 15–35% productivity lifts.
- **Levin & Tadelis** show partnership structures emerge as optimal where production is human-capital-intensive — a near-perfect match for an AI-orchestration era.
- **The gig economy is now structural, not marginal.** Roughly **36% of US workers (~70–76M people)** participate in independent / gig work in 2025 (Upwork / MBO Partners), with the **>50% threshold projected by 2027**. **5.6M independent workers earn >$100k/year**, up 87% from 3M in 2020 (MBO Partners *State of Independence* 2025). On crypto rails: **Triple-A reports 56% of crypto-owning freelancers accept crypto for work**; **Ruul reports ~30% of its freelancer payouts now settle in digital dollars**. The direction is unambiguous; the rails are now production-grade.
- **Crypto-rail compensation infrastructure is production-grade.** Stablecoin payroll settles in seconds for fractions of a cent vs. 1.5–5% all-in cost and multi-day timelines for SWIFT. Rise (Circle partner) has processed >$1B in payroll volume; >50% of worker withdrawals are in stablecoins. EU MiCA and the US GENIUS Act now provide regulatory clarity.

**The seven-layer compensation picture (the YOLO model):**

A complete partner package consists of:

1. **Guaranteed base.** Small. Dignified. The deal is *partner*, not *contractor*; the base recognises that.
2. **Output variable.** Monthly. Calculated from the partner output ledger against value-tier multipliers in the reward-species declaration.
3. **Long-tail outcome.** Quarterly. A percentage entitlement against the *value the artefact actually generated* — features that compound for three years pay their contributors for three years; features that turn out useless pay nothing further. This kills the feature-bloat incentive at the root.
4. **Subscription credits.** Issued alongside variable pay. Non-transferable. Time-bounded. The right to subscribe to the internal Unit Fund. Cash without credits cannot buy in. *(Generation 2.)*
5. **Role-weighted annual bonus.** Roughly thirds split: a third on personal output, a third on team contribution, a third on company outcomes. Weights shift by role.
6. **Dividends on units held.** From Unit Fund participation. *(Generation 2.)*
7. **Capital appreciation on units sold back.** The fund stands ready to repurchase at a published bid; treasury reserves make this real. *(Generation 2.)*

ØØT v1.0 ships **layers 1–3 and 5** as operational. Layers 4, 6, 7 are deferred to Generation 2 because they require legal scoping, treasury reserve discipline, and (typically) crypto rails — none of which should be rushed.

**The reward-species declaration.** Per MHPR Advisors' typology of seven reward species, partnerships fail when reward species is not explicit. ØØT mandates a written declaration per partner, signed at onboarding, stored in `reward-species-declaration.xlsx`. The choices are: pure eat-what-you-kill (high variability, no team component), pure lockstep (low variability, full team smoothing), or a declared hybrid with explicit weights. The choice is not made for the partner; it is *recorded*, version-controlled, and renegotiable on a defined cadence.

**The attribution agent.** The technology that finally makes output-based pay practical at scale. An agent reads commits, pull requests, specs, contracts, milestones, deals; produces a daily per-partner ledger; trains a value-creation model on the firm's own ground truth; gets continuously better at predicting outcome from output every quarter. ØØT v1.0 implements this as a Routine + Skill + Excel pattern. Generation 2 promotes it to a dedicated service.

**The pay rails.** Generation 1 is FIAT. The reward-species declaration includes a one-line preference for stablecoin upgrade when available. Generation 2 is FIAT + stablecoin opt-in (USDC, EURC, via Rise). Generation 3 is fully on-chain entitlements + dividends.

**The honest framing of headcount.** A company running on this no longer hires people; it hires output. The question is not "do we need another full-time engineer" but "do we have enough variable budget to pay for the output we want, and is anyone available who would commit to producing it?" Headcount as a control variable disappears. What remains is the ratio between output produced and total cost — across humans, AI agents, contractors, tooling — and that ratio becomes the **operating measure** of the business. Microsoft calls this the *human-agent ratio*; ØØT operationalises it in `agent-skill-roi.xlsx`.

**Honesty clause:** Output-based pay is empirically grounded for many roles and shaky for others. Some work has long input-to-outcome cycles (R&D, sales for long-cycle products, regulatory work). Some output is hard to attribute (creative collaboration, mentorship, recognition). The framework includes recognition layers and team-bonus components specifically because attribution alone is incomplete. The legal wrappers vary materially by jurisdiction. ØØT does not solve the legal problem; it points at it (`docs/06-when-to-call-a-lawyer.md`) and runs.

---

## Thesis 4 — The firm's IP is its Collecting Brain

Every conversation, every decision, every contract, every deal closed, every code review, every customer interaction, every research session — these are all candidate nodes in a queryable knowledge graph. The firm that captures them in a structured, retrievable, agent-readable form has a compounding asset. The firm that does not is leaking its institutional memory through the cracks every time someone leaves, switches projects, or simply forgets.

This is not a new observation. Karpathy framed it as the "second brain". Nonaka and Takeuchi formalised it as the **SECI model** (Socialization → Externalisation → Combination → Internalisation). Polanyi distinguished tacit from explicit knowledge in 1966. What has changed in 2024–2026 is that the **machinery to operate the second brain at firm scale is now production-grade**.

**The reference architecture (converged 2024–2026):**

1. **Capture layer.** Plain markdown (Obsidian-compatible). Atomic notes. YAML frontmatter. *Exactly the SKILL.md pattern.* This format survives any single vendor's roadmap.
2. **Graph layer.** Knowledge graph linking entities, concepts, summaries. The GraphRAG pattern (Microsoft Edge et al. 2024) is the current best-in-class.
3. **Retrieval layer.** Hybrid vector + graph traversal. Shapley-style influence attribution for downstream compensation (the link back to Thesis 3).
4. **Agentic interface layer.** MCP server exposing tools (the Curator MCP exposes 17). Compatible with any MCP client — Claude Desktop, Cursor, LM Studio, ChatGPT.
5. **Governance layer.** Per-document permissions. Audit logs. EU AI Act Article 12 compliance. The framework's Governance & Compliance Skill Pack handles this.

**The Curator** is the canonical reference implementation in ØØT. It is integrated as Skill Pack S1, with the full SKILL.md adopted from `talirezun/the-curator/blob/main/claude-skills/my-curator/SKILL.md`. Cloud-LLM ingest is operational today (Gemini Flash Lite or Anthropic, pay-as-you-go pricing well under €10/month for heavy usage). Local-LLM ingest is on the Curator roadmap and lands in Generation 2.

**Why this matters at compensation time.** The attribution agent (Thesis 3) reads the same graph. The Brain is not a separate "knowledge management" investment — it is the substrate the compensation system runs on. The same node that records "Tali drafted the term sheet on 2026-04-12" feeds the variable pay calculation, the long-tail tracker, and the institutional memory simultaneously. The firm's value-creation model trains on the firm's own ground truth.

**The five-level Collecting Brain maturity model:**

| Level | State | Indicators |
|---|---|---|
| 0 | None | Knowledge lives in heads, Slack, scattered Drives |
| 1 | Flat docs | Confluence/Notion, no graph, no retrieval, no agent |
| 2 | Vector RAG | Embedding-based search, no graph, single-tool retrieval |
| 3 | GraphRAG | Knowledge graph, hybrid retrieval, manual curation |
| 4 | Agentic MCP-native | The Curator pattern: graph + MCP + skill-driven write discipline |

ØØT v1.0 deploys at **Level 4** by default. There is no point in retrofitting Levels 1–3 if you can start at the destination.

**Polanyi's caveat.** Not all tacit knowledge externalises cleanly. Nonaka's *Ba* (shared context, shared space) reminds us that some knowledge transfer requires synchronous, in-person interaction. The framework includes synchronous rituals (the Friday Business Review, the quarterly partner check-in) precisely because file artefacts alone are insufficient.

**Honesty clause:** The Brain is the right thesis, but it is the most demanding to operate. A poorly-curated Brain becomes a museum of broken wikilinks and stale summaries that nobody trusts. The Curator's MCP scan tools (`scan_wiki_health`, `scan_semantic_duplicates`) are the discipline that prevents this. ØØT's R5 Routine runs the health check weekly. Without the discipline, the thesis collapses into a pile of markdown.

---

## Thesis 5 — The framework is composable Lego

ØØT is a **markdown framework**. It runs on open standards: SKILL.md (Anthropic), AGENTS.md (the cross-vendor orientation file), MCP server cards (Linux Foundation Agentic AI Foundation, December 2025), and the Curator's MyCuratorMCP pattern. These primitives are vendor-neutral by design. They are governed under the Linux Foundation, not by any single AI lab.

This is a deliberate architectural choice. The history of organisational software — ERPs, CRMs, HRIS — is a graveyard of vendor lock-in. Every comparable framework that has tried to ship "the operating system for the future of work" has done so as a SaaS platform with a proprietary data model. ØØT does not do that. The Brain is a folder of markdown files. The Skills are a folder of markdown files. The Routines are markdown prompts. The Excel templates are .xlsx files. The governance documents are markdown files. Anything ØØT writes can be read by any text editor on any operating system in any decade.

**The Lego inventory:**

- **SKILL.md** — Anthropic Agent Skills format. The Skill Pack canonical structure.
- **AGENTS.md** — cross-vendor orientation file at the root of any agent-readable repo.
- **MCP** — Model Context Protocol. Open standard for agent ↔ tool communication.
- **MyCuratorMCP** — the Curator's MCP server. 17 tools. Open source.
- **Plain markdown** — the universal substrate. Obsidian, VS Code, Cursor, GitHub, any text editor.
- **GitHub** — the version-controlled distribution channel. Free for public repos.
- **The xlsx skill** (Anthropic public skills) — the way Claude generates the Excel templates.
- **The Curator** — the reference Brain implementation.
- **4thtech and PollinationX** — the privacy-track communication and storage substrates.
- **Linux Foundation AAIF** — the standards body.

**ØØT's contribution.** Other frameworks publish opinions, methodologies, or platforms. ØØT publishes a markdown spec, twelve hand-built Skill Packs, nine pre-built Excel templates, sixteen Routine prompts (eight cloud + eight privacy), four governance documents, and a GitHub repository. The opinion is in the artefacts. The artefacts are in the repository. The repository is in your filesystem. There is no vendor between you and the framework.

**The "two corners" thesis ØØT occupies:**

The 2025 framework landscape has four corners: (1) Beyond Budgeting / ROWE compensation primitives; (2) Anthropic Skills + MCP + AGENTS.md technical primitives; (3) explicit resistance / change-management playbooks; (4) Collecting Brain knowledge layer with attribution. **No competitor occupies all four corners.** ØØT does, by construction.

**Honesty clause:** Composability is the cleanest thesis to assert and the hardest to prove. It is proven by adoption: when other frameworks borrow our Skill Pack format, when third parties write Routines that run against our Excel schemas, when a partner can leave the framework with their Brain intact and unmodified. ØØT is designed to be left without penalty. The exit door is not vendor lock-in's antonym; it is its disproof.

---

## What ØØT is not

A few common misreadings of the framework, addressed plainly so they don't fester:

**ØØT is not a no-headcount fundamentalism.** Some roles in some jurisdictions need to be employees for legal, tax, or human reasons. The framework specifies the partner model as the default operating mode and provides a clear path for organisations that need a hybrid. The reward-species declaration explicitly accommodates "project specialist" and "advisor" cohorts alongside "full-time partner."

**ØØT is not a crypto-first framework.** Generation 1 is FIAT-default. Stablecoin rails are an opt-in upgrade path documented for partners who want them, available from Generation 2 onward. The framework's commitments to self-custody and on-chain communication (in the privacy track) are about *infrastructure resilience*, not crypto-maximalism.

**ØØT is not anti-management.** The framework removes status meetings and time-tracking; it does not remove leadership. The Friday Business Review, the quarterly partner check-in, the AI Champion role, the human recognition layer in the attribution system — these are explicit, structured, and non-negotiable. Vision-keepers are a named role.

**ØØT is not legal or financial advice.** The framework points at eleven jurisdiction-specific legal touchpoints (`docs/06-when-to-call-a-lawyer.md`). It does not solve them. EU founders adopting ØØT must reconcile the framework with worker classification law, variable-pay legality, securities law (long-tail entitlements, Unit Fund), the EU AI Act (Articles 9, 12, 13, 14 — high-risk obligations from 2 August 2026), GDPR Article 22 (right against solely-automated decisions), data residency, and the Italian Law 132/2025 indicator. Local counsel is mandatory.

**ØØT is not a substitute for the Klarna Test.** Every recommendation in the framework is subject to the Klarna Test. If the test fails, the recommendation is held — even if every other indicator says proceed. The test is not a courtesy. It is the framework's signature epistemic discipline and the most important single sentence in the entire repository: *any ØØT recommendation that would have produced the Klarna outcome must be flagged*.

---

## A closing note on tone

This manifesto deliberately under-claims. The temptation in a document like this is to oversell — to make confident predictions about 2030, to pick a side in the "AI replaces humans / AI augments humans" debate, to declare a winner among current vendors. We have tried not to do any of that.

We do not know what the median enterprise human-agent ratio will be in 2030. We do not know which of Claude, GPT, or Gemini will dominate developer tooling in 2027. We do not know which jurisdictions will move first on the legal frameworks the Unit Fund needs.

What we know is that the *direction* is well-evidenced, the *primitives* are now production-grade, and the *organisations that move first* — carefully, with epistemic discipline, with the Klarna Test in their pocket — will be the ones who turn the technological inflection into a durable advantage. The ones who wait will be the 95% in the MIT NANDA cohort.

ØØT is a way to move first without being foolish about it. The pieces are real. The infrastructure is here. The legal landmines are mapped. The discipline is in the framework.

That is what this manifesto is for. The rest of the repository is what to do about it.

— Dr. Tali Režun, with Dražen Kapusta and the COTRUGLI Business School. Generation 1, 2026.