# Translation Instructions (Translation-Only Contract)

This document defines only translation requirements and JSON output quality.

It intentionally does **not** define parallel-worker behavior (claiming pages, heartbeats, sync frequency, branch protocol, or session management). Keep those rules in a separate worker-protocol document.

---

## 1) Scope: One Input Page -> One Output JSON

For each assigned page number `XXXX`:

- **Read source** from:
  - PDF: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
  - Image: `source_pages/page_XXXX.png`
- **Write output** to:
  - `translations/page_XXXX.json`

Hard constraints:

1. Do not create `*_temp.json`, `*_test.json`, or any other non-standard filename in `translations/`.
2. Do not save partial work as `page_XXXX.json`.
3. A page file is valid only when the full page has been translated and validated.

---

## 2) Atomic Workflow Per Page

### Step A - Page Identity Gate (prevents wrong-page translations)

Before translating:

1. Open `source_pages/page_XXXX.png`.
2. Confirm page number equals `XXXX`.
3. Record two anchors from the original page:
   - `page_anchor.top`: first clearly visible original phrase near top
   - `page_anchor.bottom`: last clearly visible original phrase near bottom

Each anchor should be at least 8 characters when possible.

### Step B - Coverage Gate (prevents partial-page output)

Capture **all visible textual content** on the page:

- Main prose
- Dialogue
- Poetry
- Commentary (眉批, 夹批, 侧批, 回末批, etc.)

Rules:

- Every segment must include `commentary` (empty `[]` if none).
- If a sentence starts on previous page or continues to next page, translate the visible part and mention continuation in `notes`.
- Never skip difficult lines. If uncertain, provide best translation and log uncertainty in `notes`.

### Step C - Research Notes Gate (prevents shallow translation)

Before finalizing, write at least **2 substantive notes** in `notes`:

- allusions /典故
- wordplay / names / register choices
- commentary source interpretation
- culture-specific context

### Step D - Translation Quality Gate

For every segment and commentary item, provide:

- `zh_modern`
- `en`
- `ru`
- `ja`

Quality requirements:

- Preserve literary tone (no flat machine-like paraphrase)
- Keep names consistent across pages
- Keep poem line breaks in all target languages when source is verse
- Do not use placeholders (`TODO`, `TBD`, `待补`, `未翻译`, etc.)

### Step E - Validation Gate

Run:

```bash
python3 tools/validate_json.py translations/page_XXXX.json
```

Only keep the file if validation passes.

---

## 3) Strict JSON Schema

### Required root keys (exact)

- `page` (int)
- `chapter` (string)
- `page_image` (string; must be `source_pages/page_XXXX.png`)
- `page_anchor` (object with `top`, `bottom`)
- `segments` (array)
- `notes` (array of strings, at least 2 items)

No extra root keys.

### Required segment keys (exact)

- `id` (1..N, sequential)
- `type` (`"prose" | "poem" | "dialogue"`)
- `original`
- `zh_modern`
- `en`
- `ru`
- `ja`
- `commentary` (array; empty allowed)

No extra segment keys.

### Required commentary keys (exact)

- `source`
- `original`
- `zh_modern`
- `en`
- `ru`
- `ja`

No extra commentary keys.

---

## 4) JSON Example (abbreviated schema demo)

```json
{
  "page": 20,
  "chapter": "第一回",
  "page_image": "source_pages/page_0020.png",
  "page_anchor": {
    "top": "士隐意欲也跟了过去，方举步时，忽听一声霹雳",
    "bottom": "你我不必同行，就此分手，各干营生去罢。三劫后，"
  },
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "士隐意欲也跟了过去，方举步时，忽听一声霹雳，有若山崩地陷。",
      "zh_modern": "士隐也想跟过去，刚抬步，忽然一声霹雳，好像山崩地裂。",
      "en": "Shiyin meant to follow, but as he stepped forward, a thunderclap broke out as if mountains collapsed and earth split apart.",
      "ru": "Шиинь хотел последовать за ними, но едва шагнул, как грянул гром, словно рушились горы и трескалась земля.",
      "ja": "士隠も後を追おうとしたが、踏み出した途端、山崩れ地割れのごとき雷鳴が轟いた。",
      "commentary": [
        {
          "source": "脂批",
          "original": "真是大警觉大转身。",
          "zh_modern": "这真是一次大警醒、大转折。",
          "en": "This is truly a great awakening and a decisive turn.",
          "ru": "Воистину великое пробуждение и резкий поворот.",
          "ja": "まことに大いなる警醒、大いなる転身である。"
        }
      ]
    },
    {
      "id": 2,
      "type": "poem",
      "original": "好防佳节元宵后，\n便是烟消火灭时。",
      "zh_modern": "要提防元宵佳节之后，\n那时便是烟消火灭之际。",
      "en": "Beware the days after the Lantern Festival:\nthat is when smoke will fade and fire go out.",
      "ru": "Берегись поры после Праздника фонарей:\nтогда рассеется дым и угаснет огонь.",
      "ja": "佳節たる元宵の後をこそ戒めよ、\nその時こそ煙は消え、火は尽きる。",
      "commentary": []
    }
  ],
  "notes": [
    "“元宵后” foreshadows Yinglian's abduction and the family's subsequent disaster.",
    "“烟消火灭” works both as literal omen and structural foreshadowing of household collapse.",
    "This page ends mid-line; continuation should be checked against page 21."
  ]
}
```

---

## 5) Anti-Patterns (Reject Immediately)

- Wrong source page translated into `page_XXXX.json`
- Only partial page translated (top half only, or a few sentences only)
- Missing required keys
- Missing `commentary` key on any segment
- Invalid JSON syntax
- Placeholder text in any language field
- Empty `notes` or purely trivial notes

---

## 6) Final Checklist Per Page

- [ ] `page` matches filename `page_XXXX.json`
- [ ] `page_image` matches `source_pages/page_XXXX.png`
- [ ] `page_anchor.top` and `page_anchor.bottom` are filled
- [ ] All visible page text translated (main + commentary)
- [ ] Every segment has all four target languages and `commentary`
- [ ] IDs are sequential from 1
- [ ] `notes` has at least 2 substantive items
- [ ] `python3 tools/validate_json.py translations/page_XXXX.json` passes
