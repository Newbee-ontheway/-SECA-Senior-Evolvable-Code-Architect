# SECA — Senior Evolvable Code Architect

> 一个让 AI 助手 **写代码、记经验、会进化** 的开源框架，专为编程初学者设计。

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么？

SECA 不只是一个文件夹 — 它是一套 **AI 协作框架**，解决三个问题：

| 问题 | 传统 AI | 有了 SECA |
|------|--------|----------|
| 每次对话从零开始 | 你得反复解释项目背景 | AI 自动读取上次状态，秒级恢复 |
| AI 犯过的错不记住 | 同样的坑踩两遍 | 经验写入 lessons，不再重犯 |
| 规则全靠口头约定 | 说了不一定听 | 行为规则写进文件，强制执行 |

### 三大能力

**🔧 写代码** — 遵循明确的编码规范、权限协议和质量门禁，输出专业级代码。不偷懒（禁止 `// ... existing code`），不猜测（不确定就问）。

**📝 记知识** — 每次对话后自动提炼经验、更新索引。目前积累了 **24 条工程原则**，从哲学层（KISS）到 AI 协作层（Token 经济学），形成可检索的知识体系。

**🧬 会进化** — 解决新问题后自动提炼为可复用技能。跨项目携带时，AI 立即"认识"你 — 你的编码风格、项目偏好、踩过的坑。

### 为什么适合初学者？

- **透明**：所有规则、记忆、技能都是普通 markdown 文件，你能看懂、能修改
- **有约束**：AI 的行为受文件控制，不是靠运气 — 写操作必须问你，大改动必须先提案
- **有积累**：你的每一次对话都在给 AI "升级"，而不是用完即弃
- **有教学**：INDEX 里的 24 条原则配有通俗解释和类比，本身就是一份软件工程入门教材

### 核心文件

```
_ai_evolution/
├── role-SECA.md            # AI 行为规则（强制执行的"法律"）
├── last_session.md         # 上次做了什么（断点续传，不上传 Git）
├── project_context.md      # 项目结构和关键决策
├── agent_profile.md        # 你的偏好和工作模式
├── skills.md               # 技能和工具目录
├── lessons_learned.md      # 踩坑记录
├── scripts/                # 确定性自动化脚本
├── workflows/              # 可重复的工作流程
└── session_notes/
    ├── INDEX.md            # 24 条工程原则索引（知识图谱）
    └── projects/           # 按项目分类的经验笔记
```

### 设计哲学

- **单一事实来源** — 每条规则只在一个文件中定义，不重复
- **懒加载** — 启动时只读 3 个文件，按需加载其他内容，节省 Token
- **确定性优先** — 能用脚本的不用 AI 判断，能用工具的不用子代理
- **数据有保质期** — 所有外部数据标注采集时间和证据强度

### 怎么用？

1. 把 `_ai_evolution/` 文件夹放到你的项目根目录
2. 让 AI 在对话开始时读取 `role-SECA.md`
3. 正常工作 — SECA 会自动在 session 结束时更新索引
4. 换项目时，复制整个文件夹即可 — AI 马上"认识"你

---

## English

### What is this?

SECA is not just a folder — it's an **AI collaboration framework** that gives your AI assistant three abilities:

| Problem | Traditional AI | With SECA |
|---------|---------------|-----------|
| Every conversation starts from zero | You re-explain everything | AI reads last session state, resumes instantly |
| AI repeats the same mistakes | Falls into the same traps | Lessons are recorded, never repeated |
| Rules are verbal agreements | Sometimes followed, sometimes not | Behavior rules are in files, enforced |

### Three Core Capabilities

**🔧 Code** — Follows strict coding standards, permission protocols, and quality gates. No lazy output (`// ... existing code` is banned). When uncertain, asks instead of guessing.

**📝 Learn** — After each session, automatically extracts lessons and updates indexes. Currently holds **24 engineering principles** spanning from philosophy (KISS) to AI-specific (Token Economy), forming a searchable knowledge system.

**🧬 Evolve** — Automatically distills new solutions into reusable skills. When carried to a new project, the AI instantly "knows" you — your coding style, preferences, and past mistakes.

### Why is it beginner-friendly?

- **Transparent**: All rules, memory, and skills are plain markdown files you can read and edit
- **Constrained**: AI behavior is controlled by files, not luck — write operations require permission, major changes need proposals
- **Cumulative**: Every conversation upgrades your AI, nothing is wasted
- **Educational**: The 24 principles in INDEX come with plain-language explanations and analogies — it doubles as a software engineering primer

### How to use

1. Place `_ai_evolution/` in your project root
2. Have the AI read `role-SECA.md` at conversation start
3. Work normally — SECA auto-updates indexes at session end
4. Moving to a new project? Copy the folder — AI remembers you instantly
