# Research Resources

This document lists available research materials. **Don't read all files at once** - reference them as needed during translation.

---

## Available in Repository

### Core References

| File | Content | When to Use |
|------|---------|-------------|
| `research/glossary.md` | Character names, titles, terminology | When encountering character names or formal titles |
| `research/chapter_structure.md` | Chapter titles and summaries | To identify which chapter you're in |
| `research/character_guide.md` | Main character profiles and relationships | When characters are introduced or interact |
| `research/poetry_guide.md` | Poetry forms and translation approaches | When translating verse |
| `research/commentary_guide.md` | Commentary sources (甲戌本, 庚辰本, etc.) | When identifying commentary annotations |
| `research/cultural_context.md` | Qing dynasty customs, hierarchy, ceremonies | When encountering cultural practices |
| `research/existing_translations.md` | Reference to Hawkes, Yang, others | For comparison and difficult passages |

### Examples

| File | Content | When to Use |
|------|---------|-------------|
| `examples/page_0020.json` | Complete page translation with commentary | As JSON structure reference |

---

## Workflow: Research During Translation

### Step 1: Quick Scan
1. Open the page (PDF or `source_pages/page_XXXX.png`)
2. Identify main elements: prose, poetry, commentary

### Step 2: Character Names
- First occurrence? → Check `research/glossary.md` for correct transliteration
- Unfamiliar relationship? → Check `research/character_guide.md`

### Step 3: Cultural Context
- Ceremonial event? → Reference `research/cultural_context.md`
- Social custom? → Reference `research/cultural_context.md`
- Formal title? → Reference `research/glossary.md`

### Step 4: Poetry
- Verse form? → Check `research/poetry_guide.md` for structure
- Classical allusion? → Search online or reference `research/cultural_context.md`

### Step 5: Commentary
- Manuscript source? → Identify from markers (【甲戌】【庚辰】)
- Need context? → Reference `research/commentary_guide.md`

### Step 6: Difficult Passages
- Search online: "[passage text] 红楼梦 解释"
- Check existing translations (Hawkes Vol. 1-3, Yang Xianyi)
- Academic resources: RedologyNet, CText, CBETA

---

## Online Resources

### Classical Chinese Dictionaries
- **汉典** (zdic.net) - Comprehensive character dictionary
- **教育部重編國語辭典** - Classical meanings
- **CText (ctext.org)** - Chinese Text Project with concordances

### 红楼梦-Specific
- **RedologyNet** - Academic articles and interpretations
- **红楼梦研究 (Hongloumeng Yanjiu)** - Scholarly journal archive
- **百度百科: 红楼梦** - Quick reference for characters and plot

### Existing Translations (for comparison)
- **David Hawkes** (The Story of the Stone, Vol. 1-3)
- **Yang Xianyi & Gladys Yang** (A Dream of Red Mansions)
- **John Minford** (The Story of the Stone, Vol. 4-5)

### Poetry References
- Classical Chinese poetry databases
- Rhyme dictionaries for Classical Chinese
- Comparative translations of Tang/Song poetry

---

## Research Tips

### For Allusions (典故)

1. Search: "[phrase] 典故" or "[phrase] 出处"
2. Check if it references:
   - Classical texts (论语, 诗经, etc.)
   - Historical events
   - Earlier literature

### For Puns (谐音)

1. Look for character names that sound like phrases
2. Check commentary for hints (often annotated)
3. Search: "[character name] 谐音"

Example: 贾雨村 (Jia Yucun) = 假语存 (false words remain)

### For Social Customs

1. Identify the context (wedding, funeral, festival, etc.)
2. Reference `research/cultural_context.md`
3. Search: "[custom] 清朝" or "[custom] 红楼梦"

### For Poetry Forms

1. Count characters per line (5-char or 7-char most common)
2. Count lines (4 lines = 绝句, 8 lines = 律诗)
3. Check `research/poetry_guide.md` for form rules
4. Search: "[poem first line] 红楼梦" for existing analyses

---

## Time Management

### Budget Per Page: 45-60 minutes

- View/scan: 2-3 min
- Research: 10-15 min
- Translate main text: 20-25 min
- Translate commentary: 5-10 min
- Review/polish: 5-8 min
- Save JSON: 1-2 min

### If Taking Too Long

- Set 5-minute limit per difficult passage
- Make best interpretation
- Note uncertainty in `notes` field
- Move on

**Goal**: 1-1.5 pages per hour sustained pace

---

## Documentation in `notes` Field

Always document:

1. **Character name puns** discovered
2. **Allusions** identified (source text)
3. **Cultural practices** explained
4. **Uncertainties** or alternate interpretations
5. **Literary techniques** observed

### Good `notes` Examples

```json
"notes": [
  "贾雨村 pun on 假语存 (false words remain) - metafictional hint",
  "霍启 = 祸起 (disaster begins), foreshadows Yinglian's kidnapping",
  "Allusion to 洛神赋 in description of Tanchun ('shoulders as if carved')",
  "元宵节 (Lantern Festival) - 15th day of 1st lunar month, family reunion theme",
  "Uncertain: '三劫' may mean 90 years or Buddhist kalpas; commentary incomplete on this page"
]
```

### Poor `notes` Examples

❌ `"Translated page 20"` - Not a research finding  
❌ `"Good quality translation"` - Not useful  
❌ `"See commentary for details"` - Commentary should be translated, not referenced  
❌ Empty array `[]` - Always document at least one finding  

---

## Quick Reference: Character Names

### Jia Family (贾府)

**Generation 1 (Grandparents)**:
- 贾母 (Jia Mu) = Grandmother Jia, née Shi (史太君)

**Generation 2 (Parents)**:
- 贾赦 (Jia She) = Eldest son, married to 邢夫人 (Lady Xing)
- 贾政 (Jia Zheng) = Second son, married to 王夫人 (Lady Wang)

**Generation 3 (Grandchildren)**:
- 贾宝玉 (Jia Baoyu) = Protagonist, son of Jia Zheng
- 贾珠 (Jia Zhu) = Deceased, son of Jia Zheng, married to 李纨 (Li Wan)
- 贾迎春 (Jia Yingchun) = Eldest daughter
- 贾探春 (Jia Tanchun) = Second daughter
- 贾惜春 (Jia Xichun) = Third daughter

### Lin Family (林府)

- 林黛玉 (Lin Daiyu) = Female protagonist, granddaughter of Jia Mu
- 林如海 (Lin Ruhai) = Daiyu's father (deceased)

### Others

- 薛宝钗 (Xue Baochai) = Female lead, cousin of Baoyu
- 王熙凤 (Wang Xifeng) = Jia Lian's wife, major character

**See `research/character_guide.md` for complete list.**

---

**Return to `01_core_task.md` for workflow.**
