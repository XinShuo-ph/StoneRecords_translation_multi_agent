# Translation Instruction Audit (2026-02-12)

This note captures findings from the recent multi-branch experiment and derives translation-instruction requirements for the next iteration.

Scope: translation instruction quality only (not worker sync protocol).

---

## Dataset and Method

- Branch set: `origin/cursor/hong-lou-meng-translation-*`
- Total branches found: 32
- Recent experiment cohort: top 16 branches by latest commit time
- Audited artifacts: `translations/*.json` at each branch HEAD

Primary checks:

1. JSON parse validity
2. Schema consistency
3. Placeholder / pseudo-translation patterns
4. Notes quality and completeness
5. Output filename hygiene
6. Basic continuity signal (files produced per branch)

---

## Top 16 Branches by Commit Time

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

---

## Key Findings

### 1) Format and schema drift is significant

- Files audited (top 16): **140**
- Invalid JSON files: **2**
  - Example class: unescaped quotes inside string literals
- Top-level schema is inconsistent across workers:
  - `page/chapter/segments` present widely
  - Optional fields vary (`chapter_title`, `total_segments`, `commentary`, etc.)
  - Multiple incompatible commentary layouts were observed

Impact: downstream parsers and quality checks cannot run uniformly.

### 2) Placeholder pseudo-translations are present

- Files with placeholder-like content: **9**
- Typical bad pattern:
  - `"[Dialogue between family members ...]"`
  - `"[Continuing ... narrative]"` in `original` or translation fields

Impact: file looks structurally complete but is not a real translation.

### 3) Notes quality is inconsistent

- Files with blank translator/research note content: **11** in the recent cohort

Impact: little evidence of passage-level research, weak translation grounding.

### 4) Output naming is not consistently canonical

- Non-canonical filenames observed:
  - `translations/page_0021_test.json`
  - `translations/page_0021_temp.json`

Impact: easy to miss in aggregation and validation.

### 5) Continuous execution is uneven

Per-branch output counts in top 16:

- min: 0
- max: 34
- mean: 8.75
- median: 6.5
- branches with <= 4 files: 7/16
- branches with <= 1 file: 3/16

Impact: many workers stop early or produce little sustained work.

---

## Instruction Implications

The translation instruction must be:

1. **Strictly canonical** in JSON schema
2. **Reject placeholder text explicitly**
3. **Require meaningful research notes**
4. **Define a hard per-page definition of done**
5. **Use machine-checkable acceptance criteria**

This is now reflected in:

- `instructions.md` (translation-only v2 contract)
- `tools/validate_json.py` (schema + placeholder enforcement)
- `examples/page_0020.json` (valid canonical sample)

---

## Suggested Next Measurement Loop

For the next run, track:

1. JSON pass rate (`validate_json.py`) at commit time
2. Placeholder detection count
3. Mean notes-per-page and non-empty note ratio
4. Completion durability: files produced per worker over time windows
5. Duplicate-page incidence across active workers

These metrics can be compared against this audit baseline.
