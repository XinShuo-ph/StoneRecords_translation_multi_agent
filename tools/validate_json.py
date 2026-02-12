#!/usr/bin/env python3
"""
Validate translation JSON files against the schema defined in translation_instructions.md.

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
    python3 validate_json.py examples/page_0020.json
"""

import json
import sys
import os
from pathlib import Path

# =============================================================================
# Schema Definition — must match translation_instructions.md Section 2
# =============================================================================

# Exactly these top-level keys are allowed, no more, no less.
REQUIRED_TOP_LEVEL_FIELDS = {
    "page": int,
    "chapter": str,
    "total_segments": int,
    "segments": list,
    "translator_notes": list,
}

# Each segment must have exactly these fields.
REQUIRED_SEGMENT_FIELDS = {
    "id": int,
    "type": str,
    "original": str,
    "zh_modern": str,
    "en": str,
    "ru": str,
    "ja": str,
    "commentary": list,
}

# Valid segment types.
VALID_SEGMENT_TYPES = {"prose", "poem", "dialogue"}

# Each commentary object must have exactly these fields.
REQUIRED_COMMENTARY_FIELDS = {
    "type": str,
    "source": str,
    "position": str,
    "original": str,
    "zh_modern": str,
    "en": str,
    "ru": str,
    "ja": str,
}

# Valid commentary types.
VALID_COMMENTARY_TYPES = {"眉批", "夹批", "侧批", "回前批", "回末批", "回末总批"}


def validate_page(filepath: str) -> tuple[bool, list[str], list[str]]:
    """
    Validate a single page JSON file.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # --- File-level checks ---
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"], []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], []
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"], []

    if not isinstance(data, dict):
        return False, ["Top-level value must be a JSON object"], []

    # --- Top-level field checks ---
    for field, expected_type in REQUIRED_TOP_LEVEL_FIELDS.items():
        if field not in data:
            errors.append(f"Missing required top-level field: '{field}'")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"Field '{field}' must be {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    # Check for unexpected top-level keys
    extra_keys = set(data.keys()) - set(REQUIRED_TOP_LEVEL_FIELDS.keys())
    if extra_keys:
        for key in sorted(extra_keys):
            errors.append(
                f"Unexpected top-level field: '{key}'. "
                f"Only allowed: {sorted(REQUIRED_TOP_LEVEL_FIELDS.keys())}"
            )

    # Stop early if top-level structure is broken
    if errors:
        return False, errors, warnings

    # --- Page number check ---
    if data["page"] < 1:
        errors.append(f"'page' must be >= 1, got {data['page']}")

    # --- Segments check ---
    segments = data["segments"]
    if len(segments) == 0:
        errors.append("'segments' array is empty — every page must have at least one segment")

    if data["total_segments"] != len(segments):
        errors.append(
            f"'total_segments' is {data['total_segments']} but 'segments' has "
            f"{len(segments)} items — these must match"
        )

    expected_id = 1
    for i, segment in enumerate(segments):
        seg_label = f"segments[{i}]"

        if not isinstance(segment, dict):
            errors.append(f"{seg_label}: must be a JSON object")
            continue

        # Check required segment fields
        for field, expected_type in REQUIRED_SEGMENT_FIELDS.items():
            if field not in segment:
                errors.append(f"{seg_label}: missing required field '{field}'")
            elif not isinstance(segment[field], expected_type):
                errors.append(
                    f"{seg_label}.{field}: must be {expected_type.__name__}, "
                    f"got {type(segment[field]).__name__}"
                )

        # Check for unexpected segment keys
        extra_seg_keys = set(segment.keys()) - set(REQUIRED_SEGMENT_FIELDS.keys())
        if extra_seg_keys:
            for key in sorted(extra_seg_keys):
                warnings.append(f"{seg_label}: unexpected field '{key}'")

        # Sequential ID check
        seg_id = segment.get("id")
        if seg_id != expected_id:
            errors.append(
                f"{seg_label}: expected id={expected_id}, got id={seg_id}"
            )
        expected_id += 1

        # Type check
        seg_type = segment.get("type")
        if isinstance(seg_type, str) and seg_type not in VALID_SEGMENT_TYPES:
            errors.append(
                f"{seg_label}.type: '{seg_type}' is invalid. "
                f"Must be one of: {sorted(VALID_SEGMENT_TYPES)}"
            )

        # Non-empty text fields
        for lang in ("original", "zh_modern", "en", "ru", "ja"):
            val = segment.get(lang)
            if isinstance(val, str):
                if len(val.strip()) == 0:
                    errors.append(f"{seg_label}.{lang}: must not be empty/whitespace")
                # Detect placeholder text
                stripped = val.strip()
                if stripped.startswith("[") and stripped.endswith("]") and len(stripped) < 200:
                    errors.append(
                        f"{seg_label}.{lang}: looks like placeholder text: '{stripped[:80]}...'. "
                        f"Must contain actual translated content, not a summary in brackets."
                    )

        # Commentary validation
        commentary_list = segment.get("commentary")
        if isinstance(commentary_list, list):
            for c_idx, comm in enumerate(commentary_list):
                c_label = f"{seg_label}.commentary[{c_idx}]"

                if not isinstance(comm, dict):
                    errors.append(f"{c_label}: must be a JSON object")
                    continue

                # Required commentary fields
                for field, expected_type in REQUIRED_COMMENTARY_FIELDS.items():
                    if field not in comm:
                        errors.append(f"{c_label}: missing required field '{field}'")
                    elif not isinstance(comm[field], expected_type):
                        errors.append(
                            f"{c_label}.{field}: must be {expected_type.__name__}, "
                            f"got {type(comm[field]).__name__}"
                        )
                    elif isinstance(comm[field], str) and len(comm[field].strip()) == 0:
                        errors.append(f"{c_label}.{field}: must not be empty")

                # Commentary type check
                comm_type = comm.get("type")
                if isinstance(comm_type, str) and comm_type not in VALID_COMMENTARY_TYPES:
                    errors.append(
                        f"{c_label}.type: '{comm_type}' is invalid. "
                        f"Must be one of: {sorted(VALID_COMMENTARY_TYPES)}"
                    )

                # Check for unexpected commentary keys
                extra_comm_keys = set(comm.keys()) - set(REQUIRED_COMMENTARY_FIELDS.keys())
                if extra_comm_keys:
                    for key in sorted(extra_comm_keys):
                        warnings.append(f"{c_label}: unexpected field '{key}'")

    # --- Translator notes check ---
    notes = data["translator_notes"]
    if len(notes) == 0:
        warnings.append("'translator_notes' is empty — you should always include research notes")
    for n_idx, note in enumerate(notes):
        if not isinstance(note, str):
            errors.append(f"translator_notes[{n_idx}]: must be a string")
        elif len(note.strip()) == 0:
            errors.append(f"translator_notes[{n_idx}]: must not be empty")

    # --- Segment count sanity ---
    if len(segments) == 1:
        warnings.append(
            "Only 1 segment — most pages have 3-8 segments. "
            "Verify you have captured all content on the page."
        )

    return len(errors) == 0, errors, warnings


def validate_directory(dirpath: str) -> dict:
    """Validate all page_*.json files in a directory."""
    results = {}
    path = Path(dirpath)
    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results
    for filepath in json_files:
        is_valid, errors, warnings = validate_page(str(filepath))
        results[filepath.name] = (is_valid, errors, warnings)
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print()
        print("Validates translation JSON files against the schema in translation_instructions.md.")
        print()
        print("Examples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        print("  python3 validate_json.py examples/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors, warnings = validate_page(target)
        filename = os.path.basename(target)

        if is_valid:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            seg_count = len(data.get("segments", []))
            comm_count = sum(
                len(s.get("commentary", []))
                for s in data.get("segments", [])
            )
            print(f"PASS  {filename}: {seg_count} segments, {comm_count} commentary annotations")
            if warnings:
                for w in warnings:
                    print(f"  WARN: {w}")
        else:
            print(f"FAIL  {filename}")
            for error in errors:
                print(f"  ERROR: {error}")
            for w in warnings:
                print(f"  WARN:  {w}")
            sys.exit(1)

    elif os.path.isdir(target):
        results = validate_directory(target)
        valid_count = 0
        invalid_count = 0
        total_segments = 0
        total_commentary = 0

        for filename, (is_valid, errors, warnings) in sorted(results.items()):
            if is_valid:
                with open(os.path.join(target, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                seg_count = len(data.get("segments", []))
                comm_count = sum(
                    len(s.get("commentary", []))
                    for s in data.get("segments", [])
                )
                total_segments += seg_count
                total_commentary += comm_count
                status = "PASS"
                print(f"  {status}  {filename}: {seg_count} segments, {comm_count} commentary")
                if warnings:
                    for w in warnings:
                        print(f"        WARN: {w}")
                valid_count += 1
            else:
                print(f"  FAIL  {filename}")
                for error in errors:
                    print(f"        ERROR: {error}")
                for w in warnings:
                    print(f"        WARN:  {w}")
                invalid_count += 1

        print()
        print(f"Summary: {valid_count} passed, {invalid_count} failed")
        print(f"Total:   {total_segments} segments, {total_commentary} commentary annotations")

        if invalid_count > 0:
            sys.exit(1)
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
