#!/usr/bin/env python3
"""
Strict JSON Schema Validator for 红楼梦 Translations

This validator enforces:
1. JSON schema compliance
2. Content quality checks
3. Completeness verification
4. Research depth requirements
5. Polish evidence

Usage:
    python3 validate_translation_v2.py translations/page_0020.json --strict
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Try to import jsonschema, provide fallback
try:
    import jsonschema
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    print("Warning: jsonschema not installed. Install with: pip3 install jsonschema")


class TranslationValidator:
    """Validates translation JSON files against strict quality standards"""
    
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.errors = []
        self.warnings = []
        
    def validate_file(self, filepath: str) -> bool:
        """Main validation entry point"""
        print(f"Validating: {filepath}")
        print("=" * 60)
        
        # Load JSON
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
            return False
        
        # Run validation checks
        self.validate_schema(data)
        self.validate_completeness(data)
        self.validate_quality(data)
        self.validate_research(data)
        self.validate_polish(data)
        self.validate_checklist(data)
        
        # Report results
        return self.report_results()
    
    def validate_schema(self, data: Dict) -> None:
        """Validate against JSON schema"""
        if not HAS_JSONSCHEMA:
            self.warnings.append("JSON schema validation skipped (jsonschema not installed)")
            return
        
        schema_path = Path(__file__).parent / "translation_schema.json"
        if not schema_path.exists():
            self.warnings.append(f"Schema file not found: {schema_path}")
            return
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            validate(instance=data, schema=schema)
            print("✓ JSON schema validation passed")
        except ValidationError as e:
            self.errors.append(f"Schema validation failed: {e.message}")
            if e.path:
                self.errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
    
    def validate_completeness(self, data: Dict) -> None:
        """Check that all content is present and non-empty"""
        
        # Check required top-level fields
        required_fields = [
            'page', 'chapter', 'chapter_title', 'page_content_type',
            'segments', 'translator_notes', 'research_sources',
            'polish_log', 'quality_checklist'
        ]
        
        for field in required_fields:
            if field not in data:
                self.errors.append(f"Missing required field: {field}")
            elif not data.get(field):
                self.errors.append(f"Empty field: {field}")
        
        # Check chapter_title has all 5 languages
        if 'chapter_title' in data:
            ct = data['chapter_title']
            for lang in ['original', 'zh_modern', 'en', 'ru', 'ja']:
                if lang not in ct or not ct[lang]:
                    self.errors.append(f"chapter_title missing {lang}")
        
        # Check segments
        if 'segments' in data:
            if not data['segments']:
                self.errors.append("No segments found - page cannot be empty")
            
            for i, seg in enumerate(data['segments']):
                seg_id = seg.get('id', i+1)
                
                # Check all 4 language translations
                for lang in ['zh_modern', 'en', 'ru', 'ja']:
                    if lang not in seg:
                        self.errors.append(f"Segment {seg_id}: missing {lang}")
                    elif not seg[lang] or not seg[lang].strip():
                        self.errors.append(f"Segment {seg_id}: empty {lang}")
                    elif len(seg[lang]) < 5:
                        self.warnings.append(f"Segment {seg_id}: {lang} suspiciously short")
                
                # Check original text
                if 'original' not in seg or not seg['original']:
                    self.errors.append(f"Segment {seg_id}: missing original text")
                
                # Check commentary if present
                if 'commentary' in seg:
                    for j, comm in enumerate(seg['commentary']):
                        for lang in ['zh_modern', 'en', 'ru', 'ja']:
                            if lang not in comm or not comm[lang]:
                                self.errors.append(
                                    f"Segment {seg_id}, commentary {j+1}: missing {lang}"
                                )
        
        if not self.errors:
            print("✓ Completeness check passed")
    
    def validate_quality(self, data: Dict) -> None:
        """Check translation quality indicators"""
        
        # Check segment count matches
        if 'segments' in data and 'total_segments' in data:
            actual = len(data['segments'])
            declared = data['total_segments']
            if actual != declared:
                self.errors.append(
                    f"Segment count mismatch: {actual} actual vs {declared} declared"
                )
        
        # Check for suspiciously uniform segment lengths (template filling)
        if 'segments' in data and len(data['segments']) > 2:
            lengths = [len(seg.get('en', '')) for seg in data['segments']]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            
            if variance < 100 and avg_len > 50:
                self.warnings.append(
                    "All translations similar length - possible template filling"
                )
        
        # Check for copy-paste between languages
        if 'segments' in data:
            for i, seg in enumerate(data['segments']):
                seg_id = seg.get('id', i+1)
                
                # Check if translations are too similar (beyond shared names)
                texts = {
                    'zh': seg.get('zh_modern', ''),
                    'en': seg.get('en', ''),
                    'ru': seg.get('ru', ''),
                    'ja': seg.get('ja', '')
                }
                
                # Simple check: English and Russian should be very different
                if texts['en'] and texts['ru']:
                    if texts['en'] == texts['ru']:
                        self.errors.append(
                            f"Segment {seg_id}: English and Russian identical (copy-paste?)"
                        )
        
        if not self.errors:
            print("✓ Quality indicators check passed")
    
    def validate_research(self, data: Dict) -> None:
        """Validate research depth"""
        
        # Check translator notes
        notes = data.get('translator_notes', [])
        if not notes:
            self.errors.append("No translator_notes - research required!")
        elif len(notes) < 1:
            self.errors.append("Insufficient translator_notes (minimum 1)")
        else:
            for i, note in enumerate(notes):
                if len(note) < 20:
                    self.warnings.append(
                        f"Translator note {i+1} too short ({len(note)} chars) - "
                        "should be substantive"
                    )
                
                # Check for generic phrases
                generic_phrases = [
                    "this is interesting",
                    "this is important",
                    "note this",
                    "see this"
                ]
                if any(phrase in note.lower() for phrase in generic_phrases):
                    self.warnings.append(
                        f"Translator note {i+1} seems generic - be more specific"
                    )
        
        # Check research sources
        sources = data.get('research_sources', [])
        if not sources:
            self.errors.append("No research_sources - minimum 3 required!")
        elif len(sources) < 3:
            self.errors.append(f"Insufficient sources: {len(sources)} (minimum 3)")
        else:
            for i, source in enumerate(sources):
                if 'type' not in source:
                    self.errors.append(f"Source {i+1}: missing type")
                if 'finding' not in source or len(source['finding']) < 10:
                    self.errors.append(
                        f"Source {i+1}: missing or too short 'finding' field"
                    )
        
        if not self.errors:
            print("✓ Research depth check passed")
    
    def validate_polish(self, data: Dict) -> None:
        """Validate polish/revision evidence"""
        
        polish_log = data.get('polish_log', [])
        if not polish_log:
            self.errors.append("No polish_log - must polish all 4 languages!")
        elif len(polish_log) < 4:
            self.errors.append(
                f"Incomplete polish_log: {len(polish_log)} entries (need 4, one per language)"
            )
        else:
            # Check all 4 languages covered
            languages_polished = set(entry.get('language') for entry in polish_log)
            required_langs = {'zh_modern', 'en', 'ru', 'ja'}
            missing = required_langs - languages_polished
            
            if missing:
                self.errors.append(
                    f"Polish missing for languages: {', '.join(missing)}"
                )
            
            # Check each entry has substantive changes
            for i, entry in enumerate(polish_log):
                changes = entry.get('changes', '')
                if len(changes) < 10:
                    self.warnings.append(
                        f"Polish log entry {i+1}: 'changes' field too short"
                    )
        
        if not self.errors:
            print("✓ Polish evidence check passed")
    
    def validate_checklist(self, data: Dict) -> None:
        """Validate quality checklist - all must be true"""
        
        checklist = data.get('quality_checklist', {})
        if not checklist:
            self.errors.append("Missing quality_checklist!")
            return
        
        required_checks = [
            'read_full_page',
            'identified_all_content',
            'researched_allusions',
            'consulted_min_3_sources',
            'all_commentary_translated',
            'all_4_languages_complete',
            'polished_each_language',
            'verified_completeness',
            'json_validated'
        ]
        
        for check in required_checks:
            if check not in checklist:
                self.errors.append(f"quality_checklist missing: {check}")
            elif checklist[check] is not True:
                self.errors.append(
                    f"quality_checklist.{check} is {checklist[check]} (must be true)"
                )
        
        if not self.errors:
            print("✓ Quality checklist passed")
    
    def report_results(self) -> bool:
        """Print validation results and return pass/fail"""
        print("\n" + "=" * 60)
        
        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
            print("\n❌ VALIDATION FAILED")
            return False
        else:
            if self.warnings:
                print("\n⚠ Validation passed with warnings")
            else:
                print("\n✅ VALIDATION PASSED - Translation meets all requirements!")
            return True


def main():
    parser = argparse.ArgumentParser(
        description='Validate 红楼梦 translation JSON files'
    )
    parser.add_argument('file', help='Path to JSON file to validate')
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict validation mode'
    )
    
    args = parser.parse_args()
    
    validator = TranslationValidator(strict_mode=args.strict)
    success = validator.validate_file(args.file)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
