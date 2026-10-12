# Skills 图解教程 - 零基础入门

欢迎来到 Skills 图解教程！本教程通过多张图表，帮助零基础的你快速理解 Skills 仓库的核心概念和使用方法。

## 教程目录

1. **[整体架构图](./01-overall-architecture.md)** - 了解 Skills 的整体结构
2. **[工作流程图](./02-workflow.md)** - 掌握日常开发流程
3. **[安装步骤图](./03-installation-steps.md)** - 学习如何安装和设置
4. **[功能对比图](./04-skills-comparison.md)** - 了解各个技能的用途
5. **[核心概念图](./05-core-concepts.md)** - 理解关键概念和关系

## 快速开始

### 1. 安装 Skills（30秒）

```bash
# 方法1: Claude Code 插件（推荐）
claude plugins install mattpocock-skills

# 方法2: npx skills
npx skills@latest add mattpocock/skills
```

### 2. 运行设置命令

```
/setup-matt-pocock-skills
```

### 3. 开始使用

```bash
# 询问适合的技能
/ask-matt

# 深入访谈新功能
/grill-me

# 测试驱动开发
/tdd
```

## 核心概念速览

### 问题追踪器 (Issue Tracker)
管理项目问题的工具，支持 GitHub Issues、Linear 或本地文件。

### 问题 (Issues)
被追踪的工作单元，可以是 Bug、Task、Spec 或 Slice。

### 分类角色 (Triage Roles)
问题的状态标签，如 `needs-triage`、`ready-for-afk`、`in-progress`、`done`。

### 共享语言 (Shared Language)
项目术语表，帮助 AI 理解项目上下文，减少沟通成本。

## 技能分类

### 工程技能 (Engineering Skills)
专注于代码开发工作，分为：
- **用户调用技能**：只能由用户触发（如 `/grill-with-docs`、`/implement`）
- **模型调用技能**：可由 AI 自动调用（如 `/tdd`、`/code-review`）

### 生产力技能 (Productivity Skills)
通用工作流程工具，分为：
- **用户调用技能**：如 `/grill-me`、`/handoff`
- **模型调用技能**：如 `/grilling`、`/writing-for-agents`

## 典型工作流程

### 新功能开发
1. `/grill-with-docs` - 深入访谈并创建文档
2. `/to-spec` - 将对话转化为规格说明
3. `/to-tickets` - 将规格分解为问题
4. `/implement` - 实现功能
5. `/code-review` - 代码审查

### Bug 修复
1. `/diagnosing-bugs` - 诊断复杂 Bug
2. `/tdd` - 测试驱动开发

### 架构改进
1. `/improve-codebase-architecture` - 扫描并改进架构
2. `/grill-me` - 深入讨论改进方案

## 学习建议

### 初学者路径
1. 先阅读 **[整体架构图](./01-overall-architecture.md)**，了解全貌
2. 学习 **[安装步骤图](./03-installation-steps.md)**，完成安装
3. 查看 **[核心概念图](./05-core-concepts.md)**，理解关键概念
4. 尝试 **[工作流程图](./02-workflow.md)** 中的简单流程

### 进阶学习
1. 研究 **[功能对比图](./04-skills-comparison.md)**，了解所有技能
2. 实践复杂的技能组合
3. 根据项目需求自定义技能

## 常见问题

### Q: 我需要安装所有技能吗？
A: 不需要。使用 `npx skills` 可以选择性安装。建议从核心技能开始：
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

## 贡献

欢迎贡献！请查看：
- 提交 Issue：报告问题或建议
- 提交 PR：改进技能或文档
- 分享经验：在社区中分享你的使用心得

---

**提示**：本教程基于 Skills 仓库的 README.md 和 CONTEXT.md 文件创建。如有疑问，建议直接阅读原始文档。