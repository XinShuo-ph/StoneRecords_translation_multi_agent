# 🚀 Translation Quick Start Card

**For AI Agents: Start translating in 5 minutes**

---

## ⚡ 3-Minute Setup

1. **Read this card** (you're doing it now!)
2. **Review one example**: `examples/page_0020_with_commentary.json`
3. **Start translating!**

---

## 📋 6-Step Workflow (Per Page)

```
1. VIEW   → Open page image (source_pages/page_XXXX.png)
2. READ   → Identify all text (main + commentary)
3. TRANSLATE → 4 languages (zh/en/ru/ja)
4. SAVE   → translations/page_XXXX.json
5. VALIDATE → python3 tools/validate_json.py [file]
6. NEXT   → Immediately start next page
```

**Time target**: 15-25 minutes per page (Tier 2 quality)

---

## ✅ Validation Checklist (Before Next Page)

Run validation:
```bash
python3 tools/validate_json.py translations/page_0020.json
```

Must pass:
- ✅ Valid JSON syntax
- ✅ All 4 languages present (zh_modern, en, ru, ja)
- ✅ No empty translations
- ✅ Sequential segment IDs (1, 2, 3...)
- ✅ Page number matches file name

If ✅ all checks → Next page
If ❌ any check → Fix errors and retry

---

## 🎯 Quality Tiers (Know Your Target)

### Tier 1: Minimum Acceptable
- All main text translated ✅
- All 4 languages ✅
- Valid JSON ✅

### Tier 2: Good (YOUR TARGET)
- All above ✅
- Commentary translated ✅
- Research notes for puns/allusions ✅

### Tier 3: Excellent (Bonus)
- All above ✅
- Deep research notes ✅
- Poetry analysis ✅

**Aim for Tier 2** on every page.

---

## 📄 JSON Format (Minimal Required)

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "...",
      "zh_modern": "...",
      "en": "...",
      "ru": "...",
      "ja": "..."
    }
  ]
}
```

**Add commentary and notes for Tier 2** (see examples).

---

## 🔍 Research Protocol

### REQUIRED (every page, 2 min):
- Check `research/glossary.md` for character names
- Note chapter context
- Identify character name puns

### CONDITIONAL (only when seen, <5 min):
- Classical allusion → research + note
- Wordplay/pun → research + note
- Cryptic commentary → research to understand

**Time limit**: Max 5 min per segment. If stuck, add "Uncertain: [question]" and continue.

---

## 🎓 Translation Style by Language

| Language | Style | Name Format | Example |
|----------|-------|-------------|---------|
| **简体中文** | Modern standard, keep elegance | 贾宝玉 | 这是开篇的第一回。 |
| **English** | Scholarly literary | Jia Baoyu (Pinyin) | This is the opening chapter. |
| **Русский** | Literary, aristocratic register | Цзя Баоюй | Это первая глава. |
| **日本語** | Classical-influenced | 賈宝玉 (音読み) | これが第一回である。 |

---

## ⚙️ Key Terms (Use Consistently)

| Original | Zh Modern | English | Russian | Japanese |
|----------|-----------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子 |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 老爷 | 老爷 | master | господин | 旦那様 |
| 太太 | 太太 | madam | госпожа | 奥様 |

Full list: `research/glossary.md`

---

## ❌ Common Mistakes to Avoid

1. ❌ **Skipping content** → Translate EVERYTHING on page
2. ❌ **Empty fields** → All translations must have content
3. ❌ **Wrong page number** → Triple-check before starting
4. ❌ **No validation** → Always validate before next page
5. ❌ **Inconsistent names** → Use glossary
6. ❌ **Stopping after 1 page** → Continue immediately

---

## 🔄 Continuous Work Mode

After each page:
1. Save JSON
2. Validate
3. If ✅ pass → **Immediately start next page**
4. If ❌ fail → Fix and retry

**DO NOT**:
- Pause between pages
- Ask for confirmation
- Wait for feedback
- Stop to review

**ONLY STOP** when:
- All assigned pages complete
- Blocking error you can't resolve
- Context limit approaching

---

## 📚 Full Documentation

**Essential reading** (~25 min total):
- `TRANSLATION_INSTRUCTIONS_V2.md` - Core workflow (10 min)
- `TRANSLATION_SCHEMA.md` - JSON schema (8 min)
- `examples/` - Review 2-3 examples (7 min)

**Reference materials** (use as needed):
- `TRANSLATION_VALIDATION.md` - Validation details
- `research/glossary.md` - Terms and names
- `research/character_guide.md` - Character info

---

## 💡 Pro Tips

1. **Speed up**: After 3-5 pages, you'll hit 15-20 min/page
2. **Commentary**: Small text with 【甲戌】【庚辰】markers
3. **Poetry**: Note form/rhyme in `poem_notes`
4. **Stuck on research?** Max 5 min, then note "Uncertain: [question]"
5. **Validation errors?** Read the error message—it tells you exactly what to fix

---

## 🎯 Success Criteria

**You're doing well if**:
- ✅ Validation passes on first try
- ✅ 15-25 minutes per page
- ✅ Tier 2 quality consistently
- ✅ Working continuously (no pauses)

**You might need to slow down if**:
- ❌ Validation fails repeatedly
- ❌ Missing content on pages
- ❌ Empty translation fields
- ❌ Taking >40 min per page

**Target: Tier 2 at 20 min/page average**

---

## 🆘 Quick Help

**Q: File naming?**
A: `page_0020.json` (4 digits, zero-padded)

**Q: What's good enough?**
A: Validation passes = Tier 1 ✅. Add commentary + notes = Tier 2 ✅.

**Q: Can I skip commentary?**
A: For Tier 1, yes. For Tier 2 (your target), no.

**Q: How many segments per page?**
A: However many sentences/paragraphs are on the page. All of them.

**Q: Validation failed, what now?**
A: Read the error message. It tells you exactly what's missing/wrong. Fix and retry.

---

## 🚀 Ready to Start?

1. ✅ Read this card
2. ✅ Review `examples/page_0020_with_commentary.json`
3. ✅ Open your first page image
4. ✅ Start translating!

**Remember**: View → Translate → Save → Validate → Next

**Good luck! 加油！**
