# Translation Tools

This directory contains tools for processing and compiling translations.

## Tools Overview

| Tool | Purpose |
|------|---------|
| `extract_text.py` | Extract text from source PDF |
| `compile_chapters.py` | Compile JSON translations to PDF |
| `validate_json.py` | Validate translation JSON files |

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

For PDF generation:
- XeLaTeX (texlive-xetex)
- xeCJK package (texlive-lang-chinese, texlive-lang-japanese)
- Noto fonts (noto-fonts, noto-fonts-cjk)

On Ubuntu/Debian:
```bash
sudo apt-get install texlive-xetex texlive-lang-chinese texlive-lang-japanese
sudo apt-get install fonts-noto fonts-noto-cjk
```

---

## extract_text.py

Extract chapter text from the source PDF.

### Usage
```bash
python3 tools/extract_text.py 红楼梦脂评汇校本_有书签目录_v3.13.pdf extracted/
```

### Output
```
extracted/
├── full.txt              # Complete text
└── chapters/
    ├── chapter_001.txt   # 第一回
    ├── chapter_002.txt   # 第二回
    └── ...
```

### Notes
- Requires manual verification of chapter boundaries
- Commentary markers should be preserved
- Text may need manual cleanup

---

## compile_chapters.py

Generate PDFs from translated JSON files.

### Usage
```bash
# Single chapter
python3 tools/compile_chapters.py translations/chapter_001.json output/

# All chapters
python3 tools/compile_chapters.py translations/ output/
```

### Output Format
Each PDF page shows:
1. Original Classical Chinese (black)
2. Modern Chinese translation (dark gray)
3. English translation (dark blue)
4. Russian translation (dark red)
5. Japanese translation (dark green)

### Color Scheme
| Language | Color | Hex |
|----------|-------|-----|
| Classical Chinese | Black | #000000 |
| Modern Chinese | Dark Gray | #333333 |
| English | Dark Blue | #00008B |
| Russian | Dark Red | #8B0000 |
| Japanese | Dark Green | #006400 |

---

## validate_json.py

Validate translation JSON files for completeness and format.

### Usage
```bash
# Single file
python3 tools/validate_json.py translations/chapter_001.json

# All files
python3 tools/validate_json.py translations/
```

### Checks
- Valid JSON syntax
- Required fields present
- No empty/null translations
- Sequential segment IDs
- UTF-8 encoding
- Matching segment counts

### Output
```
✓ chapter_001.json: Valid (52 segments)
✗ chapter_002.json: ERROR - Missing 'en' in segment 15
✓ chapter_003.json: Valid (38 segments)
```

---

## Development Notes

### Adding New Tools

When adding tools:
1. Add Python script to this directory
2. Update requirements.txt if needed
3. Document usage in this README

### LaTeX Template

The PDF compiler uses this structure:
```latex
\documentclass[11pt]{article}
\usepackage{xeCJK}
\usepackage{xcolor}
\usepackage{geometry}

% Font setup for CJK
\setCJKmainfont{Noto Serif CJK SC}
\setCJKsansfont{Noto Sans CJK SC}

% Color definitions
\definecolor{modernzh}{HTML}{333333}
\definecolor{english}{HTML}{00008B}
\definecolor{russian}{HTML}{8B0000}
\definecolor{japanese}{HTML}{006400}

% Content formatted here...
```

### Handling Long Chapters

For chapters with many segments:
- Split into multiple PDF pages automatically
- Each segment starts on new line
- Page breaks at natural points

---

## Troubleshooting

### PDF Generation Fails

1. Check XeLaTeX is installed: `xelatex --version`
2. Check fonts are available: `fc-list | grep Noto`
3. Check JSON is valid: `python3 tools/validate_json.py file.json`

### Character Encoding Issues

- Ensure all files are UTF-8
- Check terminal encoding: `echo $LANG`
- Verify JSON escape sequences

### Missing Fonts

Install Noto fonts:
```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# Or download from Google Fonts
```

---

## Integration with Workflow

### Recommended Workflow

1. **Translate** → Save to `translations/chapter_XXX.json`
2. **Validate** → `python3 tools/validate_json.py translations/chapter_XXX.json`
3. **Compile** → `python3 tools/compile_chapters.py translations/chapter_XXX.json output/`
4. **Review** → Check output PDF for formatting issues

### Continuous Integration

Workers should validate JSON before committing:
```bash
# In commit hook or manual check
python3 tools/validate_json.py translations/chapter_*.json
```

---

*Tools are provided to support the translation workflow. Report issues or suggest improvements via git commits.*
