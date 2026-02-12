# Experiment Analysis: 16-Agent Parallel Translation (Jan 3, 2026)

## Setup

16 parallel Cursor agents on branches `cursor/hong-lou-meng-translation-{suffix}`, sorted by last commit time (most recent first):

| Agent | Commits | Heartbeats | Actual Work | Translation Files |
|-------|---------|------------|-------------|-------------------|
| d4d0  | 79      | 24 (30%)   | 55          | 26                |
| 1c3a  | 95      | 24 (25%)   | 71          | 34                |
| 27e6  | 39      | 23 (59%)   | 16          | 16                |
| 40bc  | 49      | 32 (65%)   | 17          | 7                 |
| 0dac  | 47      | 19 (40%)   | 28          | 13                |
| c2f1  | 32      | 16 (50%)   | 16          | 6                 |
| 914c  | 27      | 15 (56%)   | 12          | 8                 |
| be3d  | 29      | 15 (52%)   | 14          | 4                 |
| 7748  | 30      | 13 (43%)   | 17          | 7                 |
| ebba  | 33      | 13 (39%)   | 20          | 9                 |
| f603  | 2       | 0          | 2           | 2                 |
| 5648  | 2       | 0          | 2           | 1                 |
| 843e  | 2       | 0          | 2           | 1                 |
| 54a8  | 2       | 0          | 2           | 2                 |
| 14dc  | 18      | 9 (50%)    | 9           | 4                 |
| a535  | 5       | 4 (80%)    | 1           | **0**             |

**Total translation files: ~140** (with substantial duplication)
**Unique pages translated: ~45** (of 25 available source pages)

---

## Critical Findings

### 1. Wrong Page Content (Agents Not Reading Actual PDF Pages)

Multiple agents produced translations that don't match the actual PDF page content:

- **1c3a** (the highest output agent): Its "page 20" starts with 那僧笑道 and 绛珠草 content, which is from much earlier in Chapter 1 — NOT what's on PDF page 20. Its "page 44" claims Chapter 第一回, while every other agent correctly identifies it as 第三回.
- **d4d0** (second highest output): Its "page 20" starts with 雨村兄 content (Jia Yucun's conversation), which is also NOT what's on PDF page 20.
- The actual PDF page 20 starts with 士隐意欲也跟了过去 (confirmed by viewing page_0020.png and matching with example).

**Root cause**: Agents were generating content from their training knowledge of Hong Lou Meng rather than reading the actual page images. The complex protocol setup consumed their early attention, and once they started "translating," they may have stopped consulting the source material.

### 2. Massive Protocol Overhead

The protocol infrastructure consumed enormous agent attention:

| File | Size | Purpose |
|------|------|---------|
| instructions.md | 31,862 bytes (bloated from 6,536) | Merged with protocol |
| PROTOCOL.md | 14,754 bytes | Sync protocol |
| SYNC_SERVICE.md | 11,083 bytes | Sync daemon docs |
| WORKER_STATE.md | 3,067 bytes | Worker status |
| WORKER_STATE_TEMPLATE.md | 4,349 bytes | Template |
| GLOBAL_PROGRESS.md | 6,141 bytes | Global tracker |
| STATE.md | 6,014 bytes | State file |
| ISSUES_REPORT.md | 6,940 bytes | Issues |
| **Total overhead** | **~84 KB** | Protocol docs |

The instructions file grew from 6.5KB to 31.8KB — nearly 5x — by absorbing protocol information. This diluted the actual translation guidance.

### 3. Heartbeat Spam

Between 25-80% of all commits were AUTO-SYNC heartbeat commits containing no translation work:
- **a535**: 4 of 5 commits (80%) were heartbeats. Produced ZERO translations.
- **40bc**: 32 of 49 commits (65%) were heartbeats. Only 7 translations.
- **27e6**: 23 of 39 commits (59%) were heartbeats.

The sync daemon and heartbeat system consumed computational effort that should have been spent translating.

### 4. Early Stop / Minimal Output

6 of 16 agents (37.5%) produced 0-2 translation files:
- **a535**: 0 files (never started translating)
- **f603, 5648, 843e, 54a8**: 1-2 files each (stopped almost immediately)
- **14dc**: 4 files only

### 5. Notes Field Universally Missing

Every single translation across all 16 agents is missing the `notes` field. This was a required field meant to contain research findings, cultural context, and pun explanations. No agent performed any documented research.

### 6. Inconsistent Segmentation

The same PDF page produced wildly different segment counts across agents:

| Page | Agent Segment Counts |
|------|---------------------|
| 20   | 4, 4, 6, 6, 3, 4 (range: 3-6, example has 7) |
| 21   | 4, 6, 3, 13, 7, 15 (range: 3-15!) |
| 34   | 4, 6, 5, 12, 4, 12 (range: 4-12) |

Agents ebba and be3d over-segmented (12-15 segments per page), while many others under-segmented (2-4 segments). The original character counts also varied dramatically.

### 7. Missing Commentary Fields

Multiple agents omitted the `commentary` array from segments, or produced segments with missing required fields. Example: ebba's page_0021 had 15 segments but 5 were missing the `commentary` key entirely.

### 8. Invalid JSON

- d4d0's page_0022.json has a JSON parse error (missing comma/delimiter).
- The EXAMPLE file (examples/page_0020.json) itself contains invalid JSON — unescaped ASCII double quotes inside Chinese text on line 61: `"所谓"万境都如梦境看"也。"`. Agents copying this pattern would produce broken JSON.

### 9. Duplicate Work

Despite the elaborate sync protocol meant to prevent duplication:
- Page 20 was translated by at least 6 agents
- Page 21 was translated by at least 8 agents
- Page 34 was translated by at least 7 agents
- Page 44 was translated by at least 6 agents

### 10. Short/Incomplete Translations

Many agents produced very little original text per page:
- 1c3a averaged ~180 original characters per page (some pages contain 500+ chars)
- 914c had pages with only 2 segments and 115-373 original characters
- d4d0 averaged ~220 original characters per page

The example page_0020.json contains 463 original characters across 7 segments. Most agents captured less than half the text on each page.

---

## Root Cause Analysis

### Primary: Protocol Overwhelmed Translation

The complex parallel coordination protocol (sync daemons, heartbeat systems, worker states, global progress tracking, auto-sync commits) consumed the majority of agent attention and context window. Agents spent their cognitive budget on infrastructure rather than the actual translation task.

### Secondary: Instructions Were Diluted

By merging protocol instructions into the translation instructions, the actual guidance on *how to translate* was buried in a 31KB document dominated by sync mechanics. The core message — "read the page image, translate everything on it, produce valid JSON" — was lost.

### Tertiary: Example File Was Broken

The example JSON file contains invalid JSON (unescaped quotes), meaning agents had no valid reference for the output format.

### Quaternary: No Enforcement of Page Verification

Nothing forced agents to verify their translations matched the actual page content. Agents that generated from memory rather than reading the source weren't caught.

---

## Recommendations

1. **Completely separate** translation instructions from parallel protocol
2. **Simplify** instructions to under 300 lines focused purely on translation
3. **Fix** the example JSON to be valid and well-formatted
4. **Add page-content verification** steps (e.g., "the first line of text on this page should match segment 1's original")
5. **Remove all protocol infrastructure** from the instructions (no heartbeats, no sync daemons, no worker states)
6. **Strengthen** format specification with explicit rules about Chinese quotes in JSON
7. **Make notes mandatory** with specific prompts for what to include
8. **Simplify validation** tool to match actual schema
