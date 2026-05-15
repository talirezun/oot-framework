# Firm Ontology — where ØØT content lives

**This document is normative.** It defines the canonical home of every kind of ØØT content — operational state, firm IP, and personal knowledge — across the framework's three primitives. Without a shared ontology the firm becomes the "museum of broken wikilinks" the manifesto warns against.

Read this once before installing the Curator and before configuring any Routine.

---

## The three primitives (per [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md))

Every piece of firm-or-individual content lives in exactly one of three places. The split is by **who writes it** and **what it represents**:

| Primitive | Physical location | Writers | Content type | Spec |
|---|---|---|---|---|
| **Ledger** | `<firm>-ledger` GitHub repo (per firm, one) | Routines (R1–R8); partners (acks, signed commits) | Operational state — Excel `.xlsx` + Routine-authored markdown logs + Article 12 audit trail | [ADR-001](../../docs/internal/ADR-001-cloud-routine-excel-writeback.md) |
| **Firm Brain** | `<firm>-brain` GitHub repo (per firm, one) — a Curator Shared Brain | Partners pushing from personal Curator opted-in domains; admin running weekly Synthesize | Partner-contributed firm IP — theses, decisions, ADRs, partner profiles, prompts, change-management artefacts | [ADR-002](../../docs/internal/ADR-002-firm-brain-curator-shared-brain.md) |
| **Second Brain** | Each partner's local Curator vault (per partner, one) | The partner themself | Personal knowledge — including private notes that never leave the partner's machine. One opted-in domain contributes to the Firm Brain. | Curator personal docs |

**The mental model:**
- Routine-authored? → **Ledger**.
- Partner-authored knowledge, synthesized across the firm? → **Firm Brain**.
- Personal to one partner, never to be shared? → **Second Brain** only.

There is no fourth bucket. Adding one requires an ADR superseding ADR-002.

---

## Curator domain layout (personal Second Brain and the Firm Brain)

The framework recommends a small number of Curator domains in each partner's personal Second Brain. One of those domains is opted-in to contribute to the firm's Shared Brain (the Firm Brain).

| Domain | Purpose | In whose Second Brain | Opt-in to Firm Brain? |
|---|---|---|---|
| `firm` | The partner's contributions to firm-level knowledge — their take on theses, decisions, ADRs, prompts, learnings | Every partner | **Yes — this is the opted-in domain** |
| `customers` | Per-customer knowledge — interactions, contracts, deals (sensitive; usually kept personal) | Customer-facing partners | Discretionary (firm-policy decision; defaults to no) |
| `products` | Product specs, design docs, architectural notes | Product partners | Discretionary |
| `research` | External research artefacts, market intelligence | All partners | Discretionary |
| `personal` | Career notes, learning logs, journal — strictly private | Each partner, optional | **Never** |

Smaller organisations (≤5 partners) typically start with just `firm` (opted-in) + `personal` (private) and add the others when scale demands them. The framework does not prescribe more than one opted-in domain per partner — Curator's Shared Brain model assumes one contributing domain per fellow.

After running Pull, each partner sees an additional read-only domain `shared-<firm-slug>/` in their Curator — that is the synthesized mirror of the Firm Brain, written by the admin's weekly Synthesize step.

---

## Content layout — Ledger paths (Routine-authored markdown + Excel)

Lives in the `<firm>-ledger` repo. Mutated by Routines per ADR-001 (openpyxl + signed commits on protected branch). Partners read via GitHub web / IDE / a personal Curator domain that mirrors the Ledger if desired.

```
<firm>-ledger/
├── firm/
│   ├── excel/                           # All .xlsx files (X1–X9)
│   │   ├── partner-output-ledger.xlsx
│   │   ├── reward-species-declaration.xlsx
│   │   ├── business-review.xlsx
│   │   ├── klarna-test.xlsx
│   │   ├── perception-gap-survey.xlsx
│   │   ├── agent-skill-roi.xlsx
│   │   ├── audit-log-index.xlsx
│   │   ├── treasury-runway.xlsx
│   │   └── readiness-diagnostic.xlsx
│   ├── output-logs/                     # R1 daily write target
│   │   └── YYYY-MM-DD.md
│   ├── audit-logs/                      # R6 daily write target (Article 12 record)
│   │   └── YYYY-MM-DD.md
│   ├── business-reviews/                # R2 pre-meeting; facilitator post-meeting
│   │   └── YYYY-MM-DD.md
│   ├── klarna-tests/                    # R7 + S6 + affected-partner co-sign
│   │   └── KT-YYYY-NNN.md
│   ├── brain-health/                    # R5 weekly snapshot
│   │   └── YYYY-WW.md
│   ├── partners/
│   │   └── <partner_id>/
│   │       ├── variable-statements/     # R3 monthly; partner acks
│   │       │   └── YYYY-MM.md
│   │       └── long-tail-statements/    # R4 quarterly; partner acks
│   │           └── YYYY-Q<N>.md
│   └── compensation/                    # R3/R4 + founder approval; disputes
│       └── YYYY-MM/
│           ├── founder-approval.md
│           └── disputes/
│               └── <dispute_id>.md
└── .github/                             # Branch protection requires oot/klarna-test
```

**Write authority:** Routines hold the dedicated bot identity (signed commits). Partners hold their own identities for ack edits and dispute filing. Nothing else writes here.

**No path under `firm/` in the Ledger is written outside this layout** by any Routine. Adding a new operational path category requires an ADR.

---

## Content layout — Firm Brain (Curator Shared Brain `collective/<firm-domain>/wiki/`)

Lives in the `<firm>-brain` repo. Authored in partners' personal Curator opted-in domains, pushed via Curator's `DeltaSummary` protocol, synthesized weekly by the admin. Each partner sees the synthesized result as a local read-only `shared-<firm-slug>/` domain after Pull.

Curator's prescribed structure is `entities / concepts / summaries`. The framework's semantic categorization maps as follows:

```
<firm>-brain/                            # Curator Shared Brain layout
├── collective/<firm-domain>/wiki/
│   ├── index.md                         # Hand-curated firm overview; auto-rebuilt by Synthesize
│   ├── entities/                        # Things with identity
│   │   ├── partners/<partner_id>.md     # Partner profile pages (each partner authors their own)
│   │   ├── decisions/D-YYYY-NNN.md      # Non-architectural firm decisions (S5)
│   │   ├── architecture/ADR-YYYY-NNN.md # Architectural decision records (S4)
│   │   ├── pilots/<pilot_id>.md         # Change-management pilots (S6)
│   │   ├── ai-champions/<partner_id>.md # AI champion records (S6)
│   │   └── prompts/<prompt_slug>.md     # Reusable prompt artefacts (S2)
│   ├── concepts/                        # Abstract ideas + methodologies
│   │   ├── theses.md                    # Living adaptation of MANIFESTO.md to this firm
│   │   ├── methodologies.md             # Klarna Test, METR baseline, Beyond Budgeting, etc. as practised here
│   │   └── glossary.md                  # Firm-specific terminology not covered by the framework GLOSSARY
│   └── summaries/                       # Periodic syntheses
│       ├── retrospectives/<period>.md   # Quarterly / annual retros
│       └── routines-changelog.md        # Cumulative changelog of Routine adjustments
├── contributions/<fellow_id>/           # Per-partner DeltaSummary payloads (Curator-managed)
├── digests/<fellow_id>/                 # Per-partner state tracking (Curator-managed)
└── state/last-synthesis.json            # Curator-managed
```

**Write authority:** each partner Pushes their own `DeltaSummary` payloads from their personal Curator's opted-in domain. The admin runs Synthesize. No Routine writes here. Curator's MCP write tools (`compile_to_wiki`, `fix_wiki_issue`) refuse writes to the synthesized mirror — partners contribute by editing in their *personal* opted-in domain, then Pushing.

**Provenance:** every synthesized fact carries UUID Provenance attribution by default; real names appear only when both `allow_name_attribution` (org-side) and `attribute_by_name` (contributor-side) are explicitly true. Conflicts are marked with `⚠️ CONFLICTING SOURCES`.

**Adding a new path category requires** updating this ontology and, if it changes the entities/concepts/summaries taxonomy, the change must be coordinated with the Curator project.

---

## Content layout — personal Second Brain (per-partner, never shared)

Lives only on the partner's machine. Curator manages it locally. Nothing here is pushed unless it's in the opted-in domain.

```
~/curator/                               # Each partner's local Curator vault
├── firm/                                # The opted-in domain — contributes to Firm Brain
│   └── (pages the partner is authoring for firm-level synthesis)
├── personal/                            # Strictly private
│   ├── career-notes.md
│   ├── learning-logs/
│   └── journal/
├── customers/                           # Customer-facing partners only; usually private
└── shared-<firm-slug>/                  # READ-ONLY mirror of the Firm Brain — written by Pull
    └── (synthesized firm IP, copied locally for queries)
```

**Write authority:** the partner only. Curator's MCP write tools enforce the `readonly: true` frontmatter on `shared-<firm-slug>/`.

---

## Page frontmatter schema

Every Brain page in either repo carries YAML frontmatter. The minimum schema is:

```yaml
---
title: <human-readable title>
slug: <canonical slug — matches filename without extension>
domain: firm                              # the Curator domain this page belongs to
type: <page type — see below>
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors:
  - <partner_id or routine-id>
status: <draft | active | superseded | archived>
tags:
  - <free-form>
---
```

Type-specific fields layer on top. Page-type-to-location mapping:

| `type` | Lives in | Required additional fields |
|---|---|---|
| `output-log` | Ledger | `date` |
| `audit-log` | Ledger | `date`, `entries_count`, `anomalies_flagged` |
| `business-review` | Ledger | `week_starting`, `attendees`, `decisions_logged` |
| `klarna-test` | Ledger | `test_id`, `decision`, `score`, `pr_url`, `affected_partners`, `non_beneficiary_reviewer`, `review_date_90d` |
| `variable-statement` | Ledger | `partner_id`, `month`, `total_compensation`, `ack_status` |
| `long-tail-statement` | Ledger | `partner_id`, `quarter`, `total_payment` |
| `brain-health` | Ledger | `week_starting`, `health_score` |
| `dispute` | Ledger | `dispute_id`, `tier`, `raised_by`, `against`, `status` |
| `partner-profile` | Firm Brain | `partner_id`, `cohort`, `start_date`, `jurisdiction`, `two_worlds_self_id` |
| `output-spec` | Firm Brain | `partner_id`, `value_tier`, `expected_outcome`, `outcome_review_date` |
| `reward-species-declaration` | Firm Brain (summary page; operative truth in Ledger X2) | `partner_id`, `signed_date`, `pdf_link`, `reward_species` |
| `decision` | Firm Brain | `decision_id`, `accountable`, `consulted`, `reversal_threshold` |
| `adr` | Firm Brain | `adr_id`, `status_chain`, `superseded_by` |
| `pilot` | Firm Brain | `pilot_id`, `start_date`, `end_date`, `cohort_partner_ids`, `status` |
| `prompt` | Firm Brain | `prompt_id`, `version`, `intended_skill_pack`, `input_signature`, `output_signature` |
| `thesis`, `methodology`, `summary` | Firm Brain | (free-form; status + tags sufficient) |

---

## Wikilink discipline

The Curator's wikilink syntax (`[[slug]]`) is the only canonical cross-reference mechanism inside the Firm Brain and within each partner's personal Curator. **Cross-repo wikilinks between the Ledger and the Firm Brain are not supported by Curator** — when a Firm Brain page references a Ledger artefact (e.g., a variable statement, a Klarna test row), use a relative path or full GitHub URL into the Ledger repo.

Rules every writer must follow:

1. **Every wikilink must resolve.** Never write `[[partners/jane-doe]]` if no page at that slug exists. If you intend to reference something that doesn't exist yet, create the stub first.
2. **Slugs are stable; titles can move.** Renaming a slug breaks every backlink. Curator's deprecation flow (mark old slug `status: superseded`, add `superseded_by`, leave the page in place) is the migration path.
3. **Cross-domain wikilinks use the domain prefix.** From the opted-in `firm` domain, reference a customer page as `[[customers/acme-corp]]` only if `customers` is also opted-in to the Firm Brain. Otherwise, treat the customer reference as personal-only and avoid the wikilink.
4. **The `personal/` domain is a dead-end.** No wikilinks leave it. Its content is not allowed to leak references into shared knowledge.
5. **Synthesized mirror pages (`shared-<firm-slug>/`) carry resolved wikilinks** — Curator's synthesis pipeline rewrites cross-contributor references at synthesize time. Partners do not edit the mirror.
6. **Routines that write Ledger pages always use `slug:` from frontmatter as the canonical name** — never construct slugs from titles at write time.

---

## Permissions

Curator's per-domain ACL configuration handles personal Second Brain and Firm Brain access. Ledger access is GitHub's collaborator + branch-protection model.

| Path | Repo | Read permission | Write permission |
|---|---|---|---|
| Firm Brain `entities/partners/<id>.md` | Firm Brain | All synthesized-mirror readers (i.e., all partners after Pull) | The partner themself, via Push from their personal Curator |
| Firm Brain `concepts/theses.md` | Firm Brain | All partners (via mirror) | Any partner via Push; conflicts resolved at Synthesize |
| Firm Brain `entities/decisions/*`, `entities/architecture/*` | Firm Brain | All partners (via mirror) | The Accountable per the decision-rights matrix, via Push |
| Firm Brain `entities/prompts/*` | Firm Brain | All partners (via mirror) | Any partner via Push |
| Ledger `firm/output-logs/*` | Ledger | All partners | R1 only (append-only, signed commits) |
| Ledger `firm/audit-logs/*` | Ledger | All partners + counsel + auditors | R6 only (append-only, signed commits, branch protection) |
| Ledger `firm/klarna-tests/*` | Ledger | All partners | R7 + S6; affected partners co-sign |
| Ledger `firm/business-reviews/*` | Ledger | All partners | R2 + facilitator (post-meeting) |
| Ledger `firm/partners/<id>/variable-statements/*` | Ledger | The partner + founders | R3 only (humans co-sign by editing the ack block) |
| Ledger `firm/partners/<id>/long-tail-statements/*` | Ledger | The partner + founders | R4 only |
| Ledger `firm/compensation/*` | Ledger | Founders + the affected partner | R3/R4 + founders |
| Personal `~/curator/personal/*` | Local Second Brain only | The partner only | The partner only |
| Mirror `~/curator/shared-<firm-slug>/*` | Local mirror of Firm Brain | The partner | Curator's Pull step only (read-only via MCP) |

The Curator MCP server's per-domain ACL configuration enforces Firm Brain + personal-Second-Brain permissions. The cloud and privacy installers ship the recommended ACL above. The Ledger's GitHub repo settings enforce its permissions.

---

## Sequence diagram — how a new firm decision propagates

```
1. Partner A authors `entities/decisions/D-2026-005.md` in their personal Curator's `firm` domain.
2. Partner A runs Push:
   - Curator preprocesses the page into a DeltaSummary JSON.
   - Curator uploads to <firm>-brain/contributions/<A_uuid>/<submission_id>.json.
3. Other partners' Push runs may add commentary or counterpoint to the same slug.
4. Admin (weekly) runs Synthesize:
   - Reads all new contributions to D-2026-005.
   - Applies union-merge for compatible facts; Jaccard similarity flags contradictions;
     selective LLM resolves contradictions or marks ⚠️ CONFLICTING SOURCES.
   - Writes synthesized page to collective/<firm-domain>/wiki/entities/decisions/D-2026-005.md.
   - Appends Provenance block (UUIDs by default; names only if double-flagged).
5. Each partner runs Pull:
   - Curator downloads collective pages.
   - Each partner's local shared-<firm-slug>/ domain mirrors the synthesized result.
6. Routines that need decision context (e.g., R5 weekly reporting, R2 BR pre-fill) clone the Firm Brain repo
   and read collective/<firm-domain>/wiki/entities/decisions/ directly.
```

---

## When this ontology evolves

Every change to this document is recorded as a `decisions/` entity in the Firm Brain (one ADR per ontology change). The framework's authors will accept upstream PRs to this template; firm-level customisations stay in the firm's own copy.

The pre-1.0.1 ontology is intentionally conservative: a small number of clearly-purposed paths, no deeply-nested hierarchies, no per-project domains. Larger organisations will outgrow it; the moment they do, scaling to multiple opted-in domains (per the table at the top of this document) becomes warranted.
