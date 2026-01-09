# 红楼梦 Translation Instructions

## Your Task

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

**Target time: 15-20 minutes per page**

### Step 1: View the Page (1-2 min)

Open the page image or PDF:
```bash
# View page image (if extracted)
ls source_pages/page_0020.png

# Or open PDF to the specific page
```

Identify all content:
- Main narrative text
- Any commentary (眉批, 夹批, 侧批)
- Any poetry

### Step 2: Translate All Content (10-15 min)

For each text segment on the page:

1. Copy the original Classical Chinese
2. Translate to Modern Chinese
3. Translate to English
4. Translate to Russian
5. Translate to Japanese

**Translate commentary too** - it's part of the scholarly apparatus.

### Step 3: Save as JSON (2 min)

Save to `translations/page_XXXX.json` (4-digit page number).

### Step 4: Move to Next Page

**Do NOT pause between pages.** Continue to the next page immediately.

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
      "original": "那僧笑道："此事说来好笑，竟是千古未闻的罕事。",
      "zh_modern": "那僧人笑道："这件事说来好笑，竟然是千古以来从未听说过的稀罕事。",
      "en": "The monk laughed and said, \"This matter is amusing to speak of—truly a rare occurrence, unheard of through the ages.\"",
      "ru": "Монах усмехнулся: «Эта история забавна — поистине редкость, неслыханная с древних времён».",
      "ja": "僧は笑って言った。「この事は話せば笑い話だが、実に千古未聞の稀な事じゃ。」"
    },
    {
      "id": 2,
      "type": "prose",
      "original": "只因西方灵河岸上三生石畔，有绛珠草一株...",
      "zh_modern": "只因为在西方灵河岸边的三生石旁...",
      "en": "It began on the banks of the Spirit River in the West, beside the Three Lives Stone...",
      "ru": "На берегу Духовной Реки на Западе, у Камня Трёх Жизней...",
      "ja": "西方霊河の岸、三生石のほとりに...",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "妙！所谓"三生石上旧精魂"也。",
          "zh_modern": "妙！这就是所谓的"三生石上旧精魂"。",
          "en": "Wonderful! This refers to 'the old spirit on the Three Lives Stone.'",
          "ru": "Чудесно! Это о «старой душе на Камне Трёх Жизней».",
          "ja": "妙なり！いわゆる「三生石上の旧精魂」なり。"
        }
      ]
    }
  ],
  "notes": [
    "三生石 (Three Lives Stone): Buddhist concept of karmic bonds across past, present, future",
    "绛珠草 symbolizes Lin Daiyu; 神瑛侍者 symbolizes Jia Baoyu"
  ]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | int | PDF page number |
| `chapter` | string | "前言", "第一回", "第二回", etc. |
| `segments` | array | Array of translated segments |
| `segments[].id` | int | Sequential ID (1, 2, 3...) |
| `segments[].type` | string | "prose", "poem", "dialogue" |
| `segments[].original` | string | Original Classical Chinese |
| `segments[].zh_modern` | string | Modern Chinese translation |
| `segments[].en` | string | English translation |
| `segments[].ru` | string | Russian translation |
| `segments[].ja` | string | Japanese translation |
| `notes` | array | Important observations (names, allusions, puns) |

### Optional: Commentary

If a segment has commentary, add:
```json
"commentary": [
  {
    "source": "甲戌本",
    "original": "批语原文",
    "zh_modern": "现代文",
    "en": "English",
    "ru": "Русский",
    "ja": "日本語"
  }
]
```

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

## Character Name Puns (Important!)

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

**Do NOT stop between pages to ask for confirmation.**

Work continuously:
1. Complete page → Save JSON → Next page → Repeat
2. Continue until you've completed all assigned pages

If stuck on a passage for more than 5 minutes:
- Add a note: `"Uncertain: [your question]"`
- Continue to next segment

---

## Anti-Patterns to Avoid

❌ **Skipping content** - Translate EVERYTHING on the page  
❌ **Empty translations** - Every field must have content  
❌ **Wrong page number** - Verify you're on the correct page  
❌ **Stopping to ask questions** - Keep working, add notes  
❌ **Invalid JSON** - Validate before saving  
❌ **Only translating main text** - Commentary is required too

---

## Quick Checklist Per Page

Before moving to the next page, verify:

- [ ] Page number is correct
- [ ] ALL visible text is translated (main + commentary)
- [ ] All 4 target languages are present for each segment
- [ ] Sequential IDs (1, 2, 3...)
- [ ] JSON is valid
- [ ] Notes include any important observations

---

## Example: Complete Page Translation

See `examples/page_example.json` for a complete reference.

---

*Focus on translation quality. Every page of 红楼梦 is a masterpiece deserving careful attention.*
