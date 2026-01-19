# Prompt Guidelines

This document provides guidance for constructing prompts when using the BDIR Patch Protocol.

## Core Principles

Prompts SHOULD bias the AI toward:

- Minimal changes with clear benefit
- Deletion or suggestion over rewriting for boilerplate
- Preservation of tone and intent
- Avoidance of new content or advice

## Recommended Instructions

Prompts MAY include constraints such as:

- "Only propose changes with clear improvement."
- "Prefer delete or suggest for boilerplate or UI content."
- "Do not add content that is not already present."
- "If unsure, use suggest instead of edit."

## kind_code Usage

Prompts SHOULD explain kind_code importance ranges rather than detailed mappings.

Example:

```
kind_code: 0–19 content, 20–39 boilerplate, 40–59 UI, 99 unknown.
```

## Output Constraints

Prompts SHOULD instruct the AI to:

- Output JSON only
- Conform strictly to the patch schema
- Exclude unchanged blocks from the patch

## Safety Notes

For regulated domains (e.g. medical), prompts SHOULD explicitly prohibit adding new guidance or instructions.
