# Skill Pack S1 — My Curator: SPEC

**ID:** S1
**Name:** My Curator
**Tier:** 1
**Status:** Hardened in v1.0 (imported)
**Maintainer:** Dr. Tali Režun

## Purpose

The canonical Brain Skill Pack of the ØØT framework. Operationalises Curator-MCP-driven knowledge management: ingest, query, write, scan, and graph navigation. Every other Skill Pack writes into the Brain via this pack's discipline.

## Special handling — DO NOT GENERATE FROM SCRATCH

S1 is **imported verbatim** from the canonical Curator repository:

- Source: `https://github.com/talirezun/the-curator/blob/main/claude-skills/my-curator/SKILL.md`
- License: per the Curator project's licensing terms (also CC-BY-compatible)

Claude Code's task is to:

1. Fetch the canonical `SKILL.md` from the URL above.
2. Save it as `skills/my-curator/SKILL.md`.
3. Prepend an ØØT-specific preamble (see below) at the top.
4. Do not modify the substantive content of the imported skill.

## ØØT-specific preamble (prepend to imported SKILL.md)

The preamble has two parts: (1) extra YAML frontmatter keys merged into the imported SKILL.md's existing frontmatter; (2) a short ØØT-specific prose preface that sits between the closing `---` of the frontmatter and the imported skill's first heading.

### Frontmatter additions (merge into the imported SKILL.md's frontmatter)

```yaml
oot_pack_id: S1
oot_tier: 1
oot_status: hardened
oot_dependencies: []
oot_provides_to: [S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12]
oot_klarna_test: false
last_updated: 2026-05-08
```

### Prose preface (insert immediately after the frontmatter, before the imported skill's body)

```markdown
# ØØT Skill Pack S1 — My Curator (Canonical Brain Skill Pack)

This is the canonical Brain Skill Pack of the ØØT framework. It is imported verbatim from `talirezun/the-curator` and is the single source of truth for Brain operations across all twelve ØØT Skill Packs.

**For ØØT adopters:** every other Skill Pack assumes this one is installed and operational. Install S1 first, run the Curator self-test, and verify your domain structure before installing any other pack.

**For maintainers:** do not modify this file directly. Updates flow from the upstream Curator project. To customise Brain behaviour for your firm, layer additional instructions in your firm's `CLAUDE.md` or project-level documentation, never in this `SKILL.md`.

[The imported canonical content begins below.]
```

## Acceptance criteria

- File exists at `skills/my-curator/SKILL.md`.
- Preamble matches the template above (with current `last_updated`).
- The body is the canonical Curator SKILL.md, unmodified.
- `examples/` contains 2 worked examples specific to ØØT use:
  - **Example 1:** Ingesting a partner Output Spec into the firm's `firm` domain.
  - **Example 2:** Cross-domain query — finding all references to a customer across `firm`, `customers`, `legal` domains.
- `references/` lists the Curator project, the original Karpathy "second brain" framing, the SECI model (Nonaka & Takeuchi), GraphRAG (Microsoft Edge et al. 2024).

## References

1. The Curator project: `https://github.com/talirezun/the-curator`.
2. Karpathy, A. *The second brain* (Twitter thread / blog, 2023).
3. Nonaka, I. & Takeuchi, H. *The Knowledge-Creating Company* (1995). The SECI model.
4. Edge, D. et al. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* (Microsoft Research, 2024).
5. ØØT `MANIFESTO.md`, Thesis 4 — The Collecting Brain.