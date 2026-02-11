# Lessons: Tool Usage (工具使用类经验)

Category for lessons about building, choosing, and validating tools.

---

## 内联代码 vs 实际链接混淆

- **Date**: 2026-02-10
- **Cause**: 验证脚本误将文档中的路径示例当作实际链接检查
- **Evidence**: 脚本报了大量误报，都是代码块里的示例路径
- **Reasoning**: 工具应区分「可点击链接」和「说明性路径引用」→ 正则表达式需要排除代码块
- **Fix**: 简化正则，只检查 markdown 链接语法 `[text](path)`
- **Prevention**: 验证工具的范围必须明确 — 不是所有路径都需要验证

---

## 先搜后建原则

- **Date**: 2026-02-10
- **Cause**: 直接手写 `md_dependency_graph.py` 等，没有先搜索现有方案
- **Evidence**: 搜索 skills.sh 后发现 `remembering-conversations` (SQLite+Haiku) 和 `verification-before-completion`
- **Reasoning**:
  1. 搜到的方案太重(SQLite)或空壳(无SKILL.md) → 不适合直接用
  2. 但概念有价值 — 「验证模式」已融入操作习惯
  3. 结论：先搜后建不一定是为了直接用，而是为了**知道已有什么**
- **Fix**: 确立搜索流程
- **Absorbed into**: role-SECA.md Iron Rule: SEARCH BEFORE BUILD
