#!/usr/bin/env python3
"""
Validate translation JSON files for completeness and format (V2 Schema).

Supports 3-tier validation:
- Tier 1 (Minimum): Required fields only
- Tier 2 (Good): With commentary and notes
- Tier 3 (Excellent): With all enhancements

Usage:
    python3 validate_json.py translations/page_0020.json
    python3 validate_json.py translations/
    python3 validate_json.py --verbose translations/page_0020.json
"""

import json
import sys
import os
from pathlib import Path

# V2 Schema: Only truly required fields
REQUIRED_PAGE_FIELDS = [
    "page",
    "chapter",
    "segments"
]

# Optional but recommended for Tier 2
RECOMMENDED_PAGE_FIELDS = [
    "notes"  # or "translator_notes"
]

# Required fields for chapter title (optional, only if chapter_title present)
REQUIRED_TITLE_FIELDS = ["original", "zh_modern", "en", "ru", "ja"]

# Required fields for each segment
REQUIRED_SEGMENT_FIELDS = ["id", "type", "original", "zh_modern", "en", "ru", "ja"]

# Valid segment types
VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue"]

# Required fields for commentary objects (when commentary is present)
REQUIRED_COMMENTARY_FIELDS = ["source", "original", "zh_modern", "en", "ru", "ja"]

# Optional commentary fields
OPTIONAL_COMMENTARY_FIELDS = ["type", "position"]

# Valid commentary types
VALID_COMMENTARY_TYPES = ["眉批", "夹批", "侧批", "回前批", "回末批", "回末总批"]

# Verbose mode flag
VERBOSE = False


def validate_chapter(filepath: str) -> tuple[bool, list[str]]:
    """
    Validate a single chapter JSON file.
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    
    # Check file exists
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    # Try to load JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except UnicodeDecodeError as e:
        return False, [f"Encoding error (must be UTF-8): {e}"]
    
    # Check required page fields
    for field in REQUIRED_PAGE_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check page is an integer
    if "page" in data and not isinstance(data["page"], int):
        errors.append("'page' must be an integer")
    
    # Check chapter is a string
    if "chapter" in data and not isinstance(data["chapter"], str):
        errors.append("'chapter' must be a string (e.g., '第一回', '凡例', '附录')")
    
    if errors:
        return False, errors
    
    # Check chapter title (optional - only required if present)
    if "chapter_title" in data and data["chapter_title"]:
        if isinstance(data.get("chapter_title"), dict):
            for field in REQUIRED_TITLE_FIELDS:
                if field not in data["chapter_title"]:
                    errors.append(f"Missing title field: chapter_title.{field}")
                elif not data["chapter_title"][field]:
                    errors.append(f"Empty title field: chapter_title.{field}")
        else:
            errors.append("chapter_title must be an object if provided")
    
    # Check segments
    segments = data.get("segments", [])
    if not isinstance(segments, list):
        errors.append("segments must be an array")
    elif len(segments) == 0:
        errors.append("segments array is empty")
    else:
        expected_id = 1
        for i, segment in enumerate(segments):
            segment_prefix = f"segment[{i}]"
            
            # Check required fields
            for field in REQUIRED_SEGMENT_FIELDS:
                if field not in segment:
                    errors.append(f"{segment_prefix}: Missing field '{field}'")
                elif segment[field] is None or segment[field] == "":
                    errors.append(f"{segment_prefix}: Empty field '{field}'")
            
            # Check segment ID sequence
            if segment.get("id") != expected_id:
                errors.append(f"{segment_prefix}: Expected id {expected_id}, got {segment.get('id')}")
            expected_id += 1
            
            # Check segment type
            if segment.get("type") not in VALID_SEGMENT_TYPES:
                errors.append(f"{segment_prefix}: Invalid type '{segment.get('type')}'. Must be one of {VALID_SEGMENT_TYPES}")
            
            # Check translations are non-empty strings
            for lang in ["original", "zh_modern", "en", "ru", "ja"]:
                if lang in segment:
                    val = segment[lang]
                    if not isinstance(val, str):
                        errors.append(f"{segment_prefix}.{lang}: Must be a string")
                    elif len(val.strip()) == 0:
                        errors.append(f"{segment_prefix}.{lang}: Cannot be empty/whitespace")
            
            # If poem, check for poem_notes (warning, not error)
            if segment.get("type") == "poem" and "poem_notes" not in segment:
                # This is just a warning, not an error
                pass
            
            # Validate commentary array if present
            if "commentary" in segment and segment["commentary"]:
                for c_idx, commentary in enumerate(segment["commentary"]):
                    c_prefix = f"{segment_prefix}.commentary[{c_idx}]"
                    
                    # Check required commentary fields
                    for field in REQUIRED_COMMENTARY_FIELDS:
                        if field not in commentary:
                            errors.append(f"{c_prefix}: Missing required field '{field}'")
                        elif commentary[field] is None or commentary[field] == "":
                            errors.append(f"{c_prefix}: Empty field '{field}'")
                    
                    # Check commentary type is valid (if present - optional)
                    if "type" in commentary and commentary.get("type") not in VALID_COMMENTARY_TYPES:
                        errors.append(f"{c_prefix}: Invalid commentary type '{commentary.get('type')}'. Must be one of {VALID_COMMENTARY_TYPES}")
    
    # Check total_segments matches actual count (if present - optional)
    if "total_segments" in data and data.get("total_segments") != len(segments):
        errors.append(f"total_segments ({data.get('total_segments')}) does not match actual segment count ({len(segments)})")
    
    # Check translator_notes or notes is a list (if present - optional for Tier 1)
    if "translator_notes" in data and not isinstance(data.get("translator_notes"), list):
        errors.append("translator_notes must be an array")
    if "notes" in data and not isinstance(data.get("notes"), list):
        errors.append("notes must be an array")
    
    # Check page_content_type if present
    valid_content_types = ["front_matter", "fanli", "chapter_start", "chapter_body", "chapter_end", "appendix"]
    if "page_content_type" in data:
        if data["page_content_type"] not in valid_content_types:
            errors.append(f"page_content_type must be one of {valid_content_types}")
    
    # Check chapter_end_commentary if present
    if "chapter_end_commentary" in data and data["chapter_end_commentary"]:
        for c_idx, commentary in enumerate(data["chapter_end_commentary"]):
            c_prefix = f"chapter_end_commentary[{c_idx}]"
            for field in REQUIRED_COMMENTARY_FIELDS:
                if field not in commentary:
                    errors.append(f"{c_prefix}: Missing field '{field}'")
    
    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict:
    """
    Validate all JSON files in a directory.
    
    Returns:
        {filename: (is_valid, errors)}
    """
    results = {}
    
    path = Path(dirpath)
    # Look for both page_*.json and any .json files
    json_files = sorted(path.glob("page_*.json"))
    if not json_files:
        json_files = sorted(path.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {dirpath}")
        return results
    
    for filepath in json_files:
        is_valid, errors = validate_chapter(str(filepath))
        results[filepath.name] = (is_valid, errors)
    
    return results


def determine_quality_tier(data: dict) -> tuple[int, str]:
    """Determine the quality tier of a translation."""
    has_commentary = False
    has_notes = False
    has_research_notes = False
    has_poem_notes = False
    
    # Check for commentary
    for segment in data.get("segments", []):
        if segment.get("commentary") and len(segment.get("commentary", [])) > 0:
            has_commentary = True
        if segment.get("type") == "poem" and "poem_notes" in segment:
            has_poem_notes = True
    
    # Check for notes
    if data.get("notes") or data.get("translator_notes"):
        notes = data.get("notes", []) or data.get("translator_notes", [])
        if len(notes) > 0:
            has_notes = True
    
    if data.get("research_notes") and len(data.get("research_notes", [])) > 0:
        has_research_notes = True
    
    # Tier 3: Excellent
    if has_commentary and has_notes and has_research_notes and has_poem_notes:
        return 3, "Excellent (Tier 3)"
    
    # Tier 2: Good
    if has_commentary and has_notes:
        return 2, "Good (Tier 2)"
    
    # Tier 1: Minimum acceptable
    return 1, "Minimum (Tier 1)"


def main():
    global VERBOSE
    
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py [--verbose] <file_or_directory>")
        print("\nExamples:")
        print("  python3 validate_json.py translations/page_0020.json")
        print("  python3 validate_json.py translations/")
        print("  python3 validate_json.py --verbose translations/page_0020.json")
        sys.exit(1)
    
    # Check for verbose flag
    args = sys.argv[1:]
    if "--verbose" in args:
        VERBOSE = True
        args.remove("--verbose")
    
    if not args:
        print("Error: No file or directory specified")
        sys.exit(1)
    
    target = args[0]
    
    if os.path.isfile(target):
        # Single file
        is_valid, errors = validate_chapter(target)
        filename = os.path.basename(target)
        
        if is_valid:
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            segment_count = len(data.get("segments", []))
            tier, tier_label = determine_quality_tier(data)
            
            # Count commentary
            commentary_count = sum(len(seg.get("commentary", [])) for seg in data.get("segments", []))
            
            if VERBOSE:
                print(f"✓ {filename}: VALIDATION PASSED")
                print(f"  Quality: {tier_label}")
                print(f"  Segments: {segment_count}")
                print(f"  Commentary: {commentary_count} annotations")
                print(f"  Page: {data.get('page')}")
                print(f"  Chapter: {data.get('chapter')}")
                if data.get("notes") or data.get("translator_notes"):
                    notes = data.get("notes", []) or data.get("translator_notes", [])
                    print(f"  Notes: {len(notes)} research findings")
            else:
                print(f"✓ {filename}: Valid ({segment_count} segments, {tier_label})")
        else:
            print(f"✗ {filename}: VALIDATION FAILED")
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
                tier, tier_label = determine_quality_tier(data)
                
                if VERBOSE:
                    commentary_count = sum(len(seg.get("commentary", [])) for seg in data.get("segments", []))
                    print(f"✓ {filename}: Valid - {tier_label}, {segment_count} segments, {commentary_count} annotations")
                else:
                    print(f"✓ {filename}: Valid ({tier_label})")
                valid_count += 1
            else:
                print(f"✗ {filename}: INVALID")
                if VERBOSE:
                    for error in errors:
                        print(f"    - {error}")
                invalid_count += 1
        
        print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
        
        if invalid_count > 0:
            sys.exit(1)
    
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
