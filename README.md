# SECA — Senior Evolvable Code Architect

> 一个放在项目里、跟着你走的 AI 协作框架。
> 纯 markdown + Python 脚本，让 AI 在对话间保持记忆、遵守规则、持续进化。

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

SECA 是一个文件夹。你把它放进任何项目里，AI 就能在对话开始时读取它，知道：
- **你是谁** — 工作偏好、沟通风格、决策习惯
- **上次做到哪了** — 自动恢复进度，不用复述
- **哪些规则要遵守** — 写在文件里的行为约束，不靠"请你记住"
- **踩过哪些坑** — 长期经验库，同一个错不再犯第二遍

它不是一段 system prompt，也不是一个特定平台的功能。它是一套**纯文本的 AI 记忆和行为系统**，任何 LLM 都能读。

### 特色

- **跨会话记忆** — `last_session.md` 是每次对话的断点续传文件，AI 启动即恢复
- **行为规则体系** — `role-SECA.md` 定义绝对法则和执行策略，不是建议而是约束
- **经验沉淀** — 人和 AI 共同积累的原则、规则、教训，分层索引按需加载
- **自动化脚本** — 能用脚本做的事（校验、搜索、检查）绝不让 AI 凭"自觉"
- **可移植** — 复制文件夹到新项目或换模型，零迁移成本
- **轻量** — 核心是 markdown 文件，脚本仅依赖 Python 标准库 + 少量 pip 包

### 设计直觉

1. **Token 是稀缺资源** — 启动只读 3 个文件（~800 tokens），其余按需加载
2. **确定性优先** — 能用脚本检查的事不交给 AI 判断，脚本比"请你记住"靠谱
3. **工具优先** — 苦力活交给脚本，贵的模型只做需要判断力的事
4. **造轮子前先找轮子** — 写工具前先搜现成方案，80 分就用
5. **记忆有容量** — 索引限量、经验主动修剪，不堆砌

### 项目结构

```
_ai_evolution/
├── role-SECA.md            # AI 行为规则 — 绝对法则 + 执行策略
├── last_session.md         # 断点续传 — 本地专用，不入 git
├── project_context.md      # 项目结构 + 工具清单 + 关键决策
├── agent_profile.md        # 用户偏好和工作节奏
├── skills.md               # 技能清单（8 项 Skill）+ 工具选型
├── lessons_learned.md      # 踩坑记录
├── scripts/                # 自动化脚本
│   ├── local_search.py        # BM25 本地全文搜索（tantivy）
│   ├── search.py              # 批量网络搜索（ddgs）
│   ├── rss_fetcher.py         # RSS 抓取
│   ├── session_bootstrap.py   # 启动上下文压缩
│   ├── index_check.py         # 索引一致性校验
│   └── ...                    # 更多校验和工具脚本
├── workflows/              # 可重复工作流（斜杠命令触发）
│   ├── research.md            # /research — 深度研究
│   ├── search_before_build.md # /search_before_build — 造轮子前先找轮子
│   ├── rss_briefing.md        # /rss_briefing — AI 筛选日报
│   ├── session_end.md         # /session_end — 会话结束清理
│   ├── git_sync.md            # /git_sync — 安全同步到 GitHub
│   └── distributed_execution.md # /distributed_execution — 分步执行大任务
├── readings/               # 研究笔记和日报输出
└── session_notes/
    ├── INDEX.md            # 工程原则索引（5 层分类）
    ├── RULES_CATALOG.md    # 规则总目录
    └── projects/           # 按项目分类的经验笔记
```

### 快速开始

```bash
# 克隆到你的项目根目录
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# 在 AI 对话开头说：
"读一下 _ai_evolution/role-SECA.md 和 last_session.md"

# AI 会恢复上下文，接上你上次的进度。
# 换项目或换模型？复制 _ai_evolution/ 文件夹即可。
```

> `last_session.md` 和 `agent_profile.md` 不在 git 中（.gitignore），首次使用时 AI 会自动创建。

---

## English

### What is this

SECA is a folder. Drop it into any project and your AI assistant can read it at the start of every conversation to know:
- **Who you are** — preferences, communication style, decision patterns
- **Where you left off** — automatic session restore, no re-explaining
- **What rules to follow** — written constraints, not "please remember"
- **What mistakes to avoid** — persistent lessons from past sessions

It's a **plain-text AI memory and behavior system** that works with any LLM.

### Features

- **Cross-session memory** — `last_session.md` acts as a checkpoint file; AI restores on startup
- **Behavior rules** — `role-SECA.md` defines absolute laws and execution strategies
- **Experience accumulation** — principles, rules, and lessons indexed in layers, loaded on demand
- **Automation scripts** — validation, search, and checks are scripted, not left to AI "self-discipline"
- **Portable** — copy the folder to a new project or switch models at zero cost
- **Lightweight** — core is markdown files; scripts need only Python + minimal pip packages

### Design Intuitions

1. **Tokens are scarce** — startup reads 3 files (~800 tokens); everything else loads on demand
2. **Determinism first** — if a script can verify it, don't ask the AI to remember it
3. **Tools first** — grunt work goes to scripts; expensive models only do judgment calls
4. **Search before build** — find an 80% solution before writing your own
5. **Memory has capacity** — indexes are capped, old lessons get pruned, no hoarding

### Quick Start

```bash
git clone https://github.com/Newbee-ontheway/-SECA-Senior-Evolvable-Code-Architect.git _ai_evolution

# Tell your AI at the start of any conversation:
"Read _ai_evolution/role-SECA.md and last_session.md"

# It picks up where you left off.
# Switching projects or models? Just bring the folder.
```

> `last_session.md` and `agent_profile.md` are gitignored. AI creates them on first use.

## License

MIT
