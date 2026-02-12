# Translation Instructions - Quick Navigation

## Start Here

**If you're translating pages**: Read `01_core_task.md` ONLY. It's 30 lines.

**For JSON format**: See `02_json_schema.md` for the exact structure.

**For quality tips**: Refer to `03_quality_guidelines.md` when needed.

---

## File Organization

```
instructions_v2/
├── 00_READ_ME_FIRST.md          ← You are here
├── 01_core_task.md              ← Essential task definition (30 lines)
├── 02_json_schema.md            ← Exact JSON structure required
├── 03_quality_guidelines.md     ← Style, voice, literary quality (reference)
└── 04_research_resources.md     ← Where to find background materials
```

---

## Translation Quick Start

1. Read `01_core_task.md` (30 lines)
2. Open PDF page or page image from `source_pages/`
3. Translate ALL text → 5-15 segments
4. Save to `translations/page_XXXX.json` using format from `02_json_schema.md`
5. Move to next page immediately

---

## Key Changes from v1

- **Drastically shorter** (30 lines core vs. 234 lines)
- **Modular** (split into focused files)
- **No parallel protocol** (coordination protocol is separate)
- **Explicit schema** (no ambiguity)
- **Action-oriented** (less explanation, more "do this")

---

## For Parallel Agents

If you're part of a parallel translation project, you'll receive **separate instructions** for:
- Work assignment (which pages to translate)
- Coordination protocol (claiming pages, signaling completion)
- Progress tracking (commit format, sync frequency)

**This folder contains ONLY translation instructions.**
