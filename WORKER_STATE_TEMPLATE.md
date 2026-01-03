# Worker: [SHORT_ID]

## ⚠️ SYNC DAEMON STATUS (CHECK FIRST!)

> **CRITICAL**: Start the sync daemon BEFORE doing any work!
> ```bash
> python3 tools/sync_daemon.py --start &
> ```

- **Daemon Running**: [yes/no] ← MUST BE "yes" BEFORE CLAIMING
- **Last Full Sync**: [UNIX_TIMESTAMP]
- **Global Completed Count**: [from daemon]

## Status
- **Branch**: [YOUR_FULL_BRANCH_NAME]
- **Short ID**: [LAST_4_CHARS]
- **Heartbeat**: [UNIX_TIMESTAMP]
- **Status**: online

## Current Work
- **Claimed Page**: none
- **Page Verified Available**: [yes/no] ← MUST run `sync_daemon.py --check-page N` first!
- **Started At**: -
- **Current Step**: - (research | translate | polish)

## Completed Pages
| Page | Chapter | Completed At | Hash | Segments |
|------|---------|--------------|------|----------|

## Known Workers (Last Sync - Auto-Updated by Daemon)
| Short ID | Status | Claimed Page | Completed | Last Heartbeat |
|----------|--------|--------------|-----------|----------------|

## Other Workers' Completed Pages (From Daemon Scan)
<!-- This section helps prevent duplicate work -->
| Worker | Completed Pages |
|--------|----------------|

## Notes
Ready to begin translation.

---

## How to Use This Template

### Step 0: START THE SYNC DAEMON FIRST! ⚠️

```bash
# THIS IS MANDATORY - DO THIS FIRST
python3 tools/sync_daemon.py --start &
sleep 30  # Wait for initial sync to complete
```

### Step 1: Copy this file to `WORKER_STATE.md`
```bash
cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
```

### Step 2: Get your identity
```bash
MY_BRANCH=$(git branch --show-current)
MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
echo "Branch: $MY_BRANCH"
echo "Short ID: $MY_SHORT_ID"
```

### Step 3: Fill in your details
- Replace `[YOUR_FULL_BRANCH_NAME]` with your branch
- Replace `[LAST_4_CHARS]` with your short ID
- Replace `[UNIX_TIMESTAMP]` with `$(date +%s)`
- Set `Daemon Running` to `yes`

### Step 4: Check what pages are available (FROM DAEMON!)
```bash
# MANDATORY: Use daemon to find available pages
python3 tools/sync_daemon.py --status  # See global progress
NEXT_PAGE=$(python3 tools/sync_daemon.py --next-page)  # Get next available
echo "Next available page: $NEXT_PAGE"
```

### Step 5: Commit and push (this registers you!)
```bash
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] SYNC: Registering as active worker
HEARTBEAT: $(date +%s)"
git push origin HEAD
```

### Step 6: Delete this "How to Use" section from your WORKER_STATE.md

---

## Example Filled-In State

```markdown
# Worker: d0e5

## Status
- **Branch**: cursor/honglou-translation-d0e5
- **Short ID**: d0e5
- **Heartbeat**: 1735689600
- **Status**: translating

## Current Work
- **Claimed Page**: 25
- **Started At**: 1735689500
- **Current Step**: polish

## Completed Pages
| Page | Chapter | Completed At | Hash | Segments |
|------|---------|--------------|------|----------|
| 21   | 第一回  | 1735686400   | a8f3b2c1 | 5 |
| 22   | 第一回  | 1735687200   | c9d4e5f6 | 4 |
| 23   | 第一回  | 1735688100   | 12ab34cd | 6 |
| 24   | 第一回  | 1735689000   | ef567890 | 4 |

## Known Workers (Last Sync)
| Short ID | Status | Claimed Page | Last Heartbeat |
|----------|--------|--------------|----------------|
| c3d4     | online | 26           | 1735689550     |
| e5f6     | online | 27           | 1735689500     |
| g7h8     | offline| 28           | 1735685000     |

## Notes
Page 25 has dense 甲戌本 commentary. Researched 女娲补天 allusion in detail.
Synced at 1735689600.
```

---

## Updating Your State

### When Claiming a Page
```markdown
## Current Work
- **Claimed Page**: 25
- **Started At**: 1735689500
- **Current Step**: research
```

### When Progressing Through Steps
Update the **Current Step** as you work:
- `research` → researching the content
- `translate` → translating to 4 languages
- `polish` → improving/polishing translations

### When Completing a Page
1. Move page to "Completed Pages" table
2. Set "Claimed Page" to `none` (or next claim)
3. Update heartbeat

### After Syncing
Update the "Known Workers" table with what you found.

### Regular Heartbeat
Even if just working, push a commit every 5 minutes:
```bash
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] PROGRESS: Working on page 25 (polish step)
HEARTBEAT: $(date +%s)"
git push origin HEAD
```
