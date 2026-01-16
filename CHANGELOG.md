# Changelog

All notable changes to the BDIR Patch Protocol will be documented in this file.

This project follows semantic versioning.  
The specification is considered stable within a major version.

---

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

- **kindCode codebook (v1)**
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
