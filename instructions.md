# 红楼梦 (Dream of the Red Chamber) Translation Project

## Objective

Deliver a multilingual edition of 红楼梦脂评汇校本 (Dream of the Red Chamber, with Zhiping Commentaries) translated into:
- **Modern Chinese (简体中文)**: Accessible contemporary Mandarin
- **English**: Literary, scholarly translation
- **Russian (Русский)**: Faithful literary translation  
- **Japanese (日本語)**: Classical-influenced literary Japanese

The final output presents each original Classical Chinese sentence followed by translations in all four languages, with scholarly annotations preserving the cultural richness of this masterpiece.

---

## Source Material Structure

**IMPORTANT**: The 脂评汇校本 contains:
- **Front matter**: Title pages, prefaces, editorial notes (凡例), etc.
- **80 chapters** (八十回): The authentic Cao Xueqin text with Zhiping commentary
- **Appendices**: Additional scholarly materials, variant readings, etc.

This is NOT the 120-chapter version. Work is organized by **PDF page**, not by chapter.

---

## Multi-Agent Collaborative Execution

**THIS PROJECT USES MULTIPLE AI AGENTS WORKING COLLABORATIVELY**

You are part of a team of workers translating this classic in parallel. You will:
1. **Discover** other workers and know who's online
2. **Claim** PDF pages to translate (one at a time)
3. **Sync** regularly to stay coordinated
4. **Share** your translations via git

See `PROTOCOL.md` for the complete communication protocol.

### Key Principles

- **Collaborative, not isolated**: You know who else is working and what they're doing
- **Page-based workload**: Each worker claims PDF pages (lowest available first)
- **Robust**: If workers disconnect, others can reclaim their pages
- **Sync regularly**: Fetch other workers' states every 2-3 minutes

---

## Quick Start (Agent Startup Sequence)

### ⚠️ STEP 0: START THE SYNC DAEMON FIRST! (MANDATORY)

> **CRITICAL**: Previous sessions had **83% wasted effort** because workers didn't sync properly. The sync daemon is now **MANDATORY**.

```bash
# THIS MUST BE YOUR FIRST ACTION
python3 tools/sync_daemon.py --start &
sleep 30  # Wait for initial sync to complete
```

The daemon will:
- Fetch all branches every 60 seconds
- Scan ALL worker branches for completed translations
- Maintain a global registry of completed/claimed pages
- Auto-push your changes every 3 minutes
- Prevent you from claiming pages that are already done

### Step 1: Identify Yourself
```bash
MY_BRANCH=$(git branch --show-current)
MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
echo "I am: $MY_SHORT_ID on $MY_BRANCH"
```

### Step 2: Create WORKER_STATE.md
Copy from `WORKER_STATE_TEMPLATE.md` and fill in your details. This **registers you as an active worker**.

### Step 3: Check Global Progress (Using Daemon)
```bash
# See what's already been done across ALL branches
python3 tools/sync_daemon.py --status

# Get the next ACTUALLY available page
NEXT_PAGE=$(python3 tools/sync_daemon.py --next-page)
echo "Next available page: $NEXT_PAGE"
```

### Step 4: Register Yourself
```bash
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] SYNC: Registering as active worker
HEARTBEAT: $(date +%s)"
git push origin HEAD
```

### Step 5: Claim a PDF Page (After Verification!)
```bash
# MANDATORY: Verify page is available before claiming
python3 tools/sync_daemon.py --check-page $NEXT_PAGE

# If available, update WORKER_STATE.md with your claim
# Then push immediately
```

1. ✓ Verify page is available (using daemon)
2. Update WORKER_STATE.md with your claim
3. Push immediately
4. Start the research-translate-polish workflow!

---

## Source Material

**Source Text**: 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary Collation)
- **Author**: 曹雪芹 (Cao Xueqin)
- **Era**: Qing Dynasty, mid-18th century
- **Total Content**: **80 chapters (八十回)** plus front matter and appendices
- **Genre**: Classical Chinese novel, one of the Four Great Classical Novels
- **Commentary**: Multiple manuscript sources collated (脂砚斋、畸笏叟、etc.)

**NOTE**: This is the authentic 80-chapter version, NOT the 120-chapter Cheng-Gao edition.

### PDF Structure

The source PDF `红楼梦脂评汇校本_有书签目录_v3.13.pdf` contains:

| Section | Content | Approximate Pages |
|---------|---------|-------------------|
| Front Matter | 凡例, prefaces, editorial notes | First ~10-15 pages |
| 第一回 - 第八十回 | The 80 chapters with commentary | Main body |
| Appendices | Variant readings, scholarly notes | End section |

### Working Directly from PDF Pages

**IMPORTANT**: Due to the complex formatting with multiple commentary sources and annotation tags, workers must work **directly from PDF pages or screenshots**.

The source PDF contains:
- **Main text** (正文): The novel's narrative
- **Interlinear comments** (夹批): Comments inserted within lines
- **Marginal comments** (眉批/侧批): Comments in margins
- **Chapter-end comments** (回末批): Comments at chapter ends
- **Source indicators**: Tags like 【甲戌】【庚辰】【己卯】indicating manuscript sources

**Why PDF/Image-based workflow?**
1. Preserves exact positioning of commentary
2. Shows source manuscript indicators clearly
3. Maintains relationship between text and annotations
4. Avoids OCR errors in classical Chinese
5. Workers can see the full context visually

### Work Units: PDF Pages

**Work is organized by PDF PAGE, not by chapter.**

Each worker claims individual PDF pages. One JSON file = one PDF page translated.

---

## File Structure

```
workspace/
├── instructions.md           # This file (read-only)
├── PROTOCOL.md               # Communication protocol (read-only)
├── STATE.md                  # Global project state
├── WORKER_STATE.md           # YOUR worker state (update frequently!)
├── WORKER_STATE_TEMPLATE.md  # Template for new workers
├── 红楼梦脂评汇校本_有书签目录_v3.13.pdf  # Original source PDF (80回 + front/back matter)
│
├── source_pages/             # PDF PAGES AS IMAGES (for direct viewing)
│   ├── page_0001.png         # Individual page screenshots
│   ├── page_0002.png
│   └── ...                   # Workers can also read PDF directly
│
├── research/                 # GENERAL REFERENCE (use as starting point)
│   ├── glossary.md           # Character names & terminology
│   ├── chapter_structure.md  # Chapter titles and summaries
│   ├── cultural_context.md   # Qing Dynasty context
│   ├── character_guide.md    # Main character profiles
│   ├── poetry_guide.md       # Approach to poetry translation
│   ├── commentary_guide.md   # Guide to commentary sources & tags
│   └── existing_translations.md  # Reference to existing works
│
├── examples/                 # FORMAT EXAMPLES
│   └── page_example.json     # Single page translation example
│
├── tools/                    # PROCESSING TOOLS
│   ├── compile_pages.py      # JSON → PDF compiler
│   ├── pdf_to_images.py      # Extract PDF pages as images
│   ├── validate_json.py      # Validate translation JSON
│   └── README.md
│
├── translations/             # YOUR OUTPUT (one JSON per PDF page)
│   ├── page_0001.json        # Front matter page 1
│   ├── page_0002.json        # Front matter page 2
│   ├── ...
│   ├── page_0015.json        # First page of 第一回
│   └── ...
│
└── output/                   # GENERATED PDFs
    └── ...
```

---

## Your Task: RESEARCH → TRANSLATE → POLISH

### The Workflow

**This is a scholarly translation of one of world literature's greatest masterpieces. Every sentence is highly nuanced and requires careful study.**

```
┌─────────────────────────────────────────────────────────────┐
│  1. SYNC: Fetch all branches, see who's online              │
│  2. CLAIM: Take the lowest available PDF page               │
│  3. VIEW: Open the PDF page (reader or image)               │
│  4. READ: Carefully read the page, noting all content       │
│  5. RESEARCH: For EACH sentence:                            │
│     - Search online for scholarly interpretations           │
│     - Study literary allusions and historical context       │
│     - Understand the nuanced meaning                        │
│     - Document non-trivial findings                         │
│  6. TRANSLATE: Only after research, translate to 4 langs   │
│  7. POLISH (润色): Improve translations for:                │
│     - Literary and artistic quality                         │
│     - Cultural fit for each target audience                 │
│     - Preservation of original artistry                     │
│  8. SAVE: Write translations/page_XXXX.json                 │
│  9. BROADCAST: Commit & push, update WORKER_STATE.md        │
│  10. REPEAT: Claim next page                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step for Each PDF Page

### Step 1: View the PDF Page

**Option A**: Open the PDF directly
```bash
# Use any PDF reader to navigate to your claimed page
# The PDF has bookmarks for easy navigation
```

**Option B**: Use pre-extracted page images
```bash
ls source_pages/page_00*.png
```

**Option C**: AI workers can read PDF pages as images directly

### Step 2: Identify All Content

For each PDF page, identify:

| Element | Description | How to Recognize |
|---------|-------------|------------------|
| **正文** (Main text) | The novel's narrative | Larger font, main body |
| **夹批** (Interlinear) | Comments within text | Smaller font inline, often in【】 |
| **眉批** (Top marginal) | Comments at page top | Top margin |
| **侧批** (Side marginal) | Comments at sides | Side margins |
| **回末批** (Chapter-end) | Comments after chapter | After chapter conclusion |
| **Source tags** | Manuscript indicators | 【甲戌】【庚辰】【己卯】【蒙府】etc. |

---

### Step 3: RESEARCH (Critical Step - Do Not Skip!)

**红楼梦 has the highest literary value in Chinese literature. Every sentence is carefully crafted with multiple layers of meaning.**

For EACH sentence on the page:

#### 3a. Online Research
- Search for scholarly interpretations of the specific passage
- Look up classical allusions (典故) referenced
- Find historical context for events/customs mentioned
- Check existing translations' approaches (for reference only)

#### 3b. Literary Analysis
- Identify wordplay and puns (谐音, 双关)
- Note symbolic meanings (names, objects, numbers)
- Understand the emotional undertones
- Recognize foreshadowing (伏笔) and callbacks (照应)

#### 3c. Commentary Study
- Read ALL commentary on the page carefully
- The 脂评 often reveals hidden meanings
- Note which manuscript source provides each comment
- Commentary itself requires research

#### 3d. Document Findings
**If research discovers anything non-trivial, add it to `translator_notes` field:**
- Hidden meanings in names
- Historical/cultural context needed for understanding
- Literary allusions and their significance
- Connections to other parts of the novel
- Scholarly debates about interpretation

**Example research note:**
```json
"translator_notes": [
  "「青埂峰」is a pun on「情根」(root of passion) - 甲戌本 commentary confirms this",
  "The number 36,501 stones relates to the astronomical cycle - see Chen Yinke's research",
  "「荒唐」here echoes Zhuangzi's use of the term for transcendent truth"
]
```

---

### Step 4: TRANSLATE

**Only after thorough research**, translate each segment into all 4 languages:

- **Modern Chinese (简体)**: Clear, accessible modern Mandarin
- **English**: Scholarly literary English  
- **Russian (Русский)**: Literary Russian
- **Japanese (日本語)**: Literary Japanese with classical influences

**Translate ALL content**: main text AND all commentary!

---

### Step 5: POLISH (润色) - Critical for Quality

**After initial translation, systematically improve each translation:**

#### 5a. Literary Quality Review
- Does the translation capture the artistic beauty?
- Is the rhythm and flow preserved where possible?
- For poetry: is the structure and emotional impact maintained?
- Does it read as literature, not just accurate text?

#### 5b. Cultural Adaptation by Language

**Modern Chinese (简体中文)**:
- 确保现代读者能理解古典意涵
- 保留原文的文学韵味
- 注释难懂的典故和词汇

**English**:
- Consider Western literary traditions
- Maintain scholarly register without being dry
- Poetry should feel like poetry to English readers
- Cultural footnotes for concepts with no English equivalent

**Russian (Русский)**:
- Draw on Russian classical literature traditions
- Adapt to Russian literary conventions
- Consider how 19th-century Russian novels handled similar themes
- Use appropriate register for aristocratic settings

**Japanese (日本語)**:
- Leverage shared classical Chinese literary heritage
- Use appropriate 文語 elements for literary effect
- Consider how classical Japanese literature handles similar themes
- Poetry translation should resonate with Japanese poetic traditions

#### 5c. Final Polish
- Read each translation aloud (mentally) - does it flow?
- Check consistency with glossary terms
- Verify no meaning was lost in pursuit of style
- Ensure all four translations convey the same core meaning

---

### Step 6: Save as JSON

Save to `translations/page_XXXX.json` (4-digit page number).

---

## JSON Output Format (MANDATORY)

**One JSON file per PDF page.** File naming: `page_XXXX.json` (4-digit page number)

```json
{
  "page": 15,
  "chapter": "第一回",
  "chapter_title": {
    "original": "甄士隐梦幻识通灵 贾雨村风尘怀闺秀",
    "zh_modern": "甄士隐在梦幻中认识了通灵宝玉，贾雨村在落魄时怀念闺中秀女",
    "en": "Zhen Shiyin in a Dream Perceives the Jade of Spiritual Understanding; Jia Yucun in Humble Circumstances Thinks Fondly of a Beautiful Maiden",
    "ru": "Чжэнь Шиинь во сне постигает волшебную яшму; Цзя Юйцунь в бедности вспоминает прекрасную деву",
    "ja": "甄士隠、夢幻の中で通霊を識り、賈雨村、風塵にありて閨秀を懐う"
  },
  "page_content_type": "chapter_body",
  "segments": [
    {
      "id": 1,
      "pdf_page": 15,
      "type": "prose",
      "original": "此开卷第一回也。作者自云：因曾历过一番梦幻之后，故将真事隐去，而借通灵之说，撰此《石头记》一书也。",
      "zh_modern": "这是开篇的第一回。作者自己说：因为曾经经历过一番梦幻般的往事之后，所以将真实的事情隐藏起来，借用通灵宝玉的传说，撰写了这部《石头记》。",
      "en": "This is the first chapter of the opening. The author himself says: Having once passed through a dreamlike experience, he concealed the true events and, borrowing the tale of the Spiritual Jade, composed this book called 'The Story of the Stone.'",
      "ru": "Это первая глава книги. Автор сам говорит: пережив некогда череду грёз, он скрыл истинные события и, позаимствовав легенду о волшебной яшме, написал эту книгу под названием «Записки о камне».",
      "ja": "これが冒頭の第一回である。作者自ら言う：かつて夢幻のような経験を経た後、真実を隠し、通霊の説を借りて、この『石頭記』一書を著したのだと。",
      "commentary": [
        {
          "type": "眉批",
          "source": "甲戌本",
          "position": "top margin",
          "original": "能解者方有辛酸之泪，哭成此书。壬午除夕，书未成，芹为泪尽而逝。",
          "zh_modern": "能够理解的人才会流下辛酸的眼泪，哭着写成这本书。壬午年除夕，书还没写完，曹芹便因泪尽而去世了。",
          "en": "Only those who truly understand will shed bitter tears—this book was wept into being. On New Year's Eve of the renwo year, with the book unfinished, [Cao] Qin passed away, his tears exhausted.",
          "ru": "Лишь тот, кто поистине понимает, прольёт горькие слёзы — эта книга была выплакана. В канун Нового года, с незавершённой книгой, Цинь скончался, истощив свои слёзы.",
          "ja": "能く解する者のみ辛酸の涙あり、泣きてこの書を成す。壬午除夕、書未だ成らず、芹は涙尽きて逝けり。"
        },
        {
          "type": "夹批",
          "source": "庚辰本",
          "position": "inline after 真事隐去",
          "original": "甄士隐三字妙。",
          "zh_modern": ""甄士隐"这三个字用得妙。",
          "en": "The three characters 'Zhen Shiyin' are wonderfully chosen.",
          "ru": "Три иероглифа «Чжэнь Шиинь» великолепны.",
          "ja": "「甄士隠」の三字、妙なり。"
        }
      ]
    },
    {
      "id": 2,
      "pdf_page": 15,
      "type": "poem",
      "original": "满纸荒唐言，一把辛酸泪。\n都云作者痴，谁解其中味？",
      "zh_modern": "满纸都是荒唐的话语，包含着一把辛酸的眼泪。\n人们都说作者痴傻，谁能理解其中的滋味呢？",
      "en": "Pages full of idle words,\nA handful of bitter tears.\nAll call the author mad—\nWho understands the flavor here?",
      "ru": "Страницы полны вздора,\nСлёзы горькие в них.\nВсе твердят: автор безумен—\nКто постигнет их вкус?",
      "ja": "紙に満つるは荒唐の言、\n一掬の辛酸の涙。\n皆は言う作者は痴と、\n誰か解せんその中の味を。",
      "poem_notes": {
        "form": "七言絶句 (Seven-character quatrain)",
        "rhyme_scheme": "AABA",
        "literary_devices": ["Self-deprecation", "Rhetorical question", "Metafiction"]
      },
      "commentary": [
        {
          "type": "侧批",
          "source": "甲戌本",
          "position": "right margin",
          "original": "此是第一首标题诗。",
          "zh_modern": "这是第一首标题诗。",
          "en": "This is the first title poem.",
          "ru": "Это первое титульное стихотворение.",
          "ja": "これが第一の題詩なり。"
        }
      ]
    }
  ],
  "translator_notes": [
    "「青埂峰」is a pun on「情根」(root of passion) - confirmed by 甲戌本 commentary",
    "甄士隐 (Zhen Shiyin) = 真事隐 (true events hidden)",
    "Research: Chen Yinke's commentary suggests Stone = author's self-portrait"
  ],
  "research_notes": [
    "Consulted 红楼梦学刊 for scholarly interpretation",
    "Checked Zhou Ruchang's detailed annotation edition",
    "Reviewed online commentary at 红楼品茗 forum"
  ],
  "characters_appearing": ["甄士隐"],
  "total_segments": 2,
  "manuscript_sources_on_page": ["甲戌本", "庚辰本"]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | int | PDF page number in source file |
| `chapter` | string | "前言", "凡例", "第一回", "第二回", ... "第八十回", "附录" etc. |
| `chapter_title` | object | Title in all languages (if this page starts a chapter) |
| `page_content_type` | string | "front_matter", "fanli", "chapter_start", "chapter_body", "chapter_end", "appendix" |
| `segments` | array | Array of segment objects |
| `segments[].id` | int | Sequential ID within this page (1, 2, 3, ...) |
| `segments[].type` | string | "prose", "poem", "dialogue", "title", "preface" |
| `segments[].original` | string | Original Classical Chinese text |
| `segments[].zh_modern` | string | **Polished** Modern Chinese translation |
| `segments[].en` | string | **Polished** English translation |
| `segments[].ru` | string | **Polished** Russian translation |
| `segments[].ja` | string | **Polished** Japanese translation |
| `segments[].commentary` | array | Array of commentary objects |
| `translator_notes` | array | **Non-trivial findings from research** - required! |
| `research_notes` | array | Sources consulted during research |
| `characters_appearing` | array | Characters appearing on this page |
| `manuscript_sources_on_page` | array | Manuscript sources cited on this page |

### Commentary Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | "眉批", "夹批", "侧批", "回末批", "回前批" |
| `source` | string | Manuscript source: "甲戌本", "庚辰本", "己卯本", "蒙府本", etc. |
| `position` | string | Where it appears: "top margin", "inline after X", "right margin" |
| `original` | string | Original commentary text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |

### Commentary Types Reference

| Type | Chinese | Position | Description |
|------|---------|----------|-------------|
| 眉批 | Marginal (top) | Page top/header | Extended commentary above text |
| 夹批 | Interlinear | Within text lines | Brief notes inserted in narrative |
| 侧批 | Side marginal | Page sides | Comments in margins |
| 回前批 | Chapter preface | Before chapter | Introduction to chapter |
| 回末批 | Chapter end | After chapter | Summary/reflection |

### Quality Rules

1. **Every segment has all 5 language versions** - no null/empty values
2. **ALL commentary translated** - preserve type and source attribution
3. **Valid JSON** - escape special characters properly
4. **UTF-8 encoding** - CJK characters must render correctly
5. **No skipped content** - include EVERY segment AND commentary from the page
6. **PDF page references** - note which page each segment comes from
7. **Sequential IDs** - 1, 2, 3, ... (no gaps)
8. **Preserve poetry structure** - maintain line breaks and verse forms

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

### Collaboration (CRITICAL - These Caused 83% Waste!)
- ❌ **NOT starting the sync daemon** - THIS IS MANDATORY
- ❌ **Claiming without running `--check-page`** - Page may be done on another branch!
- ❌ **Only checking WORKER_STATE.md files** - Must check actual translation files across ALL branches
- ❌ Claiming multiple chapters at once
- ❌ Forgetting to push claims immediately
- ❌ Letting heartbeat go stale (>5 min)
- ❌ Working in isolation - the daemon syncs for you

### The #1 Mistake (DO NOT DO THIS)
```bash
# ❌ WRONG: Just looking at your own branch
git fetch origin --prune
# Then claiming page 1 without checking if OTHER branches have translations/page_0001.json

# ✓ CORRECT: Use the daemon which checks ALL branches
python3 tools/sync_daemon.py --check-page 1
# Output: "✗ Page 1 is NOT AVAILABLE - completed by cursor/hong-lou-meng-translation-e575"
```

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
