# 红楼梦 Translation Guide

**Version 2.0** - Focused Translation Instructions  
**Target**: Translate PDF pages of 红楼梦脂评汇校本 into 4 languages with scholarly quality

---

## Your Task

Translate **one PDF page at a time** from Classical Chinese into:
1. **Modern Chinese** (简体中文) - Accessible contemporary Mandarin
2. **English** - Scholarly literary translation
3. **Russian** (Русский) - Literary Russian
4. **Japanese** (日本語) - Classical-influenced literary Japanese

Translate **EVERYTHING** on the page: main text AND all commentary.

---

## The 3-Step Process

Every page follows the same workflow:

```
┌─────────────────────────────────────────────┐
│  1. READ (30% of time)                      │
│     • Open PDF to assigned page             │
│     • Identify all content                  │
│     • Note difficult passages               │
│                                             │
│  2. RESEARCH & TRANSLATE (50% of time)      │
│     • Research EACH sentence                │
│     • Find scholarly interpretations        │
│     • Translate to all 4 languages          │
│                                             │
│  3. POLISH & VERIFY (20% of time)           │
│     • Improve literary quality              │
│     • Verify completeness                   │
│     • Validate JSON structure               │
└─────────────────────────────────────────────┘
```

---

## STEP 1: READ the PDF Page

### 1.1 Open the Source PDF

You will be given a page number (e.g., "Page 20"). Open `红楼梦脂评汇校本_有书签目录_v3.13.pdf` to that page.

### 1.2 Identify ALL Content on the Page

The page contains multiple types of content:

| Type | Description | How to Recognize |
|------|-------------|------------------|
| **正文** | Main narrative text | Larger font, main body |
| **夹批** | Interlinear commentary | Smaller font, inline, often in 【】 |
| **眉批** | Top marginal commentary | Top margin area |
| **侧批** | Side marginal commentary | Left/right margins |
| **回末批** | End-of-chapter commentary | After chapter conclusion |
| **Source tags** | Manuscript indicators | 【甲戌】【庚辰】【己卯】【蒙府】 |

**Critical**: You must translate EVERYTHING. Do not skip any text.

### 1.3 Note Difficult Passages

As you read, note:
- Classical terms you don't immediately understand
- Character names with potential puns
- Poetry or parallel prose
- Historical/cultural references
- Literary allusions (典故)

---

## STEP 2: RESEARCH & TRANSLATE

### 2.1 Research Protocol (MANDATORY)

For **each sentence** that contains:
- Character names
- Classical allusions
- Poetry
- Wordplay or puns
- Cultural references
- Symbolic objects

You MUST:

1. **Search online** for scholarly interpretation
   - Use search terms like: "红楼梦 [passage text] 解读"
   - Check 红楼梦学刊, 周汝昌, 蔡义江 commentaries
   - Look for literary analysis

2. **Consult at least 3 sources** per page minimum

3. **Document findings** in JSON:
   - If you discover a pun → add to `translator_notes`
   - If you find historical context → add to `translator_notes`
   - If scholars debate meaning → add to `translator_notes`

**What counts as "non-trivial" research finding:**
- ✓ Hidden meanings in names (e.g., 甄士隐 = 真事隐)
- ✓ Literary allusions to classics (e.g., references to Zhuangzi)
- ✓ Historical context needed for understanding
- ✓ Symbolic significance (e.g., numbers, colors, objects)
- ✓ Foreshadowing or callbacks to other parts
- ✗ Surface plot summary
- ✗ Generic character descriptions

### 2.2 Translation Order

For each segment:

1. **Translate to Modern Chinese first** - helps clarify meaning
2. **Then translate to English** - establishes scholarly register
3. **Then Russian** - adapt to Russian literary traditions
4. **Finally Japanese** - leverage classical Chinese heritage

### 2.3 Translation Quality Standards

#### Modern Chinese (简体中文)
- Use standard contemporary grammar
- Preserve literary beauty
- Explain archaic terms naturally
- Flow should be smooth and readable

#### English
- Scholarly but not dry
- Maintain literary register
- Use established terminology (see `research/glossary.md`)
- Poetry should read as poetry, not just accurate words

#### Russian (Русский)
- Literary Russian suitable for classics
- Draw on 19th-century Russian novel traditions
- Adapt honorifics appropriately
- Maintain aristocratic register where appropriate

#### Japanese (日本語)
- Classical-influenced literary style (文語的要素)
- Leverage shared kanji/classical heritage
- Use appropriate readings (音読み for names)
- Poetic elements should resonate with Japanese tradition

### 2.4 Translating Commentary

All commentary (夹批, 眉批, 侧批) must be translated:

```json
{
  "type": "夹批",
  "source": "甲戌本",
  "position": "inline after 真事隐去",
  "original": "甄士隐三字妙。",
  "zh_modern": ""甄士隐"这三个字用得妙。",
  "en": "The three characters 'Zhen Shiyin' are wonderfully chosen.",
  "ru": "Три иероглифа «Чжэнь Шиинь» великолепны.",
  "ja": "「甄士隠」の三字、妙なり。"
}
```

**Do NOT use shortcut formats**. All 4 languages required.

### 2.5 Reference Materials

Use these resources for consistency:
- `research/glossary.md` - Character names and terminology
- `research/character_guide.md` - Character voices and personalities
- `research/poetry_guide.md` - Approach to poetry translation
- `examples/page_example.json` - Format reference

---

## STEP 3: POLISH & VERIFY

### 3.1 Polish Each Translation

After completing first-draft translations, improve each language:

**Review checklist for each language:**
- □ Does it capture the literary beauty?
- □ Is the rhythm and flow natural?
- □ For poetry: is emotional impact preserved?
- □ Does it read as literature, not just accurate text?
- □ Are cultural elements appropriately adapted?

**Make at least one polish pass per language.**

Document your polish work:
```json
"polish_log": [
  {"language": "en", "iteration": 1, "changes": "Improved poetry rhythm in segment 2"},
  {"language": "ru", "iteration": 1, "changes": "Adjusted register for aristocratic dialogue"}
]
```

### 3.2 Completeness Verification

Before saving, verify:

- [ ] ALL main text translated
- [ ] ALL commentary translated
- [ ] ALL 4 languages complete for every segment
- [ ] NO null or empty string values
- [ ] Research notes contain non-trivial findings
- [ ] Sources documented (minimum 3)

### 3.3 Quality Checklist (MANDATORY)

Add this to your JSON:

```json
"quality_checklist": {
  "read_full_page": true,
  "identified_all_content": true,
  "researched_allusions": true,
  "consulted_min_3_sources": true,
  "all_commentary_translated": true,
  "all_4_languages_complete": true,
  "polished_each_language": true,
  "verified_completeness": true,
  "json_validated": true
}
```

All fields must be `true`. If any is `false`, the translation is incomplete.

### 3.4 JSON Validation

Before committing, validate:

```bash
python3 tools/validate_json.py translations/page_XXXX.json --strict
```

Fix any errors before proceeding.

---

## JSON Output Format

**Filename**: `translations/page_XXXX.json` (4-digit page number)

### Required Structure

```json
{
  "page": 20,
  "chapter": "第一回",
  "chapter_title": {
    "original": "...",
    "zh_modern": "...",
    "en": "...",
    "ru": "...",
    "ja": "..."
  },
  "page_content_type": "chapter_body",
  "segments": [
    {
      "id": 1,
      "pdf_page": 20,
      "type": "prose",
      "original": "Classical Chinese text...",
      "zh_modern": "Modern Chinese translation...",
      "en": "English translation...",
      "ru": "Russian translation...",
      "ja": "Japanese translation...",
      "commentary": [
        {
          "type": "夹批",
          "source": "甲戌本",
          "position": "inline after X",
          "original": "...",
          "zh_modern": "...",
          "en": "...",
          "ru": "...",
          "ja": "..."
        }
      ]
    }
  ],
  "translator_notes": [
    "Non-trivial finding 1 with source",
    "Non-trivial finding 2 with source"
  ],
  "research_sources": [
    {"title": "Source name", "type": "book|article|web", "finding": "What you learned"}
  ],
  "polish_log": [
    {"language": "en", "iteration": 1, "changes": "Description"}
  ],
  "quality_checklist": {
    "read_full_page": true,
    "identified_all_content": true,
    "researched_allusions": true,
    "consulted_min_3_sources": true,
    "all_commentary_translated": true,
    "all_4_languages_complete": true,
    "polished_each_language": true,
    "verified_completeness": true,
    "json_validated": true
  },
  "characters_appearing": ["甄士隐", "贾雨村"],
  "total_segments": 4,
  "manuscript_sources_on_page": ["甲戌本", "庚辰本"]
}
```

### Field Requirements

| Field | Required | Format |
|-------|----------|--------|
| `page` | Yes | Integer |
| `chapter` | Yes | String (e.g., "第一回") |
| `chapter_title` | Yes | Object with 5 translations |
| `page_content_type` | Yes | "front_matter" \| "chapter_body" \| "chapter_end" \| "appendix" |
| `segments` | Yes | Non-empty array |
| `segments[].original` | Yes | Non-empty string |
| `segments[].zh_modern` | Yes | Non-empty string |
| `segments[].en` | Yes | Non-empty string |
| `segments[].ru` | Yes | Non-empty string |
| `segments[].ja` | Yes | Non-empty string |
| `translator_notes` | Yes | Array with ≥1 non-trivial finding |
| `research_sources` | Yes | Array with ≥3 sources |
| `polish_log` | Yes | Array with ≥4 entries (one per language) |
| `quality_checklist` | Yes | All fields `true` |

---

## Common Pitfalls to Avoid

| ❌ Don't Do This | ✅ Do This Instead |
|-----------------|-------------------|
| Skip commentary | Translate ALL commentary |
| Generic research notes | Document specific findings with sources |
| First-draft only | Polish each language at least once |
| Leave fields empty | Every field must have content |
| Guess at meanings | Research thoroughly |
| Inconsistent names | Use glossary |
| Skip validation | Always validate before saving |
| Mechanical translation | Literary, polished translation |

---

## Time Budget

For a typical page (4-6 segments):

- **READ**: 10-15 minutes
- **RESEARCH**: 20-30 minutes
- **TRANSLATE**: 30-40 minutes
- **POLISH**: 15-20 minutes
- **VERIFY**: 5-10 minutes

**Total**: 80-115 minutes per page

Quality over speed. Better to complete 1 excellent page than 3 mediocre ones.

---

## Success Criteria

A successful translation has:
- ✓ Every piece of text on the PDF page translated
- ✓ Research documented with specific findings
- ✓ All 4 languages polished and literary
- ✓ Quality checklist all `true`
- ✓ JSON validates without errors

---

*This is a scholarly translation of one of world literature's masterpieces. Every sentence deserves careful attention. Take your time and do it right.*
