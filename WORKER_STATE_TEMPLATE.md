# Worker: [SHORT_ID]

## Status
- **Branch**: [YOUR_FULL_BRANCH_NAME]
- **Short ID**: [LAST_4_CHARS]
- **Heartbeat**: [UNIX_TIMESTAMP]
- **Status**: online

## Current Work
- **Claimed Chapter**: none
- **Started At**: -

## Completed Chapters
| Chapter | Completed At | Hash | Segments |
|---------|--------------|------|----------|

## Known Workers (Last Sync)
| Short ID | Status | Claimed Chapter | Last Heartbeat |
|----------|--------|-----------------|----------------|

## Notes
Ready to begin translation.

---

## How to Use This Template

1. **Copy this file** to `WORKER_STATE.md`:
   ```bash
   cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
   ```

2. **Get your identity**:
   ```bash
   MY_BRANCH=$(git branch --show-current)
   MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
   echo "Branch: $MY_BRANCH"
   echo "Short ID: $MY_SHORT_ID"
   ```

3. **Fill in your details**:
   - Replace `[YOUR_FULL_BRANCH_NAME]` with your branch
   - Replace `[LAST_4_CHARS]` with your short ID
   - Replace `[UNIX_TIMESTAMP]` with `$(date +%s)`

4. **Commit and push** (this registers you!):
   ```bash
   git add WORKER_STATE.md
   git commit -m "[$MY_SHORT_ID] SYNC: Registering as active worker
   HEARTBEAT: $(date +%s)"
   git push origin HEAD
   ```

5. **Delete this "How to Use" section** from your WORKER_STATE.md

---

## Example Filled-In State

```markdown
# Worker: d0e5

## Status
- **Branch**: cursor/dream-of-the-red-chamber-translation-plan-d0e5
- **Short ID**: d0e5
- **Heartbeat**: 1735689600
- **Status**: translating

## Current Work
- **Claimed Chapter**: 5
- **Started At**: 1735689500

## Completed Chapters
| Chapter | Completed At | Hash | Segments |
|---------|--------------|------|----------|
| 1       | 1735686400   | a8f3b2c1 | 52 |
| 2       | 1735687200   | c9d4e5f6 | 45 |
| 3       | 1735688100   | 12ab34cd | 38 |
| 4       | 1735689000   | ef567890 | 41 |

## Known Workers (Last Sync)
| Short ID | Status | Claimed Chapter | Last Heartbeat |
|----------|--------|-----------------|----------------|
| c3d4     | online | 6               | 1735689550     |
| e5f6     | online | 7               | 1735689500     |
| g7h8     | offline| 8               | 1735685000     |

## Notes
Currently working on Chapter 5 (太虚幻境). This chapter has many poems - taking extra care.
Synced at 1735689600.
```

---

## Updating Your State

### When Claiming a Chapter
```markdown
## Current Work
- **Claimed Chapter**: 5
- **Started At**: 1735689500
```

### When Completing a Chapter
1. Move chapter to "Completed Chapters" table
2. Set "Claimed Chapter" to `none` (or next claim)
3. Update heartbeat

### After Syncing
Update the "Known Workers" table with what you found.

### Regular Heartbeat
Even if just working, push a commit every 5 minutes:
```bash
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] PROGRESS: Working on chapter 5
HEARTBEAT: $(date +%s)"
git push origin HEAD
```
