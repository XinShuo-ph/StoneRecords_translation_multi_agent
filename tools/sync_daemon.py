#!/usr/bin/env python3
"""
Sync Daemon for Hong Lou Meng Translation Project

This daemon ensures workers stay synchronized and prevents duplicate work.
It MUST be running during any translation session.

Usage:
    python sync_daemon.py --start &     # Start daemon in background
    python sync_daemon.py --check-page N  # Check if page N is available
    python sync_daemon.py --next-page   # Get next available page
    python sync_daemon.py --status      # Show current status
    python sync_daemon.py --sync-now    # Force immediate sync
    python sync_daemon.py --stop        # Stop the daemon
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import threading
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Configuration
WORKSPACE_ROOT = Path(__file__).parent.parent
SYNC_DIR = WORKSPACE_ROOT / ".sync"
GLOBAL_PROGRESS_FILE = WORKSPACE_ROOT / "GLOBAL_PROGRESS.md"
WORKER_STATE_FILE = WORKSPACE_ROOT / "WORKER_STATE.md"
TRANSLATIONS_DIR = WORKSPACE_ROOT / "translations"

# Timing configuration
FETCH_INTERVAL = 60      # Fetch all branches every 60 seconds
PUSH_INTERVAL = 180      # Auto-push every 3 minutes
HEARTBEAT_INTERVAL = 180 # Update heartbeat every 3 minutes
CLAIM_TIMEOUT = 900      # Claimed page becomes available after 15 minutes
OFFLINE_THRESHOLD = 600  # Worker considered offline after 10 minutes

# Total pages in PDF (approximate)
TOTAL_PAGES = 1041


class SyncRegistry:
    """Maintains global state of all completed and claimed pages across all branches."""
    
    def __init__(self):
        self.completed_pages: Dict[int, dict] = {}  # page -> {branch, hash, completed_at}
        self.claimed_pages: Dict[int, dict] = {}    # page -> {branch, since, worker_id}
        self.active_workers: Dict[str, dict] = {}   # worker_id -> {branch, status, heartbeat, claimed_page, completed_count}
        self.last_sync: int = 0
        self.load()
    
    def load(self):
        """Load registry from disk if exists."""
        registry_file = SYNC_DIR / "global_progress.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    data = json.load(f)
                    self.completed_pages = {int(k): v for k, v in data.get('completed_pages', {}).items()}
                    self.claimed_pages = {int(k): v for k, v in data.get('claimed_pages', {}).items()}
                    self.active_workers = data.get('active_workers', {})
                    self.last_sync = data.get('last_sync', 0)
            except Exception as e:
                log(f"Error loading registry: {e}")
    
    def save(self):
        """Save registry to disk."""
        SYNC_DIR.mkdir(exist_ok=True)
        registry_file = SYNC_DIR / "global_progress.json"
        data = {
            'last_sync': self.last_sync,
            'completed_pages': {str(k): v for k, v in self.completed_pages.items()},
            'claimed_pages': {str(k): v for k, v in self.claimed_pages.items()},
            'active_workers': self.active_workers
        }
        with open(registry_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_completed(self, page: int, branch: str, hash_val: str, completed_at: int):
        """Mark a page as completed."""
        self.completed_pages[page] = {
            'branch': branch,
            'hash': hash_val,
            'completed_at': completed_at
        }
        # Remove from claimed if present
        if page in self.claimed_pages:
            del self.claimed_pages[page]
    
    def add_claimed(self, page: int, branch: str, worker_id: str, since: int):
        """Mark a page as claimed."""
        if page not in self.completed_pages:
            self.claimed_pages[page] = {
                'branch': branch,
                'worker_id': worker_id,
                'since': since
            }
    
    def update_worker(self, worker_id: str, branch: str, status: str, heartbeat: int, 
                      claimed_page: Optional[int], completed_count: int):
        """Update worker info."""
        self.active_workers[worker_id] = {
            'branch': branch,
            'status': status,
            'heartbeat': heartbeat,
            'claimed_page': claimed_page,
            'completed_count': completed_count
        }
    
    def is_page_available(self, page: int) -> Tuple[bool, str]:
        """Check if a page is available for claiming."""
        if page in self.completed_pages:
            return False, f"Page {page} already completed by {self.completed_pages[page]['branch']}"
        
        if page in self.claimed_pages:
            claim = self.claimed_pages[page]
            age = int(time.time()) - claim['since']
            if age < CLAIM_TIMEOUT:
                return False, f"Page {page} claimed by {claim['worker_id']} ({age}s ago, timeout at {CLAIM_TIMEOUT}s)"
            else:
                # Claim has timed out, page is available
                return True, f"Page {page} was claimed but timed out (worker {claim['worker_id']} inactive)"
        
        return True, "Page is available"
    
    def get_next_available(self) -> Optional[int]:
        """Get the lowest available page number."""
        for page in range(1, TOTAL_PAGES + 1):
            available, _ = self.is_page_available(page)
            if available:
                return page
        return None
    
    def get_available_pages(self, count: int = 10) -> List[int]:
        """Get list of next N available pages."""
        available = []
        for page in range(1, TOTAL_PAGES + 1):
            if len(available) >= count:
                break
            is_avail, _ = self.is_page_available(page)
            if is_avail:
                available.append(page)
        return available
    
    def cleanup_stale_claims(self):
        """Remove claims from workers who have gone offline."""
        current_time = int(time.time())
        stale_claims = []
        
        for page, claim in self.claimed_pages.items():
            age = current_time - claim['since']
            if age > CLAIM_TIMEOUT:
                stale_claims.append(page)
        
        for page in stale_claims:
            log(f"Removing stale claim for page {page} (timed out)")
            del self.claimed_pages[page]


def log(message: str, level: str = "SYNC"):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{level} {timestamp}] {message}")


def run_git_command(args: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=WORKSPACE_ROOT,
            capture_output=capture_output,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def get_worker_branches() -> List[str]:
    """Get list of all cursor/* branches."""
    code, stdout, _ = run_git_command(['branch', '-r'])
    if code != 0:
        return []
    
    branches = []
    for line in stdout.strip().split('\n'):
        line = line.strip()
        if 'origin/cursor/' in line and 'hong-lou-meng' in line:
            branch = line.replace('origin/', '').strip()
            branches.append(branch)
    return branches


def get_branch_worker_state(branch: str) -> Optional[dict]:
    """Get WORKER_STATE.md content from a branch."""
    code, stdout, _ = run_git_command(['show', f'origin/{branch}:WORKER_STATE.md'])
    if code != 0:
        return None
    
    # Parse the WORKER_STATE.md
    state = {
        'branch': branch,
        'short_id': branch.split('-')[-1][:4] if '-' in branch else branch[-4:],
        'heartbeat': 0,
        'status': 'unknown',
        'claimed_page': None,
        'completed_pages': []
    }
    
    lines = stdout.split('\n')
    in_completed_table = False
    
    for line in lines:
        # Parse heartbeat
        if '**Heartbeat**:' in line:
            match = re.search(r'\*\*Heartbeat\*\*:\s*(\d+)', line)
            if match:
                state['heartbeat'] = int(match.group(1))
        
        # Parse status
        if '**Status**:' in line:
            match = re.search(r'\*\*Status\*\*:\s*(\w+)', line)
            if match:
                state['status'] = match.group(1)
        
        # Parse claimed page
        if '**Claimed Page**:' in line:
            match = re.search(r'\*\*Claimed Page\*\*:\s*(\d+|none)', line)
            if match:
                val = match.group(1)
                state['claimed_page'] = int(val) if val != 'none' else None
        
        # Parse completed pages table
        if '## Completed Pages' in line:
            in_completed_table = True
            continue
        
        if in_completed_table:
            if line.startswith('##') or line.startswith('---'):
                in_completed_table = False
                continue
            # Parse table row: | Page | Chapter | Completed At | Hash | Segments |
            if '|' in line and not line.startswith('|---'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        page_num = int(parts[1])
                        state['completed_pages'].append({
                            'page': page_num,
                            'chapter': parts[2] if len(parts) > 2 else '',
                            'completed_at': int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0,
                            'hash': parts[4] if len(parts) > 4 else ''
                        })
                    except (ValueError, IndexError):
                        pass
    
    return state


def get_branch_translations(branch: str) -> List[int]:
    """Get list of page numbers with translations on a branch."""
    code, stdout, _ = run_git_command(['ls-tree', '--name-only', '-r', f'origin/{branch}', '--', 'translations/'])
    if code != 0:
        return []
    
    pages = []
    for line in stdout.strip().split('\n'):
        # Match translations/page_XXXX.json
        match = re.search(r'page_(\d+)\.json', line)
        if match:
            pages.append(int(match.group(1)))
    return pages


def do_full_sync(registry: SyncRegistry) -> bool:
    """Perform a full sync: fetch all branches and update registry."""
    log("Fetching all branches...")
    code, _, stderr = run_git_command(['fetch', 'origin', '--prune'])
    if code != 0:
        log(f"Fetch failed: {stderr}", "ERROR")
        return False
    
    branches = get_worker_branches()
    log(f"Found {len(branches)} worker branches")
    
    # Clear current registry (will rebuild)
    old_completed = set(registry.completed_pages.keys())
    registry.completed_pages = {}
    registry.claimed_pages = {}
    registry.active_workers = {}
    
    log("Scanning translations...")
    for branch in branches:
        # Get worker state
        state = get_branch_worker_state(branch)
        if state:
            worker_id = state['short_id']
            
            # Update worker info
            registry.update_worker(
                worker_id=worker_id,
                branch=branch,
                status=state['status'],
                heartbeat=state['heartbeat'],
                claimed_page=state['claimed_page'],
                completed_count=len(state['completed_pages'])
            )
            
            # Add claimed page
            if state['claimed_page']:
                registry.add_claimed(
                    page=state['claimed_page'],
                    branch=branch,
                    worker_id=worker_id,
                    since=state['heartbeat']  # Approximate claim time
                )
            
            # Add completed pages from WORKER_STATE.md
            for cp in state['completed_pages']:
                registry.add_completed(
                    page=cp['page'],
                    branch=branch,
                    hash_val=cp.get('hash', ''),
                    completed_at=cp.get('completed_at', 0)
                )
        
        # Also scan translations directory for any missed pages
        translation_pages = get_branch_translations(branch)
        for page in translation_pages:
            if page not in registry.completed_pages:
                registry.add_completed(
                    page=page,
                    branch=branch,
                    hash_val='',
                    completed_at=0
                )
    
    # Cleanup stale claims
    registry.cleanup_stale_claims()
    
    registry.last_sync = int(time.time())
    registry.save()
    
    # Report new completions
    new_completed = set(registry.completed_pages.keys()) - old_completed
    if new_completed:
        log(f"New completions found: pages {sorted(new_completed)}", "INFO")
    
    # Calculate stats
    online_workers = sum(1 for w in registry.active_workers.values() 
                        if int(time.time()) - w['heartbeat'] < OFFLINE_THRESHOLD)
    
    log(f"Registry updated: {len(registry.completed_pages)} pages completed, "
        f"{len(registry.claimed_pages)} claimed, {online_workers} workers online")
    
    # Update GLOBAL_PROGRESS.md
    update_global_progress_file(registry)
    
    return True


def update_global_progress_file(registry: SyncRegistry):
    """Update the GLOBAL_PROGRESS.md file with current state."""
    current_time = int(time.time())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    completed_count = len(registry.completed_pages)
    claimed_count = len(registry.claimed_pages)
    online_count = sum(1 for w in registry.active_workers.values() 
                      if current_time - w['heartbeat'] < OFFLINE_THRESHOLD)
    progress_pct = (completed_count / TOTAL_PAGES) * 100
    
    # Build completed pages table
    completed_rows = []
    for page in sorted(registry.completed_pages.keys()):
        info = registry.completed_pages[page]
        worker_id = info['branch'].split('-')[-1][:4] if '-' in info['branch'] else 'unknown'
        completed_at = datetime.fromtimestamp(info['completed_at']).strftime("%Y-%m-%d %H:%M") if info['completed_at'] else 'unknown'
        completed_rows.append(f"| {page} | - | {worker_id} | {info['branch'][-20:]}... | {completed_at} | {info['hash'][:8] if info['hash'] else '-'} |")
    
    # Build claimed pages table
    claimed_rows = []
    for page in sorted(registry.claimed_pages.keys()):
        info = registry.claimed_pages[page]
        age = current_time - info['since']
        age_str = f"{age}s" if age < 60 else f"{age//60}m"
        claimed_at = datetime.fromtimestamp(info['since']).strftime("%H:%M:%S")
        claimed_rows.append(f"| {page} | {info['worker_id']} | {info['branch'][-20:]}... | {claimed_at} | {age_str} |")
    
    # Build workers table
    worker_rows = []
    for worker_id, info in sorted(registry.active_workers.items()):
        age = current_time - info['heartbeat']
        age_str = f"{age}s" if age < 60 else f"{age//60}m"
        status = "offline" if age > OFFLINE_THRESHOLD else info['status']
        claimed = info['claimed_page'] if info['claimed_page'] else '-'
        worker_rows.append(f"| {worker_id} | {status} | {claimed} | {info['completed_count']} | {datetime.fromtimestamp(info['heartbeat']).strftime('%H:%M:%S')} | {age_str} |")
    
    # Get available pages
    available = registry.get_available_pages(10)
    available_str = ', '.join(str(p) for p in available) + ", ..."
    
    content = f"""# Global Translation Progress

**Auto-generated by sync daemon. Do not edit manually.**

Last Updated: `{timestamp}`

---

## Summary

| Metric | Count |
|--------|-------|
| Total PDF Pages | ~{TOTAL_PAGES} |
| Pages Completed | {completed_count} |
| Pages Claimed | {claimed_count} |
| Active Workers | {online_count} |
| Progress | {progress_pct:.1f}% |

---

## Completed Pages

| Page | Chapter | Worker | Branch | Completed At | Hash |
|------|---------|--------|--------|--------------|------|
{chr(10).join(completed_rows[:50]) if completed_rows else '| - | - | - | - | - | - |'}
{f'... and {len(completed_rows) - 50} more' if len(completed_rows) > 50 else ''}

---

## Currently Claimed Pages

| Page | Worker | Branch | Claimed At | Age |
|------|--------|--------|------------|-----|
{chr(10).join(claimed_rows) if claimed_rows else '| - | - | - | - | - |'}

---

## Active Workers

| Worker ID | Status | Current Page | Completed | Last Heartbeat | Age |
|-----------|--------|--------------|-----------|----------------|-----|
{chr(10).join(worker_rows) if worker_rows else '| - | - | - | - | - | - |'}

---

## Available Pages (Next 10)

{available_str}

---

## How This File is Updated

This file is automatically updated by the sync daemon every 60 seconds.

Workers should NOT edit this file directly. Instead:
1. Run `python tools/sync_daemon.py --status` to see current progress
2. Run `python tools/sync_daemon.py --next-page` to get next available page
3. The daemon updates this file based on all workers' branches
"""
    
    with open(GLOBAL_PROGRESS_FILE, 'w') as f:
        f.write(content)


def do_auto_push():
    """Push any uncommitted changes."""
    # Check if there are changes to push
    code, stdout, _ = run_git_command(['status', '--porcelain'])
    if code != 0 or not stdout.strip():
        return  # No changes
    
    # Get worker short ID
    code, branch, _ = run_git_command(['branch', '--show-current'])
    if code != 0:
        return
    branch = branch.strip()
    short_id = branch.split('-')[-1][:4] if '-' in branch else branch[-4:]
    
    # Stage relevant files
    run_git_command(['add', 'translations/', 'WORKER_STATE.md', 'GLOBAL_PROGRESS.md'])
    
    # Commit with heartbeat
    timestamp = int(time.time())
    run_git_command(['commit', '-m', f'[{short_id}] AUTO-SYNC: Progress update\nHEARTBEAT: {timestamp}'])
    
    # Push
    code, _, stderr = run_git_command(['push', 'origin', 'HEAD'])
    if code == 0:
        log("Auto-pushed changes", "PUSH")
    else:
        log(f"Push failed: {stderr}", "ERROR")


def update_heartbeat():
    """Update heartbeat in WORKER_STATE.md."""
    if not WORKER_STATE_FILE.exists():
        return
    
    try:
        with open(WORKER_STATE_FILE, 'r') as f:
            content = f.read()
        
        # Update heartbeat timestamp
        new_content = re.sub(
            r'\*\*Heartbeat\*\*:\s*\d+',
            f'**Heartbeat**: {int(time.time())}',
            content
        )
        
        if new_content != content:
            with open(WORKER_STATE_FILE, 'w') as f:
                f.write(new_content)
    except Exception as e:
        log(f"Error updating heartbeat: {e}", "ERROR")


class SyncDaemon:
    """Background sync daemon."""
    
    def __init__(self):
        self.registry = SyncRegistry()
        self.running = False
        self.sync_thread = None
        self.push_thread = None
    
    def start(self):
        """Start the daemon."""
        self.running = True
        
        # Initial sync
        do_full_sync(self.registry)
        
        # Start sync thread
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        
        # Start push thread
        self.push_thread = threading.Thread(target=self._push_loop, daemon=True)
        self.push_thread.start()
        
        # Save PID
        SYNC_DIR.mkdir(exist_ok=True)
        with open(SYNC_DIR / "daemon.pid", 'w') as f:
            f.write(str(os.getpid()))
        
        log("Sync daemon started", "DAEMON")
    
    def stop(self):
        """Stop the daemon."""
        self.running = False
        pid_file = SYNC_DIR / "daemon.pid"
        if pid_file.exists():
            pid_file.unlink()
        log("Sync daemon stopped", "DAEMON")
    
    def _sync_loop(self):
        """Main sync loop."""
        while self.running:
            time.sleep(FETCH_INTERVAL)
            if self.running:
                do_full_sync(self.registry)
    
    def _push_loop(self):
        """Auto-push loop."""
        while self.running:
            time.sleep(PUSH_INTERVAL)
            if self.running:
                update_heartbeat()
                do_auto_push()
    
    def check_page(self, page: int) -> Tuple[bool, str]:
        """Check if a page is available."""
        return self.registry.is_page_available(page)
    
    def next_page(self) -> Optional[int]:
        """Get next available page."""
        return self.registry.get_next_available()
    
    def status(self) -> dict:
        """Get current status."""
        current_time = int(time.time())
        online_count = sum(1 for w in self.registry.active_workers.values() 
                         if current_time - w['heartbeat'] < OFFLINE_THRESHOLD)
        
        return {
            'completed_pages': len(self.registry.completed_pages),
            'claimed_pages': len(self.registry.claimed_pages),
            'active_workers': online_count,
            'total_workers': len(self.registry.active_workers),
            'last_sync': self.registry.last_sync,
            'next_available': self.registry.get_next_available(),
            'available_pages': self.registry.get_available_pages(10)
        }


# Global daemon instance
_daemon: Optional[SyncDaemon] = None


def get_daemon() -> SyncDaemon:
    """Get or create daemon instance."""
    global _daemon
    if _daemon is None:
        _daemon = SyncDaemon()
    return _daemon


def main():
    parser = argparse.ArgumentParser(description='Sync Daemon for Hong Lou Meng Translation')
    parser.add_argument('--start', action='store_true', help='Start the daemon')
    parser.add_argument('--stop', action='store_true', help='Stop the daemon')
    parser.add_argument('--check-page', type=int, metavar='N', help='Check if page N is available')
    parser.add_argument('--next-page', action='store_true', help='Get next available page')
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--sync-now', action='store_true', help='Force immediate sync')
    
    args = parser.parse_args()
    
    if args.start:
        daemon = get_daemon()
        daemon.start()
        
        # Keep running
        def signal_handler(sig, frame):
            daemon.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        log("Daemon running. Press Ctrl+C to stop.", "DAEMON")
        
        # Keep main thread alive
        while daemon.running:
            time.sleep(1)
    
    elif args.stop:
        pid_file = SYNC_DIR / "daemon.pid"
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                os.kill(pid, signal.SIGTERM)
                log(f"Stopped daemon (PID {pid})", "DAEMON")
            except (ProcessLookupError, ValueError):
                log("Daemon not running", "DAEMON")
            pid_file.unlink(missing_ok=True)
        else:
            log("Daemon not running", "DAEMON")
    
    elif args.check_page is not None:
        registry = SyncRegistry()
        # Do a quick sync first
        do_full_sync(registry)
        available, message = registry.is_page_available(args.check_page)
        if available:
            print(f"✓ Page {args.check_page} is AVAILABLE")
            print(f"  {message}")
        else:
            print(f"✗ Page {args.check_page} is NOT AVAILABLE")
            print(f"  {message}")
            next_page = registry.get_next_available()
            if next_page:
                print(f"  Next available page: {next_page}")
        sys.exit(0 if available else 1)
    
    elif args.next_page:
        registry = SyncRegistry()
        do_full_sync(registry)
        next_page = registry.get_next_available()
        if next_page:
            print(next_page)
        else:
            print("No pages available")
            sys.exit(1)
    
    elif args.status:
        registry = SyncRegistry()
        do_full_sync(registry)
        
        current_time = int(time.time())
        online_count = sum(1 for w in registry.active_workers.values() 
                         if current_time - w['heartbeat'] < OFFLINE_THRESHOLD)
        
        print("\n" + "="*60)
        print("HONG LOU MENG TRANSLATION - SYNC STATUS")
        print("="*60)
        print(f"Last Sync: {datetime.fromtimestamp(registry.last_sync).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Completed Pages: {len(registry.completed_pages)}/{TOTAL_PAGES} ({len(registry.completed_pages)/TOTAL_PAGES*100:.1f}%)")
        print(f"Claimed Pages: {len(registry.claimed_pages)}")
        print(f"Active Workers: {online_count}/{len(registry.active_workers)}")
        print()
        
        print("WORKERS:")
        for worker_id, info in sorted(registry.active_workers.items()):
            age = current_time - info['heartbeat']
            status_symbol = "●" if age < OFFLINE_THRESHOLD else "○"
            age_str = f"{age}s ago" if age < 60 else f"{age//60}m ago"
            claimed = f"page {info['claimed_page']}" if info['claimed_page'] else "none"
            print(f"  {status_symbol} {worker_id}: {info['status']}, claimed={claimed}, completed={info['completed_count']}, heartbeat {age_str}")
        print()
        
        available = registry.get_available_pages(10)
        print(f"NEXT AVAILABLE PAGES: {', '.join(str(p) for p in available)}")
        print("="*60 + "\n")
    
    elif args.sync_now:
        registry = SyncRegistry()
        success = do_full_sync(registry)
        if success:
            print("Sync completed successfully")
        else:
            print("Sync failed")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
