# Lessons Learned (经验索引)

This file is the **summary index** — load this every session.
Full evidence chains and reasoning are in `lessons_detail/` (load on demand).

**Last Updated**: 2026-02-10
**Cleanup**: Manual trigger (user says "清理lessons")

## Categories

| Category | File | Count | Core Insight |
|----------|------|-------|-------------|
| File Management | `lessons_detail/file-management.md` | 3 | All my files go in `_ai_evolution/`, no exceptions |
| Tool Usage | `lessons_detail/tool-usage.md` | 2 | Search before build, scope validation tools carefully |
| Architecture | `lessons_detail/architecture.md` | 3 | Single storage, namespace isolation, skills are NOT "more is better" |

## Quick Reference (one-line summaries)

### File Management
1. **Path breakage** — Moving files breaks links. Run verify_structure.py after. [ABSORBED: INDEX MAINTENANCE]
2. **Wrong location** — My scripts go in `_ai_evolution/scripts/`, not project dirs. [ABSORBED: PORTABLE FILE OWNERSHIP]
3. **Bootstrap leak** — Never create files outside `_ai_evolution/`, even "pointers". [ABSORBED: PORTABLE FILE OWNERSHIP]

### Tool Usage
4. **False positives** — Validation tools must distinguish real links from code examples. [standalone]
5. **Search first** — Check skills.sh/GitHub before building tools. Even if they're too heavy, know what exists. [ABSORBED: SEARCH BEFORE BUILD]

### Architecture
6. **Skills scattered** — Same type of file in one place. Don't assume fixed skill paths across projects. [standalone]
7. **External install pollution** — npx installs to shared dirs. Copy what you need, don't delete others' dirs. [standalone]
8. **Skills bloat** — Fewer is better. Review manually. Priority: update > create > install. [ABSORBED: SKILL MANAGEMENT]
9. **Workflow ceremony overhead** — IDE 提供的流程工具（plan artifact, task_boundary, 逐步通知）是可选辅助，不是强制仪式。小任务套完整流程 = token 浪费 + 用户等待。[ABSORBED: WORKFLOW MODE SELECTION]

## Evidence/Reasoning Chain Format

New lessons should use this format in detail files:

```markdown
## [Title]
- **Date**: YYYY-MM-DD
- **Cause**: What went wrong
- **Evidence**: What I saw (facts, data, observations) — tag each: [已验证] / [有依据] / [推测]
- **Reasoning**: Step-by-step logic from evidence to conclusion
- **Fix**: What was done
- **Prevention**: Rule going forward
- **Absorbed into**: Which Iron Rule absorbed this lesson (if any)
```
