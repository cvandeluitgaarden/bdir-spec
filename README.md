# BDIR Patch Protocol

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18274720.svg)](https://doi.org/10.5281/zenodo.18274720)

The **BDIR Patch Protocol** defines a safe, deterministic way to use AI for content review by constraining AI systems to produce **block-level patch instructions** instead of rewritten documents.

This repository contains the normative specification (RFC), schemas, codebooks, and examples for the protocol.

---

## Status

This specification is archived on Zenodo and assigned the DOI: 10.5281/zenodo.18274720

---

## What problem does this solve?

Most AI-based content editing systems rewrite entire documents or large text blobs. This approach is risky in regulated, large-scale, or audit-sensitive environments because it can introduce:

- unintended semantic drift
- poor traceability
- difficult review and rollback
- high operational cost

The BDIR Patch Protocol takes a different approach:

> **AI reviews content, but never rewrites it.**  
> AI proposes *instructions* that can be validated, reviewed, and safely applied.

---

## Core ideas

- **Whole-document context**  
  AI receives the full document to understand meaning and structure.

- **Block-level targeting**  
  Changes are scoped to stable, identified blocks.

- **Patch instructions, not rewrites**  
  AI outputs operations like `replace`, `delete`, or `suggest`.

- **Hash-based safety**  
  Exact substring matching and content hashes prevent accidental misapplication.

- **Stateless by design**  
  Each request is self-contained and deterministic.

---

## BDIR (Block-based Document Intermediate Representation)

BDIR represents a document as an ordered sequence of semantic blocks.

Each block has:
- a stable identifier
- a semantic classification (`kind_code`)
- canonical text content
- a content hash

BDIR is **format-agnostic**. Markdown is commonly used as the canonical text encoding, but the protocol does not depend on Markdown specifically.

---

## Edit Packet (AI input)

To minimize token usage, AI systems receive a compact derivative of BDIR called an **Edit Packet**.

Example:

```json
{
  "v": 1,
  "tid": "example-001",
  "h": "pagehash123456",
  "ha": "sha256",
  "b": [
    ["p1", 2, "b2c3d4e5", "This is an example paragraph with a typo teh."]
  ]
}
```


**Interoperability:** Implementations **MUST** support `sha256` as a baseline hash algorithm. If `ha` is omitted, receivers **MUST** treat it as `sha256`.

Each block tuple is:

```
[block_id, kind_code, text_hash, text]
```

### JSON field naming (v1)

**Normative:** All v1 JSON wire-format field names defined by this specification **MUST** use **snake_case**.

**Non-normative compatibility note:** Receivers **MAY** accept alternate spellings (e.g. `blockId` / `kindCode`) via explicit adapters, but implementations **MUST NOT** emit non-canonical field names when producing v1 Edit Packets or patches.

---

## Patch (AI output)

AI systems return a **patch**, not modified content.

Example:

```json
{
  "v": 1,
  "h": "pagehash123456",
  "ha": "sha256",
  "ops": [
    {
      "op": "replace",
      "block_id": "p1",
      "before": "teh",
      "after": "the",
      "message": "Fix common typo."
    }
  ]
}
```

Patches are:
- deterministic
- human-reviewable
- safe to validate and apply

---

## Repository contents

```
RFC/
  RFC-0001-bdir-patch-protocol.md   # Normative specification

spec/
  schemas/                          # JSON Schemas (normative)
  codebooks/                        # kind_code mappings
  examples/                         # Minimal working examples
  fixtures/                         # Reference validation fixtures (non-normative)

docs/
  design-rationale.md               # Why the protocol is designed this way
  caching.md                        # Caching & deduplication guidance
  prompt-guidelines.md              # Prompting best practices
  implementation-notes.md           # Non-normative edge cases & operational guidance
```

---

## Specification status

- **RFC-0001**: Informational
- **Protocol version**: v1.0
- **Stability**: Suitable for production use
- **AI-agnostic**: Works with any LLM capable of structured output

Breaking changes, if any, will result in a new major version.

---

## Who should use this?

The BDIR Patch Protocol is intended for:

- CMS and publishing platforms
- Web crawlers and content auditors
- Regulated domains (medical, legal, financial)
- Human-in-the-loop editorial workflows
- Large-scale AI-assisted content review

---

## What this protocol does NOT do

- No direct HTML rewriting
- No full-document regeneration
- No per-block AI calls
- No reliance on AI memory or sessions

---

## License

This specification is licensed under the **Apache License 2.0**.  
See the `LICENSE` file for details.

---

## Feedback and contributions

Feedback is welcome.

- Clarifications and corrections: open an issue
- Spec changes: open a pull request with rationale
- Implementations: links and experience reports are encouraged

See `docs/design-rationale.md`, `docs/prompt-guidelines.md`, and `docs/implementation-notes.md` for additional context.


---

## Summary

The BDIR Patch Protocol provides a structured, auditable contract between AI systems and content pipelines.

It enables AI-assisted review **without trusting AI to rewrite your content**.
