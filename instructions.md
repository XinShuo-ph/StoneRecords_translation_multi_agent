## Goal

Translate pages from **红楼梦脂评汇校本** (Dream of the Red Chamber with Zhiping Commentary) into four languages:
- **Modern Chinese (简体中文)**: accurate, readable, lightly literary
- **English**: scholarly literary register
- **Russian (Русский)**: literary Russian
- **Japanese (日本語)**: classical-influenced literary Japanese

**One PDF page = one JSON file.** Translate **ALL visible text** on that page: **main text (正文) + all commentary (脂评/眉批/夹批/侧批/回末批等) + poetry + headers/labels when meaningful**.

This document is **translation-only**. Worker coordination/progress protocols (if any) are defined elsewhere and must not change the translation output contract below.

---

## Source Material

**PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`

**Page Images**: `source_pages/page_XXXX.png`

The source contains:
- **Main text (正文)**: The novel's narrative
- **Commentary (脂评)**: Annotations from various manuscript sources marked with 【甲戌】【庚辰】【己卯】etc.

---

## Workflow: For Each Page

### Step 0: Verify you are on the correct page (non-negotiable)

- Open `source_pages/page_XXXX.png` and confirm the **file name’s XXXX** matches the page you will output in JSON (`"page": XXXX`).
- Scan the full page (top/bottom + margins). If the page ends mid-sentence, **include the partial text** and note “continues next page” in `translator_notes`.

### Step 1: Inventory the page before translating (prevents missing/partial work)

Before translating, do a quick **content inventory**:
- Split the main text into **segments** (paragraph-sized chunks; poems as their own segments).
- For each segment, collect **all** commentary that belongs to it (including margin notes).
- If a commentary’s attachment is unclear, still include it and add `position` like `"top margin (applies to whole page)"`.

### Step 2: Research (light but mandatory)

Before translating, research each segment:
- Read relevant materials in `research/` directory
- (Optional) quick online lookup for idioms/allusions when needed
- Look up classical allusions (典故)
- Understand character name puns and hidden meanings
- Note historical and cultural context

Record findings as short bullets in `translator_notes` (and optionally `research_notes`).

### Step 3: Translate

For each segment on the page:
1. **Copy the original text exactly** (no summarizing; no skipping sentences).
2. Translate into **all 4 target languages**.
3. Translate **all commentary objects** in all 4 target languages.

Practical order that improves consistency: **original → zh_modern (accuracy anchor) → en/ru/ja**.

### Step 4: 润色 (Polish)

Review and refine each translation:
- Ensure literary quality matches the original's elegance
- Verify cultural nuances are preserved
- Check that poetry maintains its structure and rhythm
- Confirm consistency with glossary terms
- Read translations aloud mentally—do they flow naturally?

### Step 5: Save as JSON

Save to `translations/page_XXXX.json` (4-digit page number).

### Step 6: Validate before moving on (non-negotiable)

Run:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Fix all errors until it validates.

---

## JSON Output Format (strict contract)

### Required top-level fields

- `page` (int)
- `chapter` (string, e.g. `"第一回"`, `"前言"`, `"凡例"`)
- `segments` (array, non-empty)
- `translator_notes` (array of strings, non-empty)
- `total_segments` (int, must equal `segments.length`)

### Optional (recommended when applicable)

- `chapter_title` (object with `original/zh_modern/en/ru/ja`) when the page contains the chapter heading
- `page_content_type` (one of `front_matter`, `fanli`, `chapter_start`, `chapter_body`, `chapter_end`, `appendix`)
- `research_notes` (array of strings)

### Segment requirements

Each item in `segments[]` MUST include:
- `id` (1..N, sequential)
- `type` (`"prose" | "poem" | "dialogue"`)
- `original`, `zh_modern`, `en`, `ru`, `ja` (all non-empty strings)
- `commentary` (array; use `[]` if none)

### Commentary requirements

Each item in `commentary[]` MUST include:
- `type` (one of `眉批`, `夹批`, `侧批`, `回前批`, `回末批`, `回末总批`)
- `source` (the label seen on the page, e.g. `甲戌本`, `庚辰本`, `己卯本`, `蒙府本`, `脂批`, `校者`…)
- `original`, `zh_modern`, `en`, `ru`, `ja` (all non-empty strings)

Optional commentary fields: `position`, `commentator`.

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
          "type": "夹批",
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
  "translator_notes": ["Research findings: puns, allusions, cultural context"],
  "total_segments": 1
}
```

See `examples/page_0020.json` for a complete example (and validate with `tools/validate_json.py`).

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

When translating, keep transliterated names and note the pun in `translator_notes`.

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
1. Inventory → Translate → Polish → Validate → Save
2. Repeat for all assigned pages

If stuck on a passage for more than 5 minutes:
- Make a best-effort translation and add a note: `"Uncertain: [your question]"` in `translator_notes`
- Continue to next segment

---

## Anti-Patterns to Avoid

- Skipping content (instead, **inventory first** and translate everything you can see)
- Partial translation of a paragraph (instead, copy the full paragraph into `original` before translating)
- Wrong page number (instead, verify `source_pages/page_XXXX.png` and set `"page": XXXX`)
- Empty fields / missing keys (instead, follow the strict schema and validate)
- Invalid JSON (instead, validate before moving on)
- Getting stuck and stopping (instead, best-effort + `translator_notes` + continue)

---

## Quick Checklist Per Page

Before moving to the next page, verify:

- [ ] Page number is correct
- [ ] ALL visible text is translated (main + commentary + poems + margin notes)
- [ ] All 4 target languages are present for each segment
- [ ] All segments have `commentary: []` or a non-empty array of valid commentary objects
- [ ] Sequential IDs (1, 2, 3...)
- [ ] JSON is valid
- [ ] `translator_notes` includes research findings and any uncertainties
- [ ] `total_segments` equals the number of segments in this file
