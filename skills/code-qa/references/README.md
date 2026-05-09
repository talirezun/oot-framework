# References — Skill Pack S4 (Code & QA)

The intellectual and technical foundations of the framework's coding discipline.

## Primary sources

1. **Karpathy, A.** *Software 3.0* (Sequoia AI Ascent 2026). The framing of human-AI division of labour the pack rests on. https://karpathy.bearblog.dev/sequoia-ascent-2026/

2. **Anthropic.** *CLAUDE.md and AGENTS.md conventions documentation.* https://docs.claude.com/en/docs/claude-code/

3. **Dr. Tali Režun.** *Three Philosophies, One Goal: Augment Code, Claude Code, Codex CLI* (Medium, April 2026). The selection rubric the pack adopts.

## Empirical evidence base

4. **Forsgren, N., Humble, J., Kim, G.** *Accelerate: The Science of Lean Software and DevOps* (IT Revolution Press, 2018). The DORA metrics foundation.

5. **DORA Report 2025: State of AI-Assisted Software Development.** https://dora.dev/dora-report-2025/. The "mirror and multiplier" framing that AI assistance amplifies whatever's already there — informs the §4.0 setup pre-requisites.

6. **METR.** *RCT on AI tools and developer productivity* (July 2025) and February 2026 follow-up. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/. The perception-gap study — basis for the Plan Mode discipline (humans are unreliable self-evaluators of AI-assisted productivity without baseline measurement).

7. **Dell'Acqua, F., Kellogg, K., et al.** *The Cybernetic Teammate* (HBS Working Paper 25-043, 2025). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5188231. The P&G field-experiment showing AI-augmented individuals match human teams.

## Adjacent open-source

8. **aider** — open-source pair-programming with LLMs. https://github.com/paul-gauthier/aider. Influenced the parallel-session pattern.

9. **Continue.dev** — open-source agentic IDE. https://continue.dev/. Reference for the Three Philosophies' privacy-track Open Codex equivalent.

10. **Cody (Sourcegraph), GitHub Copilot, Cursor.** — the broader agentic-coding ecosystem the framework's tools sit alongside; included for cross-reference but not specifically endorsed by ØØT.

## Standards / governance

11. **Conventional Commits** — https://www.conventionalcommits.org/. The commit-message convention the `Co-authored-by:` discipline composes with.

12. **`Co-authored-by:` trailer** — git documentation. https://git-scm.com/docs/git-interpret-trailers. The framework's AI-authorship attribution mechanism.

13. **GitHub branch protection rules.** https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches. The five §4.0 pre-requisites configure here.

## Cross-references inside ØØT

- ØØT [`governance/KLARNA-TEST.md`](../../../governance/KLARNA-TEST.md) — the gate this pack wires.
- ØØT [`governance/EU-AI-ACT.md`](../../../governance/EU-AI-ACT.md) — Article 12 audit retention depends on the §4.0 branch protections.
- ØØT [`governance/SECRETS-POLICY.md`](../../../governance/SECRETS-POLICY.md) — the secrets discipline this pack enforces.
- ØØT [`templates/brain/SPEC.md`](../../../templates/brain/SPEC.md) `adr.md`, `decision-record.md` templates.
- ØØT Skill Pack S6 — Change Management (METR baseline integration).
- ØØT Skill Pack S3 — Compensation & Attribution (output capture integration).
