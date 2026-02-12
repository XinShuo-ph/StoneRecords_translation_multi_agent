# Core Translation Task

## Goal

Translate 红楼梦脂评汇校本 from Classical Chinese into:
- Modern Chinese (简体中文)
- English
- Russian (Русский)
- Japanese (日本語)

One PDF page → One JSON file.

---

## Task Per Page

1. **View** the page (PDF or `source_pages/page_XXXX.png`)
2. **Identify** all text: main narrative, commentary (脂评), poetry
3. **Research** meanings, allusions, context (use `research/` files and web search)
4. **Segment** the page into 5-15 logical units (sentences, paragraphs, or stanzas)
5. **Translate** each segment into all 4 target languages
6. **Translate** all commentary annotations
7. **Document** research findings in `notes` field
8. **Save** as `translations/page_XXXX.json` (see `02_json_schema.md` for format)
9. **Move** to next page immediately

---

## Success Criteria

✓ ALL visible text on page is translated (main text AND commentary)  
✓ 4 target languages present for every segment  
✓ Commentary field exists for every segment (empty `[]` if none)  
✓ Research notes document key findings  
✓ JSON validates against schema  
✓ File saved before moving to next page  

---

## What Is a "Segment"?

- **Prose**: 1-3 sentences of narrative or dialogue
- **Poetry**: One complete poem or stanza
- **Commentary**: Usually separate from main text segments

Typical page: 5-15 segments (more if dense text, fewer if sparse)

---

## Work Continuously

- Complete page → Save JSON → Next page → Repeat
- Don't pause between pages
- If stuck on a passage >5 minutes: add note `"Uncertain: [question]"` and continue
- Don't stop to ask for confirmation

---

**That's it. See `02_json_schema.md` for output format.**
