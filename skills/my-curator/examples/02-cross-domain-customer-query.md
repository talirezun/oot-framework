# Example 2 — Cross-domain query: finding all references to a customer

A worked example of using S1 to surface every Brain reference to a single customer across multiple domains (`firm`, `customers`, `legal`) without violating the per-domain siloing model.

## Context

The firm's quarterly business review is approaching. The founder wants to ask: *"Show me every interaction, decision, contract, output spec, and audit-log entry related to Acme Corp across the past quarter."* Acme Corp data is naturally fragmented:

- `customers/acme-corp/*` — interactions, deals, contracts.
- `firm/output-logs/*` — outputs that landed for Acme.
- `firm/decisions/*` — decisions that mentioned Acme.
- `firm/klarna-tests/*` — any test that touched Acme work.
- `legal/contracts/*` — signed contracts.

The siloing model means each of these domains is its own knowledge graph. A wikilink from `firm/` to `[[customers/acme-corp]]` is a *cross-domain reference* (which the framework supports for *reasoning*) but not a wikilink-resolved relation (which only works within a single domain).

## Step-by-step

### 1. Confirm domains in scope

```
mcp__my-curator__list_domains
```

Returns: `firm`, `customers`, `legal`, `products`, `research`. The query crosses 4 of these.

### 2. Run the cross-domain search

```
mcp__my-curator__search_cross_domain query="Acme Corp" domains=["firm","customers","legal","products"] since="2026-01-01"
```

Returns a structured response: per-domain hit counts + the top N results per domain ranked by relevance.

### 3. Drill into each domain's hits

For each domain, the skill calls `get_node` on the highest-relevance pages:

```
mcp__my-curator__get_node domain=customers slug=acme-corp
mcp__my-curator__get_connected_nodes domain=customers slug=acme-corp depth=1
```

In `customers/`, this surfaces:
- The customer profile page.
- Every interaction page in `customers/acme-corp/interactions/`.
- The deal-tracking page.

In `firm/`:
- Output-log entries mentioning Acme.
- Decision records D-2026-NN-NNN that referenced Acme.
- The Klarna Test KT-2026-002 (the held-then-passed test about automating Acme's customer-onboarding contract review).

In `legal/`:
- The signed master services agreement (contract page).
- The Q1 amendment.

### 4. Compose a Brain summary page (the meta-output)

```
mcp__my-curator__compile_to_wiki domain=firm slug=business-reviews/quarterly-prep/acme-corp-q1-2026 type="freeform"
```

The summary page wikilinks back to each source domain page using cross-domain link syntax (`[[customers/acme-corp]]`, `[[legal/contracts/acme-msa]]`). It does NOT collapse the data into one place — the original pages remain canonical; the summary is a navigation page.

### 5. Verify

```
mcp__my-curator__scan_wiki_health domain=firm
```

Confirms the summary page has no broken wikilinks.

```
mcp__my-curator__get_backlinks domain=customers slug=acme-corp
```

Now shows the new firm summary page as a backlink — the founder can navigate from any direction.

## Output

A composite navigation page at `firm/business-reviews/quarterly-prep/acme-corp-q1-2026.md` that:
- Lists every Acme-related Brain page across 4 domains.
- Shows the cross-domain relationships clearly.
- Stays inside the framework's siloing rules (no inappropriate same-domain wikilinks, no cross-domain wikilink resolution).
- Becomes the founder's pre-read for the quarterly review.

## Anti-patterns this example avoids

- **Trying to merge customer data into the `firm/` domain** — would violate the siloing model and create duplicate sources of truth.
- **Pasting page content into a chat instead of querying** — produces a snapshot that's stale the moment a new interaction lands.
- **Speculative wikilinks across domains** — the skill refuses; cross-domain *reasoning* yes, cross-domain *linking* no.
