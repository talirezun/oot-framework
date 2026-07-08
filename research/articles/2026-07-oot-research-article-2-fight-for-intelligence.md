---
title: "The Fight for Intelligence: Putting the Organisation of Tomorrow to Work — Use Cases, Vendor Independence, and the Brain Behind the Framework"
author: "Dr. Tali Režun"
author_affiliation: "Vice Dean of Frontier Technologies, COTRUGLI Business School; Founder, The Curator, Block Labs, Lumina AI, Moj AI, 4thTech, PollinationX, Immu3, Online Guerrilla"
date: 2026-07-08
topic: "Use cases / Vendor independence / Three deployment tracks / The Brain (Second Brain, Firm Brain, Ledger)"
peer_reviewed: no
type: original-article
publication: "ØØT Research Series — Article 2 (Use Cases & Vendor Independence)"
series: "ØØT Research Series"
article_number: 2
---

# The Fight for Intelligence: Putting the Organisation of Tomorrow to Work

**By Dr. Tali Režun**
Vice Dean of Frontier Technologies, COTRUGLI Business School · Founder, The Curator, Block Labs, Lumina AI, Moj AI, 4thTech, PollinationX, Immu3, Online Guerrilla
Published: 2026-07-08
Series: ØØT Research Articles — Article 2 (Use Cases & Vendor Independence)
Repository: [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)

> A practitioner's guide to what the Organisation of Tomorrow actually does once it is running: four places founders and leaders feel it immediately, the architecture that keeps any single vendor from holding a firm hostage to its own intelligence supply, and the second-brain infrastructure that turns a company's accumulated judgement into a compounding asset.

---

## Abstract

[Article 1](2026-05-oot-research-article-1-overview.md) in this series made the case for the Organisation of Tomorrow (ØØT) as an operating system for partner-run, AI-augmented firms. This article assumes that case and moves to practice. It opens with an argument that the competitive terrain has shifted from a fight for resources to a fight for intelligence itself, and uses a real nineteen-day event from the eight weeks since Article 1 published to show why a firm's dependence on a single intelligence vendor is now a live operational risk rather than a thought experiment. It then covers what has changed in the framework's own architecture since v1.0 — a third deployment track, a more precisely separated Brain — before turning to four concrete places where founders and leaders feel the framework immediately: speed to market, visibility into technical work without needing to read code, a regulatory-monitoring capability tested in real time by a deadline that moved out from under the framework's own documentation while this article was being researched, and an honest account of what the finance layer can and cannot yet do. It closes with a deeper look at the Curator's Second Brain, Firm Brain (i.e. shared brain), and Ledger architecture — the mechanism by which a firm's judgement compounds instead of walking out the door with every departing partner.

---

## Section 1 — From Manifesto to Practice

In May 2026, this series opened with the case for the Organisation of Tomorrow: an open-source, markdown-first operating system for firms that run on partners rather than employees, and on AI augmentation rather than AI replacement (see [Article 1](2026-05-oot-research-article-1-overview.md)). If you read that piece, you already know its five theses: that resistance to AI tooling is a cultural problem before it is a technical one; that human work in the AI era is centaur work — judgement plus machine speed, neither sufficient alone; that compensation belongs to output rather than hours logged; that a firm's most valuable asset is the knowledge it manages to keep rather than the knowledge that walks out the door with every departure; and that the whole stack should be built from parts nobody can take away from you. The full argument lives in the framework's [`MANIFESTO.md`](../../MANIFESTO.md).

If you are meeting the framework here for the first time, that is a reasonable place to start — and it's just as reasonable to keep reading, because this article doesn't assume you did the homework. ØØT is not a piece of software you buy. It is a GitHub repository: twelve [Skill Packs](../../skills/) (instruction manuals an AI agent reads before doing a job), nine [Excel templates](../../templates/excel/), sixteen [Routine prompts](../../routines/) that run on a schedule, four [governance documents](../../governance/), and a companion app — the [Curator](https://github.com/talirezun/the-curator) — that turns a folder of plain text files into a queryable knowledge graph. Every one of those components is a markdown file, a spreadsheet, or ordinary code. None of it requires the framework's own survival to keep working for you.

Article 1 spent most of its length making the intellectual case and walking the architecture end to end. This article does something narrower: it shows what the framework looks like from inside four specific jobs — founder, leader, compliance-minded operator, and the partner who watches the money — and takes a harder look at two claims Article 1 made almost in passing. Both have since been tested by events neither this series' author nor its readers could have anticipated in May.

The first claim was that no single vendor should sit between an organisation and its own intelligence supply. The second was that a firm's accumulated knowledge, not its headcount, is the asset that compounds. Both got a real-world stress test in the eight weeks since Article 1 published. This article opens with the first, because it is the more urgent of the two — and because the case for it just became considerably more concrete than a line in a manifesto.

---

## Section 2 — The Fight for Intelligence

For most of the industrial and information ages, a firm's competitive advantage was measured in resources it could accumulate faster than its rivals: capital, distribution, talent, patents, shelf space. That fight for resources hasn't ended. But a second one has opened alongside it, running on a different currency: intelligence itself — which frontier model you can call, at what price, under whose terms, and whether that access is something you control or something you rent.

Article 1 raised this as a hypothetical. In its section explaining why the framework's tools were chosen the way they were, it quoted the framework's own [specification](../../SPEC.md) posing a deliberately provocative question to itself — what happens if the vendor changes? Its answer, in May, was architectural and confident: the framework is markdown and open standards, so it survives any single vendor's decisions. That was true then. It is still true now. But "survives a change" stopped being a hypothetical about three weeks after Article 1 went out.

On 12 June 2026, one of Anthropic's newest frontier models — Claude Fable 5, released just three days earlier — went dark worldwide. The U.S. Department of Commerce had issued an export-control directive ordering Anthropic to cut off access for any foreign national anywhere, including the company's own non-U.S. employees. Anthropic said at the time it had not been given a specific reason beyond national-security concerns; later reporting pointed to a disclosed method for partially bypassing one of the models' cybersecurity safeguards. Because there was no way to verify every user's nationality in real time, the only way to comply was to suspend both models for everyone (CNBC, 30 June 2026; Forbes, 1 July 2026).

The suspension lasted nineteen days. On 30 June, the Department of Commerce lifted the export controls following what Commerce Secretary Howard Lutnick described as roughly two weeks of joint review with Anthropic; global access began returning on 1 July, with Fable 5 restored on a narrower basis to specific vetted organisations.

Nothing about this sequence required a villain, and it is worth resisting the temptation to cast it as one. The order came from a government agency responding to a disclosed vulnerability, not from Anthropic itself, and the company spent the intervening weeks negotiating its way back rather than benefiting from the outage — its public statements once access returned were thankful toward affected users rather than triumphant. That is precisely the point worth sitting with: an organisation does not need anyone to act in bad faith for a single-vendor intelligence dependency to become a real operating risk. A regulator's order, a policy shift in a country you don't operate in, or simply a change of terms can now reach directly into what your firm is capable of doing on a Tuesday morning, and you will have had no vote in the decision.

The nineteen days produced one more data point worth recording, because it is the exact shape of the argument this framework has been making since Article 1: officials in Europe and other U.S. allies reportedly voiced concern, during the blackout, about their own institutions' dependence on decisions made in Washington (reported by Semafor, 27 June 2026, and cited in subsequent industry coverage of the episode). That is not a EU entrepreneur's thought experiment about sovereignty. That is other governments discovering, in real time, the same single point of failure this framework was built to route around.

> **In plain terms.** For nineteen days in June, one of the world's most capable AI models simply wasn't available to most of the planet — not because the company that built it wanted it that way, but because one government said so, and there was no way to argue with a border. If your firm's daily operations run entirely inside one vendor's cloud, that is now a demonstrated risk, not a paranoid one. The Organisation of Tomorrow's answer is not "don't use Anthropic" — the cloud track remains the framework's recommended, fastest path for most founders. Its answer is: never let your firm's ability to function depend on only one path existing.

This is the argument the rest of this article is really about. Use cases are downstream of architecture. Before getting to what a founder, a leader, or a finance partner actually does with ØØT day to day, it's worth being precise about the architecture that makes all of it survivable.

---

## Section 3 — No Vendor, No Lock-In: Three Tracks Today

Article 1 described two deployment tracks: cloud and privacy. Since then, a third has shipped — the **Community track**, added in the framework's [v1.3.0 release](../../CHANGELOG.md) (5 July 2026) for founders who want independence from any subscription at all, not necessarily a sovereignty mandate. All three tracks run the identical sixteen [Routine prompts](../../routines/), the same twelve [Skill Packs](../../skills/), the same nine [Excel templates](../../templates/excel/), and the same [governance documents](../../governance/). Only two things differ between them: which agent drives the work, and what wakes it up on schedule. The decision to keep the rulebook byte-identical across tracks is recorded in [ADR-003](../../docs/internal/ADR-003-community-track-no-subscription.md).

The **cloud track** remains the fastest path for most founders: Claude Desktop and Claude Code as the daily interface, with Claude Code Routines firing the scheduled work on Anthropic's own infrastructure, so automation keeps running with the laptop closed.

The **privacy track** is for firms with an actual sovereignty requirement — customer data that legally cannot touch a cloud model, or a founder who simply wants every dependency to sit on hardware they own. It runs on an always-on machine, local open-weight models served through LM Studio, and the operating system's own scheduler, firing the same Routine prompts against a locally hosted model via a lightweight open-source coding agent called [OpenCode](../../installer/agent-assisted/OPENCODE-SETUP.md). The one honest trade-off: the machine has to stay switched on.

That hardware line deserves more precision than "buy a cheap always-on box." The framework's own live testing found its smallest tested local model produced small but real cosmetic errors on daily runs — a stray file suffix, a dropped line of formatting, the kind of thing a founder catches on review but would rather not have to. The finding that came out of that testing was to run something meaningfully larger for production Routines. That is a genuine infrastructure decision with a genuine memory cost, and it's exactly why "invest in a capable machine" is the honest way to describe this track, rather than "buy the minimum that boots." If a serious business is going to run its daily operations on a local model, size the machine to the model you actually intend to run — realistically a Mac mini or similar unified-memory machine with real headroom, not the cheapest box that technically starts LM Studio.

The **community track**, new in this release, exists for a founder with no subscription budget and no sovereignty mandate — someone who wants to try the framework for the cost of electricity. It runs the same OpenCode harness against free or self-supplied models and climbs a three-rung automation ladder, from manually pasting a prompt, to a laptop cron job, to a scheduled GitHub Actions workflow. It makes no sovereignty claim: its Ledger data still transits whichever model provider is chosen, so it is a budget answer, not a privacy answer.

| | **Cloud** (canonical) | **Privacy** (sovereignty) | **Community** (no subscription) |
|---|---|---|---|
| **Harness** | Claude Desktop / Claude Code | OpenCode, headless, against a local model | OpenCode, free or self-supplied models |
| **Automation** | Runs on Anthropic's infrastructure — laptop can stay closed | OS scheduler (cron / launchd) — the machine must stay on | Manual → laptop cron → GitHub Actions (a 3-rung ladder) |
| **Typical cost** | ~€20–100 / month per active seat | ~€2,460 one-time + ~€8–15 / month electricity | Free to start + ~€5–10 / month for Brain ingest |
| **Sovereignty claim** | No | Yes | No |
| **Best for** | Most founders — fastest path | Regulated data, or a philosophical commitment to self-custody | No budget yet; testing the framework |

*Canonical cost tables and the full track comparison live in [`docs/ECOSYSTEM.md`](../../docs/ECOSYSTEM.md#cost-summary).*

> **In plain terms.** There are now three ways to run this framework and they all follow the exact same rulebook — only the "robot assistant" and the "alarm clock" differ. Because the rulebook never changes, a firm that starts on the free path can move to cloud once revenue justifies it, or a cloud-track firm with a new regulated client can move part of its operation to the privacy track, without rebuilding a single Skill Pack, Excel template, or governance document. That portability is the actual disproof of lock-in — not a slogan, but a firm's demonstrated ability to leave and take everything with it, working, on day one of the move.

The vendor-independence argument in Section 2 is not really about Anthropic, or about any one company. It is about never letting the choice of who to build a business on be a choice a firm only gets to make once.

---

## Section 4 — Four Places Leaders Feel This Immediately

Everything above is architecture. This section is where that architecture turns into something a founder, a manager, or a partner actually does on a Tuesday. Four places stand out — not because they are the only ones, but because they map directly onto the four jobs a leader running a technology-adjacent company actually has: get to market, understand what the team is building, stay ahead of the rules, and know where the money is going.

### 4.1 — Founders: Speed as the Only Moat

For a founder, the entire pitch of AI augmentation collapses into one word: speed. Every week spent building the thing that gets discovered first is a week a competitor doesn't get. But speed from AI tooling is not automatic, and the evidence on this point is uncomfortable enough to deserve stating plainly before making any promises.

A randomised controlled trial run by [METR in 2025](../papers/metr-rct-2025.md) measured experienced open-source developers working on real tasks with and without AI coding tools. The developers using AI tools were measurably slower — by roughly a fifth — while believing, just as strongly, that they had been faster by about the same margin. That is not a rounding error; it is close to a 40-point gap between how fast people felt and how fast they actually were, and it is exactly the kind of gap a founder cannot see from the inside without instrumentation.

This is the argument for structure over enthusiasm. ØØT's founder-facing Skill Packs exist to convert raw model capability into measured throughput rather than felt throughput: an [Output Spec](../../templates/output-spec.md) defines what "done" looks like before work starts, so a shipped feature has a clear finish line instead of a vibe; a daily [output-capture Routine](../../routines/) logs what actually got produced, with no one filling in a timesheet; and the framework's own recommended discipline — encoded in the [change-management Skill Pack](../../skills/change-management/SKILL.md) — is to establish a real productivity baseline before rolling out a new Skill at all, precisely so a firm can catch its own version of the METR gap instead of discovering it a year later in a board meeting.

The Curator adds a second, quieter speed advantage. A founder juggling customer interviews, competitor teardowns, term sheets, and technical specs can feed all of it into a personal knowledge graph and query it directly — "summarise the recurring friction points across the last twenty customer conversations" returns a cited answer in seconds rather than a re-read of twenty transcripts. In practice it functions as a standing board of advisors built entirely from a founder's own accumulated observation, weighted by nothing except how often something has actually come up (see the Curator's own [use cases](https://github.com/talirezun/the-curator/blob/main/docs/use-cases.md)).

None of this replaces judgement. It replaces the time judgement used to cost.

### 4.2 — Leaders & Managers: X-Ray Vision Into the Machine

The second use case speaks most directly to a non-technical leader: how do you actually know what your development team — human and AI both — is doing, without learning to read the code yourself?

The honest mechanism is a daily habit, not a dashboard to stare at. The framework's own monitoring discipline asks for sixty seconds a day, five minutes on Fridays, and fifteen minutes on the first of the month. The sixty seconds: a scheduled Routine posts a plain-language summary of the previous day's shipped work every evening, and a green or red status tells you immediately whether anything needs a look (walkthrough: [monitoring the Routines dashboard](../../docs/walkthroughs/W6-monitoring-routines-dashboard.md)). The five minutes: a Friday-morning [Business Review](../../skills/reporting-business-review/SKILL.md) — also prepared automatically — turns a week of commits, reviews, and decisions into a short readable report: what shipped, what's still open, what the automation itself cost to run that week (walkthrough: [running the Friday Business Review](../../docs/walkthroughs/W4-running-the-friday-business-review.md)).

The deeper version of this is what happens when someone proposes replacing a piece of human judgement with an AI system entirely — and this is where the framework's signature discipline, the [Klarna Test](../../governance/KLARNA-TEST.md), does its real work. Named for Klarna's public [2024 reversal](../papers/klarna-2024-2026.md) — roughly 700 customer-service roles cut in favour of AI, then quietly rehired on a hybrid model once quality slipped — the test is a ten-question rubric, scored out of twenty, that any such proposal has to clear before it can go live. A leader does not need to understand a single line of code to read the scorecard.

Here is what that looks like in the framework's own worked example. [Solunar Studio](../../examples/small-org/), a three-partner reference firm the framework uses to teach itself, proposed handing its routine customer-onboarding emails to an AI system, with the partner who used to write them by hand kept on as the escalation path for anything unusual. The proposal scored 16 out of 20. The two soft spots were flagged in plain language — the pilot had run four weeks rather than the recommended three months, and the 90-day follow-up review was thin — and both were scheduled to be tightened rather than waved through. The reviewer who signed off was, by design, someone whose own pay does not increase because of the change, so the sign-off carries no obvious conflict of interest. A calendar invite for the 90-day recheck existed before the decision went live. If a defined threshold is breached — satisfaction dropping, error rates climbing — a same-day reversal plan reactivates the human step.

That entire paragraph is readable by a founder with zero engineering background, because it was written to be. This is what "AI can simplify and teach you what your developers and their AI agents are actually doing" looks like in practice: not a black box you're asked to trust, but a scorecard, a named non-beneficiary reviewer, a reversal plan, and a date already on the calendar. The framework calls this transparency architecture rather than technical gatekeeping — a leader is being asked to understand a decision, not audit an implementation. (Step-by-step: the [using the Klarna Test](../../docs/05-using-the-klarna-test.md) guide and the [W5 walkthrough](../../docs/walkthroughs/W5-running-a-klarna-test.md).)

### 4.3 — Watching the Rules Change While You Sleep

The third use case is the one this research turned up a genuinely useful example of while writing it, which is an unusual sentence to write and also the whole point.

Founders operating in the EU have had one date circled for two years: 2 August 2026, when the EU AI Act's high-risk obligations — covering AI used in employment decisions, credit access, and a handful of other sensitive categories — were due to take full effect. This framework's own [governance documentation](../../governance/EU-AI-ACT.md), current as of its most recent release on 5 July 2026, still cites that date as the operative deadline. As of this writing, that date has moved.

Through the spring of 2026, the European Commission, Parliament, and Council negotiated a "Digital Omnibus" package to simplify the Act's rollout. Trilogue talks collapsed once, in late April, then produced a political agreement in early May. The European Parliament formally endorsed it on 16 June; the Council of the EU gave its final green light on 29 June. Formal publication in the Official Journal was, at the time of the most recent reporting available, still pending — but substantively, the high-risk deadline for the categories that affect most employers has moved from 2 August 2026 to 2 December 2027, sixteen months later than nearly everyone had been planning for (Gibson Dunn, 2026; DLA Piper GENIE, 2026). A narrower set of obligations — chiefly the requirement to disclose when someone is interacting with an AI system — still lands on the original August date.

Sit with what just happened in the paragraph above. A deadline that shaped two years of compliance planning across the European Union shifted by more than a year, through a legislative process that ran for months in full public view — and a carefully maintained, actively updated open-source framework's own governance files, refreshed as recently as three days before this article was drafted, hadn't caught up with it yet. Not because anyone was careless. Because tracking regulatory reality continuously, rather than checking it once and filing it away, is a genuinely hard, ongoing job — exactly the job the [governance & compliance Skill Pack](../../skills/governance-compliance/SKILL.md) exists to eventually do without anyone having to remember to look.

Today, what actually runs is more modest than that, and it's worth being honest about the gap between the two. A scheduled Routine writes a timestamped, cryptographically signed audit entry every night at 23:00, recording what the firm's AI systems did that day — the Article 12 record-keeping obligation, satisfied automatically, whether or not anyone remembers to ask for it. On a day with no relevant AI activity, it writes that too, so a gap in the log is never silently indistinguishable from a quiet day. That piece works today. The deeper capability this article just demonstrated the need for — a system that actually watches Brussels and Washington so a founder doesn't have to, and flags when the ground has shifted — is still on the framework's own [roadmap](../../GENERATIONS.md), honestly labelled as such in its own documentation.

None of this replaces counsel, and the framework is unusually blunt about that: it maintains an explicit list of [eleven legal touchpoints](../../docs/06-when-to-call-a-lawyer.md) — worker classification, variable-pay legality, cross-border data handling, and others — where local counsel is described as mandatory, not optional. What the framework offers is not a lawyer. It is the thing that makes sure a lawyer's advice from eighteen months ago gets revisited before it quietly goes stale.

### 4.4 — An Honest Look at the Finance Layer

The fourth use case — "AI can keep track of the finances" — is the one where this article is least able to promise a finished product, and the framework's own honesty principle means saying so rather than describing the roadmap as though it had already shipped.

What works today: a running ledger of what the firm's AI stack actually costs, broken down by which Skill Pack or Routine is spending the money, updated automatically from usage data. That answers a question every founder eventually asks nervously — is this AI subscription actually paying for itself, or are we just paying rent on enthusiasm? — with a number instead of a guess. A monthly rollup turns that into a return-on-investment figure per Skill Pack, so a founder can see, in plain terms, which parts of the automation are earning their keep and which have quietly stopped.

What's still hardening: the deeper treasury layer — cash-runway tracking, obligation forecasting, the eventual bridge to automated payroll execution — is specified in detail in the [finance & treasury Skill Pack](../../skills/finance-treasury/SKILL.md) but ships today as what the framework candidly calls a scaffold: the shape is there, the operational instructions are still being filled in release by release. This is deliberate sequencing, not an oversight. The framework's compensation architecture is explicit that FIAT currency is the default in this generation, with stablecoin payroll rails and a genuine internal investment fund deferred to the [next one](../../GENERATIONS.md) — gated behind six to nine months of real pilot data and a jurisdictional legal review the framework insists on rather than skips.

The instinct to want this already finished is understandable, and the honest answer is: not yet, on purpose. A firm adopting the framework today gets a real, working cost-visibility layer and a clearly labelled roadmap for the rest, rather than a glossy promise that quietly under-delivers eight months in. Given what Section 4.3 just demonstrated about what happens when a framework's own claims outrun what has actually been tested, that sequencing discipline is worth more than it might first appear.

---

## Section 5 — The Brain Behind It: Second Brain, Firm Brain, and the End of Institutional Amnesia

Thesis four of the original [manifesto](../../MANIFESTO.md) claimed that a firm's most valuable asset is not its headcount but its Collecting Brain — the compounding record of everything it has decided, learned, and produced. Article 1 described this as a single shared knowledge graph that every partner reads from and writes to. Since then the architecture has matured into something more precise, and the change is worth explaining because it fixes a real problem the earlier design had. The separation is recorded canonically in [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md).

As of the framework's current release, what used to be one Brain is now three distinct primitives, and conflating them is explicitly treated as a design error:

- **The Second Brain** is personal — one per partner, living on that partner's own machine, capturing everything they read, decide, and think through, whether or not any of it ever leaves their laptop.
- **The Firm Brain** is the firm's shared library — a synthesised, queryable collective wiki, rebuilt weekly from whatever each partner has chosen to contribute.
- **The Ledger** is the firm's accounting books — spreadsheets and a signed audit trail, written only by automation, never by hand-editing history.

> **In plain terms.** Think of three separate books, kept in three separate places on purpose. Your personal notebook is yours; you choose the one section of it that ever gets shared. The company library is everyone's shared sections, merged into one searchable collection every week. The accounting books are written automatically and never touched by hand. Keeping them apart is what stopped an earlier version of this design from accidentally leaking a partner's private notes into company infrastructure — a real problem in the framework's first release, fixed in the second.

Only one domain of a partner's personal Curator ever contributes to the Firm Brain, and it does so as a pre-processed summary rather than a raw file dump, so a partner's private journal, unrelated side project, or unfinished thinking never crosses into company records by accident. Attribution defaults to a pseudonymous code rather than a name — a real person's name surfaces in the Firm Brain only if both the firm and that individual partner separately opt in — and the framework ships a working right-to-erasure mechanism that removes a departed contributor's fingerprints from the collective record entirely, not just from a list somewhere. Full detail on how this is set up and administered is in the Curator's own [Shared Brain architecture](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md) and [Shared Brain user guide](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-user-guide.md).

Why does any of this matter more than it sounds like it should? Because of two properties a spreadsheet or a shared drive cannot replicate.

The first is what a firm's own executives already get from the Curator in its general-purpose form: an intelligence layer with no recency bias. A transcript from six months ago and a transcript from yesterday carry equal weight in the graph unless something about the content itself makes one more relevant — which directly answers the distortion every leader eventually runs into, where the loudest recent voice in the room quietly outweighs a much better insight from a customer call two quarters back. Query it and it returns, with citations, which concern has actually recurred most often across every conversation fed into it — not which one happens to be most vividly remembered.

The second is what happens when a partner leaves. The Curator's own [documentation](https://github.com/talirezun/the-curator/blob/main/docs/use-cases.md) walks through exactly this scenario for a mid-sized engineering team: a new hire, in their first week, asks why the team chose one database over another, and gets back a plain answer with a citation to a decision made years before they joined — the kind of onboarding that used to take weeks, compressed into days, because the reasoning behind a decision, not just its outcome, survived the person who made it. That is the literal mechanism behind the claim that employees can come and go while the knowledge stays. It isn't a retention policy. It's an architecture that makes the why — the actual context behind a choice — as durable as the choice itself, which is the only form of institutional memory that has ever been worth anything.

One honest caveat belongs here, in the same spirit as the finance-layer admission above: the Firm Brain's weekly synthesis step currently makes one small outbound call to a low-cost cloud model to help merge contributions cleanly — the one piece of the privacy track that isn't yet fully local. The next generation's [roadmap](../../GENERATIONS.md) removes it, bringing the Brain itself to full sovereignty. Until then, it is a narrow, disclosed exception in an otherwise self-hosted stack, not a hidden one.

Compounding is the word that matters most here, and it is worth taking literally rather than as a metaphor. A spreadsheet does not get smarter with use. A Slack archive does not get more useful the longer nobody searches it. A knowledge graph built this way does get more valuable every week, because every new page strengthens the links around it rather than sitting beside them — and unlike almost every other asset a small firm owns, this one has no natural ceiling on how much more valuable next year's version can be than this year's.

---

## Section 6 — Radical Simplicity as a Design Philosophy

One more property of the architecture deserves its own space, because it is easy to undervalue precisely because it looks unglamorous: every single component of this framework is a plain text file, a spreadsheet, or ordinary code. Markdown files. `.xlsx` workbooks that open in Excel, LibreOffice, or Numbers without complaint. A GitHub repository as the version-controlled record of everything. No proprietary database, no vendor-specific storage format, nothing that requires a running service just to read what you've built.

This is a second, independent line of defence against lock-in — one that operates below the level of Section 3's argument about deployment tracks. Even a firm that abandoned this framework entirely tomorrow would walk away with a folder of files any text editor built in any decade could open. That is a different, and in some ways stronger, guarantee than "you can switch AI vendors": it's the guarantee that the underlying record of the firm's work was never actually dependent on the framework's own continued existence, let alone anyone else's.

The discipline behind this choice cost more time to get right than it might look like from the outside, and it is worth saying plainly that simplicity of this kind is a design decision, not an absence of one. It would have been faster to reach for a purpose-built database, a hosted app, a proprietary format optimised for the job at hand. Every one of those choices would have been more convenient in the first month and a genuine liability in the third year. Markdown and spreadsheets are not the ambitious choice. They are the choice still legible in 2036.

> **In plain terms.** Everything this framework produces is a file that could be opened on a computer built decades from now, using software that doesn't exist yet, because the format itself — plain text, standard spreadsheets — has already survived that test once. That is not a modest claim. It is the specific property that lets a small firm behave, structurally, like an organisation built to outlast the tools it happens to be using this year.

---

## Section 7 — Conclusion: Where This Goes Next

Generation 1 — everything described in this article — is what ships today, and it is no longer only theory: it has now been validated end to end against a real test company rather than on paper alone. Generation 2, expected within the next six to twelve months, brings stablecoin payroll rails, a genuine internal investment fund gated behind real pilot data, a fully local Curator that finally removes the one remaining cloud dependency described in Section 5, and a native desktop app so a non-technical founder never has to open a terminal at all. Generation 3 is further out and more speculative: the Cotrugli Ledger governance layer, developed with Dražen Kapusta, and the genuinely frontier idea of an autonomous agent operating as its own business unit — its own legal entity, its own wallet, hiring human partners through the same framework described in this article. The framework is explicit that Generation 3 is research-stage, that no timeline is promised, and that some of it may simply not work. That honesty is a feature, not hedging. The full roadmap is in [`GENERATIONS.md`](../../GENERATIONS.md).

What ties this article back to Article 1 is a single idea, restated with more evidence behind it than it had in May: the fight ahead is a fight for intelligence, and the firms that win it will not be the ones with the single best model on a given Tuesday. They will be the ones whose architecture doesn't depend on which model is best on a given Tuesday — because the framework, the Brain, and the firm's own accumulated judgement all belong to the firm itself: portable, readable, and running regardless of what any one vendor, regulator, or government decides next.

The next article in this series will go deeper into a single piece of this stack rather than surveying all of it — the framework's own live validation, the real gotchas its authors hit running this against an actual test company, and the diagnostic honesty that produced a fifty-one-test automated suite where there was none eight weeks ago. For now, the guides below cover installation, the Klarna Test, and the Curator's Shared Brain in more detail than this article had room for.

---

## Further Reading

The framework and the Curator are both fully open-source. The following guides, referenced throughout this article, go deeper into specific pieces of the stack.

### Organisation of Tomorrow ([github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework))

- [Article 1 — Building the Organization of Tomorrow](2026-05-oot-research-article-1-overview.md)
- [Cloud track quickstart](../../docs/00-quickstart-cloud.md)
- [Privacy track quickstart](../../docs/00-quickstart-privacy.md)
- [Using the Klarna Test](../../docs/05-using-the-klarna-test.md) · [the canonical rubric](../../governance/KLARNA-TEST.md)
- [When to call a lawyer — the eleven touchpoints](../../docs/06-when-to-call-a-lawyer.md)
- [EU AI Act mapping methodology](../../governance/EU-AI-ACT.md)
- [Walkthrough — monitoring the Routines dashboard](../../docs/walkthroughs/W6-monitoring-routines-dashboard.md)
- [Walkthrough — running the Friday Business Review](../../docs/walkthroughs/W4-running-the-friday-business-review.md)
- [Installing the Curator](../../docs/01-installing-the-curator.md)
- [The Glossary](../../GLOSSARY.md)
- [The Manifesto](../../MANIFESTO.md)

### The Curator ([github.com/talirezun/the-curator](https://github.com/talirezun/the-curator))

- [Use cases](https://github.com/talirezun/the-curator/blob/main/docs/use-cases.md)
- [Shared Brain — concept & architecture](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md)
- [Shared Brain — user guide](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-user-guide.md)
- [Main user guide](https://github.com/talirezun/the-curator/blob/main/docs/user-guide.md)
- [MCP user guide (connecting Claude and other clients)](https://github.com/talirezun/the-curator/blob/main/docs/mcp-user-guide.md)

---

## References

### Framework

- Režun, T. (2026). *ØØT — Organisation of Tomorrow* (v1.3.0). GitHub. [github.com/talirezun/oot-framework](https://github.com/talirezun/oot-framework)
- Režun, T. (2026). [*Building the Organization of Tomorrow*](2026-05-oot-research-article-1-overview.md). ØØT Research Series, Article 1.

### The Fable / Mythos export-control episode

- CNBC (30 June 2026). *Anthropic says Trump admin has lifted export controls on Claude Fable 5 and Mythos 5.*
- Forbes (1 July 2026). *White House Lifts Restrictions On Anthropic's Mythos And Fable AI Models.*
- MarketScale (2026). *Fable 5 and Mythos 5 Are Back: What the 19-Day Shutdown Taught Every Enterprise About AI as Infrastructure.*
- Semafor (27 June 2026). *Allied governments voice concern over dependence on U.S. AI export decisions* (cited in subsequent industry coverage of the episode).

### The EU AI Act Digital Omnibus

- Gibson Dunn (2026). *EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key Changes.*
- DLA Piper GENIE (2026). *The Digital AI Omnibus: Proposed deferral of high-risk AI obligations under the AI Act.*

### Enterprise AI research (carried forward from Article 1)

- METR. (July 2025). *Randomised Controlled Trial on AI Tools and Developer Productivity.* Summary: [`research/papers/metr-rct-2025.md`](../papers/metr-rct-2025.md).
- Klarna. (2024–2025). *AI-driven customer service transformation: public reporting and reversal.* Summary: [`research/papers/klarna-2024-2026.md`](../papers/klarna-2024-2026.md).

---

## About the Author

Dr. Tali Režun is a serial entrepreneur, business developer, and academic at the forefront of frontier technologies. As Vice Dean of Frontier Technologies at COTRUGLI Business School, he leads AI innovation initiatives and shapes MBA curricula for the next generation of technology leaders. With over thirty years of entrepreneurial experience — founding and scaling ventures including The Curator, Lumina AI, Moj AI, Block Labs, 4thTech, Immu3, PollinationX, and Online Guerrilla — he bridges cutting-edge research in AI and Web3 with practical business transformation.

[github.com/talirezun](https://github.com/talirezun) · [researchgate.net/profile/Tali-Rezun](https://researchgate.net/profile/Tali-Rezun) · [cotrugli.org/talirezun](https://cotrugli.org/talirezun)

---

*This article is published under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](../../LICENSE-DOCS). It is **Research Article 2** in the **ØØT Research Series**.*
