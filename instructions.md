## Goal

Translate pages from 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary) into four languages:
- **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
- **English** - Scholarly literary translation
- **Russian (Русский)** - Literary Russian translation
- **Japanese (日本語)** - Classical-influenced literary Japanese

Each PDF page becomes one JSON file. Translate ALL content on each page: main text AND commentary.

---

## Source Material

**PDF**: `红楼梦脂评汇校本_有书签目录_v3.13.pdf`

**Page Images**: `source_pages/page_XXXX.png`

The source contains:
- **Main text (正文)**: The novel's narrative
- **Commentary (脂评)**: Annotations from various manuscript sources marked with 【甲戌】【庚辰】【己卯】etc.

---

## Workflow: For Each Page

### Step 1: View the Page

Open the page image or PDF. Identify all content:
- Main narrative text
- Any commentary (眉批, 夹批, 侧批)
- Any poetry

### Step 2: Research

Before translating, research each segment:
- Read relevant materials in `research/` directory
- Search online for scholarly interpretations
- Look up classical allusions (典故)
- Understand character name puns and hidden meanings
- Note historical and cultural context

Document findings in the `notes` field.

### Step 3: Translate

For each text segment on the page:
1. Copy the original Classical Chinese
2. Translate to Modern Chinese
3. Translate to English
4. Translate to Russian
5. Translate to Japanese

Translate all commentary as well.

### Step 4: 润色 (Polish)

Review and refine each translation:
- Ensure literary quality matches the original's elegance
- Verify cultural nuances are preserved
- Check that poetry maintains its structure and rhythm
- Confirm consistency with glossary terms
- Read translations aloud mentally—do they flow naturally?

### Step 5: Save as JSON

Save to `translations/page_XXXX.json` (4-digit page number).

### Step 6: Next Page

Continue to the next page immediately. Do not pause between pages.

---

## JSON Output Format

```json
{
  "page": 20,
  "chapter": "第一回",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "士隐意欲也跟了过去，方举步时，忽听一声霹雳，有若山崩地陷。士隐大叫一声，定睛一看，只见烈日炎炎，芭蕉冉冉，梦中之事便忘了对半。",
      "zh_modern": "士隐也想要跟着过去，刚举步的时候，忽然听见一声霹雳，好像山崩地陷一般。士隐大叫一声，定睛一看，只见烈日炎炎，芭蕉叶缓缓摇动，梦中的事便忘了一大半。",
      "en": "Shiyin wished to follow them, but just as he was about to step forward, he suddenly heard a thunderclap, as if mountains were crumbling and the earth was caving in. Shiyin cried out in alarm and, fixing his eyes, saw only the blazing sun and the banana leaves gently swaying—half of what had happened in the dream was already forgotten.",
      "ru": "Шиинь хотел последовать за ними, но едва он сделал шаг, как вдруг раздался удар грома, словно горы рушились и земля разверзалась. Шиинь вскрикнул и, присмотревшись, увидел лишь палящее солнце и мерно колышущиеся банановые листья — половина того, что было во сне, уже забылась.",
      "ja": "士隠も後を追おうとして、まさに足を踏み出そうとした時、突然雷鳴が轟き、山が崩れ地が陥没するかのようであった。士隠は大声で叫び、目を凝らして見れば、ただ烈日が照りつけ、芭蕉の葉がゆらゆらと揺れるばかり。夢の中の出来事は半ば忘れてしまった。",
      "commentary": [
        {
          "source": "脂批",
          "original": "真是大警觉大转身。",
          "zh_modern": "真是大警醒大转折。",
          "en": "Truly a great awakening and great turning point.",
          "ru": "Поистине великое пробуждение и великий поворот.",
          "ja": "まことに大いなる警醒、大いなる転身なり。"
        }
      ]
    },
    {
      "id": 2,
      "type": "dialogue",
      "original": ""施主，你把这有命无运，累及爹娘之物，抱在怀内作甚？"",
      "zh_modern": ""施主，你把这个有命无运、会连累爹娘的东西，抱在怀里干什么？"",
      "en": "\"Benefactor, why do you hold in your arms this creature who has fate but no fortune, who will bring calamity upon her parents?\"",
      "ru": "«Благодетель, зачем вы держите на руках это существо, у которого есть судьба, но нет удачи, которое навлечёт беду на своих родителей?»",
      "ja": "「施主よ、この命はあれど運なく、父母に災いを及ぼす者を、何故に懐に抱いておられるのか？」",
      "commentary": []
    },
    {
      "id": 3,
      "type": "poem",
      "original": "惯养娇生笑你痴，\n菱花空对雪澌澌。\n好防佳节元宵后，\n便是烟消火灭时。",
      "zh_modern": "惯常娇生惯养，笑你太痴愚，\n镜中容颜空对着纷纷飘落的雪花。\n要提防佳节元宵节之后，\n那便是烟消火灭之时。",
      "en": "You dote and pamper her—how foolish you are!\nThe water-chestnut flower faces the drifting snow in vain.\nBeware the time after the Lantern Festival—\nThat will be when smoke disperses and fire dies.",
      "ru": "Ты балуешь её — как ты глуп!\nЦветок водяного ореха тщетно глядит на падающий снег.\nОстерегайся времени после Праздника фонарей —\nТогда рассеется дым и погаснет огонь.",
      "ja": "惯れ養い娇に生ず、汝の痴を笑う、\n菱花空しく雪澌澌に対す。\n好く防げよ佳節元宵の後、\n便ち是れ煙消え火滅する時。",
      "commentary": []
    }
  ],
  "notes": [
    "英莲 (Yinglian): Her name puns on 应怜 (should be pitied). Foreshadows her tragic fate.",
    "菱花: Puns on her later name 香菱, also means 'mirror' (菱花镜).",
    "元宵: Lantern Festival—foreshadows when Yinglian will be kidnapped.",
    "烟消火灭: Foreshadows the fire destroying the Zhen family home."
  ]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | int | PDF page number |
| `chapter` | string | "前言", "第一回", "第二回", etc. |
| `segments` | array | Array of translated segments |
| `segments[].id` | int | Sequential ID (1, 2, 3...) |
| `segments[].type` | string | "prose", "poem", "dialogue" |
| `segments[].original` | string | Original Classical Chinese |
| `segments[].zh_modern` | string | Modern Chinese translation |
| `segments[].en` | string | English translation |
| `segments[].ru` | string | Russian translation |
| `segments[].ja` | string | Japanese translation |
| `segments[].commentary` | array | Commentary annotations (empty `[]` if none) |
| `notes` | array | Research findings: puns, allusions, cultural context |

### Commentary Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Manuscript source: "甲戌本", "庚辰本", "脂批", etc. |
| `original` | string | Original commentary text |
| `zh_modern` | string | Modern Chinese translation |
| `en` | string | English translation |
| `ru` | string | Russian translation |
| `ja` | string | Japanese translation |

---

## Translation Quality Guidelines

### Voice and Style

红楼梦 is one of the greatest works of world literature. Preserve:
- **Elegant classical beauty** - Don't over-modernize
- **Psychological depth** - Subtle emotional nuances
- **Symbolic richness** - Names and objects carry meaning
- **Poetry structure** - Maintain verse forms

### By Language

**Modern Chinese (简体中文)**:
- 使用规范现代汉语，保留古典韵味
- 保留原有的典故和意涵

**English**:
- Scholarly literary register
- Pinyin for names (Jia Baoyu, Lin Daiyu)
- Cultural notes where needed

**Russian (Русский)**:
- Literary Russian for classical literature
- Preserve aristocratic register

**Japanese (日本語)**:
- Classical-influenced literary style
- Use 音読み for Chinese names

---

## Key Terms Reference

| Classical | Modern Chinese | English | Russian | Japanese |
|-----------|----------------|---------|---------|----------|
| 公子 | 公子/少爷 | young master | молодой господин | 公子 |
| 小姐 | 小姐 | young lady | барышня | お嬢様 |
| 丫鬟 | 丫鬟/婢女 | maidservant | служанка | 女中 |
| 老爷 | 老爷/大人 | master/lord | господин | 旦那様 |
| 太太 | 太太/夫人 | madam/lady | госпожа | 奥様 |

See `research/glossary.md` for complete terminology.

---

## Character Name Puns

Many names contain hidden meanings:

| Name | Hidden Meaning |
|------|----------------|
| 甄士隐 (Zhen Shiyin) | 真事隐 - True events hidden |
| 贾雨村 (Jia Yucun) | 假语存 - False words remain |
| 贾宝玉 (Jia Baoyu) | 假宝玉 - False precious jade |

When translating, keep transliterated names and note the pun in `notes`.

---

## Commentary Types

| Type | Position | Description |
|------|----------|-------------|
| 眉批 | Top of page | Extended commentary |
| 夹批 | Inline | Brief notes within text |
| 侧批 | Side margin | Side comments |
| 回末批 | Chapter end | End-of-chapter comments |

---

## Continuous Execution

Work continuously:
1. Complete page → Save JSON → Next page → Repeat
2. Continue until you've completed all assigned pages

If stuck on a passage for more than 5 minutes:
- Add a note: `"Uncertain: [your question]"`
- Continue to next segment

---

## Anti-Patterns to Avoid

- Skipping content - Translate EVERYTHING on the page
- Empty translations - Every field must have content
- Wrong page number - Verify you're on the correct page
- Stopping to ask questions - Keep working, add notes
- Invalid JSON - Validate before saving
- Skipping research - Always research before translating

---

## Quick Checklist Per Page

Before moving to the next page, verify:

- [ ] Page number is correct
- [ ] ALL visible text is translated (main + commentary)
- [ ] All 4 target languages are present for each segment
- [ ] All segments have `commentary` field (empty `[]` if none)
- [ ] Sequential IDs (1, 2, 3...)
- [ ] JSON is valid
- [ ] Notes include research findings

---

## Example

See `examples/page_0020.json` for a complete reference.
