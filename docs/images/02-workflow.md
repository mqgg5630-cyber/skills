# Skills 工作流程图

```mermaid
flowchart TD
    Start([开始]) --> Install[安装 Skills]
    Install --> Setup[运行 /setup-matt-pocock-skills]
    Setup --> Config[配置问题追踪器<br/>和分类标签]
    Config --> Ready([准备就绪])
    
    Ready --> Decision{需要做什么?}
    
    Decision -->|新功能开发| Grill[使用 /grill-me<br/>或 /grill-with-docs]
    Decision -->|修复 Bug| TDD[使用 /tdd]
    Decision -->|代码审查| Review[使用 /code-review]
    Decision -->|架构改进| Architecture[使用 /improve-codebase-architecture]
    
    Grill --> Spec[创建规格说明<br/>/to-spec]
    Spec --> Tickets[分解为问题<br/>/to-tickets]
    Tickets --> Implement[实现功能<br/>/implement]
    Implement --> Review
    
    TDD --> Red[编写失败测试]
    Red --> Green[编写代码通过测试]
    Green --> Refactor[重构代码]
    Refactor --> Review
    
    Review --> Done([完成])
    
    Architecture --> Survey[扫描代码库]
    Survey --> Candidates[识别改进候选]
    Candidates --> Grill
    
    style Start fill:#e8f5e8
    style Ready fill:#e8f5e8
    style Done fill:#e8f5e8
    style Install fill:#e1f5fe
    style Setup fill:#e1f5fe
    style Config fill:#e1f5fe
    style Decision fill:#fff3e0
    style Grill fill:#f3e5f5
    style TDD fill:#f3e5f5
    style Review fill:#f3e5f5
    style Architecture fill:#f3e5f5
    style Spec fill:#fce4ec
    style Tickets fill:#fce4ec
    style Implement fill:#fce4ec
    style Red fill:#fce4ec
    style Green fill:#fce4ec
    style Refactor fill:#fce4ec
    style Survey fill:#fce4ec
    style Candidates fill:#fce4ec
```

## 工作流程说明

### 1. 安装和设置阶段
1. **安装 Skills**：通过 Claude Code 插件或 `npx skills` 命令
2. **运行设置命令**：`/setup-matt-pocock-skills`
3. **配置**：选择问题追踪器（GitHub Issues、Linear 或本地文件）和分类标签

### 2. 日常开发工作流

#### 新功能开发流程
1. **需求收集**：使用 `/grill-me` 或 `/grill-with-docs` 进行深入访谈
2. **创建规格**：使用 `/to-spec` 将对话转化为规格说明
3. **分解任务**：使用 `/to-tickets` 将规格分解为可管理的问题
4. **实现功能**：使用 `/implement` 进行开发
5. **代码审查**：使用 `/code-review` 进行审查

#### 测试驱动开发 (TDD) 流程
1. **红灯**：编写一个失败的测试
2. **绿灯**：编写代码使测试通过
3. **重构**：优化代码结构

#### 架构改进流程
1. **扫描**：使用 `/improve-codebase-architecture` 扫描代码库
2. **识别**：找到改进候选
3. **访谈**：使用 `/grill-me` 深入讨论改进方案

### 3. 核心优势
- **小步前进**：每个步骤都有明确的反馈
- **持续反馈**：通过测试和审查获得即时反馈
- **文档化**：自动记录决策和规格说明