# Worker: [ID]

## Status
- **Branch**: [YOUR_FULL_BRANCH_NAME]
- **Worker ID**: [LAST_4_CHARS]
- **Heartbeat**: [UNIX_TIMESTAMP]
- **Session Start**: [UNIX_TIMESTAMP]
- **Status**: online

## Current Page
- **Page**: none
- **Step**: -
- **Started**: -

## Completed This Session
| Page | Finished At | Segments | Commentary |
|------|-------------|----------|------------|

## Sync Info
- **Daemon Running**: no
- **Last Sync**: -
- **Global Completed**: -
- **Global In-Progress**: -

---

## Setup Instructions (Delete After Setup)

### 1. Start the sync daemon FIRST

```bash
python3 tools/sync_daemon.py --start &
sleep 30
```

### 2. Copy this file

```bash
cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
```

### 3. Get your identity

```bash
MY_BRANCH=$(git branch --show-current)
MY_ID="${MY_BRANCH: -4}"
echo "Branch: $MY_BRANCH"
echo "Worker ID: $MY_ID"
```

### 4. Fill in your details and register

Replace the placeholders above, then:

```bash
git add WORKER_STATE.md
git commit -m "[$MY_ID] REGISTER: Starting session"
git push -u origin HEAD
```

### 5. Get your first page

```bash
NEXT=$(python3 tools/sync_daemon.py --next-page)
echo "Assigned page: $NEXT"
```

### 6. Delete this "Setup Instructions" section and start translating!
