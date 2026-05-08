---
name: <pack-id>
description: <one-line description of what this Skill Pack does and when to invoke it>
version: 1.0.0
tier: 1 | 2
status: hardened | scaffold
allowed_tools:
  - <mcp-tool-name-1>
  - <mcp-tool-name-2>
  - <built-in-tool>
authors:
  - Dr. Tali Režun
license: CC BY-SA 4.0
last_updated: YYYY-MM-DD
---

# <Pack Name>

> **Generation marker:** This pack ships in v1.0 as <hardened | scaffold>. <If scaffold: "Substantive content lands in v1.x; this file currently provides structure and TODOs.">
> **Klarna Test interaction:** <Yes (specify trigger) | No>
> **Brain interaction:** <Reads | Writes | Both — describe>

## 1. Purpose

One paragraph describing what this Skill Pack does and what problem it solves. Be specific about the operational problem, not the conceptual one. This is the section the model uses to decide whether to invoke the Pack.

## 2. When to invoke this pack

A numbered list of trigger situations. Each item starts with a verb. Examples:

1. When a partner asks how to <X>.
2. When a Routine produces output of type <Y>.
3. When the Brain receives a new document tagged <Z>.

If the pack has a Klarna Test interaction, that trigger goes here explicitly.

## 3. When NOT to invoke this pack

Three to five entries. Specific. The model uses this to disambiguate from adjacent packs.

## 4. Operational instructions

The substantive section. Numbered steps the model follows when the pack is invoked. Each step:

- States the action.
- States the tool used (must be in `allowed_tools`).
- States the success criterion.
- Includes the specific prompt fragment if applicable.

The structure mirrors the My Curator skill: clear, sequential, with explicit branching where the workflow differs by case.

### 4.1 <First sub-workflow>

Step-by-step instructions. Include code or prompt snippets in fenced blocks. Reference Brain pages, Excel files, and Routines by their canonical paths.

### 4.2 <Second sub-workflow>

As above.

## 5. Brain interaction protocol

How this pack reads from and writes to the Brain.

**Reads:**
- <Brain query patterns the pack uses>

**Writes:**
- <Where the pack creates or updates Brain pages>
- <The wikilink discipline — must reference existing slugs only, etc.>

**Domains:**
- <Which Brain domains the pack is allowed to operate in>

## 6. Excel interaction protocol

If the pack reads from or writes to any Excel template:

- File: `templates/excel/<file>.xlsx`
- Sheet: `<sheet name>`
- Operation: read | write | both
- Trigger: manual | Routine ID

## 7. Routine integration

If the pack is invoked by a scheduled Routine:

- Routine ID (R1–R8).
- Trigger.
- Expected output shape.

## 8. Don'ts

Numbered list of failure modes specific to this pack. Each one a one-sentence prohibition.

1. Don't <specific failure mode>.
2. Don't <another>.

The "Don'ts" list is non-negotiable. Anything in it is a hard prohibition; the model refuses requests that would require violating it.

## 9. Quick reference

A compact cheat sheet for partners using the pack interactively. Aim for one screen.

| Situation | Action | Output |
|---|---|---|
| <Common situation 1> | <Action verb> | <What lands where> |
| <Common situation 2> | <Action> | <Output> |

## 10. References

Citations for the substantive content. Include: peer-reviewed papers, industry reports, regulatory texts, the framework's own SPEC, anchor URLs.

Format: numbered list, full citations, no "URL only" entries.

## Acceptance criteria for this SKILL.md

- All sections 1–10 present.
- Frontmatter passes the Phase 8 linter.
- Every tool referenced is in `allowed_tools`.
- Every Brain page referenced exists or is explicitly noted as TODO.
- At least 2 worked examples in `examples/`.
- At least 5 references in section 10.