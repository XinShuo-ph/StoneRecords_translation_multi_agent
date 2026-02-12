# Translation Instructions v2 (Content-Only)

## Scope

This file defines **translation instructions only**.

It does **not** define worker claiming, heartbeat/progress sync, branch coordination, or parallel scheduling. Those belong to a separate worker protocol.

## Goal

Translate each source PDF page of 《红楼梦脂评汇校本》 into:

- Modern Chinese (简体中文)
- English
- Russian (Русский)
- Japanese (日本語)

Each source page must produce exactly one JSON file:

- `translations/page_XXXX.json` (4-digit page number)

Translate all visible page content:

- Main text (正文)
- Commentary (脂批): 眉批 / 夹批 / 侧批 / 回前批 / 回末批
- Poetry, couplets, and chapter headings

## Source Files

- PDF: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
- Page image: `source_pages/page_XXXX.png`

Use both image and PDF:

- image for layout + marginal commentary
- PDF for accurate character reading/copying

## Canonical Output Schema (Single Source of Truth)

### Required top-level keys

```json
{
  "page": 20,
  "chapter": "第一回",
  "page_type": "chapter_body",
  "source_anchor": {
    "first_visible_text": "士隐意欲也跟了过去",
    "last_visible_text": "三劫后"
  },
  "segments": [],
  "research_notes": [],
  "total_segments": 0
}
```

### Optional top-level keys

- `translator_notes`: array of translation decisions or uncertainty notes
- `manuscript_sources_on_page`: array such as `["甲戌", "庚辰"]`

Do not add other top-level keys.

### `page_type` allowed values

- `front_matter`
- `fanli`
- `chapter_start`
- `chapter_body`
- `chapter_end`
- `appendix`

### Segment schema (required keys)

Each item in `segments` must include:

- `id` (1..N sequential)
- `type` (`prose` | `dialogue` | `poem` | `heading`)
- `original`
- `zh_modern`
- `en`
- `ru`
- `ja`
- `commentary` (array, use `[]` if none)

### Commentary item schema (required keys)

Each commentary object must include:

- `type` (`眉批` | `夹批` | `侧批` | `回前批` | `回末批` | `其他`)
- `source` (e.g., `甲戌`, `庚辰`, `己卯`, `脂批`, `未标注`)
- `original`
- `zh_modern`
- `en`
- `ru`
- `ja`

See `examples/page_0020.json` for a valid canonical file.

## Workflow Per Page

### 1) Confirm page identity

- Open `source_pages/page_XXXX.png`
- Open corresponding PDF page
- Record short anchors:
  - `source_anchor.first_visible_text`
  - `source_anchor.last_visible_text`

This is a hard requirement to reduce wrong-page outputs.

### 2) Segment all visible text

- Split page into logical segments (prose/dialogue/poem/heading)
- Include all visible commentary with each segment
- Do not skip text because it is difficult

If a character/phrase is unclear, keep best-effort reading and explain uncertainty in `translator_notes`.

### 3) Translate each segment fully

For each segment and commentary item, fill all language fields:

- `zh_modern`, `en`, `ru`, `ja`

No empty strings allowed for required translation fields.

### 4) Add research notes

`research_notes` must contain concrete findings that affected translation choices.

Minimum expectation: at least 2 non-empty notes per page, focusing on:

- allusions/典故
- name puns/双关
- manuscript commentary context
- culture-specific lexical choices

### 5) Validate before save

Run:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Fix all errors before moving on.

## Definition of Done (Per Page)

A page is complete only if all are true:

- [ ] File name is exactly `translations/page_XXXX.json`
- [ ] JSON parses successfully
- [ ] `page` matches file name number
- [ ] `source_anchor.first_visible_text` and `last_visible_text` are filled
- [ ] `segments` is non-empty and `id` is sequential from 1
- [ ] Every segment has non-empty `original`, `zh_modern`, `en`, `ru`, `ja`
- [ ] Every segment has `commentary` array (empty only when truly absent)
- [ ] Every commentary item has required keys and 4 language translations
- [ ] `research_notes` has at least 2 non-empty, specific items
- [ ] `total_segments == len(segments)`

## Translation Quality Rules

### Global rules

- Preserve narrative tone and emotional nuance.
- Do not flatten poetic or symbolic language into plain paraphrase.
- Keep proper names consistent with `research/glossary.md`.
- Preserve poem line breaks in all target languages where possible.

### Language-specific rules

- **Modern Chinese**: readable modern syntax, retain classical flavor.
- **English**: literary-academic register; preserve ambiguity where meaningful.
- **Russian**: literary style, avoid colloquial modern slang.
- **Japanese**: literary style with classical shading, but readable.

## Anti-Patterns (Fail Conditions)

- Wrong page content
- Partial page translation ("only a few sentences")
- Missing required keys
- Empty translation strings
- Invalid JSON
- Temporary/test filenames in `translations/` (e.g., `_temp`, `_test`)
- Generic or empty research notes

## Quick Command Reference

```bash
# Validate one page
python3 tools/validate_json.py translations/page_0020.json

# Validate all pages in translations/
python3 tools/validate_json.py translations/
```
