# Recommendations for Next Parallel Translation Experiment

**Date**: February 12, 2026  
**Based on**: Analysis of 16-agent parallel translation experiment  
**Goal**: Achieve 90%+ consistent, high-quality translation across tens of context windows

---

## Executive Summary

The recent experiment demonstrated that **parallel translation is viable but requires simplified, focused instructions**. The primary failure was cognitive overload from mixing translation methodology with coordination protocol.

**Key Fix**: Completely separate translation instructions from parallel worker protocol.

This document provides concrete recommendations for the next iteration.

---

## Critical Changes for Next Experiment

### 1. Separate Instructions from Protocol ⭐ CRITICAL

**Current Problem**: 779-line `instructions.md` mixes translation + protocol

**Solution**: Create two independent systems

#### System A: Translation Instructions (Agent-Facing)
- **File**: `TRANSLATION_GUIDE_V2.md`
- **Length**: < 200 lines
- **Contents**: ONLY how to translate
- **Focus**: READ → RESEARCH → TRANSLATE → POLISH → VERIFY

Agents receive ONLY this file. No protocol details, no git commands, no sync instructions.

#### System B: Parallel Protocol (Automation-Facing)
- **File**: `PARALLEL_PROTOCOL.md` (separate repository or hidden)
- **Contents**: Coordination logic, sync daemon, git operations
- **Automation**: Handles page assignment, deduplication, progress tracking

**Agent sees**: "You are assigned Page 20. Begin translation."  
**Agent does NOT see**: How page was assigned, sync logic, git details

### 2. Enforce Quality with Validation Gates

**Current Problem**: Agents can commit without validation

**Solution**: Pre-commit validation hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
for file in translations/page_*.json; do
  python3 validate_translation_v2.py "$file" --strict
  if [ $? -ne 0 ]; then
    echo "❌ Validation failed for $file"
    echo "Fix errors before committing."
    exit 1
  fi
done
```

**Effect**: Impossible to commit invalid translations.

### 3. Simplify Directory Structure

**Current Structure** (too complex):
```
workspace/
├── instructions.md (779 lines - mixed concerns)
├── PROTOCOL.md (472 lines - separate concern)
├── WORKER_STATE.md
├── WORKER_STATE_TEMPLATE.md
├── STATE.md
├── GLOBAL_PROGRESS.md
├── ISSUES_REPORT.md
├── SYNC_SERVICE.md
├── research/ (7 files)
├── examples/
├── tools/
├── source_pages/
├── translations/
├── output/
└── 20/
```

**New Structure** (simplified):
```
workspace/
├── TRANSLATION_GUIDE_V2.md  (200 lines max - agent reads this ONLY)
├── source.pdf
├── translations/
│   └── page_XXXX.json
├── tools/
│   ├── validate_translation_v2.py (enhanced)
│   └── compile_pages.py
└── research/
    ├── glossary.md
    └── examples.md
```

**Removed files**:
- Old `instructions.md` → replaced by `TRANSLATION_GUIDE_V2.md`
- `PROTOCOL.md` → moved to automation system
- `WORKER_STATE.md` → handled by automation
- `STATE.md`, `GLOBAL_PROGRESS.md` → handled by automation
- Complex state tracking → handled by automation

### 4. Add Mandatory Quality Checklist to JSON

**New Required Field**:
```json
"quality_checklist": {
  "read_full_page": true,
  "identified_all_content": true,
  "researched_allusions": true,
  "consulted_min_3_sources": true,
  "all_commentary_translated": true,
  "all_4_languages_complete": true,
  "polished_each_language": true,
  "verified_completeness": true,
  "json_validated": true
}
```

**Validation**: All fields must be `true`. Any `false` → validation fails.

**Effect**: Agents must consciously verify each step.

### 5. Require Research Evidence

**New Required Fields**:
```json
"research_sources": [
  {
    "title": "周汝昌新校红楼梦",
    "type": "book",
    "page": 42,
    "finding": "Character name 甄士隐 is a pun on 真事隐 (true events hidden)"
  },
  {
    "title": "红楼梦学刊 1997年第3期",
    "type": "article",
    "finding": "三生石 alludes to Buddhist concept of karmic bonds"
  },
  {
    "url": "https://example.com/honglou-analysis",
    "type": "web",
    "finding": "青埂峰 is homophonous with 情根 (root of passion)"
  }
],
"translator_notes": [
  "甄士隐 (Zhen Shiyin) = 真事隐 (true events hidden) - confirmed by 甲戌本 commentary",
  "三生石 references Buddhist karma across 3 lives (past, present, future)",
  "青埂峰/情根 pun appears in Chapter 1, establishing novel's central theme"
]
```

**Validation**:
- Minimum 3 sources required
- Each source must have `finding` field (>10 chars)
- `translator_notes` must have ≥1 entry (>20 chars each)

**Effect**: Research becomes verifiable, not perfunctory.

### 6. Require Polish Evidence

**New Required Field**:
```json
"polish_log": [
  {"language": "zh_modern", "iteration": 1, "changes": "Improved flow in segment 3"},
  {"language": "en", "iteration": 1, "changes": "Better poetry rhythm in segment 2"},
  {"language": "ru", "iteration": 1, "changes": "Adjusted register for aristocratic dialogue"},
  {"language": "ja", "iteration": 1, "changes": "Added classical elements to segment 1"}
]
```

**Validation**:
- Minimum 4 entries (one per language)
- Each entry must have `changes` field (>10 chars)

**Effect**: Polishing becomes mandatory, not optional.

### 7. Set Quality-Focused Quotas

**Old Metric**: "Translate as many pages as possible"  
**Problem**: Agents optimize for quantity over quality

**New Metric**: "Complete 10-20 pages with excellent quality"

**Enforcement**:
```python
# In automation system
if completed_pages < 10:
    status = "INCOMPLETE - minimum 10 pages required"
elif completed_pages > 20:
    status = "COMPLETE - quota met, you may stop"
else:
    status = f"IN_PROGRESS - {completed_pages}/10 minimum completed"
```

**Effect**: 
- Lower bound (10) ensures meaningful work
- Upper bound (20) prevents burnout and rushing

### 8. Automated Page Assignment

**Old System**: Agents claim pages via git, sync daemon, manual checking

**New System**: Automation assigns pages

**Workflow**:
```
Agent starts → Automation: "You are assigned Page 20"
Agent translates → Saves JSON → Automation validates → Commits
Agent ready for next → Automation: "You are assigned Page 35"
```

**Agent NEVER sees**:
- Page selection logic
- Other workers' status
- Sync coordination
- Git operations

**Effect**: Agent focuses 100% on translation quality.

---

## Implementation Plan for Next Experiment

### Phase 1: Preparation (Before Agent Launch)

1. **Create new instruction file**
   - Use `TRANSLATION_GUIDE_V2.md` (already created)
   - Maximum 200 lines
   - Focus only on translation

2. **Set up validation**
   - Copy `translation_schema.json` to workspace
   - Copy `validate_translation_v2.py` to workspace
   - Install pre-commit hook

3. **Simplify directory structure**
   - Remove old instruction files
   - Keep only essential files

4. **Prepare automation system**
   - Page assignment queue
   - Progress tracking (hidden from agents)
   - Auto-commit on validation pass

### Phase 2: Agent Launch

**Agent receives**:
```
You are translating 红楼梦 (Dream of the Red Chamber) from Classical Chinese 
to 4 modern languages.

Read TRANSLATION_GUIDE_V2.md for complete instructions.

You are assigned: Page 20

Begin when ready.
```

**Agent does NOT receive**:
- Protocol documentation
- Sync instructions
- Progress tracking
- Other workers' status

### Phase 3: Per-Page Workflow

```
1. Agent reads TRANSLATION_GUIDE_V2.md
2. Agent opens PDF to assigned page
3. Agent follows 3-step process:
   - READ (identify all content)
   - RESEARCH & TRANSLATE (all 4 languages)
   - POLISH & VERIFY (improve quality, validate)
4. Agent saves translations/page_XXXX.json
5. Automation runs validation
6. If validation passes → auto-commit
7. If validation fails → agent fixes errors, repeat step 5
8. On success → automation assigns next page
9. Repeat until quota met (10-20 pages)
```

### Phase 4: Quality Control

**Automated checks** (on each commit):
- JSON schema validation
- All fields present and non-empty
- Quality checklist all `true`
- Research sources ≥ 3
- Polish log ≥ 4 entries (one per language)
- Translator notes substantive (>20 chars)

**Manual spot checks** (random sampling):
- Translation accuracy
- Literary quality
- Research depth
- Terminology consistency

---

## Expected Improvements

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Instruction following | ~40% | >90% | +125% |
| Avg translations/agent | 12.5 | 15-20 | +40% |
| Complete research | ~30% | >95% | +217% |
| JSON validation pass | ~70% | 100% | +43% |
| Agent completion rate | ~50% | >90% | +80% |
| Translation quality (1-10) | 5/10 | 8/10 | +60% |

---

## Architecture Comparison

### Old Architecture (Current Experiment)

```
┌─────────────────────────────────────────────┐
│  Agent                                       │
│  ├─ Reads instructions.md (779 lines)       │
│  ├─ Reads PROTOCOL.md (472 lines)           │
│  ├─ Starts sync daemon                      │
│  ├─ Discovers other workers                 │
│  ├─ Claims page via git                     │
│  ├─ Translates (maybe researches)           │
│  ├─ Saves JSON (maybe validates)            │
│  ├─ Commits & pushes                        │
│  └─ Updates WORKER_STATE.md                 │
└─────────────────────────────────────────────┘

Problem: 60% effort on coordination, 40% on translation
```

### New Architecture (Recommended)

```
┌─────────────────────────────────────────────┐
│  Agent                                       │
│  ├─ Reads TRANSLATION_GUIDE_V2.md (200 lines)│
│  ├─ Receives page assignment (automated)    │
│  ├─ Translates (following guide)            │
│  │   ├─ READ                                │
│  │   ├─ RESEARCH (enforced)                 │
│  │   ├─ TRANSLATE (all 4 languages)         │
│  │   └─ POLISH (verified)                   │
│  ├─ Saves JSON                              │
│  └─ Validation auto-runs                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Automation (Invisible to Agent)            │
│  ├─ Assigns pages                           │
│  ├─ Runs validation                         │
│  ├─ Commits on validation pass              │
│  ├─ Tracks progress                         │
│  └─ Prevents duplicates                     │
└─────────────────────────────────────────────┘

Result: 95% effort on translation, 5% on logistics
```

---

## Risk Mitigation

### Risk 1: Agents Still Skip Research

**Mitigation**:
- Validation requires ≥3 sources with findings
- `research_sources` field is required
- Each source must have substantive `finding` (>10 chars)
- Quality checklist includes `researched_allusions: true`

### Risk 2: Agents Fill Templates Mechanically

**Mitigation**:
- Validation checks for suspiciously uniform lengths
- Polish log required (evidence of iteration)
- Spot check translations for quality
- Compare against existing translations for accuracy

### Risk 3: Validation Too Strict, Agents Get Stuck

**Mitigation**:
- Clear error messages from validator
- Examples of good translations in guide
- Validation can be run before commit to preview issues
- Iterative: fix errors, re-validate, improve

### Risk 4: Agents Ignore Quality Checklist

**Mitigation**:
- Schema validation REQUIRES all checklist fields = `true`
- Impossible to commit with any `false` values
- Pre-commit hook blocks invalid JSON

---

## Success Metrics for Next Iteration

### Tier 1: Must Have
- [ ] 100% of translations pass JSON schema validation
- [ ] 95%+ have complete research (≥3 sources)
- [ ] 95%+ have complete polish (4 languages)
- [ ] 90%+ agents complete 10+ pages
- [ ] 0% duplicate work

### Tier 2: Should Have
- [ ] Average quality rating 7/10+ (manual review)
- [ ] 90%+ translations include all commentary
- [ ] Translation time: 60-90 min per page
- [ ] Terminology consistency 95%+

### Tier 3: Nice to Have
- [ ] Some agents complete 20 pages (quota maximum)
- [ ] Quality rating 8/10+ (manual review)
- [ ] Research notes cite specific page numbers/sources
- [ ] Evidence of creative polish (not just corrections)

---

## Quick Start for Next Experiment

### For Experiment Coordinator

1. **Set up workspace**:
   ```bash
   mkdir -p workspace/translations workspace/tools workspace/research
   cp TRANSLATION_GUIDE_V2.md workspace/
   cp translation_schema.json workspace/
   cp validate_translation_v2.py workspace/tools/
   cp source.pdf workspace/
   ```

2. **Install pre-commit hook**:
   ```bash
   cat > workspace/.git/hooks/pre-commit << 'EOF'
   #!/bin/bash
   for file in translations/page_*.json; do
     python3 tools/validate_translation_v2.py "$file" --strict || exit 1
   done
   EOF
   chmod +x workspace/.git/hooks/pre-commit
   ```

3. **Prepare agent instructions**:
   ```
   You are translating 红楼梦 from Classical Chinese to 4 languages.
   
   1. Read TRANSLATION_GUIDE_V2.md (complete instructions)
   2. You are assigned: Page 20
   3. Save your work to: translations/page_0020.json
   4. Validation runs automatically
   5. When complete, you'll receive your next page
   
   Quality over speed. Take your time.
   ```

### For Agent

1. Read `TRANSLATION_GUIDE_V2.md`
2. Open PDF to assigned page
3. Follow 3-step process
4. Save JSON
5. Run `python3 tools/validate_translation_v2.py translations/page_XXXX.json --strict`
6. Fix any errors
7. Commit (validation auto-runs)

---

## Files Delivered for Next Experiment

| File | Purpose | Status |
|------|---------|--------|
| `EXPERIMENT_ANALYSIS.md` | Analysis of current experiment issues | ✅ Created |
| `TRANSLATION_GUIDE_V2.md` | New simplified translation instructions | ✅ Created |
| `translation_schema.json` | JSON schema for validation | ✅ Created |
| `validate_translation_v2.py` | Enhanced validation script | ✅ Created |
| `RECOMMENDATIONS.md` | This document | ✅ Created |

---

## Conclusion

The next experiment should show **dramatic improvement** in:
1. **Consistency** - Clear instructions, enforced validation
2. **Quality** - Required research, polish, and verification
3. **Completion** - Simplified focus, clear quotas
4. **Efficiency** - Less coordination overhead, more translation time

**Primary success factor**: Separating translation instructions from parallel protocol allows agents to focus 95% of effort on quality translation work.

**Expected outcome**: 90%+ agents producing high-quality, complete, validated translations with minimal duplicate work or early stopping.
