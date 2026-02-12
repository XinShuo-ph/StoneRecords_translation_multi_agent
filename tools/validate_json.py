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
from pathlib import Path

# Required top-level fields
REQUIRED_TOP_FIELDS = ["page", "chapter", "segments", "notes"]

# Required fields for each segment
REQUIRED_SEGMENT_FIELDS = ["id", "type", "original", "zh_modern", "en", "ru", "ja", "commentary"]

# Valid segment types
VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue"]

# Required fields for commentary objects
REQUIRED_COMMENTARY_FIELDS = ["source", "original", "zh_modern", "en", "ru", "ja"]


def validate_page(filepath: str) -> tuple[bool, list[str], list[str]]:
    """
    Validate a single page translation JSON file.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Check file exists
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"], []

    # Try to load JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], []
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"], []

    # Check required top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Check page is an integer
    if "page" in data:
        if not isinstance(data["page"], int):
            errors.append("'page' must be an integer")
        else:
            # Check filename matches page number
            basename = os.path.basename(filepath)
            expected = f"page_{data['page']:04d}.json"
            if basename != expected:
                warnings.append(f"Filename '{basename}' doesn't match page number {data['page']} (expected '{expected}')")

    # Check chapter is a string
    if "chapter" in data and not isinstance(data["chapter"], str):
        errors.append("'chapter' must be a string (e.g., '第一回', '凡例')")

    # Check notes
    if "notes" in data:
        if not isinstance(data["notes"], list):
            errors.append("'notes' must be an array of strings")
        elif len(data["notes"]) == 0:
            errors.append("'notes' array is empty (minimum 3 items required)")
        elif len(data["notes"]) < 3:
            warnings.append(f"'notes' has only {len(data['notes'])} items (recommended minimum: 3)")
        else:
            for i, note in enumerate(data["notes"]):
                if not isinstance(note, str):
                    errors.append(f"notes[{i}] must be a string")
                elif len(note.strip()) == 0:
                    errors.append(f"notes[{i}] is empty")

    if errors:
        return False, errors, warnings

    # Check segments
    segments = data.get("segments", [])
    if not isinstance(segments, list):
        errors.append("'segments' must be an array")
    elif len(segments) == 0:
        errors.append("'segments' array is empty")
    else:
        total_original_chars = 0
        expected_id = 1

        for i, segment in enumerate(segments):
            prefix = f"segments[{i}]"

            # Check required fields
            for field in REQUIRED_SEGMENT_FIELDS:
                if field not in segment:
                    errors.append(f"{prefix}: Missing field '{field}'")

            # Check segment ID sequence
            if segment.get("id") != expected_id:
                errors.append(f"{prefix}: Expected id {expected_id}, got {segment.get('id')}")
            expected_id += 1

            # Check segment type
            seg_type = segment.get("type")
            if seg_type not in VALID_SEGMENT_TYPES:
                errors.append(f"{prefix}: Invalid type '{seg_type}'. Must be one of {VALID_SEGMENT_TYPES}")

            # Check all text fields are non-empty strings
            for lang in ["original", "zh_modern", "en", "ru", "ja"]:
                if lang in segment:
                    val = segment[lang]
                    if not isinstance(val, str):
                        errors.append(f"{prefix}.{lang}: Must be a string")
                    elif len(val.strip()) == 0:
                        errors.append(f"{prefix}.{lang}: Cannot be empty")

            # Track original text length
            if "original" in segment and isinstance(segment["original"], str):
                total_original_chars += len(segment["original"])

            # Validate commentary array
            if "commentary" in segment:
                if not isinstance(segment["commentary"], list):
                    errors.append(f"{prefix}.commentary: Must be an array")
                else:
                    for c_idx, commentary in enumerate(segment["commentary"]):
                        c_prefix = f"{prefix}.commentary[{c_idx}]"

                        for field in REQUIRED_COMMENTARY_FIELDS:
                            if field not in commentary:
                                errors.append(f"{c_prefix}: Missing field '{field}'")
                            elif not isinstance(commentary.get(field), str):
                                errors.append(f"{c_prefix}.{field}: Must be a string")
                            elif len(commentary.get(field, "").strip()) == 0:
                                errors.append(f"{c_prefix}.{field}: Cannot be empty")

        # Warn if very few original characters (suggests incomplete translation)
        if total_original_chars < 200:
            warnings.append(f"Total original text is only {total_original_chars} characters (typical page has 400-800). Translation may be incomplete.")

        # Warn if no commentary found on any segment
        total_commentary = sum(len(s.get("commentary", [])) for s in segments)
        if total_commentary == 0:
            warnings.append("No commentary found on any segment. Re-check the page image for red/blue commentary text.")

    return len(errors) == 0, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors, warnings = validate_page(target)
        filename = os.path.basename(target)

        if is_valid:
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            seg_count = len(data.get("segments", []))
            note_count = len(data.get("notes", []))
            total_commentary = sum(len(s.get("commentary", [])) for s in data.get("segments", []))
            print(f"PASS  {filename}: {seg_count} segments, {total_commentary} commentary, {note_count} notes")
            if warnings:
                for w in warnings:
                    print(f"  WARN: {w}")
        else:
            print(f"FAIL  {filename}")
            for error in errors:
                print(f"  ERROR: {error}")
            for w in warnings:
                print(f"  WARN: {w}")
            sys.exit(1)

    elif os.path.isdir(target):
        path = Path(target)
        json_files = sorted(path.glob("page_*.json"))
        if not json_files:
            json_files = sorted(path.glob("*.json"))

        if not json_files:
            print(f"No JSON files found in {target}")
            sys.exit(1)

        valid_count = 0
        invalid_count = 0

        for filepath in json_files:
            is_valid, errors, warnings = validate_page(str(filepath))

            if is_valid:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                seg_count = len(data.get("segments", []))
                note_count = len(data.get("notes", []))
                total_commentary = sum(len(s.get("commentary", [])) for s in data.get("segments", []))
                print(f"PASS  {filepath.name}: {seg_count} segments, {total_commentary} commentary, {note_count} notes")
                if warnings:
                    for w in warnings:
                        print(f"  WARN: {w}")
                valid_count += 1
            else:
                print(f"FAIL  {filepath.name}")
                for error in errors:
                    print(f"  ERROR: {error}")
                for w in warnings:
                    print(f"  WARN: {w}")
                invalid_count += 1

        print(f"\nSummary: {valid_count} passed, {invalid_count} failed, {valid_count + invalid_count} total")

        if invalid_count > 0:
            sys.exit(1)

    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
