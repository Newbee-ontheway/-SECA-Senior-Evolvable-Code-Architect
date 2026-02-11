# Project Context (项目上下文)

This file stores high-level architectural decisions and domain knowledge.
It ensures that the AI understands the "Big Picture" even after memory resets.

**Last Updated**: 2026-02-10

## 1. Project Overview

- **Name**: V3.5_System_Export
- **Goal**: Self-learning AI curriculum designer: JSON → Typst → PDF
- **Core Logic**: `agent_rules/V3.5_Golden_Rulebook.md` (1062 lines, 30KB)
- **Boot**: `README_AND_BOOT.md`

## 2. V3.5 Architecture

### 3-Role Pipeline

```text
Architect (分析) → Builder (生成) → Compiler (编译)
  ↓                  ↓                ↓
Design Brief    JSON Schema     Typst → PDF
  P0/P1/P2        3 Phases
  Theme选择        Components
```

### 3 Generation Phases

| Phase | Purpose | Layout |
|-------|---------|--------|
| Phase 1: Discovery | 视觉引入、quiz/gamification | Visual-heavy |
| Phase 2: Scaffolding | 模式操练、递进难度 | Drill-focused |
| Phase 3: Exam | 模拟高考、完形填空 | Exam-paper |

### 5 Fixed Themes

| Theme | Mood | Primary Color |
|-------|------|---------------|
| `swiss_minimal` | 理科/逻辑 | Klein Blue #0044CC |
| `oxford_classic` | 文学/故事 | Oxford Blue #1B365D |
| `nature_wisdom` | 环保/生物 | Sage Green #3A6B56 |
| `retro_poster` | 侦探/历史 | Caramel #B85C38 |
| `tech_future` | 科技/AI | Neon Blue #38BDF8 |

### Supervised Learning Loop

```text
Generate unit → AI proposes new skill → User approves → Save to library
```

### Feedback Protocol (3-Level)

| Level | Scope | Action |
|-------|-------|--------|
| 🟢 LOCAL | Typo, single item | Fix immediately |
| 🟡 SKILL | Teaching strategy | Update skill file, regenerate |
| 🔴 SYSTEM | Golden Rulebook rule | STOP, wait for user confirmation |

## 3. My Tools (in `_ai_evolution/`)

| Tool | Path | Purpose |
|------|------|---------|
| Structure Validator | `_ai_evolution/scripts/verify_structure.py` | Check broken markdown links |
| Dependency Graph | `_ai_evolution/scripts/md_dependency_graph.py` | Visualize .md cross-references |
| Skills Library | `_ai_evolution/skills.md` | Skill catalog + tool reference |
| Agent Profile | `_ai_evolution/agent_profile.md` | Cross-project user preferences |
| Session Handoff | `_ai_evolution/last_session.md` | Resume from where I left off |
| Lessons Learned | `_ai_evolution/lessons_learned.md` | Operational error log |
| Installed Skills | `_ai_evolution/skills/` | External agent skills |

## 4. Key Project Paths

```text
agent_rules/V3.5_Golden_Rulebook.md   # System logic (DO NOT OWN)
agent_rules/skills/                    # Teaching strategies (22 files)
agent_script/skills_library.py         # Skills CRUD (project asset)
agent_script/skill_recorder.py         # Auto-learn from output
library/knowledge/grammar/             # Topic knowledge files
templates/lib-colors.typ               # 5-theme color system
workspace/                             # User input files (highest priority)
output/                                # Generated units appear here
```

> **Note**: `agent_script/verify_structure.py` and `agent_script/md_dependency_graph.py`
> are identical copies of my scripts in `_ai_evolution/scripts/`. My copies are canonical.

## 5. Key Decisions

- **5 fixed themes**: No custom colors allowed — must use theme palette
- **Priority**: workspace/ > skills/ > library/knowledge/
- **Typst imports**: `../templates/lib-colors.typ` (relative from units/)
- **Skills**: Teaching strategies in `agent_rules/skills/`, NOT code skills

## 6. Verification Status (2026-02-10)

- Path References: 0 broken links
- Doc Coverage: 76.9%
- Dependency Graph: 133 files, 18 refs, 0 broken
