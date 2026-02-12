# Translation Quality Guidelines

**Reference document** - Consult when you need guidance on literary style and translation approach.

---

## Literary Voice

红楼梦 is one of the greatest works of world literature. Your translations must preserve:

### Essential Qualities
- **Elegant classical beauty** - Don't over-modernize
- **Psychological depth** - Capture subtle emotional nuances
- **Symbolic richness** - Names and objects carry hidden meanings
- **Poetry structure** - Maintain verse forms and rhythm where possible

---

## Language-Specific Guidelines

### Modern Chinese (简体中文)

- Use standardized contemporary Mandarin
- Preserve classical elegance where natural
- Keep allusions and cultural references
- Clarify obscure passages but don't over-explain
- Use 现代白话文 register, not overly formal

**Example transformation**:
- Original: 黛玉方进入房时
- Modern: 黛玉刚进入房门时

### English

- **Register**: Scholarly literary English (similar to David Hawkes or Penguin Classics)
- **Names**: Use Pinyin (Jia Baoyu, Lin Daiyu, not translated names)
- **Titles**: Translate (Grandmother Jia, Lady Wang, not Jia Laomu, Wang Furen)
- **Cultural terms**: Keep key terms in Pinyin with context (e.g., "the old madam" for 老太太)
- **Poetry**: Attempt to preserve structure; meter when feasible, but prioritize meaning

**Example**:
- 贾母 → Grandmother Jia
- 老太太 → the old madam / Grandmother
- 姑娘 → young lady / Miss

### Russian (Русский)

- **Register**: Literary Russian appropriate for classical literature
- **Style**: Preserve aristocratic register (19th-century literary style acceptable)
- **Names**: Transcribe Chinese names phonetically (Цзя Баоюй, Линь Дайюй)
- **Titles**: Translate (матушка Цзя, госпожа Ван)
- **Poetry**: Maintain literary quality; strive for rhythm but prioritize meaning

**Key terms**:
- 公子 → молодой господин
- 小姐 → барышня
- 丫鬟 → служанка
- 老爷 → господин
- 太太 → госпожа

### Japanese (日本語)

- **Register**: Classical-influenced literary style (文語調)
- **Script**: Mix kanji and kana as appropriate
- **Names**: Use on'yomi (音読み) for Chinese names when suitable
  - 賈宝玉 (Jia Baoyu) → カホウギョク or 賈宝玉
  - 林黛玉 (Lin Daiyu) → リンタイギョク or 林黛玉
- **Titles**: Use Japanese equivalents with classical flavor
- **Poetry**: Attempt classical Japanese poetic forms when structure allows

**Key terms**:
- 公子 → 公子 (こうし)
- 小姐 → お嬢様 (おじょうさま)
- 丫鬟 → 女中 (じょちゅう)
- 老爷 → 旦那様 (だんなさま)
- 太太 → 奥様 (おくさま)

---

## Character Name Puns

Many names contain hidden meanings (谐音). **Preserve the transliterated name** and document the pun in `notes`.

| Name | Pinyin | Hidden Meaning | Translation Approach |
|------|--------|----------------|----------------------|
| 甄士隐 | Zhen Shiyin | 真事隐 (true events hidden) | Keep "Zhen Shiyin", note the pun |
| 贾雨村 | Jia Yucun | 假语存 (false words remain) | Keep "Jia Yucun", note the pun |
| 贾宝玉 | Jia Baoyu | 假宝玉 (false precious jade) | Keep "Jia Baoyu", note in analysis |
| 霍启 | Huo Qi | 祸起 (disaster begins) | Keep "Huo Qi", note foreshadowing |

**In `notes` field**:
```json
"notes": [
  "贾雨村 (Jia Yucun) is a pun on 假语存 (false words remain), indicating the metafictional nature of the narrative"
]
```

---

## Commentary Types

Recognize and label commentary by source and position:

| Type | Position | Description | Example Marker |
|------|----------|-------------|----------------|
| 眉批 (méi pī) | Top of page | Extended commentary | Often unsigned or signed |
| 夹批 (jiā pī) | Inline | Brief notes within text | 【甲戌】【庚辰】 |
| 侧批 (cè pī) | Side margin | Side comments | Appears in margins |
| 回末批 (huí mò pī) | Chapter end | End-of-chapter comments | At chapter conclusion |

**Common manuscript sources**:
- 甲戌本 (Jiaxu edition)
- 庚辰本 (Gengchen edition)
- 己卯本 (Jimao edition)
- 蒙府本 (Mengfu edition)
- 戚序本 (Qixu edition)

---

## Research Before Translating

### What to Research

1. **Classical allusions** (典故)
   - Historical references
   - Literary references
   - Mythological references

2. **Cultural context**
   - Social customs
   - Family hierarchy
   - Ceremonial practices

3. **Character relationships**
   - Family trees
   - Social positions
   - Name significance

4. **Linguistic nuances**
   - Classical grammar
   - Poetic devices
   - Wordplay

### Where to Research

1. **Project resources** (first priority):
   - `research/glossary.md` - Character names & terminology
   - `research/chapter_structure.md` - Chapter summaries
   - `research/character_guide.md` - Character profiles
   - `research/poetry_guide.md` - Poetry forms
   - `research/commentary_guide.md` - Commentary sources
   - `research/cultural_context.md` - Cultural background

2. **Online resources**:
   - Academic articles on 红楼梦
   - Classical Chinese dictionaries (e.g., 汉典)
   - Existing translations (Hawkes, Yang Xianyi, Kuhn)
   - Literary analysis websites

3. **When in doubt**:
   - Search for scholarly interpretations
   - Compare existing translations
   - Note uncertainty in `notes` field if unresolved

---

## Poetry Translation

红楼梦 contains many poems. Preserve as much as possible:

### Priorities (in order)
1. **Meaning** - Don't sacrifice clarity for form
2. **Imagery** - Preserve visual and emotional images
3. **Tone** - Maintain the emotional register
4. **Form** - Attempt to echo structure (line count, parallelism)
5. **Rhyme/Meter** - Desirable but lowest priority

### Common Forms
- 七言绝句 (7-character quatrain)
- 五言绝句 (5-character quatrain)
- 七言律诗 (7-character regulated verse)
- 词 (ci poetry, various forms)

### Example Approach

Original (七言绝句):
```
惯养娇生笑你痴，
菱花空对雪澌澌。
好防佳节元宵后，
便是烟消火灭时。
```

English (preserve line count, approximate meter):
```
Spoiled and pampered, you're mocked as mad;
The mirror faces only melting snow.
Beware: once the Lantern Festival has passed,
The hour comes when smoke is gone, fire quenched.
```

**Document in `notes`**:
```json
"notes": [
  "Poem form: 七言绝句 (7-character quatrain)",
  "'烟消火灭' foreshadows the family's decline after the festival"
]
```

---

## Common Terminology Reference

| Classical | Modern Chinese | English | Russian | Japanese |
|-----------|----------------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子 (こうし) |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | 丫鬟/婢女 | maidservant | служанка | 女中 |
| 老爷 | 老爷/大人 | master/lord | господин | 旦那様 |
| 太太 | 太太/夫人 | madam/lady | госпожа | 奥様 |
| 姑娘 | 姑娘 | young lady/miss | барышня | 娘 (むすめ) |
| 嬷嬷 | 嬷嬷 | old nurse/nanny | старая няня | 乳母 (うば) |

See `research/glossary.md` for complete terminology.

---

## Quality Checks

Before saving each page, verify:

- [ ] ALL visible text is translated (main + commentary)
- [ ] Literary quality matches original's register
- [ ] Names are transliterated consistently
- [ ] Puns and wordplay are documented in `notes`
- [ ] Poetry maintains structure where feasible
- [ ] Cultural context is clear without over-explanation
- [ ] All 4 target languages sound natural to native speakers

---

## When Stuck

If you're uncertain about a passage after 5 minutes of research:

1. Make your best scholarly interpretation
2. Add to `notes`: `"Uncertain: [your question or alternate interpretations]"`
3. Continue to next segment
4. DO NOT stop and wait for clarification

**Example**:
```json
"notes": [
  "Uncertain: '三分' may refer to Three Kingdoms period or Buddhist triple division; context unclear",
  "Translation reflects most common scholarly interpretation"
]
```

---

**This is a reference document. Return to `01_core_task.md` for the essential workflow.**
