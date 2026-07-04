# Reference Org Examples

Three reference organisations that will demonstrate the framework in operation. **In v1.0 these are scaffolds, not populated firms** — each folder's `README.md` describes the target population (partners, awkward edges, the Excel and Brain data the org *will* contain), but the full `firm/` tree, resolving wikilinks, and evaluated Excel formulas land in v1.x. `small-org/` additionally ships two representative Brain pages; `medium-org/` and `regulated-eu-org/` ship their README only today. Read a README to understand the profile and what the framework will look like at that scale.

| Example | Profile | Demonstrates |
|---|---|---|
| [small-org](small-org/) | 3-partner cloud-track studio (Solunar Studio) | The framework working at minimum scale |
| [medium-org](medium-org/) | 12-partner cloud-track cooperative (Brda Cooperative) | Cohort diversity, Tier-2 disputes, EU AI Act high-risk use case |
| [regulated-eu-org](regulated-eu-org/) | 6-partner regulated-EU consultancy (AdriaLex AI) | EU AI Act compliance, Klarna Test that abandoned an engagement, mid-migration to privacy track |

> 📖 The full specifications for each org are in [`examples/SPEC.md`](SPEC.md). The reference orgs are scaffolds in v1.0; v1.x will populate the full 60-90 days of Brain pages + Excel data per each org's spec.

---

## How to read a reference org

Each org folder ships (v1.0):
- `README.md` — explains the org's profile and the awkward edges its populated v1.x form will contain.
- (`small-org/` only) A couple of representative `firm/` Brain pages (`firm/klarna-tests/KT-2026-001.md`, `firm/partners/index.md`) so you can see the *shape* of a Brain page.

Each org folder **will** ship (v1.x):
- `firm/` — a partial Brain mirror with the canonical pages (partners, recent BRs, key decisions, Klarna tests).
- Populated Excel files showing 60-90 days of operational data.

Recommended reading order (once populated in v1.x — today only the README exists for medium/regulated, README + 2 pages for small):

1. The org's `README.md` — understand the profile.
2. The partner roster (`firm/partners/index.md`).
3. The most recent BR (`firm/business-reviews/<latest>.md`) — see the rhythm.
4. Any Klarna Test entries (`firm/klarna-tests/`) — see the discipline.
5. Any open disputes — see how they resolved.

---

## v1.0 status

The reference orgs in v1.0 are **scaffolds**:
- README describing the target population for each org.
- `small-org/` also ships 2 representative Brain pages (`firm/klarna-tests/KT-2026-001.md`, `firm/partners/index.md`); `medium-org/` and `regulated-eu-org/` ship README only.
- The directory tree, the full operational data (60-90 days of ledger rows, BRs, audit logs), and the resolving wikilinks land in v1.x.

This is intentional — generating fully-coherent reference orgs requires the framework's Routines to actually run on the example data, which is best done iteratively as the framework is adopted.

For the canonical worked examples WITHIN the framework, see the `examples/` folders inside each Skill Pack — those are complete in v1.0:
- [`skills/compensation-attribution/examples/`](../skills/compensation-attribution/examples/) — partner onboarding + variable + long-tail + rework.
- [`skills/code-qa/examples/`](../skills/code-qa/examples/) — Plan Mode + ai-replaces-human PR end-to-end.
- [`skills/change-management/examples/`](../skills/change-management/examples/) — pilot that worked + pilot that abandoned.
- [`skills/privacy-self-sovereign/examples/`](../skills/privacy-self-sovereign/examples/) — 5-partner privacy setup + cron-missed incident.
- (and others — see each Skill Pack's `examples/` folder).

These per-Skill-Pack examples are individually complete and walk through specific scenarios. The `examples/<org>/` reference orgs are *firm-level* worked examples that will integrate the per-Skill examples into a coherent firm story in v1.x.
