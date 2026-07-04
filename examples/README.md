# Reference Org Examples

Three reference organisations demonstrating the framework in operation. **`small-org/` is populated with a representative, internally-consistent two-week operational slice (2026-04-06 → 2026-04-19)** — ~30 Brain pages whose wikilinks all resolve within the example. `medium-org/` and `regulated-eu-org/` remain specified-but-unpopulated (README only); their population — and small-org's full quarter — lands in v1.x.

| Example | Profile | Status | Demonstrates |
|---|---|---|---|
| [small-org](small-org/) | 3-partner cloud-track studio (Solunar Studio) | **Populated — two-week slice** | The framework working at minimum scale |
| [medium-org](medium-org/) | 12-partner cloud-track cooperative (Brda Cooperative) | Specified; population v1.x | Cohort diversity, Tier-2 disputes, EU AI Act high-risk use case |
| [regulated-eu-org](regulated-eu-org/) | 6-partner regulated-EU consultancy (AdriaLex AI) | Specified; population v1.x | EU AI Act compliance, Klarna Test that abandoned an engagement, mid-migration to privacy track |

> 📖 The full specifications for each org are in [`examples/SPEC.md`](SPEC.md). Full-quarter population (60-90 days of Brain pages) lands in v1.x per each org's spec.

---

## How to read a reference org

Each org folder ships today:
- `README.md` — explains the org's profile and the awkward edges.
- (`small-org/` only) A populated `firm/` tree: two-week slice of output logs, BRs, a decision, a Klarna Test, compensation (summary + resolved dispute), a perception-gap page, audit logs, and a brain-health snapshot.

Still to come (v1.x):
- `firm/` population for medium-org and regulated-eu-org; small-org's remaining ~10 weeks of the quarter.
- Excel operational data is **not** checked into examples — the `.xlsx` state is generated at adoption (`scripts/build_excel.py`) and mutated by Routines; binaries in an example would rot instantly. The markdown pages are the human-readable mirror.

Recommended reading order (works today for small-org; for medium/regulated only the README exists):

1. The org's `README.md` — understand the profile.
2. The partner roster (`firm/partners/index.md`).
3. The most recent BR (`firm/business-reviews/<latest>.md`) — see the rhythm.
4. Any Klarna Test entries (`firm/klarna-tests/`) — see the discipline.
5. Any open disputes — see how they resolved.

---

## Current status

- **`small-org/`** — populated with a representative two-week slice (2026-04-06 → 2026-04-19): ~30 internally-consistent Brain pages; every wikilink resolves within the example; numbers agree with the S3 worked examples (Mira's €1,371 March proration, Davor's Acme long-tail, Anya's dispute). The full quarter lands in v1.x.
- **`medium-org/` and `regulated-eu-org/`** — specified (README + [`SPEC.md`](SPEC.md)); population lands in v1.x.

Full-quarter population is deferred deliberately — generating a fully-coherent 90-day reference org requires the framework's Routines to actually run on the example data, which is best done iteratively as the framework is adopted.

For the canonical worked examples WITHIN the framework, see the `examples/` folders inside each Skill Pack — those are complete in v1.0:
- [`skills/compensation-attribution/examples/`](../skills/compensation-attribution/examples/) — partner onboarding + variable + long-tail + rework.
- [`skills/code-qa/examples/`](../skills/code-qa/examples/) — Plan Mode + ai-replaces-human PR end-to-end.
- [`skills/change-management/examples/`](../skills/change-management/examples/) — pilot that worked + pilot that abandoned.
- [`skills/privacy-self-sovereign/examples/`](../skills/privacy-self-sovereign/examples/) — 5-partner privacy setup + cron-missed incident.
- (and others — see each Skill Pack's `examples/` folder).

These per-Skill-Pack examples are individually complete and walk through specific scenarios. The `examples/<org>/` reference orgs are *firm-level* worked examples that will integrate the per-Skill examples into a coherent firm story in v1.x.
