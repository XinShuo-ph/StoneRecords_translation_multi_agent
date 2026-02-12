# Translation Instructions - Version 2.0

## Overview

This directory contains **improved translation instructions** designed based on analysis of the recent 16-parallel-agent experiment.

## Key Improvements from V1

### 1. **Separation of Concerns**
- Translation instructions are NOW COMPLETELY SEPARATE from parallel worker protocol
- Focus purely on translation quality and methodology
- No git operations, sync procedures, or coordination details

### 2. **Radical Simplification**
- Core instructions reduced from 779 lines → **~300 lines**
- Essential information prioritized
- Progressive complexity (minimal → standard → complete)

### 3. **Clear Quality Tiers**
- **Tier 1 (Minimum)**: Basic requirements to pass validation
- **Tier 2 (Good)**: Recommended target quality
- **Tier 3 (Excellent)**: Aspirational quality with deep research

### 4. **Built-in Validation**
- Mandatory validation checklist before moving to next page
- Automated validation script integration
- Self-checking procedures

### 5. **Progressive Examples**
- 3 example files demonstrating quality tiers
- Minimal, standard, and poetry-focused examples
- Real translation content, not abstract schemas

---

## File Structure

### Core Documents (Read First)

| File | Purpose | Read Time |
|------|---------|-----------|
| `TRANSLATION_INSTRUCTIONS_V2.md` | Core translation workflow | 10 min |
| `TRANSLATION_SCHEMA.md` | JSON schema with 3 levels | 8 min |
| `TRANSLATION_VALIDATION.md` | Validation procedures | 6 min |

**Total essential reading: ~24 minutes**

### Example Files

| File | Demonstrates | Quality Tier |
|------|--------------|--------------|
| `examples/page_0020_minimal.json` | Minimal required format | Tier 1 |
| `examples/page_0020_with_commentary.json` | Standard with commentary | Tier 2 |
| `examples/page_0025_poetry.json` | Poetry translation | Tier 2 |

### Reference Documents (Use as Needed)

| File | Purpose |
|------|---------|
| `research/glossary.md` | Character names and terminology |
| `research/character_guide.md` | Character profiles |
| `research/cultural_context.md` | Historical background |
| `research/poetry_guide.md` | Poetry translation approaches |

---

## Quick Start for Agents

### First Time (Allow 30 minutes)

1. ✅ Read `TRANSLATION_INSTRUCTIONS_V2.md` (10 min)
2. ✅ Read `TRANSLATION_SCHEMA.md` (8 min)
3. ✅ Review 2-3 examples (5 min each)
4. ✅ Skim `TRANSLATION_VALIDATION.md` (5 min)
5. ✅ Start first page

### Subsequent Pages (15-30 min per page)

1. View page image
2. Translate to 4 languages
3. Save as JSON
4. Validate with `python3 tools/validate_json.py`
5. Next page immediately

---

## Comparison: V1 vs V2

### V1 (Original - 779 lines)

**Structure**:
```
instructions.md (779 lines)
├── Translation objectives
├── Multi-agent protocol ← Mixed concern
├── Sync daemon setup ← Mixed concern
├── Quick start guide ← Mixed concern
├── Source material structure
├── File structure
├── Workflow (research → translate → polish)
├── JSON format
├── Chapter structure reference
├── Translation quality guidelines
├── Special challenges
├── Glossary excerpt
├── Collaboration protocol ← Mixed concern
└── Anti-patterns
```

**Issues**:
- Too long (agents don't read it all)
- Mixed translation + coordination concerns
- No clear minimum quality bar
- No built-in validation
- Overwhelming research requirements

### V2 (New - ~300 lines across 3 docs)

**Structure**:
```
TRANSLATION_INSTRUCTIONS_V2.md (300 lines)
├── Mission (clear objective)
├── 6-step workflow
├── JSON schema (minimal → complete)
├── Validation checklist
├── Quality tiers (1, 2, 3)
├── Translation guidelines by language
├── Key terms reference
├── Research protocol (required vs conditional)
├── Continuous work protocol
└── Quick start checklist

TRANSLATION_SCHEMA.md (separate, detailed)
TRANSLATION_VALIDATION.md (separate, detailed)
examples/*.json (3 demonstration files)
```

**Improvements**:
- Clear prioritization (core vs reference)
- Separated concerns (translation only)
- Progressive complexity (3 tiers)
- Built-in validation
- Streamlined research (required vs conditional)
- Concrete examples

---

## Success Metrics

After implementing V2 instructions, we expect:

| Metric | V1 Results | V2 Target |
|--------|------------|-----------|
| JSON validity rate | ~80% | 100% |
| Complete translations (all 4 languages) | ~85% | 100% |
| Pages with research notes | ~40% | 80% |
| Agent continuation (>5 pages) | ~30% | 80% |
| Schema compliance | ~60% | 95% |
| Wrong page numbers | ~10% | <1% |
| Empty translation fields | ~15% | 0% |

---

## Design Principles

### 1. Progressive Disclosure
Show simple concepts first, add complexity later.

### 2. Actionable > Comprehensive
Better to give clear, actionable steps than comprehensive background.

### 3. Examples > Abstract Descriptions
Show real examples rather than describe abstract schemas.

### 4. Validation as First-Class Citizen
Validation is not an afterthought—it's built into the workflow.

### 5. Clear Minimum Bar
Agents must know "what is good enough" vs "what is excellent."

### 6. Separate Concerns
Translation instructions should contain ZERO coordination/protocol details.

---

## Usage Recommendations

### For New Agents

**Day 1**:
1. Read all 3 core documents
2. Review all 3 examples
3. Translate 2-3 pages (aim for Tier 1)
4. Get comfortable with workflow

**Day 2-3**:
5. Aim for Tier 2 quality
6. Start adding commentary and notes
7. Build speed (15-20 min per page)

**Day 4+**:
8. Maintain Tier 2 quality
9. Occasionally attempt Tier 3 for complex pages
10. Contribute to research materials

### For Experienced Agents

If you've already translated pages:
1. Skim `TRANSLATION_INSTRUCTIONS_V2.md` for new workflows
2. Review `TRANSLATION_SCHEMA.md` for any schema changes
3. Note the 3-tier quality system
4. Start translating immediately

---

## Migration from V1

### If You Used V1 Instructions

**Key Changes**:
1. ❌ No more multi-agent protocol in translation docs
2. ❌ No more sync daemon setup here
3. ✅ Mandatory validation before next page
4. ✅ 3-tier quality system introduced
5. ✅ Streamlined research protocol
6. ✅ JSON schema simplified (3 levels)

**What to Keep**:
- Translation quality standards (unchanged)
- Glossary terms (unchanged)
- Research materials (unchanged)
- Cultural context (unchanged)

**What Changed**:
- Workflow simplified (6 steps instead of 10)
- JSON schema has 3 levels now (minimal → standard → complete)
- Validation is now mandatory
- Research is streamlined (required vs conditional)

---

## Feedback and Iteration

### How to Report Issues

If you encounter problems with these instructions:

1. **Document the issue**: What was unclear? What went wrong?
2. **Note the context**: Which section? Which step?
3. **Suggest improvement**: How could it be clearer?
4. **Add to work log**: Include in your session notes

### Continuous Improvement

This is **Version 2.0** of the translation instructions. We expect to iterate based on real usage feedback.

Future versions may address:
- Additional example types
- More detailed poetry guidance
- Advanced research techniques
- Quality assessment rubrics

---

## FAQ

### Q: Do I need to read all 3 core documents?
**A**: Yes, but it only takes ~25 minutes total. This is much faster than the 779-line V1 document.

### Q: What if I just want to start translating?
**A**: Minimum reading:
1. `TRANSLATION_INSTRUCTIONS_V2.md` sections 1-4 (Workflow + Schema)
2. Review one example file
3. Start translating (aim for Tier 1 first)

### Q: How do I know if my translation is "good enough"?
**A**: Run `python3 tools/validate_json.py`. If it passes, you meet Tier 1. If you also have commentary and notes, you meet Tier 2.

### Q: What about the parallel worker protocol?
**A**: That's in separate documents (not in translation instructions). See `PROTOCOL.md` or `WORKER_INSTRUCTIONS.md`.

### Q: Can I use the old V1 instructions?
**A**: Not recommended. V2 is designed to fix the issues observed in the 16-agent experiment.

### Q: How long should each page take?
**A**:
- Tier 1 (minimal): 10-15 minutes
- Tier 2 (good): 15-25 minutes
- Tier 3 (excellent): 30-60 minutes

Target: Tier 2 at 20 minutes/page average.

### Q: What if the page is really complex?
**A**: It's okay to take longer. Complex pages with lots of poetry and commentary can take 30-60 minutes. That's normal.

### Q: What if I can't find information during research?
**A**: Don't spend more than 5 minutes researching one segment. If stuck, add a note like "Uncertain: [your question]" and continue.

---

## Summary

**Version 2.0 Translation Instructions** are designed to:

1. ✅ **Focus purely on translation** (no protocol mixing)
2. ✅ **Be quickly readable** (~25 min vs 60+ min)
3. ✅ **Provide clear quality tiers** (minimum vs good vs excellent)
4. ✅ **Include mandatory validation** (built into workflow)
5. ✅ **Offer progressive examples** (3 demonstration files)
6. ✅ **Streamline research** (required vs conditional)

**Start reading**: `TRANSLATION_INSTRUCTIONS_V2.md`

**Questions?** Add them to your work log and continue translating.
