# Translation Instruction Trial Audit (2026-02-12)

## Scope

Investigated the 32 branches matching:

- `origin/cursor/hong-lou-meng-translation-*`

Sorted by commit time, then selected the latest 16 as the most recent parallel cohort.

## Latest 16 Branches (by commit time)

1. `origin/cursor/hong-lou-meng-translation-1c3a` (2026-01-03 04:15:22 +0000)
2. `origin/cursor/hong-lou-meng-translation-d4d0` (2026-01-03 04:15:22 +0000)
3. `origin/cursor/hong-lou-meng-translation-27e6` (2026-01-03 04:12:42 +0000)
4. `origin/cursor/hong-lou-meng-translation-40bc` (2026-01-03 04:06:16 +0000)
5. `origin/cursor/hong-lou-meng-translation-0dac` (2026-01-03 04:00:37 +0000)
6. `origin/cursor/hong-lou-meng-translation-c2f1` (2026-01-03 03:51:24 +0000)
7. `origin/cursor/hong-lou-meng-translation-914c` (2026-01-03 03:48:39 +0000)
8. `origin/cursor/hong-lou-meng-translation-be3d` (2026-01-03 03:48:25 +0000)
9. `origin/cursor/hong-lou-meng-translation-7748` (2026-01-03 03:42:21 +0000)
10. `origin/cursor/hong-lou-meng-translation-ebba` (2026-01-03 03:42:15 +0000)
11. `origin/cursor/hong-lou-meng-translation-f603` (2026-01-03 03:42:10 +0000)
12. `origin/cursor/hong-lou-meng-translation-5648` (2026-01-03 03:36:16 +0000)
13. `origin/cursor/hong-lou-meng-translation-843e` (2026-01-03 03:35:58 +0000)
14. `origin/cursor/hong-lou-meng-translation-54a8` (2026-01-03 03:35:21 +0000)
15. `origin/cursor/hong-lou-meng-translation-14dc` (2026-01-03 03:30:52 +0000)
16. `origin/cursor/hong-lou-meng-translation-a535` (2026-01-03 03:15:19 +0000)

## Key Findings

### 1) Schema drift was severe

Across the latest 16 branches, root schemas diverged into multiple variants. The dominant schema used extra keys such as:

- `chapter_title`
- `characters_appearing`
- `manuscript_sources_on_page`
- `page_content_type`
- `research_notes`
- `translator_notes`
- `total_segments`

This diverged from current main-branch `instructions.md`, which expected a smaller schema with `notes`.

### 2) Format failures were common

- 138 `translations/page_XXXX.json` files detected in latest 16 branches.
- At least 1 invalid `page_XXXX.json` file (JSON syntax error).
- 2 non-standard output filenames detected (e.g., `page_0021_test.json`, `page_0021_temp.json`).
- Missing `commentary` key found in multiple segment objects (32 affected files in audit checks).

### 3) Wrong-page symptoms were observable

For same filename/page number, opening lines of `segments[0].original` often differed drastically across branches.

Example for `page_0020.json`:

- `27e6`, `0dac`, `f603`, `54a8`: starts with `士隐意欲也跟了过去...`
- `1c3a`: starts with `那僧笑道：“此事说来好笑...`
- `d4d0`: starts with `偏值士隐走来听见...`

This indicates page-identification failures in at least some runs.

### 4) Coverage inconsistency was high

For identical page IDs, segment counts varied widely across branches:

- `page_0021`: min 3, max 15
- `page_0026`: min 2, max 12
- `page_0030`: min 3, max 13
- `page_0035`: min 2, max 13

Large variance strongly suggests partial-page translations in some outputs.

### 5) Continuous work reliability was weak

- 1 of the latest 16 branches had zero `page_XXXX.json` outputs.
- Many latest commits were heartbeat/progress updates, not translation completions.

## Implications for Translation Instructions

Translation instructions should be:

1. **Translation-only** (no worker sync/claim/heartbeat logic).
2. **Schema-locked** (exact keys; no extra keys).
3. **Page-anchored** (require top/bottom source anchors per page).
4. **Coverage-gated** (all visible page content required; no partial output files).
5. **Validator-first** (mandatory local validation before keeping output).

These requirements are implemented in this branch via:

- `instructions.md` (rewritten translation-only contract)
- `tools/validate_json.py` (strict schema/completeness validator)
- `examples/page_0020.json` (valid schema example)
