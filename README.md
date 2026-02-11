# SECA — Senior Evolvable Code Architect

> **Portable AI Memory System | 可跨项目携带的 AI 记忆系统**

[English](#english) | [中文](#中文)

---

## English

### What is this?

This is an **AI evolution directory** — a portable knowledge base that makes AI assistants "remember" across sessions and projects. Instead of starting from scratch every conversation, the AI reads these files to recall your coding style, project context, and lessons learned.

### Core Idea

```
Traditional AI:  Each conversation starts from zero.
With SECA:       AI reads _ai_evolution/ → instantly knows your style, your project, your rules.
```

### How it works

| File | Purpose |
|------|---------|
| `role-SECA.md` | AI behavior rules — coding standards, permissions, communication style |
| `agent_profile.md` | User preferences and working patterns |
| `project_context.md` | Current project architecture and key decisions |
| `last_session.md` | What happened last time, what to do next |
| `skills.md` | Reusable tools and skill catalog |
| `lessons_learned.md` | Engineering lessons extracted from real bugs |

### Architecture Principles

This system is built on **24 engineering principles** organized in 5 layers:

```
Layer 1: Philosophy     — KISS, YAGNI
Layer 2: Architecture   — Separation of Concerns, SSOT, Portability, ...
Layer 3: Design         — Open-Closed, Data Integrity
Layer 4: Practice       — Quality Gate, Quantifiable Thresholds, Deterministic-First
Layer AI: AI-Specific   — Context Window, Selective Memory, Token Economy, ...
```

Full index: [`session_notes/INDEX.md`](session_notes/INDEX.md)

### Key Design Decisions

- **Single source of truth** — Each rule lives in exactly one file
- **Lazy loading** — AI reads only 3 files at startup, loads others on demand
- **Deterministic-first** — Scripts over AI judgment, tools over sub-agents
- **Data has expiry dates** — External data is annotated with collection time and evidence strength

### Directory Structure

```
_ai_evolution/
├── role-SECA.md            # AI behavior rules (enforced)
├── agent_profile.md        # User preferences
├── project_context.md      # Project architecture
├── last_session.md         # Session checkpoint (git-ignored)
├── skills.md               # Skill & tool catalog
├── lessons_learned.md      # Transferable lessons
├── lessons_detail/         # Detailed lesson breakdowns
├── scripts/                # Deterministic automation scripts
├── skills/                 # Reusable skill definitions
├── workflows/              # Repeatable workflow procedures
└── session_notes/          # Experience notes & principle INDEX
    ├── INDEX.md            # Master principle index (24 principles)
    └── projects/           # Per-project session notes
```

### License

This is a personal knowledge management system. Feel free to fork and adapt the structure for your own AI workflow.

---

## 中文

### 这是什么？

这是一个 **AI 进化目录** — 一个可跨项目携带的知识库。它让 AI 助手能够跨对话、跨项目地"记住"你的编码风格、项目背景和经验教训。

### 核心理念

```
传统 AI：  每次对话从零开始。
有了 SECA：AI 读取 _ai_evolution/ → 立即了解你的风格、你的项目、你的规则。
```

### 工作原理

| 文件 | 用途 |
|------|------|
| `role-SECA.md` | AI 行为规则 — 编码规范、权限、沟通风格 |
| `agent_profile.md` | 用户偏好和工作模式 |
| `project_context.md` | 当前项目结构和关键决策 |
| `last_session.md` | 上次做了什么、下次做什么 |
| `skills.md` | 可复用工具和技能目录 |
| `lessons_learned.md` | 从真实 Bug 中提炼的工程经验 |

### 架构原则

本系统基于 **24 条工程原则**，分为 5 个层次：

```
第 1 层：哲学层     — KISS（简单）、YAGNI（不做多余的事）
第 2 层：架构层     — 关注点分离、单一事实来源、可移植性、...
第 3 层：设计层     — 开闭原则、数据完整性
第 4 层：实践层     — 质量门禁、可量化阈值、确定性优先
AI 层：AI 协作层   — 上下文窗口、选择性记忆、Token 经济学、...
```

完整索引：[`session_notes/INDEX.md`](session_notes/INDEX.md)

### 关键设计选择

- **单一事实来源** — 每条规则只在一个文件中定义
- **懒加载** — AI 启动时只读 3 个文件，其他按需加载
- **确定性优先** — 能用脚本就不用 AI 判断
- **数据有保质期** — 外部数据标注采集时间和证据强度

### 目录结构

```
_ai_evolution/
├── role-SECA.md            # AI 行为规则（强制执行）
├── agent_profile.md        # 用户偏好
├── project_context.md      # 项目架构
├── last_session.md         # 会话检查点（不上传 Git）
├── skills.md               # 技能和工具目录
├── lessons_learned.md      # 可迁移的经验
├── lessons_detail/         # 详细经验分类
├── scripts/                # 确定性自动化脚本
├── skills/                 # 可复用技能定义
├── workflows/              # 可重复的工作流程
└── session_notes/          # 经验笔记和原则索引
    ├── INDEX.md            # 原则主索引（24 条）
    └── projects/           # 按项目分类的会话笔记
```

### 许可

这是个人知识管理系统。欢迎 Fork 并根据你自己的 AI 工作流进行调整。
