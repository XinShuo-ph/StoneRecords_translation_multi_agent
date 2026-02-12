# 红楼梦 Translation Instructions

## Mission

Translate pages from the PDF `红楼梦脂评汇校本_有书签目录_v3.13.pdf` into 4 languages.

**Input**: One PDF page
**Output**: One JSON file with translations in Modern Chinese, English, Russian, and Japanese

---

## 6-Step Workflow

### 1. View the Page

Open the page image: `source_pages/page_XXXX.png`

Identify all content:
- Main text (正文)
- Commentary (批语) - usually in smaller font with markers like 【甲戌】【庚辰】
- Poetry (if any)

### 2. Read & Understand

- Read the entire page carefully
- Identify character names, places, and cultural terms
- Check `research/glossary.md` for standard translations
- Note any puns, allusions, or special meanings

### 3. Translate to 4 Languages

For each text segment on the page:

1. **Modern Chinese (简体中文)**: Accessible contemporary Mandarin
2. **English**: Scholarly literary translation
3. **Russian (Русский)**: Literary translation
4. **Japanese (日本語)**: Classical-influenced literary Japanese

Translate ALL visible text: main text AND commentary.

### 4. Save as JSON

Save to `translations/page_XXXX.json` (4-digit page number, zero-padded).

Use the JSON schema below.

### 5. Validate

Run validation:
```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Fix any errors before continuing.

### 6. Next Page

Immediately start the next page. **Do not pause between pages.**

---

## JSON Schema

### Minimal Required Format

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "此开卷第一回也。",
      "zh_modern": "这是开篇的第一回。",
      "en": "This is the first chapter of the opening.",
      "ru": "Это первая глава книги.",
      "ja": "これが冒頭の第一回である。"
    }
  ]
}
```

### With Commentary (When Present)

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
      "ja": "...",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "能解者方有辛酸之泪。",
          "zh_modern": "能够理解的人才会流下辛酸的眼泪。",
          "en": "Only those who truly understand will shed bitter tears.",
          "ru": "Лишь тот, кто поистине понимает, прольёт горькие слёзы.",
          "ja": "能く解する者のみ辛酸の涙あり。"
        }
      ]
    }
  ]
}
```

### With Research Notes (When Meaningful Findings)

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [ ... ],
  "notes": [
    "甄士隐 (Zhen Shiyin) is a pun on 真事隐 (true events hidden)",
    "青埂峰 (Qing Gen Feng) puns on 情根 (root of passion)"
  ]
}
```

---

## Required Fields Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `page` | number | ✅ | PDF page number |
| `chapter` | string | ✅ | "前言", "第一回", "第二回", etc. |
| `segments` | array | ✅ | Array of text segments (at least 1) |
| `segments[].id` | number | ✅ | Sequential ID: 1, 2, 3, ... |
| `segments[].type` | string | ✅ | "prose", "poem", "dialogue" |
| `segments[].original` | string | ✅ | Original Classical Chinese text |
| `segments[].zh_modern` | string | ✅ | Modern Chinese translation |
| `segments[].en` | string | ✅ | English translation |
| `segments[].ru` | string | ✅ | Russian translation |
| `segments[].ja` | string | ✅ | Japanese translation |
| `segments[].commentary` | array | Optional | Commentary annotations (empty `[]` if none) |
| `notes` | array | Optional | Research findings and translator notes |

---

## Validation Checklist

Before moving to the next page, verify:

1. ✅ **File naming**: `page_XXXX.json` (4 digits, e.g., `page_0020.json`)
2. ✅ **Page number**: Matches the PDF page and file name
3. ✅ **All main text translated**: Every sentence on the page is in `segments`
4. ✅ **All 4 languages present**: Every segment has `zh_modern`, `en`, `ru`, `ja`
5. ✅ **No empty translations**: Every translation field has actual content (not "" or null)
6. ✅ **Valid JSON**: File parses without syntax errors
7. ✅ **Sequential IDs**: Segment IDs are 1, 2, 3, ... (no gaps)

**If any check fails**: Fix before continuing to next page.

---

## Translation Quality Guidelines

### Quality Tiers

**Tier 1 - MINIMUM ACCEPTABLE**:
- All main text translated ✅
- All 4 languages present ✅
- Valid JSON ✅
- Correct page number ✅

**Tier 2 - GOOD** (aim for this):
- All commentary translated ✅
- Basic research notes for puns/allusions ✅
- Consistent terminology (use glossary) ✅
- Literary quality preserved ✅

**Tier 3 - EXCELLENT** (bonus):
- Deep research notes on cultural context ✅
- Poetic meter analysis ✅
- Scholarly references ✅
- Polished literary translations ✅

**Your target**: Tier 2 (GOOD)

### Voice and Style by Language

**Modern Chinese (简体中文)**:
- Use standard modern Chinese grammar
- Keep classical elegance where possible
- Preserve literary flavor

**English**:
- Scholarly literary register (like David Hawkes' translation)
- Use Pinyin for names: Jia Baoyu, Lin Daiyu
- Keep honorifics: "young master", "madam", "master"

**Russian (Русский)**:
- Literary Russian suitable for 19th-century novels
- Preserve aristocratic register
- Use appropriate case and aspect

**Japanese (日本語)**:
- Classical-influenced literary style (文語的要素)
- Use 音読み (on-yomi) for Chinese names
- Literary register with respect language where appropriate

---

## Key Terms (Use Consistently)

| Classical | Zh Modern | English | Russian | Japanese |
|-----------|-----------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子 |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | 丫鬟/婢女 | maidservant | служанка | 女中 |
| 老爷 | 老爷 | master/sir | господин | 旦那様 |
| 太太 | 太太 | madam/lady | госпожа | 奥様 |

Full glossary: `research/glossary.md`

---

## Character Name Puns (Note These)

Many character names contain hidden meanings:

| Name | Pinyin | Hidden Meaning |
|------|--------|----------------|
| 甄士隐 | Zhen Shiyin | 真事隐 (true events hidden) |
| 贾雨村 | Jia Yucun | 假语存 (false words remain) |
| 贾宝玉 | Jia Baoyu | 假宝玉 (false jade) |
| 林黛玉 | Lin Daiyu | 林中黛玉 (jade in the forest) |

When you encounter these, add a note in the `notes` field.

---

## Commentary Types

| Type | Position | Description |
|------|----------|-------------|
| 眉批 | Top of page | Marginal commentary above text |
| 夹批 | Inline | Interlinear comments within text |
| 侧批 | Side | Side marginal comments |
| 回末批 | Chapter end | End-of-chapter commentary |

Translate all commentary you can identify. Include the source marker if visible (甲戌本, 庚辰本, etc.).

---

## Research Protocol

### REQUIRED (for every page):
1. Check `research/glossary.md` for character names and terms
2. Note the chapter context
3. Identify any character name puns

### CONDITIONAL (only when you see them):
4. If you see a classical allusion (典故) → research and add note
5. If you see wordplay/puns → research and add note
6. If commentary seems cryptic → research to understand it
7. If you see poetry → note the form and rhyme scheme

**Document findings** in the `notes` field.

**Time limit**: Don't spend more than 5 minutes researching one segment. If stuck, add a note like "Uncertain: [your question]" and continue.

---

## Common Issues to Avoid

❌ **Skipping content**: Translate EVERYTHING on the page, not just a few sentences
❌ **Empty translations**: Every field must have content (no `""` or `null`)
❌ **Wrong page number**: Triple-check page number before starting
❌ **Invalid JSON**: Always validate before moving on
❌ **Inconsistent names**: Use the same translation for character names throughout
❌ **Missing commentary**: Don't skip the small-print annotations
❌ **Stopping after 1 page**: Continue to next page immediately

---

## Continuous Work Protocol

After completing each page:

1. Save JSON file
2. Run `python3 tools/validate_json.py translations/page_XXXX.json`
3. If validation passes ✅ → **Immediately start next page**
4. If validation fails ❌ → Fix errors and retry

**Do NOT**:
- Pause between pages to ask for confirmation
- Wait for feedback
- Stop to review previous work
- Take breaks between pages

**ONLY STOP** when:
- All assigned pages are complete
- You encounter a blocking error you cannot resolve
- You are approaching context limit

---

## Examples

See `examples/` directory for complete examples:

- `examples/page_0020_minimal.json` - Simple prose page (Tier 1)
- `examples/page_0020_with_commentary.json` - Page with commentary (Tier 2)
- `examples/page_0025_poetry.json` - Page with poetry
- `examples/page_0015_chapter_start.json` - Chapter opening page
- `examples/page_0020_excellent.json` - Complex page with deep research (Tier 3)

---

## Quick Start Checklist

Before you begin your first page:

1. ✅ Read this entire document (you're doing it now!)
2. ✅ Review 2-3 examples in `examples/` directory
3. ✅ Check `research/glossary.md` for common terms
4. ✅ Confirm validation tool works: `python3 tools/validate_json.py --help`

Then start translating!

---

## Reference Materials

- `research/glossary.md` - Character names and terminology
- `research/character_guide.md` - Main character profiles
- `research/chapter_structure.md` - Chapter summaries
- `research/cultural_context.md` - Historical background
- `research/poetry_guide.md` - Poetry translation approaches
- `research/commentary_guide.md` - Commentary source guide

These are reference materials. You don't need to read them all before starting. Use them when needed.

---

**Ready? Start with your first assigned page and work continuously!**
