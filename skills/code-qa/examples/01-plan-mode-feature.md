# Example 1 — A non-trivial feature, full Plan Mode

End-to-end Plan Mode workflow on a real-feeling feature: implementing OAuth2 PKCE flow for partner onboarding in the firm's TypeScript SaaS.

## Setup

- **Partner:** Mira (agentic-engineer cohort).
- **Output Spec:** `firm/partners/mira-tek/output-specs/2026-05-10--oauth2-pkce.md`. Value tier `M`.
- **Repo:** `firm-saas`. CLAUDE.md, AGENTS.md, the 5 setup pre-requisites all present (verified by `oot-codeqa setup-protections --check`).
- **Stack:** TypeScript, Next.js, NextAuth.

## Discovery (12 minutes)

Mira opens Claude Code in the repo. Plan Mode is OFF.

```
Read the current authentication implementation. Files of interest: src/auth/*, pages/api/auth/*. Produce a one-page summary of:
1. Current authentication flow (verbal walkthrough, no code).
2. Where session tokens are issued.
3. What protections exist against authorization-code interception.
4. Where the existing tests live.
Do not propose changes yet.
```

Output → committed to `firm/architecture/oauth2-pkce-2026-05/discovery.md`. Key findings:
- NextAuth handles OAuth2 authorization-code flow without PKCE.
- Session tokens issued in `pages/api/auth/[...nextauth].ts`.
- No PKCE protection currently; potential authorization-code interception risk if the redirect URI is intercepted.
- Tests in `tests/auth/*.test.ts`.

## Plan (22 minutes)

Mira toggles Plan Mode ON. Hands the model the discovery summary + Output Spec.

```
Given the discovery and the Output Spec [[partners/mira-tek/output-specs/2026-05-10--oauth2-pkce]], produce a step-by-step plan to add PKCE protection to the OAuth2 flow. Format:
- Numbered steps, each with affected files, what the change is, what tests are added/changed.
- An explicit risk list.
- A "what-could-go-wrong" appendix with rollback steps.
```

Output → `firm/architecture/oauth2-pkce-2026-05/plan.md`. Key sections:
1. Add `PKCEStore` interface and `RedisPKCEStore` implementation. New file `src/auth/pkce-store.ts`. Tests: `tests/auth/pkce-store.test.ts`.
2. Modify NextAuth options to inject PKCE config. File: `pages/api/auth/[...nextauth].ts`. Tests: extend `tests/auth/nextauth.test.ts`.
3. Add code-verifier generation to client-side login flow. File: `src/auth/login.tsx`. Tests: `tests/auth/login.test.tsx`.
4. Add code-challenge sending in authorization request. Same file as step 3.
5. Add code-verifier exchange in token request. File: `pages/api/auth/[...nextauth].ts`.
6. Integration test: full OAuth2-PKCE round-trip. New file: `tests/integration/auth-oauth-pkce.test.ts`.
7. Add ADR. New file: `firm/architecture/ADR-2026-014.md`.

**Risks:** existing sessions invalidate on deploy if migration incorrectly handled (mitigation: phased rollout with dual support); PKCEStore Redis dependency (already on stack, but document).

**Rollback:** revert PR; existing sessions remain valid; no data migration to reverse.

## Review (8 minutes)

Mira shares the plan with Davor (a fellow agentic-engineer; the firm has a 2-reviewer convention for auth-touching changes).

Davor's comments inline on the Brain page:
- *"Step 1 — should `PKCEStore` be ephemeral or persisted? You're using Redis but PKCE state typically TTL <10 min. Recommend explicit TTL config."*
- *"Step 2 — NextAuth has built-in PKCE support since v4.24. Are we writing our own to keep control, or did you miss this? Worth an ADR-level discussion."*
- *"Step 6 — integration test is good, but also add a security regression test that confirms the flow rejects code-verifier mismatches (the actual attack PKCE prevents)."*

Mira responds inline:
- TTL: agreed, will add explicit 10-min TTL config in `PKCEStore`.
- NextAuth's built-in: oversight; let me check whether we can use it directly. Updating plan.
- Security regression test: yes, adding to step 6.

Updated plan committed (v2). Davor approves.

## Execute (3 hours, 7 plan-steps)

Fresh Claude Code session for execute. Plan Mode OFF.

Plan-step 1 (turns out NextAuth's built-in PKCE works, so step 1 changes from "implement own store" to "configure NextAuth's built-in"):

```
Implement plan-step 1 of [[architecture/oauth2-pkce-2026-05/plan]] (v2 — using NextAuth's built-in PKCE). Produce a diff for the affected file(s) only. If a needed function does not exist in the codebase, STOP and flag in your output.
```

Diff produced. Mira reviews. Test passes locally. Commit:

```
[plan-step 1/7] feat: enable NextAuth built-in PKCE in auth config

Adds PKCE configuration per [[architecture/oauth2-pkce-2026-05/plan]] (v2).
NextAuth handles state + verifier internally; we configure TTL to 10 minutes.

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

Plan-steps 2–7 follow. Each commit references the plan. Where the model proposes something not in the plan, Mira either (a) updates the plan first then proceeds, or (b) flags as a deviation in the eventual PR description.

Total commits: 9 (7 plan-steps + 1 ADR commit + 1 fix-up after a verify-stage failure on the integration test).

## Verify (35 minutes)

Mira runs the test plan:
- Unit tests: pass.
- Integration test: pass.
- Security regression test (Davor's addition): catches a real bug — initial implementation of step 5 didn't validate code-verifier length. Mira halts; opens a fresh planning conversation; updates plan-step 5 with explicit length validation; re-executes that step. Re-run all tests: pass.
- Manual smoke test (login from local dev): works.

## PR (7 minutes)

PR opened against `main`. Description:

```
## OAuth2 PKCE for partner onboarding

Implements PKCE protection for the OAuth2 authorization-code flow.
Plan: [[architecture/oauth2-pkce-2026-05/plan]] (v2).
ADR: [[architecture/ADR-2026-014]].

## Plan-steps completed

- [x] 1/7 — NextAuth built-in PKCE config (deviation from v1; v2 plan)
- [x] 2/7 — Auth config TTL
- [x] 3/7 — Client login code-verifier generation
- [x] 4/7 — Authorization request code-challenge
- [x] 5/7 — Token exchange (revised to add length validation per verify-stage finding)
- [x] 6/7 — Integration test + security regression test
- [x] 7/7 — ADR committed

## Deviations from plan

- v1 plan had us implementing our own PKCEStore; v2 (post-Davor's review) used NextAuth's built-in. Plan Brain page updated.
- Step 5 was extended mid-execution to add explicit code-verifier length validation after the security regression test surfaced the gap. Plan Brain page updated.

## Klarna Test relevance

This PR does not remove a code path that was routing to a human; it adds protection to an existing automated flow. Auto-labeller did not apply `ai-replaces-human`. Confirmed by [reviewer]: not a Klarna trigger.
```

Davor reviews the PR (different role than the plan-review reviewer; per the firm's convention, plan-reviewer ≠ PR-reviewer when possible). Approves. CI green. Mira merges.

## After merge

- ADR-2026-014 status flips: `proposed` → `accepted`.
- The Output Spec page updates: `status: shipped`.
- R1 captures the merged PR that evening; X1 row appended for Mira: `value_tier=M`, `ai_authored_pct=45%` (estimated from `Co-authored-by:` trailers + diff stats).
- The plan Brain page stays in place; future auth-related work references it.

## What this example demonstrates

- The full discovery → plan → review → execute → verify → PR flow.
- The Brain as the persistent substrate (every artefact has a stable wikilink).
- Plan v1 → v2 evolution from review (the review caught the NextAuth-built-in oversight).
- Verify-stage finding that triggered a plan revision mid-execution.
- The `Co-authored-by:` trailer flowing through to R1's attribution.
- Honest deviation reporting in the PR description.
