# Translation Instructions Improvements - Summary

## Context

This document summarizes the improvements made to the 红楼梦 translation instructions based on analysis of the January 3, 2026 parallel translation experiment involving 16 AI agents.

## Experiment Results

**Key Statistics:**
- 16 parallel agents
- 156 total pages translated (average: 9.75 per agent)
- Range: 1-35 pages per agent
- 37.5% of agents completed <5 pages
- Only 12.5% completed >20 pages

**Major Problems Identified:**
1. Agents not following instructions
2. Wrong or partial page translations
3. Low translation quality
4. Incorrect JSON format (missing keys, extra fields)
5. Early stopping (87.5% stopped after <20 pages)

## Root Causes

### 1. Instruction Complexity
The original `instructions.md` mixed:
- Parallel coordination protocol
- Translation workflow
- JSON format specification
- Quality guidelines

**Impact**: Cognitive overload, agents focused on protocol over quality

### 2. Unclear JSON Format
Too many optional fields led to inconsistent outputs with agents inventing their own field structures.

### 3. Missing Quality Gates
Quality guidelines were descriptive, not prescriptive. No explicit verification steps or self-checking mechanism.

### 4. Protocol Overhead
Sync daemon, WORKER_STATE.md updates, and heartbeat management dominated the instructions, making translation secondary.

## Solution: Complete Redesign

### New Document Structure

| Document | Purpose | Length |
|----------|---------|--------|
| `TRANSLATION_INSTRUCTIONS_V2.md` | Core translation workflow and format | Focused, ~500 lines |
| `QUALITY_GUIDE.md` | Concrete quality examples and standards | Detailed, ~600 lines |
| `VERIFICATION_CHECKLIST.md` | Mandatory pre-save verification | Systematic, ~400 lines |
| `examples/page_0020_simplified.json` | Reference example with correct format | Standard |
| `analysis/experiment_findings.md` | Analysis of what went wrong | Reference |

### Key Improvements

## 1. Simplified JSON Format

**Before (complex, with optional fields):**
```json
{
  "page": 20,
  "chapter": "第一回",
  "chapter_title": {...},        // Optional - caused confusion
  "page_content_type": "...",    // Optional - not needed
  "segments": [
    {
      "id": 1,
      "pdf_page": 20,             // Redundant
      "type": "prose",
      "original": "...",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "...",
      "commentary": [...]
    }
  ],
  "translator_notes": [...],     // vs research_notes - inconsistent
  "research_notes": [...],
  "characters_appearing": [...], // Optional - added complexity
  "manuscript_sources_on_page": [...] // Optional - not enforced
}
```

**After (minimal, required fields only):**
```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "...",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "...",
      "commentary": [...]
    }
  ],
  "notes": [...]
}
```

**Benefits:**
- Clear structure
- Easy validation
- No ambiguity
- Consistent outputs

## 2. Concrete Workflow Steps

**Before (vague):**
```
RESEARCH → TRANSLATE → POLISH
```

**After (actionable):**
```
1. Open the page (PDF or image)
2. Identify all content (main text + commentary)
3. Research EACH segment:
   - 3a. Online search (specific queries)
   - 3b. Check reference materials
   - 3c. Document findings
4. Translate to all languages
5. Polish each translation:
   - 5a. Literary quality review
   - 5b. Cultural adaptation by language
   - 5c. Final polish
6. Self-verification checklist (12 items)
7. Save JSON
8. Continue to next page
```

**Benefits:**
- Every step actionable
- Time-boxed guidance
- Clear sufficiency criteria

## 3. Explicit Verification Checklist

**Before:**
- Quality guidelines buried in text
- No self-checking mechanism

**After:**
- Mandatory 48-item checklist
- Organized in 5 sections:
  1. Pre-translation (4 items)
  2. During translation (11 items)
  3. Post-translation polish (11 items)
  4. Pre-save format (13 items)
  5. Final verification (9 items)

**Benefits:**
- Forces completeness
- Catches errors before saving
- Builds good habits

## 4. Quality-First Framing

**Before:**
Instructions started with multi-agent protocol, making coordination the priority.

**After:**
Instructions start with:
> "This is one of world literature's greatest masterpieces. Every word deserves careful attention."

Quality and literary excellence positioned as the primary goal, not an afterthought.

## 5. Comprehensive Quality Guide

**New content:**
- 9 detailed good vs. bad translation examples
- Covers prose, poetry, and commentary
- Shows all 4 target languages
- Explains WHY examples are good or bad
- Addresses common failures with fixes

**Benefits:**
- Concrete quality standards
- Reduces ambiguity
- Shows expected level of work

## 6. Separation of Concerns

**Before:**
One file (`instructions.md`) contained:
- Translation instructions
- Parallel protocol
- Quality guidelines
- Examples
- Anti-patterns

**After:**
Clean separation:
- Translation workflow → `TRANSLATION_INSTRUCTIONS_V2.md`
- Quality standards → `QUALITY_GUIDE.md`
- Verification → `VERIFICATION_CHECKLIST.md`
- Parallel protocol → (separate concern, not mixed in)

**Benefits:**
- Focused attention
- Clear responsibility
- Easier to follow

## Implementation Recommendations

### For Individual Translators

Use these documents in order:
1. **Start**: Read `TRANSLATION_INSTRUCTIONS_V2.md` completely
2. **Reference**: Keep `QUALITY_GUIDE.md` open while working
3. **Before saving**: Complete `VERIFICATION_CHECKLIST.md`
4. **Model**: Use `examples/page_0020_simplified.json` as template

### For Parallel Agents

**Option A: Protocol-Free (Recommended for Initial Testing)**
- Use only translation instructions
- Manually assign page ranges to avoid conflicts
- Focus entirely on translation quality

**Option B: With Lightweight Protocol**
- Separate protocol document (not in translation instructions)
- Simple page claiming mechanism
- No complex sync daemon

**Avoid**: Mixing protocol complexity with translation instructions

### Quality Assurance

**Spot-check criteria:**
- Random sample 10% of completed pages
- Verify checklist compliance
- Review JSON format consistency
- Check translation quality against examples in QUALITY_GUIDE.md

**Red flags:**
- Pages completed in <20 minutes (likely rushed)
- Missing commentary translations
- Generic/obvious research notes
- Extra JSON fields

## Expected Improvements

Based on root cause analysis, these improvements should:

### Increase Completion Rate
- **Previous**: 87.5% stopped early
- **Expected**: >60% complete full assignment

**Why**: Clearer workflow, no protocol confusion

### Improve Translation Quality
- **Previous**: Minimal research, rushed work
- **Expected**: 30-45 min/page minimum, substantive research notes

**Why**: Quality-first framing, explicit time expectations

### Ensure Format Consistency
- **Previous**: Varied JSON structures, extra fields
- **Expected**: 100% format compliance

**Why**: Minimal required format, clear specification

### Reduce Partial Translations
- **Previous**: Many pages with only few segments
- **Expected**: <5% partial translations

**Why**: Explicit verification checklist, completeness requirement

### Increase Commentary Translation
- **Previous**: Commentary often skipped
- **Expected**: >90% commentary coverage

**Why**: Checklist explicitly requires commentary translation

## Testing Plan

### Phase 1: Single Agent Test (1 agent, 5 pages)
**Goal**: Verify instructions are clear and actionable

**Success criteria:**
- Agent completes all 5 pages
- Average >30 min/page
- All pages pass verification checklist
- JSON format 100% compliant

### Phase 2: Small Parallel Test (3 agents, 10 pages each)
**Goal**: Test with minimal coordination

**Success criteria:**
- >80% completion rate
- No format violations
- Quality matches QUALITY_GUIDE.md standards

### Phase 3: Full Parallel Test (16 agents, full assignment)
**Goal**: Replicate original experiment conditions

**Success criteria:**
- >60% completion rate (vs 12.5% previously)
- Average >30 min/page (vs ~15-20 min previously)
- >90% format compliance (vs ~50% previously)
- Quality spot-check passes >80% of samples

## Metrics to Track

| Metric | Previous Experiment | Target with New Instructions |
|--------|---------------------|------------------------------|
| Average pages per agent | 9.75 | >20 |
| Agents completing >20 pages | 12.5% | >60% |
| JSON format compliance | ~50% | >95% |
| Commentary translation rate | ~30% | >90% |
| Average time per page | ~15-20 min | >30 min |
| Research notes per page | <2 | >3 |

## Key Insights

### 1. Clarity Over Comprehensiveness
Better to have focused, actionable instructions than comprehensive but overwhelming documentation.

### 2. Checklists Enforce Quality
Explicit verification checklists are more effective than general quality guidelines.

### 3. Examples > Descriptions
Concrete good vs. bad examples teach better than abstract quality standards.

### 4. Separate Concerns
Translation workflow should not be mixed with coordination protocol.

### 5. Quality Must Be Primary
When protocol and quality compete for attention, protocol wins (it's binary/measurable). Therefore, protocol must be separated or minimized.

## Conclusion

The new instruction set addresses all five major failure categories from the original experiment:

1. ✅ **Agents not following instructions** → Simplified, focused instructions
2. ✅ **Wrong/partial translations** → Explicit verification checklist
3. ✅ **Low quality** → Quality-first framing, detailed quality guide
4. ✅ **Format errors** → Minimal required format, clear specification
5. ✅ **Early stopping** → Clearer workflow, reduced protocol overhead

**Expected outcome**: Significantly improved consistency, completeness, and quality across parallel translation agents.

## Next Steps

1. **Immediate**: Test with single agent on 5-10 pages
2. **Short-term**: Refine based on initial feedback
3. **Medium-term**: Run small parallel test (3 agents)
4. **Long-term**: Full parallel replication with new instructions

---

*Created: February 12, 2026*  
*Based on analysis of January 3, 2026 parallel translation experiment*
