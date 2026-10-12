#!/bin/bash

# 生成所有图表图片的脚本

echo "开始生成 Skills 图表图片..."

# 创建输出目录
mkdir -p /home/user/skills/docs/images/output

# 生成整体架构图
echo "生成整体架构图..."
mmdc -i /home/user/skills/docs/images/01-overall-architecture.md -o /home/user/skills/docs/images/output/01-overall-architecture.png -t default -b white

# 生成工作流程图
echo "生成工作流程图..."
mmdc -i /home/user/skills/docs/images/02-workflow.md -o /home/user/skills/docs/images/output/02-workflow.png -t default -b white

# 生成安装步骤图
echo "生成安装步骤图..."
mmdc -i /home/user/skills/docs/images/03-installation-steps.md -o /home/user/skills/docs/images/output/03-installation-steps.png -t default -b white

# 生成功能对比图
echo "生成功能对比图..."
mmdc -i /home/user/skills/docs/images/04-skills-comparison.md -o /home/user/skills/docs/images/output/04-skills-comparison.png -t default -b white

# 生成核心概念图
echo "生成核心概念图..."
mmdc -i /home/user/skills/docs/images/05-core-concepts.md -o /home/user/skills/docs/images/output/05-core-concepts.png -t default -b white

echo "所有图片生成完成！"
echo "输出目录: /home/user/skills/docs/images/output/"
ls -la /home/user/skills/docs/images/output/