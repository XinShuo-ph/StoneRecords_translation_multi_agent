# 红楼梦 Translation Project

**红楼梦脂评汇校本 → Modern Chinese, English, Russian, Japanese**

A translation project for *Dream of the Red Chamber* (红楼梦), one of the Four Great Classical Novels of Chinese Literature.

---

## Overview

This project translates 脂评汇校本 version of 红楼梦 from Classical Chinese into:

- **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
- **English** - Scholarly literary translation
- **Russian (Русский)** - Literary Russian
- **Japanese (日本語)** - Classical-influenced literary Japanese

---

## Quick Start

1. Read `instructions.md` for the translation task
2. View source pages in `source_pages/` or open the PDF directly
3. Save translations to `translations/page_XXXX.json`

---

## Project Structure

```
workspace/
├── instructions.md              # Translation instructions
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf  # Source PDF
│
├── source_pages/                # Extracted PDF pages as images
│   ├── page_0001.png
│   └── ...
│
├── research/                    # Reference materials
│   ├── glossary.md              # Character names & terminology
│   ├── chapter_structure.md     # Chapter titles and summaries
│   ├── character_guide.md       # Main character profiles
│   ├── poetry_guide.md          # Poetry translation approaches
│   ├── commentary_guide.md      # Commentary types & sources
│   └── ...
│
├── examples/                    # Format examples
│   └── page_0020.json           # Complete page translation example
│
├── tools/                       # Utilities
│   ├── pdf_to_images.py         # Extract PDF pages as images
│   ├── validate_json.py         # Validate translation JSON
│   └── compile_chapters.py      # Compile translations to PDF
│
├── translations/                # Output directory
│   └── page_XXXX.json           # Translation files go here
│
└── output/                      # Generated PDFs
```

---

## Translation Output Format

Each page becomes a JSON file:

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Classical Chinese text...",
      "zh_modern": "Modern Chinese...",
      "en": "English...",
      "ru": "Russian...",
      "ja": "Japanese...",
      "commentary": [...]
    }
  ],
  "notes": ["Translator observations"]
}
```

See `examples/page_0020.json` for a complete example.

---

## Extracting PDF Pages

To extract pages as images for viewing:

```bash
# Extract all pages
python3 tools/pdf_to_images.py 红楼梦脂评汇校本_有书签目录_v3.13.pdf source_pages/

# Extract specific range
python3 tools/pdf_to_images.py 红楼梦脂评汇校本_有书签目录_v3.13.pdf source_pages/ 20 40
```

---

## About 红楼梦

*Dream of the Red Chamber* (红楼梦), also known as *The Story of the Stone* (石头记), was written by Cao Xueqin (曹雪芹) in the 18th century. It tells the story of the decline of a great aristocratic family through the eyes of Jia Baoyu and his relationships with his cousins Lin Daiyu and Xue Baochai.

The 脂评汇校本 version includes the Zhiping (脂砚斋) commentaries from various manuscript sources, providing valuable scholarly annotations.

---

**让我们一起把这部伟大的文学作品呈现给世界！**

*Let's bring this masterpiece to the world!*
