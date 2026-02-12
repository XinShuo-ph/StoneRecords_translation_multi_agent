# 红楼梦 Translation Instructions

## Mission

Translate 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary) page by page into four languages with scholarly rigor and literary artistry.

**This is one of world literature's greatest masterpieces. Every word deserves careful attention.**

---

## Target Languages

Each PDF page is translated into:
1. **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
2. **English** - Scholarly literary translation
3. **Russian (Русский)** - Literary Russian translation
4. **Japanese (日本語)** - Classical-influenced literary Japanese

---

## Source Material

**PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`  
**Page Images**: `source_pages/page_XXXX.png`

Each PDF page contains:
- **Main text (正文)**: The novel's narrative
- **Commentary (脂评)**: Annotations marked with 【甲戌】【庚辰】【己卯】etc.

**Work unit**: ONE PDF page = ONE JSON file

---

## JSON Output Format

Save each page as `translations/page_XXXX.json` (4-digit page number).

### Minimal Required Format

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "士隐意欲也跟了过去...",
      "zh_modern": "士隐也想要跟着过去...",
      "en": "Shiyin wished to follow them...",
      "ru": "Шиинь хотел последовать за ними...",
      "ja": "士隠も後を追おうとして...",
      "commentary": [
        {
          "source": "脂批",
          "original": "真是大警觉大转身。",
          "zh_modern": "真是大警醒大转折。",
          "en": "Truly a great awakening and great turning point.",
          "ru": "Поистине великое пробуждение и великий поворот.",
          "ja": "まことに大いなる警醒、大いなる転身なり。"
        }
      ]
    }
  ],
  "notes": [
    "英莲 (Yinglian): Her name is a pun on 应怜 (should be pitied).",
    "菱花: 'Water-chestnut flower' puns on 英莲's later name 香菱.",
    "元宵 (Lantern Festival): Foreshadows when Yinglian will be kidnapped."
  ]
}
```

### Required Fields Only

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | PDF page number |
| `chapter` | string | "前言", "第一回", "第二回", etc. |
| `segments` | array | Array of text segments (see below) |
| `notes` | array | Research findings and translator notes |

### Segment Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Sequential ID (1, 2, 3...) |
| `type` | string | "prose", "poem", or "dialogue" |
| `original` | string | Original Classical Chinese text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |
| `commentary` | array | Commentary annotations (empty `[]` if none) |

### Commentary Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Manuscript source: "脂批", "甲戌本", "庚辰本", etc. |
| `original` | string | Original commentary text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |

### Format Rules

1. **ONLY these fields** - Do not add extra fields
2. **All fields required** - No null/empty values for translations
3. **UTF-8 encoding** - All CJK characters must render correctly
4. **Valid JSON** - Must parse without errors
5. **Sequential IDs** - Start from 1, no gaps

---

## Workflow: Translate One Page

### Step 1: Open the Page

View the PDF page or corresponding image in `source_pages/page_XXXX.png`.

### Step 2: Identify All Content

Read carefully and identify EVERY element:
- Main narrative text (正文)
- Any poetry or verse
- ALL commentary annotations (眉批, 夹批, 侧批)
- Source tags (【甲戌】【庚辰】etc.)

### Step 3: Research EACH Segment

For each text segment, research:

**3a. Online Search**
- Search: `"红楼梦" + "text snippet" + "解读"`
- Read at least 2 scholarly sources
- Look for: allusions (典故), wordplay (双关), symbolism

**3b. Check Reference Materials**
- `research/glossary.md` - Character names and terms
- `research/character_guide.md` - Character backgrounds
- `research/cultural_context.md` - Historical context
- `research/poetry_guide.md` - Poetry translation approach
- `research/commentary_guide.md` - Commentary sources

**3c. Document Findings**
- If you discover anything non-trivial, add it to `notes`
- Examples: name puns, hidden meanings, foreshadowing, allusions
- Time-box: If nothing found in 5 minutes, mark as straightforward and continue

### Step 4: Translate to All Languages

For each segment:

1. Copy original Classical Chinese to `original`
2. Translate to Modern Chinese → `zh_modern`
3. Translate to English → `en`
4. Translate to Russian → `ru`
5. Translate to Japanese → `ja`

**Translate ALL commentary the same way.**

### Step 5: Polish Each Translation

Review and refine:

**5a. Literary Quality**
- Does it capture the original's elegance?
- Does poetry feel like poetry?
- Is the rhythm natural?

**5b. Cultural Fit**
- **Modern Chinese**: Accessible but retains classical flavor
- **English**: Scholarly literary register, use Pinyin for names
- **Russian**: Literary Russian, aristocratic register
- **Japanese**: Classical-influenced literary style, 音読み for names

**5c. Accuracy Check**
- All four translations convey the same core meaning?
- No loss of nuance?
- Commentary preserves the original's intent?

### Step 6: Self-Verification Checklist

Before saving, verify:

- [ ] Every visible text segment on the page is translated
- [ ] Every commentary annotation is translated
- [ ] All 4 languages present for EVERY segment
- [ ] All segments have `commentary` field (even if empty `[]`)
- [ ] At least 3 research notes in `notes` (if applicable)
- [ ] JSON is valid (no syntax errors)
- [ ] Sequential IDs (1, 2, 3...)
- [ ] Re-read the original page - did I miss anything?

### Step 7: Save the JSON File

Save to `translations/page_XXXX.json` with 4-digit page number.

### Step 8: Continue to Next Page

Immediately move to the next page. Do not pause.

---

## Quality Standards

### Translation Philosophy

红楼梦 is:
- **World-class literature** - Not pulp fiction
- **Psychologically subtle** - Every word carries emotional weight
- **Symbolically rich** - Names, objects, numbers have meanings
- **Culturally deep** - Embedded in Qing Dynasty aristocratic life

Your translations must:
- **Preserve literary beauty** - Don't over-simplify
- **Maintain psychological nuance** - Subtle emotions matter
- **Explain cultural context** - Add notes for non-Chinese readers
- **Respect the original** - Cao Xueqin's artistry deserves care

### Examples of Quality Translation

**Original**: 满纸荒唐言，一把辛酸泪。

**❌ Bad Modern Chinese**: 整页都是胡说八道，还有很多伤心的眼泪。  
**✓ Good Modern Chinese**: 满纸都是荒唐的话语，包含着一把辛酸的眼泪。

**❌ Bad English**: The whole page is nonsense, with a lot of sad tears.  
**✓ Good English**: Pages full of idle words, a handful of bitter tears.

**Why?** 
- "荒唐" is deliberate artistic self-deprecation, not literal "nonsense"
- "一把" is a literary measure word, not "a lot"
- Rhythm and conciseness matter in poetry

### Character Name Translation

Many names contain puns:

| Name | Literal | Hidden Meaning |
|------|---------|----------------|
| 甄士隐 | Zhen Shiyin | 真事隐 (True events hidden) |
| 贾雨村 | Jia Yucun | 假语存 (False words remain) |
| 英莲 | Yinglian | 应怜 (Should be pitied) |

**Rule**: Always transliterate names (Pinyin for English, appropriate systems for Russian/Japanese), then explain the pun in `notes`.

### Commentary Translation

The 脂评 (Zhiping commentary) is valuable scholarship:
- **Translate all commentary** - Don't skip it
- **Preserve source attribution** - Note which manuscript (甲戌本, 庚辰本, etc.)
- **Maintain commentary's tone** - Often poetic or enigmatic itself
- **Research commentary** - It also requires interpretation

### Poetry Translation

The novel contains over 200 poems.

**Approach:**
1. **Meaning first** - Preserve the content accurately
2. **Structure awareness** - Note original form (绝句, 律诗, etc.)
3. **Rhythm where possible** - Natural flow in target language
4. **Don't force rhyme** - Better to preserve meaning than rhyme

**Example:**

**Original** (7-character quatrain):
```
世人都晓神仙好，惟有功名忘不了！
古今将相在何方？荒冢一堆草没了。
```

**English** (preserves meaning and rhythm, not rhyme):
```
Men all know that salvation should be won,
But with ambition they won't have done, have done.
Where are the famous ones of days gone by?
In grassy graves they lie now, every one.
```

---

## Common Pitfalls (Anti-Patterns)

### ❌ DON'T: Skip difficult passages
**✓ DO:** Translate everything, add notes for uncertainty

### ❌ DON'T: Translate only a few sentences per page
**✓ DO:** Translate ALL content visible on the page

### ❌ DON'T: Skip commentary because it's hard
**✓ DO:** Translate all commentary, it's part of the work

### ❌ DON'T: Over-modernize the language
**✓ DO:** Preserve literary and classical beauty

### ❌ DON'T: Add extra JSON fields for convenience
**✓ DO:** Use only the specified format

### ❌ DON'T: Submit without self-verification
**✓ DO:** Complete the checklist before saving

### ❌ DON'T: Rush through research
**✓ DO:** Spend time understanding each segment

### ❌ DON'T: Copy other translations verbatim
**✓ DO:** Use existing translations as reference only, create original work

---

## Reference Materials

Use these files as references:

| File | Purpose |
|------|---------|
| `research/glossary.md` | Consistent terminology |
| `research/character_guide.md` | Character backgrounds |
| `research/cultural_context.md` | Qing Dynasty context |
| `research/poetry_guide.md` | Poetry translation approach |
| `research/commentary_guide.md` | Commentary source guide |
| `research/existing_translations.md` | Reference translations |
| `examples/page_0020.json` | Full example of completed page |

---

## Continuous Work

Work continuously without pausing:

1. Open page → Research → Translate → Polish → Verify → Save
2. Move to next page immediately
3. Repeat until all assigned pages complete

**If stuck** on a passage for >10 minutes:
- Add a note: `"Uncertain: [your question]"`
- Continue to next segment
- Don't let one difficulty block all progress

---

## Success Criteria

A successful page translation has:

1. **Completeness**: Every text segment and commentary translated
2. **Quality**: All four languages are polished and literary
3. **Accuracy**: Faithful to the original meaning
4. **Research**: Non-trivial findings documented in `notes`
5. **Format**: Valid JSON with required fields only
6. **Verification**: Passed the 8-point checklist

---

## Example: Complete Page

See `examples/page_0020.json` for a full example meeting all criteria:
- 7 segments with all 4 languages
- 12 commentary annotations fully translated
- 8 research notes documenting findings
- Valid JSON format
- All content from page 20 included

---

## Quick Reference: Translation Checklist

**Before marking a page complete:**

- [ ] Opened and viewed the source page?
- [ ] Identified all text segments?
- [ ] Identified all commentary?
- [ ] Researched each segment?
- [ ] Translated all segments to 4 languages?
- [ ] Translated all commentary to 4 languages?
- [ ] Polished each translation for literary quality?
- [ ] Documented findings in `notes`?
- [ ] Used correct JSON format (required fields only)?
- [ ] Validated JSON syntax?
- [ ] Sequential segment IDs (1, 2, 3...)?
- [ ] Re-read source page to check for missed content?

**If all ✓, save and continue to next page.**

---

*This is scholarly work on a literary masterpiece. Take your time, do it right, and honor Cao Xueqin's artistry.*
