#!/usr/bin/env python3
"""
Validate translation JSON files for completeness and format.

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
"""

import json
import sys
import os
import re
from pathlib import Path

# Canonical top-level keys (strict for consistency)
REQUIRED_TOP_LEVEL_KEYS = ["page", "chapter", "segments", "notes"]
ALLOWED_TOP_LEVEL_KEYS = set(REQUIRED_TOP_LEVEL_KEYS)

# Required fields for each segment (strict for consistency)
REQUIRED_SEGMENT_KEYS = [
    "id",
    "type",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
    "commentary",
]
ALLOWED_SEGMENT_KEYS = set(REQUIRED_SEGMENT_KEYS)

# Valid segment types
VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue"]

# Required fields for commentary objects
REQUIRED_COMMENTARY_KEYS = ["source", "original", "zh_modern", "en", "ru", "ja"]

# Placeholder checks targeting observed failure patterns.
BRACKET_PLACEHOLDER_RE = re.compile(r"^\s*\[[^\]]+\]\s*$")
PLACEHOLDER_MARKERS = [
    "todo",
    "tbd",
    "placeholder",
    "to be translated",
    "not translated",
]
PAGE_FILENAME_RE = re.compile(r"page_(\d{4})\.json$")


def is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def looks_like_placeholder(text: str) -> bool:
    stripped = text.strip()
    lowered = stripped.lower()

    # e.g. "[Dialogue between ...]"
    if BRACKET_PLACEHOLDER_RE.match(stripped):
        inner = stripped[1:-1]
        if any(ch.isalpha() for ch in inner):
            return True

    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def validate_commentary_array(commentary: object, prefix: str, errors: list[str]) -> None:
    if not isinstance(commentary, list):
        errors.append(f"{prefix}: must be an array")
        return

    for c_idx, item in enumerate(commentary, start=1):
        c_prefix = f"{prefix}[{c_idx}]"

        if not isinstance(item, dict):
            errors.append(f"{c_prefix}: must be an object")
            continue

        for key in REQUIRED_COMMENTARY_KEYS:
            if key not in item:
                errors.append(f"{c_prefix}: missing key '{key}'")
                continue
            if not is_non_empty_str(item[key]):
                errors.append(f"{c_prefix}.{key}: must be a non-empty string")
                continue
            if looks_like_placeholder(item[key]):
                errors.append(f"{c_prefix}.{key}: placeholder-like content is not allowed")


def validate_file(filepath: str) -> tuple[bool, list[str]]:
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
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"]

    if not isinstance(data, dict):
        return False, ["Top-level JSON must be an object"]

    # Top-level keys: required + no extras.
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            errors.append(f"Missing required key: '{key}'")

    extra_top_keys = sorted(set(data.keys()) - ALLOWED_TOP_LEVEL_KEYS)
    if extra_top_keys:
        errors.append(
            "Unexpected top-level keys: "
            + ", ".join(extra_top_keys)
            + " (allowed: page, chapter, segments, notes)"
        )

    # page
    page = data.get("page")
    if not isinstance(page, int) or page <= 0:
        errors.append("'page' must be a positive integer")

    # Check filename/page consistency when possible.
    basename = os.path.basename(filepath)
    match = PAGE_FILENAME_RE.match(basename)
    if match and isinstance(page, int):
        expected_page = int(match.group(1))
        if page != expected_page:
            errors.append(
                f"Filename-page mismatch: file is page_{expected_page:04d}.json but 'page' is {page}"
            )

    # chapter
    if not is_non_empty_str(data.get("chapter")):
        errors.append("'chapter' must be a non-empty string")

    # notes
    notes = data.get("notes")
    if not isinstance(notes, list):
        errors.append("'notes' must be an array")
    else:
        if len(notes) < 3:
            errors.append("'notes' must contain at least 3 items")
        for idx, note in enumerate(notes, start=1):
            prefix = f"notes[{idx}]"
            if not is_non_empty_str(note):
                errors.append(f"{prefix}: must be a non-empty string")
                continue
            if len(note.strip()) < 8:
                errors.append(f"{prefix}: is too short to be a meaningful research note")
            if looks_like_placeholder(note):
                errors.append(f"{prefix}: placeholder-like content is not allowed")

    # segments
    segments = data.get("segments")
    if not isinstance(segments, list):
        errors.append("'segments' must be an array")
        return len(errors) == 0, errors

    if not segments:
        errors.append("'segments' must not be empty")
        return len(errors) == 0, errors

    expected_id = 1
    for idx, segment in enumerate(segments, start=1):
        s_prefix = f"segments[{idx}]"

        if not isinstance(segment, dict):
            errors.append(f"{s_prefix}: must be an object")
            continue

        for key in REQUIRED_SEGMENT_KEYS:
            if key not in segment:
                errors.append(f"{s_prefix}: missing key '{key}'")

        extra_segment_keys = sorted(set(segment.keys()) - ALLOWED_SEGMENT_KEYS)
        if extra_segment_keys:
            errors.append(
                f"{s_prefix}: unexpected keys: {', '.join(extra_segment_keys)} "
                "(allowed: id, type, original, zh_modern, en, ru, ja, commentary)"
            )

        if segment.get("id") != expected_id:
            errors.append(
                f"{s_prefix}.id: expected {expected_id}, got {segment.get('id')}"
            )
        expected_id += 1

        seg_type = segment.get("type")
        if seg_type not in VALID_SEGMENT_TYPES:
            errors.append(
                f"{s_prefix}.type: invalid '{seg_type}' (must be one of {VALID_SEGMENT_TYPES})"
            )

        for key in ["original", "zh_modern", "en", "ru", "ja"]:
            value = segment.get(key)
            if not is_non_empty_str(value):
                errors.append(f"{s_prefix}.{key}: must be a non-empty string")
                continue
            if looks_like_placeholder(value):
                errors.append(f"{s_prefix}.{key}: placeholder-like content is not allowed")

        validate_commentary_array(segment.get("commentary"), f"{s_prefix}.commentary", errors)

    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict:
    """
    Validate all page JSON files in a directory.

    Returns: {filename: (is_valid, errors)}
    """
    results = {}

    path = Path(dirpath)
    # Canonical names first
    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results

    for filepath in json_files:
        is_valid, errors = validate_file(str(filepath))
        results[filepath.name] = (is_valid, errors)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        # Single file
        is_valid, errors = validate_file(target)
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

    elif os.path.isdir(target):
        # Directory
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

    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
