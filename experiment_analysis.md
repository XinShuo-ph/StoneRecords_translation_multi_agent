# Experiment Analysis: 16-Agent Parallel Translation Run

**Date**: 2026-01-03
**Branches analyzed**: 16 most recent `cursor/hong-lou-meng-translation-*` branches (sorted by commit time)
**Analysis date**: 2026-02-12

---

## Summary Statistics

| Worker | Translation Files | Total Segments | Commits | Issues Found |
|--------|----------------:|---------------:|--------:|-------------:|
| 1c3a   | 34              | 153            | 95      | 68           |
| d4d0   | 26              | 89             | 79      | 76           |
| 27e6   | 16              | 69             | 39      | 32           |
| 0dac   | 13              | 62             | 47      | 26           |
| ebba   | 9               | 100            | 33      | 25           |
| 914c   | 8               | 28             | 27      | 16           |
| 40bc   | 7               | 69             | 49      | 14           |
| c2f1   | 6               | 27             | 32      | 12           |
| 7748   | 6               | 22             | 30      | 12           |
| 14dc   | 4               | 21             | 18      | 8            |
| be3d   | 3               | 36             | 29      | 6            |
| f603   | 2               | 5              | 2       | 4            |
| 54a8   | 2               | 7              | 2       | 4            |
| 5648   | 1               | 3              | 2       | 2            |
| 843e   | 1               | 3              | 2       | 2            |
| a535   | 0               | 0              | 5       | 0            |

**Total files produced**: 138 (across all workers; many are duplicates of the same pages)
**Workers producing zero output**: 1 (a535 — stuck in research/claiming phase)
**Workers producing only 1-2 files**: 4 (f603, 54a8, 5648, 843e)

---

## Root Cause Analysis

### Problem 1: Instructions Too Large and Conflated

The `instructions.md` on experiment branches was ~500+ lines, mixing three completely separate concerns:
- **Translation task** (what to translate, how, format)
- **Parallel protocol** (sync daemon, worker states, claiming, heartbeats)
- **Git operations** (commit message formats, push conventions)

**Impact**: Agents spend significant context window on protocol overhead. The instructions contained multiple conflicting sections (e.g., "Continuous Execution" vs. "Sync every 2-3 minutes"). The best performer (1c3a, 34 files) had 95 commits but only 34 were actual translations — the other 61 were heartbeat/sync overhead.

### Problem 2: Protocol Overhead Drowning Out Translation Work

Each agent was required to:
1. Start a sync daemon (that doesn't exist as a real tool)
2. Create WORKER_STATE.md
3. Fetch all branches every 2-3 minutes
4. Update heartbeats every 5 minutes
5. Read other workers' states
6. Run pre-claim checks
7. Use specific commit message formats

The weakest performers (f603, 5648, 843e, 54a8 — only 1-2 files each) had only 2 commits each, suggesting they spent their entire context trying to set up the protocol rather than translating.

Worker a535 produced zero translations despite 5 commits — all heartbeat updates. It was stuck in the "research" phase of page 20, never reaching actual translation.

### Problem 3: Wrong Page Content

**Page 44 conflict**: Branch 1c3a says Chapter 1 (好了歌/Won-Done Song) while 5 other branches say Chapter 3 (Daiyu arriving at Rong Mansion — 过插屏，小小三间内厅). These are clearly completely different content. One set of agents is reading the wrong page.

**Page 21 conflict**: Branch 1c3a starts with "恰近日这神瑛侍者凡心偶炽" (the Divine Luminescent Stone Attendant) while all other branches start with "年为一世。三劫者" (the monk's farewell). These are from different parts of the text.

**Root cause**: No verification mechanism. Agents may be reading extracted text from wrong pages, or the PDF page numbering doesn't match the source_pages/ numbering. Without a ground truth check, agents can't validate they're translating the right content.

### Problem 4: JSON Format Inconsistencies

The format requirements were contradictory across different sources:

| Source | Notes Field | Extra Required Fields |
|--------|------------|----------------------|
| `instructions.md` (main) | `notes` | none |
| Example `page_0020.json` | `notes` | none |
| `validate_json.py` | `translator_notes` | `total_segments` |
| `instructions.md` (branches) | mentions both | `page_content_type` |
| Actual agent output | `translator_notes`, `research_notes` | `characters_appearing`, `manuscript_sources_on_page`, etc. |

**Result**: Every single file across all 16 branches is missing the `notes` key (the one the example uses). Agents invented their own field names like `translator_notes` and `research_notes` because the branch instructions emphasized those terms.

### Problem 5: Inconsistent Segment Granularity

The same page translated by different agents has wildly different segment counts:

| Page | Worker | Segments |
|------|--------|----------|
| 21   | 1c3a   | 4        |
| 21   | 914c   | 3        |
| 21   | 27e6   | 6        |
| 21   | 40bc   | 9        |
| 21   | be3d   | 13       |
| 21   | ebba   | 15       |
| 34   | d4d0   | 4        |
| 34   | be3d   | 12       |
| 34   | ebba   | 12       |
| 34   | 914c   | 6        |

**Root cause**: No clear guidance on what constitutes a "segment". Some agents treat each sentence as a segment, others group multiple sentences into one. Neither approach is wrong per se, but the inconsistency makes the output unusable for assembly.

### Problem 6: Missing Commentary Field

Some segments across branches are missing the `commentary` array entirely (not even an empty `[]`). The instructions said "empty `[]` if none" but agents sometimes omitted it. This breaks downstream processing.

### Problem 7: Agents Hallucinating OCR Content

Several branches show signs of agents "reading" the PDF page but getting garbled text:
- Branch 914c page 21: "车驾一世" (should be "年为一世")
- Branch c2f1 page 21: "年方一世，三者，惟以九十春言之" (garbled)
- Branch 7748 page 21: "太虚幻境甘" (should be "太虚幻境销号")

**Root cause**: Agents reading page images with OCR inaccuracies and not cross-checking. Classical Chinese characters are frequently misread by OCR, and agents don't have a reliable text extraction path.

---

## Key Recommendations

1. **Completely separate translation instructions from parallel protocol.** The instructions.md should contain ONLY the translation task — what to translate, the output format, quality guidelines. No mention of workers, syncing, claiming, heartbeats, or git operations.

2. **Fix the JSON schema.** Make the validator, the example, and the instructions all agree on exactly the same field names and requirements. Eliminate ambiguity.

3. **Provide clear segmentation rules.** Define what a "segment" is: a natural paragraph or verse unit. Give explicit guidance on granularity.

4. **Include extracted text as ground truth.** If agents are reading images and hallucinating characters, provide authoritative text extraction alongside the images so agents can cross-reference.

5. **Simplify the example.** The example should exactly match the required format with no extra fields, demonstrating every required feature.

6. **Add a self-validation step.** Agents should validate their own JSON before committing, using the same validator.

7. **Reduce the number of fields.** Eliminate optional/extra fields that confuse agents. Keep the schema minimal and strict.
