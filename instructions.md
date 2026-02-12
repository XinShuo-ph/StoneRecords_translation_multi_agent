# Translation Instructions

Translate pages from 红楼梦脂评汇校本 (Dream of the Red Chamber, Zhiping Commentary Edition) into four languages: Modern Chinese, English, Russian, and Japanese.

Each PDF page produces one JSON file. You must translate ALL visible text on each page — main text AND commentary.

---

## Source Material

- **PDF file**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf` (in workspace root)
- **Page images**: `source_pages/page_XXXX.png` (pre-extracted PNG images)
- **Reference materials**: `research/` directory (glossary, character guide, poetry guide, etc.)

### Page Numbering — READ THIS CAREFULLY

The page number in `page_XXXX.png` is the **physical PDF page number** (the position of the page in the PDF file). This is NOT the number printed at the bottom of the page.

For example, `source_pages/page_0020.png` is the 20th page of the PDF file. The number printed at the bottom of that page happens to be "11". **Always use the PDF page number (the filename number), never the printed number.**

When you are assigned page 20, you must open `source_pages/page_0020.png` (or navigate to page 20 in the PDF). Verify visually that the content matches before translating. The first line of page 20 begins with: "士隐意欲也跟了过去".

---

## What the Source Contains

- **Main text (正文)**: The novel's narrative prose, dialogue, and poetry
- **Commentary (脂评)**: Annotations from historical manuscript sources, marked with tags like【甲戌】【庚辰】【己卯】etc. These appear as red or differently-formatted text in the margins or inline.

Commentary types by position:

| Type | Position | Description |
|------|----------|-------------|
| 眉批 | Top margin | Extended commentary above main text |
| 夹批 | Inline | Brief notes inserted within the text flow |
| 侧批 | Side margin | Comments alongside main text |
| 回末批 | End of chapter | Summary commentary after chapter ends |

---

## Workflow Per Page

Follow these steps for every page. Do not skip steps.

### Step 1 — Read the Page

Open the page image (`source_pages/page_XXXX.png`). Also open the PDF to the same page for text clarity if the image is hard to read.

**Before doing anything else, confirm the page content.**

Identify every piece of text on the page:
- Main narrative text (prose, dialogue, poetry)
- All commentary annotations (in margins and inline)
- The chapter title if one appears on this page

Do NOT proceed until you have accounted for all visible text.

### Step 2 — Research

Before translating, consult the reference materials:
- `research/glossary.md` — Standardized translations for character names, places, terms
- `research/character_guide.md` — Character profiles and speech patterns
- `research/poetry_guide.md` — If the page contains poetry
- `research/commentary_guide.md` — Commentary source identification
- `research/existing_translations.md` — For reference (do NOT copy)
- `research/chapter_structure.md` — Chapter context

Look up any classical allusions (典故), character name puns, or cultural references. You will record your research findings in the `notes` field.

### Step 3 — Segment the Page

Divide the page's main text into segments. A **segment** is one of:
- A continuous block of prose narration (typically one paragraph on the page)
- A passage of dialogue (one speaker's complete utterance, including the narration tag like 某某道)
- A complete poem or verse (all lines together as one segment)

Rules for segmentation:
- Follow the natural paragraph breaks on the page
- Each segment should be a meaningful unit, not a single sentence
- If a paragraph is very long (more than ~200 characters), it is still ONE segment
- Poetry/verse is always one segment per poem, even if it spans many lines
- If the page starts mid-sentence (continuing from the previous page), that partial text is segment 1

### Step 4 — Translate

For each segment, produce all five text fields:
1. `original` — The original Classical Chinese text, copied exactly from the page
2. `zh_modern` — Modern Chinese (简体中文) translation
3. `en` — English translation
4. `ru` — Russian translation
5. `ja` — Japanese translation

Also translate every commentary annotation attached to or near each segment.

**Copying the original text**: Transcribe carefully from the page image. Do NOT mix commentary text into the main text. Commentary markers like【甲戌】belong in the commentary objects, not in the `original` field of the segment.

### Step 5 — Polish (润色)

Review each translation:
- Does the Modern Chinese preserve classical elegance while being accessible?
- Does the English read as scholarly literary prose?
- Does the Russian maintain the aristocratic literary register?
- Does the Japanese use appropriate classical-influenced style?
- Are character names consistent with `research/glossary.md`?
- Is poetry formatted with line breaks preserved?

### Step 6 — Save the JSON

Save to `translations/page_XXXX.json` (4-digit, zero-padded page number).

Validate your JSON before saving:
- Valid JSON syntax (no trailing commas, proper quoting)
- All required fields present
- All segments have all five text fields filled (no empty strings)
- Commentary arrays present (empty `[]` if no commentary for a segment)
- Sequential segment IDs starting at 1

### Step 7 — Next Page

Move to the next assigned page immediately. Do not stop between pages.

---

## JSON Format

Every translation file must use exactly this structure. No extra fields. No missing fields.

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "原文...",
      "zh_modern": "现代中文翻译...",
      "en": "English translation...",
      "ru": "Русский перевод...",
      "ja": "日本語訳...",
      "commentary": [
        {
          "source": "甲戌",
          "original": "批语原文...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": [
    "Research finding or translation note 1",
    "Research finding or translation note 2"
  ]
}
```

### Field Reference

**Top-level fields** (all required):

| Field | Type | Description |
|-------|------|-------------|
| `page` | integer | PDF page number (matches filename `page_XXXX.png`) |
| `chapter` | string | Chapter identifier: `"前言"`, `"凡例"`, `"第一回"`, `"第二回"`, etc. |
| `segments` | array | Array of segment objects (never empty) |
| `notes` | array of strings | Research findings, allusions, puns, cultural context, translation decisions |

**Segment fields** (all required):

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Sequential ID starting at 1 |
| `type` | string | One of: `"prose"`, `"poem"`, `"dialogue"` |
| `original` | string | Original Classical Chinese text (non-empty) |
| `zh_modern` | string | Modern Chinese translation (non-empty) |
| `en` | string | English translation (non-empty) |
| `ru` | string | Russian translation (non-empty) |
| `ja` | string | Japanese translation (non-empty) |
| `commentary` | array | Array of commentary objects. Use `[]` if no commentary for this segment. |

**Commentary fields** (all required when a commentary object exists):

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Manuscript source tag: `"甲戌"`, `"庚辰"`, `"己卯"`, `"脂批"`, etc. |
| `original` | string | Original commentary text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |

### What NOT to Include

Do not add any fields beyond those listed above. Specifically, do not add:
- `chapter_title` (not needed; the chapter title text goes in a segment if it appears on the page)
- `page_content_type` (not needed)
- `total_segments` (not needed; derivable from the array)
- `research_notes` (use `notes` instead)
- `translator_notes` (use `notes` instead)
- `characters_appearing` (not needed)
- `manuscript_sources_on_page` (not needed)
- `pdf_page` on segments (not needed; it's in the top-level `page` field)

---

## Translation Quality Standards

### General Principles

红楼梦 is one of the Four Great Classical Novels of Chinese literature and one of the greatest works of world literature. Your translations must reflect this stature.

- **Completeness**: Translate ALL text on the page. Every sentence, every commentary annotation.
- **Accuracy**: The `original` field must be an exact transcription of the source text. Do not paraphrase or abridge.
- **Fidelity**: Translations must convey the full meaning of the original. Do not omit phrases or simplify complex passages.
- **Literary quality**: Translations should read well in their target language. Avoid stilted or mechanical phrasing.

### By Language

**Modern Chinese (简体中文)**:
- 使用规范现代汉语，保留古典韵味
- 保留原有的典故和意涵
- 不要过度口语化
- 保持人物说话的语气和身份感

**English**:
- Scholarly literary register (think Penguin Classics, not casual)
- Use Pinyin for all character names: Jia Baoyu, Lin Daiyu, Xue Baochai
- Cultural concepts that have no English equivalent should be transliterated with a brief gloss on first appearance
- Poetry should preserve line structure and attempt natural rhythm

**Russian (Русский)**:
- Literary Russian appropriate for classical literature translation
- Preserve the aristocratic register of the original
- Use established Russian transliterations for character names (see glossary)
- Poetry should draw on Russian literary verse traditions

**Japanese (日本語)**:
- Classical-influenced literary style (文語的要素を含む文体)
- Use 音読み for Chinese character names
- Leverage shared kanji heritage where natural
- Poetry can preserve more of the original Chinese structure

### Character Names

Always use the standardized translations in `research/glossary.md`. Key examples:

| Original | English | Russian | Japanese |
|----------|---------|---------|----------|
| 贾宝玉 | Jia Baoyu | Цзя Баоюй | 賈宝玉（かほうぎょく） |
| 林黛玉 | Lin Daiyu | Линь Дайюй | 林黛玉（りんたいぎょく） |
| 甄士隐 | Zhen Shiyin | Чжэнь Шиинь | 甄士隠（しんしいん） |
| 贾雨村 | Jia Yucun | Цзя Юйцунь | 賈雨村（かうそん） |

### Character Name Puns

Many names contain hidden meanings through homophones. Record these in the `notes` field.

| Name | Hidden Meaning |
|------|----------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 — True events are hidden |
| 贾雨村 (Jia Yucun) | 假语存 — False words remain |
| 贾宝玉 (Jia Baoyu) | 假宝玉 — False precious jade |
| 元迎探惜 | 原应叹息 — One should sigh |

### Poetry

When a segment is type `"poem"`:
- Preserve line breaks with `\n` in all translation fields
- Maintain the verse structure (couplets, quatrains, etc.)
- In English, attempt natural rhythm without forcing rhyme
- Record the poem's form, allusions, and significance in `notes`

### Commentary

Commentary annotations are integral to this edition. Treat them with the same care as main text:
- Identify the manuscript source from the tag (【甲戌】→ `"甲戌"`, 【庚辰】→ `"庚辰"`)
- If no specific source is identifiable, use `"脂批"` as the source
- Translate the full commentary text in all four languages
- Commentary markers/tags should NOT appear in the segment's `original` field

---

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Translating the wrong page (confusing printed page number with PDF page number) | Always use the filename number from `source_pages/page_XXXX.png` |
| Translating only a few sentences instead of the entire page | Translate every line of text visible on the page |
| Mixing commentary text into the `original` field | Keep commentary markers (【甲戌】etc.) in commentary objects only |
| Leaving translation fields empty or with placeholder text | Every `original`, `zh_modern`, `en`, `ru`, `ja` field must contain real content |
| Adding extra fields to the JSON | Use exactly the fields defined above, no more |
| Using `translator_notes` or `research_notes` instead of `notes` | The field is called `notes` |
| Skipping commentary annotations | Translate ALL commentary visible on the page |
| Stopping to ask questions instead of continuing | Add a note like `"Uncertain: [your question]"` and continue |
| Producing invalid JSON | Validate JSON syntax before saving |
| Over-segmenting (one sentence per segment) | Follow paragraph structure; each segment is a meaningful block |
| Under-segmenting (entire page as one segment) | Separate distinct paragraphs, dialogue exchanges, and poems |

---

## Checklist — Verify Before Moving to Next Page

- [ ] The `page` field matches the `page_XXXX.png` filename number
- [ ] ALL visible text on the page is included in segments
- [ ] ALL commentary annotations are captured in the correct segment's `commentary` array
- [ ] Every segment has all 5 text fields (`original`, `zh_modern`, `en`, `ru`, `ja`) filled with real content
- [ ] Segment IDs are sequential (1, 2, 3...)
- [ ] Segment types are one of: `"prose"`, `"poem"`, `"dialogue"`
- [ ] Commentary sources are identified (`"甲戌"`, `"庚辰"`, `"脂批"`, etc.)
- [ ] The `notes` array contains research findings (allusions, puns, cultural context)
- [ ] Character names match `research/glossary.md`
- [ ] The JSON file is syntactically valid
- [ ] The file is saved as `translations/page_XXXX.json` with zero-padded 4-digit page number

---

## Continuous Execution

Work through your assigned pages one after another without stopping:

1. Read page → Research → Segment → Translate → Polish → Save JSON → Commit
2. Move to next page → Repeat

If stuck on a passage for more than a few minutes:
- Write your best attempt
- Add `"Uncertain: [description of the difficulty]"` to the `notes` array
- Continue to the next segment or page

Do not stop working until all assigned pages are complete.
