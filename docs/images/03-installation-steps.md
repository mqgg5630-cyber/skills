# Skills 安装步骤图

```mermaid
flowchart LR
    subgraph "方法1: Claude Code 插件"
        direction TB
        A1[打开 Claude Code] --> A2[运行命令:<br/>claude plugins install<br/>mattpocock-skills]
        A2 --> A3[插件自动安装]
        A3 --> A4[运行 /setup-matt-pocock-skills]
        A4 --> A5[配置完成]
    end
    
    subgraph "方法2: npx skills"
        direction TB
        B1[打开终端] --> B2[运行命令:<br/>npx skills@latest add<br/>mattpocock/skills]
        B2 --> B3[选择要安装的技能]
        B3 --> B4[运行 /setup-matt-pocock-skills]
        B4 --> B5[配置完成]
    end
    
    subgraph "方法3: 手动安装"
        direction TB
        C1[克隆仓库:<br/>git clone<br/>mattpocock/skills]
        C1 --> C2[复制技能文件<br/>到项目目录]
        C2 --> C3[运行 /setup-matt-pocock-skills]
        C3 --> C4[配置完成]
    end
    
    style A1 fill:#e1f5fe
    style A2 fill:#e1f5fe
    style A3 fill:#e1f5fe
    style A4 fill:#e1f5fe
    style A5 fill:#e8f5e8
    
    style B1 fill:#f3e5f5
    style B2 fill:#f3e5f5
    style B3 fill:#f3e5f5
    style B4 fill:#f3e5f5
    style B5 fill:#e8f5e8
    
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
    style C4 fill:#e8f5e8
```

## 安装方法详解

### 方法 1: Claude Code 插件（推荐）

**优点**：
- 最简单快捷
- 自动更新
- 官方支持

**步骤**：
1. 打开 Claude Code
2. 运行安装命令：
   ```bash
   claude plugins install mattpocock-skills
   ```
3. 插件会自动安装所有技能
4. 运行设置命令：
   ```
   /setup-matt-pocock-skills
   ```

### 方法 2: npx skills（灵活）

**优点**：
- 可以选择性安装技能
- 适合想要自定义的用户
- 支持多种代理

**步骤**：
1. 打开终端
2. 运行安装命令：
   ```bash
   npx skills@latest add mattpocock/skills
   ```
3. 从列表中选择想要的技能（确保包含 `setup-matt-pocock-skills`）
4. 运行设置命令：
   ```
   /setup-matt-pocock-skills
   ```

### 方法 3: 手动安装（高级）

**优点**：
- 完全控制
- 可以修改技能文件
- 适合贡献者

**步骤**：
1. 克隆仓库：
   ```bash
   git clone https://github.com/mattpocock/skills.git
   ```
2. 复制技能文件到你的项目目录
3. 运行设置命令：
   ```
   /setup-matt-pocock-skills
   ```

## 设置过程

运行 `/setup-matt-pocock-skills` 后，系统会询问：

1. **问题追踪器选择**：
   - GitHub Issues
   - Linear
   - 本地文件（`.scratch/` 目录）

2. **分类标签设置**：
   - 用于 `/triage` 命令的标签
   - 例如：`needs-triage`, `ready-for-afk`

3. **文档存储位置**：
   - 指定文档保存目录

## 验证安装

安装完成后，可以尝试运行：
- `/grill-me` - 测试访谈功能
- `/ask-matt` - 询问适合的技能
- `/tdd` - 测试 TDD 功能