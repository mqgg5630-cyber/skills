# Skills 整体架构图

```mermaid
graph TB
    subgraph "用户层"
        User[用户/开发者]
    end
    
    subgraph "Skills 分类"
        direction TB
        Engineering[工程技能<br/>Engineering Skills]
        Productivity[生产力技能<br/>Productivity Skills]
    end
    
    subgraph "工程技能细分"
        direction LR
        UserInvoked1[用户调用技能]
        ModelInvoked1[模型调用技能]
    end
    
    subgraph "生产力技能细分"
        direction LR
        UserInvoked2[用户调用技能]
        ModelInvoked2[模型调用技能]
    end
    
    subgraph "核心概念"
        IssueTracker[问题追踪器<br/>Issue Tracker]
        Issues[问题<br/>Issues]
        TriageRoles[分类角色<br/>Triage Roles]
        SharedLanguage[共享语言<br/>Shared Language]
    end
    
    User --> Engineering
    User --> Productivity
    
    Engineering --> UserInvoked1
    Engineering --> ModelInvoked1
    Productivity --> UserInvoked2
    Productivity --> ModelInvoked2
    
    UserInvoked1 --> IssueTracker
    UserInvoked1 --> Issues
    UserInvoked1 --> TriageRoles
    UserInvoked1 --> SharedLanguage
    
    ModelInvoked1 --> IssueTracker
    ModelInvoked1 --> Issues
    ModelInvoked1 --> TriageRoles
    ModelInvoked1 --> SharedLanguage
    
    UserInvoked2 --> IssueTracker
    UserInvoked2 --> Issues
    UserInvoked2 --> TriageRoles
    UserInvoked2 --> SharedLanguage
    
    ModelInvoked2 --> IssueTracker
    ModelInvoked2 --> Issues
    ModelInvoked2 --> TriageRoles
    ModelInvoked2 --> SharedLanguage
    
    style User fill:#e1f5fe
    style Engineering fill:#f3e5f5
    style Productivity fill:#e8f5e8
    style UserInvoked1 fill:#fff3e0
    style ModelInvoked1 fill:#fce4ec
    style UserInvoked2 fill:#fff3e0
    style ModelInvoked2 fill:#fce4ec
    style IssueTracker fill:#f1f8e9
    style Issues fill:#f1f8e9
    style TriageRoles fill:#f1f8e9
    style SharedLanguage fill:#f1f8e9
```

## 图表说明

**整体架构**：Skills 仓库分为两大类技能：

1. **工程技能 (Engineering Skills)**：专注于代码开发工作
2. **生产力技能 (Productivity Skills)**：通用工作流程工具

每个技能类别又分为：
- **用户调用技能**：只能由用户通过命令触发
- **模型调用技能**：可以由用户或 AI 模型自动调用

**核心概念**：
- **问题追踪器 (Issue Tracker)**：管理项目问题的工具
- **问题 (Issues)**：被追踪的工作单元
- **分类角色 (Triage Roles)**：问题的状态标签
- **共享语言 (Shared Language)**：项目术语表，帮助 AI 理解项目上下文