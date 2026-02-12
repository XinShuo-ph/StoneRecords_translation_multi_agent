# Translation Instructions (v2, Translation-Only)

## Scope

This document defines **translation work only**:
- how to translate one page
- how to structure output JSON
- how to quality-check before finishing

This document does **not** define worker orchestration:
- branch sync
- heartbeat/daemon
- page claiming
- retry/recovery logic

Those belong to a separate parallel worker protocol.

---

## Task

Translate each assigned page from `source_pages/page_XXXX.png` into:
- Modern Chinese (`zh_modern`)
- English (`en`)
- Russian (`ru`)
- Japanese (`ja`)

Translate **all visible text** on the page:
- main narrative text
- poems/couplets
- commentary (眉批, 夹批, 侧批, 回前批, 回末批)

No summarization. No skipping.

---

## Output Contract (Strict)

Write exactly one file per page:
- Path: `translations/page_XXXX.json`
- Example: `translations/page_0020.json`

Top-level keys must be exactly:
- `page`
- `source_page`
- `chapter`
- `segments`
- `notes`

### Canonical JSON Shape

```json
{
  "page": 20,
  "source_page": "page_0020.png",
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "原文",
      "zh_modern": "现代中文",
      "en": "English",
      "ru": "Русский",
      "ja": "日本語",
      "commentary": [
        {
          "type": "夹批",
          "source": "甲戌本",
          "original": "批语原文",
          "zh_modern": "批语现代中文",
          "en": "Commentary in English",
          "ru": "Комментарий по-русски",
          "ja": "注釈の日本語訳"
        }
      ]
    }
  ],
  "notes": [
    "Research note on allusion or pun.",
    "Uncertain: if any reading remains ambiguous."
  ]
}
```

### Allowed Values

- `segments[].type`: `prose` | `poem` | `dialogue` | `other`
- `segments[].commentary[].type`:
  - `眉批`
  - `夹批`
  - `侧批`
  - `回前批`
  - `回末批`
  - `回末总批`
  - `其他`

### Hard Requirements

- `page` must match filename `page_XXXX.json`
- `source_page` must match `page_XXXX.png`
- `segments[].id` must be sequential `1..N`
- Every segment must include `commentary` (use `[]` if none)
- Every translation field must be a non-empty string
- `notes` must be a non-empty array of non-empty strings

Do not use alternate keys such as:
- `translator_notes`
- `total_segments`
- `page_content_type`
- `pdf_page`

---

## Page Workflow (Quality-First)

### 1) Lock the Page
- Confirm target page number before writing.
- Open `source_pages/page_XXXX.png`.
- Verify the output filename matches the same page.

### 2) Segment for Full Coverage
- Split main text into natural reading segments.
- Attach each commentary item to the nearest segment.
- If no commentary belongs to a segment, use `commentary: []`.
- Preserve source order from top to bottom, left to right.

### 3) Translate Faithfully
- `original` should be exact source text (including punctuation where visible).
- Translate meaning, tone, and register; do not paraphrase away key details.
- For poetry, preserve poetic quality and line structure where possible.

### 4) Add Research Notes
Document important findings in `notes`, such as:
- allusions (典故)
- name puns and double meanings
- historical/cultural context
- unresolved ambiguity (`Uncertain: ...`)

### 5) Validate Before Done

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Do not consider a page complete unless validation passes.

---

## Definition of Done (Per Page)

- Correct file path and page number
- Full page coverage (main text + commentary)
- Complete 4-language translation for each segment and commentary item
- Strict JSON schema compliance
- Validation command passes

---

## Common Failure Modes to Avoid

- Translating the wrong page
- Translating only part of the page
- Leaving empty translation fields
- Omitting `commentary` on some segments
- Using non-canonical filenames (`*_temp.json`, `*_test.json`)
- Using old schema keys (`translator_notes`, etc.)
