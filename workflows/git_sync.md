---
description: Safe Git sync workflow for _ai_evolution — fetch, commit, push
---

# Git Sync Workflow

Safe four-step workflow for syncing `_ai_evolution/` to GitHub.
Execute at the end of every session after updating index files.

## Prerequisites
- Git repo initialized in `_ai_evolution/`
- Remote `origin` configured (SSH)
- SSH key added to GitHub

## Steps

// turbo
1. Fetch remote to check for upstream changes (zero risk, read-only):
```bash
git -C <project_root>/_ai_evolution fetch
```

// turbo
2. Check if remote has new commits:
```bash
git -C <project_root>/_ai_evolution log HEAD..origin/main --oneline
```
- If **empty output**: no upstream changes, proceed to Step 4
- If **has output**: upstream has new commits, proceed to Step 3

3. Pull and merge upstream changes (only if Step 2 found new commits):
```bash
git -C <project_root>/_ai_evolution pull
```
- If merge conflict occurs: notify user, do NOT auto-resolve
- If clean merge: proceed to Step 4

// turbo
4. Stage all changes:
```bash
git -C <project_root>/_ai_evolution add .
```

// turbo
5. Verify what will be committed:
```bash
git -C <project_root>/_ai_evolution status --short
```
- Confirm `last_session.md` is NOT in the list (excluded by .gitignore)
- If nothing to commit, stop here

6. Commit with descriptive message:
```bash
git -C <project_root>/_ai_evolution commit -m "<session_date>: <brief summary of changes>"
```
- Message format: `2026-02-11: added git workflow, updated skills`

7. Push to remote:
```bash
git -C <project_root>/_ai_evolution push
```

## Error Handling
- **Auth failure**: Check SSH key with `ssh -T git@github.com`
- **Merge conflict**: Show conflicting files to user, let user decide
- **Push rejected**: Run `git pull --rebase` then push again
