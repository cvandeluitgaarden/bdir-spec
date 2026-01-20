# Changelog

All notable changes to the BDIR Patch Protocol will be documented in this file.

This project follows semantic versioning.  
The specification is considered stable within a major version.

---

## [1.0.2] — 2026-01-20

### Summary

This release contains **editorial clarifications and documentation improvements only**.
No protocol semantics, schemas, validation rules, or wire formats were changed.

### Changed

- **RFC-0001**
  - Clarified the protocol subject and interaction model in the Abstract and Introduction
  - Improved readability and scanability in complex sections (Unicode normalization, validation)
  - Improved clarity around the non-mutating nature of `suggest`
  - Minor wording and heading consistency fixes

- _No changes yet._

## [1.0.2] - 2026-01-20

### Added

- **RFC-0001**
  - Normative semantics and validation rules for the `suggest` operation as a non-mutating, advisory op
  - Explicitly define Unicode normalization expectations (NFC) for canonical text, hashing, and substring matching
  - Mandate `sha256` as a MUST-implement baseline hash algorithm for Edit Packet interoperability
  - Define defaulting rule: if `ha` is omitted, receivers MUST treat it as `sha256`
  - Clarify hashes are for deterministic equality/binding and validation (not a standalone security claim)
  - Specify required top-level BDIR document metadata fields (`version`, `url`, `hash_algorithm`)
  - Define accepted `hash_algorithm` baseline and clarify Edit Packet hash truncation semantics
  - Clarify ambiguous `before` substring handling for `replace`/`delete` (require `occurrence` when `before` is non-unique; define deterministic occurrence selection)

- **AI Patch schema (v1)**
  - Require page-level hash binding on patches (`h`, `ha`) for safe application
  - Add `insert_after` wire format fields (`new_block_id`, `kind_code`, `text`)
  - Add optional `occurrence` selector for deterministic disambiguation (if omitted and `before` is non-unique, receivers MUST reject)
  - Optional `severity` field for `suggest` operations (`low` | `medium` | `high`)
  - Validation rule: `suggest` MUST NOT include `before`/`after`

- **Examples**
  - Added canonical `suggest` examples (mixed patch + suggest-only; full + ultra-min)

- **Testing**
  - Added reference validation fixtures (JSON inputs + expected outcomes) mapping to RFC sections

- **Documentation**
  - Added non-normative implementation notes covering edge cases and operational guidance
  - `docs/mental-model.md` — end-to-end conceptual overview
  - `docs/versioning-policy.md` — semantic versioning guarantees for spec releases

### Changed
- RFC-0001 updated for v1.0.2 clarifications (snake_case wire format, Unicode NFC normalization, occurrence ambiguity rules, advisory `suggest` semantics).
- Added canonical v1 JSON schemas for Edit Packet and Patch (`spec/schemas/edit-packet.v1.schema.json`, `spec/schemas/patch.v1.schema.json`).

### Notes
- This release is intended to be **non-breaking** for compliant v1 implementations; changes are clarifications + schema synchronization.

## [1.0.0] — 2026-01-16

### Added

- **RFC-0001: BDIR Patch Protocol**
  - Initial Informational specification defining the protocol model
  - Normative requirements using RFC 2119 / RFC 8174 terminology
  - Defined safety, validation, and application rules

- **Edit Packet format**
  - Ultra-minimal block-based input representation
  - Stable block identifiers, kind codes, and content hashes
  - Page-level hashing for deterministic validation

- **AI Patch format**
  - Instruction-based patch operations (`replace`, `delete`, `insert_after`, `suggest`)
  - Exact substring matching for safe application
  - Schema-enforced validation rules

- **kind_code codebook (v1)**
  - Importance-oriented block classification
  - Reserved numeric ranges for future extension

- **Examples**
  - Minimal edit packet example
  - Canonical patch example
  - Ultra-minimized patch example

- **Documentation**
  - Design rationale
  - Prompting guidelines
  - Caching and deduplication guidance

- **Project governance**
  - Apache License 2.0
  - NOTICE file
  - CONTRIBUTING and GOVERNANCE documents
  - GitHub issue and pull request templates

### Notes

- This is the **initial public release** of the BDIR Patch Protocol.
- The protocol is published as an **independent, RFC-style specification**.
- Backward compatibility is expected within the v1.x series.

---

## Future versions

Future releases may include:
- Clarifications and editorial improvements
- Additional examples and guidance
- Optional extensions that do not break v1 compatibility

Breaking changes, if ever required, will result in a new major version.

