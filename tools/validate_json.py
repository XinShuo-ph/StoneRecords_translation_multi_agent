#!/usr/bin/env python3
"""
Validate translation JSON files against the required schema.

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
    python3 validate_json.py examples/page_0020.json
"""

import json
import sys
import os
from pathlib import Path

# ── Schema Definition ──
# These must match instructions.md exactly.

REQUIRED_PAGE_FIELDS = ["page", "chapter", "total_segments", "segments", "notes"]

REQUIRED_SEGMENT_FIELDS = ["id", "type", "original", "zh_modern", "en", "ru", "ja", "commentary"]
VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue"]

REQUIRED_COMMENTARY_FIELDS = ["type", "source", "original", "zh_modern", "en", "ru", "ja"]
VALID_COMMENTARY_TYPES = ["眉批", "夹批", "侧批", "回前批", "回末批"]

TRANSLATION_LANGS = ["original", "zh_modern", "en", "ru", "ja"]


def validate_page(filepath: str) -> tuple[bool, list[str], list[str]]:
    """
    Validate a single page translation JSON file.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"], []

    # Load JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], []
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"], []

    # Check required top-level fields
    for field in REQUIRED_PAGE_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return False, errors, warnings

    # Check page is integer
    if not isinstance(data["page"], int):
        errors.append(f"'page' must be an integer, got {type(data['page']).__name__}")

    # Check chapter is non-empty string
    if not isinstance(data["chapter"], str) or not data["chapter"].strip():
        errors.append("'chapter' must be a non-empty string (e.g. '第一回', '凡例')")

    # Check notes is a non-empty list of strings
    if not isinstance(data["notes"], list):
        errors.append("'notes' must be an array")
    elif len(data["notes"]) == 0:
        errors.append("'notes' must contain at least one research note")
    else:
        for i, note in enumerate(data["notes"]):
            if not isinstance(note, str) or not note.strip():
                errors.append(f"notes[{i}]: must be a non-empty string")

    # Check segments
    segments = data["segments"]
    if not isinstance(segments, list):
        errors.append("'segments' must be an array")
        return len(errors) == 0, errors, warnings

    if len(segments) == 0:
        errors.append("'segments' array is empty — page must have at least one segment")

    # Check total_segments matches
    if isinstance(data["total_segments"], int):
        if data["total_segments"] != len(segments):
            errors.append(
                f"'total_segments' is {data['total_segments']} but 'segments' has {len(segments)} items"
            )
    else:
        errors.append(f"'total_segments' must be an integer, got {type(data['total_segments']).__name__}")

    # Validate each segment
    expected_id = 1
    for i, seg in enumerate(segments):
        prefix = f"segments[{i}]"

        # Check required fields
        for field in REQUIRED_SEGMENT_FIELDS:
            if field not in seg:
                errors.append(f"{prefix}: missing required field '{field}'")

        # Check sequential ID
        seg_id = seg.get("id")
        if seg_id != expected_id:
            errors.append(f"{prefix}: expected id={expected_id}, got id={seg_id}")
        expected_id += 1

        # Check type
        seg_type = seg.get("type")
        if seg_type not in VALID_SEGMENT_TYPES:
            errors.append(f"{prefix}: invalid type '{seg_type}', must be one of {VALID_SEGMENT_TYPES}")

        # Check translation fields are non-empty strings
        for lang in TRANSLATION_LANGS:
            val = seg.get(lang)
            if val is None:
                # Already reported as missing field above
                continue
            if not isinstance(val, str):
                errors.append(f"{prefix}.{lang}: must be a string, got {type(val).__name__}")
            elif not val.strip():
                errors.append(f"{prefix}.{lang}: must not be empty")

        # Check commentary array
        commentary = seg.get("commentary")
        if commentary is None:
            continue  # Already reported as missing field
        if not isinstance(commentary, list):
            errors.append(f"{prefix}.commentary: must be an array (use [] if no commentary)")
            continue

        for c_idx, comm in enumerate(commentary):
            c_prefix = f"{prefix}.commentary[{c_idx}]"

            for field in REQUIRED_COMMENTARY_FIELDS:
                if field not in comm:
                    errors.append(f"{c_prefix}: missing required field '{field}'")
                elif comm[field] is None or (isinstance(comm[field], str) and not comm[field].strip()):
                    errors.append(f"{c_prefix}.{field}: must not be empty")

            comm_type = comm.get("type")
            if comm_type and comm_type not in VALID_COMMENTARY_TYPES:
                warnings.append(
                    f"{c_prefix}: commentary type '{comm_type}' not in standard list {VALID_COMMENTARY_TYPES}"
                )

    # Warn about extra top-level fields
    known_fields = set(REQUIRED_PAGE_FIELDS)
    extra = set(data.keys()) - known_fields
    if extra:
        warnings.append(f"Extra top-level fields (not required): {extra}")

    return len(errors) == 0, errors, warnings


def validate_directory(dirpath: str) -> dict:
    """Validate all page_*.json files in a directory."""
    results = {}
    path = Path(dirpath)
    json_files = sorted(path.glob("page_*.json"))

    if not json_files:
        print(f"No page_*.json files found in {dirpath}")
        return results

    for filepath in json_files:
        is_valid, errors, warnings = validate_page(str(filepath))
        results[filepath.name] = (is_valid, errors, warnings)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print()
        print("Examples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        print("  python3 validate_json.py examples/page_0020.json")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors, warnings = validate_page(target)
        filename = os.path.basename(target)

        if is_valid:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            seg_count = len(data.get("segments", []))
            note_count = len(data.get("notes", []))
            comm_count = sum(
                len(s.get("commentary", [])) for s in data.get("segments", [])
            )
            print(f"PASS  {filename}: {seg_count} segments, {comm_count} commentaries, {note_count} notes")
        else:
            print(f"FAIL  {filename}")
            for err in errors:
                print(f"  ERROR: {err}")

        for warn in warnings:
            print(f"  WARN:  {warn}")

        if not is_valid:
            sys.exit(1)

    elif os.path.isdir(target):
        results = validate_directory(target)

        valid_count = 0
        invalid_count = 0

        for filename, (is_valid, errors, warnings) in results.items():
            if is_valid:
                with open(os.path.join(target, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                seg_count = len(data.get("segments", []))
                print(f"PASS  {filename}: {seg_count} segments")
                valid_count += 1
            else:
                print(f"FAIL  {filename}")
                for err in errors:
                    print(f"  ERROR: {err}")
                invalid_count += 1

            for warn in warnings:
                print(f"  WARN:  {warn}")

        print(f"\nTotal: {valid_count} passed, {invalid_count} failed")

        if invalid_count > 0:
            sys.exit(1)
    else:
        print(f"Error: '{target}' is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
