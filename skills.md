# AI Skills Library

This file stores reusable skills, patterns, and code snippets learned during the project.
It is designed to be portable across projects.

## Format

### [Skill Name]

- **Context**: When to use this skill.
- **Solution**: The code characteristic or pattern.
- **Example**:

```language
// Code snippet
```

---

## Skills

### 0. Web Content Reading (Tool Selection)

- **Context**: When user provides a URL or you need to read web content, choose the right tool.

| Condition                              | Tool                                | Why                                              |
| -------------------------------------- | ----------------------------------- | ------------------------------------------------ |
| No URL yet, need to find articles      | `search_web`                        | Fast, returns summaries + links                  |
| URL is a blog post / docs / article    | `read_url_content`                  | Fast, no JS needed, converts HTML to markdown    |
| URL is GitHub (github.com/...)         | `read_url_content` with **raw URL** | Replace `github.com/.../blob/main/` with `raw.githubusercontent.com/.../main/` |
| URL is a JS-heavy app (SPA, dashboard) | `browser_subagent`                  | Last resort, slow but can execute JS             |
| URL requires login or interaction      | `browser_subagent`                  | Only tool that can handle auth flows             |
| Not sure which to use                  | Try `read_url_content` first        | If it fails, fall back to `browser_subagent`     |

- **Default strategy**: `read_url_content` first → `browser_subagent` as fallback
- **Never** use `browser_subagent` for plain text content — it wastes resources

---

### 1. Structure Verification Script

- **Context**: Projects with many relative path references in docs need validation that all links point to real files.
- **Solution**: Python script scans all `.md` files for markdown links and verifies targets exist.
- **Location**: `_ai_evolution/scripts/verify_structure.py`
- **Usage**:

```bash
cd [project_root]
python _ai_evolution/scripts/verify_structure.py
```

- **Prerequisites**: Python 3.6+, no external dependencies
- **Key Design**: Only checks `[text](path)` format links; ignores code blocks and inline code examples.
- **Best Practice**: Always run this **after** moving/renaming files — don't wait for broken links to surface later.

---

### 2. Authoritative Structure File

- **Context**: Multiple docs describing directory structure tend to drift out of sync.
- **Solution**: Create `STRUCTURE.md` as single source of truth. Other docs reference it instead of maintaining their own descriptions.
- **Location**: Project root `STRUCTURE.md`
- **Rule**: After any directory structure change → update `STRUCTURE.md` first → then run verification script.
- **Best Practice**: Explain "why" this structure exists, not just "what" it looks like. Future developers need the rationale behind the design decisions (ADR principle).

---

### 3. README Indexing Principles

- **Context**: Deciding which directories need a `README.md` index file.
- **Rule**: Indexes are designed for cases where **discovery cost > maintenance cost**.

**Needs index**:

| Scenario | Reason |
|----------|--------|
| Complex directory (10+ files) | Many files, mixed categories; index aids navigation |
| Public interface directory | Others/agents need quick overview of available resources |
| User-facing directory | Needs input/output format expectations explained |

**Skip index**:

| Scenario | Reason |
|----------|--------|
| Single-file directory | Self-explanatory |
| Internal implementation | External access not needed |
| Frequently changing dir | Maintenance cost > benefit |

---

### 4. Project Architecture Discovery Flow

- **Context**: When entering a new project, avoid carrying assumptions from previous projects.
- **Process**:

```
1. List root directory files → identify core files (README, STRUCTURE, Golden Rulebook)
2. Read STRUCTURE.md or README → understand official structure definition
3. Scan major directories → analyze file naming patterns, function categories
4. Identify conventions: skills location, config location, output location
5. Record findings in _ai_evolution/project_context.md
```

- **Output**: A cognitive map of the project, preventing incorrect assumptions.
- **Best Practice**: Start with the file tree — see which layers the code touches and identify cross-layer coupling. Focus on module boundaries and separation of concerns, not syntax details (macro-first review).

---

### 5. Post-Fix Prevention (Systematic Bug Prevention)

- **Context**: After fixing a bug, proactively propose how to prevent recurrence at the process/tooling level.
- **Three-layer defense**:

| Layer | Method | Example |
|-------|--------|---------|
| **Tooling** | Write verification scripts | `verify_structure.py` auto-detects broken links |
| **Process** | Establish checkpoints | Must run verification after moving files |
| **Documentation** | Record lessons learned | Write to `_ai_evolution/lessons_learned.md` |

- **Best Practice**: If the code is not testable, it is not reliable. When designing fixes, ask "how would I verify this never happens again?" before closing the issue.

---

### 6. Script Prerequisites Template

- **Context**: Scripts may fail when migrated to different projects/environments. Prerequisites must be explicit.
- **Every script must include**:

```markdown
## Prerequisites
- **Python Version**: 3.8+
- **Dependencies**: None / requirements.txt
- **Working Directory**: Must run from project root
- **Expected Files**: Requires `STRUCTURE.md` to exist
- **OS Compatibility**: Windows/Linux/macOS

## Known Limitations
- Does not check paths inside code blocks
- Cannot verify external URLs
```

---

### 7. External Skill Isolation

- **Context**: Installing skills via `npx skills add` defaults to shared directories (`.agents/`, `.agent/`), potentially interfering with other agents.
- **Solution**: Always copy needed content to exclusive folder (`_ai_evolution/skills/`), then clean up shared directories **only if they were created by me**.
- **Process**:

```
1. BEFORE install: Check if .agents/ and .agent/ already exist
2. AFTER install: Copy needed files to _ai_evolution/skills/
3. CLEANUP:
   ✅ Directory was created by this installation → safe to delete
   ❌ Directory existed before → NEVER delete, only remove my added files
```

- **Installed Skills**: See `_ai_evolution/skills/` directory for individual SKILL.md files.

---

### 8. Search Intent Clarification

- **Context**: When user asks you to "look something up", "research X", or "find out about Y", **classify intent first**. Don't jump straight into searching.
- **Rule**: If intent is ambiguous, **ask the user** — show them the types below and let them pick. Don't guess.
- **Decision Tree**:

| User Says (Pattern) | Intent Type | Action |
|---|---|---|
| "这个是什么？" / "X 怎么用？" / factual question | **Quick Answer** | `search_web` → read top 1-2 results via `read_url_content` → answer inline. No file saved. |
| "最佳实践？" / "别人怎么做的？" / "有什么好的 X？" | **Landscape Scan** | 3 different search queries → read 3-5 articles → summarize options **with tradeoffs**. Save to `readings/` if substantial. |
| "A 和 B 哪个好？" / "对比一下" | **Comparison** | Parallel searches for A and B → structured comparison table (features, pros, cons, use cases). |
| "我之前写过..." / "在哪个笔记里提过 X？" | **Local Recall** | `grep_search` / `find_by_name` across project dirs. **No web search needed.** |
| "帮我深入研究 X" / explicit "research" | **Deep Research** | Follow `/research` workflow (see `_ai_evolution/workflows/research.md`). |

- **Key Principle**: The user often doesn't know which type they need. If they say something vague like "查一下 X", proactively offer: "你想要快速回答, 还是全面对比, 还是深入研究?" — this 5-second clarification saves minutes of wrong-direction work.
- **Upstream of Skill #0**: This skill (intent classification) runs BEFORE Skill #0 (tool selection). First decide *what* to do, then decide *which tool* to use.

---

## Tool Catalog

Reference of useful tools across project types. Evaluated for relevance to SECA work.
**Review schedule**: Manual trigger only — user says "审查skills". Prune unused, merge overlapping, update paths.

### For JS/TS Projects

| Tool | Purpose | Install |
|------|---------|---------|
| **dependency-cruiser** | Dependency graph validation & visualization | `npm install -D dependency-cruiser` |
| **madge** | Circular dependency detection + graph | `npm install -D madge` |
| **Remark** | Markdown linting & transformation | `npm install -D remark-cli` |
| **Vibe-Poo** | AI-powered code quality checker for AI-generated code | `npm install -g vibe-poo` |

> **Vibe-Poo** triggers when: checking quality of AI-generated (Vibe Coding) JS/TS/Python code. Detects oversized files (>800 lines), poor variable scoping, dead code. Requires OpenAI API key. Repo: `github.com/karminski/vibe-poo`.

### For Python Projects

| Tool | Purpose | Install |
|------|---------|---------|
| **Ruff** | Ultra-fast Python linter + formatter (replaces Flake8/Pylint/isort) | `pip install ruff` |
| **Mypy** | Static type checking | `pip install mypy` |
| **Pytest** | Testing framework | `pip install pytest` |
| **commitizen** | Conventional commits + changelog for Python | `pip install commitizen` |

### For Documentation Projects (Markdown/Typst)

| Tool | Purpose | Install |
|------|---------|---------|
| **markdownlint** | Markdown style enforcement | `npm install -D markdownlint-cli` |
| **MkDocs + Material** | Generate documentation sites from MD | `pip install mkdocs-material` |
| **Typst CLI** | Compile Typst documents | `typst compile file.typ` |

### For Release & Changelog

| Tool | Purpose | Install |
|------|---------|---------|
| **changelog-automation** (Agent Skill) | Conventional Commits + changelog guide | Installed in `_ai_evolution/skills/` |
| **git-cliff** | Fast changelog generation from commits | `cargo install git-cliff` or binary |
| **standard-version** | Bump version + generate changelog (Node.js) | `npm install -D standard-version` |
| **semantic-release** | Fully automated releases | `npm install -D semantic-release` |

### Custom Tools (in `_ai_evolution/scripts/`)

| Tool | Purpose | Usage |
|------|---------|-------|
| `md_dependency_graph.py` | Cross-reference graph between .md files | `python _ai_evolution/scripts/md_dependency_graph.py [--format mermaid\|json\|csv]` |
| `verify_structure.py` | Validate broken markdown links | `python _ai_evolution/scripts/verify_structure.py` |

### AI Code Comprehension

| Tool | Purpose | Access |
|------|---------|--------|
| **DeepWiki** | AI-powered wiki + Q&A for any GitHub repo | `deepwiki.com` (URL 替换 github→deepwiki) |

> **DeepWiki** 来源: Karpathy 推荐 (2026-02)。支持 MCP 接入。核心用途: 让 AI agent 理解整个代码库后提取特定功能（"Bacterial Code" 模式）。当前评估: 教材项目不急需，编程项目可用。

### Evaluated: Documentation Coverage

| Tool | Verdict | Notes |
|------|---------|-------|
| **docstr-coverage** ✅ | **Recommended** | Installed. Current project: 76.9% coverage |
| **interrogate** ⚠️ | Skipped | Similar to docstr-coverage but less maintained |

Usage:
```bash
# Full path required (not on PATH)
C:\Users\10653\AppData\Local\Python\pythoncore-3.14-64\Scripts\docstr-coverage.exe agent_script/
```

### Evaluated: Architecture Diagram Generators

| Tool | Verdict | Notes |
|------|---------|-------|
| **diagrams** (Python) ✅ | **Best option** | "Diagrams as Code" — define architecture in Python, renders via Graphviz |
| **code2flow** ⚠️ | Experimental | Call graph from Python source; limited for dynamic languages |
| **pyan3** ❌ | Unmaintained | Offline call graph generator; maintainer stepped down 2023 |

Install when needed:
```bash
python -m pip install diagrams  # Also needs Graphviz installed
```
