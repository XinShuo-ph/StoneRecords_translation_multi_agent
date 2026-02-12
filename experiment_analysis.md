# Parallel Translation Experiment Analysis

Analysis of the 16-agent parallel translation experiment (Jan 3, 2026).

---

## Experiment Setup

- 32 branches total (`cursor/hong-lou-meng-translation-XXXX`)
- 16 branches with recent commits represent the parallel experiment
- Each agent was assigned to translate pages from 红楼梦脂评汇校本

## Results Summary

| Branch | Translation Files | Notes |
|--------|-------------------|-------|
| 1c3a | 34 | Best output volume |
| d4d0 | 26 | Good volume but segments thin toward end |
| 27e6 | 16 | Sequential pages 20-35, decent quality |
| 0dac | 13 | Scattered pages |
| ebba | 9 | Completed 9 then declared SESSION_END |
| 914c | 8 | |
| 7748 | 7 | **Contains placeholder text** |
| 40bc | 7 | |
| c2f1 | 6 | |
| 14dc | 4 | |
| be3d | 3 | |
| 54a8 | 2 | |
| f603 | 2 | |
| 5648 | 1 | |
| 843e | 1 | |
| a535 | 0 | **Produced zero translations** (stuck in "research" phase) |

**Total unique translation files across all 16 agents**: ~137
**Agents that produced 0-2 files**: 5 out of 16 (31%)

---

## Failure Patterns Identified

### 1. Placeholder/Summary Text Instead of Actual Translation

Branch `7748`, page 47:
```json
"original": "[Dialogue between family members discussing arrangements and interactions]"
```
This is a description of what should be on the page, not the actual text. The agent never read the actual page content.

### 2. Inconsistent JSON Schema

At least 4 different schema variants were used across agents:
- Some use `"notes"` (per old example), others use `"translator_notes"`
- Some add `"chapter_title"`, `"page_content_type"`, `"characters_appearing"`, `"research_notes"`, `"manuscript_sources_on_page"` — none of which are in the official schema
- Some put `"total_segments"` in the output, others omit it
- Commentary format varies: `"source": "脂批"` vs `"source": "甲戌本"`, `"type"` present vs absent

**Root cause**: The old `instructions.md` example JSON did not match what `validate_json.py` expected. The example used `"notes"` and `"source": "脂批"` for commentary, while the validator expected `"translator_notes"`, `"total_segments"`, and commentary with `"type"` + `"source"` (manuscript).

### 3. Low Segment Counts (Incomplete Page Coverage)

Many pages from later in agent sessions have only 1-3 segments. The example page (page 20) has 7 segments. Pages in the novel typically have 3-8 segments of content. A page with only 2 segments is almost certainly missing content.

Branch `d4d0` progression:
- Early pages: 4-5 segments each
- Later pages (62+): only 2-3 segments each

This suggests agents got fatigued or started rushing.

### 4. Agents That Produced Nothing

Branch `a535` spent its entire session in "research" and "claiming" phases without ever producing a translation file. Its WORKER_STATE.md shows it claimed page 20 but never completed it.

### 5. Massive Protocol Overhead

The parallel coordination consumed significant agent attention:
- WORKER_STATE.md management
- GLOBAL_PROGRESS.md updates
- Heartbeat commits (every ~180 seconds)
- Sync daemon operation
- Page claiming/verification logic

Many branches have 30-80+ commits, but most are heartbeat/sync commits, not translation work. For example, `a535` has 14 commits and 0 translations — all commits are protocol overhead.

### 6. Duplicate Work

Multiple agents translated the same pages. For instance, page 20, 21, 34, and 44 were each translated by 5+ agents independently. The "claiming" protocol was supposed to prevent this but clearly failed.

### 7. Early Session Termination

Branch `ebba` explicitly declared `SESSION_END` after 9 pages. Multiple other branches show only initial commits, suggesting the agent conversation ended prematurely.

---

## Root Causes

1. **Format ambiguity**: The example, the instructions, and the validator were inconsistent with each other, so agents guessed differently.

2. **Protocol overload**: The parallel coordination protocol (heartbeats, sync daemons, claiming, worker state) dominated agent attention instead of translation.

3. **No validation enforcement**: No step in the workflow required agents to run `validate_json.py` before committing. Format errors were never caught.

4. **No content verification**: No mechanism to verify that the "original" field actually contains text from the correct PDF page. Agents could hallucinate or use placeholders.

5. **Combined instructions**: Translation task + parallel protocol in the same context confused agents about priorities.

---

## Changes Made

### New `translation_instructions.md`

A completely rewritten, self-contained translation instruction document that:

1. **Strict JSON schema**: Every field defined with type, valid values, and examples. No ambiguity.
2. **Explicit anti-patterns**: Section 5 lists every observed failure with concrete WRONG/RIGHT examples.
3. **Separated from parallel protocol**: Contains zero references to worker state, heartbeats, sync daemons, or coordination.
4. **Aligned example**: `examples/page_0020.json` now exactly matches the schema.
5. **Aligned validator**: `tools/validate_json.py` now enforces the exact same schema, including:
   - Detects placeholder text in brackets
   - Warns on low segment count
   - Rejects unexpected fields
   - Validates commentary structure

### Key Schema Changes

| Old (ambiguous) | New (strict) |
|-----------------|--------------|
| `"notes"` (from old example) | `"translator_notes"` (array of strings) |
| `"source": "脂批"` (commentary) | `"type": "夹批"` + `"source": "甲戌本"` |
| `total_segments` optional | `total_segments` required, must match |
| Extra fields allowed | Extra fields rejected |
| No `position` in commentary | `position` required |

---

## Recommendations for Next Experiment

1. **Separate protocols completely**: Translation instructions should be injected independently of any parallel coordination protocol.
2. **Pre-validate before commit**: Add a git pre-commit hook or explicit workflow step requiring `validate_json.py` to pass.
3. **Content spot-checks**: Implement automated checks that compare `original` field text against known page content.
4. **Smaller batch sizes**: Instead of assigning many pages to each agent, assign 3-5 pages and verify quality before assigning more.
5. **Reduce coordination overhead**: Simplify the parallel protocol to minimize non-translation commits and agent distraction.
