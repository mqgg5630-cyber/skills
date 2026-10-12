# Skills 图解教程总结

## 教程概述

本教程通过 5 张图表，帮助零基础的用户快速理解 Skills 仓库的核心概念和使用方法。

## 图表列表

### 1. 整体架构图 (01-overall-architecture.md)
**目的**：了解 Skills 的整体结构

**核心内容**：
- Skills 分为工程技能和生产力技能两大类
- 每个类别又分为用户调用技能和模型调用技能
- 核心概念包括问题追踪器、问题、分类角色和共享语言

**关键点**：
- 工程技能：专注于代码开发工作
- 生产力技能：通用工作流程工具
- 用户调用技能：只能由用户触发
- 模型调用技能：可由 AI 自动调用

### 2. 工作流程图 (02-workflow.md)
**目的**：掌握日常开发流程

**核心内容**：
- 安装和设置流程
- 新功能开发流程
- 测试驱动开发 (TDD) 流程
- 架构改进流程

**关键点**：
- 新功能开发：`/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` → `/code-review`
- TDD 流程：红灯 → 绿灯 → 重构
- 架构改进：`/improve-codebase-architecture` → `/grill-me` → `/implement`

### 3. 安装步骤图 (03-installation-steps.md)
**目的**：学习如何安装和设置

**核心内容**：
- 三种安装方法：Claude Code 插件、npx skills、手动安装
- 每种方法的优缺点
- 设置过程和验证安装

**关键点**：
- 推荐方法：Claude Code 插件（最简单）
- 灵活方法：npx skills（可选择性安装）
- 高级方法：手动安装（完全控制）

### 4. 功能对比图 (04-skills-comparison.md)
**目的**：了解各个技能的用途

**核心内容**：
- 工程技能和生产力技能的详细列表
- 每个技能的用途和使用场景
- 技能选择指南

**关键点**：
- 用户调用技能：ask-matt、grill-with-docs、triage、improve-codebase-architecture 等
- 模型调用技能：prototype、diagnosing-bugs、research、tdd 等
- 技能选择：根据任务类型和项目阶段选择合适的技能

### 5. 核心概念图 (05-core-concepts.md)
**目的**：理解关键概念和关系

**核心内容**：
- 问题追踪器、问题、分类角色、共享语言、决策工单
- 概念之间的关系
- 实际应用示例

**关键点**：
- 问题追踪器：GitHub Issues、Linear、本地文件
- 分类角色：needs-triage、ready-for-afk、in-progress、done
- 共享语言：项目术语表，帮助 AI 理解项目上下文

## 学习路径

### 初学者路径
1. **第 1 步**：阅读整体架构图，了解 Skills 的全貌
2. **第 2 步**：学习安装步骤图，完成安装和设置
3. **第 3 步**：查看核心概念图，理解关键概念
4. **第 4 步**：尝试工作流程图中的简单流程
5. **第 5 步**：研究功能对比图，了解所有技能

### 进阶学习
1. 实践复杂的技能组合
2. 根据项目需求自定义技能
3. 参与社区贡献

## 核心概念速览

### 问题追踪器 (Issue Tracker)
- **定义**：管理项目问题的工具
- **类型**：GitHub Issues、Linear、本地文件
- **用途**：存储和管理问题，跟踪工作进度

### 问题 (Issues)
- **定义**：被追踪的工作单元
- **类型**：Bug、Task、Spec、Slice
- **作用**：Skills 工作流的核心

### 分类角色 (Triage Roles)
- **定义**：问题的状态标签
- **示例**：needs-triage、ready-for-afk、in-progress、done
- **用途**：管理工作流程

### 共享语言 (Shared Language)
- **定义**：项目术语表
- **作用**：帮助 AI 理解项目上下文
- **好处**：减少沟通成本，提高代码质量

### 决策工单 (Decision Ticket)
- **定义**：需要做出决策的特殊问题
- **特点**：记录问题、选项、考虑因素和最终决策
- **用途**：大型项目的规划阶段

## 技能分类详解

### 工程技能 (Engineering Skills)

#### 用户调用技能
| 技能 | 用途 | 使用场景 |
|------|------|----------|
| ask-matt | 询问适合的技能 | 不确定使用哪个技能时 |
| grill-with-docs | 深入访谈 + 文档 | 开始新功能开发前 |
| triage | 问题分类 | 处理问题列表时 |
| improve-codebase-architecture | 架构改进 | 定期代码库维护 |
| setup-matt-pocock-skills | 初始设置 | 首次安装后 |
| to-spec | 创建规格说明 | 需求讨论完成后 |
| to-tickets | 分解为问题 | 规格创建后 |
| implement | 实现功能 | 开始编码时 |
| wayfinder | 规划大型任务 | 复杂项目规划 |

#### 模型调用技能
| 技能 | 用途 | 使用场景 |
|------|------|----------|
| prototype | 原型设计 | 验证设计想法 |
| diagnosing-bugs | 诊断 Bug | 遇到难以调试的问题 |
| research | 技术研究 | 需要深入调查时 |
| tdd | 测试驱动开发 | 编写新功能时 |
| domain-modeling | 领域建模 | 理解业务逻辑 |
| codebase-design | 代码库设计 | 设计模块接口 |
| code-review | 代码审查 | 完成功能后 |
| resolving-merge-conflicts | 解决合并冲突 | Git 合并冲突时 |
| wizard | 生成向导 | 需要用户手动操作时 |

### 生产力技能 (Productivity Skills)

#### 用户调用技能
| 技能 | 用途 | 使用场景 |
|------|------|----------|
| grill-me | 深入访谈 | 非代码相关的需求 |
| handoff | 交接文档 | 切换工作上下文时 |
| teach | 教学功能 | 学习新技能时 |
| to-questionnaire | 创建问卷 | 需要他人输入时 |
| wait-what | 澄清误解 | 沟通不畅时 |

#### 模型调用技能
| 技能 | 用途 | 使用场景 |
|------|------|----------|
| grilling | 访谈原语 | 其他技能的基础 |
| writing-for-agents | 为代理写作 | 创建文档时 |

## 典型工作流程示例

### 场景 1：开发用户登录功能

1. **需求收集**
   - 使用 `/grill-with-docs` 进行深入访谈
   - 创建共享语言文档

2. **创建规格说明**
   - 使用 `/to-spec` 将对话转化为规格说明
   - 明确功能需求和验收标准

3. **分解任务**
   - 使用 `/to-tickets` 将规格分解为问题
   - 在问题追踪器中创建 Issue

4. **实现功能**
   - 使用 `/implement` 进行开发
   - 使用 `/tdd` 进行测试驱动开发

5. **代码审查**
   - 使用 `/code-review` 进行审查
   - 确保代码符合共享语言规范

6. **完成工作**
   - 关闭问题
   - 更新文档

### 场景 2：架构改进

1. **扫描代码库**
   - 使用 `/improve-codebase-architecture`
   - 识别改进候选

2. **创建决策工单**
   - 记录需要做出的决策
   - 列出选项和考虑因素

3. **做出决策**
   - 使用 `/grill-me` 深入讨论
   - 记录最终决策

4. **实施改进**
   - 根据决策创建问题
   - 使用 `/implement` 实施改进

## 常见问题解答

### Q: 我需要安装所有技能吗？
A: 不需要。建议从核心技能开始：
- `setup-matt-pocock-skills`（必须）
- `grill-with-docs`（推荐）
- `tdd`（推荐）
- `code-review`（推荐）

### Q: 这些技能支持哪些 AI 代理？
A: 主要支持：
- Claude Code（官方插件）
- Codex
- 其他支持自定义技能的代理

### Q: 如何更新技能？
A:
- **Claude Code 插件**：自动更新
- **npx skills**：运行 `npx skills update`

### Q: 我可以修改这些技能吗？
A: 可以！使用 `npx skills` 安装的技能文件可以自由修改。

## 更多资源

- **官方仓库**：https://github.com/mattpocock/skills
- **官方网站**：https://skills.sh
- **文档**：https://skills.sh/mattpocock/skills

## 总结

Skills 仓库提供了一套完整的 AI 代理技能系统，帮助开发者提高工作效率和代码质量。通过本教程的 5 张图表，你可以：

1. **理解整体架构**：了解 Skills 的分类和核心概念
2. **掌握工作流程**：学会日常开发中的典型流程
3. **完成安装设置**：选择适合的安装方法并完成配置
4. **了解功能对比**：知道每个技能的用途和使用场景
5. **理解核心概念**：掌握问题追踪器、问题、分类角色等关键概念

开始你的 Skills 学习之旅吧！