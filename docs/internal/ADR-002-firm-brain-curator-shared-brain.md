# ADR-002 — The Firm Brain is a Curator Shared Brain, distinct from the Ledger

**Status:** Accepted
**Date:** 2026-05-15
**Decision-makers:** Dr. Tali Režun (initiator), Claude Code (drafting)
**Relates to:** ADR-001 (Ledger writeback via openpyxl + signed commits) — unchanged.
**Triggers:** The Curator v3.0.0-beta.1 release (May 2026) introduces a first-class *Shared Brain* primitive that supersedes the framework's hand-rolled "firm Brain repo" model.

---

## Context

Before v1.0, the framework used a single concept — "the firm Brain" — to cover two distinct things:

1. **Operational state** — the firm's Excel ledgers, audit logs, output logs. Mutated by Routines. Per [ADR-001](ADR-001-cloud-routine-excel-writeback.md), this lives in the firm's GitHub repo and is written via openpyxl + signed commits on a protected branch. We retroactively named this layer the **Ledger** (commits `27e0afa`, `aa739cc`, `c59595e`).

2. **Knowledge / firm IP** — the synthesized organisational memory: decision rationales, partner contributions, market intelligence, the things that make this firm *this firm*. In v1.0 this was a folder structure inside the same Brain repo, authored directly by partners in markdown. Provenance was carried by signed commits; conflict resolution was manual; GDPR Article 17 erasure was a hand-rolled procedure ([governance/EU-AI-ACT.md](../../governance/EU-AI-ACT.md), [skills/privacy-self-sovereign/SKILL.md](../../skills/privacy-self-sovereign/SKILL.md)).

The [Curator v3.0.0-beta Shared Brain feature](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md) now provides layer 2 as a first-class primitive: opted-in personal domains push `DeltaSummary` payloads to a shared GitHub repo, weekly synthesis merges them into a `collective/<domain>/wiki/` tree with UUID-pseudonymous Provenance attribution, and an admin revoke endpoint covers Article 17 with a typed-confirmation safety gate.

This is a strictly better substrate for layer 2 than the hand-rolled markdown repo, and it changes how the framework should describe its own architecture.

## Decision

**Treat the Firm Brain and the Ledger as two separate primitives, in two separate GitHub repositories, with two different write models. Retire the per-partner `<firm>-secondbrain` repo as a framework concept.**

| Primitive | Repo (per firm) | Writers | Write mechanism | Spec source |
|---|---|---|---|---|
| **Ledger** | `<firm>-ledger` | Routines, founder (manual) | openpyxl + signed commits on protected `main` | [ADR-001](ADR-001-cloud-routine-excel-writeback.md), [templates/excel/SPEC.md](../../templates/excel/SPEC.md), [routines/SPEC.md](../../routines/SPEC.md) |
| **Firm Brain** | `<firm>-brain` | Partners (via Push from personal Curator), admin (via Synthesize) | Curator Shared Brain v3.0.0-beta protocol | Curator's [shared-brain.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md) + [shared-brain-design.md](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-design.md) |

The two repos coexist; nothing in this ADR changes ADR-001 or the Ledger.

### Retiring the per-partner `<firm>-secondbrain` repo

Pre-v1.0.1 the framework provisioned a third repo per partner — `<firm>-secondbrain` — to which the partner synced their *entire* Curator vault (all domains together). Cloud Routines read from this repo, scoped to `wiki/<firm-curator-domain>/`, to get company-context knowledge that cloud-hosted compute could not reach via a local my-curator MCP.

That pattern is **retired as a framework concept** in v1.0.1. Three reasons:

1. **Privacy.** It pushes a partner's *entire* vault — non-firm domains included — into a firm-named GitHub repo. Even with read-scoping at the Routine level, the non-firm content is physically present in firm infrastructure. The Shared Brain protocol only pushes the *opted-in domain's* preprocessed `DeltaSummary` payloads, which is strictly less data leakage.
2. **No canonical firm context.** Each partner had their own copy of `wiki/<firm-curator-domain>/` with no merge layer; Routines had to pick one or stitch by convention. The Firm Brain's `collective/<firm-domain>/wiki/` is synthesized across all partners with UUID Provenance and conflict markers — that is the canonical surface Routines should target.
3. **Wizard surface area.** Provisioning N+2 repos (Ledger + Firm Brain + one secondbrain per partner) is materially worse onboarding than provisioning 2 firm repos. Personal Curator backup-to-GitHub is a *personal-tooling* choice (Curator's built-in two-way sync handles it independently); it does not belong in the firm wizard.

**Post-v1.0.1 framework provisions exactly two firm repos: `<firm>-ledger` and `<firm>-brain`.** Cloud Routines that need firm context read `collective/<firm-domain>/wiki/` in the Firm Brain repo. Partners who want a personal backup of their Second Brain configure Curator's personal Sync feature independently — it is not framework-orchestrated.

**Migration for existing v1.0 installs:** no forced action. Existing `<firm>-secondbrain` repos can stay (as personal backup), be archived, or be deleted at the firm's discretion. Routines that previously read `<firm>-secondbrain` are updated in [routines/SPEC.md](../../routines/SPEC.md) to read the Firm Brain instead; the v1.0.1 release notes carry a one-paragraph migration note.

### Concretely

1. **The Firm Brain is a Curator Shared Brain instance.** The admin (typically the founding partner) creates a private GitHub repo, runs the Curator admin wizard, generates an `sbi_…` invite token, and distributes it to each partner. Each partner accepts a GitHub collaborator invite, creates a fine-grained PAT, picks which of their personal Curator domains to opt in, and consents to the IP-mode terms.

2. **Each partner keeps their own personal Curator instance on their own machine.** They author and edit pages in their personal domains via MCP from any LLM they choose — Claude Desktop / Claude Code / a local LM Studio model on the privacy track / Cursor / any other Curator-MCP-aware client. Their personal Brain is not affected by Shared Brain installation; only the opted-in domain participates in Push.

3. **The `collective/<domain>/wiki/` tree in the Firm Brain repo is the firm's synthesized organisational memory.** Each partner sees it locally as a sibling read-only domain (`shared-<slug>/`) after running Pull. To contribute new knowledge, a partner edits in their *personal* opted-in domain and runs Push. To contribute corrections, same path. **The brain as a whole is writable; only the synthesized mirror is read-only by design.**

4. **Synthesis is weekly, admin-run.** Reads new contributions since the last run, applies Curator's Jaccard + selective-LLM merge rules, writes synthesized pages with Provenance markers, rebuilds `collective/index.md`. Cost per Curator's own measurement: under $0.01 per weekly run for a 100-page brain with 5 contributors.

5. **The IP mode default for ØØT firms is `organisational`** — partners assign IP to the operating LLC per their partner charter, which is the standard ØØT assumption. Advisors, contractors, and outside collaborators connect in `contributor_retains` mode. **Both flags `allow_name_attribution` (org-side) and `attribute_by_name` (contributor-side) default to `false`** — UUID-pseudonymous attribution is the safe baseline; surface real names only when both sides explicitly opt in.

6. **The framework's R3 partner acknowledgement discipline ([CLAUDE.md decision #5](../../CLAUDE.md)) is preserved unchanged.** R3 is a Routine; Routines write to the Ledger (per ADR-001). The variable-statement markdown page lives at `firm/partners/<id>/variable-statements/YYYY-MM.md` in the **Ledger** repo, alongside the `.xlsx` mutations R3 also makes. The partner acknowledges by editing that file (ticking the checkbox), creating a signed commit on the Ledger's protected branch. R3 reads the first checked box once per day. **No Curator Shared Brain involvement.** The audit trail is signed commits on the Ledger's `main` — exactly the existing pattern. This applies to *all Routine-authored operational artefacts*: output logs, audit logs, business reviews, klarna tests, variable statements, long-tail statements, compensation packets, founder approvals — these are Ledger content, not Firm Brain content. The Firm Brain is for *partner-contributed knowledge* (theses, decisions, ADRs, partner profiles, prompts, change-management artefacts), authored in personal Curators and synthesized.

7. **GDPR Article 17 erasure uses Curator's `POST /api/sharedbrain/:id/revoke` endpoint.** Admin token + typed `REVOKE-<fellow_id>` confirmation; deletes contributions; rebuilds affected collective pages; appends to the revoke audit log. Replaces the previously hand-rolled procedure in [governance/EU-AI-ACT.md](../../governance/EU-AI-ACT.md) and [skills/privacy-self-sovereign/SKILL.md](../../skills/privacy-self-sovereign/SKILL.md). Absolute erasure (git history rewrite, force-push, backup purge, contributor notification) remains a separate procedure — Curator's revoke does not pretend to cover it.

8. **Storage backend = GitHub for v1.x.** Curator v3.0.0-beta ships only the GitHub adapter; Cloudflare R2 with per-bucket `jurisdiction = "eu"` is on Curator's v3.1 roadmap. EU firms that need data residency *today* must use **GitHub Enterprise Cloud with the EU data residency option** for the Firm Brain repo (Finding #16's plan-tier issue, amplified). Most firms will hold on Team or Enterprise pending v3.1.

9. **Synthesis-LLM choice is the admin's.** Curator v3.0.0-beta uses Gemini Flash Lite at the synthesis step (called from the admin's machine). The privacy-track aspiration of "no cloud LLM in Gen 1" is **not** met by Shared Brain synthesis today; this is the same Gen-1 gap [GENERATIONS.md](../../GENERATIONS.md) already flags for Curator broadly. It does not regress; it does not fix it either. Partners' personal-Curator writing can use a local LLM (LM Studio + Qwen / Llama / DeepSeek), but the admin's weekly Synthesize step calls a cloud model. **This is acceptable for v1.x.** v2.0+ will revisit when Curator's local-LLM synthesis ships.

## Plan-tier implications (Finding #16 amplified)

Each firm now provisions **two protected GitHub repos**: Ledger + Firm Brain. GitHub Free private repos do not enforce branch protection (Finding #16). Recommendation:

- **Solo / 2-partner exploratory firms:** GitHub Pro on both repos; understand that branch protection is best-effort, not enforced.
- **3+ partner operating firms:** GitHub Team minimum on both repos. Branch protection enforced; signed commits required; required-status-checks on Ledger's `oot/klarna-test`.
- **EU firms with GDPR data-residency requirements:** GitHub Enterprise Cloud with EU residency on the Firm Brain repo. Ledger can stay Team if cost matters, but Enterprise Cloud across both is cleaner.

The install plans surface this as a structural decision *before* repo creation, not after (per Finding #16 in [install-test-report-2026-05-10.md](install-test-report-2026-05-10.md)).

## Consequences

### Positive

1. **Curator carries the discipline.** Provenance attribution, conflict markers, weekly merge, Article 17 revoke — all built-in. Less framework surface to maintain.
2. **S12 aligns natively.** `contributor_retains` + UUID-pseudonymous attribution maps directly to S12's self-sovereign discipline; advisors can adopt it without surrendering IP.
3. **Per-LLM neutrality.** Partners write via whatever LLM they prefer (privacy = local; cloud = Claude/etc). The shared layer doesn't constrain individual choice.
4. **Track symmetry preserved.** Cloud and privacy partners contribute to the same Firm Brain the same way. The only delta is *which LLM the partner uses on their own machine* — exactly the framework's stated track-symmetry principle.
5. **Ledger ↔ Firm Brain separation makes Routines simpler to classify.** Ledger-writing routines (R1, R3, R4, R5, R6, R8) keep the openpyxl + signed-commit pattern from ADR-001. Knowledge-capture routines (e.g., R2 weekly recap) can be rewritten to write into a partner's personal Curator domain and Push, or to author the firm's "decision rationale" pages directly into the admin's opted-in domain.
6. **Charter-level IP assignment is now machine-enforced.** The `data_handling_terms` field locks at admin setup ("locked after invites go out" per Curator's admin doc). Drift is caught at consent time, not at audit time.

### Negative / cost

1. **Two repos per firm to provision and protect.** Each needs a PAT, branch protection, signing setup. The install plans add ~5 minutes per partner.
2. **EU firms hit GitHub Enterprise Cloud cost early.** Free / Pro / Team are US-only for storage. v3.1's Cloudflare R2 path will relieve this; firms launching before then on EU residency have a real cost.
3. **Synthesis is admin-coupled.** Until Curator v3.1 ships automation, the admin (founder, typically) must remember to run weekly Synthesize. This is exactly the role R9 should fill — see follow-up below.
4. **Partner charter must contain an explicit IP-assignment clause** for `organisational` mode to be defensible. [templates/partner-charter.md](../../templates/partner-charter.md) needs verification (Tier 2 follow-up).
5. **The previously-conflated "Brain repo" needs renaming across the framework.** Where v1.0 said "Brain repo" meaning the operational state, that is now the Ledger; where v1.0 said "Brain" meaning firm knowledge, that is now the Firm Brain. Bridge commits aa739cc and 27e0afa started this work; this ADR completes the conceptual split.

### Plan-tier implication (cost summary)

For a 3-partner firm on the cloud track with this ADR adopted:

- 2 GitHub Team seats minimum (admin + 1 partner; the third uses collaborator access, $0 incremental) ≈ $8/mo.
- Claude Max on at least the admin's account (R-routines + synthesis prompts) ≈ $200/mo per admin.
- Optional: Claude Pro for non-admin partners if they want personal-Curator MCP from Claude Desktop ≈ $20/mo each.

EU firms add GitHub Enterprise Cloud (~$21/seat/mo) until v3.1 R2 lands.

## Alternatives considered

### Alternative A — keep the v1.0 hand-rolled Brain repo, ignore Curator Shared Brain
**Rejected.** Sacrifices native UUID attribution, the machine-enforced IP-mode lock, the typed-confirmation revoke endpoint, and the Jaccard conflict detector. All three of those are real value the framework was carrying as governance disciplines and TODOs; Curator now provides them.

### Alternative B — collapse Firm Brain into the Ledger repo (single-repo model)
**Rejected.** Two reasons. First, the writers and write models are fundamentally different — Routines mutate `.xlsx` via openpyxl on every R1 run; partners push `DeltaSummary` JSON into `contributions/<fellow_id>/` via Curator's protocol. Mixing them invites accidental cross-writes (a Routine appending markdown to `collective/`, or a Curator Push touching `firm/excel/`). Second, the branch protection rules differ — the Ledger requires `oot/klarna-test` as a required status check on `main` (decision #10); the Firm Brain doesn't. Cleaner to separate.

### Alternative C — single-repo with subdirectories enforced via CODEOWNERS
**Rejected.** Workable but fragile. CODEOWNERS enforces review, not write paths. Curator's adapter expects the repo root to be the brain root; squeezing it into a subdirectory means patching Curator. Not worth it.

### Alternative D — use Curator Shared Brain for layer 2 *and* layer 1
**Rejected as a non-option.** Curator does not handle Excel mutation. The Ledger's openpyxl + signed-commit pattern is the right substrate for state that has formulas, named ranges, and validation. Shared Brain handles markdown. These are different jobs.

## What this changes in the codebase

The full sequence is laid out in [CLAUDE.md → Active conversations](../../CLAUDE.md). Tier-by-tier:

**Tier 1 — strategic (this ADR + index lock)**
- This ADR (`ADR-002`).
- New decisions #14–#16 added to [CLAUDE.md](../../CLAUDE.md) "Key design decisions".
- [GLOSSARY.md](../../GLOSSARY.md) — add **Firm Brain**, **Shared Brain (Curator)**, **personal Curator**, **opted-in domain**, **synthesized mirror**; cross-reference with existing **Ledger** and **Second Brain** entries.
- [GENERATIONS.md](../../GENERATIONS.md) — Shared Brain reclassified from "Gen 1 manual / Gen 2 automated" to "Gen 1 native via Curator v3.0.0-beta+".

**Tier 2 — spec rewrites**
- [templates/brain/FIRM-ONTOLOGY.md](../../templates/brain/FIRM-ONTOLOGY.md) + [templates/brain/SPEC.md](../../templates/brain/SPEC.md) — recast as Curator-Shared-Brain-native: pages live in partners' personal domains; collective is synthesized.
- [skills/my-curator/SKILL.md](../../skills/my-curator/SKILL.md) — Shared Brain mirror semantics, onboarding flow, IP mode flags.
- [skills/privacy-self-sovereign/SKILL.md](../../skills/privacy-self-sovereign/SKILL.md) (S12) — map `contributor_retains` + UUID attribution to S12 discipline.
- [skills/governance-compliance/SKILL.md](../../skills/governance-compliance/SKILL.md) (S7) + [governance/EU-AI-ACT.md](../../governance/EU-AI-ACT.md) + [governance/SECRETS-POLICY.md](../../governance/SECRETS-POLICY.md) — admin_token policy, PAT lifecycle, revoke runbook.
- [routines/SPEC.md](../../routines/SPEC.md) — classify each Routine as Ledger-writing or Firm-Brain-pushing.
- **New R9** — weekly admin-run Synthesize routine (or fold into an existing routine; deferred to Tier 2 design).
- [templates/partner-charter.md](../../templates/partner-charter.md) — verify / harden the IP-assignment clause for `organisational` mode.

**Tier 3 — onboarding**
- [installer/agent-assisted/cloud-install-plan.md](../../installer/agent-assisted/cloud-install-plan.md) + [installer/agent-assisted/privacy-install-plan.md](../../installer/agent-assisted/privacy-install-plan.md) — add Firm Brain provisioning (admin wizard) + per-partner contributor wizard (six-step).
- [installer/wizard.py](../../installer/wizard.py) — corresponding Path B steps.
- [docs/00-quickstart-cloud.md](../../docs/00-quickstart-cloud.md) + [docs/00-quickstart-privacy.md](../../docs/00-quickstart-privacy.md) — Firm Brain setup in the first-Sunday flow; plan-tier callout amplified.
- [docs/ECOSYSTEM.md](../../docs/ECOSYSTEM.md) — Curator entry bumped to v3.0.0-beta.1 with Shared Brain capability.
- Reference orgs in [examples/](../../examples/) — scaffold a Firm Brain config alongside the Ledger.

## References

- [Curator Shared Brain user guide](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain.md)
- [Curator Shared Brain admin operations](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-admin.md)
- [Curator Shared Brain compliance reference](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-compliance.md)
- [Curator Shared Brain design / architecture](https://github.com/talirezun/the-curator/blob/main/docs/shared-brain-design.md)
- [ADR-001](ADR-001-cloud-routine-excel-writeback.md) — Ledger writeback (unchanged by this ADR).
- [CLAUDE.md](../../CLAUDE.md) — repository orientation + decisions-of-record list.
- [install-test-report-2026-05-10.md](install-test-report-2026-05-10.md) — Finding #16 (GitHub Free private repos do not enforce branch protection).
