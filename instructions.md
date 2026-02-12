## Translation Instructions (pages → JSON)

This document defines the **translation instructions only** (what to translate, how to translate, and the required JSON contract). Keep any parallel/worker execution protocol separate.

---

## Non‑negotiables

- **Translate the exact requested PDF page**. The JSON `page` value must match the file name `translations/page_XXXX.json`.
- **Translate ALL visible content on the page**:
  - Main narrative text (正文)
  - All commentary (脂评): 眉批 / 夹批 / 侧批 / 回前批 / 回末批 / 回末总批 (or mark type as `未知` if uncertain)
  - Poetry and any headings
- **Every segment must include all 4 target translations**: Modern Chinese, English, Russian, Japanese.
- **Do not copy from copyrighted translations**. Use `research/existing_translations.md` only for comparison.
- **Consistency is mandatory**: follow `research/glossary.md` for names/terms.

---

## Source material

- **PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
- **Preferred visual reference**: `source_pages/page_XXXX.png` (if available)

---

## Per‑page workflow (recommended)

### 1) Inventory the page (completeness first)

Before translating, scan the full page and list everything you must cover:
- Paragraphs (正文)
- Poetry blocks (keep original line breaks)
- Commentary blocks (note type + where it appears)

### 2) Research (only what you need)

Use `research/` as the shared “anchor” across many context windows:
- Glossary/terms: `research/glossary.md`
- Commentary conventions: `research/commentary_guide.md`
- Poetry strategy: `research/poetry_guide.md`
- Cultural background: `research/cultural_context.md`

Record research outcomes as bullet points in `translator_notes` (minimum 1 note per page).

### 3) Translate

Segment the page into small units (usually paragraph-sized; poetry as stanza blocks). For each segment:
- Copy the **full original** text for that segment into `original`
- Translate into `zh_modern`, `en`, `ru`, `ja`
- Attach any commentary items to the segment via `commentary` (or use a short `position` string to clarify anchoring)

### 4) Polish (润色)

Do a fast quality pass:
- Names and key terms match the glossary
- English is literary and precise (not “chatty”)
- Russian is literary (not machine-literal)
- Japanese keeps a classical literary tone
- Poetry preserves structure (line breaks) and explains allusions in notes

### 5) Validate & save

Save as `translations/page_XXXX.json`.

Run validation locally (recommended): `python3 tools/validate_json.py translations/page_XXXX.json`

---

## JSON output contract (schema `page.v2`)

### Top‑level shape (required)

```json
{
  "schema_version": "page.v2",
  "page": 20,
  "chapter": "第一回",
  "source": {
    "pdf": "红楼梦脂评汇校本_有书签目录_v3.13.pdf",
    "page_image": "source_pages/page_0020.png"
  },
  "segments": [],
  "translator_notes": []
}
```

### Rules

- **Only these top-level keys are allowed**: `schema_version`, `page`, `chapter`, `source`, `segments`, `translator_notes`, plus optional `chapter_title`, `page_content_type`, and optional `meta` (put any extra data under `meta` only).
- `translator_notes` must be a **non-empty** array of strings.
- `segments` must be non-empty, and `segments[].id` must be sequential starting at 1.
- Every segment must include `commentary` (use `[]` if none).
- **JSON safety**: do not put raw `"` characters inside text fields. Use Chinese quotation marks (e.g. `“…”`, `「…」`) or escape as `\"`.

### Segment object (required fields)

```json
{
  "id": 1,
  "type": "prose",
  "original": "原文...",
  "zh_modern": "现代汉语...",
  "en": "English...",
  "ru": "Русский...",
  "ja": "日本語...",
  "commentary": []
}
```

Valid `type`: `prose` | `dialogue` | `poem`.

### Commentary object (required fields)

```json
{
  "type": "夹批",
  "source": "脂批",
  "position": "after …", 
  "original": "批语原文…",
  "zh_modern": "现代汉语…",
  "en": "English…",
  "ru": "Русский…",
  "ja": "日本語…"
}
```

- `type` must be one of: `眉批` | `夹批` | `侧批` | `回前批` | `回末批` | `回末总批` | `未知`.
- `position` is optional but recommended for 夹批 / 侧批.

See `examples/page_0020.json` for a complete, page-sized example.

---

## Definition of done (per page)

- [ ] File name matches page: `translations/page_XXXX.json` and JSON `page == XXXX`
- [ ] All visible main text + all visible commentary translated
- [ ] Every segment has all 4 target languages filled (no empty strings)
- [ ] Every segment has a `commentary` array (empty `[]` if none)
- [ ] `translator_notes` is present and non-empty (research, allusions, decisions)
- [ ] JSON validates with `tools/validate_json.py`
