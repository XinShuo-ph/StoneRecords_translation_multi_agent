#!/usr/bin/env python3
"""
Validate translation JSON files for completeness and format.

Usage:
    python3 validate_json.py translations/chapter_001.json
    python3 validate_json.py translations/
"""

import json
import sys
import os
from pathlib import Path

# Required fields for chapter JSON
REQUIRED_CHAPTER_FIELDS = [
    "chapter",
    "chapter_title",
    "segments",
    "translator_notes",
    "total_segments"
]

# Required fields for chapter title
REQUIRED_TITLE_FIELDS = ["original", "zh_modern", "en", "ru", "ja"]

# Required fields for each segment
REQUIRED_SEGMENT_FIELDS = ["id", "type", "original", "zh_modern", "en", "ru", "ja"]

# Valid segment types
VALID_SEGMENT_TYPES = ["prose", "poem", "dialogue", "commentary"]


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
    
    # Check required chapter fields
    for field in REQUIRED_CHAPTER_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Check chapter title
    if isinstance(data.get("chapter_title"), dict):
        for field in REQUIRED_TITLE_FIELDS:
            if field not in data["chapter_title"]:
                errors.append(f"Missing title field: chapter_title.{field}")
            elif not data["chapter_title"][field]:
                errors.append(f"Empty title field: chapter_title.{field}")
    else:
        errors.append("chapter_title must be an object")
    
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
    
    # Check total_segments matches actual count
    if data.get("total_segments") != len(segments):
        errors.append(f"total_segments ({data.get('total_segments')}) does not match actual segment count ({len(segments)})")
    
    # Check translator_notes is a list
    if not isinstance(data.get("translator_notes"), list):
        errors.append("translator_notes must be an array")
    
    return len(errors) == 0, errors


def validate_directory(dirpath: str) -> dict:
    """
    Validate all JSON files in a directory.
    
    Returns:
        {filename: (is_valid, errors)}
    """
    results = {}
    
    path = Path(dirpath)
    json_files = sorted(path.glob("chapter_*.json"))
    
    if not json_files:
        print(f"No chapter_*.json files found in {dirpath}")
        return results
    
    for filepath in json_files:
        is_valid, errors = validate_chapter(str(filepath))
        results[filepath.name] = (is_valid, errors)
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py <file_or_directory>")
        print("\nExamples:")
        print("  python3 validate_json.py translations/chapter_001.json")
        print("  python3 validate_json.py translations/")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target):
        # Single file
        is_valid, errors = validate_chapter(target)
        filename = os.path.basename(target)
        
        if is_valid:
            with open(target, 'r', encoding='utf-8') as f:
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
                with open(os.path.join(target, filename), 'r', encoding='utf-8') as f:
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
