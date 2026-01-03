# 红楼梦 (Dream of the Red Chamber) Translation Project

## Objective

Deliver a multilingual edition of 红楼梦脂评汇校本 (Dream of the Red Chamber, with Zhiping Commentaries) translated into:
- **Modern Chinese (简体中文)**: Accessible contemporary Mandarin
- **English**: Literary, scholarly translation
- **Russian (Русский)**: Faithful literary translation  
- **Japanese (日本語)**: Classical-influenced literary Japanese

The final output presents each original Classical Chinese sentence followed by translations in all four languages, with scholarly annotations preserving the cultural richness of this masterpiece.

---

## Multi-Agent Collaborative Execution

**THIS PROJECT USES MULTIPLE AI AGENTS WORKING COLLABORATIVELY**

You are part of a team of workers translating this classic in parallel. You will:
1. **Discover** other workers and know who's online
2. **Claim** chapters to translate (one at a time)
3. **Sync** regularly to stay coordinated
4. **Share** your translations via git

See `PROTOCOL.md` for the complete communication protocol.

### Key Principles

- **Collaborative, not isolated**: You know who else is working and what they're doing
- **Simple workload**: Each worker claims chapters (lowest available first)
- **Robust**: If workers disconnect, others can reclaim their chapters
- **Sync regularly**: Fetch other workers' states every 2-3 minutes

---

## Quick Start (Agent Startup Sequence)

### Step 1: Identify Yourself
```bash
MY_BRANCH=$(git branch --show-current)
MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
echo "I am: $MY_SHORT_ID on $MY_BRANCH"
```

### Step 2: Create WORKER_STATE.md
Copy from `WORKER_STATE_TEMPLATE.md` and fill in your details. This **registers you as an active worker**.

### Step 3: Sync & Discover Other Workers
```bash
git fetch origin --prune

# Find all active workers
for branch in $(git branch -r | grep 'origin/cursor/' | sed 's|origin/||' | tr -d ' '); do
  if git show "origin/${branch}:WORKER_STATE.md" &>/dev/null 2>&1; then
    short_id=$(echo "$branch" | grep -oE '[^-]+$' | tail -c 5)
    echo "Active worker: $short_id ($branch)"
  fi
done
```

### Step 4: Register Yourself
```bash
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] SYNC: Registering as active worker
HEARTBEAT: $(date +%s)"
git push origin HEAD
```

### Step 5: Claim a Chapter and Start Translating
1. Find the lowest chapter number not claimed or completed
2. Update WORKER_STATE.md with your claim
3. Push immediately
4. Start translating!

---

## Source Material

**Source Text**: 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary Collation)
- **Author**: 曹雪芹 (Cao Xueqin), with continuation attributed to 高鹗 (Gao E)
- **Era**: Qing Dynasty, mid-18th century
- **Total Chapters**: 120 chapters (前80回 by Cao Xueqin, 后40回 traditionally attributed to Gao E)
- **Genre**: Classical Chinese novel, considered one of the Four Great Classical Novels of Chinese literature
- **Commentary**: Zhiyan Zhai (脂砚斋) commentaries included

### Text Extraction Required
The source PDF needs text extraction before translation can begin. Workers should:
1. Extract chapter text from `红楼梦脂评汇校本_有书签目录_v3.13.pdf`
2. Save to `extracted/chapters/chapter_XXX.txt`
3. Maintain original formatting including commentary markers

---

## File Structure

```
workspace/
├── instructions.md           # This file (read-only)
├── PROTOCOL.md               # Communication protocol (read-only)
├── STATE.md                  # Global project state
├── WORKER_STATE.md           # YOUR worker state (update frequently!)
├── WORKER_STATE_TEMPLATE.md  # Template for new workers
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf  # Original source
│
├── extracted/                # EXTRACTED TEXT
│   ├── full.txt              # Complete book text
│   └── chapters/
│       ├── chapter_001.txt   # 第一回
│       ├── chapter_002.txt   # 第二回
│       └── ...               # through chapter_120.txt
│
├── research/                 # BACKGROUND RESEARCH
│   ├── glossary.md           # Character names & terminology
│   ├── chapter_structure.md  # Chapter titles and summaries
│   ├── cultural_context.md   # Qing Dynasty context
│   ├── character_guide.md    # Main character profiles
│   ├── poetry_guide.md       # Approach to poetry translation
│   └── existing_translations.md  # Reference to existing works
│
├── examples/                 # FORMAT EXAMPLES
│   ├── chapter_001_example.json
│   └── format_demo.tex
│
├── tools/                    # PDF GENERATION
│   ├── compile_chapters.py
│   ├── extract_text.py
│   └── README.md
│
├── translations/             # YOUR OUTPUT (translations go here)
│   ├── chapter_001.json
│   ├── chapter_002.json
│   └── ...
│
└── output/                   # GENERATED PDFs
    ├── chapter_001.pdf
    └── ...
```

---

## Your Task: TRANSLATE

### The Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. SYNC: Fetch all branches, see who's online              │
│  2. CLAIM: Take the lowest available chapter                │
│  3. READ: Get the Classical Chinese text from extracted/    │
│  4. TRANSLATE: Classical Chinese → Modern Chinese,          │
│               English, Russian, Japanese                    │
│  5. ANNOTATE: Add scholarly notes for cultural references   │
│  6. SAVE: Write translations/chapter_XXX.json               │
│  7. BROADCAST: Commit & push, update WORKER_STATE.md        │
│  8. REPEAT: Claim next chapter                              │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step for Each Chapter

#### 1. Read the Extracted Text
```bash
cat extracted/chapters/chapter_001.txt
```

#### 2. Parse Into Segments
Divide the chapter into logical segments:
- Each prose paragraph becomes one segment
- Each poem/verse is a separate segment
- Commentary (脂评) kept with its associated text

#### 3. Translate Each Segment
For each Classical Chinese segment, produce:
- **Modern Chinese (简体)**: Clear, accessible modern Mandarin
- **English**: Scholarly literary English
- **Russian**: Literary Russian
- **Japanese**: Literary Japanese with classical influences

#### 4. Add Annotations
- Cultural context notes
- Character relationship clarifications
- Historical references
- Poetry interpretation

#### 5. Save as JSON
Save to `translations/chapter_XXX.json` using the exact format below.

---

## JSON Output Format (MANDATORY)

Every chapter translation MUST follow this structure:

```json
{
  "chapter": 1,
  "chapter_title": {
    "original": "甄士隐梦幻识通灵 贾雨村风尘怀闺秀",
    "zh_modern": "甄士隐在梦幻中认识了通灵宝玉，贾雨村在落魄时怀念闺中秀女",
    "en": "Zhen Shiyin in a Dream Perceives the Jade of Spiritual Understanding; Jia Yucun in Humble Circumstances Thinks Fondly of a Beautiful Maiden",
    "ru": "Чжэнь Шиинь во сне постигает волшебную яшму; Цзя Юйцунь в бедности вспоминает прекрасную деву",
    "ja": "甄士隠、夢幻の中で通霊を識り、賈雨村、風塵にありて閨秀を懐う"
  },
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "此开卷第一回也。作者自云：因曾历过一番梦幻之后，故将真事隐去，而借通灵之说，撰此《石头记》一书也。",
      "zh_modern": "这是开篇的第一回。作者自己说：因为曾经经历过一番梦幻般的往事之后，所以将真实的事情隐藏起来，借用通灵宝玉的传说，撰写了这部《石头记》。",
      "en": "This is the first chapter of the opening. The author himself says: Having once passed through a dreamlike experience, he concealed the true events and, borrowing the tale of the Spiritual Jade, composed this book called 'The Story of the Stone.'",
      "ru": "Это первая глава книги. Автор сам говорит: пережив некогда череду грёз, он скрыл истинные события и, позаимствовав легенду о волшебной яшме, написал эту книгу под названием «Записки о камне».",
      "ja": "これが冒頭の第一回である。作者自ら言う：かつて夢幻のような経験を経た後、真実を隠し、通霊の説を借りて、この『石頭記』一書を著したのだと。",
      "zhiping_commentary": "脂批：能解者方有辛酸之泪...",
      "zhiping_translation": {
        "zh_modern": "脂砚斋评注：能够理解的人才会流下辛酸的眼泪...",
        "en": "Zhiyan Zhai commentary: Only those who truly understand will shed tears of bitterness...",
        "ru": "Комментарий Чжиянь Чжай: Лишь тот, кто поймёт, прольёт горькие слёзы...",
        "ja": "脂硯斎評：理解できる者のみが辛酸の涙を流すであろう..."
      }
    },
    {
      "id": 2,
      "type": "poem",
      "original": "满纸荒唐言，一把辛酸泪。都云作者痴，谁解其中味？",
      "zh_modern": "满纸都是荒唐的话语，包含着一把辛酸的眼泪。人们都说作者痴傻，谁能理解其中的滋味呢？",
      "en": "Pages full of idle words, / A handful of bitter tears. / All call the author mad— / Who understands the flavor here?",
      "ru": "Страницы полны вздора, / Слёзы горькие в них. / Все твердят: автор безумен— / Кто постигнет их вкус?",
      "ja": "紙に満つるは荒唐の言、/ 一掬の辛酸の涙。/ 皆は言う作者は痴と、/ 誰か解せんその中の味を。",
      "poem_notes": {
        "meter": "七言絶句 (Seven-character quatrain)",
        "rhyme_scheme": "AABA",
        "literary_devices": ["Self-deprecation", "Rhetorical question", "Metafiction"]
      }
    }
  ],
  "translator_notes": [
    "Chapter 1 establishes the frame narrative with the Stone's origin story",
    "甄士隐 (Zhen Shiyin) is a pun: 真事隐 (true events hidden)",
    "贾雨村 (Jia Yucun) is a pun: 假语村 (false words exist)"
  ],
  "character_appearances": ["甄士隐", "贾雨村", "甄英莲", "封氏", "娇杏"],
  "total_segments": 2,
  "segment_types": {
    "prose": 1,
    "poem": 1
  }
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `chapter` | int | Chapter number (1-120) |
| `chapter_title` | object | Title in all languages |
| `segments` | array | Array of segment objects |
| `segments[].id` | int | Sequential ID (1, 2, 3, ...) |
| `segments[].type` | string | "prose", "poem", "dialogue", "commentary" |
| `segments[].original` | string | Original Classical Chinese text |
| `segments[].zh_modern` | string | Modern Chinese translation |
| `segments[].en` | string | English translation |
| `segments[].ru` | string | Russian translation |
| `segments[].ja` | string | Japanese translation |
| `translator_notes` | array | Context, cultural notes |
| `character_appearances` | array | Characters in this chapter |
| `total_segments` | int | Count of segments |

### Quality Rules

1. **Every segment has all 5 language versions** - no null/empty values
2. **Valid JSON** - escape special characters properly
3. **UTF-8 encoding** - CJK characters must render correctly
4. **No skipped content** - include EVERY segment from the chapter
5. **Sequential IDs** - 1, 2, 3, ... (no gaps)
6. **Preserve poetry structure** - maintain line breaks and verse forms

---

## Chapter Structure Reference

### Volume 1: 前八十回 (First 80 Chapters by Cao Xueqin)

| Chapters | Content |
|----------|---------|
| 1-5 | Frame narrative, Stone's origin, introduction to Jia family |
| 6-18 | Grand View Garden establishment, Lin Daiyu arrives |
| 19-27 | Development of Baoyu-Daiyu-Baochai triangle |
| 28-40 | Garden life, poetry clubs, festivals |
| 41-54 | Peak of prosperity, Xue Pan's troubles |
| 55-70 | Signs of decline, various tragedies |
| 71-80 | Deepening sorrows, deaths and partings |

### Volume 2: 后四十回 (Last 40 Chapters, attributed to Gao E)

| Chapters | Content |
|----------|---------|
| 81-90 | Transition period, examinations |
| 91-100 | Baoyu's marriage deception planned |
| 101-110 | Daiyu's death, Baoyu's wedding |
| 111-120 | Family's fall, Baoyu becomes monk, ending |

---

## Target Reader Profile

**Primary Audience:**
- International scholars and advanced students of Chinese literature
- Comparative literature researchers
- Readers familiar with at least one of the target languages
- Chinese heritage speakers seeking deeper understanding

**Cultural Bridge Goals:**
- Make Qing Dynasty culture accessible to international readers
- Preserve the literary sophistication and wordplay
- Provide scholarly apparatus for academic use
- Enable cross-cultural literary comparison

---

## Translation Quality Guidelines

### Voice and Style Preservation

红楼梦's distinctive qualities to preserve:
- **Elegant classical prose**: Balance between accessibility and literary quality
- **Psychological depth**: Subtle emotional nuances in dialogue
- **Symbolic richness**: Names, objects, and events carry deeper meanings
- **Poetic integration**: Poems that advance the narrative and character development
- **Social commentary**: Critique of feudal society embedded in the narrative

### Cultural Localization by Language

**Modern Chinese (简体中文):**
- 使用规范现代汉语，保留古典韵味
- 对难懂的古词给予注释
- 保留原有的典故和文化指涉
- Example: 金陵十二钗 → 保留原称，加注解释

**English:**
- Scholarly literary register, avoid excessive modernization
- Transliterate names consistently (use Pinyin)
- Provide cultural footnotes for untranslatable concepts
- Poetry: prioritize meaning over rhyme, indicate original meter
- Example: 金陵十二钗 → "Twelve Beauties of Jinling" with note

**Russian (Русский):**
- Literary Russian suitable for classical literature
- Follow established Sinological transliteration conventions
- Adapt honorifics to Russian literary conventions
- Preserve the aristocratic register of the original
- Example: 金陵十二钗 → "Двенадцать красавиц из Цзиньлина"

**Japanese (日本語):**
- Classical-influenced literary Japanese (文語的要素を含む)
- Leverage shared literary heritage with Classical Chinese
- Use appropriate kanji readings (音読み for names)
- Poetry: consider Japanese poetic traditions in translation
- Example: 金陵十二钗 → "金陵十二釵（きんりょうじゅうにさい）"

---

## Special Translation Challenges

### 1. Character Names (Puns and Meanings)

Many names in 红楼梦 contain hidden meanings:

| Name | Literal Meaning | Hidden Meaning |
|------|-----------------|----------------|
| 甄士隐 | Zhen Shiyin | 真事隐 (True events hidden) |
| 贾雨村 | Jia Yucun | 假语存 (False words remain) |
| 贾宝玉 | Jia Baoyu | 假宝玉 (False precious jade) |
| 林黛玉 | Lin Daiyu | 林中带玉 (Jade in the forest) |
| 薛宝钗 | Xue Baochai | 雪中宝钗 (Precious hairpin in snow) |
| 元春/迎春/探春/惜春 | Four Springs | Four seasons, four fates |

**Translation Approach**: Keep transliterated names with explanatory notes on first appearance.

### 2. Poetry Translation

The novel contains over 200 poems. Approach:
- Preserve the meaning first, form second
- Note original meter/rhyme scheme
- For important poems, provide multiple translation approaches
- Include original Chinese alongside for reference

### 3. Classical Chinese Grammar

- Handle classical particles (之、乎、者、也) appropriately
- Convert classical verb aspects to modern equivalents
- Preserve sentence rhythm where possible

### 4. Zhiping Commentary

The 脂评 (Zhiping commentaries) are valuable scholarly additions:
- Translate all commentary
- Distinguish commentary from main text
- Note which commentator when identifiable

---

## Common Terms Glossary (Summary)

See `research/glossary.md` for complete reference.

| Classical Chinese | Modern Chinese | English | Russian | Japanese |
|------------------|----------------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子・若君 |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | 丫鬟/婢女 | maidservant | служанка | 女中 |
| 老爷 | 老爷/大人 | master/lord | господин | 旦那様 |
| 太太 | 太太/夫人 | madam/lady | госпожа | 奥様 |
| 姨娘 | 姨娘/妾 | concubine | наложница | 側室 |
| 银子 | 银两/银子 | silver (taels) | серебро | 銀 |
| 府 | 府邸 | mansion/residence | особняк | 邸宅 |

---

## Collaboration Protocol Summary

### Regular Sync (Every 2-3 Minutes)
```bash
git fetch origin --prune
# Read other workers' WORKER_STATE.md files
# Update your "Known Workers" table
```

### Chapter Claiming
1. Sync first (always!)
2. Find lowest available chapter
3. Update WORKER_STATE.md with claim
4. Push immediately
5. Start translating

### Completing a Chapter
```bash
git add translations/chapter_XXX.json WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] DONE: Completed chapter XXX
HASH: $(sha256sum translations/chapter_XXX.json | cut -c1-8)
HEARTBEAT: $(date +%s)"
git push origin HEAD
```

---

## Anti-Patterns to Avoid

### Translation
- ❌ Skipping difficult passages - include EVERYTHING with notes
- ❌ Over-modernizing the language - preserve literary quality
- ❌ Inconsistent name translations - use the glossary
- ❌ Ignoring poetry structure - preserve verse forms
- ❌ Missing cultural context - add translator notes
- ❌ Invalid JSON - validate before committing

### Collaboration
- ❌ Claiming without syncing first
- ❌ Claiming multiple chapters at once
- ❌ Forgetting to push claims immediately
- ❌ Letting heartbeat go stale (>5 min)
- ❌ Working in isolation - sync every 2-3 min

---

## Context Efficiency

- Use `research/chapter_structure.md` for chapter overviews
- Use `research/glossary.md` for consistent terminology
- Use `research/character_guide.md` for character relationships
- If stuck on a passage > 10 minutes, add a translator note and continue
- Each chapter should take roughly 30-60 minutes depending on length and poetry content

---

## Continuous Execution Rules

**Do NOT pause** between chapters to ask for confirmation. Keep working:

1. Complete chapter → Push → Claim next → Repeat
2. Sync every 2-3 minutes between chapters
3. Continue until:
   - All chapters are translated, OR
   - A blocking error requires help, OR
   - Context limit (~10k tokens remaining)

---

## Session End Protocol

When ending your session (or running low on context):

1. **Complete current chapter** if possible
2. **Update WORKER_STATE.md** with final status
3. **Push everything**:
   ```bash
   git add .
   git commit -m "[$MY_SHORT_ID] SESSION_END: Completed chapters X-Y
   STATUS: [summary]
   HEARTBEAT: $(date +%s)"
   git push origin HEAD
   ```

If you can't complete your current chapter:
1. Update WORKER_STATE.md to release the claim
2. Push so others know the chapter is available

---

## Key Files Reference

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `WORKER_STATE.md` | Your status (claims, completions) | Every action |
| `PROTOCOL.md` | Communication rules | Read-only |
| `instructions.md` | Task instructions | Read-only |
| `translations/chapter_XXX.json` | Your output | Per chapter |
| `research/glossary.md` | Term consistency | Reference |
| `research/character_guide.md` | Character info | Reference |

---

*Start translating! Sync regularly, push often, and coordinate with your team. Together we bring this masterpiece to the world.*
