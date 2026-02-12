#!/usr/bin/env python3
"""
Validate per-page translation JSON files.

This project’s canonical output is one JSON per PDF page:
  translations/page_XXXX.json

Usage:
    python3 tools/validate_json.py translations/page_0020.json
    python3 tools/validate_json.py translations/
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


SCHEMA_VERSION = "page.v2"

ALLOWED_TOP_LEVEL_KEYS = {
    "schema_version",
    "page",
    "chapter",
    "source",
    "segments",
    "translator_notes",
    # optional
    "chapter_title",
    "page_content_type",
    "meta",
}

ALLOWED_SOURCE_KEYS = {"pdf", "page_image"}

ALLOWED_SEGMENT_KEYS = {
    "id",
    "type",
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
    "commentary",
}

ALLOWED_COMMENTARY_KEYS = {
    "type",
    "source",
    "position",     # optional, recommended
    "commentator",  # optional
    "original",
    "zh_modern",
    "en",
    "ru",
    "ja",
}

REQUIRED_SEGMENT_FIELDS = ["id", "type", "original", "zh_modern", "en", "ru", "ja", "commentary"]
REQUIRED_COMMENTARY_FIELDS = ["type", "source", "original", "zh_modern", "en", "ru", "ja"]

VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue"]
VALID_COMMENTARY_TYPES = ["眉批", "夹批", "侧批", "回前批", "回末批", "回末总批", "未知"]

VALID_PAGE_CONTENT_TYPES = [
    "front_matter",
    "fanli",
    "chapter_start",
    "chapter_body",
    "chapter_end",
    "appendix",
]


def _is_non_empty_string(v: object) -> bool:
    return isinstance(v, str) and len(v.strip()) > 0


def validate_page_file(filepath: str) -> tuple[bool, list[str]]:
    """
    Validate a single page JSON file.

    Returns:
        (is_valid, list_of_errors)
    """
    errors: list[str] = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    # Load JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"]

    if not isinstance(data, dict):
        return False, ["Top-level JSON must be an object"]

    # Enforce schema version
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be '{SCHEMA_VERSION}'")

    # Unknown top-level keys
    unknown_top = set(data.keys()) - ALLOWED_TOP_LEVEL_KEYS
    if unknown_top:
        errors.append(f"Unknown top-level keys (not allowed): {sorted(unknown_top)}")

    # page
    if "page" not in data:
        errors.append("Missing required field: page")
    elif not isinstance(data["page"], int):
        errors.append("'page' must be an integer")

    # page number must match file name when using page_XXXX.json
    m = re.search(r"page_(\d{4})\.json$", os.path.basename(filepath))
    if m and isinstance(data.get("page"), int):
        expected_page = int(m.group(1))
        if data["page"] != expected_page:
            errors.append(f"page ({data['page']}) does not match file name page_{expected_page:04d}.json")

    # chapter
    if "chapter" not in data:
        errors.append("Missing required field: chapter")
    elif not _is_non_empty_string(data["chapter"]):
        errors.append("'chapter' must be a non-empty string (e.g., '第一回', '凡例', '附录')")

    # source
    src = data.get("source")
    if not isinstance(src, dict):
        errors.append("Missing or invalid required field: source (must be an object)")
    else:
        unknown_src = set(src.keys()) - ALLOWED_SOURCE_KEYS
        if unknown_src:
            errors.append(f"source has unknown keys (not allowed): {sorted(unknown_src)}")
        if not _is_non_empty_string(src.get("pdf")):
            errors.append("source.pdf must be a non-empty string")
        if not _is_non_empty_string(src.get("page_image")):
            errors.append("source.page_image must be a non-empty string (e.g., 'source_pages/page_0020.png')")

    # translator_notes
    notes = data.get("translator_notes")
    if not isinstance(notes, list):
        errors.append("translator_notes must be an array of strings")
    else:
        if len(notes) == 0:
            errors.append("translator_notes must be non-empty (at least 1 note per page)")
        else:
            for i, n in enumerate(notes):
                if not _is_non_empty_string(n):
                    errors.append(f"translator_notes[{i}] must be a non-empty string")

    # page_content_type
    if "page_content_type" in data and data["page_content_type"] not in VALID_PAGE_CONTENT_TYPES:
        errors.append(f"page_content_type must be one of {VALID_PAGE_CONTENT_TYPES}")

    # chapter_title (optional)
    if "chapter_title" in data:
        title = data.get("chapter_title")
        if title is not None:
            if not isinstance(title, dict):
                errors.append("chapter_title must be an object if provided")
            else:
                for k in ["original", "zh_modern", "en", "ru", "ja"]:
                    if k not in title:
                        errors.append(f"chapter_title missing field: {k}")
                    elif not _is_non_empty_string(title.get(k)):
                        errors.append(f"chapter_title.{k} must be a non-empty string")

    # segments
    segments = data.get("segments")
    if not isinstance(segments, list):
        errors.append("segments must be an array")
        return len(errors) == 0, errors
    if len(segments) == 0:
        errors.append("segments array is empty")
        return len(errors) == 0, errors

    expected_id = 1
    for i, seg in enumerate(segments):
        seg_prefix = f"segments[{i}]"
        if not isinstance(seg, dict):
            errors.append(f"{seg_prefix} must be an object")
            continue

        unknown_seg = set(seg.keys()) - ALLOWED_SEGMENT_KEYS
        if unknown_seg:
            errors.append(f"{seg_prefix}: Unknown keys (not allowed): {sorted(unknown_seg)}")

        for field in REQUIRED_SEGMENT_FIELDS:
            if field not in seg:
                errors.append(f"{seg_prefix}: Missing field '{field}'")

        # id
        if seg.get("id") != expected_id:
            errors.append(f"{seg_prefix}: Expected id {expected_id}, got {seg.get('id')}")
        expected_id += 1

        # type
        if seg.get("type") not in VALID_SEGMENT_TYPES:
            errors.append(f"{seg_prefix}: Invalid type '{seg.get('type')}'. Must be one of {VALID_SEGMENT_TYPES}")

        # translations
        for lang in ["original", "zh_modern", "en", "ru", "ja"]:
            if lang not in seg:
                continue
            if not _is_non_empty_string(seg.get(lang)):
                errors.append(f"{seg_prefix}.{lang} must be a non-empty string")

        # commentary
        comm = seg.get("commentary")
        if not isinstance(comm, list):
            errors.append(f"{seg_prefix}.commentary must be an array (use [] if none)")
            continue

        for c_idx, c in enumerate(comm):
            c_prefix = f"{seg_prefix}.commentary[{c_idx}]"
            if not isinstance(c, dict):
                errors.append(f"{c_prefix} must be an object")
                continue

            unknown_c = set(c.keys()) - ALLOWED_COMMENTARY_KEYS
            if unknown_c:
                errors.append(f"{c_prefix}: Unknown keys (not allowed): {sorted(unknown_c)}")

            for field in REQUIRED_COMMENTARY_FIELDS:
                if field not in c:
                    errors.append(f"{c_prefix}: Missing field '{field}'")
                elif not _is_non_empty_string(c.get(field)):
                    errors.append(f"{c_prefix}.{field} must be a non-empty string")

            if "type" in c and c.get("type") not in VALID_COMMENTARY_TYPES:
                errors.append(f"{c_prefix}.type must be one of {VALID_COMMENTARY_TYPES}")

    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict:
    """
    Validate all JSON files in a directory.
    
    Returns:
        {filename: (is_valid, errors)}
    """
    results = {}
    
    path = Path(dirpath)
    # Prefer page_*.json; fall back to any *.json
    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results
    
    for filepath in json_files:
        is_valid, errors = validate_page_file(str(filepath))
        results[filepath.name] = (is_valid, errors)
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 tools/validate_json.py translations/page_0020.json")
        print("  python3 tools/validate_json.py translations/")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target):
        # Single file
        is_valid, errors = validate_page_file(target)
        filename = os.path.basename(target)
        
        if is_valid:
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            segment_count = len(data.get("segments", []))
            page_num = data.get("page", "?")
            print(f"✓ {filename}: Valid (page {page_num}, {segment_count} segments)")
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
                with open(os.path.join(target, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                segment_count = len(data.get("segments", []))
                page_num = data.get("page", "?")
                print(f"✓ {filename}: Valid (page {page_num}, {segment_count} segments)")
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
