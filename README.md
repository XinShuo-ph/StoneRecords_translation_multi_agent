# 红楼梦 Translation Project

**红楼梦脂评汇校本 → Modern Chinese, English, Russian, Japanese**

A scholarly multilingual translation of *Dream of the Red Chamber* (红楼梦), one of the Four Great Classical Novels of Chinese Literature, from the Zhiping Commentary Collation edition.

---

## Quick Start

1. Read `instructions.md` — the complete translation task specification
2. View source pages in `source_pages/` or open the PDF directly
3. Save translations to `translations/page_XXXX.json`
4. Validate with `python3 tools/validate_json.py translations/page_XXXX.json`

---

## Project Structure

```
workspace/
├── instructions.md                         # Translation task instructions (START HERE)
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf   # Source PDF
│
├── source_pages/                           # PDF pages as images
│   ├── page_0001.png
│   └── ...
│
├── research/                               # Reference materials
│   ├── glossary.md                         # Character names & terminology
│   ├── chapter_structure.md                # Chapter titles and summaries
│   ├── character_guide.md                  # Character profiles
│   ├── poetry_guide.md                     # Poetry translation approaches
│   ├── commentary_guide.md                 # Commentary types & sources
│   ├── cultural_context.md                 # Qing Dynasty context
│   └── existing_translations.md            # Reference existing translations
│
├── examples/                               # Format reference
│   └── page_0020.json                      # Complete validated example
│
├── tools/                                  # Utilities
│   ├── validate_json.py                    # Validate translation JSON
│   ├── pdf_to_images.py                    # Extract PDF pages as images
│   └── compile_chapters.py                 # Compile translations
│
├── translations/                           # Translation output
│   └── page_XXXX.json                      # One file per PDF page
│
├── output/                                 # Generated output
│
└── experiment_analysis.md                  # Analysis of previous parallel run
```

---

## Translation Output Format

Each page becomes one JSON file. Required fields:

```json
{
  "page": 20,
  "chapter": "第一回",
  "total_segments": 3,
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Classical Chinese...",
      "zh_modern": "现代中文...",
      "en": "English...",
      "ru": "Русский...",
      "ja": "日本語...",
      "commentary": [
        {
          "type": "侧批",
          "source": "甲戌本",
          "original": "...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": ["Research findings, allusions, puns, cultural context"]
}
```

See `examples/page_0020.json` for a complete validated example with 7 segments and 13 commentary annotations.

---

## About 红楼梦

*Dream of the Red Chamber* (红楼梦), also known as *The Story of the Stone* (石头记), was written by Cao Xueqin (曹雪芹) in the 18th century. It tells the story of the decline of a great aristocratic family through the eyes of Jia Baoyu and his relationships with his cousins Lin Daiyu and Xue Baochai.

The 脂评汇校本 version includes the Zhiping (脂砚斋) commentaries from various manuscript sources, providing valuable scholarly annotations alongside the text.
