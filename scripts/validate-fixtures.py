#!/usr/bin/env python3
"""Validate reference fixtures and examples against the normative JSON Schemas.

This script is intentionally lightweight and has no repo-local dependencies.
CI installs `jsonschema` at runtime.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]

SCHEMA_EDIT_PACKET = REPO_ROOT / "spec" / "schemas" / "bdir-edit-packet.ultra-min.v1.schema.json"
SCHEMA_PATCH = REPO_ROOT / "spec" / "schemas" / "ai-patch.schema.json"

FIXTURES_DIR = REPO_ROOT / "spec" / "fixtures" / "validation"
EXAMPLES_DIR = REPO_ROOT / "spec" / "examples"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validator(schema_path: Path) -> Draft202012Validator:
    schema = load_json(schema_path)
    return Draft202012Validator(schema)


def format_error(e) -> str:
    loc = "/".join([str(p) for p in e.absolute_path])
    if loc:
        loc = f"/{loc}"
    return f"{loc}: {e.message}"


def validate_instance(v: Draft202012Validator, instance: Any) -> List[str]:
    return [format_error(e) for e in sorted(v.iter_errors(instance), key=lambda x: x.path)]


def main() -> int:
    v_packet = validator(SCHEMA_EDIT_PACKET)
    v_patch = validator(SCHEMA_PATCH)

    failures: List[Tuple[str, str]] = []

    # --- Fixtures ---
    for path in sorted(FIXTURES_DIR.glob("v*.json")):
        data = load_json(path)

        expected_valid = bool(data.get("expect", {}).get("valid", True))

        # Validate embedded packet/patch (if present).
        # If a fixture expects invalid behavior, it may be schema-invalid (e.g. missing block_id)
        # or schema-valid but semantically invalid (e.g. page hash mismatch). We only fail the
        # validation run when a fixture that claims to be valid is not schema-valid.
        if "packet" in data:
            errs = validate_instance(v_packet, data["packet"])
            if expected_valid:
                for err in errs:
                    failures.append((str(path.relative_to(REPO_ROOT)), f"packet{err}"))

        if "patch" in data:
            errs = validate_instance(v_patch, data["patch"])
            if expected_valid:
                for err in errs:
                    failures.append((str(path.relative_to(REPO_ROOT)), f"patch{err}"))

    # --- Examples (best-effort) ---
    example_packet_files = [
        EXAMPLES_DIR / "edit-packet.min.json",
    ]
    for path in example_packet_files:
        if not path.exists():
            continue
        data = load_json(path)
        errs = validate_instance(v_packet, data)
        for err in errs:
            failures.append((str(path.relative_to(REPO_ROOT)), err))

    example_patch_files = [
        EXAMPLES_DIR / "patch.example.json",
        EXAMPLES_DIR / "patch.min.example.json",
        EXAMPLES_DIR / "patch.suggest.example.json",
        EXAMPLES_DIR / "patch.suggest.min.example.json",
    ]
    for path in example_patch_files:
        if not path.exists():
            continue
        data = load_json(path)
        errs = validate_instance(v_patch, data)
        for err in errs:
            failures.append((str(path.relative_to(REPO_ROOT)), err))

    if failures:
        print("Schema validation failures:\n")
        for file, err in failures:
            print(f"- {file}: {err}")
        return 1

    print("OK: fixtures and examples validate against schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
