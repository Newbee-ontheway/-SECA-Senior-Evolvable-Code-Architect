---
description: Before building any tool/script, search for existing solutions — reuse > adapt > build
---

# Search Before Build Workflow (造轮子前先找轮子)

> **Canonical location**: `_ai_evolution/workflows/search_before_build.md`
> Portable skill. Copy `_ai_evolution/` to any project to reuse.

## When to Use

Trigger when **any** of these are true:
- About to write a new script or tool
- About to create a new workflow from scratch
- About to install a new library or dependency
- User asks "有没有现成的 X？"

**DO NOT SKIP THIS WORKFLOW.** The urge to build immediately is your known bias
(see `agent_profile.md` → Eager Builder Syndrome).

## Steps

### Step 1: Define What You Need (一句话定义)
// turbo

Write a **one-line capability statement**:

```
I need: [能力描述], input: [输入], output: [输出]
```

Example:
```
I need: batch web search with compact output, input: list of queries, output: structured text ~50 tokens/result
```

**Why**: Prevents scope creep. If you can't state it in one line, you don't understand the need yet — ask the user.

### Step 2: Search Local (查本地)
// turbo

Check what already exists in this project:

```bash
# Search existing scripts
ls _ai_evolution/scripts/

# Search skills catalog
grep -i "[keyword]" _ai_evolution/skills.md

# Search workflows
ls _ai_evolution/workflows/
```

**Decision gate**:
- ✅ Found exact match → **use it**. Done.
- 🔧 Found 80%+ match → **adapt it** (modify existing, don't create new). Done.
- ❌ Nothing useful → proceed to Step 3.

### Step 3: Search External (查外部)
// turbo

Three-layer search, stop as soon as you find something good enough:

```
Layer 1: GitHub (highest signal)
  search_web --site github.com "[capability] [language]"

Layer 2: Package registries
  search_web --site pypi.org OR npmjs.com "[capability]"

Layer 3: General web (lowest signal, most noise)
  search_web "[capability] best tool 2025"
```

For each candidate, evaluate:
- **Fit**: Does it solve ≥80% of the need?
- **Weight**: Dependencies, install size, maintenance burden
- **Freshness**: Last commit < 1 year? Active maintainer?
- **License**: Compatible? (MIT/Apache = safe)

**Decision gate**:
- ✅ Found good external tool → **install or adapt**. Record in `skills.md` Tool Catalog.
- 🔧 Found partial fit → **extract the relevant pattern**, build your own informed by it.
- ❌ Nothing suitable → proceed to Step 4.

### Step 4: Build (造轮子)

Now you have permission to build. But record why:

```markdown
## Build Justification
- Need: [one-line from Step 1]
- Local search: [what was found / nothing]
- External search: [what was found / why rejected]
- Decision: Build because [reason]
```

Save this justification as a comment in the script header or in `lessons_learned.md`.

### Step 5: Record (记录)

After building or adopting:
- New script → add to `project_context.md` tools table
- New external tool → add to `skills.md` Tool Catalog with verdict
- Rejected candidate worth remembering → add to Tool Catalog with ⚠️ or ❌

## Quick Reference (Decision Tree)

```
Need a capability
  │
  ├─ Step 2: Local search
  │   ├─ Exact match → USE IT ✅
  │   ├─ 80%+ match → ADAPT IT 🔧
  │   └─ Nothing → ↓
  │
  ├─ Step 3: External search (GitHub → PyPI/npm → General)
  │   ├─ Good fit + lightweight → INSTALL ✅
  │   ├─ Partial fit → EXTRACT PATTERN 🔧
  │   └─ Nothing suitable → ↓
  │
  └─ Step 4: BUILD 🔨 (with justification)
      │
      └─ Step 5: RECORD in project_context / skills.md
```

## Design Notes

> Informed by enterprise "Build vs Buy" decision frameworks (Forbes, ThoughtWorks, MadDevs)
> and AI agent tool selection patterns (OpenAI, IBM, Retool).
> Simplified from 9-step TCO analysis to 5-step lightweight workflow suitable for
> single-developer AI agent context. Key adaptation: replaced cost/vendor analysis
> with fit/weight/freshness evaluation relevant to open-source tooling.

## Portability
To migrate: copy `_ai_evolution/` folder. The workflow references only built-in tools.
