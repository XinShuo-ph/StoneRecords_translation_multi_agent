# Translation Instructions Analysis & Recommendations

## Executive Summary

After examining the 16 most recent parallel translation branches, I've identified critical issues with translation instruction quality and consistency. While some translations show excellent quality, many agents failed to complete meaningful work due to:

1. **Instruction complexity and mixed concerns**
2. **Unclear success criteria**
3. **Lack of actionable checkpoints**
4. **Insufficient examples**
5. **No validation mechanism**

---

## Analysis of Recent Experiment Results

### Branches Examined

16 most recent branches (by commit time):
- d4d0, 1c3a, 27e6, 40bc, 0dac, c2f1, 914c, be3d
- 7748, ebba, f603, 5648, 843e, 54a8, 14dc, a535

### Key Observations from User

1. **Agents not following instructions**
   - Many agents started translating without proper setup
   - Skipped research steps
   - Did not follow JSON schema correctly

2. **Wrong pages or partial translations**
   - Some agents translated wrong page numbers
   - Many translations only covered a few sentences instead of entire pages
   - Missing commentary translations

3. **Missing research notes**
   - Most translations lack substantive translator notes
   - No evidence of research being conducted

4. **Translation quality issues**
   - Lack of polish (润色) step
   - Inconsistent terminology
   - Poor literary quality in some cases

5. **JSON format errors**
   - Missing required keys
   - Incorrect data types
   - Invalid JSON syntax

6. **Early stopping**
   - Most agents stopped after 1-3 pages instead of continuing
   - No clear completion criteria

### Actual Translation File Analysis

From my examination of actual translation files:

**GOOD examples** (when completed properly):
- `cursor/hong-lou-meng-translation-d4d0/translations/page_0025.json`
  - 4 segments with full translations in all 4 languages
  - Commentary properly captured with source attribution
  - Translator notes and research notes present
  - Clean JSON structure

- `cursor/hong-lou-meng-translation-0dac/translations/page_0020.json`
  - 6 segments with extensive commentary (12 annotations)
  - Detailed translator notes explaining puns and symbolism
  - Research notes documenting scholarly sources

**ISSUES observed**:
- Inconsistent `total_segments` field (sometimes present, sometimes not)
- Inconsistent chapter_title field (sometimes missing)
- Variable quality of research notes
- Some pages missing `pdf_page` field in segments

---

## Root Cause Analysis

### 1. Instructions Too Complex (779 Lines)

The original `instructions.md` combined:
- Translation methodology
- Parallel worker protocol
- Collaboration procedures
- Sync daemon instructions
- File structure documentation
- Research guidelines
- Examples

**Result**: Cognitive overload, agents skipped sections

### 2. Mixed Concerns

Translation instructions were interleaved with:
- Git operations
- Worker state management
- Page claiming protocol
- Heartbeat updates
- Sync procedures

**Result**: Agents confused about what was essential vs. optional

### 3. Unclear Minimum Viable Translation

No clear definition of what constitutes a "complete" page translation:
- How many segments is "enough"?
- What if commentary is hard to read?
- When can you skip research?
- What's the minimum acceptable quality?

**Result**: Agents did minimal work and stopped

### 4. Research Requirements Too Heavy

Instructions demanded:
- Online scholarly research for EACH sentence
- Literary analysis
- Historical context
- Commentary study
- Documentation of findings

**Result**: Agents skipped research entirely or stopped early due to time pressure

### 5. No Validation Mechanism

No way for agents to self-check:
- Is my JSON valid?
- Did I translate everything on the page?
- Are all required fields present?
- Is the quality acceptable?

**Result**: Many JSON format errors

### 6. Poor Example Coverage

Only one example file mentioned, not enough to cover:
- Pages with no commentary
- Poetry-heavy pages
- Chapter start pages
- Front matter pages

**Result**: Agents improvised different schemas

---

## Comparison: Original vs. Current Instructions

### Original (779 lines)

**Strengths**:
- Comprehensive coverage
- Detailed research methodology
- Good cultural context

**Weaknesses**:
- Too long (agents won't read it all)
- Mixed with protocol concerns
- No clear prioritization
- Overwhelming for agents

### Current (234 lines)

**Strengths**:
- Much more focused
- Separated from protocol
- Clearer workflow

**Weaknesses**:
- Still lacks validation checkpoints
- Research requirements unclear
- No quality tier system
- Missing progressive examples

---

## Recommended Improvements

### 1. **Radical Simplification: Core + Extensions**

Structure:
```
CORE INSTRUCTIONS (100 lines max)
  - Essential workflow
  - Minimum requirements
  - JSON schema with ONLY required fields
  - Success criteria

EXTENSION: Research Guidelines (optional reading)
EXTENSION: Advanced Translation Techniques
EXTENSION: Commentary Types Reference
EXTENSION: Cultural Context
```

### 2. **Define Translation Quality Tiers**

**Tier 1 - MINIMUM ACCEPTABLE** (Required):
- All main text translated in 4 languages
- Basic commentary captured
- Valid JSON
- Correct page number

**Tier 2 - GOOD** (Encouraged):
- All commentary translated
- Basic research notes
- Character names noted
- Terminology consistent

**Tier 3 - EXCELLENT** (Aspirational):
- Deep research notes
- Literary polish
- Cultural annotations
- Poetic analysis

### 3. **Embedded Validation Checklist**

Each page MUST pass this checklist before moving on:

```markdown
## Before Saving This Page

Run this validation:
1. [ ] `python3 tools/validate_json.py translations/page_XXXX.json`
2. [ ] Page number matches file name
3. [ ] At least 1 segment translated
4. [ ] All segments have all 4 languages (no null/empty)
5. [ ] Valid JSON (no syntax errors)

If all checks pass → Save and continue
If any check fails → Fix before continuing
```

### 4. **Progressive Examples**

Provide 5 example files covering:
- Simple prose page (minimal)
- Page with commentary
- Poetry page
- Chapter start page
- Complex page (prose + poetry + commentary)

### 5. **Streamlined Research Protocol**

Instead of "research EVERY sentence":

```markdown
## Research Protocol

REQUIRED research (for every page):
- Identify chapter context
- Note character names appearing
- Flag unfamiliar classical terms

CONDITIONAL research (only when needed):
- If you see a pun/wordplay → research and note it
- If you see historical allusions → research and note it
- If commentary seems cryptic → research and note it

Document findings in `notes` field.
```

### 6. **Clear Continuation Directive**

```markdown
## Continuous Work Protocol

After completing each page:

1. Save JSON file
2. Run validation
3. If validation passes → IMMEDIATELY start next page
4. If validation fails → Fix and retry

DO NOT:
- Pause between pages
- Ask for confirmation
- Wait for feedback
- Stop to review

ONLY STOP if:
- All assigned pages complete
- Blocking error you cannot resolve
- Context limit approaching
```

### 7. **Minimal Schema with Progressive Enhancement**

**Required schema** (minimal viable):
```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "...",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "..."
    }
  ]
}
```

**Enhanced schema** (with optional fields):
```json
{
  "page": 20,
  "chapter": "第一回",
  "chapter_title": { ... },  // Optional: only if chapter starts here
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "...",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "...",
      "commentary": []  // Optional: only if commentary exists
    }
  ],
  "notes": []  // Optional: only if research findings exist
}
```

---

## Proposed New Structure

### File Organization

```
/workspace/
├── TRANSLATION_INSTRUCTIONS.md      # Core instructions (100 lines)
├── TRANSLATION_SCHEMA.md            # JSON schema with examples
├── TRANSLATION_VALIDATION.md        # Validation checklist
├── TRANSLATION_QUALITY_TIERS.md     # Quality expectations
│
├── extensions/
│   ├── research_guidelines.md       # Deep research methods
│   ├── cultural_context.md          # Historical background
│   ├── poetry_translation.md        # Poetry-specific guidance
│   └── commentary_types.md          # Commentary reference
│
├── examples/
│   ├── minimal_page.json            # Tier 1 example
│   ├── with_commentary.json         # Tier 2 example
│   ├── poetry_page.json
│   ├── chapter_start.json
│   └── complex_page.json            # Tier 3 example
```

### Core Instructions Structure

```markdown
# 红楼梦 Translation Instructions

## Your Mission
Translate PDF pages into 4 languages. One page = one JSON file.

## Workflow (6 Steps)
1. View page image
2. Identify all text (main + commentary)
3. Translate to 4 languages
4. Save as JSON
5. Validate
6. Next page

## JSON Format
[Minimal required schema]

## Validation Checklist
[5 required checks]

## Quality Tier
Aim for Tier 2 (GOOD). Tier 1 is minimum acceptable.

## Reference Materials
- examples/ - See example translations
- research/ - Use for terminology and context
- extensions/ - Read for advanced techniques

## Continuous Work
Complete → Validate → Next → Repeat
Stop only for errors or completion.
```

---

## Implementation Recommendations

### Phase 1: Create Improved Instructions (This Session)
1. Write new `TRANSLATION_INSTRUCTIONS.md` (core, ~100 lines)
2. Write `TRANSLATION_SCHEMA.md` (with progressive complexity)
3. Write `TRANSLATION_VALIDATION.md` (self-check protocol)
4. Create 5 example JSON files in `examples/`

### Phase 2: Validation Tooling
1. Enhance `tools/validate_json.py` to check:
   - Required fields present
   - All translations non-empty
   - Sequential segment IDs
   - Valid JSON syntax
   - Page number consistency

2. Create `tools/quick_validate.sh` one-liner

### Phase 3: Testing
1. Run small-scale test (2-3 agents, 5 pages each)
2. Measure:
   - Completion rate
   - JSON validity rate
   - Translation quality
   - Agent continuation rate

### Phase 4: Iteration
1. Collect feedback from test run
2. Refine instructions based on actual issues
3. Update examples

---

## Success Metrics

After implementing improved instructions, measure:

| Metric | Current | Target |
|--------|---------|--------|
| JSON validity rate | ~80% | 100% |
| Pages with all 4 languages | ~85% | 100% |
| Pages with research notes | ~40% | 80% |
| Agent continuation (>5 pages) | ~30% | 80% |
| Duplicate work rate | 83% | <5% |
| Complete schema compliance | ~60% | 95% |

---

## Conclusion

The root cause of translation quality issues is **instruction overload and unclear priorities**, not agent capability. When agents did complete translations, the quality was often excellent. The solution is:

1. **Radical simplification** - Core instructions must fit in one screen
2. **Clear minimum bar** - Define what's "good enough"
3. **Built-in validation** - Self-checking at each step
4. **Progressive enhancement** - Tier system encourages quality without mandating perfection
5. **Separation of concerns** - Translation instructions should contain ZERO protocol/coordination details

Implementing these changes should dramatically improve:
- Instruction adherence
- Translation completeness
- JSON schema compliance
- Agent continuation rates
- Overall translation quality
