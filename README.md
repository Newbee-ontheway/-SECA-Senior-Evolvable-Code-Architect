# SECA — Senior Evolvable Code Architect

> 你的 AI 每次对话都失忆。SECA 让它长出持久记忆、行为规则和一套能跟着你成长的知识体系。
>
> 纯 markdown，无依赖，跨平台，跨模型。带着这个文件夹，走到哪里 AI 都认识你。

[中文](#中文) | [English](#english)

---

## 中文

### 场景：你可能正在经历这些

```
周一: "这个项目用 Typst 写教材，目录结构是……"
周二: "我昨天跟你说了，项目用 Typst……"
周三: "……算了，我重新说一遍"
```

每次新对话，都得把 AI 当新人重新带一遍。说好的规则，它转头就忘。踩过的坑，换个说法又踩一遍。更别提换一个模型、换一个工具——一切归零。

你辛辛苦苦攒下的"调教成果"，全锁在一个平台的上下文里，随时会蒸发。

### SECA 是什么

SECA 不是一个 system prompt，也不是一段复制粘贴的咒语。它是一个**放在项目里、跟着你走的 AI 协作框架**——用一堆 markdown 文件，告诉任何 AI"我是谁、我做过什么、接下来该怎么做"。

| 你的痛 | SECA 怎么治 | 靠什么 |
|--------|-----------|--------|
| AI 失忆 | 秒级恢复上次状态 | `last_session.md` — 每次对话的断点续传 |
| 说了不听 | 行为规则白纸黑字 | `role-SECA.md` — AI 宪法，置顶绝对法则 |
| 踩坑轮回 | 犯过的错写进长期记忆 | `lessons_learned.md` + 工程规则库 |
| 平台锁定 | 纯文本，哪个 AI 都能读 | 复制文件夹 → 换模型零成本 |

### 和市面方案的区别

| | `.cursorrules` / `CLAUDE.md` | system prompt | **SECA** |
|--|-------|------------|------|
| 持久记忆 | ❌ | ❌ | ✅ 跨会话、跨项目 |
| 自我进化 | ❌ 全靠手动 | ❌ | ✅ AI 主动提炼经验 |
| 知识体系 | ❌ 一堆扁平规则 | ❌ | ✅ 29+ 原则 · 38+ 规则 · 分层索引 |
| 确定性验证 | ❌ | ❌ | ✅ 用脚本检查，不靠 AI 自觉 |
| 可移植性 | 🔒 绑定特定工具 | 🔒 绑定特定平台 | ✅ 纯 markdown，不挑 LLM |

### 项目结构

```
_ai_evolution/
├── role-SECA.md            # AI 宪法 — 行为规则 + 绝对法则 + 执行策略
├── last_session.md         # 断点续传 — 本地专用，不上传
├── project_context.md      # 项目结构 + 关键决策快照
├── agent_profile.md        # 你的偏好和工作节奏
├── skills.md               # 技能清单 + 工具选型表
├── lessons_learned.md      # 踩坑记录 — 犯一次就够了
├── scripts/                # 自动化脚本（脚本 > AI 判断）
│   ├── validate_sessions.py    # 笔记规则号一致性校验
│   ├── check_file_size.py      # 400 行法则检查
│   ├── search.py               # 批量搜索（ddgs，省 10x token）
│   ├── pre_commit_check.py     # Git 提交前统一检查入口
│   └── install_hooks.py        # pre-commit hook 一键安装
├── workflows/              # 可重复工作流（git sync 等）
└── session_notes/
    ├── INDEX.md            # 29 条工程原则（5 层分类索引）
    ├── RULES_CATALOG.md    # 38+ 条规则按类别总目录
    ├── layers/             # 原则详解（按需加载，不占启动 token）
    └── projects/           # 按项目分类的经验笔记 + sparks
```

### 背后的几个设计直觉

1. **Token 是稀缺资源** — 启动只读 3 个文件。其余按需加载，不浪费上下文窗口。
2. **确定性优先** — 能用脚本检查的事，别让 AI 凭自觉。脚本永远比"请你记住"靠谱。
3. **工具优先** — 苦力活交给脚本或便宜的模型，贵的模型只做判断。
4. **造轮子前先找轮子** — 写工具前先搜 GitHub，找到 80 分方案就用。
5. **记忆有容量** — 索引文件限 ≤100 条，长期记忆主动修剪，不堆砌。

### 快速开始

```bash
# 克隆到你的项目根目录
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# 在 AI 对话开头说一句：
"读一下 _ai_evolution/role-SECA.md 和 last_session.md"

# AI 会自己恢复上下文，接上你上次的进度。
# 换项目？换模型？复制 _ai_evolution/ 文件夹就行。
```

> `last_session.md` 不包含在 Git 中（.gitignore），首次使用时 AI 会自动创建。

---

## English

### The Problem

Your AI assistant has amnesia. Every conversation starts from scratch. Rules you painstakingly set get forgotten on the next chat. Bugs you already fixed reappear in new disguises. And all your "training effort" is locked inside one platform's context window, ready to evaporate.

SECA fixes this. It's not a system prompt you copy-paste. It's a **portable AI collaboration framework** — a folder of plain markdown files that tells any LLM who you are, what you've built, and how to keep going.

### What It Does

| Pain Point | Fix | Mechanism |
|-----------|-----|-----------|
| AI amnesia | Instant session restore | `last_session.md` — checkpoint & resume |
| Rules ignored | Written-down behavior rules | `role-SECA.md` — an "AI constitution" with absolute laws |
| Repeated mistakes | Persistent error memory | `lessons_learned.md` + engineering rules catalog |
| Platform lock-in | Pure text, any LLM reads it | Copy the folder → zero migration cost |

### vs. Alternatives

| | `.cursorrules` / `CLAUDE.md` | System prompts | **SECA** |
|--|-----|------|------|
| Persistent memory | ❌ | ❌ | ✅ Cross-session, cross-project |
| Self-evolution | ❌ Manual | ❌ | ✅ AI auto-extracts lessons |
| Knowledge system | ❌ Flat rules | ❌ | ✅ 29+ principles · 38+ rules · layered index |
| Deterministic checks | ❌ | ❌ | ✅ Scripts verify, not AI self-discipline |
| Portable | 🔒 Tool-locked | 🔒 Platform-locked | ✅ Pure markdown, any LLM |

### Quick Start

```bash
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# Tell your AI at the start of any conversation:
"Read _ai_evolution/role-SECA.md and last_session.md"

# That's it. It picks up where you left off.
# Switching projects or models? Just bring the folder.
```

---

## By the Numbers

- **29** engineering principles across 5 layers
- **38+** battle-tested rules, each traced to a real session
- **11** AI-specific collaboration principles (context, memory, cognition...)
- **5** automation scripts (no AI self-discipline required)
- **0** dependencies — it's just markdown

## License

MIT
