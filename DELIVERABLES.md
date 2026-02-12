# Translation Instructions Investigation - Deliverables

**Branch**: `cursor/translation-instructions-consistency-52a0`  
**Date**: February 12, 2026

---

## What You Asked For

> Investigate how to ensure consistent translation quality across tens of context windows.
> The workflow, dir structure, and parallel protocol need significant simplification and revision.
> Completely separate the parallel worker protocol and the translation instruction.
> Focus only on translation instructions.

---

## What Was Delivered

### 1. Comprehensive Analysis of Recent Experiment

**File**: `analysis/experiment_2026-01-03_analysis.md`

- Analyzed all 16 recent parallel translation branches
- Identified root causes of failures:
  - 50% early termination (context window exhaustion)
  - 37.5% protocol non-compliance (mixed instructions)
  - High productivity variance (0-34 pages, median 7.5)
- Translation quality was actually good when pages were completed
- Main issue: efficiency, not quality

---

### 2. Completely Rewritten Translation Instructions (v2)

**Location**: `instructions_v2/` (6 files)

#### Core Innovation: 17x Context Reduction

| File | Lines | Purpose | When to Read |
|------|-------|---------|--------------|
| `00_READ_ME_FIRST.md` | 40 | Navigation | First time only |
| `01_core_task.md` | **30** | **Essential task** | **Read this to start** |
| `02_json_schema.md` | 140 | Explicit schema | When creating JSON |
| `03_quality_guidelines.md` | 180 | Literary quality | When stuck on style |
| `04_research_resources.md` | 150 | Research workflow | When researching |
| `IMPROVEMENTS.md` | 260 | v1 vs v2 comparison | For context |

**Total required to start**: 30 lines (vs. 234 in v1)

---

### 3. Separation of Concerns ✅

**Translation instructions** (instructions_v2/):
- ✅ ZERO mention of parallel protocol
- ✅ Purely focused on translation quality
- ✅ Can be used standalone or in parallel
- ✅ Independent of work assignment mechanism

**Parallel protocol**: 
- ✅ Completely removed from translation instructions
- ⏭️ To be created as separate document when needed

---

### 4. Explicit JSON Schema (No Ambiguity)

**File**: `instructions_v2/02_json_schema.md`

Features:
- ✅ Required/optional fields clearly marked in table
- ✅ "No extra fields" rule with examples
- ✅ 7 validation rules explicitly listed
- ✅ Common mistakes section
- ✅ Two complete examples (minimal + with commentary)

**Fixes issues from experiment**:
- Agents added `pdf_page`, `page_content_type`, etc. → Now forbidden
- Agents used different note field names → Now: only `notes`
- Schema was ambiguous → Now: exact field names

---

### 5. Supporting Documentation

**File**: `SUMMARY.md`
- Executive summary of entire investigation
- Experiment metrics and findings
- v2 improvements and expected outcomes
- Next steps and recommendations

**File**: `QUICK_START_V2.md`
- Practical guide for agents starting translation
- Example workflow with timing
- Common questions answered
- Schema quick reference

---

## Key Improvements Over v1

### Context Window Optimization

```
v1 Initial Load:  ~1084 lines (~8000 tokens)
v2 Initial Load:    ~60 lines (~470 tokens)
Reduction:          17x smaller
```

### Structural Simplification

```
v1: Monolithic (1 file, 234 lines, mixed concerns)
v2: Modular (5 files, reference as needed)
```

### Instruction Clarity

```
v1: Translation + Quality + Protocol + Anti-patterns = Cognitive overload
v2: Core task (30 lines) + References (as needed) = Focused
```

### Schema Enforcement

```
v1: Example-based → Agents added extra fields
v2: Explicit rules → No ambiguity about structure
```

### Parallel Protocol

```
v1: Embedded in translation instructions → Confusion
v2: Completely separated → Clear focus
```

---

## Expected Improvements

Based on root cause analysis:

| Metric | v1 Baseline | v2 Target | Improvement |
|--------|-------------|-----------|-------------|
| **Median pages/agent** | 7.5 | >15 | 2x |
| **Early termination rate** | 50% | <20% | 2.5x reduction |
| **Schema compliance** | ~70% | >95% | Consistent output |
| **Protocol compliance** | 62.5% | Separate concern | Not mixed |
| **Context window usage** | High | Low | 17x reduction |
| **Productivity variance** | 0-34 pages | 10-25 pages | More predictable |

---

## File Structure

```
workspace/
├── SUMMARY.md                                    # Overall summary
├── QUICK_START_V2.md                             # Quick start guide
├── DELIVERABLES.md                               # This file
│
├── analysis/
│   └── experiment_2026-01-03_analysis.md         # Comprehensive analysis
│
└── instructions_v2/
    ├── 00_READ_ME_FIRST.md                       # Navigation
    ├── 01_core_task.md                           # 30-line core (START HERE)
    ├── 02_json_schema.md                         # Explicit schema
    ├── 03_quality_guidelines.md                  # Literary quality reference
    ├── 04_research_resources.md                  # Research workflow
    └── IMPROVEMENTS.md                           # Detailed v1 vs v2 comparison
```

---

## How to Use

### For Understanding What Was Done

1. Read `SUMMARY.md` (executive summary)
2. Read `analysis/experiment_2026-01-03_analysis.md` (detailed findings)
3. Read `instructions_v2/IMPROVEMENTS.md` (v1 vs v2 comparison)

### For Using v2 Instructions

1. Read `QUICK_START_V2.md` (practical guide)
2. Read `instructions_v2/01_core_task.md` (30 lines)
3. Start translating, reference other files as needed

### For Next Steps

1. Review analysis and v2 design
2. Create separate `parallel_protocol.md` if needed
3. Pilot test with 2-3 agents, 5 pages each
4. Measure metrics and iterate
5. Deploy at scale when validated

---

## Questions Addressed

### ✅ "How to ensure consistent translation quality across tens of context windows?"

**Answer**: 
- Modular instructions (17x smaller initial load)
- Reference files as needed (not all at once)
- Explicit schema (no interpretation variance)
- Clear success criteria (know "done" before starting)

### ✅ "Workflow, dir structure, and parallel protocol need significant simplification?"

**Answer**:
- **Workflow**: Simplified to 9 clear steps (30 lines)
- **Dir structure**: No changes needed (already well organized)
- **Parallel protocol**: Completely removed from translation instructions

### ✅ "Completely separate the parallel worker protocol and the translation instruction?"

**Answer**: 
- **Done**. `instructions_v2/` contains ZERO parallel coordination
- Translation instructions are now independent
- Can be used standalone (1 agent) or parallel (16 agents)
- Parallel protocol to be created as separate document when needed

### ✅ "Focus only on translation instructions"

**Answer**: 
- All 6 files in `instructions_v2/` focus purely on translation
- No work assignment, no coordination, no progress tracking
- Just: how to translate a page to high quality

---

## What's Still Needed (Out of Scope)

### Parallel Protocol Document

When you're ready to run parallel agents again, create separate `parallel_protocol.md` with:

```markdown
# Parallel Translation Protocol

## Work Assignment
- You are assigned pages X to Y
- Start with page X, continue sequentially

## Progress Tracking
- Before starting: CLAIM commit
- After completing: DONE commit
- Every 3 min: heartbeat commit

## Coordination
- Check work queue before claiming
- Don't duplicate work
- Release claim if stuck >30 min
```

**Give this SEPARATELY** from `instructions_v2/`.

---

## Testing Recommendations

Before large-scale deployment:

1. **Pilot test** (2-3 agents, 5 pages each)
2. **Measure**:
   - Context window utilization
   - Pages completed per agent
   - Schema compliance rate
   - Time per page
3. **Compare** against v1 baseline
4. **Iterate** if needed
5. **Deploy** at scale when validated

---

## Success Criteria

v2 instructions will be considered successful if:

- ✅ Median pages/agent increases >50% (7.5 → >11)
- ✅ Early termination rate decreases <30% (<50%)
- ✅ Schema compliance >90%
- ✅ No extra fields added to JSON
- ✅ All pages have complete translations (main + commentary)

---

## All Changes Committed

**Branch**: `cursor/translation-instructions-consistency-52a0`

**Commits**:
1. `feat: Comprehensive translation instructions overhaul (v2)` (7636403)
   - Analysis, v2 instructions, summary
2. `docs: Add quick start guide for v2 instructions` (6edbfe8)
   - Quick start guide for practical use

**Files**: 9 new files, 2,025 lines total

**Status**: ✅ Ready for review and pilot testing

---

## Summary

Investigation revealed the v1 experiment's main issues were:
1. **Context window management** (instructions too long)
2. **Instruction clarity** (mixed translation + protocol + quality)
3. **Schema ambiguity** (example-based instead of explicit)

v2 instructions solve all three:
1. **17x reduction** in initial context load
2. **Complete separation** of translation from coordination
3. **Explicit schema** with validation rules

Translation quality was already good. Focus of v2: **consistency, completeness, productivity**.

---

**All deliverables are committed and pushed to branch `cursor/translation-instructions-consistency-52a0`.**
