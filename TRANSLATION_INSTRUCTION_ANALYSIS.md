# Translation Instruction Quality Analysis

## Executive Summary

After analyzing 16 parallel agent branches from the recent Hong Lou Meng translation experiment and comparing with the successful Durov Code translation project (99 pages with consistent quality), I've identified the root causes of failure and recommendations for improvement.

---

## Observed Problems in Recent Experiment

### 1. Massive Productivity Variance

| Branch | Translation Files | Notes |
|--------|-------------------|-------|
| 1c3a | 34 files | Best performer |
| d4d0 | 26 files | Good |
| 27e6 | 16 files | Decent |
| 40bc | 7 files | Struggled |
| a535 | **0 files** | Claimed page 20, never completed |
| 5648 | 1 file | Early stop |
| 843e | 1 file | Early stop |
| f603 | 2 files | Early stop |

**Key finding**: 6 of 16 branches (37.5%) produced ≤2 translation files.

### 2. Duplicate Work / Wrong Pages

Multiple branches translated the same pages with different content:
- Branch 1c3a page_0020.json: Contains the "绛珠草" (Crimson Pearl) origin story
- Branch d4d0 page_0020.json: Contains Jia Yucun receiving money from Zhen Shiyin

**Both claim to be page 20 but contain completely different content.** This indicates:
1. Agents are misidentifying which PDF page they're on
2. The PDF page viewing method is unreliable
3. No verification that content matches claimed page

### 3. Content Incompleteness

Many translations only capture a few sentences from a page that should have 10-20 segments. Comparing:
- Branch 914c page_0021.json: 3 segments, no commentary
- Branch 40bc page_0021.json: 4 segments, rich commentary

The same page should produce consistent segment counts.

### 4. Early Conversation Stops

Agents getting stuck in loops:
```
[a535] AUTO-SYNC: Progress update HEARTBEAT: 1767410119
[a535] AUTO-SYNC: Progress update HEARTBEAT: 1767409939
[a535] AUTO-SYNC: Progress update HEARTBEAT: 1767409758
...
```

Branch a535 made 5+ AUTO-SYNC commits but **never produced any translation**. It was stuck in sync/claim loops.

### 5. JSON Format Inconsistencies

Some files missing required fields:
- Missing `chapter_title` object
- Missing `pdf_page` in segment objects  
- Empty `commentary` arrays vs missing `commentary` field
- `translator_notes` and `research_notes` inconsistently filled

---

## Root Cause Analysis

### Problem 1: Instruction Overload (779 lines)

The current `instructions.md` is **779 lines** covering:
- Translation task description
- Multi-agent protocol
- Sync daemon operation
- Git command sequences  
- JSON format specification
- Research workflow (3 sub-steps)
- Polish workflow (3 sub-steps)
- Commentary handling guide
- Chapter reference tables
- Anti-patterns
- Session end protocol

**Cognitive overload causes agents to:**
- Lose focus on the actual translation task
- Get stuck in protocol management
- Prioritize sync over translation work

### Problem 2: PDF-Based Workflow Without Reliable Page Access

Current instructions say:
> "Work directly from PDF pages or screenshots"

But agents cannot reliably:
1. View PDF pages (need image extraction tool)
2. Identify page boundaries
3. Match content to page numbers

**Contrast with Durov Code**: Pre-extracted text in `extracted/pages/page_XXX.txt`

### Problem 3: Overly Complex JSON Schema

Current required fields per segment:
```json
{
  "id": 1,
  "pdf_page": 15,
  "type": "prose",
  "original": "...",
  "zh_modern": "...",
  "en": "...",
  "ru": "...",
  "ja": "...",
  "commentary": [{
    "type": "眉批",
    "source": "甲戌本", 
    "position": "top margin",
    "original": "...",
    "zh_modern": "...",
    "en": "...",
    "ru": "...",
    "ja": "..."
  }]
}
```

Plus page-level metadata:
- `chapter_title` (5 language fields)
- `page_content_type`
- `translator_notes`
- `research_notes`  
- `characters_appearing`
- `manuscript_sources_on_page`

**This complexity causes format errors and incomplete output.**

### Problem 4: "Research-Translate-Polish" is Too Abstract

Current workflow:
```
RESEARCH → TRANSLATE → POLISH
     ↓         ↓          ↓
 (vague)   (okay)     (vague)
```

Agents don't know:
- What "research" actually means in practice
- How long to spend on research
- When research is "done enough"
- What "polish" actually requires

**Durov Code workflow** is concrete:
```
READ extracted text → PARSE sentences → TRANSLATE → SAVE JSON
```

### Problem 5: Sync Daemon Overhead

The mandatory sync daemon:
- Requires background process management
- Creates AUTO-SYNC commit noise
- Distracts from translation work
- Doesn't actually prevent duplicate work (agents still claimed same pages)

---

## Comparison: Successful Durov Code Instructions

| Aspect | Durov Code (Success) | Hong Lou Meng (Failed) |
|--------|---------------------|----------------------|
| Length | ~500 lines | 779 lines |
| Source text | Pre-extracted TXT files | "View PDF somehow" |
| JSON format | Simple sentences array | Complex nested schema |
| Workflow | 4 clear steps | 10 vague steps |
| Research | Not emphasized | Mandatory but undefined |
| Sync | Simple git fetch | Mandatory daemon |
| Focus | Translation task | Protocol management |

### What Durov Code Gets Right

1. **Pre-provided resources ready to use**
   ```
   extracted/pages/page_001.txt  # Just cat and translate
   ```

2. **Simple JSON structure**
   ```json
   {
     "page": 13,
     "sentences": [
       {"id": 1, "ru": "...", "en": "...", "zh": "...", "ja": "..."}
     ]
   }
   ```

3. **Concrete step-by-step**
   ```
   1. cat extracted/pages/page_013.txt
   2. Parse into sentences
   3. Translate each sentence  
   4. Save as JSON
   ```

4. **Continuous execution emphasized**
   > "Do NOT pause between pages to ask for confirmation. Keep working."

5. **Time estimates provided**
   > "Each page should take roughly 10-20 minutes"

---

## Recommendations

### 1. Completely Separate Translation Instructions from Parallel Protocol

Create two separate documents:
- `TRANSLATION_INSTRUCTIONS.md` - Pure translation task (this agent's job)
- `PARALLEL_PROTOCOL.md` - Multi-agent coordination (system-level concern)

Agents should focus 100% on translation. Coordination should be handled by:
- External orchestrator
- Pre-assigned page ranges
- Post-processing deduplication

### 2. Provide Extracted Text or Clear Page Viewing

Option A: Extract all PDF pages as text
```
extracted/
├── page_0001.txt
├── page_0002.txt
└── ...
```

Option B: Extract as images with clear naming
```
source_pages/
├── page_0001.png  # Must match exactly
└── ...
```

### 3. Simplify JSON Output Format

Minimal required fields:
```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "original": "原文",
      "zh_modern": "现代文",
      "en": "English",
      "ru": "Русский",
      "ja": "日本語"
    }
  ],
  "notes": ["Any important observations"]
}
```

Commentary can be inline or separate, but don't require 5 metadata fields per comment.

### 4. Define Concrete Workflow with Time Limits

```
For each page (target: 15-20 minutes):

1. VIEW PAGE (1 min)
   - Open source_pages/page_XXXX.png
   - Identify all text content

2. EXTRACT TEXT (2 min)
   - Copy all original Classical Chinese text
   - Note any commentary present

3. TRANSLATE (10 min)
   - Translate each segment to 4 languages
   - Include commentary translations inline

4. SAVE & CONTINUE (2 min)
   - Write translations/page_XXXX.json
   - Move to next page immediately
```

### 5. Remove Sync Daemon Requirement

Replace with:
- Pre-assigned page ranges per worker
- Simple progress file update (no daemon)
- Accept some overlap, deduplicate later

### 6. Add "Golden Examples" with Exact Expected Output

Provide 2-3 complete page translations showing:
- Exact format expected
- All fields properly filled
- Realistic content length
- Commentary handling

---

## Proposed New Instruction Structure

```
# 红楼梦 Translation Task

## Your Task (One Sentence)
Translate PDF pages from Classical Chinese to 4 languages, saving each as JSON.

## Source Material
- Pages are at: source_pages/page_XXXX.png
- Start with page: [assigned]
- End with page: [assigned]

## For Each Page (15-20 min target)

### Step 1: View
[how to view]

### Step 2: Translate
[what to translate, example]

### Step 3: Save
[exact format, example]

### Step 4: Next Page
[continue without stopping]

## Output Format
[simple JSON with example]

## Quality Guidelines
[brief, specific]

## Don't Do
[anti-patterns]
```

**Target: ~200 lines maximum**

---

## Next Steps

1. Create `TRANSLATION_INSTRUCTIONS_v2.md` following the simplified structure
2. Extract source pages to images (if not done)
3. Create 3 "golden example" complete page translations
4. Test with a single agent before parallel deployment
5. Separate parallel protocol to different document

---

*Analysis completed: 2026-01-09*
