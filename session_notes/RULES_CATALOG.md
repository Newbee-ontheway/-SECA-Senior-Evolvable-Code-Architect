# 规则总目录 (RULES CATALOG)

> 38 条规则按类别组织。详细内容点击来源链接。
> 原则定义见 [INDEX.md](./INDEX.md)。

---

## 🏗️ Architecture 架构

| # | 名称 | 原则 | 一句话 | 来源 |
|---|------|------|--------|------|
| 1 | 关注点分离 | ARCH-01 | 操作手册和参考资料必须分开存放 | [2026-02-10-pm](./projects/001-textbook/2026-02-10-pm.md) |
| 3 | 开闭原则 | ARCH-03 | 系统必须预留多条路径，不为一种输入硬编码 | [同上](./projects/001-textbook/2026-02-10-pm.md) |
| 4 | 单一真相源 | ARCH-02 | 每份文件/数据只允许存在于一个位置 | [同上](./projects/001-textbook/2026-02-10-pm.md) |
| 6 | 内部一致性 | ARCH-03 | 系统规则不能自相矛盾 | [2026-02-11-late](./projects/001-textbook/2026-02-11-late.md) |
| 7 | 可移植性 | ARCH-04 | 你的东西必须能打包搬走，不依赖外部位置 | [同上](./projects/001-textbook/2026-02-11-late.md) |
| 11 | 分布式索引 | ARCH-05 | 不是每个文件夹都需要目录，按需建索引 | [2026-02-11-late-2](./projects/001-textbook/2026-02-11-late-2.md) |
| 20 | Failure Mode Multiplication | ARCH-06 | 多 Agent 概率相乘，环节越多越不可靠 | [2026-02-11-late-4](./projects/001-textbook/2026-02-11-late-4.md) |
| 24 | Code is Truth | ARCH-02 延伸 | 代码是真相源，文档会过时 | [2026-02-12-pm-1](./projects/001-textbook/2026-02-12-pm-1.md) |

---

## 🎨 Design 设计

| # | 名称 | 原则 | 一句话 | 来源 |
|---|------|------|--------|------|
| 2 | 数据链路完整 | DESIGN-02 | 不要设计依赖于你没有的数据的功能 | [2026-02-10-pm](./projects/001-textbook/2026-02-10-pm.md) |
| 23 | Bacterial Code | DESIGN-03 | 自包含、无状态、独立存活的代码设计 | [2026-02-12-pm-1](./projects/001-textbook/2026-02-12-pm-1.md) |

---

## 🔧 Practice 实践

| # | 名称 | 原则 | 一句话 | 来源 |
|---|------|------|--------|------|
| 5 | 技术债优先级 | PRACTICE-01 | 每次操作都触发的问题 > 功能开发 | [2026-02-10-pm](./projects/001-textbook/2026-02-10-pm.md) |
| 8 | 依赖重量 | PRACTICE-02 | 安装依赖前检查兼容性、体积、替代方案 | [2026-02-11-late](./projects/001-textbook/2026-02-11-late.md) |
| 9 | 推理链记录 | PRACTICE-03 | 每个有选项的决策都要留下"为什么"的记录 | [2026-02-11-late-2](./projects/001-textbook/2026-02-11-late-2.md) |
| 19 | 四层防线 | PRACTICE-04 | 缩小射程→结构化→事后验证→人类兜底 | [2026-02-11-late-4](./projects/001-textbook/2026-02-11-late-4.md) |
| 21 | 确定性优先 | PRACTICE-07 | 脚本 > 工具 > MCP > Sub-agent > 多 Agent | [同上](./projects/001-textbook/2026-02-11-late-4.md) |
| 27 | 验证层悖论 | PRACTICE-04 延伸 | 验证层必须是确定性的，不能是另一个 AI | [2026-02-12-pm-3](./projects/001-textbook/2026-02-12-pm-3.md) |
| 28 | 冗余 vs 分工 | PRACTICE-04 延伸 | 软件用分工+信息交流，不用航天级冗余 | [同上](./projects/001-textbook/2026-02-12-pm-3.md) |
| 35 | FOMO Treadmill | PRACTICE-02 延伸 | 投资不会 churn 的基础层，不追 trending 工具 | [2026-02-13-am-1](./projects/001-textbook/2026-02-13-am-1.md) |

---

## 🤖 AI 协作

| # | 名称 | 原则 | 一句话 | 来源 |
|---|------|------|--------|------|
| 10 | 上下文窗口管理 | AI-01 | AI 的"书桌"有限，5+文件就快满了 | [2026-02-11-late-2](./projects/001-textbook/2026-02-11-late-2.md) |
| 12 | AI 性格偏差 | AI-04 | 不同 AI 有不同偏差（保守/胡说/吹捧），识别并对冲 | [2026-02-11-late-3](./projects/001-textbook/2026-02-11-late-3.md) |
| 13 | 注意力崩溃 | AI-01 延伸 | 上下文边缘时 AI 不是均匀遗忘，而是注意力乱飘 | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 14 | 测试绕过 | AI-03 | AI 可能偷偷修改测试来通过，而不是修 Bug | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 15 | Memory 200行真相 | AI-02 | Memory 质量 > 数量。精准索引 > 堆砌笔记 | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 16 | 硬约束打断计划 | AI-05 | 触发型规则可能中断 AI 的多任务执行 | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 17 | 知识保质期 | AI-06 | AI 知识有截止日期，版本敏感决策必须验证 | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 18 | 400行法则 | AI-01 延伸 | AI 有效注意力上限 ~400 行，超过后失去大局观 | [同上](./projects/001-textbook/2026-02-11-late-3.md) |
| 22 | Token 经济学 | AI-07 | Token = 钱 + 注意力，减少轮次比缩短每轮更有效 | [2026-02-11-late-4](./projects/001-textbook/2026-02-11-late-4.md) |
| 26 | 同源盲区 | AI-03 延伸 | AI 无法有效 Review 自己生成的代码 | [2026-02-12-pm-3](./projects/001-textbook/2026-02-12-pm-3.md) |
| 29 | Manager-Worker Review | AI-08 | 异构模型并联 + 强模型整合 = 有效 Review 架构 | [同上](./projects/001-textbook/2026-02-12-pm-3.md) |
| 30 | 组合创新器 | AI-03 延伸 | AI 能组合创新，不能跳出训练分布做根本突破 | [2026-02-12-pm-4](./projects/001-textbook/2026-02-12-pm-4.md) |
| 31 | 世界模型进展 | — | 多模态≠世界模型，但领域世界模型已实质进展 | [同上](./projects/001-textbook/2026-02-12-pm-4.md) |
| 32 | Production Cost Paradox | AI-09 | AI 提速但增加协调/审阅/决策成本，总负荷更高 | [2026-02-13-am-1](./projects/001-textbook/2026-02-13-am-1.md) |
| 33 | Review Fatigue | AI-03 延伸 | 审阅 AI 代码比自己写更耗认知，创造 > 审阅 | [同上](./projects/001-textbook/2026-02-13-am-1.md) |
| 34 | Nondeterminism Tax | PRACTICE-07 延伸 | AI 概率输出 vs 人脑确定性预期，持续低级焦虑 | [同上](./projects/001-textbook/2026-02-13-am-1.md) |
| 36 | Prompt Spiral | AI-07 延伸 | 三次未达 70% 就手写，不要无限 re-prompt | [同上](./projects/001-textbook/2026-02-13-am-1.md) |
| 37 | Thinking Atrophy | AI-10 | 外包思考会萎缩推理能力，需保持无 AI 训练时间 | [同上](./projects/001-textbook/2026-02-13-am-1.md) |
| 38 | Cognitive Governor | AI-09 延伸 | AI 移除速度限制，需人工加回调速器防 burnout | [同上](./projects/001-textbook/2026-02-13-am-1.md) |

---

## 📚 Learning 学习

| # | 名称 | 原则 | 一句话 | 来源 |
|---|------|------|--------|------|
| 25 | SOAR 自课程 | DESIGN-04 | 学不会可能是教法问题，"刚好够难"的练习最有效 | [2026-02-12-pm-2](./projects/001-textbook/2026-02-12-pm-2.md) |

---

## 统计

| 类别 | 规则数 |
|------|--------|
| Architecture | 8 |
| Design | 2 |
| Practice | 8 |
| AI 协作 | 18 |
| Learning | 1 |
| **不含重复引用** | **37** |
| **含 Rule 35 (跨 Practice+AI)** | **38** |
