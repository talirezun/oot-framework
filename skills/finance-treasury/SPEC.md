# Skill Pack S10 — Finance & Treasury: SPEC

**ID:** S10 | **Tier:** 2 | **Status:** Scaffold in v1.0; harden in v1.x

## Purpose

FIAT-default in v1.0; documents the stablecoin upgrade path for Gen 2. Owns treasury management, agent-cost attribution (Prefactor / Bifrost-style per-agent token accounting), forecasting, and the (optional) treasury runway tracker (X8).

## Scope

**Generation 1:** FIAT payroll coordination with banking partners. Agent-cost attribution (per-Skill, per-Routine token costs allocated to use cases). Monthly financial close coordination. Treasury runway tracker (X8 — optional; only orgs adopting Unit Fund). Forecasting basics.

**Generation 2:** Stablecoin payroll rail integration (Rise / Circle). Smart-contract long-tail entitlement disbursement. Internal Unit Fund treasury reserve management. Triple-entry-style audit log integration.

## Allowed tools

Curator MCP. Excel MCP / Sheets. Banking integrations (jurisdiction-specific). Stablecoin payment APIs (Gen 2).

## Section structure

Standard 10 sections, scaffold-level.

## Don'ts (scaffold)

1. Don't activate stablecoin payroll without counsel review for the partner's jurisdiction.
2. Don't open the Unit Fund without ≥6–9 months of attribution accuracy data.
3. Don't bypass treasury runway discipline if the Unit Fund is open.

## References

1. Yolo Investments. *Stop paying for hours.* — treasury reserve discipline.
2. Rise (Circle partner) — stablecoin payroll case studies.
3. EU MiCA + US GENIUS Act — regulatory framework.
4. Prefactor, Bifrost — per-agent cost attribution patterns.
5. ØØT Skill Pack S3 — Compensation & Attribution (upstream dependency).

## Acceptance criteria

Scaffold passes linter. Gen 1 vs. Gen 2 boundary explicit.