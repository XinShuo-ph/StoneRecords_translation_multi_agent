# Commentary Guide - 脂评汇校本

## Overview

The 红楼梦脂评汇校本 (Dream of the Red Chamber with Zhiping Commentary Collation) contains commentary from multiple manuscript sources. This guide explains how to identify, categorize, and translate these commentaries.

---

## Manuscript Sources (版本)

The commentary comes from several manuscript versions, each indicated by tags in the text:

| Tag | Full Name | Chinese | Date | Notes |
|-----|-----------|---------|------|-------|
| 【甲戌】| Jiaxu manuscript | 甲戌本 | 1754 | Earliest; most detailed commentary |
| 【庚辰】| Gengchen manuscript | 庚辰本 | 1760 | Comprehensive; 78 chapters |
| 【己卯】| Jimao manuscript | 己卯本 | 1759 | Early version |
| 【蒙府】| Mengfu (Qing palace) | 蒙府本 | Later | Palace copy |
| 【戚序】| Qi Liaoqi preface | 戚序本 | Later | Has Qi's preface |
| 【列藏】| Leningrad (St. Petersburg) | 列藏本 | Later | Held in Russia |
| 【舒序】| Shu Yuan preface | 舒序本 | Later | Has Shu's preface |
| 【郑藏】| Zheng collection | 郑藏本 | Later | Zheng family collection |

### Most Important Sources

1. **甲戌本 (Jiaxu)**: Contains the most authentic early commentary, likely closest to Cao Xueqin and his circle
2. **庚辰本 (Gengchen)**: Most complete early manuscript, extensive marginalia
3. **己卯本 (Jimao)**: Important early source

---

## Commentary Types (批语类型)

### 1. 眉批 (Marginal Notes - Top)

**Position**: Top margin of the page (眉 = eyebrow)
**Character**: Often extended commentary, analysis
**Format**: Usually marked clearly in the top space

**Example**:
```
【甲戌眉批】能解者方有辛酸之泪，哭成此书。
```

**Translation approach**: Full translation with all four target languages

### 2. 夹批 (Interlinear Notes)

**Position**: Inserted within the text lines
**Character**: Brief comments, often reactions or clarifications
**Format**: Usually smaller font, sometimes in【】brackets

**Example**:
```
原文："故将真事隐去"【甲戌夹批：甄士隐三字妙】
```

**Translation approach**: Note the exact position (after which phrase)

### 3. 侧批 (Side Marginal Notes)

**Position**: Left or right margins
**Character**: Medium-length comments
**Format**: Vertical text alongside main text

**Example**:
```
【庚辰侧批】此处伏下文...
```

**Translation approach**: Note whether left or right margin

### 4. 回前批 (Chapter Preface Commentary)

**Position**: Before the chapter begins
**Character**: Introduction or setup for the chapter
**Format**: Clearly before the chapter title

**Translation approach**: Translate as part of chapter introduction

### 5. 回末批 (Chapter-End Commentary)

**Position**: After the chapter ends
**Character**: Summary, reflection, or thematic analysis
**Format**: After "正文完" or chapter conclusion

**Example**:
```
【甲戌回末总批】此回声色货利四大魔障...
```

**Translation approach**: Translate as `chapter_end_commentary` array

---

## Commentator Attribution

### Known Commentators

| Name | Chinese | Relationship | Style |
|------|---------|--------------|-------|
| 脂砚斋 | Zhiyan Zhai | Close to Cao Xueqin | Literary, emotional |
| 畸笏叟 | Jihu Sou | Inner circle | Editorial, clarifying |
| 梅溪 | Meixi | Unknown | Occasional notes |
| 松斋 | Songzhai | Unknown | Rare comments |

### Identifying Commentators

Sometimes the commentator signs:
```
【脂砚】此处一字不可更。
【畸笏】前批系脂砚所书...
```

When unsigned, attribute to the manuscript source only.

---

## Visual Recognition in PDF

### How to Identify Commentary in the PDF

1. **Font Size**: Commentary usually in smaller font than main text
2. **Position**: Look at margins (top, sides) and inline insertions
3. **Brackets**: 【】often enclose source/type labels
4. **Color/Formatting**: Some editions use different formatting for commentary

### Common Patterns

```
Main text layout:

    【眉批】Extended commentary text here...
    ═══════════════════════════════════════
    
    正文正文正文【夹批：简短评语】正文正文
    正文正文正文正文正文正文正文正文正文
    
    ║                                   ║
    ║【侧批】                          ║
    ║Side commentary                    ║
    ║                                   ║
```

---

## Translation Guidelines

### Preserve Structure

When translating commentary:
1. **Keep the type** (眉批, 夹批, etc.)
2. **Keep the source** (甲戌本, 庚辰本, etc.)
3. **Note the position** for夹批 (what text it follows)

### Translation Register

Commentary should be translated with:
- **Scholarly tone** for analytical comments
- **Emotional resonance** for personal remarks
- **Precision** for textual/editorial notes

### Handling Difficult Commentary

| Situation | Approach |
|-----------|----------|
| Unclear source | Note as "unknown source" |
| Illegible text | Note as [illegible] |
| Multiple readings | List variants |
| Editorial marks | Describe the mark |

---

## JSON Format for Commentary

```json
{
  "commentary": [
    {
      "type": "眉批",
      "source": "甲戌本",
      "commentator": "脂砚斋",  // if known
      "position": "top margin, above paragraph 1",
      "original": "能解者方有辛酸之泪...",
      "zh_modern": "能够理解的人才会流下辛酸的眼泪...",
      "en": "Only those who truly understand will shed bitter tears...",
      "ru": "Лишь тот, кто поистине понимает, прольёт горькие слёзы...",
      "ja": "能く解する者のみ辛酸の涙あり..."
    }
  ]
}
```

---

## Common Commentary Vocabulary

| Chinese | Meaning | Translation Note |
|---------|---------|------------------|
| 伏 | foreshadowing | "This plants the seed for..." |
| 照应 | echoing/callback | "This echoes..." |
| 神来之笔 | stroke of genius | "A masterful touch" |
| 妙 | wonderful/subtle | "Wonderfully done" |
| 有深意 | deeper meaning | "There is deeper meaning here" |
| 可叹 | lamentable | "How lamentable!" |
| 可笑 | laughable | "How laughable!" |
| 可敬 | admirable | "How admirable!" |
| 正是 | exactly right | "Exactly so" |
| 一字不可易 | not one word can be changed | "Perfect as written" |

---

## Commentary Importance by Chapter

Some chapters have particularly rich commentary:

| Chapter | Commentary Notes |
|---------|------------------|
| 1 | Heavy commentary on allegory and authorial intent |
| 5 | Dream sequence with prophetic commentary |
| 13 | 秦可卿 death - deleted content discussed |
| 27 | 葬花吟 - extensive literary analysis |
| 78 | 芙蓉诔 - Baoyu's elegy analyzed |

---

## Working Directly from PDF

When viewing PDF pages:

1. **Scan entire page** for all commentary locations
2. **Note the visual markers** (brackets, font changes)
3. **Identify source tags** 【甲戌】【庚辰】etc.
4. **Map commentary to text segments** it references
5. **Translate everything** - don't skip any commentary

### Example PDF Page Analysis

```
PDF Page 15:
┌─────────────────────────────────────┐
│【甲戌眉批】Commentary A...           │ ← 眉批 at top
├─────────────────────────────────────┤
│  第一回                              │
│  甄士隐梦幻识通灵...                 │
│                                     │
│  正文段落一【夹批B】续正文           │ ← 夹批 inline
│  正文段落续...                       │
│                        │【侧批C】   │ ← 侧批 in margin
│                        │继续        │
│  正文段落二...                       │
└─────────────────────────────────────┘

Must capture: Commentary A, B, C with proper attribution
```

---

## Quality Checklist for Commentary

Before submitting a chapter:

- [ ] All 眉批 captured and translated
- [ ] All 夹批 captured with position noted
- [ ] All 侧批 captured and translated
- [ ] All 回末批 captured in chapter_end_commentary
- [ ] Source manuscript noted for each commentary
- [ ] Commentator noted when identifiable
- [ ] Commentary position clear (relates to which text)
- [ ] All four language translations provided

---

*The commentary is integral to understanding 红楼梦. Treat it with the same care as the main text.*
