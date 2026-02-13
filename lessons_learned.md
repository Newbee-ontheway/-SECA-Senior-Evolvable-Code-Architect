# Lessons Learned

This file is the **summary index** — load this every session.
Full evidence chains and reasoning are in `lessons_detail/` (load on demand).

**Last Updated**: 2026-02-13
**Cleanup**: Manual trigger (user says "清理lessons")

## Categories

| Category | File | Count | Core Insight |
|----------|------|-------|-------------|
| File Management | `lessons_detail/file-management.md` | 3 | All my files go in `_ai_evolution/`, no exceptions |
| Tool Usage | `lessons_detail/tool-usage.md` | 2 | Search before build, scope validation tools carefully |
| Architecture | `lessons_detail/architecture.md` | 3 | Single storage, namespace isolation, skills are NOT "more is better" |
| Behavioral | (inline) | 2 | Don't skip the "understand" phase; process serves output |

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

### Behavioral
9. **Workflow ceremony overhead** — IDE tooling (plan artifacts, task_boundary, step-by-step notifications) is optional scaffolding, NOT mandatory ceremony. Wrapping small tasks in full ceremony = token waste + user waiting. [ABSORBED: WORKFLOW MODE SELECTION]
10. **Eager builder syndrome** — Received vague request and jumped straight to building, simultaneously skipping SEARCH-BEFORE-BUILD. Both violations share the same root cause: rushing to produce output, skipping the "understand the problem" phase. Prevention: vague request → ask 3-5 clarifying questions → search existing tools → THEN decide build vs. reuse. [BURNED-IN: role-SECA.md §0]

## Evidence/Reasoning Chain Format

New lessons should use this format in detail files:

```markdown
## [Title]
- **Date**: YYYY-MM-DD
- **Cause**: What went wrong
- **Evidence**: What I saw (facts, data, observations) — tag each: [verified] / [supported] / [speculative]
- **Reasoning**: Step-by-step logic from evidence to conclusion
- **Fix**: What was done
- **Prevention**: Rule going forward
- **Absorbed into**: Which Iron Rule absorbed this lesson (if any)
```
