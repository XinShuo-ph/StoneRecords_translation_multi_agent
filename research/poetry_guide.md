# Poetry Translation Guide - 红楼梦

## Overview

红楼梦 contains over 200 poems, songs, and rhymed passages. Poetry translation is one of the most challenging aspects of this project. This guide provides principles and examples for handling poetry across all four target languages.

---

## Types of Poetry in 红楼梦

### 1. 诗 (Shi) - Regulated Verse

| Form | Lines | Characters/Line | Rhyme | Example |
|------|-------|----------------|-------|---------|
| 五言绝句 | 4 | 5 | lines 2,4 | Many casual poems |
| 七言绝句 | 4 | 7 | lines 2,4 | 葬花吟引子 |
| 五言律诗 | 8 | 5 | even lines | Formal occasions |
| 七言律诗 | 8 | 7 | even lines | Poetry club competitions |

**Characteristics:**
- Strict tonal patterns (平仄)
- Rhyme on even-numbered lines
- Parallelism in couplets (律诗)
- Caesura after character 2 (五言) or 4 (七言)

### 2. 词 (Ci) - Song Lyrics

Poems written to existing musical patterns (词牌):
- Variable line lengths
- Specific patterns for each 词牌
- Examples: 寄生草, 好事近, 临江仙

### 3. 曲 (Qu) - Dramatic Songs

Used in the 红楼梦曲 (Dream songs of Ch. 5):
- More colloquial than 诗/词
- Often tell stories or express emotion directly
- The twelve songs prophesying the Twelve Beauties

### 4. 联句 (Linked Verse)

Collaborative poetry (Ch. 50, 76):
- Multiple poets contribute alternating lines
- Must maintain consistency of theme and form
- Often competitive/playful

### 5. 谜语 (Riddles)

Verse riddles (Ch. 22, 50):
- Each line provides clues
- Answer often symbolic of character's fate

---

## Translation Principles

### Priority Order

When translating poetry, prioritize in this order:
1. **Meaning** - What does the poem say?
2. **Imagery** - What pictures does it paint?
3. **Tone/Mood** - What feeling does it convey?
4. **Sound** - Rhythm, rhyme (when possible without sacrificing above)

### General Guidelines

| Aspect | Approach |
|--------|----------|
| Rhyme | Attempt if natural; don't force |
| Meter | Preserve rhythm where possible |
| Line breaks | Maintain original structure |
| Imagery | Translate metaphors, not just words |
| Allusions | Note in translator comments |

---

## Language-Specific Approaches

### Modern Chinese (简体中文)

**Goal**: Make classical poetry accessible while preserving elegance

**Approach**:
- 保留诗歌格式（行数、换行）
- 将文言词汇转化为现代表达
- 保留重要意象和修辞
- 可适当添加注释解释典故

**Example**:
```
原文：满纸荒唐言，一把辛酸泪。
译文：满纸都是荒唐的话语，包含着无尽辛酸的眼泪。
```

### English

**Goal**: Create readable poetry that captures meaning and mood

**Approach**:
- Prioritize natural English over forced rhyme
- Maintain line structure when possible
- Use poetic diction appropriate to literary translation
- Indicate original form in notes

**Example**:
```
Original: 满纸荒唐言，一把辛酸泪。
Translation: Pages full of idle words,
            A handful of bitter tears.
```

**Note**: Some translators (Hawkes) use rhyme; others (Yang) don't. Both are valid.

### Russian (Русский)

**Goal**: Literary Russian verse in classical tradition

**Approach**:
- Russian poetry tradition favors rhyme
- Attempt rhymed translation when natural
- Use appropriate meter (iambic common in Russian)
- Draw on Russian classical poetry vocabulary

**Example**:
```
Original: 满纸荒唐言，一把辛酸泪。
Translation: Страницы полны вздорных слов,
            Горсть горьких слёз в них.
```

### Japanese (日本語)

**Goal**: Literary Japanese with classical flavor

**Approach**:
- Japanese poetry has own traditions (和歌, 俳句)
- Use 文語 (classical Japanese) elements where appropriate
- Maintain 漢詩 reading patterns for shared characters
- Consider 5-7 rhythm of traditional Japanese poetry

**Example**:
```
Original: 满纸荒唐言，一把辛酸泪。
Translation: 紙に満つるは荒唐の言、
            一掬の辛酸の涙。
```

---

## Key Poems to Note

### 1. 好了歌 (Song of Good-Done, Ch. 1)

**Importance**: Thematic statement of the novel
**Challenges**: 
- Puns on 好/了 (good/done, like/finish)
- Buddhist philosophy
- Repeated structure

**Approach**: Preserve the questioning structure and ironic tone

### 2. 葬花吟 (Flower-Burial Lament, Ch. 27)

**Importance**: Lin Daiyu's signature poem; over 50 lines
**Challenges**:
- Extended length
- Intense emotion
- Rich imagery
- Self-identification with dying flowers

**Approach**: 
- Maintain elegiac tone throughout
- Preserve flower/death imagery
- Let emotion build through the poem

### 3. 红楼梦曲十二支 (Twelve Songs of the Red Chamber Dream, Ch. 5)

**Importance**: Prophecies for the Twelve Beauties
**Challenges**:
- Each song uses different 词牌
- Dense with allusion and foreshadowing
- Must convey fate while remaining poetic

**Approach**:
- Note the 词牌 form
- Explain prophetic elements in notes
- Balance mystery and meaning

### 4. 芙蓉女儿诔 (Elegy for the Hibiscus Spirit, Ch. 78)

**Importance**: Baoyu's masterpiece; mourning for Qingwen
**Challenges**:
- Long prose-poem (赋 style)
- Dense classical allusions
- Multiple voices and modes

**Approach**:
- Preserve the formal, ritualistic feeling
- Note all major allusions
- Convey grief and indignation

### 5. 菊花诗十二首 (Twelve Chrysanthemum Poems, Ch. 38)

**Importance**: Poetry club competition
**Challenges**:
- Twelve poems on same theme
- Different characters' styles must show
- Daiyu wins—her poems must shine

**Approach**:
- Differentiate each poet's voice
- Daiyu's poems should feel most original
- Note the competitive context

---

## Poetry Translation Template

When translating a poem, include:

```json
{
  "id": 1,
  "type": "poem",
  "original": "Original classical Chinese text",
  "zh_modern": "Modern Chinese version",
  "en": "English translation",
  "ru": "Russian translation", 
  "ja": "Japanese translation",
  "poem_notes": {
    "form": "七言绝句 (Seven-character quatrain)",
    "rhyme_scheme": "AABA or description",
    "meter": "Describe rhythm",
    "literary_devices": ["List devices used"],
    "allusions": ["List classical allusions"],
    "significance": "Why this poem matters"
  },
  "translator_notes": [
    "Additional context",
    "Translation decisions explained"
  ]
}
```

---

## Handling Specific Challenges

### Puns and Wordplay

**Problem**: Many poems contain puns untranslatable directly

**Solution**: 
- Translate the surface meaning
- Explain the pun in notes
- If possible, create equivalent wordplay

**Example**: 
好了歌 puns on 好/了
- Surface: "good" and "done"
- Hidden: "like/love" and "finish/let go"
- Note both meanings

### Classical Allusions

**Problem**: References to Tang poetry, historical events, etc.

**Solution**:
- Translate the allusion's function, not just words
- Provide context in notes
- Don't over-explain in the translation itself

### Prophetic Content

**Problem**: Poems foreshadow fates readers don't yet know

**Solution**:
- Preserve the ambiguity
- Let imagery suggest without explicit spoilers
- Notes can explain for readers who want to know

### Names in Poetry

**Problem**: Character names are often meaningful

**Solution**:
- Keep transliterated names in translation
- Note name meanings separately
- The poetry should work even without knowing name meanings

---

## Quality Standards for Poetry

✅ **Good Translation**:
- Captures meaning accurately
- Reads as poetry in target language
- Preserves key imagery
- Notes explain important context
- Character's voice comes through

❌ **Poor Translation**:
- Sacrifices meaning for rhyme
- Reads as awkward prose
- Loses central images
- No context for allusions
- All poems sound the same

---

## Example: Full Poetry Translation

### Original (葬花吟 excerpt)

```
花谢花飞花满天，
红消香断有谁怜？
游丝软系飘春榭，
落絮轻沾扑绣帘。
```

### Modern Chinese
```
花儿凋谢、花儿飘飞、落花满天，
红色消退、香气断绝，有谁怜惜？
游丝轻柔地飘系在春日的亭榭，
落下的柳絮轻轻沾上绣花的帘子。
```

### English
```
Flowers wither, flowers fly, flowers fill the sky,
Their red fades, fragrance dies—who will grieve?
Gossamer threads drift soft by the spring pavilion,
Falling catkins gently touch the embroidered screen.
```

### Russian
```
Цветы увяли, цветы летят, цветами полно небо,
Их алость гаснет, аромат исчез—кто пожалеет их?
Паутинки тихо вьются у весенней беседки,
Пух летящий нежно касается вышитой занавеси.
```

### Japanese
```
花は萎れ、花は飛び、花は天に満ち、
紅は消え、香は断えて、誰か憐れまん。
遊糸は柔らかく春榭に繋がり、
落絮は軽く繍帘を撲つ。
```

### Notes
```json
{
  "form": "七言 (Seven-character verse)",
  "imagery": "Falling flowers = dying beauty, youth, the speaker herself",
  "speaker": "Lin Daiyu identifying with the flowers",
  "significance": "Central to Daiyu's character; her most famous poem",
  "allusions": [
    "落花 (falling flowers) traditional symbol of transience",
    "柳絮 (willow catkins) often linked to women in poetry"
  ]
}
```

---

## Resources

- **Hawkes' translations**: See how he handles poetry in "The Story of the Stone"
- **Yang Xianyi translations**: More literal approach for comparison
- **Classical Chinese poetry guides**: For understanding original forms

---

*Poetry is the heart of 红楼梦. Take extra care with these sections, and don't hesitate to add extensive notes explaining your translation choices.*
