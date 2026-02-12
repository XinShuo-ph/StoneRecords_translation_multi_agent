# 红楼梦 Translation Project

**红楼梦脂评汇校本 → Modern Chinese, English, Russian, Japanese**

A scholarly translation project for *Dream of the Red Chamber* (红楼梦), one of the Four Great Classical Novels of Chinese Literature, translating from the 脂评汇校本 critical edition with Zhiping commentary.

---

## Quick Start

1. Read `instructions.md` — the complete translation task specification
2. View source pages in `source_pages/page_XXXX.png` or open the PDF directly
3. Consult reference materials in `research/`
4. Save translations to `translations/page_XXXX.json`
5. Validate with `python3 tools/validate_json.py translations/page_XXXX.json`

---

## Project Structure

```
workspace/
├── instructions.md                          # Translation instructions (START HERE)
├── INVESTIGATION.md                         # Analysis of prior experiment results
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf    # Source PDF
│
├── source_pages/                            # Pre-extracted PDF pages as PNG images
│   ├── page_0001.png
│   ├── page_0002.png
│   └── ... (page number = PDF page number)
│
├── research/                                # Reference materials
│   ├── glossary.md                          # Character names & term translations
│   ├── chapter_structure.md                 # Chapter titles, summaries, page ranges
│   ├── character_guide.md                   # Character profiles and speech patterns
│   ├── poetry_guide.md                      # Poetry translation approaches
│   ├── commentary_guide.md                  # Commentary types & manuscript sources
│   ├── cultural_context.md                  # Historical and cultural notes
│   └── existing_translations.md             # Survey of prior translations
│
├── examples/                                # Format examples
│   └── page_0020.json                       # Complete page translation example
│
├── tools/                                   # Utilities
│   ├── pdf_to_images.py                     # Extract PDF pages as PNG images
│   ├── validate_json.py                     # Validate translation JSON format
│   └── compile_chapters.py                  # Compile translations into documents
│
├── translations/                            # Output directory for translations
│   └── page_XXXX.json                       # One file per PDF page
│
└── output/                                  # Generated compiled documents
```

---

## Translation Output Format

Each PDF page produces one JSON file with this exact structure:

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
      "commentary": [
        {
          "source": "甲戌",
          "original": "Commentary text...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "notes": ["Research findings, allusions, cultural context"]
}
```

See `examples/page_0020.json` for a complete working example with 7 segments and 12 commentary annotations.

---

## Page Numbering

**Important**: The page numbers used in this project are **PDF page numbers** (the physical position of the page in the PDF file), NOT the numbers printed at the bottom of each page. For example, `page_0020.png` is the 20th page of the PDF, even though the printed number on that page is "11".

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

## Validating Translations

```bash
# Validate a single file
python3 tools/validate_json.py translations/page_0020.json

# Validate all translations
python3 tools/validate_json.py translations/

# Validate the example
python3 tools/validate_json.py examples/
```

---

## About 红楼梦

*Dream of the Red Chamber* (红楼梦), also known as *The Story of the Stone* (石头记), was written by Cao Xueqin (曹雪芹) in the 18th century. It tells the story of the decline of a great aristocratic family through the eyes of Jia Baoyu and his relationships with his cousins Lin Daiyu and Xue Baochai.

The 脂评汇校本 version includes the Zhiping (脂砚斋) commentaries from various manuscript sources, providing invaluable scholarly annotations that illuminate the author's intent and the text's rich layers of meaning.

---

**让我们一起把这部伟大的文学作品呈现给世界！**

*Let's bring this masterpiece to the world!*
