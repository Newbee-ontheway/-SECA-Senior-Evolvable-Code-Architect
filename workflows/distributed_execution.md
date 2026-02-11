---
description: How to execute large multi-file tasks in phases to avoid context overflow
---

# Distributed Execution Protocol (分步执行协议)

> **这是正本。** `.agent/workflows/` 中有一份精简副本供系统命令调用。

## When to Use

- Task involves modifying 4+ files
- Task requires multi-step verification
- Expected to consume significant context (large files, complex diffs)

## Protocol

### Phase 0: Plan

1. Create `implementation_plan.md` with clear phases
2. Each phase should modify ≤3 files
3. Notify user for approval before execution

### Phase 1-N: Execute

1. Read `_ai_evolution/last_session.md` to restore context
2. Execute ONE phase only (≤3 file modifications)
3. At end of phase:
   - Update `_ai_evolution/last_session.md` with progress
   - Update task checklist
   - Summarize changes to user (what changed, why)
4. If more phases remain → user says "Continue" → next phase

### Final Phase: Verify + Report

1. Run any verification scripts
2. Create session note in `_ai_evolution/session_notes/`
3. Update `last_session.md` with final state

## Key Rules

- **≤3 files per phase** (prevents lint/context explosion)
- **Summarize changes** after each phase (user requirement)
- **Use `write_to_file` for full rewrites**, `multi_replace` for patches
- **Ignore cosmetic lint** during functional edits (`.markdownlint.json` handles suppression)
- **Session notes** folder stores per-session experience notes for user reference

## File Locations

| Item | Location | Note |
|------|----------|------|
| 正本 (canonical) | `_ai_evolution/workflows/distributed_execution.md` | 跟着 _ai_evolution 走 |
| 系统副本 | `.agent/workflows/distributed_execution.md` | Antigravity 系统需要，不能移 |
| Session notes | `_ai_evolution/session_notes/` | 经验笔记 |
| Task state | `_ai_evolution/last_session.md` | 跨会话状态 |
| Role rules | `_ai_evolution/role-SECA.md` | AI 行为规则 |
