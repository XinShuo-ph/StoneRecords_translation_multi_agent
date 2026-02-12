# Translation Instruction Audit (2026-02-12)

## Scope

This audit focuses on **translation instructions only** (not worker orchestration protocol), using the latest parallel experiment branches:

- Branch family: `cursor/hong-lou-meng-translation-*`
- Total branches found: **32**
- "Recent experiment workers": **the 16 most recent branches by tip commit time**

## Method

Primary checks were run directly against remote-tracking branches:

1. Sort branches by commit time
2. Select top 16 branches
3. Inspect `translations/*.json` outputs for:
   - JSON validity
   - schema consistency
   - required segment keys
   - filename conventions
   - continuity signals (latest commit touches translation or not)

## 32 Branches Sorted by Tip Commit Time

1. `origin/cursor/hong-lou-meng-translation-1c3a`
2. `origin/cursor/hong-lou-meng-translation-d4d0`
3. `origin/cursor/hong-lou-meng-translation-27e6`
4. `origin/cursor/hong-lou-meng-translation-40bc`
5. `origin/cursor/hong-lou-meng-translation-0dac`
6. `origin/cursor/hong-lou-meng-translation-c2f1`
7. `origin/cursor/hong-lou-meng-translation-914c`
8. `origin/cursor/hong-lou-meng-translation-be3d`
9. `origin/cursor/hong-lou-meng-translation-7748`
10. `origin/cursor/hong-lou-meng-translation-ebba`
11. `origin/cursor/hong-lou-meng-translation-f603`
12. `origin/cursor/hong-lou-meng-translation-5648`
13. `origin/cursor/hong-lou-meng-translation-843e`
14. `origin/cursor/hong-lou-meng-translation-54a8`
15. `origin/cursor/hong-lou-meng-translation-14dc`
16. `origin/cursor/hong-lou-meng-translation-a535`
17. `origin/cursor/hong-lou-meng-translation-01d9`
18. `origin/cursor/hong-lou-meng-translation-1434`
19. `origin/cursor/hong-lou-meng-translation-6bc6`
20. `origin/cursor/hong-lou-meng-translation-6514`
21. `origin/cursor/hong-lou-meng-translation-e575`
22. `origin/cursor/hong-lou-meng-translation-c11a`
23. `origin/cursor/hong-lou-meng-translation-00b8`
24. `origin/cursor/hong-lou-meng-translation-9a1b`
25. `origin/cursor/hong-lou-meng-translation-342e`
26. `origin/cursor/hong-lou-meng-translation-e020`
27. `origin/cursor/hong-lou-meng-translation-381b`
28. `origin/cursor/hong-lou-meng-translation-a1a9`
29. `origin/cursor/hong-lou-meng-translation-e37a`
30. `origin/cursor/hong-lou-meng-translation-dfe5`
31. `origin/cursor/hong-lou-meng-translation-9b73`
32. `origin/cursor/hong-lou-meng-translation-ad86`

## Findings from the Top-16 Branches

### 1) Output consistency is weak

- Total translation JSON files: **140**
- Invalid JSON files: **2**
- Non-canonical translation filenames (e.g., `_temp`, `_test`): **2**
- Files missing expected top-level translation fields: **1**
- Files with very low segment counts:
  - `<= 4` segments: **79 files**
  - `<= 2` segments: **8 files**

Interpretation: a large fraction of outputs likely capture only part of the page or fail to enforce a stable page segmentation policy.

### 2) Schema drift is significant

Observed top-level schema differs from the current `instructions.md` example.

- Most branch outputs use `translator_notes` and `research_notes`
- Current `instructions.md` specifies `notes`
- Existing local `examples/page_0020.json` was also invalid JSON

Interpretation: instructions, examples, and validator were not aligned, so agents followed mixed targets.

### 3) "Wrong work" / low-value work appears in recent tails

- In **12 of the top 16 branches**, the **latest commit did not touch** `translations/`
- Several latest commits are heartbeat/progress-only messages
- One recent branch (`a535`) had **0 translation JSON files**

Interpretation: agents may stay alive in process terms while no longer doing translation work.

### 4) Research quality requirements are underspecified

- "Research" is requested but not tightly defined with minimum acceptance criteria.
- This encourages shallow or generic notes that do not materially improve translation quality.

## Translation-Instruction Design Implications

To improve consistency across many context windows, translation instructions should:

1. **Be standalone and task-pure**
   - No worker claiming/sync/progress protocol in translation instructions.

2. **Lock one canonical JSON schema**
   - Single required top-level key set
   - Fixed per-segment and per-commentary required keys
   - Stable filename convention (`translations/page_XXXX.json`)

3. **Add wrong-page safeguards**
   - Require source anchors from the page (`first_visible_text`, `last_visible_text`) to prove page match.

4. **Use strict pre-save quality gates**
   - Enforce JSON validity and required keys via validator before saving.
   - Require all four target languages for each segment and commentary item.

5. **Define "complete page" explicitly**
   - No omitted visible text.
   - Commentary must be translated or marked empty only when absent.
   - Segment IDs must be sequential.

6. **Require minimum research evidence**
   - Structured notes with allusion/pun/context and translation impact, not generic statements.

## Next Step Implemented in This Branch

The repository is updated to reflect this audit:

- translation-only instruction rewrite (`instructions.md`)
- aligned validator (`tools/validate_json.py`)
- fixed canonical example (`examples/page_0020.json`)
- docs alignment updates (`README.md`, `tools/README.md`)
