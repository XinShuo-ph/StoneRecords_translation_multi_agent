# Translation Verification Checklist

## Purpose

This is a mandatory checklist to complete BEFORE saving each page's translation.

Use this to verify completeness and quality. Do not skip any items.

---

## Pre-Translation Checklist

Before starting translation work on a page:

- [ ] **Page source opened**: Viewing the PDF page or corresponding image
- [ ] **Page number confirmed**: Verified I'm working on the correct page
- [ ] **Content identified**: Noted all text segments and commentary on the page
- [ ] **Research materials ready**: Have access to `research/` folder files

---

## During Translation Checklist

While translating:

### Content Identification

- [ ] **All prose segments identified**: Every paragraph/narrative section noted
- [ ] **All poetry identified**: Every poem/verse section noted  
- [ ] **All dialogue identified**: Every speech/conversation noted
- [ ] **All commentary identified**: Found all 眉批/夹批/侧批 annotations
- [ ] **Source tags noted**: Identified all 【甲戌】【庚辰】etc. markers

### Research Completed

- [ ] **Online search done**: Searched for scholarly interpretations of key passages
- [ ] **Reference materials checked**: Consulted `glossary.md`, `character_guide.md`, etc.
- [ ] **Allusions researched**: Looked up any classical allusions (典故)
- [ ] **Symbolism identified**: Noted any puns, hidden meanings, foreshadowing
- [ ] **Findings documented**: Added non-obvious insights to `notes` array

### Translation Completed

For EACH segment:

- [ ] **Original copied**: Classical Chinese text in `original` field
- [ ] **Modern Chinese done**: Translated to `zh_modern`
- [ ] **English done**: Translated to `en`
- [ ] **Russian done**: Translated to `ru`
- [ ] **Japanese done**: Translated to `ja`
- [ ] **Commentary translated**: All commentary for this segment in all 4 languages

---

## Post-Translation (Polish) Checklist

After initial translation, before saving:

### Literary Quality Review

- [ ] **Modern Chinese polished**: Natural, accessible, retains classical flavor
- [ ] **English polished**: Scholarly literary register, smooth flow
- [ ] **Russian polished**: Literary Russian, appropriate register
- [ ] **Japanese polished**: Classical-influenced style, appropriate vocabulary
- [ ] **Poetry feels poetic**: Verse translations have rhythm and structure
- [ ] **Read aloud**: Each translation sounds natural when read aloud (mentally)

### Accuracy Check

- [ ] **Four languages consistent**: All translations convey the same core meaning
- [ ] **No meaning lost**: Nothing from original omitted or distorted
- [ ] **Cultural context explained**: Added notes for culture-specific concepts
- [ ] **Names consistent**: Character names match `glossary.md` conventions
- [ ] **Terminology consistent**: Key terms translated consistently

### Commentary Quality

- [ ] **All commentary translated**: No commentary annotations skipped
- [ ] **Source attribution preserved**: Each commentary notes its manuscript source
- [ ] **Commentary tone maintained**: Preserved the original's tone (poetic/scholarly/etc.)

---

## Pre-Save (Format) Checklist

Before saving the JSON file:

### JSON Structure

- [ ] **Required fields only**: No extra fields added
- [ ] **Page number correct**: `page` field matches the actual PDF page
- [ ] **Chapter correct**: `chapter` field matches the chapter this page belongs to
- [ ] **Segments array complete**: All segments included
- [ ] **Notes array complete**: All research findings documented

### Segment Validation

- [ ] **Sequential IDs**: Segments numbered 1, 2, 3... with no gaps
- [ ] **Type specified**: Each segment has correct `type` (prose/poem/dialogue)
- [ ] **All 5 text fields present**: `original`, `zh_modern`, `en`, `ru`, `ja` all filled
- [ ] **Commentary field present**: Every segment has `commentary` (even if empty `[]`)
- [ ] **No null values**: No fields left as `null` or empty string

### JSON Validity

- [ ] **Valid JSON**: File parses without syntax errors
- [ ] **UTF-8 encoding**: All Chinese/Russian/Japanese characters render correctly
- [ ] **Proper escaping**: Special characters (quotes, newlines) properly escaped
- [ ] **No trailing commas**: JSON syntax clean

---

## Final Verification Checklist

Final check before considering the page complete:

### Completeness Verification

- [ ] **Re-read source page**: Looked at the original page again
- [ ] **Every visible element translated**: No text left untranslated
- [ ] **No content skipped**: Main text AND commentary both complete
- [ ] **Nothing missed**: Compared translation segment count to expected count

### Quality Verification

- [ ] **Meets quality standards**: Translations are literary, not mechanical
- [ ] **Research adequate**: At least 3 substantive research notes (if applicable)
- [ ] **No obvious errors**: No typos, grammatical errors, or awkward phrasing
- [ ] **Scholarly value**: Translation would be useful for academic study

### Meta-Check

- [ ] **File naming correct**: Saved as `translations/page_XXXX.json` (4-digit page number)
- [ ] **Time invested**: Spent adequate time (30-120 minutes depending on complexity)
- [ ] **Self-evaluation passed**: Answered quality questions honestly

---

## Quick Numerical Checks

Count these before saving:

| What to Count | Minimum Expected | Your Count |
|---------------|------------------|------------|
| Segments | (varies by page) | ___ |
| Segments with commentary | (at least 30% of segments) | ___ |
| Research notes | 3+ for typical page | ___ |
| Languages per segment | Always exactly 4 | ___ |

**If any count is below minimum, review and fix.**

---

## Common Failures to Check For

Before saving, explicitly verify you did NOT:

- [ ] ❌ Skip commentary (all commentary translated?)
- [ ] ❌ Translate only partial page (all segments included?)
- [ ] ❌ Add extra JSON fields (only required fields used?)
- [ ] ❌ Leave placeholder text (all translations actually completed?)
- [ ] ❌ Copy-paste without verification (each translation is original work?)
- [ ] ❌ Skip research (documented non-obvious findings?)
- [ ] ❌ Create invalid JSON (file validates?)
- [ ] ❌ Use wrong page number (double-checked page number?)

**If any ✓, fix before saving.**

---

## How to Use This Checklist

### Method 1: Mental Walkthrough

Go through each checkbox mentally before saving. If you can't confidently check it, review that aspect.

### Method 2: Systematic Review

Complete the checklist in order:
1. Pre-translation checks
2. During translation checks
3. Post-translation polish checks
4. Pre-save format checks
5. Final verification checks

### Method 3: Sampling

For experienced translators: Sample-check at least 50% of items each time, rotating which items you check.

**Recommendation**: Use Method 2 (systematic) for first 5-10 pages, then transition to Method 1 (mental) once workflow is internalized.

---

## Checklist Completion Standard

**To mark a page as complete, you must:**

1. Complete ALL items in "Pre-Save Checklist" (100%)
2. Complete ALL items in "Final Verification Checklist" (100%)
3. Complete at least 80% of "During Translation" items
4. Complete at least 80% of "Post-Translation" items

**If you cannot meet this standard:**
- Note what's incomplete in a `INCOMPLETE.md` file
- Save your partial work
- Return to complete it later
- Do not mark the page as "complete"

---

## Time-Boxing Guidelines

If you're stuck on a checklist item:

| Checklist Item | Max Time to Spend | If Still Stuck |
|----------------|-------------------|----------------|
| Research a passage | 10 minutes | Add note: "Uncertain: [question]" and continue |
| Polish a translation | 5 minutes per segment | Accept "good enough" and continue |
| Find a commentary | 3 minutes | If truly can't find it, note in `MISSING.md` |
| Validate JSON | 2 minutes | Use online JSON validator |

**Do not let perfection block completion. Document uncertainties and continue.**

---

## Example: Completed Checklist for Page 20

This is what a completed checklist looks like for reference:

```
✅ Pre-Translation Checklist (4/4 items)
✅ During Translation Checklist (11/11 items)
✅ Post-Translation Checklist (11/11 items)
✅ Pre-Save Checklist (13/13 items)
✅ Final Verification Checklist (9/9 items)
✅ Common Failures Check (8/8 verified NOT present)

Numerical checks:
- Segments: 7 (expected: 6-8) ✅
- Segments with commentary: 5 (71%, expected: 30%+) ✅
- Research notes: 8 (expected: 3+) ✅
- Languages per segment: 4 (expected: 4) ✅

Result: Page 20 COMPLETE and verified
```

---

## Checklist Violations: What to Do

If you realize you violated the checklist after saving:

### Minor Violation (1-2 items missed)
- Fix immediately
- Update the file
- Learn for next page

### Major Violation (3+ items missed)
- Re-do the page from scratch
- Don't try to patch it
- Better to spend 60 minutes doing it right than 30 minutes doing it wrong + 30 minutes fixing

### Systematic Violations (same items missed repeatedly)
- Review the corresponding section in `TRANSLATION_INSTRUCTIONS_V2.md`
- Read examples in `QUALITY_GUIDE.md`
- Slow down and be more deliberate

---

## Final Reminder

**This checklist exists to ensure quality and completeness.**

It may feel tedious initially, but:
1. It prevents incomplete work
2. It catches errors before they propagate
3. It builds good habits
4. It ensures consistency across all translators

**Every checkbox is there for a reason—use it.**

---

*Quality over speed. Completeness over partial work. Honor the masterpiece.*
