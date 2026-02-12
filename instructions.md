# Translation Instructions (Translation-Only, v2)

This file defines **translation quality and JSON output only**.

It does **not** define worker coordination, claiming pages, heartbeat, or branch sync behavior.
Those belong to a separate worker protocol.

---

## 1) Goal

Translate each assigned PDF page of `红楼梦脂评汇校本_有书签目录_v3.13.pdf` into:

- Modern Chinese (`zh_modern`)
- English (`en`)
- Russian (`ru`)
- Japanese (`ja`)

For each page, translate **all visible text**:

- Main narrative text (正文)
- Poetry
- Commentary (脂评: 眉批 / 夹批 / 侧批 / 回末批 etc.)

One PDF page = one JSON file at `translations/page_XXXX.json`.

---

## 2) Definition of Done (Non-Negotiable)

A page is complete only if all conditions below are true:

1. Filename and page number match (`page_0020.json` => `"page": 20`).
2. Every segment has all required translation fields.
3. Every segment has `commentary` (use `[]` when none).
4. No placeholders or summaries (forbidden: `[Dialogue ...]`, `TODO`, `TBD`, "continued...", etc.).
5. JSON is valid and passes `python3 tools/validate_json.py translations/page_XXXX.json`.
6. `notes` contains concrete research findings (minimum 3 non-empty items).

If any item fails, the page is **not done**.

---

## 3) Workflow Per Page

### Step A: Lock the source page

- Open the exact target page in PDF or page image.
- Confirm page number before translating.
- Read top-to-bottom and mark all text blocks (main text + commentary).

### Step B: Build segments before writing

- Split by natural textual units (prose block / poem / dialogue block).
- Keep source order.
- Do not merge unrelated blocks.
- Do not skip "small" marginal comments.

### Step C: Translate each segment fully

For each segment:

1. Copy original Classical Chinese into `original`.
2. Translate to `zh_modern`, `en`, `ru`, `ja`.
3. Add segment-level `commentary` array:
   - `[]` if no commentary belongs to this segment.
   - Otherwise add commentary objects with full 5-language coverage.

### Step D: Research and polish

Before finalizing:

- Check terms against `research/glossary.md`.
- Resolve key allusions/puns and capture them in `notes`.
- Polish for literary tone and clarity.
- Ensure names and terms stay consistent inside the page.

### Step E: Validate and save

- Save to `translations/page_XXXX.json`.
- Run validator:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

- Fix all errors before moving on.

---

## 4) Canonical JSON Schema (Required)

Use this exact top-level structure:

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "原文...",
      "zh_modern": "现代汉语...",
      "en": "English...",
      "ru": "Русский...",
      "ja": "日本語...",
      "commentary": [
        {
          "source": "甲戌本",
          "original": "批语原文",
          "zh_modern": "现代汉语批语",
          "en": "English commentary",
          "ru": "Комментарий",
          "ja": "日本語注釈"
        }
      ]
    }
  ],
  "notes": [
    "Research finding 1...",
    "Research finding 2...",
    "Research finding 3..."
  ]
}
```

### Required keys

- Top level: `page`, `chapter`, `segments`, `notes`
- Segment: `id`, `type`, `original`, `zh_modern`, `en`, `ru`, `ja`, `commentary`
- Commentary object: `source`, `original`, `zh_modern`, `en`, `ru`, `ja`

### `type` allowed values

- `prose`
- `poem`
- `dialogue`

### `notes` requirements

- Must be an array of strings.
- Minimum 3 items.
- Must contain concrete findings (allusion, term choice, textual ambiguity, source comparison, etc.).
- No blank or generic filler notes.

---

## 5) Quality Floor

### Fidelity

- Do not paraphrase away key meaning.
- Keep metaphors, irony, and foreshadowing explicit where present.
- Preserve poem line breaks.

### Register

- `zh_modern`: readable modern Chinese with classical flavor retained.
- `en`: literary-scholarly tone, consistent pinyin names.
- `ru`: literary Russian register, no colloquial flattening.
- `ja`: literary Japanese tone with classical influence.

### Completeness

- Never skip commentary.
- Never submit partial-page stubs.
- Never replace unknown text with bracket placeholders.

If uncertain:

- Keep the best faithful translation you can produce.
- Record uncertainty in `notes` with a concrete explanation.
- Continue; do not leave fields empty.

---

## 6) Hard Reject Patterns

Any of the following is an automatic failure:

- Wrong page in filename vs `page` value
- Invalid JSON (quote escaping errors, trailing commas, etc.)
- Missing required keys
- Empty translation fields
- Placeholder text (`[ ... ]`, `TODO`, `TBD`, etc.)
- Commentary translated in only one language
- Fewer than 3 meaningful notes

---

## 7) Pre-Save Checklist

Before finalizing each page:

- [ ] Correct page number and filename
- [ ] All visible main text is segmented and translated
- [ ] All visible commentary is included and translated
- [ ] Every segment has full `zh_modern/en/ru/ja`
- [ ] Every segment has `commentary` (`[]` if none)
- [ ] IDs are 1..N with no gaps
- [ ] `notes` has at least 3 concrete research items
- [ ] `python3 tools/validate_json.py translations/page_XXXX.json` passes

If any box is unchecked, revise before proceeding.
