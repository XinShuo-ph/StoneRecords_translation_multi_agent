## Goal

Translate pages from 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary) into four languages:
- **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
- **English** - Scholarly literary translation
- **Russian (Русский)** - Literary Russian translation
- **Japanese (日本語)** - Classical-influenced literary Japanese

Each PDF page becomes one JSON file. Translate ALL content on each page: main text AND commentary.

---

## Source Material

**PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`

**Page Images**: `source_pages/page_XXXX.png`

The source contains:
- **Main text (正文)**: The novel's narrative
- **Commentary (脂评)**: Annotations from various manuscript sources marked with 【甲戌】【庚辰】【己卯】etc.

---

## Workflow: For Each Page

### Step 1: View the Page

Read both:
- The page image (`source_pages/page_XXXX.png`) for visual layout
- The PDF for text selection and formatting context

Identify all content:
- Main narrative text
- Any commentary (眉批, 夹批, 侧批)
- Any poetry

### Step 2: Research

Before translating, research each segment:
- Read relevant materials in `research/` directory
- Search online for scholarly interpretations
- Look up classical allusions (典故)
- Understand character name puns and hidden meanings
- Note historical and cultural context

Document findings in the `notes` field.

### Step 3: Translate

For each text segment on the page:
1. Copy the original Classical Chinese
2. Translate to Modern Chinese
3. Translate to English
4. Translate to Russian
5. Translate to Japanese

Translate all commentary as well.

### Step 4: 润色 (Polish)

Review and refine each translation:
- Ensure literary quality matches the original's elegance
- Verify cultural nuances are preserved
- Check that poetry maintains its structure and rhythm
- Confirm consistency with glossary terms
- Read translations aloud mentally—do they flow naturally?

### Step 5: Save as JSON

Save to `translations/page_XXXX.json` (4-digit page number).

### Step 6: Next Page

Continue to the next page immediately. Do not pause between pages.

---

## JSON Output Format

```json
{
  "page": 20,
  "chapter": "第一回",
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
          "source": "脂批",
          "original": "批语原文",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": ["Research findings: puns, allusions, cultural context"]
}
```

See `examples/page_0020.json` for a complete example with 7 segments and 12 commentary annotations.

### Required Fields

| Field | Description |
|-------|-------------|
| `page` | PDF page number |
| `chapter` | "前言", "第一回", "第二回", etc. |
| `segments[].id` | Sequential ID (1, 2, 3...) |
| `segments[].type` | "prose", "poem", "dialogue" |
| `segments[].original` | Original Classical Chinese |
| `segments[].zh_modern` | Modern Chinese translation |
| `segments[].en` | English translation |
| `segments[].ru` | Russian translation |
| `segments[].ja` | Japanese translation |
| `segments[].commentary` | Array of commentary (empty `[]` if none) |
| `notes` | Research findings |

---

## Translation Quality Guidelines

### Voice and Style

红楼梦 is one of the greatest works of world literature. Preserve:
- **Elegant classical beauty** - Don't over-modernize
- **Psychological depth** - Subtle emotional nuances
- **Symbolic richness** - Names and objects carry meaning
- **Poetry structure** - Maintain verse forms

### By Language

**Modern Chinese (简体中文)**:
- 使用规范现代汉语，保留古典韵味
- 保留原有的典故和意涵

**English**:
- Scholarly literary register
- Pinyin for names (Jia Baoyu, Lin Daiyu)
- Cultural notes where needed

**Russian (Русский)**:
- Literary Russian for classical literature
- Preserve aristocratic register

**Japanese (日本語)**:
- Classical-influenced literary style
- Use 音読み for Chinese names

---

## Key Terms Reference

| Classical | Modern Chinese | English | Russian | Japanese |
|-----------|----------------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子 |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | 丫鬟/婢女 | maidservant | служанка | 女中 |
| 老爷 | 老爷/大人 | master/lord | господин | 旦那様 |
| 太太 | 太太/夫人 | madam/lady | госпожа | 奥様 |

See `research/glossary.md` for complete terminology.

---

## Character Name Puns

Many names contain hidden meanings:

| Name | Hidden Meaning |
|------|----------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 - True events hidden |
| 贾雨村 (Jia Yucun) | 假语存 - False words remain |
| 贾宝玉 (Jia Baoyu) | 假宝玉 - False precious jade |

When translating, keep transliterated names and note the pun in `notes`.

---

## Commentary Types

| Type | Position | Description |
|------|----------|-------------|
| 眉批 | Top of page | Extended commentary |
| 夹批 | Inline | Brief notes within text |
| 侧批 | Side margin | Side comments |
| 回末批 | Chapter end | End-of-chapter comments |

---

## Continuous Execution

Work continuously:
1. Complete page → Save JSON → Next page → Repeat
2. Continue until you've completed all assigned pages

If stuck on a passage for more than 5 minutes:
- Add a note: `"Uncertain: [your question]"`
- Continue to next segment

---

## Anti-Patterns to Avoid

- Skipping content (instead, translate EVERYTHING on the page)
- Empty translations (instead, ensure every field has content)
- Wrong page number (instead, verify page number before starting)
- Stopping to ask questions (instead, add a note and continue)
- Invalid JSON (instead, validate before saving)
- Skipping research (instead, always research before translating)

---

## Quick Checklist Per Page

Before moving to the next page, verify:

- [ ] Page number is correct
- [ ] ALL visible text is translated (main + commentary)
- [ ] All 4 target languages are present for each segment
- [ ] All segments have `commentary` field (empty `[]` if none)
- [ ] Sequential IDs (1, 2, 3...)
- [ ] JSON is valid
- [ ] Notes include research findings
