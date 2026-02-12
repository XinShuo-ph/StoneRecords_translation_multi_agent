# Parallel Translation Experiment Analysis

## Experiment Overview

**Date**: January 3, 2026  
**Branches**: 32 total `cursor/hong-lou-meng-translation-*` branches  
**Active Agents**: 16 most recent branches (by commit time)  
**Objective**: Translate 红楼梦脂评汇校本 pages in parallel

## Results Summary

### Quantitative Results

| Metric | Value |
|--------|-------|
| Total translations (16 agents) | ~156 pages |
| Average per agent | 9.75 pages |
| Range | 1-35 pages |
| Agents completing <5 pages | 6/16 (37.5%) |
| Agents completing >20 pages | 2/16 (12.5%) |

### Key Observations

1. **Agents not following instructions**
   - Many outputs deviated from specified JSON format
   - Extra fields added: `page_content_type`, `pdf_page`, `chapter_title`, `poem_notes`, `research_notes`, `translator_notes` (vs specified `notes`)
   - Inconsistent field naming and structure

2. **Wrong or partial page translations**
   - Some translations were of wrong pages
   - Many translations only covered a few sentences instead of full page
   - Missing research notes in most outputs

3. **Low translation quality**
   - Lack of depth in actual translation work
   - Insufficient research evident
   - Commentary often missing or incomplete

4. **JSON format errors**
   - Missing required keys
   - Invalid JSON structure in some cases
   - Inconsistent field usage

5. **Early stopping**
   - Most agents (87.5%) stopped after <20 pages
   - Median output: 7.5 pages per agent
   - Only 2 agents showed sustained work (35 and 27 pages)

## Root Cause Analysis

### 1. Instruction Complexity

**Problem**: The `instructions.md` file mixed multiple concerns:
- Parallel protocol (sync daemon, WORKER_STATE.md, heartbeats)
- Translation workflow
- JSON format specification
- Quality guidelines
- Collaboration rules

**Impact**: 
- Cognitive overload
- Agents focused on protocol compliance over translation quality
- Critical translation steps buried in protocol details

### 2. Unclear JSON Format

**Problem**: Format specification was too flexible:
- Many "optional" fields led to inconsistent outputs
- Example showed complex format but didn't enforce it
- No clear distinction between required vs. optional fields

**Impact**:
- Agents created their own field variations
- Made it hard to validate/compile outputs
- Inconsistent data structure across branches

### 3. Missing Concrete Quality Gates

**Problem**: Quality guidelines were descriptive, not prescriptive:
- "Polish translations" - but how?
- "Research each sentence" - but what counts as sufficient?
- "Translate ALL content" - but no explicit verification step

**Impact**:
- Agents skipped quality steps
- Partial translations accepted as "good enough"
- No self-checking mechanism

### 4. Workflow Not Actionable Enough

**Problem**: Workflow steps were high-level:
- "RESEARCH → TRANSLATE → POLISH" stages clear but execution vague
- No concrete sub-steps within each stage
- No explicit verification checkpoints

**Impact**:
- Agents rushed through research
- Skipped polish step entirely
- Incomplete commentary translation

### 5. Protocol Overhead

**Problem**: Parallel protocol dominated instructions:
- Sync daemon setup as "STEP 0"
- WORKER_STATE.md updates
- Heartbeat management
- Branch coordination

**Impact**:
- Agents spent energy on coordination, not translation
- Protocol failures led to early stopping
- Translation quality secondary to protocol compliance

## Specific Examples of Failures

### Example 1: Incomplete Translations (branch 1c3a)

Page 0021.json contains only 4 segments, but visual inspection of page 21 shows at least 6-7 distinct text segments plus multiple commentary annotations that were missed.

### Example 2: Wrong JSON Format (branch d4d0)

Added unauthorized fields:
- `chapter_title` (object with translations)
- `poem_notes` (object with form/rhyme analysis)
- `characters_appearing` (array)
- `manuscript_sources_on_page` (array)

These were not in the specification.

### Example 3: Missing Research (branch 27e6)

Page 0023.json has only 3 generic research notes, despite the page containing:
- Fire symbolism (葫芦庙 = 糊涂)
- Specific idioms (牵五挂四)
- Foreshadowing elements

Minimal research effort evident.

### Example 4: Low Output Volume (branch a535)

Agent produced only 1 translation file before stopping.
No error messages, just stopped.
Likely hit protocol complexity or unclear workflow.

## Recommendations for Improved Instructions

### 1. Separate Protocol from Translation

**Create two distinct documents:**
- `TRANSLATION_INSTRUCTIONS.md` - Pure translation workflow
- `PARALLEL_PROTOCOL.md` - Coordination mechanism (separate concern)

**Benefits:**
- Agents focus on translation quality first
- Protocol becomes optional optimization
- Instructions stay focused

### 2. Simplify JSON Format

**Enforce minimal required format:**
```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [...],
  "notes": [...]
}
```

**Remove optional fields that caused confusion:**
- NO `chapter_title` (redundant)
- NO `page_content_type` (not needed)
- NO `pdf_page` in segments (redundant with top-level `page`)
- NO separate `translator_notes` vs `research_notes` (just use `notes`)

**Benefits:**
- Clear structure
- Easy validation
- Consistent outputs

### 3. Add Explicit Verification Steps

**After each page, agent must verify:**
- [ ] Every visible text segment translated?
- [ ] Every commentary annotation translated?
- [ ] All 4 target languages present?
- [ ] At least 3 research notes documented?
- [ ] JSON validates?
- [ ] Re-read original page - anything missed?

**Benefits:**
- Forces completeness
- Self-checking mechanism
- Prevents partial work

### 4. Make Workflow Extremely Concrete

**Instead of:** "Research each sentence"

**Write:** 
1. For each segment, search: `"红楼梦" + "original text snippet" + "解读"` 
2. Read at least 2 scholarly sources
3. Document any non-obvious finding
4. If nothing found in 5 minutes, mark as "straightforward" and continue

**Benefits:**
- Actionable steps
- Time-boxed to prevent blocking
- Clear sufficiency criteria

### 5. Prioritize Translation Quality

**Move quality guidelines to FRONT of instructions:**
- Lead with "This is world-class literature, every word matters"
- Show examples of GOOD vs BAD translations
- Make quality the hero, not the protocol

**Benefits:**
- Sets the right focus
- Motivates careful work
- Protocol becomes supporting tool

### 6. Provide Better Examples

**Current example (page_0020.json) should be supplemented with:**
- Example of a SIMPLE page (minimal commentary)
- Example of a COMPLEX page (heavy commentary)
- Example of WRONG output with explanations
- Side-by-side "before polish" vs "after polish"

**Benefits:**
- Shows range of expectations
- Demonstrates quality levels
- Reduces ambiguity

## Conclusion

The parallel experiment revealed that **instruction clarity** is the bottleneck, not agent capability.

**Key insight**: When instructions mix protocol complexity with translation quality requirements, agents optimize for protocol compliance (measurable, binary) over translation quality (subjective, continuous).

**Solution**: Radically simplify translation instructions, separate protocol concerns, and make quality verification explicit and actionable.

The next iteration should focus on:
1. **Minimal JSON format** (4 required fields only)
2. **Concrete workflow** (12 explicit steps per page)
3. **Explicit verification** (6-point checklist per page)
4. **Quality-first framing** (protocol as optional)
5. **Better examples** (show good, bad, simple, complex)
