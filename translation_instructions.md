# Translation Instructions — 红楼梦脂评汇校本

> **This document covers ONLY the translation task.**
> It is completely independent of any parallel execution protocol.
> A single agent following these instructions should be able to produce correct output without any coordination files.

---

## 1. What You Are Translating

**Source**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`

Each PDF page contains two kinds of content:

- **Main text (正文)**: The novel's narrative — prose, dialogue, poetry.
- **Commentary (脂评)**: Annotations from historical manuscripts, marked with tags like 【甲戌】【庚辰】【己卯】 etc. Commentary appears as 眉批 (top margin), 夹批 (inline), 侧批 (side margin), or 回末批 (end-of-chapter).

**You must translate ALL visible content on every assigned page — both main text and every piece of commentary.**

**Target languages** (for every segment and every commentary):
1. Modern Chinese (简体中文)
2. English
3. Russian (Русский)
4. Japanese (日本語)

---

## 2. Output Format — One JSON File Per Page

Save each page as `translations/page_XXXX.json` (zero-padded 4-digit page number).

### 2.1 Complete JSON Schema

```json
{
  "page": 20,
  "chapter": "第一回",
  "total_segments": 7,
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "原文...",
      "zh_modern": "现代文...",
      "en": "English...",
      "ru": "Русский...",
      "ja": "日本語...",
      "commentary": [
        {
          "type": "夹批",
          "source": "甲戌本",
          "position": "after 原文片段",
          "original": "批语原文...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "translator_notes": [
    "Note 1: research finding about a pun or allusion",
    "Note 2: cultural context"
  ]
}
```

### 2.2 Field-by-Field Specification

**Every field listed below is REQUIRED. Do not omit any.**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `page` | integer | PDF page number | `20` |
| `chapter` | string | Chapter label | `"第一回"`, `"前言"`, `"凡例"` |
| `total_segments` | integer | Number of segments (must equal `segments.length`) | `7` |
| `segments` | array | Array of segment objects (see below) | `[...]` |
| `translator_notes` | array of strings | Research findings: puns, allusions, cultural context | `["Note..."]` |

**Each segment object:**

| Field | Type | Description | Rules |
|-------|------|-------------|-------|
| `id` | integer | Sequential starting from 1 | Must be 1, 2, 3... in order |
| `type` | string | Content type | Must be `"prose"`, `"poem"`, or `"dialogue"` |
| `original` | string | Original Classical Chinese text | Must be the ACTUAL text from the page — never a summary or placeholder |
| `zh_modern` | string | Modern Chinese translation | Full translation, not a summary |
| `en` | string | English translation | Full translation |
| `ru` | string | Russian translation | Full translation |
| `ja` | string | Japanese translation | Full translation |
| `commentary` | array | Commentary annotations on this segment | Use `[]` if no commentary on this segment |

**Each commentary object:**

| Field | Type | Description | Rules |
|-------|------|-------------|-------|
| `type` | string | Commentary type | Must be one of: `"眉批"`, `"夹批"`, `"侧批"`, `"回前批"`, `"回末批"`, `"回末总批"` |
| `source` | string | Manuscript source | e.g., `"甲戌本"`, `"庚辰本"`, `"己卯本"`, `"蒙府本"`, `"戚序本"` |
| `position` | string | Where commentary appears relative to text | e.g., `"after 甄士隐三字"`, `"top margin"` |
| `original` | string | Original commentary text | Actual text — never a summary |
| `zh_modern` | string | Modern Chinese translation | Full translation |
| `en` | string | English translation | Full translation |
| `ru` | string | Russian translation | Full translation |
| `ja` | string | Japanese translation | Full translation |

### 2.3 Strict Format Rules

1. **No extra top-level keys.** Only `page`, `chapter`, `total_segments`, `segments`, `translator_notes`.
2. **No `null` values.** Every field must have content. Use `[]` for empty commentary arrays. Use `[]` for translator_notes if you truly have nothing to note (but you should always have notes).
3. **Sequential IDs.** Segment IDs must be 1, 2, 3... with no gaps.
4. **`total_segments` must match.** It must equal the actual number of items in `segments`.
5. **All 5 text fields required per segment.** `original`, `zh_modern`, `en`, `ru`, `ja` — none may be empty.
6. **All 8 fields required per commentary.** `type`, `source`, `position`, `original`, `zh_modern`, `en`, `ru`, `ja`.
7. **Valid JSON.** Escape special characters. No trailing commas. UTF-8 encoding.

---

## 3. Workflow Per Page

Follow these steps in order for every page.

### Step 1: Read the Page

Open the page image (`source_pages/page_XXXX.png`) and/or the PDF.

Identify **all** content on the page:
- Main text paragraphs (narrative, dialogue)
- Poetry (verses, songs, riddles)
- Commentary (眉批 at top, 夹批 inline, 侧批 in margins)
- Chapter titles or section markers

**Critical: Verify you are looking at the correct page.** Compare the page number shown in the PDF with your target page number. If the content does not match what you expect for this chapter/section, STOP and re-check.

### Step 2: Transcribe the Original Text

Copy (or carefully transcribe) ALL original text from the page. Break it into logical segments:
- Each paragraph of prose → one segment
- Each poem or verse → one segment (with `\n` between lines)
- Each passage of dialogue → one segment (or group short exchanges)

**The `original` field must contain the ACTUAL text visible on the page.** If you cannot read certain characters, mark them as `[?]` — but never substitute placeholder text like `"[dialogue about family matters]"` or summaries.

### Step 3: Research Before Translating

Before writing any translation, check the reference materials:
- `research/glossary.md` — Consistent names and terms across all languages
- `research/character_guide.md` — Character profiles and relationships
- `research/commentary_guide.md` — How to identify and categorize commentary
- `research/poetry_guide.md` — Poetry translation approaches
- `research/chapter_structure.md` — Chapter summaries for context
- `research/cultural_context.md` — Historical and cultural background
- `research/existing_translations.md` — How prior translators handled key passages

Look up any classical allusions (典故), character name puns, or unfamiliar terms. Record what you find in `translator_notes`.

### Step 4: Translate

For each segment, produce all four translations:

**Modern Chinese (简体中文):**
- Use standard modern Mandarin
- Preserve classical flavor — do not over-modernize
- Keep original allusions and imagery
- Clarify obscure classical grammar without dumbing down

**English:**
- Scholarly literary register
- Use Pinyin for names: Jia Baoyu (not "Precious Jade"), Lin Daiyu, etc.
- Follow the glossary in `research/glossary.md` for all name/term translations
- Add brief parenthetical context only when essential for comprehension

**Russian (Русский):**
- Literary Russian appropriate for classical literature translation
- Preserve the aristocratic register
- Use transliterated names per the glossary
- Maintain the emotional subtlety of the original

**Japanese (日本語):**
- Classical-influenced literary style (文語的な文体)
- Use 音読み for Chinese names per the glossary
- Maintain poetic structure where applicable

**For all languages:** Translate COMPLETELY. Every sentence in the original must appear in every translation. If you are uncertain about a passage, translate it to the best of your ability and add an "Uncertain" note in `translator_notes` — never leave it out.

### Step 5: Translate Commentary

Translate every commentary annotation with the same four-language treatment. Identify:
- The `type` (眉批/夹批/侧批/回末批 etc.)
- The `source` manuscript (甲戌本/庚辰本 etc.) — look for 【brackets】
- The `position` relative to the main text

Attach each commentary to the segment it annotates.

### Step 6: Validate

Before saving, mentally verify:

- [ ] `page` number matches the actual PDF page
- [ ] Every piece of visible text on the page is accounted for in segments
- [ ] Every segment has all 5 text fields filled (original + 4 translations)
- [ ] Every commentary has all 8 fields filled
- [ ] `total_segments` equals the actual count of segments
- [ ] Segment IDs are sequential (1, 2, 3...)
- [ ] `translator_notes` contains at least one research observation
- [ ] JSON is valid (no syntax errors)

If the validation tool is available, run: `python3 tools/validate_json.py translations/page_XXXX.json`

### Step 7: Save and Continue

Save the file and move to the next page. Do not stop between pages.

---

## 4. Translation Quality Standards

### 4.1 Literary Quality

红楼梦 is one of the greatest novels in world literature. Your translations must reflect:
- **Elegance**: Preserve the beauty of the original prose
- **Psychological depth**: Capture subtle emotional nuances
- **Symbolic richness**: Names and objects carry meaning — preserve or annotate it
- **Poetry**: Maintain verse structure, rhythm, and imagery

### 4.2 Completeness Standards

A properly translated page should have:
- **Every paragraph** of main text as a separate segment
- **Every poem** as a segment (type `"poem"`)
- **Every dialogue exchange** captured (type `"dialogue"`)
- **Every commentary annotation** attached to the correct segment
- **Research notes** documenting puns, allusions, or cultural context

A typical content-rich page will have 3-8 segments. A page with only 1-2 segments is likely INCOMPLETE — go back and check for missed content.

### 4.3 Name Puns to Document

Many names in 红楼梦 contain hidden meanings. Always note these in `translator_notes`:

| Name | Hidden Meaning |
|------|----------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 — True events hidden |
| 贾雨村 (Jia Yucun) | 假语存 — False words remain |
| 贾宝玉 (Jia Baoyu) | 假宝玉 — False precious jade |
| 贾府 | 假 — False/illusory |
| 封肃 | 风俗 — Social customs |
| 元迎探惜 | 原应叹息 — Should sigh/lament |

### 4.4 Glossary Compliance

You MUST use the standardized translations from `research/glossary.md`. Key examples:

| Chinese | English | Russian | Japanese |
|---------|---------|---------|----------|
| 林黛玉 | Lin Daiyu | Линь Дайюй | 林黛玉（りんたいぎょく）|
| 贾宝玉 | Jia Baoyu | Цзя Баоюй | 賈宝玉（かほうぎょく）|
| 荣国府 | Rong-guo House | Дом Жунго | 栄国府（えいこくふ）|
| 太虚幻境 | Land of Illusion | Царство Великой Пустоты | 太虚幻境 |
| 丫鬟 | maid(servant) | служанка | 女中 |
| 老爷 | Master | Господин | 旦那様 |

---

## 5. Things That Will Be Considered Failures

These are the specific anti-patterns observed in prior experiments. **Do not do any of these.**

### 5.1 Placeholder or Summary Text (CRITICAL)

**WRONG:**
```json
"original": "[Dialogue between family members discussing arrangements]"
```
```json
"original": "[Continued family dialogue and narrative]"
```

**RIGHT:**
```json
"original": "黛玉方进入房时，只见两个人搀着一位鬓发如银的老母迎上来..."
```

The `original` field must contain the actual Classical Chinese text from the page. Summaries, descriptions, or placeholders in brackets are never acceptable.

### 5.2 Wrong Page Content

If you are assigned page 47, you must translate the content that appears on PDF page 47. Not page 46, not page 48, not a mix. Verify the page number before starting.

### 5.3 Incomplete Page Coverage

If a page has 6 paragraphs of text and 4 commentary annotations, your output must account for all of them. Do not translate only the first paragraph and skip the rest.

### 5.4 Missing Translation Fields

**WRONG:**
```json
{
  "id": 1,
  "type": "prose",
  "original": "原文...",
  "en": "English..."
}
```

Every segment needs all 5 text fields: `original`, `zh_modern`, `en`, `ru`, `ja`.

### 5.5 Missing or Malformed Commentary

If commentary is visible on the page, it MUST appear in the output. Each commentary must have `type`, `source`, `position`, `original`, and all 4 translations.

### 5.6 Invalid JSON

Trailing commas, unescaped quotes, missing brackets — all make the file unusable. Always verify your JSON is syntactically valid.

### 5.7 Extra/Non-Standard Fields

Do not add fields not in the schema (e.g., `chapter_title`, `page_content_type`, `characters_appearing`, `research_notes`, `manuscript_sources_on_page`). Stick to the exact schema defined in Section 2.

### 5.8 Stopping Early

If your session can continue, keep translating the next page. Do not stop after one or two pages if you have more to do.

---

## 6. Handling Edge Cases

### Page Crosses a Chapter Boundary

If a page contains the end of one chapter and the start of another:
- Use the chapter label of whichever chapter has MORE content on the page
- Note the chapter boundary in `translator_notes`

### Page Ends Mid-Sentence

- Include whatever text is on the page (even if incomplete)
- Note in `translator_notes`: "Text continues on next page"

### Illegible or Damaged Text

- Transcribe what you can read
- Mark unclear characters as `[?]`
- Note in `translator_notes`: "Characters unclear at [location]"

### Page Contains Only Commentary (No Main Text)

- Still create segments for the commentary, setting `type` to `"prose"` and `original` to the commentary's parent text if identifiable
- If the page is a 回末批 (chapter-end commentary), create one segment per commentary block

### Front Matter / Table of Contents Pages

- Translate these as well using the standard format
- Set `chapter` to `"前言"`, `"凡例"`, `"目录"`, etc. as appropriate

---

## 7. Reference File Locations

| File | Purpose |
|------|---------|
| `research/glossary.md` | **Mandatory** — Names, terms, translations across all 4 languages |
| `research/character_guide.md` | Character profiles and relationships |
| `research/chapter_structure.md` | Chapter titles, summaries, and PDF page mapping |
| `research/commentary_guide.md` | Commentary types, manuscript sources, visual identification |
| `research/poetry_guide.md` | Poetry forms and translation approaches |
| `research/cultural_context.md` | Historical and cultural background |
| `research/existing_translations.md` | Prior translation approaches (Hawkes, Yang Xianyi, etc.) |
| `examples/page_0020.json` | Reference example of a completed page translation |
| `tools/validate_json.py` | Validation tool — run before committing |

---

## 8. Quick Reference Card

```
For each page:
  1. READ the page image/PDF → identify all content
  2. VERIFY the page number is correct
  3. RESEARCH allusions, names, terms → check glossary
  4. TRANSCRIBE original text into segments
  5. TRANSLATE each segment into 4 languages
  6. TRANSLATE each commentary into 4 languages
  7. WRITE translator_notes with research findings
  8. VALIDATE: all fields present, JSON valid, total_segments correct
  9. SAVE to translations/page_XXXX.json
  10. CONTINUE to next page
```
