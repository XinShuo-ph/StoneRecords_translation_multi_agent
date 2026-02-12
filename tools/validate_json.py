#!/usr/bin/env python3
"""
Validate page-level translation JSON files against the canonical schema in
instructions.md.

Usage:
    python3 tools/validate_json.py translations/page_0020.json
    python3 tools/validate_json.py translations/
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REQUIRED_TOP_FIELDS = {
    "page",
    "chapter",
    "page_type",
    "source_anchor",
    "segments",
    "research_notes",
    "total_segments",
}
OPTIONAL_TOP_FIELDS = {
    "translator_notes",
    "manuscript_sources_on_page",
}
ALLOWED_TOP_FIELDS = REQUIRED_TOP_FIELDS | OPTIONAL_TOP_FIELDS

REQUIRED_SOURCE_ANCHOR_FIELDS = {"first_visible_text", "last_visible_text"}

REQUIRED_SEGMENT_FIELDS = {
    "id",
    "type",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
    "commentary",
}
ALLOWED_SEGMENT_TYPES = {"prose", "dialogue", "poem", "heading"}

REQUIRED_COMMENTARY_FIELDS = {
    "type",
    "source",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
}
ALLOWED_COMMENTARY_TYPES = {"眉批", "夹批", "侧批", "回前批", "回末批", "其他"}

ALLOWED_PAGE_TYPES = {
    "front_matter",
    "fanli",
    "chapter_start",
    "chapter_body",
    "chapter_end",
    "appendix",
}

PAGE_FILENAME_PATTERN = re.compile(r"^page_(\d{4})\.json$")


def _is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_filename_page_match(filepath: str, page_value: object, errors: List[str]) -> None:
    filename = os.path.basename(filepath)
    match = PAGE_FILENAME_PATTERN.match(filename)
    if not match:
        errors.append(
            "Filename must match page_XXXX.json (e.g., page_0020.json), "
            f"got: {filename}"
        )
        return

    if isinstance(page_value, int):
        file_page = int(match.group(1))
        if page_value != file_page:
            errors.append(
                f"page value ({page_value}) does not match filename page ({file_page})"
            )


def validate_page(filepath: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a single page JSON file.

    Returns:
        (is_valid, errors, warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"], warnings

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        return False, [f"Invalid JSON: {exc}"], warnings
    except UnicodeDecodeError as exc:
        return False, [f"Encoding error (must be UTF-8): {exc}"], warnings

    if not isinstance(data, dict):
        return False, ["Top-level JSON value must be an object"], warnings

    # Top-level key checks
    for field in sorted(REQUIRED_TOP_FIELDS):
        if field not in data:
            errors.append(f"Missing required field: {field}")

    for key in sorted(data.keys()):
        if key not in ALLOWED_TOP_FIELDS:
            errors.append(f"Unknown top-level field: {key}")

    page_value = data.get("page")
    _validate_filename_page_match(filepath, page_value, errors)

    if "page" in data and not isinstance(data["page"], int):
        errors.append("'page' must be an integer")

    if "chapter" in data and not _is_non_empty_str(data["chapter"]):
        errors.append("'chapter' must be a non-empty string")

    if "page_type" in data:
        if data["page_type"] not in ALLOWED_PAGE_TYPES:
            errors.append(
                f"page_type must be one of {sorted(ALLOWED_PAGE_TYPES)}"
            )

    # source_anchor checks
    source_anchor = data.get("source_anchor")
    if not isinstance(source_anchor, dict):
        errors.append("source_anchor must be an object")
    else:
        for field in sorted(REQUIRED_SOURCE_ANCHOR_FIELDS):
            if field not in source_anchor:
                errors.append(f"source_anchor missing field: {field}")
            elif not _is_non_empty_str(source_anchor[field]):
                errors.append(f"source_anchor.{field} must be a non-empty string")

    # research notes
    research_notes = data.get("research_notes")
    if not isinstance(research_notes, list):
        errors.append("research_notes must be an array")
    else:
        non_empty = [n for n in research_notes if _is_non_empty_str(n)]
        if len(non_empty) < 2:
            errors.append(
                "research_notes must contain at least 2 non-empty items"
            )

    # optional arrays
    if "translator_notes" in data and not isinstance(data["translator_notes"], list):
        errors.append("translator_notes must be an array when present")

    if "manuscript_sources_on_page" in data:
        sources = data["manuscript_sources_on_page"]
        if not isinstance(sources, list):
            errors.append("manuscript_sources_on_page must be an array when present")
        else:
            for idx, source in enumerate(sources):
                if not _is_non_empty_str(source):
                    errors.append(
                        f"manuscript_sources_on_page[{idx}] must be a non-empty string"
                    )

    # segment checks
    segments = data.get("segments")
    if not isinstance(segments, list):
        errors.append("segments must be an array")
        segments = []
    elif len(segments) == 0:
        errors.append("segments array is empty")

    if "total_segments" in data:
        if not isinstance(data["total_segments"], int):
            errors.append("total_segments must be an integer")
        elif isinstance(segments, list) and data["total_segments"] != len(segments):
            errors.append(
                f"total_segments ({data['total_segments']}) does not match "
                f"actual segment count ({len(segments)})"
            )

    expected_id = 1
    total_original_chars = 0
    for idx, segment in enumerate(segments):
        prefix = f"segment[{idx}]"
        if not isinstance(segment, dict):
            errors.append(f"{prefix} must be an object")
            expected_id += 1
            continue

        for field in sorted(REQUIRED_SEGMENT_FIELDS):
            if field not in segment:
                errors.append(f"{prefix} missing required field: {field}")

        for key in sorted(segment.keys()):
            if key not in REQUIRED_SEGMENT_FIELDS:
                errors.append(f"{prefix} has unknown field: {key}")

        if segment.get("id") != expected_id:
            errors.append(
                f"{prefix} id must be sequential: expected {expected_id}, "
                f"got {segment.get('id')}"
            )
        expected_id += 1

        if segment.get("type") not in ALLOWED_SEGMENT_TYPES:
            errors.append(
                f"{prefix}.type must be one of {sorted(ALLOWED_SEGMENT_TYPES)}"
            )

        for field in ["original", "zh_modern", "en", "ru", "ja"]:
            if field in segment:
                value = segment[field]
                if not _is_non_empty_str(value):
                    errors.append(f"{prefix}.{field} must be a non-empty string")
                elif field == "original":
                    total_original_chars += len(value.strip())

        commentary = segment.get("commentary")
        if not isinstance(commentary, list):
            errors.append(f"{prefix}.commentary must be an array")
            continue

        for c_idx, item in enumerate(commentary):
            c_prefix = f"{prefix}.commentary[{c_idx}]"
            if not isinstance(item, dict):
                errors.append(f"{c_prefix} must be an object")
                continue

            for field in sorted(REQUIRED_COMMENTARY_FIELDS):
                if field not in item:
                    errors.append(f"{c_prefix} missing required field: {field}")

            for key in sorted(item.keys()):
                if key not in REQUIRED_COMMENTARY_FIELDS:
                    errors.append(f"{c_prefix} has unknown field: {key}")

            if item.get("type") not in ALLOWED_COMMENTARY_TYPES:
                errors.append(
                    f"{c_prefix}.type must be one of "
                    f"{sorted(ALLOWED_COMMENTARY_TYPES)}"
                )

            if "source" in item and not _is_non_empty_str(item.get("source")):
                errors.append(f"{c_prefix}.source must be a non-empty string")

            for field in ["original", "zh_modern", "en", "ru", "ja"]:
                if field in item and not _is_non_empty_str(item.get(field)):
                    errors.append(f"{c_prefix}.{field} must be a non-empty string")

    # Heuristic warnings for likely partial output.
    if (
        data.get("page_type") == "chapter_body"
        and isinstance(segments, list)
        and len(segments) <= 2
    ):
        warnings.append(
            "Very few segments for chapter_body page (<=2). "
            "Check for partial-page translation."
        )

    if data.get("page_type") == "chapter_body" and total_original_chars < 120:
        warnings.append(
            "Low original-text character count (<120) for chapter_body page. "
            "Check for missing content."
        )

    return len(errors) == 0, errors, warnings


def validate_directory(dirpath: str) -> Dict[str, Tuple[bool, List[str], List[str]]]:
    """Validate all JSON files in a directory."""
    path = Path(dirpath)
    json_files = sorted(path.glob("*.json"))
    results: Dict[str, Tuple[bool, List[str], List[str]]] = {}

    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results

    for filepath in json_files:
        results[filepath.name] = validate_page(str(filepath))

    return results


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 tools/validate_json.py translations/page_0020.json")
        print("  python3 tools/validate_json.py translations/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        valid, errors, warnings = validate_page(target)
        filename = os.path.basename(target)
        if valid:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✓ {filename}: Valid ({len(data.get('segments', []))} segments)")
            for warning in warnings:
                print(f"  ! WARNING: {warning}")
            return

        print(f"✗ {filename}: INVALID")
        for error in errors:
            print(f"  - {error}")
        for warning in warnings:
            print(f"  ! WARNING: {warning}")
        sys.exit(1)

    if os.path.isdir(target):
        results = validate_directory(target)
        valid_count = 0
        invalid_count = 0
        warning_count = 0

        for filename, (valid, errors, warnings) in results.items():
            if valid:
                valid_count += 1
                print(f"✓ {filename}: Valid")
            else:
                invalid_count += 1
                print(f"✗ {filename}: INVALID")
                for error in errors:
                    print(f"  - {error}")

            for warning in warnings:
                warning_count += 1
                print(f"  ! WARNING: {warning}")

        print(
            f"\nSummary: {valid_count} valid, {invalid_count} invalid, "
            f"{warning_count} warnings"
        )
        if invalid_count > 0:
            sys.exit(1)
        return

    print(f"Error: {target} is not a file or directory")
    sys.exit(1)


if __name__ == "__main__":
    main()
