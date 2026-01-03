# Mandatory Sync Service Protocol

## ⚠️ CRITICAL: READ THIS FIRST

**The sync service is MANDATORY for all translation workers.**

Previous translation sessions resulted in **83% wasted effort** because workers translated the same pages multiple times. This document describes the sync service that MUST run during your entire session.

---

## Quick Start

### On Session Start (REQUIRED)

```bash
# Start the sync daemon FIRST before any translation work
python3 tools/sync_daemon.py --start &

# Wait for initial sync to complete
sleep 30

# Then proceed with your work
```

### The daemon will:
1. Fetch all branches every 60 seconds
2. Scan for completed translations across ALL branches  
3. Maintain a local registry of all completed pages
4. Alert you if you try to claim a page that's already done
5. Auto-push your changes every 3 minutes
6. Update your WORKER_STATE.md heartbeat automatically

---

## How the Sync Service Works

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYNC DAEMON                                  │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   FETCHER    │───▶│   SCANNER    │───▶│   REGISTRY   │          │
│  │  (60s loop)  │    │ (all branches)│   │ (completed   │          │
│  │              │    │              │    │   pages)     │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                │                     │
│                                                ▼                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   ALERTER    │◀───│  PRE-CLAIM   │◀───│   WORKER     │          │
│  │  (console)   │    │   CHECK      │    │              │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐                               │
│  │  AUTO-PUSH   │    │  HEARTBEAT   │                               │
│  │  (3m loop)   │    │  (3m loop)   │                               │
│  └──────────────┘    └──────────────┘                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Functions

#### 1. Branch Fetcher (runs every 60s)
```bash
git fetch origin --prune
```

#### 2. Translation Scanner (runs after each fetch)
For each `cursor/*` branch, scans for:
- `translations/page_*.json` files
- `WORKER_STATE.md` completed pages table

#### 3. Global Registry (updated continuously)
Maintains a file at `.sync/global_progress.json`:
```json
{
  "last_sync": 1767407500,
  "completed_pages": {
    "1": {"branch": "cursor/hong-lou-meng-translation-e575", "hash": "b481725d"},
    "2": {"branch": "cursor/hong-lou-meng-translation-e575", "hash": "dda00072"},
    ...
  },
  "claimed_pages": {
    "20": {"branch": "cursor/hong-lou-meng-translation-01d9", "since": 1767407289}
  },
  "active_workers": [
    {"id": "e575", "heartbeat": 1767406537, "status": "idle"},
    {"id": "01d9", "heartbeat": 1767407289, "status": "translating"}
  ]
}
```

#### 4. Pre-Claim Check (called before claiming)
```python
def can_claim_page(page_num):
    if page_num in registry.completed_pages:
        return False, f"Page {page_num} already completed by {registry.completed_pages[page_num]['branch']}"
    if page_num in registry.claimed_pages:
        claim = registry.claimed_pages[page_num]
        age = time.time() - claim['since']
        if age < 900:  # 15 minutes
            return False, f"Page {page_num} claimed by {claim['branch']} {age}s ago"
    return True, "OK"
```

#### 5. Auto-Push (every 3 minutes)
```bash
# If there are uncommitted changes
git add translations/ WORKER_STATE.md
git commit -m "[SHORT_ID] AUTO-SYNC: Progress update
HEARTBEAT: $(date +%s)"
git push origin HEAD
```

#### 6. Heartbeat Updater (every 3 minutes)
Automatically updates the heartbeat in `WORKER_STATE.md`.

---

## Using the Sync Service

### Command Line Interface

```bash
# Start daemon in background
python3 tools/sync_daemon.py --start &

# Check if a page is available
python3 tools/sync_daemon.py --check-page 25

# Get next available page
python3 tools/sync_daemon.py --next-page

# Show global progress
python3 tools/sync_daemon.py --status

# Force immediate sync
python3 tools/sync_daemon.py --sync-now

# Stop daemon
python3 tools/sync_daemon.py --stop
```

### Before Claiming Any Page

**MANDATORY**: Run this BEFORE updating your WORKER_STATE.md with a claim:

```bash
# Check if page is available
python3 tools/sync_daemon.py --check-page PAGE_NUMBER

# If available, proceed with claim
# If NOT available, use --next-page to find what's available
```

### Example Workflow

```bash
# 1. Start daemon
python3 tools/sync_daemon.py --start &

# 2. Find next available page
NEXT_PAGE=$(python3 tools/sync_daemon.py --next-page)
echo "Next available page: $NEXT_PAGE"

# 3. Claim the page (update WORKER_STATE.md)
# ... edit WORKER_STATE.md ...
git add WORKER_STATE.md
git commit -m "[SHORT_ID] CLAIM: Starting page $NEXT_PAGE
HEARTBEAT: $(date +%s)"
git push origin HEAD

# 4. Do translation work
# ... translate page ...

# 5. Save translation
# ... save to translations/page_XXXX.json ...

# 6. The daemon will auto-push, or you can push manually
git add translations/ WORKER_STATE.md
git commit -m "[SHORT_ID] DONE: Completed page $NEXT_PAGE
HEARTBEAT: $(date +%s)"
git push origin HEAD

# 7. Get next page
NEXT_PAGE=$(python3 tools/sync_daemon.py --next-page)
# ... repeat ...
```

---

## Console Output

The daemon provides real-time console output:

```
[SYNC 12:00:00] Fetching all branches...
[SYNC 12:00:02] Found 16 worker branches
[SYNC 12:00:03] Scanning translations...
[SYNC 12:00:05] Registry updated: 20 pages completed, 2 claimed
[SYNC 12:00:05] Active workers: e575(idle), 01d9(translating), 1434(translating)

[SYNC 12:01:00] Fetching all branches...
[SYNC 12:01:02] No changes since last sync

[PUSH 12:03:00] Auto-pushing changes...
[PUSH 12:03:03] Pushed: 2 files, heartbeat updated

[ALERT 12:03:30] ⚠️ You're working on page 21, which was just completed by worker 1434!
[ALERT 12:03:30] ⚠️ Please claim a different page. Next available: 25
```

---

## Sync State Files

The daemon maintains local state in `.sync/` directory:

```
.sync/
├── global_progress.json    # All known completed/claimed pages
├── last_fetch.txt          # Timestamp of last git fetch
├── daemon.pid              # PID of running daemon
└── sync.log                # Sync activity log
```

**Note**: `.sync/` is gitignored - it's local state only.

---

## Failure Modes and Recovery

### If Daemon Crashes

```bash
# Restart it
python3 tools/sync_daemon.py --start &
```

### If Git Push Fails

The daemon will:
1. Log the error
2. Retry in 60 seconds
3. Alert you after 3 failures

### If Network is Down

The daemon will:
1. Continue local operations
2. Queue pushes for when network returns
3. Alert you that sync is stale

### If You Forget to Start Daemon

The pre-claim check will warn you:
```
[ERROR] Sync daemon not running. Start it with: python3 tools/sync_daemon.py --start &
```

---

## Integration with Translation Workflow

### Modified Quick Start Sequence

```bash
# 1. Start sync daemon FIRST
python3 tools/sync_daemon.py --start &
sleep 30  # Wait for initial sync

# 2. Get your identity
MY_BRANCH=$(git branch --show-current)
MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)

# 3. Create/update WORKER_STATE.md
cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
# ... fill in details ...

# 4. Get next available page (from daemon)
NEXT_PAGE=$(python3 tools/sync_daemon.py --next-page)

# 5. Claim and translate
# ... normal workflow ...
```

### Modified WORKER_STATE.md

Add this section to track sync status:

```markdown
## Sync Status
- **Daemon Running**: yes
- **Last Full Sync**: [UNIX_TIMESTAMP]
- **Pages Verified Available**: [list from daemon]
- **Global Completed Count**: [from registry]

## Other Workers' Progress (Auto-Updated by Daemon)
| Worker | Completed Pages | Last Heartbeat |
|--------|----------------|----------------|
| e575   | 15             | 1767406537     |
| 01d9   | 14             | 1767407289     |
| 1434   | 11             | 1767406941     |
```

---

## Rules Enforced by Sync Service

### BLOCKING Rules (Cannot Proceed Without)

1. **Must start daemon before claiming**: Cannot claim pages without daemon running
2. **Must verify page availability**: Pre-claim check required
3. **Must have recent sync**: Claim rejected if last sync > 5 minutes ago

### WARNING Rules (Alerts But Doesn't Block)

1. **Push frequency**: Alert if no push in 5 minutes
2. **Heartbeat staleness**: Alert if heartbeat > 3 minutes old
3. **Concurrent claims**: Alert if another worker claims same page

### AUTO Rules (Daemon Handles Automatically)

1. **Auto-fetch**: Every 60 seconds
2. **Auto-push**: Every 3 minutes (if changes exist)
3. **Auto-heartbeat**: Every 3 minutes
4. **Auto-registry**: Continuous update of global progress

---

## Troubleshooting

### "Page X already completed"

Someone else finished this page. Run `--next-page` to find available work.

### "Daemon not responding"

```bash
# Check if running
ps aux | grep sync_daemon

# If not running, start it
python3 tools/sync_daemon.py --start &
```

### "Sync is stale (> 5 minutes)"

```bash
# Force immediate sync
python3 tools/sync_daemon.py --sync-now
```

### "Push failed"

Check git status and resolve any conflicts:
```bash
git status
git pull origin HEAD --rebase
git push origin HEAD
```

---

## Summary

**The sync daemon is not optional.** 

Start it at the beginning of your session:
```bash
python3 tools/sync_daemon.py --start &
```

Check before claiming:
```bash
python3 tools/sync_daemon.py --check-page PAGE_NUMBER
```

This prevents the 83% waste that occurred in previous sessions.
