# Translation Instruction Investigation (2026-02-12)

## Scope

This investigation focuses on **translation instructions only**.

Out of scope for this document:
- worker heartbeat
- branch sync daemon
- page claiming and conflict resolution

Those are worker-protocol concerns and should stay in a separate document.

---

## Method

1. Enumerated remote branches matching:
   - `origin/cursor/hong-lou-meng-translation-*`
2. Sorted by `committerdate` descending.
3. Selected the newest 16 branches as the recent parallel trial cohort.
4. Audited translation outputs on these 16 branches for:
   - filename compliance
   - JSON parse validity
   - schema-key compliance
   - required field presence

---

## Sorted Branches (All 32)

The latest 16 are marked `TOP16`.

| Rank | Commit time | Branch | Cohort | Head commit subject |
|---|---|---|---|---|
| 1 | 2026-01-03 04:15:22 +0000 | origin/cursor/hong-lou-meng-translation-1c3a | TOP16 | [1c3a] AUTO-SYNC: Progress update HEARTBEAT: 1767413722 |
| 2 | 2026-01-03 04:15:22 +0000 | origin/cursor/hong-lou-meng-translation-d4d0 | TOP16 | [d4d0] AUTO-SYNC: Progress update HEARTBEAT: 1767413722 |
| 3 | 2026-01-03 04:12:42 +0000 | origin/cursor/hong-lou-meng-translation-27e6 | TOP16 | [27e6] AUTO-SYNC: Progress update HEARTBEAT: 1767413562 |
| 4 | 2026-01-03 04:06:16 +0000 | origin/cursor/hong-lou-meng-translation-40bc | TOP16 | [40bc] AUTO-SYNC: Progress update HEARTBEAT: 1767413176 |
| 5 | 2026-01-03 04:00:37 +0000 | origin/cursor/hong-lou-meng-translation-0dac | TOP16 | [0dac] AUTO-SYNC: Progress update HEARTBEAT: 1767412837 |
| 6 | 2026-01-03 03:51:24 +0000 | origin/cursor/hong-lou-meng-translation-c2f1 | TOP16 | [c2f1] AUTO-SYNC: Progress update HEARTBEAT: 1767412284 |
| 7 | 2026-01-03 03:48:39 +0000 | origin/cursor/hong-lou-meng-translation-914c | TOP16 | [914c] AUTO-SYNC: Progress update HEARTBEAT: 1767412119 |
| 8 | 2026-01-03 03:48:25 +0000 | origin/cursor/hong-lou-meng-translation-be3d | TOP16 | [be3d] AUTO-SYNC: Progress update HEARTBEAT: 1767412105 |
| 9 | 2026-01-03 03:42:21 +0000 | origin/cursor/hong-lou-meng-translation-7748 | TOP16 | [7748] AUTO-SYNC: Progress update HEARTBEAT: 1767411741 |
| 10 | 2026-01-03 03:42:15 +0000 | origin/cursor/hong-lou-meng-translation-ebba | TOP16 | [ebba] AUTO-SYNC: Progress update HEARTBEAT: 1767411735 |
| 11 | 2026-01-03 03:42:10 +0000 | origin/cursor/hong-lou-meng-translation-f603 | TOP16 | Update progress and add page 26 and 53 translations |
| 12 | 2026-01-03 03:36:16 +0000 | origin/cursor/hong-lou-meng-translation-5648 | TOP16 | Update progress and add page 44 translation |
| 13 | 2026-01-03 03:35:58 +0000 | origin/cursor/hong-lou-meng-translation-843e | TOP16 | Update progress and worker status, add page 44 |
| 14 | 2026-01-03 03:35:21 +0000 | origin/cursor/hong-lou-meng-translation-54a8 | TOP16 | feat: Add translation for page 44 and update progress |
| 15 | 2026-01-03 03:30:52 +0000 | origin/cursor/hong-lou-meng-translation-14dc | TOP16 | [14dc] AUTO-SYNC: Progress update HEARTBEAT: 1767411052 |
| 16 | 2026-01-03 03:15:19 +0000 | origin/cursor/hong-lou-meng-translation-a535 | TOP16 | [a535] AUTO-SYNC: Progress update HEARTBEAT: 1767410119 |
| 17 | 2026-01-03 02:28:16 +0000 | origin/cursor/hong-lou-meng-translation-01d9 |  | Translate page 19: famous couplet 假作真时真亦假 and Jade of Spiritual Understanding |
| 18 | 2026-01-03 02:22:21 +0000 | origin/cursor/hong-lou-meng-translation-1434 |  | [1434] DONE: Completed page 13 (Stone origin myth, Nuwa, Monk & Taoist), claiming page 14 HASH: 6f803b8c SEGMENTS: 5 HEARTBEAT: 1767406941 |
| 19 | 2026-01-03 02:20:25 +0000 | origin/cursor/hong-lou-meng-translation-6bc6 |  | [6bc6] DONE: Completed pages 11-12 (凡例 end, Chapter 1 start) HEARTBEAT: 1767406825 |
| 20 | 2026-01-03 02:18:55 +0000 | origin/cursor/hong-lou-meng-translation-6514 |  | [6514] DONE: Completed page 18 (Crimson Pearl Flower mythology) HASH: 7767c020 SEGMENTS: 4 HEARTBEAT: 1767406735 |
| 21 | 2026-01-03 02:16:05 +0000 | origin/cursor/hong-lou-meng-translation-e575 |  | Add tools to extract PDF metadata and page text |
| 22 | 2026-01-03 02:10:01 +0000 | origin/cursor/hong-lou-meng-translation-c11a |  | [c11a] DONE: Completed page 10 (editorial principles - fanli) HASH: fe0bc19e SEGMENTS: 4 HEARTBEAT: 1767406201 |
| 23 | 2026-01-03 02:08:51 +0000 | origin/cursor/hong-lou-meng-translation-00b8 |  | feat: Add initial translations for pages 1, 3, 7, and 11 |
| 24 | 2026-01-03 02:08:09 +0000 | origin/cursor/hong-lou-meng-translation-9a1b |  | Add source images for pages 0001-0035 |
| 25 | 2026-01-03 02:08:01 +0000 | origin/cursor/hong-lou-meng-translation-342e |  | Add source page images |
| 26 | 2026-01-03 02:07:56 +0000 | origin/cursor/hong-lou-meng-translation-e020 |  | Add pages 1 through 100 to the document |
| 27 | 2026-01-03 02:06:01 +0000 | origin/cursor/hong-lou-meng-translation-381b |  | [381b] DONE: Completed page 9 (table of contents conclusion) HASH: 8bca6cbe SEGMENTS: 3 HEARTBEAT: 1767405961 |
| 28 | 2026-01-03 02:02:06 +0000 | origin/cursor/hong-lou-meng-translation-a1a9 |  | Add translations for front matter pages |
| 29 | 2026-01-03 02:01:21 +0000 | origin/cursor/hong-lou-meng-translation-e37a |  | Add new page images to source_pages |
| 30 | 2026-01-03 01:55:49 +0000 | origin/cursor/hong-lou-meng-translation-dfe5 |  | feat: Add initial worker state file |
| 31 | 2026-01-02 17:51:38 -0800 | origin/cursor/hong-lou-meng-translation-9b73 |  | Update project description in README.md |
| 32 | 2026-01-02 17:51:38 -0800 | origin/cursor/hong-lou-meng-translation-ad86 |  | Update project description in README.md |

---

## Key Findings from the Latest 16 Branches

### 1) Translation work is frequently displaced by sync/status activity
- 12/16 latest branch head commits are `AUTO-SYNC` / `HEARTBEAT`.
- 1/16 branches had zero translation JSON files at head (`a535`).

### 2) Schema divergence is widespread
- Audited JSON files in TOP16 branches: **140**
  - Canonical `translations/page_XXXX.json`: **138**
  - Non-canonical names: **2**
    - `translations/page_0021_test.json`
    - `translations/page_0021_temp.json`
- Parse errors among canonical files: **1**
  - `origin/cursor/hong-lou-meng-translation-d4d0:translations/page_0022.json`
  - Root cause: unescaped quotes inside JSON string.

### 3) Required-key consistency is effectively absent
- In parseable canonical files, `notes` missing in **137** files.
- Those files used legacy key `translator_notes` instead.
- Segments missing required `commentary` key: **103** segments.

### 4) Layout/workspace noise increases cognitive load
- Large non-translation artifacts are committed in worker branches
  (example: one branch adds 1041 files under `20/`), making it harder for agents to focus on per-page translation quality.

---

## Design Implications for Translation Instructions

To improve consistency across many parallel contexts, translation instructions should be:

1. **Strictly separated from worker protocol**
   - no heartbeat/sync/claim logic in translation instructions
2. **Single-schema and machine-checkable**
   - one canonical JSON contract
   - no legacy aliases (`translator_notes`, etc.)
3. **Filename and page-lock enforced**
   - `page_XXXX.json` + matching `page` + matching `source_page`
4. **Completion-gated**
   - page is not done until `tools/validate_json.py` passes
5. **Coverage-explicit**
   - every segment must carry `commentary` (possibly empty array)
   - no partial pages

---

## Changes Implemented in This Branch

- Rewrote `instructions.md` as translation-only (v2).
- Added `parallel_worker_protocol.md` to keep orchestration separate.
- Rebuilt `tools/validate_json.py` around strict page schema validation.
- Replaced `examples/page_0020.json` with a valid canonical example.
- Updated documentation references in `README.md`, `tools/README.md`, and `research/poetry_guide.md`.
