# Brain Ontology — the `firm/` namespace

**This document is normative.** Every ØØT Skill Pack and every ØØT Routine writes Brain pages under the `firm/` domain following the slug structure, frontmatter schema, and wikilink discipline specified here. Without a shared ontology, the Brain becomes the "museum of broken wikilinks" the manifesto warns against.

Read this once before installing the Curator and before configuring any Routine. The Curator's `list_domains` will show `firm` (and any custom domains you add); this document specifies the canonical *folder structure inside* `firm/` and the rules for cross-references.

---

## Domain layout

The framework recommends six top-level Curator domains for a typical adopting organisation:

| Domain | Purpose | Primary writers | Visibility |
|---|---|---|---|
| `firm` | Internal company knowledge — the operational substrate | Every Skill Pack; Routines R1–R8 | Founders + partners |
| `customers` | Per-customer knowledge — interactions, contracts, deals | S11 (Sales & BD); S3 (when sales output lands) | Founders + customer-facing partners |
| `products` | Product specs, design docs, architectural decisions | S4 (Code & QA); founders | Founders + product partners |
| `legal` | Counsel-touched documents, contract repository, compliance evidence | S8 (Legal Operations); S7 (Governance) | Founders + counsel; tightly scoped |
| `research` | External research artefacts, market intelligence, competitor notes | S2 (Context Engineering writes prompt artefacts here); S9 (Marketing) | All partners |
| `partners` | Reserved domain for per-partner private knowledge — career notes, learning logs | The partner themself only | Per-partner private |

Smaller organisations (≤5 partners) can collapse to just `firm` + `customers` + `legal` for the first 90 days; add the others when scale demands them. Larger organisations may add domain-specific siblings (e.g., `regulated`, `m&a`, `trust-and-safety`) — keep the count under ten total.

The remainder of this document specifies the structure **inside `firm/`**, since that is where the framework's Routines and Skill Packs all converge.

---

## The `firm/` folder structure

Every path below is a slug under the `firm` Curator domain. Routines write to these paths automatically; partners can navigate them manually.

```
firm/
├── index.md                          # Hand-curated firm overview (founder authors)
├── theses.md                         # Living adaptation of MANIFESTO.md to your firm
├── partners/
│   ├── index.md                      # Roster + cohort designations + active reward species
│   └── <partner_id>/
│       ├── profile.md                # Identity, contact, jurisdiction, two-worlds-of-code declaration
│       ├── reward-species-declaration.md  # Wikilink to the X2 row + signed PDF; renegotiations log
│       ├── output-specs/             # One markdown page per Output Spec
│       │   └── YYYY-MM-DD--<slug>.md
│       ├── variable-statements/      # Monthly statements written by R3
│       │   └── YYYY-MM.md
│       ├── long-tail-statements/     # Quarterly statements written by R4
│       │   └── YYYY-Q<N>.md
│       └── private/                  # Ignored by all Routines except the owning partner; per-partner permissioned
├── output-logs/                      # Daily write target for R1
│   └── YYYY-MM-DD.md
├── business-reviews/                 # Friday BR summaries committed by R2
│   └── YYYY-MM-DD.md
├── klarna-tests/                     # One page per Klarna Test entry, written by R7 + S6
│   └── KT-YYYY-NNN.md
├── audit-logs/                       # Article 12 audit trail, written daily by R6
│   └── YYYY-MM-DD.md
├── compensation/                     # Founder-approval packets, dispute records
│   └── YYYY-MM/
│       ├── founder-approval.md
│       └── disputes/
│           └── <dispute_id>.md
├── change/                           # Change-management artefacts (S6)
│   ├── pilots/
│   │   └── <pilot_id>.md
│   ├── ai-champions/
│   │   └── <partner_id>.md
│   └── plateau-plan.md
├── brain-health/                     # Weekly snapshot from R5
│   └── YYYY-WW.md
├── routines/                         # Per-Routine setup notes + changelog
│   ├── changelog.md
│   ├── R1.md … R8.md
│   └── privacy-track-overrides.md
├── privacy-track/                    # Setup, migration logs, hardware register (S12)
│   ├── always-on-machine.md
│   ├── per-partner-trezor.md
│   └── migration-runbook.md
├── prompts/                          # S2 — reusable, versioned prompt artefacts
│   └── <prompt_slug>.md
├── decisions/                        # Versioned decision records (D-YYYY-NNN)
│   └── D-YYYY-NNN.md
└── architecture/                     # Architectural decision records from S4
    └── ADR-YYYY-NNN.md
```

**No path under `firm/` is ever modified outside this layout** by any Routine or Skill Pack. Adding a new path category requires updating this ontology document and committing the change as a `firm/decisions/` ADR.

---

## Page frontmatter schema

Every Brain page in `firm/` carries YAML frontmatter. The minimum schema is:

```yaml
---
title: <human-readable title>
slug: <canonical slug — matches filename without extension>
domain: firm
type: <one of: index | output-log | output-spec | variable-statement | long-tail-statement | klarna-test | audit-log | business-review | decision | adr | pilot | ai-champion | brain-health | routine-doc | partner-profile | reward-species-declaration | dispute | prompt | freeform>
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors:
  - <partner_id or routine-id>
status: <one of: draft | active | superseded | archived>
tags:
  - <free-form>
---
```

Type-specific fields layer on top. The most important ones:

| `type` | Required additional fields |
|---|---|
| `output-log` | `date` (the YYYY-MM-DD covered) |
| `output-spec` | `partner_id`, `value_tier` (S/M/L/XS), `expected_outcome` (free text), `outcome_review_date` |
| `variable-statement` | `partner_id`, `month` (YYYY-MM), `total_compensation`, `ack_status` (one of: pending / reviewed / disputed / unresponsive) |
| `long-tail-statement` | `partner_id`, `quarter` (YYYY-Q<N>), `total_payment` |
| `klarna-test` | `test_id` (KT-YYYY-NNN), `decision`, `score`, `pr_url`, `affected_partners`, `non_beneficiary_reviewer`, `review_date_90d` |
| `audit-log` | `date`, `entries_count`, `anomalies_flagged` (Yes/No) |
| `business-review` | `week_starting`, `attendees`, `decisions_logged` |
| `decision` | `decision_id` (D-YYYY-NNN), `accountable`, `consulted` (list), `reversal_threshold` (free text or "irreversible") |
| `adr` | `adr_id` (ADR-YYYY-NNN), `status_chain` (proposed → accepted → superseded), `superseded_by` |
| `pilot` | `pilot_id`, `start_date`, `end_date`, `cohort_partner_ids` (list), `status` |
| `partner-profile` | `partner_id`, `cohort`, `start_date`, `jurisdiction`, `two_worlds_self_id` |
| `reward-species-declaration` | `partner_id`, `signed_date`, `pdf_link`, `reward_species` |
| `dispute` | `dispute_id`, `tier` (1/2/3), `raised_by`, `against`, `status` |
| `prompt` | `prompt_id`, `version` (semver), `intended_skill_pack`, `input_signature`, `output_signature` |

---

## Wikilink discipline

The Curator's wikilink syntax (`[[slug]]`) is the only canonical cross-reference mechanism inside the Brain. A few rules every writer (human or Routine) must follow:

1. **Every wikilink must resolve.** Never write `[[partners/jane-doe]]` if no page at that slug exists. If you intend to reference something that doesn't exist yet, create the stub first (one-line page with `status: stub`) and link to it.
2. **Slugs are stable; titles can move.** Renaming a slug breaks every backlink. The Curator MCP's `fix_wiki_issue` is for typo correction, not for restructuring. If you must rename, use the Curator's deprecation flow (mark old slug `status: superseded`, add `superseded_by` frontmatter, leave the page in place).
3. **Cross-domain wikilinks use the domain prefix.** From `firm/`, link to a customer page as `[[customers/acme-corp]]`. The Curator's `search_cross_domain` exposes these.
4. **No wikilinks from `partners/<id>/private/` to other domains.** Private pages are intentionally dead-ends; their content is not allowed to leak references back into shared knowledge.
5. **Routines that write Brain pages always use `slug:` from frontmatter as the canonical name** — never construct slugs from titles at write time. Titles are mutable display strings; slugs are immutable identifiers.

---

## Permissions

Curator's per-page permissions are honoured by the Skills and Routines:

| Path pattern | Read permission | Write permission |
|---|---|---|
| `firm/index.md`, `firm/theses.md` | All partners | Founders only |
| `firm/partners/<id>/profile.md` | All partners | The partner + founders |
| `firm/partners/<id>/reward-species-declaration.md` | The partner + founders | Founders + the partner (via signed renegotiation) |
| `firm/partners/<id>/variable-statements/*` | The partner + founders | R3 only (humans co-sign by editing the ack block) |
| `firm/partners/<id>/long-tail-statements/*` | The partner + founders | R4 only |
| `firm/partners/<id>/private/*` | The partner only | The partner only |
| `firm/output-logs/*` | All partners | R1 only (append-only) |
| `firm/audit-logs/*` | All partners + counsel + auditors | R6 only (append-only); requires signed commits + branch protection |
| `firm/klarna-tests/*` | All partners | R7 + S6; the affected partners co-sign |
| `firm/business-reviews/*` | All partners | R2 + facilitator (post-meeting) |
| `firm/compensation/*` | Founders + the affected partner | R3/R4 + founders |
| `firm/decisions/*` | All partners | The Accountable per the matrix; logged via S5 |
| `firm/architecture/*` | All partners | S4; partners with merge authority |
| `firm/prompts/*` | All partners | Any partner via S2 |

Implementation detail: Curator permissions are enforced by the Curator MCP server's per-domain ACL configuration. The cloud installer ships the recommended ACL per the table above; founders can tighten. Privacy-track Curator instances inherit the same ACL via the same MCP config.

---

## When this ontology evolves

Every change to this document is a `firm/decisions/` ADR. The framework's authors will accept upstream PRs to this template; firm-level customisations stay in the firm's own copy.

The pre-1.0 ontology is intentionally conservative: a small number of clearly-purposed paths, no deeply-nested hierarchies, no per-project domains. Larger organisations will outgrow it; that is the point at which scaling to multiple domains (per the table at the top of this document) becomes warranted.
