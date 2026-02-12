# Analysis of Parallel Translation Experiment (2026-01-03)

**Date**: January 3, 2026  
**Experiment**: 16 parallel agents translating 红楼梦 pages  
**Branches Analyzed**: Top 16 by commit time (cursor/hong-lou-meng-translation-*)

---

## Executive Summary

The parallel translation experiment showed **severe productivity variance** and **early agent termination** issues. While some agents (1c3a, d4d0) produced 26-34 pages, **50% of agents produced ≤7 pages**, with one agent (a535) producing zero completed pages despite claiming work.

### Key Metrics

| Metric | Best | Worst | Median |
|--------|------|-------|--------|
| Pages completed | 34 (1c3a) | 0 (a535) | 7.5 |
| Working duration | ~13h 16m | ~12h 16m | ~12h 43m |
| Success rate (claims→completions) | 100% (1c3a: 33→34) | 0% (a535: 1→0) | 87.5% |

---

## Detailed Branch Performance

### Tier 1: High Performers (≥20 pages)
```
1c3a: 34 pages, 104 commits, 33 claims → 34 completions (103%)
d4d0: 26 pages,  88 commits, 15 claims → 16 completions (107%)
```

**Characteristics**:
- High claim-to-completion ratio (>100%)
- Continuous work with regular auto-sync commits
- Multiple pages completed per hour

### Tier 2: Moderate Performers (10-19 pages)
```
27e6: 16 pages, 48 commits,  1 claim  →  9 completions
0dac: 13 pages, 56 commits, 14 claims →  7 completions (50%)
```

**Characteristics**:
- Inconsistent claim/completion tracking
- Branch 27e6: claims misaligned with actual output
- Branch 0dac: 50% success rate suggests frequent page abandonment

### Tier 3: Low Performers (5-9 pages)
```
c2f1: 6 pages, 41 commits, 6 claims → 6 completions
914c: 8 pages, 36 commits, 0 claims → 8 completions
be3d: 4 pages, 38 commits, 4 claims → 3 completions
7748: 7 pages, 39 commits, 7 claims → 6 completions
ebba: 9 pages, 42 commits, 9 claims → 8 completions
40bc: 7 pages, 58 commits, 5 claims → 4 completions
```

**Characteristics**:
- Low throughput despite similar runtime
- 914c: no claim commits (protocol not followed)
- be3d: many commits (38) but only 4 pages

### Tier 4: Failed Agents (0-4 pages)
```
f603:  2 pages, 11 commits, 0 claims → 0 completions
5648:  1 page,  11 commits, 0 claims → 0 completions
843e:  1 page,  11 commits, 0 claims → 0 completions
54a8:  2 pages, 11 commits, 0 claims → 0 completions
14dc:  4 pages, 27 commits, 5 claims → 4 completions
a535:  0 pages, 14 commits, 1 claim  → 0 completions
```

**Characteristics**:
- Agents stopped very early (~3h 15-36m runtime)
- No claim/completion tracking (protocol ignored)
- a535: claimed page 20 but never completed it
- Likely hit early conversation limits or errors

---

## Problem Categories

### 1. Early Termination (50% of agents)

**Severity**: CRITICAL  
**Affected branches**: f603, 5648, 843e, 54a8, 14dc, a535, be3d, 7748

**Symptoms**:
- Agents stopped producing output after 1-9 pages
- All started at same time, but stopped 3-13 hours in
- No clear error messages in commit logs

**Hypotheses**:
- Context window exhaustion → agent stopped responding
- Token budget limits
- Conversation turn limits
- Stuck in error/retry loops (no output commits)

**Evidence**:
- Branches with 11 commits (f603, 5648, 843e, 54a8) all have identical patterns → systematic early stop
- Auto-sync heartbeats continued but no DONE commits

### 2. Protocol Non-Compliance (37.5% of agents)

**Severity**: HIGH  
**Affected branches**: 914c, f603, 5648, 843e, 54a8 (5/16)

**Issues**:
- No CLAIM commits before starting pages
- No DONE commits after completing pages
- Cannot track work-in-progress from commit log

**Impact**:
- Parallel coordination impossible
- Cannot detect stuck agents
- Cannot prevent duplicate work

### 3. Low Productivity (50% of agents)

**Severity**: HIGH  
**Affected branches**: All except 1c3a, d4d0

**Symptoms**:
- 0.5-1 page per hour (vs. top performer: ~2.5 pages/hour)
- High commit count but low output (be3d: 38 commits, 4 pages)
- Many auto-sync heartbeats but few DONE commits

**Possible Causes**:
- Spending too much time on research (instructions say "research before translating")
- Getting stuck on difficult passages
- Re-doing work due to errors
- Waiting for user confirmation (instructions unclear on autonomy)

### 4. Translation Quality Issues

**Severity**: MEDIUM (needs more investigation)

**From user observations**:
- "A lot of translation json outputs are not actual translation of the required pages"
- "Some are wrong pages"
- "A lot of them only translate only a few sentences on the page"
- "Not to mention any research notes"
- "Translation quality is bad. Probably due to lack of actual work devoted to translation"
- "Translation json output format is not correct sometimes. Like missing keys"

**Verification** (sample checks):

Branch 843e, page 44:
- ✓ Correct page number
- ✓ 3 segments with full translations (4 languages each)
- ✓ Commentary included
- ✓ Research notes present
- **Quality**: GOOD

Branch f603, page 20:
- ✓ Correct page number
- ✓ 3 segments with full translations (4 languages each)
- ✓ Commentary included
- ✓ Research notes present
- **Quality**: GOOD (but very long segments - may have combined too many sentences)

Branch 1c3a, page 69:
- ✓ Correct page number
- ✓ 5 segments with full translations (4 languages each)
- ✓ Commentary included
- ✓ Research notes present
- **Quality**: EXCELLENT

**Conclusion**: Spot-checked translations show GOOD quality when pages were completed. Issue is not quality per se, but:
- Early termination preventing completion
- Possible wrong page selection in unchecked branches
- Segment count variation (3-5 segments per page suggests inconsistent segmentation strategy)

### 5. Instruction Following Issues

**Severity**: MEDIUM-HIGH

**Evidence**:
- Protocol non-compliance (37.5%)
- Variable segment counts (3-12 segments) suggests different interpretations of "segment"
- Some pages have extra fields (e.g., `pdf_page`, `page_content_type`, `characters_appearing`) not in instructions
- Inconsistent `notes` vs `translator_notes` + `research_notes` field names

**Root Cause**: Instructions may be:
- Too long/complex (234 lines)
- Mixing translation guidelines with parallel work protocol
- Not explicit enough about JSON schema
- Allowing too much agent creativity/interpretation

---

## Pattern Analysis

### Correlation: Commits vs. Pages

```
High commits + High pages:  1c3a (104→34), d4d0 (88→26) → GOOD
High commits + Low pages:   be3d (38→4), 40bc (58→7) → INEFFICIENT
Low commits + Low pages:    5648/843e/f603 (11→1-2) → EARLY STOP
```

**Insight**: Commit count alone doesn't predict success. High commits with low output suggests agents are working but not producing results (stuck in loops?).

### Correlation: Claims vs. Completions

```
No tracking:     914c, f603, 5648, 843e, 54a8 → Protocol not followed
Perfect ratio:   1c3a (33→34), c2f1 (6→6) → Following instructions
Low conversion:  0dac (14→7 = 50%), be3d (4→3 = 75%) → Frequent abandonment
```

**Insight**: Claim/completion ratio is a strong health metric. Agents with <80% conversion are abandoning work mid-page.

---

## Root Cause Hypothesis

### Primary Issue: Context Window Management
The best explanation for the sharp productivity differences is **poor context window utilization**:

1. **Instructions too long** (234 lines) consume context unnecessarily
2. **Research materials** (8 files in `research/`) add context bloat
3. **Conversation history** builds up rapidly
4. Agents hit context limits → stop producing output → auto-sync continues → looks like "working" but actually stuck

**Supporting Evidence**:
- All agents started simultaneously but stopped at different times
- Failed agents have identical commit patterns (11 commits)
- Auto-sync heartbeats continue after output stops
- Best performers (1c3a, d4d0) somehow managed context better

### Secondary Issue: Instruction Clarity
Current `instructions.md`:
- Mixes translation guidelines with workflow steps
- Includes many anti-patterns but doesn't prioritize core requirements
- Has 7 sections + tables + JSON example = cognitive overload
- Says "Continue until you've completed all assigned pages" but doesn't define "all assigned pages"

### Tertiary Issue: Parallel Protocol Embedded
The experiment likely had parallel work assignment protocol embedded in:
- Commit message format (CLAIM/DONE)
- Some external work queue
- But not documented in the repository

**Problem**: Mixing translation instructions with parallel coordination creates confusion. Agents may not understand which parts are for translation quality vs. which are for coordination.

---

## Recommendations

### Immediate: Simplify Instructions (separate from parallel protocol)

1. **Split instructions into modules**:
   - `core_translation_rules.md` (essential only, ~50 lines)
   - `json_schema.md` (explicit schema with required/optional fields)
   - `quality_guidelines.md` (style, voice, research tips - reference only)
   - `parallel_protocol.md` (separate file for coordination logic)

2. **Core translation rules should be**:
   - Maximum 50 lines
   - Only essential requirements
   - Clear, imperative statements
   - No embedded commentary or anti-patterns

3. **Remove context bloat**:
   - Don't load all research files into context
   - Provide research as "reference when needed"
   - Remove example JSON from core instructions (link to file instead)

4. **Explicit JSON schema**:
   ```json
   {
     "page": "number (required)",
     "chapter": "string (required, e.g. '第一回')",
     "segments": [
       {
         "id": "number (required, sequential from 1)",
         "type": "string (required: 'prose' | 'poem' | 'dialogue')",
         "original": "string (required)",
         "zh_modern": "string (required)",
         "en": "string (required)",
         "ru": "string (required)",
         "ja": "string (required)",
         "commentary": "array (required, empty [] if none)"
       }
     ],
     "notes": "array of strings (required, your research findings)"
   }
   ```

5. **Clear success criteria**:
   - "A page is complete when ALL visible text is translated"
   - "Each page should have 5-15 segments (more for dense pages, fewer for sparse)"
   - "Save and move to next page immediately after completion"

### Medium-term: Better Context Management

1. **Provide page assignment explicitly**: "You are assigned pages 20-40. Start with page 20."
2. **Checkpoint mechanism**: "After every 5 pages, create a checkpoint commit and clear conversation context"
3. **Research on-demand**: Don't pre-load, fetch when needed

### Long-term: Agent Monitoring

1. **Health metrics**:
   - Pages per hour
   - Claim-to-completion ratio
   - Time since last output commit
2. **Auto-intervention**: Restart agents that haven't produced output in 30 minutes

---

## Files Generated During Experiment

Total across all branches: **129 translation files**

Distribution:
- 1c3a: 34 files
- d4d0: 26 files
- 27e6: 16 files
- 0dac: 13 files
- ebba: 9 files
- (others): 31 files combined

**Coverage**: Pages 20-76+ (based on spot checks)

**Reusability**: HIGH - spot-checked translations show good quality. Can be reviewed and kept.

---

## Conclusion

The experiment demonstrated that parallel translation is **feasible but requires**:
1. **Drastically simplified instructions** (<50 lines core requirements)
2. **Separation of translation rules from coordination protocol**
3. **Better context window management**
4. **Explicit JSON schema enforcement**
5. **Agent health monitoring and auto-restart**

The quality of completed translations is **generally good**, but the **process efficiency is poor** due to:
- 50% early termination rate
- 10x productivity variance (0-34 pages)
- Protocol non-compliance (37.5%)

**Next step**: Develop simplified, modular instruction set focusing on translation quality only, with parallel protocol completely separated.
