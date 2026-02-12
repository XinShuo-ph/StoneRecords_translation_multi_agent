# Branch Investigation Report: Parallel Collaboration Protocols

## Executive Summary

Investigated all 16 non-translation branches to understand how each approach tried to maintain translation quality while enabling parallel collaborative work. The branches represent three evolutionary phases of the protocol, plus 11 independent worker branches that demonstrate the real-world outcomes.

**Core Finding**: Translation quality was consistently high across all approaches. The critical failure was in coordination — workers repeatedly translated the same pages because the protocol either (a) was too complex to follow, or (b) was removed entirely for simplicity.

---

## Branch Classification

### Phase 1: Initial Parallel Protocol (1 branch)

**Branch: `dream-of-the-red-chamber-translation-plan-d0e5`**

| Aspect | Details |
|--------|---------|
| Files Added | PROTOCOL.md (421 lines), STATE.md (187 lines), WORKER_STATE_TEMPLATE.md (128 lines) |
| Instructions | 790 lines (expanded from original 233) |
| Key Innovation | Worker identity system, heartbeat-based health monitoring, git-based communication |

**Approach to Quality**:
- 10-step workflow: SYNC → CLAIM → VIEW → READ → RESEARCH → TRANSLATE → POLISH → SAVE → BROADCAST → REPEAT
- Mandatory research step with online scholarly search
- `translator_notes` and `research_notes` as required JSON fields
- `characters_appearing` and `manuscript_sources_on_page` metadata fields
- Enhanced commentary object with `type`, `source`, `position` fields
- Detailed character name pun documentation

**Approach to Parallel Coordination**:
- Workers identify via branch short ID (last 4 chars)
- WORKER_STATE.md file per branch for status broadcasting
- Heartbeat system: update every 5 min, offline after 10 min, reclaimable after 15 min
- Sync loop: fetch all branches every 2-3 minutes
- "Claim lowest available page" assignment rule
- Conflict resolution: earlier commit timestamp wins
- "Known Workers" table in each worker's state file

**Strengths**: Comprehensive, well-thought-out distributed systems design. Proper handling of worker disconnection/reconnection. Clear commit message format for machine-readable state.

**Weaknesses**: Entirely manual sync process. No enforcement mechanism. Workers must shell out to run bash loops to discover other workers. Too complex for AI agents to reliably follow alongside translation work.

---

### Phase 2: Sync Daemon Enhancement (1 branch + 2 copies)

**Branch: `translation-branch-synchronization-protocol-2616`**
**Copies: `instruction-investigation`, `parallel-investigation`** (identical content)

| Aspect | Details |
|--------|---------|
| Files Added | SYNC_SERVICE.md (380 lines), GLOBAL_PROGRESS.md (89 lines), ISSUES_REPORT.md (208 lines), tools/sync_daemon.py (733 lines) |
| Instructions | 825 lines (expanded from d0e5's 790) |
| Key Innovation | Automated background sync daemon, mandatory pre-claim verification |

**Approach to Quality**: Same as Phase 1 (inherited unchanged).

**Approach to Parallel Coordination**:
- **Mandatory sync daemon**: `python3 tools/sync_daemon.py --start &` must run before any work
- Auto-fetch all branches every 60 seconds
- Auto-push changes every 3 minutes  
- Auto-heartbeat update every 3 minutes
- Global registry in `.sync/global_progress.json`
- **Pre-claim verification**: `--check-page N` and `--next-page` commands
- GLOBAL_PROGRESS.md auto-generated with completion/claim status
- Three rule categories: BLOCKING (must-have), WARNING (alert), AUTO (daemon handles)

**The Critical Discovery** (documented in ISSUES_REPORT.md):
- Investigated 16 `hong-lou-meng-translation-*` worker branches from Phase 1
- Pages 1-12 were translated an average of **8 times each**
- Page 1 was translated **12 times** by 12 different workers
- Only ~20 unique pages translated out of ~120 total translation instances
- **83% of all work was wasted** due to duplication
- Root causes: workers never checked other branches' files, empty "Known Workers" tables, no background sync enforcement, some workers never created WORKER_STATE.md

**Strengths**: Identified and directly addressed the #1 problem (duplication). Automated sync removes human/agent compliance burden. Pre-claim check provides guardrail.

**Weaknesses**: Even more complex than Phase 1 (now ~2,000+ lines of protocol docs). Sync daemon requires Python background process. Daemon only scans `hong-lou-meng-translation-*` branches (hardcoded). Total protocol surface area is overwhelming.

---

### Phase 3: Radical Simplification (1 branch)

**Branch: `translation-instruction-quality-76e2`**

| Aspect | Details |
|--------|---------|
| Files Removed | PROTOCOL.md, STATE.md, SYNC_SERVICE.md, WORKER_STATE_TEMPLATE.md, GLOBAL_PROGRESS.md, ISSUES_REPORT.md, tools/sync_daemon.py |
| Instructions | Reduced from 825 → 233 lines |
| Key Innovation | Strip ALL collaboration protocol; focus purely on translation quality |

**Approach to Quality**:
- 6-step workflow: View → Research → Translate → Polish → Save → Next Page
- Concise, actionable instructions
- Required fields reduced to essentials: page, chapter, segments (id/type/original/4 translations/commentary), notes
- Anti-patterns with "instead" guidance (e.g., "Skipping content → instead, translate EVERYTHING")
- Quick checklist per page
- "If stuck > 5 minutes, add note and continue"

**Approach to Parallel Coordination**: **None**. All collaboration protocol was deliberately removed.

**Rationale** (from commit messages):
- "Focus purely on translation task (no multi-agent protocol)"
- "Simplify translation instructions and clean up repo"
- "Reduce instructions.md from 778 to 275 lines"

**Strengths**: Clean, focused, achievable instructions. Workers produce high-quality translations without being overwhelmed by protocol overhead. The simplified JSON format is practical and consistent.

**Weaknesses**: Complete absence of coordination leads to the same duplication problem. Workers all start translating from page 1 or the first chapter page.

---

### Phase 4: Worker Branches (11 branches)

All 11 `content-translation-instructions-*` branches forked from main after the Phase 3 (76e2) merge. They share the simplified 233-line instructions.md and have NO coordination protocol.

| Branch | Pages Translated | Page Range | Unique? |
|--------|-----------------|------------|---------|
| **0ef3** | 5 pages | 12-16 | Overlaps with 5328, ccac |
| **159d** | 5 pages | 21-25 | Heavy overlap with others |
| **1baa** | 2 pages | 21-22 | Full overlap |
| **5328** | 5 pages | 12-16 | Full overlap with 0ef3 |
| **6602** | 11 pages | 1-11 | **Only branch to cover 1-11** |
| **8534** | 5 pages | 21-25 | Heavy overlap |
| **ccac** | 2 pages | 15-16 | Partial overlap |
| **d2de** | 8 pages | 21-28 | **Only branch to reach 26-28** |
| **ddce** | 1 page | 21 | Full overlap |
| **de1e** | 1 page | 21 | Full overlap |
| **fefc** | 3 pages | 21-23 | Full overlap |

**Overlap Analysis**:
- Page 21: translated **7 times** (by 159d, 1baa, 8534, d2de, ddce, de1e, fefc)
- Page 22: translated **5 times**
- Pages 12-16: translated **2-3 times** each
- Pages 26-28: translated **only once** (by d2de)
- Pages 1-11: translated **only once** (by 6602)

**Quality Observations Across Workers**:

| Metric | Range | Best |
|--------|-------|------|
| Segments per page (page 21) | 3-15 | d2de (15 segments, finest granularity) |
| Commentary items (page 21) | 6-15 | ddce (15 items), fefc (15), 8534 (15) |
| Research notes (page 21) | 0-7 | d2de (7 notes with pun/allusion analysis) |
| Original text coverage | 562-595 chars | Similar across all (same source page) |

**Key Quality Findings**:
1. **All branches produced valid, complete JSON** — the simplified instructions worked
2. **Segment boundaries differed** — some split text into 3 large segments, others into 15 fine-grained ones
3. **Commentary capture varied** — from 6 to 15 annotations per page depending on how diligently the worker read the source
4. **Research notes were optional in practice** — only d2de and de1e included them despite instructions saying to
5. **All 4 target languages were present** in every translation
6. **Translation quality was consistently good** across all branches regardless of segmentation strategy

---

## Lessons Learned

### 1. Instructions Must Be Concise
The 233-line version (Phase 3) produced the same quality translations as the 825-line version (Phase 2). Simpler instructions = less confusion = better adherence.

### 2. Coordination Cannot Be Optional
Removing ALL coordination (Phase 3) led to 7x duplication on popular pages. Some form of coordination is essential.

### 3. Manual Sync Protocols Are Not Followed
Phase 1's "sync every 2-3 minutes" was completely ignored by actual workers (evidenced by 83% waste in the hong-lou-meng branches).

### 4. Automated Enforcement Works (When Used)
Phase 2's sync daemon concept was sound but was removed before workers could use it.

### 5. Deterministic Assignment Beats Claiming
The "claim lowest available" approach creates races. Workers should receive deterministic page assignments based on their worker ID.

### 6. Research Notes Should Be Required
Branch d2de (the only one with notes) produced demonstrably richer translations with pun explanations, allusion documentation, and cultural context.

### 7. Page-Based Work Units Are Correct
All branches confirmed that one-page-per-file is the right granularity for parallel work.

---

## Recommendation

The best protocol combines:
- **Quality focus** from Phase 3 (concise instructions, 6-step workflow)
- **Automated coordination** from Phase 2 (sync daemon concept, pre-claim verification)
- **Deterministic assignment** (new: hash-based page distribution, no claiming needed)
- **Required research notes** from Phase 1 / branch d2de
- **Lightweight state file** (simplified from Phase 1's complex WORKER_STATE.md)

See `PROTOCOL.md` for the finalized best version.
