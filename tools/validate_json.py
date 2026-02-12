#!/usr/bin/env python3
"""
Validate page translation JSON files for schema and completeness.

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


REQUIRED_PAGE_FIELDS = [
    "page",
    "chapter",
    "page_image",
    "page_anchor",
    "segments",
    "notes",
]
ALLOWED_PAGE_FIELDS = set(REQUIRED_PAGE_FIELDS)

REQUIRED_ANCHOR_FIELDS = ["top", "bottom"]
ALLOWED_ANCHOR_FIELDS = set(REQUIRED_ANCHOR_FIELDS)

REQUIRED_SEGMENT_FIELDS = [
    "id",
    "type",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
    "commentary",
]
ALLOWED_SEGMENT_FIELDS = set(REQUIRED_SEGMENT_FIELDS)

VALID_SEGMENT_TYPES = {"prose", "poem", "dialogue"}

REQUIRED_COMMENTARY_FIELDS = [
    "source",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
]
ALLOWED_COMMENTARY_FIELDS = set(REQUIRED_COMMENTARY_FIELDS)

PLACEHOLDER_RE = re.compile(
    r"(?i)\b(todo|tbd|placeholder|lorem ipsum|fixme)\b|待补|未翻译|未完成|待完善|\[(unclear|illegible|missing)\]"
)


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _contains_placeholder(text: str) -> bool:
    stripped = text.strip()
    if stripped in {"...", "……", "[...]", "（略）"}:
        return True
    return bool(PLACEHOLDER_RE.search(text))


def _check_unknown_keys(obj: dict, allowed: set[str], prefix: str, errors: list[str]) -> None:
    unknown = sorted(set(obj.keys()) - allowed)
    if unknown:
        errors.append(f"{prefix}: Unknown fields {unknown}")


def _check_required_string(
    obj: dict,
    field: str,
    prefix: str,
    errors: list[str],
    min_len: int = 1,
    forbid_placeholders: bool = True,
) -> None:
    value = obj.get(field)
    if not _is_non_empty_string(value):
        errors.append(f"{prefix}.{field}: Must be a non-empty string")
        return

    text = value.strip()
    if len(text) < min_len:
        errors.append(f"{prefix}.{field}: Too short (min length {min_len})")
    if forbid_placeholders and _contains_placeholder(text):
        errors.append(f"{prefix}.{field}: Contains placeholder text")


def validate_page(filepath: str) -> tuple[bool, list[str]]:
    """
    Validate a single page JSON file.

    Returns:
        (is_valid, errors)
    """
    errors: list[str] = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        return False, [f"Invalid JSON: {exc}"]
    except UnicodeDecodeError as exc:
        return False, [f"Encoding error (must be UTF-8): {exc}"]

    if not isinstance(data, dict):
        return False, ["Top-level JSON must be an object"]

    # Root schema checks
    _check_unknown_keys(data, ALLOWED_PAGE_FIELDS, "root", errors)
    for field in REQUIRED_PAGE_FIELDS:
        if field not in data:
            errors.append(f"root: Missing required field '{field}'")

    page_value = data.get("page")
    if not isinstance(page_value, int) or page_value <= 0:
        errors.append("root.page: Must be a positive integer")

    _check_required_string(data, "chapter", "root", errors)
    _check_required_string(data, "page_image", "root", errors)

    # page_image consistency
    if isinstance(page_value, int) and _is_non_empty_string(data.get("page_image")):
        expected_image = f"source_pages/page_{page_value:04d}.png"
        if data["page_image"] != expected_image:
            errors.append(
                f"root.page_image: Expected '{expected_image}', got '{data['page_image']}'"
            )

    # filename/page consistency if filename follows page_XXXX.json
    filename = os.path.basename(filepath)
    match = re.match(r"page_(\d{4})\.json$", filename)
    if match and isinstance(page_value, int):
        file_page = int(match.group(1))
        if file_page != page_value:
            errors.append(
                f"root.page: Value {page_value} does not match filename page_{file_page:04d}.json"
            )

    # page_anchor checks
    page_anchor = data.get("page_anchor")
    if not isinstance(page_anchor, dict):
        errors.append("root.page_anchor: Must be an object")
    else:
        _check_unknown_keys(page_anchor, ALLOWED_ANCHOR_FIELDS, "root.page_anchor", errors)
        for field in REQUIRED_ANCHOR_FIELDS:
            _check_required_string(
                page_anchor,
                field,
                "root.page_anchor",
                errors,
                min_len=8,
                forbid_placeholders=True,
            )

    # segments checks
    segments = data.get("segments")
    if not isinstance(segments, list):
        errors.append("root.segments: Must be an array")
        segments = []
    elif not segments:
        errors.append("root.segments: Must contain at least one segment")

    expected_id = 1
    for idx, segment in enumerate(segments):
        prefix = f"segments[{idx}]"

        if not isinstance(segment, dict):
            errors.append(f"{prefix}: Must be an object")
            continue

        _check_unknown_keys(segment, ALLOWED_SEGMENT_FIELDS, prefix, errors)
        for field in REQUIRED_SEGMENT_FIELDS:
            if field not in segment:
                errors.append(f"{prefix}: Missing required field '{field}'")

        if segment.get("id") != expected_id:
            errors.append(
                f"{prefix}.id: Expected {expected_id}, got {segment.get('id')}"
            )
        expected_id += 1

        if segment.get("type") not in VALID_SEGMENT_TYPES:
            errors.append(
                f"{prefix}.type: Must be one of {sorted(VALID_SEGMENT_TYPES)}"
            )

        for lang in ["original", "zh_modern", "en", "ru", "ja"]:
            _check_required_string(segment, lang, prefix, errors)

        commentary = segment.get("commentary")
        if not isinstance(commentary, list):
            errors.append(f"{prefix}.commentary: Must be an array")
            continue

        for c_idx, item in enumerate(commentary):
            c_prefix = f"{prefix}.commentary[{c_idx}]"
            if not isinstance(item, dict):
                errors.append(f"{c_prefix}: Must be an object")
                continue

            _check_unknown_keys(item, ALLOWED_COMMENTARY_FIELDS, c_prefix, errors)
            for field in REQUIRED_COMMENTARY_FIELDS:
                if field not in item:
                    errors.append(f"{c_prefix}: Missing required field '{field}'")
                else:
                    _check_required_string(item, field, c_prefix, errors)

    # notes checks
    notes = data.get("notes")
    if not isinstance(notes, list):
        errors.append("root.notes: Must be an array")
    else:
        if len(notes) < 2:
            errors.append("root.notes: Must contain at least 2 substantive notes")
        for i, note in enumerate(notes):
            if not _is_non_empty_string(note):
                errors.append(f"root.notes[{i}]: Must be a non-empty string")
                continue
            text = note.strip()
            if len(text) < 8:
                errors.append(f"root.notes[{i}]: Too short (min length 8)")
            if _contains_placeholder(text):
                errors.append(f"root.notes[{i}]: Contains placeholder text")

    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict[str, tuple[bool, list[str]]]:
    """
    Validate page JSON files in a directory.
    """
    results: dict[str, tuple[bool, list[str]]] = {}
    path = Path(dirpath)

    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results

    for filepath in json_files:
        is_valid, errors = validate_page(str(filepath))
        results[filepath.name] = (is_valid, errors)

    return results


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors = validate_page(target)
        filename = os.path.basename(target)

        if is_valid:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            segment_count = len(data.get("segments", []))
            print(f"✓ {filename}: Valid ({segment_count} segments)")
        else:
            print(f"✗ {filename}: INVALID")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        return

    if os.path.isdir(target):
        results = validate_directory(target)
        valid_count = 0
        invalid_count = 0

        for filename, (is_valid, errors) in results.items():
            if is_valid:
                with open(os.path.join(target, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                segment_count = len(data.get("segments", []))
                print(f"✓ {filename}: Valid ({segment_count} segments)")
                valid_count += 1
            else:
                print(f"✗ {filename}: INVALID")
                for error in errors:
                    print(f"  - {error}")
                invalid_count += 1

        print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
        if invalid_count > 0:
            sys.exit(1)
        return

    print(f"Error: {target} is not a file or directory")
    sys.exit(1)


if __name__ == "__main__":
    main()
