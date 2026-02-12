# Layer 1 & 2: 哲学层 + 架构层 — 详细定义

> 本文件是 [INDEX.md](./INDEX.md) 的展开。AI 按需读取，不在 startup 时加载。

---

## Layer 1: 哲学层

### KISS — Keep It Simple, Stupid

**含义**: 能简单就不要复杂。每多一层抽象、多一个配置、多一个文件，都是成本。

**判断标准**: 如果你无法在 30 秒内向别人解释某个设计，它可能太复杂了。

**关系**: 是所有其他原则的"仲裁者" —— 当两条原则冲突时，选更简单的方案。

---

### YAGNI — You Aren't Gonna Need It

**含义**: 不要为"将来可能需要"的功能写代码。只建造当前需要的东西。

**判断标准**: 如果功能需求来自"万一以后..."的句式 → 大概率不需要。

**与 KISS 的关系**: KISS 说"做简单"，YAGNI 说"少做"。两者共同防止过度工程。

---

### Errors are Data — 错误是数据

**含义**: Bug、失败、报错不是需要消灭的敌人，而是需要采集的数据。每一个错误都包含"哪里薄弱"的信息，记录和分析它们就是在给系统做体检。

**判断标准**: 出错后的第一反应应该是"记录"，不是"赶紧改掉忘了它"。

**机制**:

```
传统心态：Bug → 沮丧 → 修掉 → 忘记 → 下次再踩
数据心态：Bug → 记录 → 分析成因 → 提炼规则 → 系统性避免
```

**在我们系统中的体现**:
- `lessons_learned.md` + `lessons_detail/` = 错误数据库
- `INDEX.md` 的每条原则都是从真实错误中提炼出来的

**与其他原则的关系**: 是 `PRACTICE-03`（Traceability）的哲学基础。

**出现记录**: [2026-02-12 社区经验讨论](./projects/001-textbook/2026-02-11-late-4.md)

---

## Layer 2: 架构层

### ARCH-01: Separation of Concerns — 关注点分离

**含义**: 每个模块/目录/文件只负责一件事。不同职责的东西不混在一起。

**应用场景**: 目录结构设计、数据库设计、代码组织

**出现记录**: [2026-02-10-pm 规则1](./projects/001-textbook/2026-02-10-pm.md)

---

### ARCH-02: Single Source of Truth (SSOT) — 单一真相源

**含义**: 每条信息只有一个权威版本。其他地方需要时，链接到那个版本，不复制。

**与 DRY 的关系**: DRY（不重复自己）是 SSOT 在代码层面的具体表现。

```
SSOT (架构层)
 └── DRY (设计层) ← 代码不复制粘贴
 └── 规范化 (数据库层) ← 数据不冗余存储
```

**出现记录**: [2026-02-10-pm 规则4](./projects/001-textbook/2026-02-10-pm.md), [2026-02-11-late-2 规则11](./projects/001-textbook/2026-02-11-late-2.md)

---

### ARCH-03: Internal Consistency — 内部一致性

**含义**: 系统中的规则不能自相矛盾。每条新规则写入前，检查是否与已有规则冲突。

**与 SSOT 的关系**: SSOT 防止数据矛盾，Internal Consistency 防止逻辑矛盾。

**出现记录**: [2026-02-11-late 规则6](./projects/001-textbook/2026-02-11-late.md)

---

### ARCH-04: Portability — 可移植性

**含义**: 一个模块/工作空间的所有依赖必须能跟着它一起迁移。

**判断测试**: "如果只复制这一个文件夹到新环境，所有功能能正常工作吗？"

**出现记录**: [2026-02-11-late 规则7](./projects/001-textbook/2026-02-11-late.md)

---

### ARCH-05: Distributed State Synchronization — 分布式状态同步

**含义**: 当同一个系统的多个副本各自积累经验后，需要一种策略来合并它们的知识。

**三种合并策略**:

| 策略 | 适用场景 | 例子 |
|------|---------|------|
| Append-Only | 数据只增不改 | session_notes (按日期命名, 不冲突) |
| Last-Writer-Wins | 谁最后改谁赢 | last_session.md |
| Manual Merge | 冲突需要人判断 | role-SECA.md, INDEX.md |

**实现**: 用 Git 管理 `_ai_evolution/` 目录即可。

**出现记录**: [2026-02-11-late-2 规则11](./projects/001-textbook/2026-02-11-late-2.md)

---

### ARCH-06: Failure Mode Multiplication — 多 Agent 可靠性陷阱

**含义**: N 个串联的不可靠环节，系统可靠性 = P₁ × P₂ × ... × Pₙ。每加一个 Agent，总可靠性只会下降。

**结论**: 除非任务量大到单 Agent 处理不过来，否则单 Agent + 确定性工具是最佳选择。

**出现记录**: [2026-02-11-late-4 规则20](./projects/001-textbook/2026-02-11-late-4.md)
