# Mental Model

This document is **non-normative**. It provides a conceptual overview of the BDIR Patch Protocol.

## The core idea

The AI reviews content, but **does not rewrite documents**.

Instead, the AI produces **block-scoped patch instructions** (a Patch) that downstream systems can validate and apply deterministically.

## Roles and responsibilities

- **Extractor / Producer**
  - Converts a source document into an ordered list of BDIR blocks.
  - Derives an **Edit Packet** for AI input.

- **AI system (untrusted proposer)**
  - Reads the full Edit Packet for context.
  - Outputs a **Patch** (operations such as `replace`, `delete`, `insert_after`, `insert_before`, `replace_block`, `delete_block`, or `suggest`).

- **Validator / Applier (trusted)**
  - Validates the Patch against the RFC and schemas.
  - Rejects the Patch if any rule is violated (page hash mismatch, missing block, ambiguous substring match, etc.).
  - Applies the Patch as an all-or-nothing operation.

## Data flow

1. **Extract**: Source document → BDIR blocks → Edit Packet
2. **Propose**: Edit Packet → AI → Patch
3. **Validate**: Patch + target document state → accept or reject
4. **Apply**: Accepted Patch → deterministic document update

## Mutating vs advisory operations

- `replace`, `delete`, and `insert_after` are **mutating** operations and are only applied after validation.
- `suggest` is **non-mutating** and **advisory**. Consumers may drop all `suggest` operations without changing the resulting document state.

## What makes this safe

- Block-level targeting prevents whole-document rewrites.
- Page-level hash binding prevents applying patches to the wrong document state.
- Exact substring matching and ambiguity rejection prevents accidental misapplication.
- The AI is treated as untrusted; safety is enforced by validation.