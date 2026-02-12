# Translation Instructions — 红楼梦脂评汇校本

You are translating pages from 红楼梦脂评汇校本 (Dream of the Red Chamber, Zhiping Commentary Collation) into four languages. This document contains **everything you need**. Follow it exactly.

---

## Your Task

For each assigned PDF page:

1. **Read** the page image carefully
2. **Transcribe** all original text (main text + commentary)
3. **Translate** into Modern Chinese, English, Russian, and Japanese
4. **Research** puns, allusions, and cultural context
5. **Save** as a valid JSON file
6. **Validate** your JSON before committing

---

## Step 1: Read the Page Image

Open the page image at `source_pages/page_XXXX.png`.

Study it carefully. Identify:
- **Main text (正文)**: The novel's narrative, in black
- **Commentary (脂评)**: Annotations in red or blue, marked with 【甲戌】【庚辰】etc.
- **Poetry**: Verse passages with distinct formatting
- **Dialogue**: Speech within quotation marks

**CRITICAL**: Your translation MUST match what is actually on the page image. Do NOT translate from memory or knowledge of the novel. The first line of your `original` text in segment 1 must match the first line of main text visible on the page image.

### Page Verification

After writing segment 1, verify: does your `original` field match the opening text visible on the page image? If not, you are translating the wrong content. Stop and re-read the image.

---

## Step 2: Segment the Page

Break the page content into logical segments. Each segment is one of:

| Type | Use for |
|------|---------|
| `prose` | Narrative paragraphs |
| `poem` | Poetry, songs, verse |
| `dialogue` | Direct speech by characters |

**Segmentation guidelines**:
- A typical page has 4-8 segments
- Each segment should contain a complete thought or paragraph
- Commentary is attached to the segment it annotates (not a separate segment)
- If a page starts/ends mid-sentence, include the partial text

---

## Step 3: Translate Each Segment

For every segment, provide all five text fields:

| Field | Content |
|-------|---------|
| `original` | Exact Classical Chinese from the page |
| `zh_modern` | Modern Chinese (简体中文) translation |
| `en` | English translation |
| `ru` | Russian translation |
| `ja` | Japanese translation |

### Translation Quality Standards

**红楼梦 is one of the greatest works of world literature.** Your translations must reflect this.

**Modern Chinese (简体中文)**:
- 使用规范简体中文，保留古典韵味
- 保留典故和文化内涵
- 确保现代读者能够理解

**English**:
- Scholarly literary register
- Pinyin for character names: Jia Baoyu, Lin Daiyu, Zhen Shiyin
- Preserve metaphors and imagery
- Natural English that reads as literature, not a word-for-word crib

**Russian (Русский)**:
- Literary Russian appropriate for classical literature
- Preserve aristocratic register for noble characters
- Attempt rhyme in poetry when natural

**Japanese (日本語)**:
- Classical-influenced literary style (文語的表現)
- Use 音読み for Chinese character names
- Use Japanese quotation marks「」for dialogue

### Poetry Translation

Poetry requires special care:
- Maintain the original line structure (line breaks with `\n`)
- Prioritize meaning > imagery > tone > sound
- Attempt rhyme only when it doesn't sacrifice meaning
- See `research/poetry_guide.md` for detailed guidance

---

## Step 4: Translate Commentary

Commentary (脂评) appears throughout the text in red/blue. For each commentary annotation:

1. Identify it on the page image
2. Determine its source: 【甲戌】【庚辰】【己卯】【蒙府】etc.
3. Transcribe the original
4. Translate into all four languages

Attach commentary to the segment it annotates, in the `commentary` array.

If a segment has no commentary, use an empty array: `"commentary": []`

See `research/commentary_guide.md` for commentary types and sources.

---

## Step 5: Research and Notes

The `notes` field is **mandatory**. For every page, research and document:

- **Name puns** (谐音): e.g., 甄士隐 = 真事隐 (true events hidden)
- **Classical allusions** (典故): literary/historical references
- **Foreshadowing** (伏笔): what events are being set up
- **Cultural context**: customs, social norms, Buddhist/Taoist concepts
- **Translation decisions**: why you chose a particular rendering

Minimum: 3 notes per page. If the page has poetry, allusions, or name puns, provide more.

Consult the reference materials in `research/`:
- `research/glossary.md` — Character names and key terms in all languages
- `research/character_guide.md` — Character profiles and voice
- `research/chapter_structure.md` — Chapter titles and summaries
- `research/poetry_guide.md` — Poetry translation approaches
- `research/commentary_guide.md` — Commentary types and sources

---

## Step 6: Save as JSON

Save your translation to `translations/page_XXXX.json` (4-digit page number, e.g., `page_0020.json`).

### JSON Schema

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Classical Chinese text from the page...",
      "zh_modern": "Modern Chinese translation...",
      "en": "English translation...",
      "ru": "Russian translation...",
      "ja": "Japanese translation...",
      "commentary": [
        {
          "source": "脂批",
          "original": "Commentary original text...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": [
    "Research finding 1...",
    "Research finding 2...",
    "Research finding 3..."
  ]
}
```

### Required Fields — Top Level

| Field | Type | Description |
|-------|------|-------------|
| `page` | integer | PDF page number (must match filename) |
| `chapter` | string | Chapter identifier: "前言", "凡例", "第一回", "第二回", etc. |
| `segments` | array | Array of segment objects (must not be empty) |
| `notes` | array of strings | Research notes (minimum 3 items) |

### Required Fields — Each Segment

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Sequential starting from 1 |
| `type` | string | One of: `"prose"`, `"poem"`, `"dialogue"` |
| `original` | string | Original Classical Chinese text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |
| `commentary` | array | Commentary objects (empty `[]` if none) |

### Required Fields — Each Commentary Object

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Source: "脂批", "甲戌本", "庚辰本", etc. |
| `original` | string | Original commentary text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |

### JSON Safety Rules

Chinese text often contains characters that break JSON if not handled properly:

- **Chinese quotation marks** `""` and `''`: Use Unicode escapes `\u201c` `\u201d` `\u2018` `\u2019` OR use the actual Unicode characters (both are valid in JSON, but be careful not to use ASCII `"` inside strings)
- **Newlines in poetry**: Use `\n` for line breaks within strings
- **Backslashes**: Escape as `\\`
- **Em dashes**: Use Unicode `\u2014` or the actual character `—`

**Test**: After saving, verify your file is valid JSON:
```bash
python3 -c "import json; json.load(open('translations/page_XXXX.json')); print('Valid')"
```

---

## Step 7: Validate

Run the validation tool before committing:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Fix any errors before proceeding.

---

## Step 8: Commit and Continue

After validating:

```bash
git add translations/page_XXXX.json
git commit -m "Translate page XXXX"
git push -u origin HEAD
```

Then immediately proceed to your next assigned page. Do not stop between pages.

---

## Complete Example

See `examples/page_0020.json` for a fully worked example with:
- 7 segments (prose, dialogue, poem)
- 12 commentary annotations translated in all 4 languages
- 8 research notes covering puns, allusions, and foreshadowing

This is the quality bar. Your translations should match this level of thoroughness.

---

## Key Terms Quick Reference

| Classical | English | Russian | Japanese |
|-----------|---------|---------|----------|
| 公子 | young master | молодой господин | 公子 |
| 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | maidservant | служанка | 女中 |
| 老爷 | master/lord | господин | 旦那様 |
| 太太 | madam/lady | госпожа | 奥様 |
| 脂砚斋 | Zhiyan Zhai | Чжияньчжай | 脂硯斎 |
| 大观园 | Grand View Garden | Сад Великого Вида | 大観園 |

Full glossary: `research/glossary.md`

---

## Character Name Puns

| Name | Hidden Meaning | Note in translations |
|------|---------------|---------------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 — True events hidden | Keep pinyin, explain in notes |
| 贾雨村 (Jia Yucun) | 假语存 — False words remain | Keep pinyin, explain in notes |
| 贾宝玉 (Jia Baoyu) | 假宝玉 — False precious jade | Keep pinyin, explain in notes |
| 英莲 (Yinglian) | 应怜 — Should be pitied | Keep pinyin, explain in notes |
| 元迎探惜 | 原应叹息 — Originally should sigh | Explain in notes at first appearance |

---

## Common Mistakes to Avoid

| Mistake | Consequence | Prevention |
|---------|------------|------------|
| Not reading the page image | Translating wrong content | Always start by viewing `source_pages/page_XXXX.png` |
| Missing `notes` field | No research documentation | Write at least 3 notes per page |
| Missing `commentary` key on segments | Invalid schema | Every segment needs `"commentary": []` even if empty |
| Unescaped quotes in JSON | Invalid JSON file | Use `\u201c` `\u201d` for Chinese quotes, or validate after saving |
| Translating only a few sentences | Incomplete page coverage | Translate ALL visible text on the page |
| All segments have 0 commentary | Missed commentary | Re-examine page image for red/blue text |
| Wrong page number | Misfiled translation | Verify filename matches `page` field matches actual PDF page |

---

## Self-Check Before Committing

Before you `git add` a translation file, verify all of the following:

- [ ] I read the actual page image before translating
- [ ] Segment 1's `original` matches the first main text on the page image
- [ ] ALL visible text on the page is covered (not just a few sentences)
- [ ] Every segment has all 5 text fields (`original`, `zh_modern`, `en`, `ru`, `ja`)
- [ ] Every segment has a `commentary` field (array, empty `[]` if none)
- [ ] IDs are sequential: 1, 2, 3...
- [ ] `notes` field exists with at least 3 research items
- [ ] `page` number matches the filename
- [ ] JSON is valid (test with `python3 -c "import json; json.load(open('...'));"`)
- [ ] Translation quality: reads as literature, not machine output

---

## Workflow Summary

```
For each assigned page:
  1. Read source_pages/page_XXXX.png
  2. Identify all text and commentary on the page
  3. Segment the content (4-8 segments typical)
  4. For each segment:
     a. Transcribe original Classical Chinese
     b. Translate to Modern Chinese
     c. Translate to English
     d. Translate to Russian
     e. Translate to Japanese
     f. Translate all attached commentary
  5. Research and write notes (minimum 3)
  6. Save to translations/page_XXXX.json
  7. Validate JSON
  8. Commit and push
  9. Proceed to next page immediately
```
