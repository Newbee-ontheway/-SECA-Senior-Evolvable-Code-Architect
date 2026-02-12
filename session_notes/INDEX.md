# 软件工程原则索引

> 本文件是所有 session notes 的**知识图谱**（紧凑版）。
> 每条原则的详细定义在 `layers/` 目录中，按需加载。
> 项目专属笔记按目录归类在 `projects/` 下。

---

## 项目目录

| 编号 | 代号 | 项目全名 | 领域 | 状态 |
|------|------|---------|------|------|
| 001 | textbook | V3.5 高中英语教材生成系统 | 教育/排版 | 活跃 |

---

## 原则总览

> 25 条原则，5 个层级。ID 即指针 — 详情请查阅对应的 layer 文件。

### Layer 1: 哲学层 — [详情](./layers/layer-1-2-philosophy-architecture.md#layer-1-哲学层)

| 原则 | 一句话 |
|------|--------|
| KISS | 能简单就不复杂。两条原则冲突时，选更简单的。 |
| YAGNI | 不为"将来可能需要"写代码。只建造当前需要的。 |
| Errors are Data | 错误是数据不是敌人。记录 → 分析 → 提炼规则 → 系统性避免。 |

---

### Layer 2: 架构层 — [详情](./layers/layer-1-2-philosophy-architecture.md#layer-2-架构层)

| ID | 原则 | 一句话 |
|----|------|--------|
| ARCH-01 | Separation of Concerns | 每个模块只负责一件事，不混职责 |
| ARCH-02 | SSOT (Single Source of Truth) | 每条信息只有一个权威版本 |
| ARCH-03 | Internal Consistency | 新规则写入前检查是否与已有规则冲突 |
| ARCH-04 | Portability | 复制文件夹到新环境，功能要能正常工作 |
| ARCH-05 | Distributed State Sync | 多副本用 Git 合并知识（Append/LWW/Manual） |
| ARCH-06 | Failure Mode Multiplication | 串联 N 个不可靠环节，总可靠性指数下降 |

---

### Layer 3: 设计层 — [详情](./layers/layer-3-4-design-practice.md#layer-3-设计层)

| ID | 原则 | 一句话 |
|----|------|--------|
| DESIGN-01 | Open-Closed (OCP) | 加功能靠扩展，不靠改已有代码 |
| DESIGN-02 | Data Integrity | 没有数据支撑的功能不应该存在 |
| — | SOLID 族谱 | S/O/L/I/D 五原则参考表（O 已遇到） |

---

### Layer 4: 实践层 — [详情](./layers/layer-3-4-design-practice.md#layer-4-实践层)

| ID | 原则 | 一句话 |
|----|------|--------|
| PRACTICE-01 | Tech Debt Prioritization | 影响效率的问题优先于新功能 |
| PRACTICE-02 | Dependency Weight | 装依赖前查兼容性、体积、替代方案 |
| PRACTICE-03 | Traceability | 决策要能回答"为什么"，标注证据强度 |
| PRACTICE-04 | Quality Gate | 四层防线：缩小射程→结构约束→事后验证→人类兜底 |
| PRACTICE-05 | Quantifiable Thresholds | 质量检查必须有具体数字 |
| PRACTICE-07 | Deterministic-First | 脚本 > 工具 > MCP > Sub-agent > 多Agent |

---

### Layer AI: AI 协作层 — [详情](./layers/layer-ai.md)

| ID | 原则 | 一句话 |
|----|------|--------|
| AI-01 | Context Window | 上下文 = 书桌，满了就忘旧的。≤400行/文件 |
| AI-02 | Selective Memory | 跨对话记忆全靠文件，分层索引 > 堆砌 |
| AI-03 | Generation Pitfalls | 四大通病：堆砌、冗余、作用域乱、测试绕过 |
| AI-04 | Personality Bias | Claude 保守、ChatGPT 胡说、Gemini 吹捧 |
| AI-05 | Hard Constraint Derailment | 硬约束越少越好，优先事后检查 |
| AI-06 | Knowledge Expiry | AI 知识有截止日期，版本敏感要搜索验证 |
| AI-07 | Token Economy | Token = 钱 + 注意力。减轮次比缩每轮有效 |

---

## 原则关系图

```
+-------------------------------------------------+
|               Layer 1: Philosophy               |
|  +------+  +-------+  +--------+               |
|  | KISS |  | YAGNI |  | Errors |               |
|  |      |  |       |  | = Data |               |
|  +--+---+  +---+---+  +--------+               |
|     |          |                                 |
+-----+----------+--------------------------------+
|     |    Layer 2: Architecture                   |
|  +--+---+  +------+  +----+  +----+  +----+----+
|  |  01  |  |  02  |  | 03 |  | 04 |  | 05 | 06|
|  |SepCon|  | SSOT |  |Con.|  |Port|  |Sync|Fail|
|  +--+---+  +--+---+  +----+  +----+  +----+----+
|     |         |                                  |
+-----+---------+---------------------------------+
|     |    Layer 3: Design                         |
|  +--+----+  +------+  +--------+               |
|  |DES-01 |  | DRY  |  |DES-02  |               |
|  |  OCP  |  |(SSOT)|  |DataInt.|               |
|  +-------+  +------+  +--------+               |
+--------------------------------------------------+
|          Layer 4: Practice                       |
|  +----+ +----+ +----+ +----+ +----+ +----+     |
|  | 01 | | 02 | | 03 | | 04 | | 05 | | 07 |     |
|  |Debt| |Dep.| |Trac| |QGat| |Thre| |Det.|     |
|  +----+ +----+ +----+ +----+ +----+ +----+     |
+--------------------------------------------------+
|          Layer AI: AI Collaboration              |
|  +----+ +----+ +----+ +----+ +----+ +----+ +--+ |
|  | 01 | | 02 | | 03 | | 04 | | 05 | | 06 | |07| |
|  |Ctx.| |Mem.| |Pit.| |Bias| |Hard| |Exp.| |Tk| |
|  +----+ +----+ +----+ +----+ +----+ +----+ +--+ |
+--------------------------------------------------+
```

---

## 使用规则

1. **查原则** → 看本文件的总览表，一句话定义够用就不读详情
2. **要详情** → 点层级链接跳到 `layers/` 文件
3. **新原则** → 先在本文件总览表加一行，再在对应 layer 文件写详情
4. **笔记引用** → 只写编号（如 `ARCH-01`），不重复定义
