#!/usr/bin/env python3
"""
Validate translation JSON files against the format defined in instructions.md.

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
    python3 validate_json.py examples/

Exit code 0 = all valid, 1 = errors found.
"""

import json
import sys
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema: exactly the fields from instructions.md, no more, no fewer.
# ---------------------------------------------------------------------------

REQUIRED_TOP_FIELDS = {"page", "chapter", "segments", "notes"}
VALID_SEGMENT_TYPES = {"prose", "poem", "dialogue"}
REQUIRED_SEGMENT_FIELDS = {"id", "type", "original", "zh_modern", "en", "ru", "ja", "commentary"}
TRANSLATION_FIELDS = {"original", "zh_modern", "en", "ru", "ja"}
REQUIRED_COMMENTARY_FIELDS = {"source", "original", "zh_modern", "en", "ru", "ja"}


def validate_page(filepath: str) -> tuple[bool, list[str]]:
    """Validate a single page JSON file. Returns (is_valid, errors)."""
    errors: list[str] = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    # -- Parse JSON --------------------------------------------------------
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"]

    if not isinstance(data, dict):
        return False, ["Top-level value must be a JSON object"]

    # -- Top-level fields --------------------------------------------------
    actual_top = set(data.keys())
    missing_top = REQUIRED_TOP_FIELDS - actual_top
    extra_top = actual_top - REQUIRED_TOP_FIELDS
    for f in sorted(missing_top):
        errors.append(f"Missing required top-level field: '{f}'")
    for f in sorted(extra_top):
        errors.append(f"Unexpected top-level field: '{f}' (remove it)")

    if "page" in data and not isinstance(data["page"], int):
        errors.append("'page' must be an integer")

    if "chapter" in data and not isinstance(data["chapter"], str):
        errors.append("'chapter' must be a string (e.g. '第一回')")

    if "notes" in data:
        if not isinstance(data["notes"], list):
            errors.append("'notes' must be an array of strings")
        else:
            for i, note in enumerate(data["notes"]):
                if not isinstance(note, str):
                    errors.append(f"notes[{i}]: must be a string")

    # -- Segments ----------------------------------------------------------
    segments = data.get("segments")
    if segments is None:
        pass  # already reported as missing
    elif not isinstance(segments, list):
        errors.append("'segments' must be an array")
    elif len(segments) == 0:
        errors.append("'segments' array must not be empty")
    else:
        expected_id = 1
        for idx, seg in enumerate(segments):
            prefix = f"segments[{idx}]"

            if not isinstance(seg, dict):
                errors.append(f"{prefix}: must be a JSON object")
                continue

            # Field presence
            seg_keys = set(seg.keys())
            missing_seg = REQUIRED_SEGMENT_FIELDS - seg_keys
            extra_seg = seg_keys - REQUIRED_SEGMENT_FIELDS
            for f in sorted(missing_seg):
                errors.append(f"{prefix}: missing required field '{f}'")
            for f in sorted(extra_seg):
                errors.append(f"{prefix}: unexpected field '{f}' (remove it)")

            # Sequential ID
            if "id" in seg:
                if seg["id"] != expected_id:
                    errors.append(f"{prefix}: expected id={expected_id}, got {seg['id']}")
                expected_id = (seg["id"] if isinstance(seg["id"], int) else expected_id) + 1

            # Segment type
            if "type" in seg and seg["type"] not in VALID_SEGMENT_TYPES:
                errors.append(
                    f"{prefix}: invalid type '{seg['type']}' "
                    f"(must be one of {sorted(VALID_SEGMENT_TYPES)})"
                )

            # Translation text fields
            for lang in TRANSLATION_FIELDS:
                val = seg.get(lang)
                if val is None:
                    pass  # already reported as missing field
                elif not isinstance(val, str):
                    errors.append(f"{prefix}.{lang}: must be a string")
                elif len(val.strip()) == 0:
                    errors.append(f"{prefix}.{lang}: must not be empty")

            # Commentary array
            commentary = seg.get("commentary")
            if commentary is None:
                pass  # already reported as missing
            elif not isinstance(commentary, list):
                errors.append(f"{prefix}.commentary: must be an array (use [] if none)")
            else:
                for c_idx, comm in enumerate(commentary):
                    c_prefix = f"{prefix}.commentary[{c_idx}]"

                    if not isinstance(comm, dict):
                        errors.append(f"{c_prefix}: must be a JSON object")
                        continue

                    comm_keys = set(comm.keys())
                    missing_c = REQUIRED_COMMENTARY_FIELDS - comm_keys
                    extra_c = comm_keys - REQUIRED_COMMENTARY_FIELDS
                    for f in sorted(missing_c):
                        errors.append(f"{c_prefix}: missing required field '{f}'")
                    for f in sorted(extra_c):
                        errors.append(f"{c_prefix}: unexpected field '{f}' (remove it)")

                    for lang in REQUIRED_COMMENTARY_FIELDS:
                        val = comm.get(lang)
                        if val is not None:
                            if not isinstance(val, str):
                                errors.append(f"{c_prefix}.{lang}: must be a string")
                            elif len(val.strip()) == 0:
                                errors.append(f"{c_prefix}.{lang}: must not be empty")

    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict[str, tuple[bool, list[str]]]:
    """Validate all page_*.json files in a directory."""
    results = {}
    path = Path(dirpath)
    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {dirpath}")
    for fp in json_files:
        results[fp.name] = validate_page(str(fp))
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print()
        print("Examples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        print("  python3 validate_json.py examples/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        is_valid, errors = validate_page(target)
        name = os.path.basename(target)
        if is_valid:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            n = len(data.get("segments", []))
            print(f"PASS  {name} ({n} segments)")
        else:
            print(f"FAIL  {name}")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)

    elif os.path.isdir(target):
        results = validate_directory(target)
        ok = 0
        bad = 0
        for name, (is_valid, errors) in results.items():
            if is_valid:
                with open(os.path.join(target, name), "r", encoding="utf-8") as f:
                    data = json.load(f)
                n = len(data.get("segments", []))
                print(f"PASS  {name} ({n} segments)")
                ok += 1
            else:
                print(f"FAIL  {name}")
                for e in errors:
                    print(f"  - {e}")
                bad += 1
        print(f"\nSummary: {ok} passed, {bad} failed")
        if bad > 0:
            sys.exit(1)
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
