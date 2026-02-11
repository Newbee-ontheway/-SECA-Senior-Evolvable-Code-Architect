# Lessons: Architecture (架构决策类经验)

Category for lessons about system design, skill management, and namespace hygiene.

---

## Skills 文件分散问题

- **Date**: 2026-02-10
- **Cause**: skill 文件分散在多处，导致引用混乱
- **Evidence**: skills 出现在 `agent_rules/skills/`, `agent_memory/`, `.agent/skills/` 等多个位置
- **Reasoning**: 「单一存储」原则 — 同类文件放同一目录。分散导致索引失效、引用断裂
- **Fix**: 统一迁移到 `_ai_evolution/skills/`
- **Key insight**: Skills 存放位置因项目而异，不要假设固定路径。正确做法是查 Golden Rulebook

---

## 安装外部工具干扰其他 Agent

- **Date**: 2026-02-10
- **Cause**: `npx skills add` 默认安装到 `.agents/` 和 `.agent/`，可能干扰其他 agent
- **Evidence**: .agent/ 和 .agents/ 是通用 agent 目录，其他 agent 可能也在用
- **Reasoning**:
  1. 安装创建的目录 ≠ 我的目录 → 不能随便删
  2. 判断法则：安装前是否已存在？→ 已存在就不能碰
- **Fix**: 复制到 `_ai_evolution/skills/`，只清理自己创建的
- **Prevention**: 我的东西必须隔离，不污染不破坏其他命名空间

---

## Skills 精简原则

- **Date**: 2026-02-10
- **Cause**: Skills 可能无限增长导致上下文污染
- **Evidence**: 安装一个 skill 后发现复杂度和维护成本远超预期
- **Reasoning**: 精简 > 数量。每个 skill 占上下文空间，unused skills 是纯负担
- **Fix**: 确立精简原则 + 手动审查机制
- **Absorbed into**: role-SECA.md SKILL MANAGEMENT section
