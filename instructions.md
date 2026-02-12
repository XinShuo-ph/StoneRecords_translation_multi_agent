## Goal (Translation Instructions Only)

Translate **each PDF page** of `红楼梦脂评汇校本_有书签目录_v3.13.pdf` into four languages:
- **Modern Chinese (简体中文)**: clear modern prose with classical flavor
- **English**: scholarly literary translation
- **Russian (Русский)**: literary Russian
- **Japanese (日本語)**: literary Japanese with a lightly classical register

This file is **only** the translation instruction + output contract. Parallel worker protocols (how to split work, coordinate, etc.) should live elsewhere.

---

## Inputs You Must Use (to avoid missing commentary)

- **PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
- **Page image**: `source_pages/page_XXXX.png` (generated via `tools/pdf_to_images.py`)

Always work from the **page image** for layout (眉批/侧批/夹批) and use the PDF for zoom/verification. Many failures come from reading only extracted text and missing margin notes.

Important: the page may print a small page number at the bottom; **ignore that** and use the **PDF page index** (the number in the filename `page_XXXX.png`).

---

## Output Location

Create one file per page:

- `translations/page_XXXX.json` (4-digit PDF page number, e.g. `page_0020.json`)

Use UTF-8. JSON must validate with `python3 tools/validate_json.py`.

---

## Canonical JSON Contract (must match the validator)

See `tools/validate_json.py` for the exact checks. Minimum required fields:

- `page` (int)
- `chapter` (string, e.g. `"第一回"`, `"凡例"`, `"附录"`)
- `segments` (non-empty array)
- `translator_notes` (array of strings)
- `total_segments` (int, must equal `segments.length`)

### Allowed values

- `segments[].type`: `"prose" | "poem" | "dialogue"`
- `segments[].commentary[].type`: `"眉批" | "夹批" | "侧批" | "回前批" | "回末批" | "回末总批"`

### Commentary objects (required keys)

Every commentary item must include:

- `type`, `source`, `original`, `zh_modern`, `en`, `ru`, `ja`

You may add extra keys (e.g. `commentator`, `position`) if helpful; they won’t break validation.

### Optional page-level keys (use when applicable)

- `page_content_type`: `"front_matter" | "fanli" | "chapter_start" | "chapter_body" | "chapter_end" | "appendix"`
- `chapter_title`: `{ original, zh_modern, en, ru, ja }` (only when the chapter title appears on this page)
- `chapter_end_commentary`: commentary array for end-of-chapter notes that are not tied to a single segment
- `pdf_page_range`: `{ start, end, note }` (only if you are sure; otherwise omit)

### Minimal template

```json
{
  "page": 20,
  "chapter": "第一回",
  "page_content_type": "chapter_body",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "原文……",
      "zh_modern": "现代汉语……",
      "en": "English…",
      "ru": "Русский…",
      "ja": "日本語…",
      "commentary": [
        {
          "type": "夹批",
          "source": "甲戌",
          "original": "批语原文……",
          "zh_modern": "……",
          "en": "…",
          "ru": "…",
          "ja": "…"
        }
      ]
    }
  ],
  "translator_notes": [
    "VERIFY: first line anchor … / last line anchor …",
    "CONTINUITY: page ends mid-sentence; continues on page 21.",
    "RESEARCH: …",
    "DECISIONS: …",
    "GLOSSARY_ADD: … (if any)"
  ],
  "total_segments": 1
}
```

See `examples/page_0020.json` for a full page example.

---

## Page Translation Workflow (prevents wrong-page + partial-coverage failures)

### Step 1: Full-page scan (coverage map)

From the page image, scan **top → bottom** and list everything visible:
- main text (正文)
- **all** commentary: 眉批 / 夹批 / 侧批 / 回末批
- poetry, embedded couplets, headings, chapter titles

If you do not see it on the page image, do not invent it. If you do see it, do not omit it.

### Step 2: Segment the main text (no omissions)

Create `segments[]` in the **reading order** of the page. Each segment should be a contiguous block of正文:
- keep poems as `"type": "poem"` and preserve line breaks (`\n`)
- keep dialogue as `"type": "dialogue"` (preserve quotation marks)

Rule: if the page contains N distinct正文 blocks, you should have N segments. Do **not** translate “a few sentences” and stop.

### Step 3: Attach commentary precisely

For each segment:
- include `commentary: []` even if there is none
- for each comment, set `commentary[].type` (眉批/夹批/侧批/…)
- set `commentary[].source` to the tag shown in the text (e.g. `甲戌`, `庚辰`, `己卯`); if none is printed, use `"未标明"`

If you’re unsure what the comment refers to, keep it with the nearest segment and add `position` like `"position": "right margin beside segment 3"` to make it auditable.

### Step 4: Translate (best-effort, never empty)

Every `segments[]` item must have non-empty:
- `original`, `zh_modern`, `en`, `ru`, `ja`

If uncertain, still translate, and record uncertainty in `translator_notes` (e.g. `UNCERTAIN: …`). Do **not** leave fields blank.

### Step 5: Multi-window consistency (the “handoff”)

To keep quality consistent across **tens of context windows**, every page must include `translator_notes` entries that future pages can rely on:
- `VERIFY:` **two anchors** from the page image (top and bottom) to prove you translated the correct page
- `CONTINUITY:` whether the page starts/ends mid-sentence; identify the cut point
- `DECISIONS:` key choices (e.g., how you rendered a pun/allusion; any tricky term)
- `GLOSSARY_ADD:` new names/terms not already in `research/glossary.md` (add them to the glossary in a separate commit when doing real translation work)

### Step 6: Validate JSON (format gate)

Run:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Fix any errors before you consider the page “done”.

---

## Quality and Style (high-level)

- **Glossary**: use `research/glossary.md` for names/terms; don’t freestyle spellings across pages.
- **Character voice**: reference `research/character_guide.md` to keep dialogue consistent.
- **Poetry**: follow `research/poetry_guide.md` (meaning → imagery → tone → sound).
- **Commentary tone**: follow `research/commentary_guide.md` (often scholarly, sometimes emotional/elliptic).
- **Existing translations**: you may consult `research/existing_translations.md` for comparison only; do **not** copy phrasing.

---

## Anti-Patterns (these caused the recent experiment failures)

- Translating the wrong page (fix: use `page_XXXX.png` and add `VERIFY:` anchors)
- Translating only part of the page (fix: segment everything; `segments` must cover all正文 blocks)
- Dropping commentary (fix: full-page scan; attach every comment with `type`/`source`)
- Invalid JSON / missing keys (fix: follow the canonical contract + run validation)
- Inconsistent names/terms across pages (fix: glossary-first + `DECISIONS:` + `GLOSSARY_ADD:`)
