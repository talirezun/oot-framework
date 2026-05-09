# Example 2 — Debugging an unsatisfactory AI output

A worked example of using the Output Evaluation rubric (§4.4) and the construction discipline (§4.1) to diagnose *why* a prompt produced a bad result, then fix it.

## The starting state

A partner has been trying to get Claude Code to refactor a 4-file authentication module to use a new dependency-injection pattern. After three attempts, the output is still:
- Inconsistent (different files use different injection styles).
- Missing tests for two of the four files.
- Subtly broken (one of the refactored files no longer imports a needed module).

The partner's first instinct is "the model is bad at refactoring." S2's discipline says: **debug the prompts first.**

## The diagnostic — Tier-1 rubric

The partner runs the Tier-1 quick checklist on their last attempt:

| Check | Result |
|---|---|
| Output matches requested Format exactly? | ✗ The Format said "show me the diff per file"; the model returned 4 separate refactored files in one wall of text. |
| Every Constraint satisfied? | ✗ "Use the new DI pattern from `[[architecture/ADR-2026-007]]`" — the model didn't reference the ADR; it invented its own DI pattern. |
| Self-Check the prompt requested actually performed? | ✗ The prompt had no Self-Check section at all. |
| Every fact verifiable? | ✗ The output assumes a function `inject_session()` that doesn't exist in the codebase. |
| Any hallucinated wikilink? | ✗ The output references `[[architecture/auth-rewrite-2026]]` which doesn't exist. |

Five out of five checks fail. The diagnosis is not "the model is bad"; the diagnosis is "the prompt was wrong."

## Reconstructing the prompt as a chain

The partner switches from a single mega-prompt to the **sequential chain pattern** (§4.3). New chain at `firm/prompts/auth-refactor-2026/`:

### Stage 1 — Discovery (`stage-1-discovery.md`)

```markdown
## Goal
Read the four files (paths below) and produce a one-page summary of their current authentication patterns, dependencies, and test coverage.

## Context
- Repo: [[architecture/oot-firm-saas]]
- ADR for the new pattern: [[architecture/ADR-2026-007]]
- Files in scope:
  - `src/auth/login.ts`
  - `src/auth/session.ts`
  - `src/auth/middleware.ts`
  - `src/auth/refresh.ts`

## Constraints
- Do not propose changes yet. Discovery only.
- Identify any functions that depend on global state or module-level singletons (these are the candidates for DI).
- List the existing test files for each.

## Format
Markdown. One H2 per file.

## Self-Check
- Did I look at every file in the scope list?
- Did I identify global-state dependencies?
- Did I list test files?
```

### Stage 2 — Plan (`stage-2-plan.md`)

```markdown
## Goal
Given the discovery output (in user-message), produce a 6-step refactor plan that applies the DI pattern from [[architecture/ADR-2026-007]] consistently across all four files, with test updates.

## Context
- Discovery summary: <paste from Stage 1 output>
- ADR: [[architecture/ADR-2026-007]] (in Brain)

## Constraints
- One file per step (plus a final step for cross-file integration tests).
- Each step lists the exact `inject_*` calls to replace which existing function calls.
- Each step lists the test changes required.

## Format
Numbered list of 6 steps. For each: which file, what changes, what tests.

## Self-Check
- Does the plan use the DI pattern from the ADR consistently across all 4 files?
- Does every step have explicit test changes?
- Is the cross-file integration test step explicit?
```

### Stage 3 — Review (human)

The partner reads the plan. Two pushbacks: "step 3 should come before step 2 because middleware depends on session"; "the test for refresh.ts needs a mock injected, you didn't say that". The partner edits the plan in the Brain.

### Stage 4 — Execute (`stage-4-execute.md`)

```markdown
## Goal
Implement plan-step <N> from [[architecture/auth-rewrite-2026/plan]]. Produce a diff for the affected file(s) only.

## Context
- The full plan: [[architecture/auth-rewrite-2026/plan]]
- This step's scope: <paste plan-step text>

## Constraints
- Diff format only. Do not produce full file contents.
- If a needed function does not exist in the codebase, STOP and flag in your output. Do not invent.
- Add the test changes specified in the plan-step.

## Format
Diff. Then a short note listing what was added vs. modified vs. removed.

## Self-Check
- Did I produce a diff (not full files)?
- Did I add the test changes?
- Did I flag any missing dependencies?
```

Stage 4 runs once per plan-step (4 plan-steps + 1 integration step = 5 stage-4 invocations). Each in a fresh conversation.

## Outcome

After the chain rewrite, the model produced consistent, test-covered, correctly-importing diffs. The merged branch passed CI on first try.

## What changed

- **No more single mega-prompt.** Each stage has a clean, narrow goal.
- **The Brain is the substrate.** The plan exists at a stable wikilink; the discovery output exists at a stable wikilink; the model's context window is small at each stage.
- **Self-Check at every stage.** The model catches its own errors before returning.
- **Human review between stages 2 and 4.** The partner is the merge driver; the model executes against an accepted plan.

## Anti-patterns this example diagnoses

1. **"The model is bad at X"** — usually means the prompt is wrong. Run the rubric first.
2. **Single mega-prompt for multi-file work** — context-window dilution + stage contamination.
3. **No Brain anchoring** — the plan should be a stable artefact, not in-context-only.
4. **No Self-Check** — the model has no internal correction mechanism.
