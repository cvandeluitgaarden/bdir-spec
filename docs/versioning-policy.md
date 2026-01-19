# Versioning Policy

This document is **non-normative**. It describes how versions of the BDIR Patch Protocol are published.

## Semantic versioning

The project follows semantic versioning: `MAJOR.MINOR.PATCH`.

## Version meaning

### Patch releases (`1.0.x`)

Patch releases are intended to be **stable and non-breaking**. They may include:

- Editorial clarifications to the RFC (no change in normative semantics)
- Additional non-normative documentation
- Example additions or reformatting that do not change meaning
- Packaging and repository hygiene changes

Patch releases must not:

- Change wire formats
- Change validation requirements
- Add or remove normative requirements

### Minor releases (`1.x`)

Minor releases may add **backward-compatible** extensions, such as:

- New optional fields that receivers may ignore
- Additional optional operation types with clear validation rules
- New codebook ranges or reserved values

### Major releases (`2.0`)

Major releases may include breaking changes, such as:

- Incompatible wire-format revisions
- Semantic changes to existing operations or validation rules

## Practical guidance

If you implement v1, you should expect all `1.0.x` releases to be safe to adopt without code changes.