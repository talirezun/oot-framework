# Example 1 — Ingesting a partner Output Spec into the firm domain

A worked example of using S1 (My Curator) to add a partner's Output Spec to the firm Brain in a way that integrates cleanly with the existing knowledge graph and the framework's slug conventions.

## Context

A new partner, Mira, has just drafted an Output Spec for a feature she's about to ship: an OAuth2 PKCE flow for partner onboarding. The spec is currently a markdown draft in her local editor. She wants it ingested into the firm's Brain so that:
- The variable-pay Routine (R1) can reference it tomorrow when it captures her commits.
- Other partners can find and link to it.
- Any future Klarna Test referencing onboarding can wikilink to it cleanly.

## Step-by-step

### 1. Orient on the wiki first (always)

Before any write, the skill's discipline is to orient. Mira asks Claude:

> Use my-curator. List the firm domain's index, focusing on the partners/mira-tek/output-specs slug.

Expected first move: `mcp__my-curator__list_domains` confirms `firm` exists; then `mcp__my-curator__get_index` for `firm` confirms the existing structure under `partners/mira-tek/`.

### 2. Verify the slug doesn't already exist

```
mcp__my-curator__search_wiki domain=firm query="OAuth2 PKCE onboarding"
```

If a prior spec with overlapping scope exists (e.g., a previous OAuth1 spec from 6 months ago), the skill's discipline is to either:
- **Compound into the existing page** (preferred) by adding a new section.
- **Supersede the prior page** explicitly with frontmatter `superseded_by: <new-slug>` on the old, `supersedes: <old-slug>` on the new.

Mira confirms there is no overlapping page.

### 3. Compose the page following `templates/brain/output-spec.md`

Mira hands Claude the draft and says:

> Compile this into a new Brain page at `firm/partners/mira-tek/output-specs/2026-05-08--oauth2-pkce`. Follow `templates/brain/output-spec.md`. Wikilink to my profile and to the architecture-decisions domain.

The skill's behaviour:
- Verifies `[[partners/mira-tek]]` exists (it does — Mira's profile page).
- Refuses speculative wikilinks. If Mira's draft mentions `[[architecture/auth-rewrite-2026]]` but no such page exists yet, the skill flags this and asks Mira whether to (a) create the architecture stub first, (b) drop the wikilink, or (c) defer until the ADR lands.
- Composes the page with the canonical frontmatter (per `templates/brain/SPEC.md` `output-spec` type).
- Calls `mcp__my-curator__compile_to_wiki` to write the page atomically.

### 4. Verify the write

```
mcp__my-curator__get_node domain=firm slug=partners/mira-tek/output-specs/2026-05-08--oauth2-pkce
```

Confirms the page exists, frontmatter is correct, body is well-formed.

```
mcp__my-curator__scan_wiki_health domain=firm
```

Confirms no new broken wikilinks were introduced.

### 5. Cross-link

Mira's profile page at `firm/partners/mira-tek/profile.md` has a `## Recent output specs` section. The skill appends the new wikilink there.

```
mcp__my-curator__get_backlinks domain=firm slug=partners/mira-tek
```

Confirms the new spec page now backlinks to Mira's profile.

## Output

A new Brain page at `firm/partners/mira-tek/output-specs/2026-05-08--oauth2-pkce.md` with full provenance, no broken wikilinks, integrated into the firm's existing knowledge graph. R1 will pick it up tomorrow when it captures Mira's first OAuth-related commit.

## Anti-patterns this example avoids

- **Pasting the draft into a chat without using the skill** — produces a wiki page that doesn't follow the slug convention and may have hallucinated wikilinks.
- **Skipping the orient-first discipline** — produces a page in the wrong slug or with a name collision.
- **Writing a wikilink to a non-existent target page** — produces a broken-link issue R5 (Brain Health Check) will flag the next Sunday; better to catch at write time.
