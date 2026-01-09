# Instruction Comparison: Old vs New

## Quick Summary

| Aspect | Old Instructions | New Instructions |
|--------|-----------------|------------------|
| **Length** | 779 lines | ~200 lines |
| **Focus** | Protocol + Translation | Translation only |
| **Workflow steps** | 10 vague steps | 4 concrete steps |
| **JSON fields** | 15+ required | 8 required |
| **Sync requirements** | Mandatory daemon | None (separate concern) |
| **Expected per-page time** | "30-60 minutes" | "15-20 minutes" |

---

## Key Changes

### 1. REMOVED: Parallel Protocol
The new instructions contain **zero** multi-agent coordination content:
- No sync daemon
- No WORKER_STATE.md
- No heartbeats
- No page claiming protocol

**Rationale**: Coordination is an infrastructure concern, not a translation concern. Agents should focus 100% on translation quality.

### 2. SIMPLIFIED: JSON Format

**Old format** required:
```
page, chapter, chapter_title (5 fields), page_content_type,
segments[].id, segments[].pdf_page, segments[].type, segments[].original,
segments[].zh_modern, segments[].en, segments[].ru, segments[].ja,
segments[].commentary[].type, segments[].commentary[].source,
segments[].commentary[].position, segments[].commentary[].original,
(+ 4 more commentary translations),
translator_notes, research_notes, characters_appearing,
total_segments, manuscript_sources_on_page
```

**New format** requires:
```
page, chapter, segments[].id, segments[].type, segments[].original,
segments[].zh_modern, segments[].en, segments[].ru, segments[].ja,
notes
```

Commentary is optional and simplified (no position/type metadata required).

### 3. SIMPLIFIED: Workflow

**Old workflow** (10 steps):
```
1. SYNC: Fetch all branches, see who's online
2. CLAIM: Take the lowest available PDF page
3. VIEW: Open the PDF page
4. READ: Carefully read the page
5. RESEARCH: Search online, study allusions, analyze, document
6. TRANSLATE: Translate to 4 languages
7. POLISH: Review literary quality, cultural adaptation
8. SAVE: Write JSON
9. BROADCAST: Commit & push
10. REPEAT
```

**New workflow** (4 steps):
```
1. VIEW: Open page image
2. TRANSLATE: All content to 4 languages
3. SAVE: Write JSON
4. NEXT PAGE: Continue immediately
```

### 4. ADDED: Time Targets

Old: "30-60 minutes depending on length and poetry content"
New: "15-20 minutes per page (target)"

Explicit time targets prevent agents from getting stuck in infinite research loops.

### 5. ADDED: Anti-Pattern Emphasis

Clear list of what NOT to do, with the most important being:
> **❌ Stopping to ask questions** - Keep working, add notes

---

## What Stayed the Same

- Translation to 4 languages (zh_modern, en, ru, ja)
- Quality emphasis (literary, scholarly)
- Commentary translation requirement
- Key terms glossary reference
- Character name pun documentation

---

## Files Created

1. `TRANSLATION_INSTRUCTION_ANALYSIS.md` - Detailed analysis of what went wrong
2. `TRANSLATION_INSTRUCTIONS_v2.md` - New simplified translation instructions
3. `examples/page_0020_complete.json` - Complete example in new format
4. `INSTRUCTION_COMPARISON.md` - This comparison document

---

## Recommended Next Steps

1. **Extract source pages to images** before next experiment
   ```bash
   python3 tools/pdf_to_images.py
   ```

2. **Test with single agent** using new instructions

3. **Create separate PARALLEL_PROTOCOL.md** for multi-agent coordination (if needed)

4. **Pre-assign page ranges** instead of dynamic claiming

---

## Expected Improvements

| Problem | Old Result | Expected New Result |
|---------|-----------|---------------------|
| Agents not following instructions | 37% produced ≤2 files | More consistent output |
| Wrong page content | Different content for same page# | Correct page matching |
| Early conversation stops | Stuck in sync loops | Focus on translation |
| Missing JSON fields | Inconsistent formats | Simpler = fewer errors |
| Low productivity | 0-34 files per branch | More consistent 15-25 |

---

*The best instruction is one an agent can execute without confusion.*
