# Quick Start: Using v2 Translation Instructions

**For agents translating 红楼梦 pages**

---

## TL;DR

1. Read `instructions_v2/01_core_task.md` (30 lines)
2. Start translating
3. Reference other files as needed

---

## File Map

```
instructions_v2/
├── 00_READ_ME_FIRST.md          ← Navigation guide
├── 01_core_task.md              ← START HERE (30 lines)
├── 02_json_schema.md            ← Open when creating JSON
├── 03_quality_guidelines.md     ← Reference for style questions
└── 04_research_resources.md     ← Reference when researching
```

---

## First Time? Read This

### Step 1: Core Task (2 minutes)

Open `instructions_v2/01_core_task.md` and read it. It's 30 lines.

You'll learn:
- Goal: Translate into 4 languages (Modern Chinese, English, Russian, Japanese)
- Task: 9 steps per page
- Success: 6 checkboxes to verify
- Output: `translations/page_XXXX.json`

### Step 2: JSON Format (3 minutes)

Skim `instructions_v2/02_json_schema.md` to see the required structure.

Key points:
- Required fields clearly marked
- NO extra fields allowed
- See examples at bottom

### Step 3: Start Translating

Pick a page (or you'll be assigned pages).

For each page:
1. View: Open `source_pages/page_XXXX.png` or the PDF
2. Segment: Break into 5-15 logical units
3. Translate: All 4 languages for each segment
4. Document: Research findings in `notes`
5. Save: `translations/page_XXXX.json`
6. Next: Move to next page immediately

### Reference Files (as needed)

- **Looking up a character name?** → `research/glossary.md`
- **Need style guidance?** → `instructions_v2/03_quality_guidelines.md`
- **Stuck on research?** → `instructions_v2/04_research_resources.md`
- **Unsure about JSON structure?** → `instructions_v2/02_json_schema.md`

---

## Differences from v1

If you used the old `instructions.md`:

| What | v1 | v2 |
|------|----|----|
| Length | 234 lines (one file) | 30 lines core + references |
| Structure | Monolithic | Modular (5 files) |
| JSON schema | Example-based | Explicit rules |
| Parallel protocol | Embedded | **Removed** (separate file) |
| Research | "Read before translating" | "Reference as needed" |
| Extra fields | Sometimes added | **Not allowed** |

---

## Common Questions

### Q: Where are my page assignments?

You'll receive page assignments separately (e.g., "Translate pages 40-60").

The translation instructions don't specify which pages—they only explain HOW to translate.

### Q: What about parallel protocol (CLAIM/DONE commits)?

If you're part of a parallel project, you'll receive separate coordination instructions.

`instructions_v2/` contains ONLY translation quality guidelines.

### Q: Can I add extra fields to JSON?

**NO.** The schema in `02_json_schema.md` explicitly lists allowed fields.

Don't add: `pdf_page`, `page_content_type`, `characters_appearing`, `translator_notes`, etc.

Use only the fields in the schema.

### Q: How do I know if I'm done with a page?

Check the 6 success criteria in `01_core_task.md`:

- ✓ ALL visible text translated (main + commentary)
- ✓ 4 languages for every segment
- ✓ Commentary field for every segment (empty `[]` if none)
- ✓ Research notes documented
- ✓ JSON validates
- ✓ File saved

### Q: What if I'm stuck on a passage?

From `01_core_task.md`:
> If stuck >5 minutes: add note `"Uncertain: [question]"` and continue

Don't stop. Document uncertainty and move on.

### Q: How many segments should a page have?

**5-15 segments** for most pages.

- **Prose**: 1-3 sentences per segment
- **Poetry**: 1 poem or stanza per segment
- **Dense pages**: More segments (up to 15)
- **Sparse pages**: Fewer segments (down to 5)

---

## Time Budget

**Target**: 45-60 minutes per page

Breakdown:
- View/scan: 2-3 min
- Research: 10-15 min
- Translate main: 20-25 min
- Translate commentary: 5-10 min
- Review: 5-8 min
- Save: 1-2 min

**Goal**: 1-1.5 pages per hour sustained pace

If taking much longer → you're over-researching or stuck. Note uncertainties and move on.

---

## Schema Quick Reference

```json
{
  "page": 20,                           // Required: PDF page number
  "chapter": "第一回",                  // Required: Chapter identifier
  "segments": [                         // Required: Array of segments
    {
      "id": 1,                          // Required: Sequential (1, 2, 3...)
      "type": "prose",                  // Required: prose|poem|dialogue
      "original": "...",                // Required: Classical Chinese
      "zh_modern": "...",               // Required: Modern Chinese
      "en": "...",                      // Required: English
      "ru": "...",                      // Required: Russian
      "ja": "...",                      // Required: Japanese
      "commentary": []                  // Required: Empty if none
    }
  ],
  "notes": ["Finding 1", "Finding 2"]   // Required: Research findings
}
```

**NO OTHER FIELDS ALLOWED.**

---

## Example Workflow

**Page 20 translation** (actual example):

1. **View** (2 min): Open `source_pages/page_0020.png`
   - See main narrative text
   - See 3 commentary annotations (【甲戌】)
   - See one 4-line poem

2. **Research** (12 min):
   - Look up "贾雨村" → `research/glossary.md` → Jia Yucun
   - Check commentary → `research/commentary_guide.md` → 甲戌本 annotations
   - Character name pun? → Search "贾雨村 谐音" → 假语存 (false words)
   - Poem form? → Count lines (4) and characters (7) → 七言绝句

3. **Segment** (3 min): Break into segments
   - Segment 1: Prose (dream awakening scene)
   - Segment 2: Poem (monk's prophecy)
   - Segment 3: Dialogue (monk and Daoist conversation)

4. **Translate** (25 min):
   - Segment 1: Translate into 4 languages + 3 commentary annotations
   - Segment 2: Translate poem (preserve 4-line structure)
   - Segment 3: Translate dialogue

5. **Document** (5 min): Create `notes` array
   - "贾雨村 pun on 假语存 (false words remain)"
   - "霍启 = 祸起 (disaster begins), foreshadows kidnapping"
   - "Poem form: 七言绝句, '烟消火灭' foreshadows family decline"

6. **Save** (2 min):
   - Create `translations/page_0020.json`
   - Validate JSON syntax
   - Verify all required fields present

7. **Next**: Move to page 21

**Total**: 49 minutes

---

## Ready?

1. Open `instructions_v2/01_core_task.md`
2. Read 30 lines
3. Start translating

Good luck! 加油！

---

**Questions? See `SUMMARY.md` for full context or `instructions_v2/IMPROVEMENTS.md` for v1 vs v2 comparison.**
