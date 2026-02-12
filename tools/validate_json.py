#!/usr/bin/env python3
"""
Validate page-level translation JSON files.

Usage:
    python3 tools/validate_json.py translations/page_0020.json
    python3 tools/validate_json.py translations/
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PAGE_FILE_RE = re.compile(r"page_(\d{4})\.json$")
SOURCE_PAGE_RE = re.compile(r"page_(\d{4})\.png$")

REQUIRED_TOP_LEVEL_FIELDS = [
    "page",
    "source_page",
    "chapter",
    "segments",
    "notes",
]

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

REQUIRED_COMMENTARY_FIELDS = [
    "type",
    "source",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
]

VALID_SEGMENT_TYPES = {"prose", "poem", "dialogue", "other"}
VALID_COMMENTARY_TYPES = {"眉批", "夹批", "侧批", "回前批", "回末批", "回末总批", "其他"}
TRANSLATION_TEXT_FIELDS = ["original", "zh_modern", "en", "ru", "ja"]


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load_json(filepath: str) -> Tuple[Optional[dict], List[str]]:
    if not os.path.exists(filepath):
        return None, [f"File not found: {filepath}"]

    try:
        with open(filepath, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        return None, [f"Invalid JSON: {exc}"]
    except UnicodeDecodeError as exc:
        return None, [f"Encoding error (must be UTF-8): {exc}"]

    if not isinstance(data, dict):
        return None, ["Top-level JSON value must be an object"]
    return data, []


def _validate_filename_consistency(filepath: str, data: dict, errors: List[str]) -> None:
    filename = os.path.basename(filepath)
    match = PAGE_FILE_RE.fullmatch(filename)
    if not match:
        errors.append(
            "Filename must match page_XXXX.json (for example: page_0020.json)"
        )
        return

    expected_page = int(match.group(1))
    expected_source_page = f"page_{expected_page:04d}.png"

    page_value = data.get("page")
    if isinstance(page_value, int) and page_value != expected_page:
        errors.append(
            f"'page' ({page_value}) does not match filename page number ({expected_page})"
        )

    source_page = data.get("source_page")
    if isinstance(source_page, str) and source_page != expected_source_page:
        errors.append(
            f"'source_page' ('{source_page}') must be '{expected_source_page}'"
        )


def validate_page_payload(data: dict, filepath: str) -> List[str]:
    errors: List[str] = []

    missing_top = sorted(set(REQUIRED_TOP_LEVEL_FIELDS) - set(data.keys()))
    if missing_top:
        for field in missing_top:
            errors.append(f"Missing required top-level field: {field}")

    unknown_top = sorted(set(data.keys()) - set(REQUIRED_TOP_LEVEL_FIELDS))
    if unknown_top:
        errors.append(
            "Unknown top-level fields: "
            + ", ".join(unknown_top)
            + ". Use only: "
            + ", ".join(REQUIRED_TOP_LEVEL_FIELDS)
        )

    if "page" in data:
        if not isinstance(data["page"], int):
            errors.append("'page' must be an integer")
        elif data["page"] <= 0:
            errors.append("'page' must be greater than 0")

    if "source_page" in data:
        source_page = data["source_page"]
        if not isinstance(source_page, str):
            errors.append("'source_page' must be a string like page_0020.png")
        elif not SOURCE_PAGE_RE.fullmatch(source_page):
            errors.append("'source_page' must match page_XXXX.png")

    if "chapter" in data and not _is_non_empty_string(data["chapter"]):
        errors.append("'chapter' must be a non-empty string")

    if "notes" in data:
        notes = data["notes"]
        if not isinstance(notes, list):
            errors.append("'notes' must be an array")
        elif not notes:
            errors.append("'notes' must not be empty")
        else:
            for idx, note in enumerate(notes):
                if not _is_non_empty_string(note):
                    errors.append(f"notes[{idx}] must be a non-empty string")

    segments = data.get("segments")
    if segments is None:
        # Missing key is already reported above.
        segments = []

    if not isinstance(segments, list):
        errors.append("'segments' must be an array")
        segments = []
    elif not segments:
        errors.append("'segments' must not be empty")

    expected_id = 1
    for idx, segment in enumerate(segments):
        prefix = f"segments[{idx}]"

        if not isinstance(segment, dict):
            errors.append(f"{prefix} must be an object")
            continue

        missing_segment = sorted(set(REQUIRED_SEGMENT_FIELDS) - set(segment.keys()))
        for field in missing_segment:
            errors.append(f"{prefix}: Missing field '{field}'")

        unknown_segment = sorted(set(segment.keys()) - set(REQUIRED_SEGMENT_FIELDS))
        if unknown_segment:
            errors.append(
                f"{prefix}: Unknown fields {unknown_segment}. "
                f"Use only {REQUIRED_SEGMENT_FIELDS}"
            )

        segment_id = segment.get("id")
        if not isinstance(segment_id, int):
            errors.append(f"{prefix}.id must be an integer")
        elif segment_id != expected_id:
            errors.append(
                f"{prefix}.id must be {expected_id}, got {segment_id}"
            )
        expected_id += 1

        segment_type = segment.get("type")
        if segment_type not in VALID_SEGMENT_TYPES:
            errors.append(
                f"{prefix}.type must be one of {sorted(VALID_SEGMENT_TYPES)}"
            )

        for field in TRANSLATION_TEXT_FIELDS:
            value = segment.get(field)
            if not _is_non_empty_string(value):
                errors.append(f"{prefix}.{field} must be a non-empty string")

        commentary = segment.get("commentary")
        if not isinstance(commentary, list):
            errors.append(f"{prefix}.commentary must be an array")
            continue

        for c_idx, comment in enumerate(commentary):
            c_prefix = f"{prefix}.commentary[{c_idx}]"
            if not isinstance(comment, dict):
                errors.append(f"{c_prefix} must be an object")
                continue

            missing_commentary = sorted(
                set(REQUIRED_COMMENTARY_FIELDS) - set(comment.keys())
            )
            for field in missing_commentary:
                errors.append(f"{c_prefix}: Missing field '{field}'")

            unknown_commentary = sorted(
                set(comment.keys()) - set(REQUIRED_COMMENTARY_FIELDS)
            )
            if unknown_commentary:
                errors.append(
                    f"{c_prefix}: Unknown fields {unknown_commentary}. "
                    f"Use only {REQUIRED_COMMENTARY_FIELDS}"
                )

            commentary_type = comment.get("type")
            if commentary_type not in VALID_COMMENTARY_TYPES:
                errors.append(
                    f"{c_prefix}.type must be one of {sorted(VALID_COMMENTARY_TYPES)}"
                )

            if not _is_non_empty_string(comment.get("source")):
                errors.append(f"{c_prefix}.source must be a non-empty string")

            for field in TRANSLATION_TEXT_FIELDS:
                value = comment.get(field)
                if not _is_non_empty_string(value):
                    errors.append(f"{c_prefix}.{field} must be a non-empty string")

    _validate_filename_consistency(filepath, data, errors)
    return errors


def validate_page_file(filepath: str) -> Tuple[bool, List[str], Optional[dict]]:
    data, load_errors = _load_json(filepath)
    if load_errors:
        return False, load_errors, None

    assert data is not None
    errors = validate_page_payload(data, filepath)
    return len(errors) == 0, errors, data


def validate_directory(dirpath: str) -> Dict[str, Tuple[bool, List[str], Optional[dict]]]:
    results: Dict[str, Tuple[bool, List[str], Optional[dict]]] = {}
    path = Path(dirpath)
    json_files = sorted(path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results

    for filepath in json_files:
        results[filepath.name] = validate_page_file(str(filepath))

    return results


def _format_valid_summary(data: dict) -> str:
    segments = data.get("segments", [])
    segment_count = len(segments) if isinstance(segments, list) else 0
    commentary_count = 0
    if isinstance(segments, list):
        for segment in segments:
            if isinstance(segment, dict) and isinstance(segment.get("commentary"), list):
                commentary_count += len(segment["commentary"])
    return f"Valid ({segment_count} segments, {commentary_count} commentary items)"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 tools/validate_json.py translations/page_0020.json")
        print("  python3 tools/validate_json.py translations/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors, data = validate_page_file(target)
        filename = os.path.basename(target)
        if is_valid and data is not None:
            print(f"✓ {filename}: {_format_valid_summary(data)}")
            return

        print(f"✗ {filename}: INVALID")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if os.path.isdir(target):
        results = validate_directory(target)
        valid_count = 0
        invalid_count = 0

        for filename, (is_valid, errors, data) in results.items():
            if is_valid and data is not None:
                print(f"✓ {filename}: {_format_valid_summary(data)}")
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
