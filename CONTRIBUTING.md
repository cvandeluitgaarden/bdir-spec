# Contributing to the BDIR Patch Protocol

Thank you for your interest in contributing to the BDIR Patch Protocol.

This repository defines a **specification**, not a software product. Contributions are therefore evaluated primarily on clarity, correctness, and interoperability.

---

## Scope of contributions

Contributions are welcome in the following areas:

- Clarifications or corrections to the RFC text
- Improvements to JSON Schemas or codebooks
- Additional examples that improve understanding
- Documentation improvements (design notes, guidance)
- Reports of ambiguities or edge cases found in practice

Out of scope:
- Domain-specific extraction heuristics
- AI prompt tuning or orchestration logic
- Tooling that is not directly related to the specification

---

## How to contribute

### 1. Open an issue first (recommended)

For non-trivial changes, please open an issue using one of the templates:
- **Bug report** – for errors or ambiguities
- **Specification change** – for proposed extensions or behavior changes

This helps align on intent before implementation work begins.

### 2. Submit a pull request

Pull requests should:

- Be focused and minimal
- Update all affected artifacts consistently (RFC, schema, examples)
- Clearly state compatibility impact (backward compatible vs breaking)
- Reference the relevant issue, if applicable

---

## Compatibility and versioning

- Backward-compatible clarifications and extensions may be included in minor versions.
- Breaking changes require a major version bump.
- The maintainers reserve the right to defer or reject changes that reduce safety, determinism, or clarity.

---

## Editorial vs normative changes

Please distinguish clearly between:

- **Editorial changes** (wording, formatting, examples)
- **Normative changes** (behavior, requirements, semantics)

Normative changes require stronger justification and review.

---

## Code of conduct

This project follows standard open-source collaboration norms:
- Be respectful
- Assume good intent
- Focus discussions on technical merit

---

## License

By contributing, you agree that your contributions will be licensed under the **Apache License 2.0**, consistent with the rest of the project.

## Branching & Release Process

See:
- `docs/branching-and-release.md` for the branch model and release flow
- `docs/semver-policy.md` for when changes belong in 1.1 vs 2.0
- `.github/rulesets/` for example GitHub Ruleset JSON
- `.github/ci-required-checks.md` for the required check contexts used by branch protection
