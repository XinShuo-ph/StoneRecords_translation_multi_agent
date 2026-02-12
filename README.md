# 红楼梦 Translation Project

**红楼梦脂评汇校本 → Modern Chinese, English, Russian, Japanese**

A collaborative multi-agent translation project for *Dream of the Red Chamber* (红楼梦), one of the Four Great Classical Novels of Chinese Literature.

---

## Overview

This project translates 脂评汇校本 version of 红楼梦 from Classical Chinese into:

- **Modern Chinese (简体中文)** — Accessible contemporary Mandarin
- **English** — Scholarly literary translation
- **Russian (Русский)** — Literary Russian
- **Japanese (日本語)** — Classical-influenced literary Japanese

Multiple AI agents work in parallel, coordinated by an automated sync daemon that prevents duplicate work and manages page assignment.

---

## Quick Start

### For Translation Workers

1. **Start the sync daemon** (mandatory — prevents duplication):
   ```bash
   python3 tools/sync_daemon.py --start &
   sleep 30
   ```
2. **Get your page assignment**:
   ```bash
   python3 tools/sync_daemon.py --next-page
   ```
3. **Read `instructions.md`** for the translation workflow
4. **Save translations** to `translations/page_XXXX.json`

### For Project Coordinators

- Read `PROTOCOL.md` for the collaboration architecture
- Read `INVESTIGATION_REPORT.md` for analysis of previous approaches
- Use `python3 tools/sync_daemon.py --status` to view global progress

---

## Project Structure

```
workspace/
├── instructions.md              # Translation task (concise, quality-focused)
├── PROTOCOL.md                  # Parallel collaboration protocol
├── INVESTIGATION_REPORT.md      # Analysis of 16 previous protocol branches
├── WORKER_STATE_TEMPLATE.md     # Template for new worker state files
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
│   ├── cultural_context.md      # Qing Dynasty context
│   └── existing_translations.md # Reference existing translations
│
├── examples/                    # Format examples
│   └── page_0020.json           # Complete page translation example
│
├── tools/                       # Utilities
│   ├── sync_daemon.py           # Mandatory sync daemon for coordination
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

## Collaboration Protocol

This project uses multiple AI agents translating different pages in parallel. The protocol evolved through several iterations:

1. **V1**: Manual sync with heartbeats and page claiming (too complex, not followed)
2. **V2**: Added automated sync daemon (addressed the problem but added complexity)
3. **V3**: Stripped all protocol for simplicity (high quality but 83% duplication)
4. **Best Version** (current): Concise quality instructions + automated daemon coordination

See `INVESTIGATION_REPORT.md` for the full analysis and `PROTOCOL.md` for the finalized protocol.

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
      "commentary": [
        {
          "type": "夹批",
          "source": "甲戌本",
          "original": "Commentary text...",
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

See `examples/page_0020.json` for a complete example.

---

## About 红楼梦

*Dream of the Red Chamber* (红楼梦), also known as *The Story of the Stone* (石头记), was written by Cao Xueqin (曹雪芹) in the 18th century. It tells the story of the decline of a great aristocratic family through the eyes of Jia Baoyu and his relationships with his cousins Lin Daiyu and Xue Baochai.

The 脂评汇校本 version includes the Zhiping (脂砚斋) commentaries from various manuscript sources, providing valuable scholarly annotations.

---

**让我们一起把这部伟大的文学作品呈现给世界！**

*Let's bring this masterpiece to the world!*
