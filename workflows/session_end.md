---
description: Session cleanup — update last_session, check temp files, remind git sync
---

# Session End Workflow (会话结束)

> **这是正本。** `.agent/workflows/` 中有一份精简副本供系统命令调用。

## When to Use

- User signals session end ("今天结束了", "暂停一下", "先这样")
- Context pressure warning triggered (§6)
- Any natural conversation endpoint with meaningful work done

## Steps

### Step 1: Terminate Background Processes
// turbo
Check for and kill any running background commands (dev servers, watchers):
```bash
# Check for running background command IDs — terminate if any
```

### Step 2: Check for Temp Files
// turbo
Scan for files created outside `_ai_evolution/` during this session:
```bash
# If any found: list them, ask user whether to delete or keep
```

### Step 3: Update `last_session.md`
Write/overwrite with:
```markdown
# Last Session State

**Date**: YYYY-MM-DD HH:MM
**Session Note**: [link if created]
**Summary**: [link if created]

## Completed This Session
[List of what was done, grouped by topic]

## Current INDEX Stats
[Updated counts for principles, rules, sparks]

## Pending
[Remaining tasks]

## Key Decisions Made
[Important choices that affect future sessions]
```

### Step 4: Remind Git Sync
- Say: "本次会话有 `_ai_evolution/` 变更。需要 `/git_sync` 吗?"
- Do NOT auto-execute — user must explicitly request

## Key Rules
- **DO NOT auto-run** `/git_sync` — only remind
- **Keep `last_session.md` concise** — future sessions will read it at startup
- **Omit step 2** if no external files were created
