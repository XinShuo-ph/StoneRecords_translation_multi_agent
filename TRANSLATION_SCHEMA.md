# Translation JSON Schema

## Overview

Each PDF page becomes one JSON file following this schema.

The schema has **3 levels of complexity**:
1. **Minimal** (Tier 1) - Required fields only
2. **Standard** (Tier 2) - With commentary
3. **Complete** (Tier 3) - With all optional enhancements

---

## Level 1: Minimal (Required Fields Only)

This is the **minimum acceptable** translation.

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
    },
    {
      "id": 2,
      "type": "prose",
      "original": "作者自云：因曾历过一番梦幻之后，故将真事隐去。",
      "zh_modern": "作者自己说：因为曾经经历过一番梦幻般的往事之后，所以将真实的事情隐藏起来。",
      "en": "The author himself says: Having once passed through a dreamlike experience, he concealed the true events.",
      "ru": "Автор сам говорит: пережив некогда череду грёз, он скрыл истинные события.",
      "ja": "作者自ら言う：かつて夢幻のような経験を経た後、真実を隠したのだと。"
    }
  ]
}
```

### Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `page` | number | PDF page number | Must be positive integer |
| `chapter` | string | Chapter identifier | E.g., "第一回", "第二回", "前言" |
| `segments` | array | Text segments | Must have at least 1 segment |
| `segments[].id` | number | Sequential ID | Must be 1, 2, 3, ... (no gaps) |
| `segments[].type` | string | Segment type | Must be "prose", "poem", or "dialogue" |
| `segments[].original` | string | Original Chinese text | Must be non-empty |
| `segments[].zh_modern` | string | Modern Chinese | Must be non-empty |
| `segments[].en` | string | English | Must be non-empty |
| `segments[].ru` | string | Russian | Must be non-empty |
| `segments[].ja` | string | Japanese | Must be non-empty |

---

## Level 2: Standard (With Commentary)

This is the **recommended target** for quality translation.

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "此开卷第一回也。作者自云：因曾历过一番梦幻之后，故将真事隐去，而借通灵之说，撰此《石头记》一书也。",
      "zh_modern": "这是开篇的第一回。作者自己说：因为曾经经历过一番梦幻般的往事之后，所以将真实的事情隐藏起来，借用通灵宝玉的传说，撰写了这部《石头记》。",
      "en": "This is the first chapter of the opening. The author himself says: Having once passed through a dreamlike experience, he concealed the true events and, borrowing the tale of the Spiritual Jade, composed this book called 'The Story of the Stone.'",
      "ru": "Это первая глава книги. Автор сам говорит: пережив некогда череду грёз, он скрыл истинные события и, позаимствовав легенду о волшебной яшме, написал эту книгу под названием «Записки о камне».",
      "ja": "これが冒頭の第一回である。作者自ら言う：かつて夢幻のような経験を経た後、真実を隠し、通霊の説を借りて、この『石頭記』一書を著したのだと。",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "能解者方有辛酸之泪，哭成此书。",
          "zh_modern": "能够理解的人才会流下辛酸的眼泪，哭着写成这本书。",
          "en": "Only those who truly understand will shed bitter tears—this book was wept into being.",
          "ru": "Лишь тот, кто поистине понимает, прольёт горькие слёзы — эта книга была выплакана.",
          "ja": "能く解する者のみ辛酸の涙あり、泣きてこの書を成す。"
        }
      ]
    }
  ],
  "notes": [
    "真事隐 (true events hidden) puns on the character name 甄士隐 (Zhen Shiyin)",
    "《石头记》 (Story of the Stone) is the original title of 红楼梦"
  ]
}
```

### Additional Fields (Standard)

| Field | Type | Description |
|-------|------|-------------|
| `segments[].commentary` | array | Commentary annotations for this segment |
| `segments[].commentary[].source` | string | Manuscript source: "甲戌本", "庚辰本", etc. |
| `segments[].commentary[].original` | string | Original commentary text |
| `segments[].commentary[].zh_modern` | string | Modern Chinese translation |
| `segments[].commentary[].en` | string | English translation |
| `segments[].commentary[].ru` | string | Russian translation |
| `segments[].commentary[].ja` | string | Japanese translation |
| `notes` | array | Translator notes: puns, allusions, research findings |

---

## Level 3: Complete (All Enhancements)

This is **excellent quality** with all optional fields.

```json
{
  "page": 25,
  "chapter": "第一回",
  "chapter_title": {
    "original": "甄士隐梦幻识通灵 贾雨村风尘怀闺秀",
    "zh_modern": "甄士隐在梦幻中认识了通灵宝玉，贾雨村在落魄时怀念闺中秀女",
    "en": "Zhen Shiyin in a Dream Perceives the Jade of Spiritual Understanding; Jia Yucun in Humble Circumstances Thinks Fondly of a Beautiful Maiden",
    "ru": "Чжэнь Шиинь во сне постигает волшебную яшму; Цзя Юйцунь в бедности вспоминает прекрасную деву",
    "ja": "甄士隠、夢幻の中で通霊を識り、賈雨村、風塵にありて閨秀を懐う"
  },
  "page_content_type": "chapter_body",
  "segments": [
    {
      "id": 1,
      "pdf_page": 25,
      "type": "prose",
      "original": "一日，拄了拐杖，挣挫到街前散散心。",
      "zh_modern": "这一天，他拄着拐杖，挣扎着走到街前散散心。",
      "en": "One day, leaning on a cane, he struggled out to the street to distract his mind.",
      "ru": "Однажды, опираясь на посох, он с трудом вышел на улицу, чтобы развеять тоску.",
      "ja": "ある日、杖をつき、やっとの思いで街へ出て気晴らしをした。",
      "commentary": []
    },
    {
      "id": 2,
      "pdf_page": 25,
      "type": "poem",
      "original": "世人都晓神仙好，只有功名忘不了！\n古今将相在何方？荒冢一堆草没了！",
      "zh_modern": "世人都知道做神仙好，只有功名利禄忘不了！\n古往今来的将相都在哪里？只剩下一堆荒坟被野草淹没了！",
      "en": "All men know that salvation is good,\nBut glory and fame they simply cannot forget!\nWhere are the generals and ministers of old?\nIn a heap of grassy graves, they are gone!",
      "ru": "Все люди знают: быть бессмертным — благо,\nНо славу и почесть забыть не могут!\nГде ныне полководцы и министры прошлых лет?\nЛишь холм могильный, травой поросший!",
      "ja": "世人皆知る神仙の好きを、ただ功名のみ忘れ得ず！\n古今の将相何処にか在る？荒冢一堆草没し了んぬ！",
      "poem_notes": {
        "title": "好了歌 (Won-Done Song)",
        "form": "Doggerel / Folk Song style",
        "theme": "Vanity of worldly pursuits",
        "rhyme_scheme": "AABB"
      },
      "commentary": [
        {
          "type": "眉批",
          "source": "甲戌本",
          "position": "top margin",
          "original": "昌黎云："人生只有上寿难。"非世人不知神仙好也。",
          "zh_modern": "韩昌黎说："人生只有长寿最难。"并不是世人不知道做神仙好啊。",
          "en": "Han Changli said: 'In life, only longevity is difficult.' It is not that people do not know salvation is good.",
          "ru": "Хань Чанли говорил: «В жизни труднее всего достичь долголетия». Не то чтобы люди не знали, что быть бессмертным — благо.",
          "ja": "昌黎云く：「人生ただ上寿のみ難し」と。世人神仙の好きを知らざるに非ざるなり。"
        }
      ]
    }
  ],
  "translator_notes": [
    "The 'Won-Done Song' (好了歌) is thematic core of the novel, expressing the Buddhist/Taoist view that worldly attachments are futile.",
    "'Hao' (好) translated as 'won/good/salvation' and 'Liao' (了) as 'done/finished' to capture the pun."
  ],
  "research_notes": [
    "Consulted Hawkes, Yang, and Minford translations for rhythm strategies",
    "Han Changli (韩昌黎) refers to Tang poet Han Yu"
  ],
  "characters_appearing": [
    "甄士隐",
    "跛足道人"
  ],
  "manuscript_sources_on_page": [
    "甲戌本"
  ],
  "total_segments": 2
}
```

### All Optional Fields (Complete)

| Field | Type | Description |
|-------|------|-------------|
| `chapter_title` | object | Chapter title in all languages (only if chapter starts on this page) |
| `page_content_type` | string | "front_matter", "chapter_start", "chapter_body", "chapter_end", "appendix" |
| `segments[].pdf_page` | number | PDF page number (usually same as root `page`) |
| `segments[].poem_notes` | object | For poetry: title, form, theme, rhyme_scheme, etc. |
| `segments[].commentary[].type` | string | "眉批", "夹批", "侧批", "回末批" |
| `segments[].commentary[].position` | string | Physical position: "top margin", "inline after X", etc. |
| `translator_notes` | array | Alternative name for `notes` |
| `research_notes` | array | Sources consulted during research |
| `characters_appearing` | array | List of character names appearing on this page |
| `manuscript_sources_on_page` | array | List of manuscript sources cited on this page |
| `total_segments` | number | Total number of segments (should equal `segments.length`) |

---

## Type Definitions

### Segment Types

| Type | Description | When to Use |
|------|-------------|-------------|
| `prose` | Narrative prose | Standard narrative text |
| `poem` | Poetry or verse | Any poetic content |
| `dialogue` | Direct speech | Extended dialogue passages |
| `title` | Titles/headings | Chapter titles, section headings |
| `preface` | Preface/introduction | Prefatory material |

### Page Content Types

| Type | Description |
|------|-------------|
| `front_matter` | Front matter before Chapter 1 |
| `fanli` | Editorial notes (凡例) |
| `chapter_start` | First page of a chapter |
| `chapter_body` | Middle of a chapter |
| `chapter_end` | Last page of a chapter |
| `appendix` | Appendix materials |

### Commentary Types

| Type | Chinese | Position |
|------|---------|----------|
| `眉批` | Top marginal | Above main text |
| `夹批` | Interlinear | Inline within text |
| `侧批` | Side marginal | Side of page |
| `回前批` | Chapter preface | Before chapter |
| `回末批` | Chapter end | After chapter |

---

## Validation Rules

### Required Field Validation

1. **page**: Must be a positive integer
2. **chapter**: Must be a non-empty string
3. **segments**: Must be a non-empty array
4. **segments[].id**: Must be sequential starting from 1 (1, 2, 3, ...)
5. **segments[].type**: Must be one of: "prose", "poem", "dialogue", "title", "preface"
6. **segments[].original**: Must be non-empty string
7. **segments[].zh_modern**: Must be non-empty string
8. **segments[].en**: Must be non-empty string
9. **segments[].ru**: Must be non-empty string
10. **segments[].ja**: Must be non-empty string

### Optional Field Validation

11. **segments[].commentary**: If present, must be an array (can be empty `[]`)
12. **segments[].commentary[].source**: If commentary present, must be non-empty
13. **segments[].commentary[].original**: If commentary present, must be non-empty
14. **notes** or **translator_notes**: If present, should be non-empty array
15. **chapter_title**: If present, must have all language fields

### Consistency Validation

16. **File name**: Must match `page_XXXX.json` where XXXX = page number (4 digits, zero-padded)
17. **Segment IDs**: Must be consecutive without gaps
18. **total_segments**: If present, must equal `segments.length`
19. **UTF-8 encoding**: File must be valid UTF-8
20. **Valid JSON**: Must parse without syntax errors

---

## Progressive Adoption

### Your First Page
Use **Level 1 (Minimal)** to get started and build confidence.

### After 3-5 Pages
Upgrade to **Level 2 (Standard)** - add commentary and notes.

### For Complex Pages
Use **Level 3 (Complete)** when you have:
- Poetry that needs analysis
- Rich commentary
- Substantial research findings
- Chapter start pages

---

## Common Mistakes

### ❌ Empty Translations
```json
{
  "original": "此开卷第一回也。",
  "zh_modern": "",  // ❌ Empty!
  "en": null,       // ❌ Null!
  "ru": "...",
  "ja": "..."
}
```

### ✅ All Fields Populated
```json
{
  "original": "此开卷第一回也。",
  "zh_modern": "这是开篇的第一回。",
  "en": "This is the first chapter.",
  "ru": "Это первая глава.",
  "ja": "これが第一回である。"
}
```

### ❌ Non-Sequential IDs
```json
{
  "segments": [
    {"id": 1, ...},
    {"id": 3, ...},  // ❌ Skipped 2!
    {"id": 4, ...}
  ]
}
```

### ✅ Sequential IDs
```json
{
  "segments": [
    {"id": 1, ...},
    {"id": 2, ...},
    {"id": 3, ...}
  ]
}
```

### ❌ Missing Commentary Translations
```json
{
  "commentary": [
    {
      "source": "甲戌本",
      "original": "能解者方有辛酸之泪。",
      "zh_modern": "能够理解的人才会流下辛酸的眼泪。"
      // ❌ Missing en, ru, ja!
    }
  ]
}
```

### ✅ Complete Commentary
```json
{
  "commentary": [
    {
      "source": "甲戌本",
      "original": "能解者方有辛酸之泪。",
      "zh_modern": "能够理解的人才会流下辛酸的眼泪。",
      "en": "Only those who understand will shed bitter tears.",
      "ru": "Лишь понимающий прольёт горькие слёзы.",
      "ja": "能く解する者のみ辛酸の涙あり。"
    }
  ]
}
```

---

## Schema Evolution

This schema may evolve. Current version: **v2.0**

Changes from v1.0:
- Simplified required fields
- Made many fields optional
- Introduced 3-tier system
- Clarified commentary structure
- Added validation rules

For questions or suggested improvements, document them in your work log.
