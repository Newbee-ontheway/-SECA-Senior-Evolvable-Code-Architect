---
description: Deep research workflow — decompose, search, read, synthesize, save
---

# Deep Research Workflow

> **Canonical location**: `_ai_evolution/workflows/research.md`
> Portable skill. Copy `_ai_evolution/` to any project to reuse.

## When to Use
- User explicitly says "深入研究" / "research X" / "帮我搞清楚 X"
- Triggered from Skill #8 intent classification → "Deep Research" type
- NOT for quick questions — those use inline search (see skills.md Skill #8)

## Prerequisites
- `search_web` tool available
- `read_url_content` tool available
- `readings/` directory exists at project root

## Steps

### Step 1: Decompose the Question
Break the user's question into **3-5 sub-questions** that cover different angles:

```
User:   "Zig vs Rust for systems programming"
Sub-Qs:
  1. What are Zig's key design decisions vs Rust's?
  2. Real-world adoption: which companies/projects use each?
  3. Learning curve and developer experience comparison
  4. Performance benchmarks: where does each excel?
  5. Community and ecosystem maturity
```

Rules:
- Sub-questions should be **independently searchable**
- Cover: definition, comparison, tradeoffs, real-world evidence, expert opinion
- Show the decomposition to the user before proceeding (brief confirmation)

### Step 2: Parallel Search
// turbo
For each sub-question, run `search_web`:

```
search_web("Zig design decisions vs Rust ownership model")
search_web("Zig adoption companies projects 2025")
... (one per sub-question)
```

- Run searches in parallel where possible
- 5 results per query is sufficient

### Step 3: Read Top Sources
For each sub-question, pick the **2-3 most promising URLs** from search results.
Use `read_url_content` to fetch full text.

Selection criteria:
- Prefer primary sources (official docs, author blogs) over aggregators
- Prefer recent content (< 1 year old) unless topic is stable
- Skip: SEO spam, listicles, paywalled content
- If a URL fails, skip it — don't waste tokens retrying

### Step 4: Synthesize
Cross-reference findings across all sub-questions. Structure the output:

```markdown
# Research: [Topic]

## Summary (2-3 sentences)

## Key Findings

### [Sub-question 1]
[Findings with source attribution]

### [Sub-question 2]
...

## Comparison Table (if applicable)
| Dimension | Option A | Option B |
|---|---|---|

## Open Questions
[What remains unclear or debated]

## Sources
[Numbered list of URLs actually read]
```

Rules:
- **Always surface tradeoffs** — never conclude "X is better" without qualification
- **Flag disagreements** between sources explicitly
- **Bilingual**: Main content in English, add Chinese summary at top if user prefers

### Step 5: Save and Report
1. Save to `readings/YYYY-MM-DD-<topic-slug>.md`
2. Report to user: topic, # sources read, top 3 findings, open questions

## Portability
To migrate: copy `_ai_evolution/` folder. The workflow references only built-in tools.
