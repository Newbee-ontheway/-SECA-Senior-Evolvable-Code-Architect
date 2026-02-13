# Research: BM25 本地搜索方案

**Date**: 2026-02-13
**Question**: 用什么方案实现 `_ai_evolution/` 本地 markdown 文件的 BM25 搜索？

## 研究结论

**推荐方案**: `rank-bm25`（最简单） 或 `BM25S`（更快，支持索引持久化）

**架构**: AI 意图澄清（语义→关键词）+ BM25 关键词搜索 = 轻量混合方案

## 候选方案对比

| 工具 | 依赖 | 代码量 | 索引持久化 | 适合规模 | 判断 |
|------|------|--------|-----------|---------|------|
| **rank-bm25** | numpy | ~10 行 | ❌ 每次内存重建 | <500 文件 | ✅ 最简单，够用 |
| **BM25S** | scipy, numpy | ~15 行 | ✅ save/load | <100万 | ✅ 推荐，有索引缓存 |
| **Whoosh** | 纯 Python | ~30 行 | ✅ 文件索引 | <几千 | 🔧 功能全但偏重 |
| **dotMD** | 语义模型+BM25+KG | 独立工具 | ✅ | 任意 | ❌ 太重，含向量检索 |
| **tantivy-py** | Rust 编译器 | ~20 行 | ✅ | 百万级 | ❌ 环境依赖太重 |

## rank-bm25 最小示例

```python
from rank_bm25 import BM25Okapi
import os, re

def load_markdown_files(directory):
    docs, paths = [], []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fp:
                    docs.append(fp.read())
                paths.append(path)
    return docs, paths

def tokenize(text):
    """简单分词：英文按空格，中文按字"""
    text = text.lower()
    text = re.sub(r'[#*\-_`\[\](){}|>]', ' ', text)  # 去 markdown 标记
    tokens = text.split()
    return tokens

# 构建索引
docs, paths = load_markdown_files('_ai_evolution/')
tokenized = [tokenize(doc) for doc in docs]
bm25 = BM25Okapi(tokenized)

# 搜索
query = "session end workflow cleanup"
query_tokens = tokenize(query)
scores = bm25.get_scores(query_tokens)

# 取 top 5
top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
for i in top_indices:
    if scores[i] > 0:
        print(f"  {scores[i]:.2f}  {paths[i]}")
```

## BM25S 版本（支持索引持久化）

```python
import bm25s

# 构建索引（首次）
corpus = [open(p, encoding='utf-8').read() for p in paths]
corpus_tokens = bm25s.tokenize(corpus, stopwords="en")
retriever = bm25s.BM25()
retriever.index(corpus_tokens)
retriever.save("_ai_evolution/.bm25_index", corpus=corpus)

# 加载索引（后续）
retriever = bm25s.BM25.load("_ai_evolution/.bm25_index", load_corpus=True)

# 搜索
query_tokens = bm25s.tokenize("session end workflow", stopwords="en")
results, scores = retriever.retrieve(query_tokens, k=5)
```

## 你的架构 vs 向量检索

```
你选择的方案（BM25 + AI 意图澄清）:
  用户: "我之前写过关于怎么结束会话的"
  AI:   → 关键词: "session", "end", "cleanup", "会话", "结束"
  BM25: → workflows/session_end.md (score: 12.4)
         → last_session.md (score: 5.1)

向量检索方案（需要 100MB 模型）:
  用户: "我之前写过关于怎么结束会话的"
  模型: → 向量 [0.23, -0.11, 0.87, ...]
  FAISS: → workflows/session_end.md (cosine: 0.91)
```

**结论**: 在文件量 <100 的情况下，BM25 + AI 意图澄清
的效果不会比向量检索差多少，但零额外依赖、零额外存储。
等文件量超过 200+ 且频繁出现"找不到"的痛点时，再考虑向量检索。

## 下一步

如果决定实施：
1. `pip install rank-bm25`（或 `bm25s`）
2. 写一个 `_ai_evolution/scripts/local_search.py`
3. 集成到 Skill #0 的 Local Recall 分支
4. 注册到 `project_context.md` tools 表

## Sources

- [BM25S GitHub](https://github.com/xhluca/bm25s) — 500x faster than rank-bm25, scipy-based
- [rank-bm25 PyPI](https://pypi.org/project/rank-bm25/) — simplest BM25, 2-line search engine
- [Whoosh ReadTheDocs](https://whoosh.readthedocs.io/) — pure Python full-text search
- [dotMD Reddit](https://reddit.com/r/LocalLLaMA) — hybrid search for markdown (BM25 + vectors + KG)
- Forbes, ThoughtWorks, MadDevs — Build vs Buy decision frameworks
