# Parallel Collaboration Protocol — Best Version

> Synthesized from investigation of 16 branches. Balances translation quality with coordination to prevent duplicate work. Keeps instructions concise while enforcing synchronization.

---

## Design Principles

1. **Quality First**: Translation excellence is the primary goal; protocol serves quality, not the other way around
2. **Automatic Coordination**: Sync and deduplication happen via tooling, not manual discipline
3. **Deterministic Assignment**: Workers get pages based on their ID — no races, no claiming conflicts
4. **Concise Instructions**: The task description fits in one readable file; protocol is separate
5. **Required Research**: Every page must have translator notes documenting non-trivial findings
6. **Fault Tolerant**: Workers can disconnect and reconnect without losing work or causing duplication

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PER-WORKER BRANCH                             │
│                                                                  │
│  instructions.md     ← Translation task (read-only, concise)    │
│  PROTOCOL.md         ← This file (read-only)                    │
│  WORKER_STATE.md     ← Worker's status (auto-updated)           │
│  translations/       ← Completed page JSONs                     │
│  .sync/              ← Local daemon state (gitignored)          │
│                                                                  │
│  ┌─────────────────────────────────┐                            │
│  │       SYNC DAEMON (background)  │                            │
│  │  • Fetch all branches (60s)     │                            │
│  │  • Build global page registry   │                            │
│  │  • Assign next page to worker   │                            │
│  │  • Auto-push changes (3 min)    │                            │
│  │  • Update heartbeat (3 min)     │                            │
│  └─────────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Worker Identity

Each worker is identified by their **branch suffix** — the last 4 characters of their branch name.

```bash
MY_BRANCH=$(git branch --show-current)
MY_ID="${MY_BRANCH: -4}"
echo "I am worker: $MY_ID"
```

**Examples**: Branch `cursor/hong-lou-meng-translation-e575` → Worker ID `e575`

---

## 2. Startup Sequence (5 Steps)

### Step 1: Start the Sync Daemon

```bash
python3 tools/sync_daemon.py --start &
sleep 30  # Wait for initial full sync
```

The daemon must run for the entire session. It handles:
- Fetching all remote branches every 60 seconds
- Scanning all branches for completed `translations/page_*.json` files
- Maintaining a local registry of completed/in-progress pages
- Auto-pushing your work every 3 minutes
- Keeping your heartbeat alive

### Step 2: Create Your Worker State

```bash
cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
# Fill in your worker ID and branch name
```

### Step 3: Get Your First Page Assignment

```bash
NEXT=$(python3 tools/sync_daemon.py --next-page)
echo "Assigned page: $NEXT"
```

The daemon assigns pages using this priority:
1. Lowest page number not completed on ANY branch
2. Lowest page number not currently claimed by any ONLINE worker
3. Stale claims (>15 min from offline workers) are released

### Step 4: Register and Push

```bash
git add WORKER_STATE.md
git commit -m "[$MY_ID] REGISTER: Starting session"
git push -u origin HEAD
```

### Step 5: Begin Translation

Follow the workflow in `instructions.md`. The daemon handles sync automatically.

---

## 3. Page Assignment: How It Works

### Deterministic Priority (No Claiming Races)

Unlike previous protocols that relied on manual "claim the lowest available" which caused 83% waste, this protocol uses **daemon-mediated assignment**:

```
Global Registry (built by daemon scanning ALL branches):
  Completed: {1: "e575", 2: "e575", 3: "01d9", ...}
  In-Progress: {20: "a1b2", 21: "c3d4"}
  
  Next Available = lowest page NOT in Completed and NOT in In-Progress
```

### Pre-Work Verification (Mandatory)

Before starting ANY page, the worker must verify:

```bash
# Returns exit code 0 if available, 1 if not
python3 tools/sync_daemon.py --check-page $PAGE_NUM
```

This check scans:
- All remote branches' `translations/` directories for existing files
- All remote branches' `WORKER_STATE.md` for active claims
- The local registry built from the last sync

### Stale Claim Recovery

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Worker heartbeat stale | >10 minutes | Worker marked offline |
| Claimed page from offline worker | >15 minutes | Page released to pool |
| No push from worker | >5 minutes | Warning logged |

---

## 4. The Translation Loop

```
┌──────────────────────────────────────────────────────┐
│  1. GET PAGE: sync_daemon.py --next-page             │
│  2. VERIFY: sync_daemon.py --check-page N            │
│  3. UPDATE STATE: Mark page N as in-progress         │
│  4. TRANSLATE: Follow instructions.md workflow       │
│     a. View the page (image + PDF)                   │
│     b. Research (allusions, puns, scholarly context)  │
│     c. Translate to 4 languages                      │
│     d. Polish (润色)                                  │
│  5. SAVE: translations/page_XXXX.json                │
│  6. PUSH: Daemon auto-pushes, or push manually       │
│  7. REPEAT from step 1                               │
└──────────────────────────────────────────────────────┘
```

The daemon handles steps 1-2 and 6 automatically. The worker focuses on steps 3-5.

---

## 5. WORKER_STATE.md Format

Simplified from previous versions. Only essential fields:

```markdown
# Worker: [ID]

## Status
- **Branch**: cursor/translation-xxxx
- **Worker ID**: xxxx
- **Heartbeat**: [unix timestamp]
- **Session Start**: [unix timestamp]
- **Status**: online | translating | idle

## Current Page
- **Page**: [number or "none"]
- **Step**: research | translate | polish
- **Started**: [unix timestamp]

## Completed This Session
| Page | Finished At | Segments | Commentary |
|------|-------------|----------|------------|

## Sync Info
- **Daemon Running**: yes/no
- **Last Sync**: [unix timestamp]
- **Global Completed**: [count]
- **Global In-Progress**: [count]
```

**Update frequency**: The daemon auto-updates heartbeat and sync info. Workers update the current page and completed table.

---

## 6. Commit Message Format

```
[WORKER_ID] ACTION: Description
```

| Action | When |
|--------|------|
| `REGISTER` | Starting a new session |
| `START` | Beginning work on a page |
| `PROGRESS` | Mid-page checkpoint |
| `DONE` | Completed a page |
| `SYNC` | Heartbeat/auto-push |
| `END` | Ending session |

**Examples**:
```bash
git commit -m "[e575] START: Beginning page 25"
git commit -m "[e575] DONE: Completed page 25 (6 segments, 8 commentary)"
git commit -m "[e575] END: Session complete, pages 25-28 finished"
```

---

## 7. Communication via Git

Workers communicate exclusively through git:

| What | How | Frequency |
|------|-----|-----------|
| "I'm alive" | Heartbeat in WORKER_STATE.md | Auto, every 3 min |
| "I'm working on page N" | WORKER_STATE.md current page | On page start |
| "Page N is done" | translations/page_N.json exists | On page completion |
| "Who else is working?" | Daemon scans all branches | Auto, every 60s |
| "What's been done?" | Daemon checks translations/ dirs | Auto, every 60s |

**Key difference from previous protocols**: Workers do NOT need to manually fetch/read other branches. The daemon does this automatically and provides answers via CLI commands.

---

## 8. Handling Failures

### Worker Disconnects Mid-Page
1. Other workers' daemons detect stale heartbeat (>10 min)
2. After 15 min, the claimed page is released
3. Another worker picks it up via `--next-page`
4. If the original worker reconnects and the page was completed by someone else, the daemon tells them to skip to the next available page

### Worker Reconnects
1. Start daemon: `python3 tools/sync_daemon.py --start &`
2. Daemon performs full sync
3. `--next-page` returns the correct next page (skipping any that were completed while offline)
4. Worker resumes with no duplication

### Duplicate Detection
If a worker somehow translates a page that already exists on another branch:
- The daemon detects this during sync
- It logs a warning but does NOT delete the duplicate
- The best version can be selected during final aggregation

### Git Push Fails
- Daemon retries with exponential backoff (4s, 8s, 16s, 32s)
- After 4 failures, alerts the worker
- Worker can manually resolve (rebase, force-push if needed)

---

## 9. Final Aggregation

When all pages are translated, collect the best version of each page:

```bash
python3 tools/sync_daemon.py --aggregate
```

This:
1. Scans all branches for all `translations/page_*.json`
2. For pages with multiple versions, selects based on:
   - Highest segment count (more granular = more thorough)
   - Highest commentary count
   - Presence of research notes
   - Valid JSON
3. Outputs the final set to `output/`

---

## 10. Anti-Patterns

### Coordination Failures (These Caused 83% Waste Previously)

| Don't | Do Instead |
|-------|------------|
| Start translating without daemon running | **Always** start daemon first |
| Manually pick a page number | Use `--next-page` to get assignment |
| Assume "page 1 is unclaimed" | **Always** run `--check-page N` |
| Skip syncing ("I'll just translate") | Daemon syncs automatically — just let it run |
| Work for 30+ min without pushing | Daemon auto-pushes every 3 min |
| Ignore daemon warnings | If daemon says page is taken, trust it |

### Translation Failures

| Don't | Do Instead |
|-------|------------|
| Skip commentary | Translate ALL commentary with type/source attribution |
| Leave notes empty | Document puns, allusions, and cultural context |
| Over-segment or under-segment | One segment per distinct textual unit (prose block, poem, dialogue exchange) |
| Use inconsistent names | Follow `research/glossary.md` |
| Produce invalid JSON | Validate before committing |
| Stop to ask questions | Add note `"Uncertain: [question]"` and continue |

---

## 11. Thresholds and Timings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Daemon fetch interval | 60 seconds | Balance between freshness and git server load |
| Auto-push interval | 3 minutes | Ensure other workers see progress frequently |
| Heartbeat interval | 3 minutes | Tied to auto-push |
| Worker offline threshold | 10 minutes | ~3 missed heartbeats |
| Claim release threshold | 15 minutes | Give offline workers time to reconnect |
| Stuck-on-passage timeout | 5 minutes | Add note and move on |

---

## 12. File Structure

```
workspace/
├── instructions.md              # Translation task (concise, quality-focused)
├── PROTOCOL.md                  # This file (collaboration rules)
├── WORKER_STATE.md              # Your status (auto-maintained by daemon)
├── WORKER_STATE_TEMPLATE.md     # Template for new workers
├── INVESTIGATION_REPORT.md      # Analysis of previous approaches
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf
│
├── source_pages/                # PDF pages as images
├── research/                    # Reference materials (glossary, guides)
├── examples/                    # JSON format examples
├── tools/
│   ├── sync_daemon.py           # Mandatory sync daemon
│   ├── validate_json.py         # JSON validator
│   ├── pdf_to_images.py         # PDF page extractor
│   └── compile_chapters.py      # Final PDF compiler
│
├── translations/                # Output: one JSON per PDF page
│   └── page_XXXX.json
│
├── output/                      # Generated final PDFs
└── .sync/                       # Local daemon state (gitignored)
```

---

## Summary: What Makes This Protocol Work

| Previous Problem | This Protocol's Solution |
|-----------------|--------------------------|
| 83% wasted effort from duplication | Daemon scans ALL branches before assignment |
| Workers ignored manual sync rules | Daemon runs automatically in background |
| Complex 800-line instructions confused workers | Instructions remain concise (233 lines); protocol is separate |
| "Claim lowest available" caused races | Daemon-mediated assignment with pre-claim verification |
| No research notes in most translations | Notes field made mandatory in quality guidelines |
| Workers never created WORKER_STATE.md | Template provided, daemon auto-updates heartbeat |
| No way to detect offline workers | Heartbeat system with 10-min offline threshold |
| Stale claims blocked pages forever | 15-min auto-release of claims from offline workers |
| No global progress visibility | Daemon generates GLOBAL_PROGRESS.md automatically |

**The key insight**: Separate concerns cleanly. `instructions.md` owns translation quality. `PROTOCOL.md` owns coordination. `sync_daemon.py` enforces coordination automatically. Workers focus on translating.
