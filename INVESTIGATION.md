# Parallel Translation Experiment — Investigation Findings

**Date**: 2026-01-03 experiment, analyzed 2026-02-12

## Experiment Setup

- 32 `hong-lou-meng-translation-*` branches total (two batches)
- 16 most recent branches = the parallel experiment analyzed here
- Branches sorted by most recent commit time (UTC Jan 3, 2026 ~03:15–04:15)

## Summary of Results

| Branch | Translation Files | Total Commits | Heartbeat Commits | Actual Work Commits |
|--------|-------------------|---------------|--------------------|--------------------|
| d4d0   | 26                | 79            | 56                 | 23                 |
| 1c3a   | 34                | 95            | 92                 | 3                  |
| 27e6   | 16                | 39            | 33                 | 6                  |
| 40bc   | 7                 | 49            | 43                 | 6                  |
| 0dac   | 13                | 47            | 40                 | 7                  |
| c2f1   | 6                 | 32            | 29                 | 3                  |
| 914c   | 8                 | 27            | 24                 | 3                  |
| be3d   | 4                 | 29            | 26                 | 3                  |
| 7748   | 7                 | 30            | 27                 | 3                  |
| ebba   | 9                 | 33            | 32                 | 1                  |
| f603   | 2                 | 2             | 0                  | 2                  |
| 5648   | 1                 | 2             | 0                  | 2                  |
| 843e   | 1                 | 2             | 0                  | 2                  |
| 54a8   | 2                 | 2             | 0                  | 2                  |
| 14dc   | 4                 | 18            | 18                 | 0                  |
| a535   | 0                 | 5             | 5                  | 0                  |

**Total translations produced**: ~140 files across 16 branches (with heavy duplication)

**Agents that produced nothing or almost nothing**: a535 (0 files), 5648 (1), 843e (1), 54a8 (2), f603 (2), be3d (4)

**Most productive agents**: 1c3a (34 files), d4d0 (26 files), 27e6 (16 files), 0dac (13 files)

---

## Problem 1: Protocol Overhead Dominated Agent Time

The parallel sync protocol consumed the vast majority of agent activity:

- **1c3a**: 92 of 95 commits were heartbeat/sync. Only 3 actual work commits.
- **14dc**: 18 commits, ALL heartbeat. 0 actual work commits.
- **a535**: 5 commits, ALL heartbeat. Produced 0 translation files.
- Average: **~80% of commits were protocol overhead**, not translation work.

The protocol instructed agents to:
1. Start a `sync_daemon.py` that didn't exist as runnable code
2. Create and update `WORKER_STATE.md` every few minutes
3. Run heartbeat commits every 3 minutes
4. Maintain `GLOBAL_PROGRESS.md`, `PROTOCOL.md`, `SYNC_SERVICE.md`, `ISSUES_REPORT.md`

**Root cause**: The protocol was too complex. Agents spent their context window on protocol mechanics instead of translation. The heartbeat loop (commit every 3 minutes with a timestamp) consumed most of the conversation turns.

**Fix**: Remove all protocol machinery from the translation instructions. The parallel coordination protocol must be a completely separate concern.

---

## Problem 2: Wrong Pages Translated

Multiple agents translated the wrong content for a given page number:

- **d4d0 page 20**: Contains "偏值士隐走来听见..." (甄士隐 and 贾雨村 scene — this is NOT page 20)
- **1c3a page 20**: Contains "那僧笑道：'此事说来好笑...'" (monk/Taoist origin story — also NOT page 20)
- **Actual page 20** (`source_pages/page_0020.png`): Contains "士隐意欲也跟了过去..." (matching the example)

**Root cause**: The PDF has printed page numbers at the bottom of each page that differ from the physical PDF page number. Page `source_pages/page_0020.png` shows printed number "11" at the bottom. Agents confused these two numbering systems.

**Fix**: The instructions now explicitly explain the page numbering system and state that the `page_XXXX.png` filename number is the PDF page number to use, not the number printed on the page.

---

## Problem 3: Wildly Inconsistent Segmentation

The same page (page 21) was segmented into anywhere from 3 to 15 segments:

| Branch | Segments for page 21 |
|--------|---------------------|
| 914c   | 3 segments          |
| c2f1   | 6 segments          |
| 7748   | 7 segments          |
| 14dc   | 8 segments          |
| 40bc   | 9 segments          |
| be3d   | 13 segments         |
| ebba   | 15 segments         |

**Root cause**: The instructions did not define what constitutes a "segment". Some agents treated each sentence as a segment; others used paragraphs. Some agents only translated a few sentences from the page (explaining the low segment counts).

**Fix**: The instructions now define segmentation rules clearly: follow paragraph structure, keep dialogue with its narration tag, keep complete poems together.

---

## Problem 4: JSON Format Inconsistency

The instructions defined one format, but agents used a different one:

| Field | Instructions said | Agents actually used |
|-------|-------------------|---------------------|
| Research notes | `notes` | `translator_notes` + `research_notes` |
| Commentary source | `source` | `type` + `source` |
| N/A | not defined | `chapter_title`, `page_content_type`, `characters_appearing`, `manuscript_sources_on_page`, `total_segments`, `pdf_page` on segments |

**Root cause**: The `validate_json.py` validator expected fields (`translator_notes`, `total_segments`, commentary `type`) that contradicted `instructions.md`. The instructions on the agent branches had been modified to include protocol-related fields. The agents followed the mutated instructions on their branch rather than the original format.

**Fix**: 
1. The instructions now have a definitive field list with an explicit "What NOT to include" section listing every extra field agents historically added.
2. The validator now strictly checks for exactly the defined fields and reports unexpected fields as errors.
3. The example `page_0020.json` exactly matches the specification.

---

## Problem 5: Incomplete Translations

Many translation files only contained a few sentences from the page instead of the full page content:

- 914c translated page 21 into only 3 segments (should be 7-9 based on the page content)
- Several branches produced segments with very short `original` text
- Commentary annotations were frequently skipped entirely

**Root cause**: Agents ran out of context window or conversation turns due to protocol overhead. With 80%+ of turns consumed by heartbeats and sync operations, little room remained for actual translation work.

**Fix**: By removing protocol overhead from the translation instructions, agents can devote their full capacity to translation. The instructions now emphasize completeness with a checklist: "ALL visible text on the page is included in segments."

---

## Problem 6: OCR / Transcription Errors

Some agents produced garbled `original` text:

- **c2f1**: Mixed commentary markers into the main text: `"忽见壁間【喻問】"幻境"二字就細檢"` (nonsensical)
- **7748**: Transcription errors: `"忽见隐壁"` should be `"忽见隔壁"`, stray characters

**Root cause**: Agents attempted to read from both the PDF and images, sometimes misreading characters or confusing commentary annotations with main text. The pre-extracted page images (`source_pages/`) were only available for the first 25 pages. Beyond that, agents had to extract from the PDF directly.

**Fix**: 
1. Instructions now explicitly state: "Commentary markers like【甲戌】belong in the commentary objects, not in the `original` field of the segment."
2. More source pages should be pre-extracted before the next run.
3. Future consideration: provide extracted text alongside images for verification.

---

## Problem 7: Many Agents Stopped Early

Several agents produced only 1-2 translations before stopping:

- f603: 2 files then stopped
- 5648: 1 file then stopped
- 843e: 1 file then stopped
- 54a8: 2 files then stopped
- a535: 0 files (only protocol setup)

**Root cause**: Multiple factors:
1. Protocol setup consumed initial turns
2. Some agents may have encountered errors (e.g., sync daemon not found)
3. Complex instructions led to confusion and early termination
4. No simple "just start translating" path — agents had to set up infrastructure first

**Fix**: The simplified instructions have a straightforward workflow: Read → Research → Segment → Translate → Polish → Save → Next Page. No setup steps, no daemon, no state files.

---

## Problem 8: Massive Duplication of Work

Many agents translated the same pages:

- Page 20: translated by at least 6 branches (d4d0, 1c3a, 27e6, 0dac, f603, 54a8)
- Page 21: translated by at least 7 branches
- Page 34: translated by at least 6 branches
- Page 44: translated by at least 5 branches

**Root cause**: The sync mechanism didn't work. The sync daemon referenced in PROTOCOL.md didn't exist as actual runnable code. Agents couldn't check what others had already done.

**Fix**: This is a parallel coordination problem, not a translation instruction problem. The fix belongs in the parallel worker protocol (separate document, not addressed here). But the severity is reduced when each agent's translation quality is high — even duplicate work is useful if the quality is good enough to compare and merge.

---

## Structural Changes Made

### instructions.md (completely rewritten)

Key changes:
1. **Removed all protocol/coordination content** — no WORKER_STATE, no sync daemon, no heartbeat, no branch communication
2. **Added explicit page numbering explanation** with concrete example
3. **Defined segmentation rules** (follow paragraphs, keep dialogue together, poems as single units)
4. **Defined exact JSON schema** with "What NOT to include" section
5. **Added common mistakes table** with every observed failure mode
6. **Simplified workflow** to 7 concrete steps
7. **Added pre-save checklist** covering all observed errors

### validate_json.py (rewritten)

Key changes:
1. **Strict field validation**: reports both missing AND unexpected fields
2. **Matches instructions.md exactly**: uses `notes` (not `translator_notes`), commentary has `source` (not `type`)
3. **No optional fields**: every field listed in instructions is required, nothing else is allowed

### examples/page_0020.json (fixed)

- Fixed invalid JSON (unescaped ASCII quotes in Chinese text replaced with Unicode curly quotes)
- Format already matched the specification, no structural changes needed

---

## Recommendations for Next Experiment

1. **Pre-extract more source pages**: Currently only pages 1-25 are pre-extracted. Extract at least pages 1-100 before the next run.

2. **Assign specific pages per agent**: Instead of relying on dynamic claiming, give each agent a static page range in its task description. E.g., "Translate pages 20-25" as part of the task prompt. This eliminates coordination overhead entirely.

3. **Run the validator in agent instructions**: Tell agents to run `python3 tools/validate_json.py translations/page_XXXX.json` after each page to catch format errors immediately.

4. **Reduce scope per agent**: Rather than expecting agents to translate many pages, assign 3-5 pages per agent and focus on quality. An agent that produces 3 perfect pages is more valuable than one that produces 15 incomplete ones.

5. **Test with a single agent first**: Before running 16 agents in parallel, verify that one agent can follow the instructions correctly and produce a valid, complete translation of 2-3 pages.

6. **Separate parallel protocol completely**: The coordination mechanism (how agents discover each other, claim work, avoid duplication) should be a separate system that is injected into the agent's environment, not embedded in translation instructions. The agent should receive: "Translate pages X, Y, Z" and not need to worry about coordination.
