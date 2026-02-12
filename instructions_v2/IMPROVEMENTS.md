# Improvements Over v1 Instructions

This document explains what changed and why.

---

## Overview: Before and After

| Aspect | v1 (instructions.md) | v2 (instructions_v2/) |
|--------|----------------------|------------------------|
| **Length** | 234 lines, single file | 30 lines core + modular references |
| **Structure** | Monolithic | 5 focused files |
| **Clarity** | Mixed task + quality + protocol | Separated concerns |
| **Schema** | Example-based | Explicit schema with validation rules |
| **Parallel Protocol** | Embedded (Step 6 mentions continuation) | Completely removed |
| **Context Load** | High (all at once) | Low (reference as needed) |

---

## Key Changes

### 1. Drastically Shorter Core Instructions

**v1**: 234 lines including workflow, schema, quality, terminology, anti-patterns, checklist

**v2**: `01_core_task.md` is **30 lines** with only essential task definition

**Benefit**: 
- Faster to read and internalize
- Less context window consumption
- Clearer action items

---

### 2. Modular Structure

**v1**: Single file with everything mixed together

**v2**: Separated into focused modules
- `00_READ_ME_FIRST.md` - Navigation
- `01_core_task.md` - Essential task only
- `02_json_schema.md` - Explicit schema
- `03_quality_guidelines.md` - Reference for style
- `04_research_resources.md` - Research workflow

**Benefit**:
- Read core (30 lines) to start working immediately
- Reference other files only when needed
- Reduces cognitive load

---

### 3. Explicit JSON Schema

**v1**: JSON structure shown by example, field descriptions in table

**v2**: 
- Complete schema with all required/optional fields clearly marked
- Validation rules explicitly listed
- Common mistakes highlighted
- Two examples: minimal and with commentary

**Benefit**:
- No ambiguity about field names
- Clear what's required vs. optional
- Prevents extra fields being added
- Catches common errors

---

### 4. Separated Parallel Protocol

**v1**: Workflow mentions "Continue to next page immediately" and "Continue until assigned pages"

**v2**: **Zero mention** of parallel coordination in translation instructions

**Benefit**:
- Translation quality instructions are independent
- Parallel protocol can be updated without affecting translation guidelines
- Agents focused on translation task, not coordination mechanics

---

### 5. Removed Anti-Patterns Section

**v1**: Had section "Anti-Patterns to Avoid" with 6 items

**v2**: Converted anti-patterns into:
- Explicit requirements in core task
- Validation rules in schema
- Success criteria checklist

**Benefit**:
- Positive framing (do this) instead of negative (don't do that)
- Actionable requirements instead of warnings
- Less cognitive load

---

### 6. Research as Reference, Not Pre-Read

**v1**: "Research before translating" implies reading all research files first

**v2**: `04_research_resources.md` explicitly says:
- "Don't read all files at once"
- "Reference them as needed"
- Provides lookup workflow

**Benefit**:
- Doesn't load all research files into context at once
- Agent references specific sections when encountering specific issues
- Faster startup

---

### 7. Time Budget Guidance

**v1**: No time guidance, just "if stuck for 5 minutes, add note and continue"

**v2**: `04_research_resources.md` includes:
- Budget per page: 45-60 minutes
- Breakdown by activity
- Goal: 1-1.5 pages/hour

**Benefit**:
- Sets productivity expectations
- Helps agents self-monitor
- Prevents over-research paralysis

---

### 8. Clearer Success Criteria

**v1**: Checklist at end with 7 items

**v2**: 
- Success criteria in `01_core_task.md` (6 checkboxes)
- Validation rules in `02_json_schema.md` (7 rules)
- Quality checks in `03_quality_guidelines.md` (7 checks)

Each context has its own relevant criteria.

**Benefit**:
- Know what "done" means before starting
- Relevant checks at each stage
- Easier to verify completeness

---

## Schema Enforcement

### v1 Schema Issues Observed in Experiment

From branch analysis, agents added extra fields not in instructions:
- `pdf_page` (redundant with `page`)
- `page_content_type` (not requested)
- `characters_appearing` (not requested)
- `translator_notes` + `research_notes` (should be just `notes`)
- `total_segments` (redundant, can be counted)
- `manuscript_sources_on_page` (should be in commentary)

### v2 Schema Fixes

`02_json_schema.md` now explicitly states:
- **"No extra fields"** with specific examples of what not to add
- **Required fields table** with exact names
- **Validation rules** listing what will be considered invalid

**Result**: Agents cannot claim they didn't know the schema was strict.

---

## Context Window Optimization

### v1 Context Load (estimated)

```
instructions.md:              234 lines
research/glossary.md:         ~150 lines
research/character_guide.md:  ~200 lines
research/poetry_guide.md:     ~100 lines
research/commentary_guide.md: ~80 lines
research/cultural_context.md: ~180 lines
examples/page_0020.json:      ~140 lines
--------------------------------
TOTAL IF ALL READ:            ~1084 lines (~8000 tokens)
```

### v2 Context Load (minimal start)

```
01_core_task.md:              30 lines (~220 tokens)
02_json_schema.md (header):   30 lines (~250 tokens)
--------------------------------
MINIMUM TO START:             60 lines (~470 tokens)
```

**17x reduction** in initial context load.

Additional files loaded **only when needed**:
- `03_quality_guidelines.md`: Reference for style questions
- `04_research_resources.md`: Lookup when stuck
- `research/*.md`: Specific sections on-demand

**Benefit**: 
- More context budget for actual translation work
- Less chance of hitting context limits early
- Faster agent initialization

---

## Workflow Comparison

### v1 Workflow (from instructions.md)

1. View page
2. Research (read materials in `research/`)
3. Translate (5 steps)
4. 润色 (Polish)
5. Save JSON
6. Next page

**Issues**:
- "Research" step too vague
- "Polish" step not well-defined
- No time budgets
- No clear definition of "done researching"

### v2 Workflow (from 01_core_task.md)

1. **View** the page
2. **Identify** all text types
3. **Research** (with specific lookup approach in 04_research_resources.md)
4. **Segment** (5-15 logical units)
5. **Translate** each segment
6. **Translate** all commentary
7. **Document** findings
8. **Save** JSON
9. **Move** to next page

**Improvements**:
- 9 concrete steps vs. 6 vague steps
- "Segment" step added (was implicit before)
- "Document findings" explicit
- "Move to next page" is clear termination

---

## Example: What an Agent Sees

### v1: Starting a Page

Agents would read 234-line file, including:
- Goal (8 lines)
- Source material (4 lines)
- Workflow (55 lines)
- JSON format (30 lines)
- Quality guidelines (30 lines)
- Language-specific guidelines (30 lines)
- Terminology tables (10 lines)
- Character puns (10 lines)
- Commentary types (8 lines)
- Continuous execution (10 lines)
- Anti-patterns (7 lines)
- Checklist (10 lines)

Then possibly read 6 research files (~700 lines).

**Cognitive load**: Very high. What's essential vs. reference?

### v2: Starting a Page

Agent reads `01_core_task.md` (30 lines):
```
Goal: Translate into 4 languages
Task: 9 steps
Success criteria: 6 checkboxes
What is a segment: 3 definitions
Work continuously: 4 bullets
```

If unsure about JSON format → open `02_json_schema.md`  
If unsure about style → open `03_quality_guidelines.md`  
If need to look up a name → open `research/glossary.md`

**Cognitive load**: Low. Clear starting point. Reference as needed.

---

## Addressing Experiment Issues

### Issue 1: Early Termination (50% of agents)

**Root cause hypothesis**: Context window exhaustion from loading too much upfront

**v2 solution**: 
- 17x smaller initial context load
- Research files referenced on-demand, not pre-loaded
- Modular structure allows selective loading

**Expected improvement**: Agents can translate more pages before hitting context limits

---

### Issue 2: Protocol Non-Compliance (37.5%)

**Root cause**: Parallel protocol mixed with translation instructions, not clear which is which

**v2 solution**:
- Translation instructions contain ZERO parallel protocol
- Parallel protocol will be in separate file given to agents separately
- Agents focus on translation only

**Expected improvement**: 100% compliance with translation schema (protocol compliance managed separately)

---

### Issue 3: Low Productivity (50% of agents)

**Root cause hypothesis**: Unclear time budgets, over-researching, unclear "done" criteria

**v2 solution**:
- Time budget guidance: 45-60 min/page
- Clear success criteria (6 checkboxes)
- "If stuck >5 min, note and move on"
- Goal: 1-1.5 pages/hour

**Expected improvement**: More consistent productivity across agents

---

### Issue 4: Translation Quality Variance

**Root cause**: Different interpretations of what constitutes a "segment" and when page is "complete"

**v2 solution**:
- Explicit segment definition: "5-15 segments per page"
- Segment types clearly defined (prose: 1-3 sentences, etc.)
- Success criterion: "ALL visible text translated"

**Expected improvement**: More consistent segmentation and completeness

---

### Issue 5: JSON Schema Variance

**Root cause**: Example-based schema allowed agents to add extra fields

**v2 solution**:
- Explicit "No extra fields" rule
- Table of required fields with exact names
- Common mistakes section
- Validation rules

**Expected improvement**: 100% schema compliance

---

## Metrics for Success (Next Experiment)

If v2 instructions are effective, we should see:

| Metric | v1 Baseline | v2 Target |
|--------|-------------|-----------|
| Median pages/agent | 7.5 | >15 |
| Early termination rate | 50% | <20% |
| Protocol compliance | 62.5% | >90% |
| Schema compliance | ~70% (estimated) | >95% |
| Productivity variance (std dev) | High | Medium |
| Pages with all text translated | ~80% (estimated) | >95% |

---

## Migration Path

### For New Agents

Simply provide `instructions_v2/` folder and point to `00_READ_ME_FIRST.md`.

### For Ongoing Work

If agents are mid-translation using v1:
1. Let them finish current page with v1 instructions
2. Switch to v2 for next page
3. Schema is compatible (v2 is stricter but accepts v1-compliant output)

### For Parallel Protocol

Create separate `parallel_protocol.md` with:
- Work assignment mechanism
- Page claiming protocol (CLAIM commits)
- Completion signaling (DONE commits)
- Progress tracking (heartbeat commits)
- Conflict resolution (duplicate work)

**Keep completely separate from translation instructions.**

---

## Conclusion

v2 instructions address all major issues identified in the experiment:

✅ Context window optimization (17x smaller initial load)  
✅ Modular structure (reference as needed)  
✅ Explicit schema enforcement (no ambiguity)  
✅ Separated concerns (translation vs. coordination)  
✅ Clear success criteria (know when done)  
✅ Time budget guidance (productivity expectations)  
✅ Positive framing (do this, not avoid that)  

**Next**: Test with small pilot (2-3 agents, 5 pages each) before large-scale deployment.
