# Implementation Notes (Non-normative)

**Status:** Non-normative guidance for implementers  
**Applies to:** RFC-0001 (BDIR Patch Protocol) v1.x  
**Last updated:** 2026-01-19

> **Non-normative**
>
> This document is *not* part of the normative protocol definition.
> It provides practical guidance and illustrative examples for real-world
> implementations.
>
> If anything here appears to conflict with RFC-0001, treat RFC-0001 as the
> source of truth.

---

## Scope

This companion document focuses on edge cases and operational choices that often
show up in production integrations, without expanding the normative requirements.
It covers:

- substring matching ambiguity
- Unicode normalization
- whitespace sensitivity
- empty / minimal block handling
- patch ordering and canonicalization
- illustrative error reporting formats

---

## Substring matching ambiguity (multiple matches)

RFC-0001 requires exact substring matching for `replace` and `delete` operations.
In practice, a `before` substring may appear multiple times within a block.
That can lead to non-deterministic application if an implementation implicitly
picks “the first match” (or a different match depending on the language/library).

### Recommended approaches

- Prefer rejecting an operation when `before` matches more than once.
  - This is conservative and tends to surface better AI proposals.
- Alternatively, support an optional `occurrence` selector internally
  (e.g., `0` for first match), but keep in mind it is not part of the v1 protocol.
  If you do this, consider treating it as an implementation extension and ensure
  your validator/applicator behavior stays deterministic.

### Illustrative example: ambiguous match

Given block text:

```text
The cat sat on the mat. The cat looked happy.
```

Operation:

```json
{
  "op": "replace",
  "blockId": "p1",
  "before": "cat",
  "after": "dog",
  "message": "Replace cat with dog."
}
```

This matches twice. A conservative applicator can reject the patch as ambiguous
and ask the AI (or editor) to propose a more specific `before` substring.

---

## Unicode normalization guidance

Exact substring matching can behave unexpectedly when text comes from systems
that normalize Unicode differently (or not at all). For example, `é` can appear
as a single code point (NFC) or as `e` + combining accent (NFD). They look the
same, but do not compare equal byte-for-byte.

### Recommended approaches

- Choose a single normalization strategy for canonical block `text`.
  - Many implementations use NFC for storage and matching.
- Normalize consistently across:
  - extraction → BDIR block text
  - edit packet generation
  - patch validation and application
- Log normalization decisions and version them if you change strategy.

### Illustrative example: visually identical, byte different

Block text (NFD):

```text
Café
```

Patch `before` (NFC):

```json
{
  "op": "replace",
  "blockId": "p2",
  "before": "Caf\u00e9",
  "after": "Café",
  "message": "Normalize spelling."
}
```

Even though these render similarly, exact matching may fail unless you normalize
consistently.

---

## Whitespace sensitivity and expectations

RFC-0001’s exact substring matching implies whitespace sensitivity. Variations
that look harmless to humans (tabs vs spaces, non‑breaking spaces, different
line endings) can make validation fail.

### Recommended approaches

- Treat block `text` as a canonicalized representation.
  - Decide how you represent line breaks (LF vs CRLF).
  - Decide whether you preserve trailing whitespace.
  - Decide whether you collapse repeated spaces (often not recommended for
    canonical content unless you are already doing so upstream).
- Make your extraction-to-canonicalization rules visible to implementers and
  stable over time.

### Illustrative example: invisible mismatch

Block text contains a non-breaking space (`\u00a0`):

```text
Hello\u00a0world
```

Patch tries to match a normal space:

```json
{
  "op": "replace",
  "blockId": "p3",
  "before": "Hello world",
  "after": "Hello, world",
  "message": "Add comma."
}
```

Visually identical in many renderers, but not a byte-exact match.

---

## Empty / minimal block handling

Some extraction pipelines produce blocks that are empty or nearly empty
(e.g., whitespace-only, a single punctuation mark, or a zero-width character).
These can be legitimate (a deliberate spacer), accidental (extraction artifact),
or context-dependent.

### Recommended approaches

- Decide whether your BDIR canonicalization ever emits empty blocks.
  - If you keep them, make them stable so that block IDs don’t churn.
  - If you drop them, do it consistently at extraction time so they never reach
    the edit packet.
- For patch application:
  - Be explicit about how you treat `before: ""` (empty substring).
    Many implementers reject empty `before` because it can match “everywhere”.

### Illustrative example: deleting a minimal block

If you keep a minimal block:

```json
["spacer-1", 40, "hash...", "—"]
```

Then a patch can remove it deterministically:

```json
{
  "op": "delete",
  "blockId": "spacer-1",
  "before": "—",
  "message": "Remove decorative separator."
}
```

---

## Patch ordering considerations

RFC-0001 notes that `ops` has no semantic ordering requirement, but also
recommends canonicalization for determinism.

### Recommended approaches

- Canonicalize patches immediately after generation (or immediately before
  storing/hashing) so that:
  - cache keys are stable
  - diffs in code review are quieter
  - telemetry comparisons are simpler
- When presenting patches to humans, consider grouping by document order rather
  than lexicographic blockId if you have the original edit packet.

---

## Example error reporting formats (illustrative)

The protocol intentionally does not standardize error formats. Still, many
operators benefit from consistent error reporting across validators and
applicators.

Below are small, copy-pastable formats that are easy to log, index, and display.

### Option A: compact JSON (single error)

```json
{
  "code": "PATCH_VALIDATION_FAILED",
  "reason": "before_substring_not_found",
  "opIndex": 0,
  "blockId": "p1",
  "detail": {
    "before": "teh",
    "hint": "Block text did not contain the exact substring. Check Unicode/whitespace normalization."
  }
}
```

### Option B: structured multi-error response

```json
{
  "code": "PATCH_REJECTED",
  "errors": [
    {
      "code": "UNKNOWN_BLOCK_ID",
      "opIndex": 2,
      "blockId": "p999"
    },
    {
      "code": "AMBIGUOUS_BEFORE_MATCH",
      "opIndex": 0,
      "blockId": "p1",
      "matches": 2
    }
  ]
}
```

### Option C: human-friendly one-liner

```text
PATCH_REJECTED: op[0] blockId=p1 ambiguous before match (2 occurrences)
```

---

## Operational guidance (practical)

These practices are commonly useful in production deployments:

- **Telemetry that distinguishes failure modes**
  - e.g., schema-invalid vs hash-mismatch vs substring-not-found vs ambiguous-match.
- **Redaction discipline**
  - error messages and logs often contain sensitive substrings; consider hashing
    `before`/`after` in logs while keeping full values for secure debug paths.
- **Deterministic retries**
  - when you re-run an AI proposer, include a stable trace id (`tid`) and keep
    prompt versions explicit so you can explain why a patch changed.
- **Human review ergonomics**
  - render `before`/`after` with visible whitespace markers and Unicode escapes
    on demand to reduce “it looks the same” confusion.

