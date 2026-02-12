# JSON Output Schema

## Required Structure

Save each page as `translations/page_XXXX.json` (4-digit page number, zero-padded).

---

## Complete Schema

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Classical Chinese text...",
      "zh_modern": "Modern Chinese translation...",
      "en": "English translation...",
      "ru": "Russian translation...",
      "ja": "Japanese translation...",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "Commentary in Classical Chinese",
          "zh_modern": "Modern Chinese translation",
          "en": "English translation",
          "ru": "Russian translation",
          "ja": "Japanese translation"
        }
      ]
    }
  ],
  "notes": [
    "Research finding 1: puns, allusions, cultural context",
    "Research finding 2: literary techniques observed"
  ]
}
```

---

## Field Definitions

### Root Level

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `page` | number | **YES** | PDF page number | `20` |
| `chapter` | string | **YES** | Chapter identifier | `"第一回"` or `"前言"` |
| `segments` | array | **YES** | Array of text segments | See below |
| `notes` | array | **YES** | Your research findings | `["Finding 1", "Finding 2"]` |

### Segment Object

| Field | Type | Required | Description | Values |
|-------|------|----------|-------------|--------|
| `id` | number | **YES** | Sequential ID | `1`, `2`, `3`, ... |
| `type` | string | **YES** | Segment type | `"prose"`, `"poem"`, `"dialogue"` |
| `original` | string | **YES** | Original Classical Chinese | Full text |
| `zh_modern` | string | **YES** | Modern Chinese translation | Full translation |
| `en` | string | **YES** | English translation | Full translation |
| `ru` | string | **YES** | Russian translation | Full translation |
| `ja` | string | **YES** | Japanese translation | Full translation |
| `commentary` | array | **YES** | Commentary annotations | `[]` if none, see below if present |

### Commentary Object (if present)

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `source` | string | **YES** | Manuscript source | `"甲戌本"`, `"庚辰本"`, etc. |
| `original` | string | **YES** | Original Classical Chinese | Commentary text |
| `zh_modern` | string | **YES** | Modern Chinese translation | Translation |
| `en` | string | **YES** | English translation | Translation |
| `ru` | string | **YES** | Russian translation | Translation |
| `ja` | string | **YES** | Japanese translation | Translation |

---

## Validation Rules

1. **All fields listed as "Required" MUST be present**
2. **No extra fields** (don't add `pdf_page`, `page_content_type`, `characters_appearing`, etc.)
3. **Segment IDs** must be sequential: 1, 2, 3, ...
4. **Every segment** must have all 4 translations (`zh_modern`, `en`, `ru`, `ja`)
5. **Every segment** must have `commentary` field (use `[]` if no commentary)
6. **Empty strings are not allowed** - if there's no text, don't create that segment
7. **Notes array** cannot be empty - always include at least 1 research finding

---

## Common Mistakes to Avoid

❌ Missing `commentary` field → Always include, use `[]` if none  
❌ Empty translation strings → Every language must have actual content  
❌ Adding extra fields like `translator_notes`, `research_notes` → Use only `notes`  
❌ Non-sequential IDs → Must be 1, 2, 3, ...  
❌ Wrong page number → Verify before starting  
❌ Empty `notes` array → Always document at least one finding  

---

## Example: Minimal Valid Page

```json
{
  "page": 99,
  "chapter": "第五回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "宝玉因看见他外面罩着大红羽缎对襟褂子，便问袭人道："这是谁送他的？"",
      "zh_modern": "宝玉看见他外面穿着大红色羽缎对襟褂子，便问袭人："这是谁送给他的？"",
      "en": "Baoyu, seeing him wearing a bright red feather-satin jacket, asked Xiren: 'Who gave him that?'",
      "ru": "Баоюй, увидев, что на нём яркая красная куртка из перьевого атласа, спросил Сижэнь: «Кто ему это подарил?»",
      "ja": "宝玉、彼が外に大紅の羽緞の対襟褂子を着ているのを見て、襲人に問うて曰く：「これは誰が彼に贈ったのか」",
      "commentary": []
    }
  ],
  "notes": [
    "羽缎 (feather-satin) indicates high-quality fabric, showing Baoyu's privileged status"
  ]
}
```

---

## Example: Page with Commentary

```json
{
  "page": 21,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "这贾雨村原系胡州人氏，也是诗书仕宦之族。",
      "zh_modern": "这位贾雨村原本是胡州人，也是诗书仕宦之家。",
      "en": "This Jia Yucun was originally from Huzhou, also from a family of scholars and officials.",
      "ru": "Этот Цзя Юйцунь родом из Хучжоу, тоже из семьи учёных и чиновников.",
      "ja": "この賈雨村は元来胡州の人氏、また詩書仕宦の族なり。",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "妙在胡州。胡者，胡诌也。",
          "zh_modern": "妙在"胡州"这个名字。"胡"即胡诌（胡编乱造）。",
          "en": "The brilliance is in 'Huzhou.' 'Hu' means fabrication.",
          "ru": "Прелесть в «Хучжоу». «Ху» — значит «выдумка».",
          "ja": "妙なるは「胡州」にあり。胡とは、胡謅（でたらめ）なり。"
        }
      ]
    }
  ],
  "notes": [
    "贾雨村 (Jia Yucun) = 假语村 (false words remain), a metafictional hint",
    "胡州 (Huzhou) = 胡诌 (fabrication), commentary confirms pun on place name"
  ]
}
```

---

## File Naming

- Format: `page_XXXX.json`
- 4 digits, zero-padded
- Examples: `page_0001.json`, `page_0020.json`, `page_0234.json`

---

**See `examples/page_0020.json` for a real complete example.**
