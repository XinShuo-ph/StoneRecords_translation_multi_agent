# 红楼梦 Translation Project - Version 2.0

## Quick Start

**For Translators**: Read these documents in order:

1. **START HERE**: [`TRANSLATION_INSTRUCTIONS_V2.md`](TRANSLATION_INSTRUCTIONS_V2.md)
   - Complete translation workflow
   - JSON format specification
   - Step-by-step process

2. **QUALITY REFERENCE**: [`QUALITY_GUIDE.md`](QUALITY_GUIDE.md)
   - Good vs. bad examples
   - Quality standards by language
   - Common failures and fixes

3. **BEFORE SAVING**: [`VERIFICATION_CHECKLIST.md`](VERIFICATION_CHECKLIST.md)
   - 48-item mandatory checklist
   - Ensure completeness and quality
   - Catch errors before committing

4. **EXAMPLE**: [`examples/page_0020_simplified.json`](examples/page_0020_simplified.json)
   - Reference implementation
   - Correct JSON format
   - Quality standard

## What's New in V2.0

Version 2.0 is a complete redesign based on analysis of parallel translation experiments.

### Major Changes

| Aspect | V1.0 (Original) | V2.0 (New) |
|--------|-----------------|------------|
| **JSON Format** | Complex, many optional fields | Minimal, required fields only |
| **Instructions** | Mixed with protocol (700+ lines) | Pure translation workflow (500 lines) |
| **Quality Guidance** | Abstract guidelines | Concrete examples with explanations |
| **Verification** | Implicit expectations | Explicit 48-item checklist |
| **Structure** | Single large file | Focused, separated documents |

### Key Improvements

1. **Simplified JSON Format**
   - Only 4 top-level fields required
   - No ambiguous optional fields
   - Easy to validate

2. **Actionable Workflow**
   - 8 concrete steps per page
   - Time-boxed guidance
   - Clear sufficiency criteria

3. **Quality-First Approach**
   - Literary excellence as primary goal
   - Protocol separated (not mixed)
   - Comprehensive quality examples

4. **Explicit Verification**
   - Mandatory pre-save checklist
   - Covers completeness and quality
   - Prevents incomplete work

## Document Overview

### Core Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `TRANSLATION_INSTRUCTIONS_V2.md` | Main workflow | Read first, reference during work |
| `QUALITY_GUIDE.md` | Quality standards | Reference while translating |
| `VERIFICATION_CHECKLIST.md` | Quality control | Complete before saving each page |
| `IMPROVEMENTS_SUMMARY.md` | What changed and why | Background reading |
| `analysis/experiment_findings.md` | Detailed analysis | Background reading |

### Supporting Materials

| File/Folder | Purpose |
|-------------|---------|
| `examples/page_0020_simplified.json` | Reference example |
| `examples/page_0020.json` | Original detailed example |
| `research/` | Reference materials (glossary, guides) |
| `source_pages/` | PDF pages as images |

## Project Structure

```
workspace/
├── TRANSLATION_INSTRUCTIONS_V2.md  # ← START HERE
├── QUALITY_GUIDE.md                # ← Reference while working
├── VERIFICATION_CHECKLIST.md       # ← Use before saving
├── IMPROVEMENTS_SUMMARY.md         # What changed in V2.0
│
├── examples/
│   ├── page_0020_simplified.json   # Correct format example
│   └── page_0020.json              # Detailed example
│
├── analysis/
│   └── experiment_findings.md      # Analysis of previous attempts
│
├── research/                       # Reference materials
│   ├── glossary.md
│   ├── character_guide.md
│   ├── cultural_context.md
│   ├── poetry_guide.md
│   ├── commentary_guide.md
│   └── existing_translations.md
│
├── source_pages/                   # PDF pages as images
│   └── page_XXXX.png
│
└── translations/                   # Output directory
    └── page_XXXX.json
```

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  1. Open page (PDF or image)                                │
│  2. Identify all content (text + commentary)                │
│  3. Research each segment                                   │
│  4. Translate to 4 languages                                │
│  5. Polish each translation                                 │
│  6. Complete verification checklist                         │
│  7. Save as translations/page_XXXX.json                     │
│  8. Continue to next page                                   │
└─────────────────────────────────────────────────────────────┘
```

## Target Languages

Each page is translated into:
1. **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
2. **English** - Scholarly literary translation
3. **Russian (Русский)** - Literary Russian translation
4. **Japanese (日本語)** - Classical-influenced literary Japanese

## JSON Format (Minimal)

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Original Classical Chinese...",
      "zh_modern": "Modern Chinese translation...",
      "en": "English translation...",
      "ru": "Russian translation...",
      "ja": "Japanese translation...",
      "commentary": [
        {
          "source": "脂批",
          "original": "Commentary text...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": [
    "Research finding 1",
    "Research finding 2"
  ]
}
```

## Quality Standards

### Time Investment

- **Simple page**: 30-45 minutes
- **Average page**: 45-75 minutes
- **Complex page**: 90-120 minutes

**If completing pages in <20 minutes, you're rushing.**

### Completeness Requirements

- ✅ Every text segment translated
- ✅ Every commentary annotation translated
- ✅ All 4 languages for every segment
- ✅ At least 3 substantive research notes (when applicable)
- ✅ Valid JSON format
- ✅ Passes verification checklist

### Quality Principles

1. **Literary Excellence**: Translations must be beautiful, not just accurate
2. **Scholarly Rigor**: Research and document non-obvious findings
3. **Cultural Sensitivity**: Adapt appropriately for each target language
4. **Completeness**: Translate everything, skip nothing

## Common Pitfalls to Avoid

- ❌ Skipping commentary annotations
- ❌ Translating only part of a page
- ❌ Adding extra JSON fields
- ❌ Over-modernizing the language
- ❌ Rushing through research
- ❌ Skipping verification checklist

## Success Criteria

A successful page translation:
1. Includes all visible content from the page
2. Has high literary quality in all 4 languages
3. Documents research findings
4. Passes all verification checklist items
5. Uses correct JSON format with no extra fields

## Testing & Validation

### Self-Testing

Before considering your work complete:
1. Complete the verification checklist
2. Compare your work to `examples/page_0020_simplified.json`
3. Review against quality examples in `QUALITY_GUIDE.md`

### Quality Indicators

**Good signs:**
- Spending 30+ minutes per page
- Finding 3+ non-obvious research insights
- Polishing translations multiple times
- All checklist items completed

**Warning signs:**
- Completing pages in <20 minutes
- Generic research notes only
- Missing commentary
- Skipping verification checklist

## For Parallel Translation Projects

### Recommended Approach

**Option 1: Manual Coordination (Recommended)**
- Assign page ranges to each agent manually
- Focus entirely on translation quality
- No complex protocol overhead

**Option 2: Lightweight Protocol**
- Create separate protocol document
- Simple page claiming only
- Keep protocol separate from translation instructions

**Not Recommended:**
- Mixing protocol with translation instructions
- Complex sync mechanisms
- Protocol that diverts attention from quality

## Background: Why V2.0?

Version 2.0 addresses failures in previous parallel translation experiments:

### Previous Results (V1.0)
- 16 agents, average 9.75 pages each
- 87.5% stopped early (<20 pages)
- ~50% had JSON format errors
- Many translations incomplete or low quality

### Root Causes
1. Instructions mixed protocol with translation
2. Unclear JSON format (too many optional fields)
3. No explicit verification mechanism
4. Quality guidelines too abstract

### V2.0 Solutions
1. Separated concerns (translation vs. protocol)
2. Minimal required JSON format
3. Mandatory verification checklist
4. Concrete quality examples

**Expected improvements:**
- >60% completion rate (vs. 12.5%)
- >95% format compliance (vs. ~50%)
- >90% commentary coverage (vs. ~30%)
- Higher translation quality overall

See [`IMPROVEMENTS_SUMMARY.md`](IMPROVEMENTS_SUMMARY.md) for detailed analysis.

## Getting Help

### Documentation Issues

If anything is unclear:
1. Check if `QUALITY_GUIDE.md` has relevant examples
2. Review `examples/page_0020_simplified.json`
3. Consult `research/` materials for terminology

### Translation Challenges

If stuck on a passage:
1. Time-box research to 10 minutes
2. Add note: "Uncertain: [your question]"
3. Continue to avoid blocking progress

### Format Questions

If unsure about JSON structure:
1. Compare to `examples/page_0020_simplified.json`
2. Use only the required fields listed
3. Validate JSON syntax before saving

## Contributing

### Improving Documentation

If you find issues or have suggestions:
1. Document what was unclear
2. Provide specific examples
3. Suggest concrete improvements

### Sharing Best Practices

If you develop effective techniques:
1. Document your approach
2. Share examples
3. Contribute to quality guide

## License & Attribution

This translation project is for scholarly purposes. Translations should cite:
- Original work: 曹雪芹《红楼梦》
- Source edition: 红楼梦脂评汇校本
- Translation project: [Your project details]

---

## Quick Reference Card

**Before starting:**
1. Read `TRANSLATION_INSTRUCTIONS_V2.md`
2. Review `QUALITY_GUIDE.md` examples

**While working:**
1. Open source page
2. Identify all content
3. Research → Translate → Polish
4. Reference `QUALITY_GUIDE.md` as needed

**Before saving:**
1. Complete `VERIFICATION_CHECKLIST.md`
2. Compare to `examples/page_0020_simplified.json`
3. Validate JSON

**After saving:**
1. Continue to next page
2. Don't pause between pages

---

*Version 2.0 - February 12, 2026*  
*Based on analysis of parallel translation experiments*

**Remember**: This is world-class literature. Every word deserves care.
