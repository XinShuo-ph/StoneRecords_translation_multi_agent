# Project State

**红楼梦 Multi-Agent Collaborative Translation**

---

## How to Check Active Workers

```bash
git fetch origin --prune

for branch in $(git branch -r | grep 'origin/cursor/' | sed 's|origin/||' | tr -d ' '); do
  if git show "origin/${branch}:WORKER_STATE.md" &>/dev/null 2>&1; then
    short_id=$(echo "$branch" | grep -oE '[^-]+$' | tail -c 5)
    heartbeat=$(git show "origin/${branch}:WORKER_STATE.md" 2>/dev/null | grep -oP 'Heartbeat: \K[0-9]+' | head -1)
    now=$(date +%s)
    age=$((now - heartbeat))
    if [ $age -lt 600 ]; then
      echo "ONLINE:  $short_id (heartbeat ${age}s ago)"
    else
      echo "OFFLINE: $short_id (heartbeat ${age}s ago)"
    fi
  fi
done
```

---

## Book Information

- **Title**: 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary Collation)
- **Author**: 曹雪芹 (Cao Xueqin)
- **Era**: Qing Dynasty, mid-18th century
- **Total Content**: **80 chapters (八十回)** plus front matter and appendices
- **Genre**: Classical Chinese novel, one of the Four Great Classical Novels
- **Commentary**: 脂砚斋 (Zhiyan Zhai), 畸笏叟, and others from multiple manuscript sources

**NOTE**: This is the authentic 80-chapter version with Zhiping commentary, NOT the 120-chapter Cheng-Gao edition.

## Work Organization

**Work is organized by PDF PAGE, not by chapter.**
- One JSON file per PDF page: `translations/page_XXXX.json`
- Workers claim individual pages
- Each page goes through: RESEARCH → TRANSLATE → POLISH

---

## Target Languages

| Language | Code | Notes |
|----------|------|-------|
| Classical Chinese (Original) | `original` | Source text |
| Modern Chinese (Simplified) | `zh_modern` | 简体中文 |
| English | `en` | Scholarly literary |
| Russian | `ru` | Literary Russian |
| Japanese | `ja` | Classical-influenced |

---

## PDF Structure

| Section | Content | Notes |
|---------|---------|-------|
| Front Matter | 凡例, prefaces, editorial notes | First pages |
| 第一回 - 第八十回 | The 80 chapters with commentary | Main body |
| Appendices | Variant readings, scholarly notes | End section |

### Chapter Overview (八十回)

| Chapter Range | Content Summary |
|--------------|-----------------|
| 1-5 | Frame narrative: Stone's origin, Zhen Shiyin, Jia Yucun |
| 6-12 | Lin Daiyu arrives, family introductions |
| 13-18 | Qin Keqing's death, Grand View Garden |
| 19-27 | Garden life, Daiyu-Baoyu relationship |
| 28-40 | Poetry clubs, festivals, peak prosperity |
| 41-54 | Social gatherings, Xue Pan's troubles |
| 55-70 | Decline begins, deaths and departures |
| 71-80 | Deepening sorrows, foreshadowing

---

## Main Character Reference

| Name | Relation | Notes |
|------|----------|-------|
| 贾宝玉 (Jia Baoyu) | Protagonist | Born with jade in mouth |
| 林黛玉 (Lin Daiyu) | Cousin, love interest | Sickly, poetic, sensitive |
| 薛宝钗 (Xue Baochai) | Cousin, eventual wife | Practical, composed |
| 王熙凤 (Wang Xifeng) | Baoyu's cousin-in-law | Powerful manager |
| 贾母 (Grandmother Jia) | Family matriarch | Dotes on Baoyu and Daiyu |
| 史湘云 (Shi Xiangyun) | Cousin | Lively, tomboy-ish |
| 妙玉 (Miaoyu) | Nun | Proud, artistic |
| 袭人 (Xiren) | Baoyu's chief maid | Loyal, sensible |
| 晴雯 (Qingwen) | Baoyu's maid | Spirited, tragic |

See `research/character_guide.md` for complete character profiles.

---

## Resources Available

### Source Material (Work Directly from PDF)
- `红楼梦脂评汇校本_有书签目录_v3.13.pdf` - Original source PDF with bookmarks

**IMPORTANT**: Work directly from PDF pages or screenshots, NOT extracted text. The complex commentary formatting (眉批, 夹批, 侧批, etc.) with multiple manuscript source tags (【甲戌】【庚辰】etc.) is best preserved by visual inspection.

### Page Images (Optional)
- `source_pages/page_XXXX.png` - PDF pages as images (for AI workers that read images)
- Workers can also open the PDF directly

### Research Documents
- `research/glossary.md` - Character names & terminology in all languages
- `research/chapter_structure.md` - Chapter titles and detailed summaries
- `research/cultural_context.md` - Qing Dynasty cultural context
- `research/character_guide.md` - Complete character profiles
- `research/poetry_guide.md` - Poetry translation approaches
- `research/existing_translations.md` - Reference existing translations

### Example Translations (Format Reference)
- `examples/chapter_001_example.json` - Example JSON format

### PDF Generation Tools
- `tools/compile_chapters.py` - JSON to PDF compiler
- `tools/extract_text.py` - PDF text extraction
- `tools/README.md` - Tool documentation

---

## Translation Output Location

Workers save translations to:
```
translations/
├── chapter_001.json
├── chapter_002.json
└── ...
```

Generated PDFs go to:
```
output/
├── chapter_001.pdf
├── chapter_002.pdf
└── ...
```

---

## Protocol Summary

1. **Register**: Create WORKER_STATE.md to join the team
2. **Sync**: Fetch other workers every 2-3 minutes
3. **Claim**: Take lowest available chapter, push immediately
4. **Translate**: Classical Chinese → Modern Chinese, English, Russian, Japanese
5. **Complete**: Save JSON, push, claim next chapter
6. **Repeat**: Until all 120 chapters are done

See `PROTOCOL.md` for full details.

---

## Timeouts

| Situation | Threshold |
|-----------|-----------|
| Worker considered offline | 10 min stale heartbeat |
| Chapter can be reclaimed | 15 min after worker goes offline |
| Sync frequency | 2-3 minutes |
| Heartbeat update | At least every 5 min |

---

## Quality Checkpoints

Before pushing a completed chapter, verify:
- [ ] All segments translated in all 4 target languages
- [ ] Poetry properly formatted with notes
- [ ] Character names consistent with glossary
- [ ] Commentary (脂评) translated
- [ ] JSON validates without errors
- [ ] No empty or null fields

---

*Each worker maintains their own `WORKER_STATE.md` for detailed status.*
