---
title: "{{PROMPT_TITLE}}"
slug: prompts/{{PROMPT_SLUG}}
domain: firm
type: prompt
prompt_id: {{PROMPT_SLUG}}
version: 0.1.0
intended_skill_pack: {{S1_S12}}
input_signature: "{{ONE_LINE_INPUT_DESCRIPTION}}"
output_signature: "{{ONE_LINE_OUTPUT_DESCRIPTION}}"
authors: [{{PARTNER_ID}}]
status: experimental
created: {{DATE}}
updated: {{DATE}}
---

# {{PROMPT_TITLE}}

## Description

{{ONE_PARAGRAPH_DESCRIPTION}}

## The prompt

```markdown
## Goal
{{GOAL_LINE}}

## Context
{{CONTEXT_BLOCK}}

## Constraints
{{CONSTRAINTS_BULLETS}}

## Format
{{FORMAT_SPEC}}

## Self-Check
{{SELF_CHECK_BULLETS}}
```

## Inputs required

{{INPUTS_TABLE}}

## Output schema

{{OUTPUT_SCHEMA}}

## Worked examples

{{#each examples}}
### Example {{n}} — {{example_title}}

**Input:**

{{input}}

**Output:**

{{output}}

**Notes:** {{notes}}

{{/each}}

## Changelog

{{#each changelog}}
### v{{version}} — {{date}}

{{change_summary}}

{{/each}}

### v0.1.0 — {{DATE}}

Initial draft.
