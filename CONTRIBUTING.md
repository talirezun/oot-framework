# Contributing to ØØT

Thank you for considering a contribution. This document explains what kinds of contributions the framework accepts, how they're licensed, and what the review process looks like.

ØØT is a framework, not a software product. Most contributions are documentation, Skill Pack improvements, governance refinements, citations, and reference org examples — not code. We welcome both, but the centre of gravity is markdown.

---

## Licence split (read this first)

The repository ships under two licences:

- **Apache License 2.0** — for code, scripts, installers, Routine prompts, and any future attribution-agent implementations. See [`LICENSE`](LICENSE).
- **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** — for documentation, Skill Packs (`SKILL.md` files), Excel templates, governance documents, research articles, and the manifesto. See [`LICENSE-DOCS`](LICENSE-DOCS).

By submitting a contribution, you agree to license it under the appropriate one of those two. If your contribution mixes code and documentation (e.g., a new Skill Pack that includes a `scripts/` folder), the code portion is Apache 2.0 and the markdown portion is CC BY-SA 4.0; the PR description should make this explicit.

If you have an existing copyright on the contribution that is incompatible with these licences, do not submit it. We cannot accept patches that we cannot legally redistribute.

---

## What kinds of contributions are welcome

**Documentation:**
- Fixes to typos, broken links, stale citations, or out-of-date dates.
- Expansions or clarifications to the user guides in `docs/`.
- New Tier-2 walkthroughs (the framework will grow these over time).
- Translations of the user guides (we aim to support EN first; community-led translations welcome for ES, IT, SI, DE, HR, PL).

**Skill Packs:**
- Substantive improvements to existing Tier-1 packs (S1–S6, S12).
- Hardening of Tier-2 packs (S7–S11) into Tier-1 quality.
- New domain-specific sub-packs (e.g. `legal-operations/contract-redline/`, `code-qa/python-saas/`).
- Worked examples in any pack's `examples/` folder.

**Governance:**
- Jurisdictional adaptations of `governance/EU-AI-ACT.md` (e.g., a US AI Act mapping when one exists; UK regulatory mapping; Singapore/MAS).
- Refinements to the Klarna Test rubric based on field experience.
- New decision-rights matrices for organisational shapes the foundation kit doesn't cover.

**Excel templates:**
- Bug fixes (formula errors, conditional-formatting issues, missing named ranges).
- Sheet additions to existing templates that don't break the spec.
- New optional templates that compose with the existing 9.

**Routines:**
- Bug fixes to existing prompts.
- New Routines that compose with the existing 8 (e.g., a quarterly board-pack generator; a customer-NPS rollup).

**Research:**
- Original articles in `research/articles/` per the contribution guide in [`research/README.md`](research/README.md).
- Paper summaries in `research/papers/` for any cited work that does not yet have a summary.
- Updates to `research/external-resources.md` when ecosystem tools change.

**Reference orgs:**
- New reference org examples beyond the three Phase 9 ships (different jurisdictions, different cohort mixes, different industries).

**Bug reports:**
- Failures of any Routine, Skill Pack, Excel formula, or installer step. Include reproduction steps and your environment (cloud or privacy; OS; tool versions).

---

## What kinds of contributions are NOT welcome

- **Vendor-specific lock-in.** ØØT is markdown-first by design; PRs that introduce dependency on a single SaaS vendor for a previously-vendor-neutral component are rejected unless the dependency is opt-in.
- **Marketing language.** The manifesto and the user guides earn their tone by being plain. PRs that introduce "leverage", "synergy", "transformation journey" or similar are rejected on style.
- **Unsourced claims.** Any number, statistic, or strong assertion needs a verifiable source. The framework runs the Klarna Test against itself; PRs that introduce unsourced claims are rejected on the same principle.
- **Patches that bypass the Klarna Test discipline** — including changes to the Klarna Test threshold, removal of the Q7 non-beneficiary review, or weakening of the audit-trail requirements. These are core governance commitments; they require an ADR plus founder sign-off.
- **Generated content presented as human-authored.** If your PR is substantially AI-authored, say so in the PR description (`Co-authored-by:` trailers in the commits are appreciated). The framework explicitly welcomes AI-augmented contributions; it does not welcome misattribution.

---

## Process

1. **For non-trivial changes**, open an issue first describing the change. Tag it `proposal` or `bug` or `documentation`.
2. **Fork the repo, create a feature branch**, make your changes.
3. **Follow the file-naming and frontmatter conventions** (see `AGENTS.md` and `CLAUDE.md`).
4. **Run the validators** (Phase 8 ships these): SKILL.md frontmatter linter, markdown linter, link checker, Excel validation.
5. **Open a PR** with a clear description. Reference the issue if you opened one.
6. **Sign your commits** if you can (GPG or SSH signing). The framework's audit-trail discipline (`governance/EU-AI-ACT.md` Article 12 mapping) prefers signed commits.
7. **Be patient** — the framework's authors review on their schedule. Substantive PRs typically get a review within 2 weeks.

---

## Initiator and founding contributors

- **Initiator:** Dr. Tali Režun — Vice Dean of Frontier Technologies at COTRUGLI Business School; founder of Lumina AI, Moj AI, Block Labs, 4thTech, Immu3, PollinationX, Online Guerrilla.
- **Founding contributors:**
  - **Dražen Kapusta** — co-author of the Cotrugli Ledger (the Generation 3 governance backbone) and originator of the institutional thesis ØØT extends.
  - **COTRUGLI Business School** — institutional anchor and EU positioning; ØØT is integrated into the MBA Frontier Technologies curriculum.

Additional collaborators are added as named contributors as they join the project, both in this file and in `README.md`.

---

## Code of conduct

This project follows the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md). Be the kind of collaborator a serious framework wants to have.

---

## Where to find help

- **GitHub Issues** — bugs, feature proposals, questions about the framework.
- **GitHub Discussions** — open conversations, design questions, ecosystem coordination.
- **The Curator project** at https://github.com/talirezun/the-curator — for Brain-specific questions; ØØT and the Curator share many concerns.

If you are a partner or founder *using* the framework and need operational help, the user guides in `docs/` are the right starting point. The walkthroughs in `docs/walkthroughs/` cover the most common day-to-day operations.

---

## Thank you

The framework's value compounds with contributions. Even small ones — a link fix, a typo correction, a citation update — make the framework's discipline easier for the next adopter. We notice; we appreciate; we attribute.
