# Skills 图解教程创建总结

## 创建内容

我已经为 Skills 仓库创建了一套完整的图解教程，包含以下内容：

### 1. 图表文件

#### Mermaid 图表（可编辑）
1. **整体架构图** (`01-overall-architecture.md`)
   - 展示 Skills 的整体结构
   - 包含工程技能和生产力技能的分类
   - 显示核心概念之间的关系

2. **工作流程图** (`02-workflow.md`)
   - 展示日常开发流程
   - 包含新功能开发、TDD、架构改进等流程
   - 显示技能之间的调用关系

3. **安装步骤图** (`03-installation-steps.md`)
   - 展示三种安装方法
   - 比较不同方法的优缺点
   - 显示设置过程

4. **功能对比图** (`04-skills-comparison.md`)
   - 对比工程技能和生产力技能
   - 列出所有用户调用和模型调用技能
   - 提供技能选择指南

5. **核心概念图** (`05-core-concepts.md`)
   - 展示核心概念及其关系
   - 包含问题追踪器、问题、分类角色等
   - 显示实际应用示例

#### 生成的图片
- `output/01-overall-architecture.png` (179KB)
- `output/02-workflow.png` (153KB)
- `output/03-installation-steps.png` (54KB)
- `output/04-skills-comparison.png` (97KB)
- `output/05-core-concepts.png` (76KB)

### 2. 文档文件

#### 教程文档
1. **README.md** - 教程说明文档
2. **SUMMARY.md** - 教程总结文档
3. **FINAL-TUTORIAL.md** - 完整教程文档
4. **QUICK-START.md** - 快速开始指南

#### 工具文件
1. **skills-tutorial.html** - 交互式教程网页
2. **view-tutorial.sh** - 查看教程脚本
3. **generate-images.sh** - 图片生成脚本
4. **generate-simple-images.py** - Python 图片生成脚本

### 3. 文件结构

```
/home/user/skills/docs/images/
├── 01-overall-architecture.md      # 整体架构图 Mermaid 代码
├── 01-overall-architecture.png     # 整体架构图图片
├── 02-workflow.md                  # 工作流程图 Mermaid 代码
├── 02-workflow.png                 # 工作流程图图片
├── 03-installation-steps.md        # 安装步骤图 Mermaid 代码
├── 03-installation-steps.png       # 安装步骤图图片
├── 04-skills-comparison.md         # 功能对比图 Mermaid 代码
├── 04-skills-comparison.png        # 功能对比图图片
├── 05-core-concepts.md             # 核心概念图 Mermaid 代码
├── 05-core-concepts.png            # 核心概念图图片
├── README.md                       # 教程说明文档
├── SUMMARY.md                      # 教程总结文档
├── FINAL-TUTORIAL.md               # 完整教程文档
├── QUICK-START.md                  # 快速开始指南
├── CREATION-SUMMARY.md             # 创建总结文档
├── skills-tutorial.html            # 交互式教程网页
├── view-tutorial.sh                # 查看教程脚本
├── generate-images.sh              # 图片生成脚本
├── generate-simple-images.py       # Python 图片生成脚本
└── output/                         # 图片输出目录
    ├── 01-overall-architecture.png
    ├── 02-workflow.png
    ├── 03-installation-steps.png
    ├── 04-skills-comparison.png
    └── 05-core-concepts.png
```

## 如何使用

### 方法 1：使用浏览器查看交互式教程（推荐）

```bash
# 打开 HTML 文件
open /home/user/skills/docs/images/skills-tutorial.html
```

**优点**：
- 交互式体验
- 图表自动渲染
- 响应式设计，支持移动设备

### 方法 2：查看 Markdown 文件

```bash
# 查看整体架构图
cat /home/user/skills/docs/images/01-overall-architecture.md

# 查看工作流程图
cat /home/user/skills/docs/images/02-workflow.md

# 查看安装步骤图
cat /home/user/skills/docs/images/03-installation-steps.md

# 查看功能对比图
cat /home/user/skills/docs/images/04-skills-comparison.md

# 查看核心概念图
cat /home/user/skills/docs/images/05-core-concepts.md
```

**优点**：
- 可以复制 Mermaid 代码
- 适合在 GitHub 等平台查看

### 方法 3：在线查看 Mermaid 图表

1. 访问 https://mermaid.live
2. 复制 `.md` 文件中的 Mermaid 代码
3. 粘贴到编辑器中查看图表

**优点**：
- 无需安装任何软件
- 实时编辑和预览

### 方法 4：查看生成的图片

```bash
# 查看图片文件
ls -la /home/user/skills/docs/images/output/
```

**优点**：
- 可以直接在图片查看器中打开
- 适合分享和嵌入文档

### 方法 5：使用脚本查看

```bash
# 运行查看脚本
/home/user/skills/docs/images/view-tutorial.sh
```

**优点**：
- 快速查看所有文件
- 提供学习建议

## 教程内容概述

### 1. 整体架构图
- Skills 分为工程技能和生产力技能两大类
- 每个类别又分为用户调用技能和模型调用技能
- 核心概念包括问题追踪器、问题、分类角色和共享语言

### 2. 工作流程图
- 安装和设置流程
- 新功能开发流程：`/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` → `/code-review`
- 测试驱动开发 (TDD) 流程：红灯 → 绿灯 → 重构
- 架构改进流程：`/improve-codebase-architecture` → `/grill-me` → `/implement`

### 3. 安装步骤图
- 三种安装方法：Claude Code 插件、npx skills、手动安装
- 推荐方法：Claude Code 插件（最简单）
- 设置过程：选择问题追踪器、配置分类标签、指定文档位置

### 4. 功能对比图
- 工程技能：ask-matt、grill-with-docs、triage、to-spec、implement、tdd、code-review 等
- 生产力技能：grill-me、handoff、teach、to-questionnaire、wait-what 等
- 技能选择指南：根据任务类型和项目阶段选择合适的技能

### 5. 核心概念图
- 问题追踪器：GitHub Issues、Linear、本地文件
- 问题：被追踪的工作单元
- 分类角色：needs-triage、ready-for-afk、in-progress、done
- 共享语言：项目术语表，帮助 AI 理解项目上下文
- 决策工单：需要做出决策的特殊问题

## 学习路径

### 初学者路径（第 1 周）
1. 阅读整体架构图，了解全貌
2. 学习安装步骤图，完成安装
3. 查看核心概念图，理解关键概念
4. 尝试 `/grill-me` 和 `/tdd`

### 进阶者路径（第 2 周）
1. 研究功能对比图，了解所有技能
2. 实践 `/grill-with-docs` 和 `/implement`
3. 尝试 `/code-review` 和 `/improve-codebase-architecture`

### 高级者路径（第 3 周）
1. 掌握复杂的技能组合
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

我已经为 Skills 仓库创建了一套完整的图解教程，包含：

1. **5 张 Mermaid 图表**：整体架构图、工作流程图、安装步骤图、功能对比图、核心概念图
2. **5 张生成的图片**：可以直接查看的 PNG 图片
3. **4 个文档文件**：README、SUMMARY、FINAL-TUTORIAL、QUICK-START
4. **1 个交互式网页**：skills-tutorial.html
5. **3 个工具脚本**：view-tutorial.sh、generate-images.sh、generate-simple-images.py

这套教程适合零基础的用户，通过图表和详细的文字说明，帮助快速理解 Skills 仓库的核心概念和使用方法。

开始你的 Skills 学习之旅吧！