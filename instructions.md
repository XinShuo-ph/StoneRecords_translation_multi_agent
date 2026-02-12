# Translation Instructions

Translate pages from 红楼梦脂评汇校本 (Dream of the Red Chamber, Zhiping Commentary Edition) into four languages. This document covers **only** the translation task itself — what to translate, the output format, and quality standards.

---

## Source Material

**PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
**Page images**: `source_pages/page_XXXX.png`

Each PDF page contains some combination of:
- **Main text (正文)**: The novel's narrative prose, dialogue, or poetry
- **Commentary (脂评)**: Scholarly annotations marked with manuscript source tags like 【甲戌】【庚辰】【己卯】【蒙府】

---

## Target Languages

| Language | JSON Key | Style |
|----------|----------|-------|
| Original Classical Chinese | `original` | Exact source text |
| Modern Chinese (简体中文) | `zh_modern` | Accessible contemporary Mandarin, preserving classical flavor |
| English | `en` | Scholarly literary translation |
| Russian (Русский) | `ru` | Literary Russian for classical literature |
| Japanese (日本語) | `ja` | Classical-influenced literary Japanese |

---

## Task: Translate One Page at a Time

For each assigned page, do the following in order:

### 1. Read the Page

Open the page image (`source_pages/page_XXXX.png`). Read every word on the page. Identify:
- All main text (prose, dialogue, poetry)
- All commentary (眉批 at top, 夹批 inline, 侧批 at sides)
- The manuscript source tags for each commentary

**Verification**: Confirm the page number matches what you expect. If the content does not match the assigned page number, stop and note the discrepancy.

### 2. Segment the Text

Break the page into segments. A **segment** is one of:
- A **prose paragraph**: A natural paragraph break in the narrative (typically 2-6 sentences that form a unit of action or description)
- A **poem/verse**: A complete poem, song, or set of couplets
- A **dialogue exchange**: A single character's speech (the "said X" framing + the quoted words)

**Segmentation rules**:
- Follow the natural structure of the text. If the text has clear paragraph breaks, use those.
- Do NOT split a single sentence across two segments.
- Do NOT merge unrelated paragraphs into one segment.
- Poetry is always its own segment, never merged with surrounding prose.
- Each commentary annotation attaches to the segment it comments on.

### 3. Research Key Terms

Before translating, check:
- `research/glossary.md` for character name translations and key terms
- `research/character_guide.md` for character relationships
- `research/poetry_guide.md` for poetry translation approaches (if the page has poems)
- `research/commentary_guide.md` for commentary source identification

For difficult passages, classical allusions, or puns, note your findings in the `notes` array.

### 4. Translate Every Segment

For each segment:
1. Copy the **exact original text** from the page into `original`
2. Write translations in all four target languages: `zh_modern`, `en`, `ru`, `ja`
3. For each commentary annotation on that segment, translate the commentary in all four languages too

**Do not skip any text on the page.** Every word of main text and every word of commentary must be translated.

### 5. Validate and Save

Save the result to `translations/page_XXXX.json` (4-digit zero-padded page number).

Before saving, check:
- [ ] `page` number matches the actual PDF page
- [ ] Every segment has all 5 text fields (`original`, `zh_modern`, `en`, `ru`, `ja`) — none empty
- [ ] Every segment has a `commentary` array (use `[]` if no commentary on that segment)
- [ ] Segment IDs are sequential: 1, 2, 3, ...
- [ ] `notes` array exists and contains at least one research note
- [ ] The JSON is valid (no trailing commas, proper escaping of quotes)

Run the validator:
```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

---

## JSON Output Format

```json
{
  "page": 20,
  "chapter": "第一回",
  "total_segments": 3,
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
          "type": "侧批",
          "source": "甲戌本",
          "original": "批语原文...",
          "zh_modern": "现代中文...",
          "en": "English...",
          "ru": "Русский...",
          "ja": "日本語..."
        }
      ]
    },
    {
      "id": 2,
      "type": "poem",
      "original": "诗句第一行\n诗句第二行\n诗句第三行\n诗句第四行",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "...",
      "commentary": []
    }
  ],
  "notes": [
    "英莲 (Yinglian) puns on 应怜 (should be pitied).",
    "三劫 = three kalpas. Buddhist usage: 30 years = one generation, so 三劫 ≈ 90 years."
  ]
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `page` | integer | Yes | PDF page number |
| `chapter` | string | Yes | Chapter label: "凡例", "第一回", "第二回", etc. |
| `total_segments` | integer | Yes | Number of segments (must equal `segments` array length) |
| `segments` | array | Yes | Array of segment objects |
| `notes` | array of strings | Yes | Research findings, allusions, puns, cultural context |

### Segment Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | Yes | Sequential: 1, 2, 3, ... |
| `type` | string | Yes | One of: `"prose"`, `"poem"`, `"dialogue"` |
| `original` | string | Yes | Exact original Classical Chinese text |
| `zh_modern` | string | Yes | Modern Chinese translation |
| `en` | string | Yes | English translation |
| `ru` | string | Yes | Russian translation |
| `ja` | string | Yes | Japanese translation |
| `commentary` | array | Yes | Commentary annotations (empty `[]` if none) |

### Commentary Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | One of: `"眉批"`, `"夹批"`, `"侧批"`, `"回前批"`, `"回末批"` |
| `source` | string | Yes | Manuscript source: `"甲戌本"`, `"庚辰本"`, `"己卯本"`, `"蒙府本"`, `"脂砚斋"`, etc. |
| `original` | string | Yes | Original commentary text |
| `zh_modern` | string | Yes | Modern Chinese translation |
| `en` | string | Yes | English translation |
| `ru` | string | Yes | Russian translation |
| `ja` | string | Yes | Japanese translation |

---

## Translation Quality Standards

### General Principles

红楼梦 is one of the greatest works of world literature. Every translation should:
- Preserve the **literary beauty** and emotional depth of the original
- Maintain **accuracy** — do not add, omit, or alter meaning
- Keep **cultural nuances** — names carry puns, objects carry symbolism
- Translate **all commentary** with the same care as main text

### By Language

**Modern Chinese (简体中文)**:
- 使用规范现代汉语，保留古典韵味
- 难懂的古词要解释清楚，但不要过度白话化
- 保留典故和文化含义

**English**:
- Scholarly literary register — neither archaic nor colloquial
- Use Pinyin for character names: Jia Baoyu, Lin Daiyu, Zhen Shiyin
- Translate titles and terms, with original Chinese in notes where helpful
- Poetry: prioritize meaning; note original meter/rhyme in `notes` if relevant

**Russian (Русский)**:
- Литературный русский для классической прозы
- Preserve aristocratic register and social distinctions
- Follow established Sinological transliteration for names

**Japanese (日本語)**:
- 文語的要素を含む格調高い文体
- Chinese names use 音読み
- Leverage shared Classical Chinese literary heritage

### Poetry Translation

Poems in 红楼梦 are structurally integral — they advance plot and reveal character. When translating poems:
- Preserve the **meaning** first, form second
- Maintain **line structure** (use `\n` for line breaks in JSON)
- Note the original rhyme scheme and meter in `notes` if relevant
- Translate ALL stanzas — never truncate a poem

### Character Names — Key Puns

| Name | Hidden Meaning | Note in translations |
|------|---------------|---------------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 (True events hidden) | Keep Pinyin; note pun |
| 贾雨村 (Jia Yucun) | 假语存 (False words remain) | Keep Pinyin; note pun |
| 贾宝玉 (Jia Baoyu) | 假宝玉 (False precious jade) | Keep Pinyin; note pun |
| 英莲 (Yinglian) | 应怜 (Should be pitied) | Keep Pinyin; note pun |
| 霍启 (Huo Qi) | 祸起 (Disaster arises) | Keep Pinyin; note pun |

See `research/glossary.md` for the complete list.

### Commentary Types

| Type | Position | Description |
|------|----------|-------------|
| 眉批 | Top margin | Extended critical commentary |
| 夹批 | Inline within text | Brief annotations inserted in the narrative |
| 侧批 | Side margin | Marginal notes |
| 回前批 | Before chapter | Prefatory comments |
| 回末批 | After chapter | End-of-chapter reflections |

The manuscript source (甲戌本, 庚辰本, etc.) indicates which historical copy the commentary comes from. Always identify and record the source when visible.

---

## Common Mistakes to Avoid

| Mistake | What to Do Instead |
|---------|-------------------|
| Translating the wrong page | Verify page number by checking visible content against the PDF page |
| Only translating a few sentences | Translate ALL text on the page — every paragraph, every line |
| Skipping commentary | Commentary is required. Translate every annotation |
| Missing `commentary` key on a segment | Always include it, even as empty `[]` |
| Empty or null translation fields | Every language field must have actual translated content |
| Non-sequential segment IDs | IDs must be 1, 2, 3, ... with no gaps |
| Missing `notes` array | Always include at least one research note per page |
| Invalid JSON | Validate with `python3 tools/validate_json.py` before saving |
| Stopping to ask questions | If stuck on a passage, add a note and continue: `"Uncertain: [question]"` |
| Inventing extra JSON fields | Use exactly the fields specified above — no more, no less |

---

## Reference Materials

| File | Contents |
|------|----------|
| `research/glossary.md` | Character names and key terms in all languages |
| `research/character_guide.md` | Character profiles and relationships |
| `research/chapter_structure.md` | Chapter titles and summaries |
| `research/poetry_guide.md` | Poetry translation approaches |
| `research/commentary_guide.md` | Commentary types, sources, conventions |
| `research/cultural_context.md` | Qing Dynasty historical context |
| `research/existing_translations.md` | Reference existing published translations |
| `examples/page_0020.json` | Complete example of a translated page |
