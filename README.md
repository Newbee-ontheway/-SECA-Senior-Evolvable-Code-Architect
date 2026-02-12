# SECA — Senior Evolvable Code Architect

> 你的 AI 助手每次对话都**失忆**。SECA 让它长出**持久记忆、行为规则和可进化的知识体系**。
>
> 纯 markdown，无依赖，跨平台，跨模型。

[中文](#中文) | [English](#english)

---

## 中文

### 你可能正在经历这些

```
周一: "这个项目用 Typst 写教材，目录结构是……"
周二: "我昨天跟你说了，项目用 Typst……"
周三: "……算了，我重新说一遍"
```

- ❌ 每次开新对话，AI 从零开始 — 你变成了**人形 README**
- ❌ 说好的规则，下次就忘 — "不要动这个文件"说了三次，它还是动了
- ❌ 踩过的坑，再踩一遍 — 昨天修的 bug 今天换个写法又出现
- ❌ 换个模型换个工具，一切归零 — 你的"调教成果"锁死在一个平台里

### SECA 怎么解决

SECA 不是一个 system prompt — 是一个**放在项目里、跟着你走的 AI 操作系统**。

| 你的痛 | SECA 方案 | 实现方式 |
|--------|----------|----------|
| AI 失忆 | 秒级恢复上次状态 | `last_session.md` — 断点续传 |
| 说了不听 | 行为规则强制执行 | `role-SECA.md` — 119 行"AI 宪法" |
| 踩坑轮回 | 犯过的错写进记忆 | `lessons_learned.md` + 38 条工程规则 |
| 平台锁定 | 纯 markdown，model-agnostic | 复制文件夹 → 任何 AI 秒懂你 |

### 和其他方案的区别

| | `.cursorrules` / `CLAUDE.md` | 传统 system prompt | **SECA** |
|--|-----|------|------|
| 持久记忆 | ❌ | ❌ | ✅ 跨会话、跨项目 |
| 自动进化 | ❌ 手动维护 | ❌ | ✅ AI 自动提炼经验 |
| 知识体系 | ❌ 扁平规则 | ❌ | ✅ 28 条原则 + 38 条规则，分层索引 |
| 确定性验证 | ❌ | ❌ | ✅ 脚本自动检查，不靠 AI 自觉 |
| 可移植 | 🔒 绑定工具 | 🔒 绑定平台 | ✅ 纯 markdown，任意 LLM |

### 核心架构

```
_ai_evolution/
├── role-SECA.md            # 行为规则 — 119 行"AI 宪法"，5 条绝对法则置顶
├── last_session.md         # 断点续传 — 不上传 Git，本地专用
├── project_context.md      # 项目结构 + 关键决策
├── agent_profile.md        # 你的偏好 + 工作模式
├── skills.md               # 技能 + 工具目录
├── lessons_learned.md      # 踩坑记录
├── scripts/                # 确定性自动化（脚本 > AI 判断）
│   ├── validate_sessions.py    # 笔记一致性校验
│   └── check_file_size.py      # 400 行法则自动检查
├── workflows/              # 可重复流程（git sync 等）
└── session_notes/
    ├── INDEX.md            # 28 条工程原则（5 层分类，紧凑索引）
    ├── RULES_CATALOG.md    # 38 条规则按类别总目录
    ├── layers/             # 原则详细定义（按需加载）
    └── projects/           # 按项目分类的经验笔记
```

### 设计原则

- **Token 意识** — 启动只读 3 个文件，按需加载，不浪费上下文窗口
- **确定性优先** — 能用脚本检查的就不靠 AI 自觉。`脚本 > 工具 > MCP > 子代理`
- **单一真相源** — 每条规则只在一个地方定义，不重复，不矛盾
- **数据有保质期** — 所有外部信息标注采集时间和证据强度
- **记忆有容量** — 索引文件 ≤100 条，每 session 最多推 1 条到长期记忆，主动修剪

### 快速开始

```bash
# 克隆到你的项目
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# 在 AI 对话开头说
"请先读取 _ai_evolution/role-SECA.md，然后读 last_session.md 恢复状态"

# 就这样。AI 会自动在 session 结束时更新索引。
# 换项目时复制 _ai_evolution/ 文件夹 — AI 马上"认识"你。
```

> **注意**: `last_session.md` 不包含在 Git 中。首次使用时 AI 会自动创建。

---

## English

### The Problem

Your AI assistant has **amnesia**. Every new conversation starts from zero. Rules you set are forgotten. Mistakes are repeated. Your "trained" AI is locked to one platform.

SECA fixes this. It's not a system prompt — it's a **portable AI operating system** that lives in your project as plain markdown files.

### What SECA Does

| Pain Point | Solution | How |
|-----------|----------|-----|
| AI amnesia | Instant session restore | `last_session.md` — checkpoint/resume |
| Rules ignored | Enforced behavior rules | `role-SECA.md` — 119-line "AI constitution" |
| Repeated mistakes | Persistent error memory | `lessons_learned.md` + 38 engineering rules |
| Platform lock-in | Model-agnostic markdown | Copy folder → any LLM knows you instantly |

### vs. Alternatives

| | `.cursorrules` / `CLAUDE.md` | System prompts | **SECA** |
|--|-----|------|------|
| Persistent memory | ❌ | ❌ | ✅ Cross-session, cross-project |
| Self-evolution | ❌ Manual | ❌ | ✅ AI auto-extracts lessons |
| Knowledge system | ❌ Flat rules | ❌ | ✅ 28 principles + 38 rules, layered index |
| Deterministic checks | ❌ | ❌ | ✅ Scripts verify, not AI self-discipline |
| Portable | 🔒 Tool-locked | 🔒 Platform-locked | ✅ Pure markdown, any LLM |

### Quick Start

```bash
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# Tell your AI at conversation start:
"Read _ai_evolution/role-SECA.md first, then read last_session.md to restore state"

# That's it. SECA auto-updates indexes at session end.
# Moving projects? Copy the folder — AI remembers you.
```

---

## Stats

- **28** engineering principles across 5 layers
- **38** battle-tested rules with source links
- **119** lines of enforced behavior rules
- **2** deterministic validation scripts
- **0** dependencies — pure markdown

## License

MIT
