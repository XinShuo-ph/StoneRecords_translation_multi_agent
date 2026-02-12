# Translation Validation Guide

## Purpose

This document provides self-checking procedures to ensure translation quality before moving to the next page.

**Run these checks BEFORE saving each page.**

---

## Automated Validation

### Quick Validation Command

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

This will check:
- ✅ Valid JSON syntax
- ✅ Required fields present
- ✅ No empty translation fields
- ✅ Sequential segment IDs
- ✅ Page number matches file name
- ✅ All segments have all 4 languages

### Expected Output

**✅ Pass**:
```
✓ Valid JSON syntax
✓ Page number matches file name (0020)
✓ All required fields present
✓ 6 segments with sequential IDs
✓ All segments have all 4 languages
✓ No empty translation fields
✓ 12 commentary annotations validated

VALIDATION PASSED ✓
Ready to commit.
```

**❌ Fail**:
```
✗ Segment 3: Missing 'ru' translation
✗ Segment 5: Empty 'en' translation
✗ Commentary 2 in segment 4: Missing 'ja' translation

VALIDATION FAILED ✗
Fix these issues before continuing.
```

---

## Manual Validation Checklist

Use this if the validation script is unavailable.

### Before Saving

#### 1. File Naming
- [ ] File name is `page_XXXX.json` (4 digits, zero-padded)
- [ ] Example: `page_0020.json` NOT `page_20.json`

#### 2. Page Number Consistency
- [ ] `page` field matches the PDF page number
- [ ] `page` field matches the file name
- [ ] Example: File `page_0020.json` → `"page": 20`

#### 3. Completeness Check
- [ ] ALL visible text on the PDF page is translated
- [ ] No sentences skipped
- [ ] No paragraphs skipped
- [ ] All commentary translated (if present)

#### 4. Translation Fields
For EACH segment, verify:
- [ ] `original` is non-empty
- [ ] `zh_modern` is non-empty
- [ ] `en` is non-empty
- [ ] `ru` is non-empty
- [ ] `ja` is non-empty

#### 5. Commentary Fields
For EACH commentary (if present), verify:
- [ ] `source` is present (e.g., "甲戌本")
- [ ] `original` is non-empty
- [ ] `zh_modern` is non-empty
- [ ] `en` is non-empty
- [ ] `ru` is non-empty
- [ ] `ja` is non-empty

#### 6. Sequential IDs
- [ ] Segment IDs start at 1
- [ ] Segment IDs are consecutive: 1, 2, 3, 4, ...
- [ ] No gaps in IDs
- [ ] No duplicate IDs

#### 7. JSON Syntax
- [ ] File parses as valid JSON
- [ ] No trailing commas
- [ ] Proper quote escaping
- [ ] Proper UTF-8 encoding

#### 8. Required Fields Present
- [ ] `page` (number)
- [ ] `chapter` (string)
- [ ] `segments` (array with at least 1 item)

---

## Quality Validation

### Tier 1 (Minimum) Checklist

Verify you meet the **minimum acceptable quality**:

- [ ] All main text translated
- [ ] All 4 languages present for each segment
- [ ] Valid JSON
- [ ] Correct page number
- [ ] At least 1 segment

### Tier 2 (Good) Checklist

Verify you meet the **recommended quality**:

- [ ] All commentary translated
- [ ] At least 1-2 research notes (for puns, allusions)
- [ ] Consistent character name translations
- [ ] Literary quality preserved (not too literal)

### Tier 3 (Excellent) Checklist

Verify you meet **excellent quality**:

- [ ] Deep research notes on cultural context
- [ ] Poetry meter/form analysis (if poetry present)
- [ ] Scholarly references cited
- [ ] Polished translations (reviewed and refined)

**Your target: Tier 2**

---

## Common Validation Failures

### Issue 1: Empty Translation Field

**Error**:
```json
{
  "original": "此开卷第一回也。",
  "zh_modern": "这是开篇的第一回。",
  "en": "",  // ❌ Empty!
  "ru": "Это первая глава.",
  "ja": "これが第一回である。"
}
```

**Fix**: Add the English translation.

---

### Issue 2: Missing Language

**Error**:
```json
{
  "original": "此开卷第一回也。",
  "zh_modern": "这是开篇的第一回。",
  "en": "This is the first chapter.",
  "ru": "Это первая глава."
  // ❌ Missing 'ja'!
}
```

**Fix**: Add the Japanese translation field.

---

### Issue 3: Non-Sequential IDs

**Error**:
```json
{
  "segments": [
    {"id": 1, ...},
    {"id": 3, ...},  // ❌ Skipped 2!
    {"id": 4, ...}
  ]
}
```

**Fix**: Renumber IDs to be consecutive: 1, 2, 3.

---

### Issue 4: Wrong Page Number

**Error**:
File: `page_0020.json`
```json
{
  "page": 21,  // ❌ Doesn't match file name!
  ...
}
```

**Fix**: Change to `"page": 20` to match file name.

---

### Issue 5: Incomplete Commentary

**Error**:
```json
{
  "commentary": [
    {
      "source": "甲戌本",
      "original": "能解者方有辛酸之泪。",
      "zh_modern": "能够理解的人才会流下辛酸的眼泪。"
      // ❌ Missing en, ru, ja!
    }
  ]
}
```

**Fix**: Add English, Russian, and Japanese translations.

---

### Issue 6: Invalid JSON Syntax

**Error**:
```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "...",
      ...
    },  // ❌ Trailing comma before closing bracket!
  ]
}
```

**Fix**: Remove the trailing comma.

---

### Issue 7: Null Values

**Error**:
```json
{
  "original": "此开卷第一回也。",
  "zh_modern": null,  // ❌ Null!
  "en": "This is the first chapter.",
  ...
}
```

**Fix**: Replace `null` with actual translation.

---

### Issue 8: Missing Content

**Symptom**: Validation passes, but you only translated 2 sentences when the page has 10 sentences.

**Check**: 
1. Open the PDF page image
2. Count all sentences/paragraphs
3. Verify each one has a corresponding segment

**Fix**: Add missing segments.

---

## Pre-Commit Validation Workflow

Before committing your work:

### Step 1: Run Validation
```bash
python3 tools/validate_json.py translations/page_0020.json
```

### Step 2: Check Output
- If **PASSED** ✅ → Proceed to Step 3
- If **FAILED** ❌ → Fix errors and return to Step 1

### Step 3: Visual Verification
Open the page image side-by-side with your JSON:
- Count sentences on page
- Count segments in JSON
- Verify they match

### Step 4: Quality Check
Ask yourself:
- Did I translate EVERYTHING on the page?
- Are all 4 languages present and non-empty?
- Did I include notes for any puns/allusions I found?
- Is the JSON valid?

### Step 5: Save and Continue
If all checks pass:
- Save the file
- Move to next page immediately

---

## Validation Script Usage

### Basic Usage
```bash
python3 tools/validate_json.py translations/page_0020.json
```

### Validate Multiple Files
```bash
python3 tools/validate_json.py translations/page_00*.json
```

### Validate All Translations
```bash
python3 tools/validate_json.py translations/*.json
```

### Validate and Show Details
```bash
python3 tools/validate_json.py --verbose translations/page_0020.json
```

### Expected Exit Codes
- `0` - Validation passed
- `1` - Validation failed

---

## Self-Checking Questions

Before declaring a page "complete", answer these:

### Completeness
1. Did I translate EVERY sentence on this PDF page?
2. Did I translate ALL commentary annotations?
3. Did I check for poems and translate them?

### Quality
4. Are all 4 language translations present and non-empty?
5. Do the translations preserve literary quality?
6. Are character names consistent with the glossary?

### Technical
7. Is the JSON syntactically valid?
8. Are segment IDs sequential?
9. Does the page number match the file name?

### Research
10. Did I note any character name puns?
11. Did I note any classical allusions?
12. Did I add translator notes for non-obvious findings?

**If you answer "No" to any question**: Fix it before moving on.

---

## Quick Visual Validation

### Compare Side-by-Side

**PDF Page (left)** | **Your JSON (right)**

Count:
- Paragraphs on page → Should equal number of prose segments
- Poems on page → Should equal number of poem segments
- Annotation marks → Should equal number of commentary items

**If counts don't match**: You missed something.

---

## Validation Automation

### Create a Pre-Save Hook

Add this to your workflow:

```bash
#!/bin/bash
# validate_and_save.sh

PAGE_NUM=$1
JSON_FILE="translations/page_$(printf '%04d' $PAGE_NUM).json"

echo "Validating $JSON_FILE..."
python3 tools/validate_json.py "$JSON_FILE"

if [ $? -eq 0 ]; then
  echo "✓ Validation passed! Ready to commit."
  exit 0
else
  echo "✗ Validation failed. Fix errors before continuing."
  exit 1
fi
```

Usage:
```bash
./validate_and_save.sh 20
```

---

## When Validation Fails

### Don't Panic
Validation failures are normal and easy to fix.

### Read the Error Message
The validation script tells you EXACTLY what's wrong:
```
✗ Segment 3: Missing 'ru' translation
```
This means: Go to segment 3, add the Russian translation.

### Fix One Error at a Time
Don't try to fix everything at once. Fix the first error, re-run validation, repeat.

### Common Fixes Take Seconds
- Empty field → Add translation
- Wrong ID → Renumber
- Trailing comma → Delete comma
- Missing field → Add field

---

## Validation Best Practices

### 1. Validate Early and Often
Don't wait until the end. Validate after every 2-3 segments.

### 2. Keep the Validator Running
In a separate terminal:
```bash
watch -n 10 'python3 tools/validate_json.py translations/page_0020.json'
```
This re-runs validation every 10 seconds.

### 3. Use Editor Validation
If your editor supports JSON schema validation, use it!

### 4. Test the Validator First
Before starting, verify the validator works:
```bash
python3 tools/validate_json.py --help
```

---

## Summary

**Before moving to the next page**:

1. ✅ Run `python3 tools/validate_json.py translations/page_XXXX.json`
2. ✅ Verify all checks pass
3. ✅ Visual verification: compare PDF with JSON
4. ✅ Quality check: Tier 2 target met
5. ✅ Save file

**Only then**: Start next page.

---

**Validation is not optional. It's the minimum quality gate before continuing.**
