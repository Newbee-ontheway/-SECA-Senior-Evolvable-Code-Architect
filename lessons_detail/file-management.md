# Lessons: File Management (文件管理类经验)

Category for lessons about file placement, path handling, and ownership boundaries.

---

## 路径引用断裂问题

- **Date**: 2026-02-10
- **Cause**: 文档中的相对路径引用 (`./standard_*.md`) 指向错误位置，文件实际在 `../standards/` 目录
- **Evidence**: 运行 verify_structure.py 发现 36+ 处断裂引用
- **Reasoning**: 文件被移动后路径没同步更新 → 需要自动化检测而非人工检查
- **Fix**: 创建 verify_structure.py 脚本扫描所有 markdown 链接
- **Prevention**: 移动文件后必须运行验证脚本
- **Absorbed into**: role-SECA.md Iron Rule: INDEX MAINTENANCE

---

## 工具文件放错位置

- **Date**: 2026-02-10
- **Cause**: 创建的脚本放在 `agent_script/` (项目目录) 而非 `_ai_evolution/scripts/`
- **Evidence**: 文件不会跟着 `_ai_evolution/` 迁移到新项目
- **Reasoning**: 判断法则 —「这个文件会跟着 _ai_evolution/ 移到新项目吗？」→ 是 → 放 _ai_evolution/
- **Fix**: 迁移到 `_ai_evolution/scripts/`
- **Prevention**: 项目目录是施工场所，`_ai_evolution/` 才是我的家
- **Absorbed into**: role-SECA.md Iron Rule: PORTABLE FILE OWNERSHIP

---

## Bootstrap 文件外泄

- **Date**: 2026-02-10
- **Cause**: 在 `.agent/skills/seca-bootstrap/` 创建了 SKILL.md 想实现自动加载
- **Evidence**: 用户指出 — 当 `_ai_evolution/` 被移走后，SKILL.md 留在项目里会导致原项目 agent 幻觉
- **Reasoning**:
  1. 我看到 skills.sh 文档说 .agent/ 被扫描 → [有依据]
  2. 但没验证 Antigravity 是否遵循同样的机制 → 关键遗漏
  3. 更深层：即使能自动加载，留下的文件也会"污染"原项目 → 后果没想到
- **Fix**: 删除 `.agent/` 目录，改为手动加载
- **Prevention**: 创建文件前问「如果我走了，这个文件会不会害到别人？」
- **Absorbed into**: role-SECA.md Iron Rule: PORTABLE FILE OWNERSHIP (no files outside _ai_evolution/)
