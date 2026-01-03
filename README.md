# 红楼梦 Multi-Agent Translation Project

**红楼梦脂评汇校本 → Modern Chinese, English, Russian, Japanese**

A collaborative multi-agent translation system for translating *Dream of the Red Chamber* (红楼梦), one of the Four Great Classical Novels of Chinese Literature, into four languages.

---

## Overview

This project uses **multiple AI agents working collaboratively** to translate all 120 chapters of 红楼梦 from Classical Chinese into:

- **Modern Chinese (简体中文)** - Accessible contemporary Mandarin
- **English** - Scholarly literary translation
- **Russian (Русский)** - Literary Russian
- **Japanese (日本語)** - Classical-influenced literary Japanese

### Why This Approach?

红楼梦 is an immense work (~800,000 characters) containing:
- Complex narrative prose
- Over 200 poems and songs
- Rich cultural allusions
- Wordplay and hidden meanings

Multi-agent collaboration allows:
- **Parallel progress** on different chapters
- **Consistent terminology** via shared glossary
- **Quality through coordination** between workers
- **Robust handling** of worker disconnections

---

## Multi-Agent Architecture

### Communication Method

Agents communicate via **git commits, pushes, and pulls**—using git as a message-passing interface.

### Worker Identity

- **Branch Name**: Full branch name (e.g., `cursor/honglou-translation-a1b2`)
- **Short ID**: Last 4 characters (e.g., `a1b2`) - used in commit messages
- **Registration**: Creating `WORKER_STATE.md` on your branch registers you as active

### Checking Who's Online

```bash
git fetch origin --prune
for branch in $(git branch -r | grep 'origin/cursor/' | sed 's|origin/||' | tr -d ' '); do
  if git show "origin/${branch}:WORKER_STATE.md" &>/dev/null 2>&1; then
    short_id=$(echo "$branch" | grep -oE '[^-]+$' | tail -c 5)
    echo "Active: $short_id ($branch)"
  fi
done
```

---

## Quick Start for Workers

1. **Identify yourself**:
   ```bash
   MY_BRANCH=$(git branch --show-current)
   MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
   ```

2. **Create WORKER_STATE.md**: Copy from template, fill in your info:
   ```bash
   cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
   # Edit with your details
   ```

3. **Push to register**: This makes you visible to other workers

4. **Sync and discover**: Fetch other workers' states

5. **Claim a chapter**: Lowest available chapter number

6. **Translate and push**: Save JSON, push, claim next

---

## Key Files

| File | Purpose |
|------|---------|
| `instructions.md` | Complete task instructions |
| `PROTOCOL.md` | Communication protocol |
| `STATE.md` | Global project state |
| `WORKER_STATE.md` | Your worker state (create this!) |
| `WORKER_STATE_TEMPLATE.md` | Template for new workers |

---

## Resources

### Source Material (Work Directly from PDF)
- `红楼梦脂评汇校本_有书签目录_v3.13.pdf` - Original source with Zhiping commentary

**IMPORTANT**: Work directly from PDF pages or screenshots. The 脂评汇校本 has complex formatting:
- Multiple commentary types (眉批, 夹批, 侧批, 回末批)
- Source manuscript tags (【甲戌】【庚辰】【己卯】etc.)
- Various formatting that plain text cannot preserve

### Research Documents (研究资料)
```
research/
├── glossary.md           # Character names & terminology (400+ entries)
├── chapter_structure.md  # All 120 chapter titles and summaries
├── cultural_context.md   # Qing Dynasty cultural context
├── character_guide.md    # Main character profiles and voices
├── poetry_guide.md       # Poetry translation approaches
├── commentary_guide.md   # Guide to commentary types & sources
```

### Example Translations
```
examples/
├── chapter_001_example.json   # Complete format example
```

### Tools
```
tools/
├── compile_chapters.py   # JSON → PDF compiler
├── validate_json.py      # Validate translation JSON
├── README.md             # Tool documentation
└── requirements.txt      # Python dependencies
```

---

## Work Organization

**Work is organized by PDF PAGE, not by chapter.**

The 脂评汇校本 contains 80 chapters plus front/back matter. Each PDF page is translated into one JSON file following the workflow:

```
RESEARCH → TRANSLATE → POLISH (润色)
```

## Translation Output Format

Each **PDF page** becomes a JSON file:

```json
{
  "page": 15,
  "chapter": "第一回",
  "chapter_title": {...},
  "page_content_type": "chapter_start",
  "segments": [
    {
      "id": 1,
      "type": "prose",
      "original": "Classical Chinese text...",
      "zh_modern": "Modern Chinese (polished)...",
      "en": "English (polished)...",
      "ru": "Russian (polished)...",
      "ja": "Japanese (polished)...",
      "commentary": [...]
    }
  ],
  "translator_notes": ["Research findings - required!"],
  "research_notes": ["Sources consulted"]
}
```

---

## Chapter Organization

### First 80 Chapters (Cao Xueqin)
| Range | Content |
|-------|---------|
| 1-5 | Frame narrative, Stone's origin |
| 6-18 | Daiyu arrives, Grand View Garden |
| 19-40 | Garden life, poetry clubs |
| 41-60 | Peak prosperity |
| 61-80 | Decline begins |

### Last 40 Chapters (attributed to Gao E)
| Range | Content |
|-------|---------|
| 81-96 | Examinations, marriage plot |
| 97-110 | Daiyu's death, family falls |
| 111-120 | Resolution, Baoyu becomes monk |

---

## Protocol Summary

1. **Sync regularly**: Every 2-3 minutes
2. **Claim one chapter at a time**: Lowest available
3. **Push immediately**: After claiming, after completing
4. **Heartbeat**: Update at least every 5 minutes
5. **Handle disconnection**: Reclaim chapters from offline workers (>15 min)

---

## Quality Guidelines

### Consistency
- Use `research/glossary.md` for all character names
- Maintain character voices per `research/character_guide.md`
- Follow poetry guidelines in `research/poetry_guide.md`

### Completeness
- Translate ALL segments (prose, poetry, dialogue)
- Include Zhiping commentary translations
- Add translator notes for cultural context

### Validation
```bash
python3 tools/validate_json.py translations/chapter_XXX.json
```

---

## Color Scheme (PDF Output)

| Language | Color |
|----------|-------|
| Classical Chinese (Original) | Black |
| Modern Chinese | Dark Gray |
| English | Dark Blue |
| Russian | Dark Red |
| Japanese | Dark Green |

---

## Project Background

红楼梦 (*Dream of the Red Chamber* / *The Story of the Stone*) is considered one of the greatest works of Chinese literature. Written by Cao Xueqin (曹雪芹) in the 18th century, it tells the story of the decline of a great aristocratic family through the eyes of Jia Baoyu and his relationships with his cousins Lin Daiyu and Xue Baochai.

This project aims to create a scholarly multilingual edition that:
- Makes the Classical Chinese accessible via Modern Chinese
- Provides quality literary translations for international readers
- Preserves the rich cultural context through annotations
- Enables comparative literary study across languages

---

## References

### Existing Major Translations

**English:**
- David Hawkes & John Minford - "The Story of the Stone" (Penguin)
- Yang Xianyi & Gladys Yang - "A Dream of Red Mansions" (FLP)

**Russian:**
- В. А. Панасюк - "Сон в красном тереме"

**Japanese:**
- 伊藤漱平 - "紅楼夢" (平凡社)

---

*See `instructions.md` for complete task details and `PROTOCOL.md` for collaboration rules.*

---

## Getting Started

```bash
# 1. Check your identity
MY_BRANCH=$(git branch --show-current)
MY_SHORT_ID=$(echo "$MY_BRANCH" | grep -oE '[^-]+$' | tail -c 5)
echo "I am: $MY_SHORT_ID"

# 2. Create your worker state
cp WORKER_STATE_TEMPLATE.md WORKER_STATE.md
# Edit WORKER_STATE.md with your info

# 3. Register
git add WORKER_STATE.md
git commit -m "[$MY_SHORT_ID] SYNC: Registering as active worker
HEARTBEAT: $(date +%s)"
git push origin HEAD

# 4. Start translating!
```

---

**让我们一起把这部伟大的文学作品呈现给世界！**

*Let's bring this masterpiece to the world together!*
