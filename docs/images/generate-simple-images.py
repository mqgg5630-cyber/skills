#!/usr/bin/env python3

"""
Skills 图解教程 - 简单图片生成脚本
使用 matplotlib 生成简单的图表
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_overall_architecture():
    """创建整体架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 标题
    ax.set_title('Skills 整体架构图', fontsize=16, fontweight='bold', pad=20)
    
    # 用户层
    user_box = FancyBboxPatch((0.4, 0.85), 0.2, 0.1, boxstyle="round,pad=0.02", 
                              facecolor='#e1f5fe', edgecolor='#0288d1', linewidth=2)
    ax.add_patch(user_box)
    ax.text(0.5, 0.9, '用户/开发者', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Skills 分类
    eng_box = FancyBboxPatch((0.1, 0.6), 0.35, 0.2, boxstyle="round,pad=0.02",
                             facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(eng_box)
    ax.text(0.275, 0.7, '工程技能\nEngineering Skills', ha='center', va='center', fontsize=10)
    
    prod_box = FancyBboxPatch((0.55, 0.6), 0.35, 0.2, boxstyle="round,pad=0.02",
                              facecolor='#e8f5e8', edgecolor='#388e3c', linewidth=2)
    ax.add_patch(prod_box)
    ax.text(0.725, 0.7, '生产力技能\nProductivity Skills', ha='center', va='center', fontsize=10)
    
    # 工程技能细分
    user_inv_box = FancyBboxPatch((0.1, 0.35), 0.15, 0.15, boxstyle="round,pad=0.02",
                                  facecolor='#fff3e0', edgecolor='#f57c00', linewidth=2)
    ax.add_patch(user_inv_box)
    ax.text(0.175, 0.425, '用户调用\n技能', ha='center', va='center', fontsize=9)
    
    model_inv_box = FancyBboxPatch((0.3, 0.35), 0.15, 0.15, boxstyle="round,pad=0.02",
                                   facecolor='#fce4ec', edgecolor='#c2185b', linewidth=2)
    ax.add_patch(model_inv_box)
    ax.text(0.375, 0.425, '模型调用\n技能', ha='center', va='center', fontsize=9)
    
    # 生产力技能细分
    user_inv_box2 = FancyBboxPatch((0.55, 0.35), 0.15, 0.15, boxstyle="round,pad=0.02",
                                   facecolor='#fff3e0', edgecolor='#f57c00', linewidth=2)
    ax.add_patch(user_inv_box2)
    ax.text(0.625, 0.425, '用户调用\n技能', ha='center', va='center', fontsize=9)
    
    model_inv_box2 = FancyBboxPatch((0.75, 0.35), 0.15, 0.15, boxstyle="round,pad=0.02",
                                    facecolor='#fce4ec', edgecolor='#c2185b', linewidth=2)
    ax.add_patch(model_inv_box2)
    ax.text(0.825, 0.425, '模型调用\n技能', ha='center', va='center', fontsize=9)
    
    # 核心概念
    concepts = ['问题追踪器', '问题', '分类角色', '共享语言']
    colors = ['#f1f8e9', '#f1f8e9', '#f1f8e9', '#f1f8e9']
    edge_colors = ['#689f38', '#689f38', '#689f38', '#689f38']
    
    for i, (concept, color, edge_color) in enumerate(zip(concepts, colors, edge_colors)):
        x = 0.15 + i * 0.2
        box = FancyBboxPatch((x, 0.1), 0.15, 0.12, boxstyle="round,pad=0.02",
                            facecolor=color, edgecolor=edge_color, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 0.075, 0.16, concept, ha='center', va='center', fontsize=9)
    
    # 箭头连接
    arrow_style = "Simple, tail_width=2, head_width=10, head_length=5"
    
    # 用户到分类
    ax.annotate('', xy=(0.275, 0.8), xytext=(0.5, 0.85),
                arrowprops=dict(arrowstyle=arrow_style, color='#0288d1'))
    ax.annotate('', xy=(0.725, 0.8), xytext=(0.5, 0.85),
                arrowprops=dict(arrowstyle=arrow_style, color='#0288d1'))
    
    # 分类到细分
    ax.annotate('', xy=(0.175, 0.5), xytext=(0.275, 0.6),
                arrowprops=dict(arrowstyle=arrow_style, color='#7b1fa2'))
    ax.annotate('', xy=(0.375, 0.5), xytext=(0.275, 0.6),
                arrowprops=dict(arrowstyle=arrow_style, color='#7b1fa2'))
    ax.annotate('', xy=(0.625, 0.5), xytext=(0.725, 0.6),
                arrowprops=dict(arrowstyle=arrow_style, color='#388e3c'))
    ax.annotate('', xy=(0.825, 0.5), xytext=(0.725, 0.6),
                arrowprops=dict(arrowstyle=arrow_style, color='#388e3c'))
    
    # 细分到核心概念
    for i in range(4):
        x = 0.15 + i * 0.2 + 0.075
        ax.annotate('', xy=(x, 0.22), xytext=(0.275, 0.35),
                    arrowprops=dict(arrowstyle=arrow_style, color='#f57c00', alpha=0.5))
        ax.annotate('', xy=(x, 0.22), xytext=(0.725, 0.35),
                    arrowprops=dict(arrowstyle=arrow_style, color='#388e3c', alpha=0.5))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/user/skills/docs/images/output/01-overall-architecture.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("生成整体架构图完成")

def create_workflow():
    """创建工作流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    ax.set_title('Skills 工作流程图', fontsize=16, fontweight='bold', pad=20)
    
    # 定义节点位置
    nodes = {
        'start': (0.5, 0.95),
        'install': (0.5, 0.85),
        'setup': (0.5, 0.75),
        'config': (0.5, 0.65),
        'ready': (0.5, 0.55),
        'decision': (0.5, 0.45),
        'grill': (0.2, 0.35),
        'tdd': (0.4, 0.35),
        'review': (0.6, 0.35),
        'architecture': (0.8, 0.35),
        'spec': (0.2, 0.25),
        'tickets': (0.2, 0.15),
        'implement': (0.2, 0.05),
        'red': (0.4, 0.25),
        'green': (0.4, 0.15),
        'refactor': (0.4, 0.05),
        'survey': (0.8, 0.25),
        'candidates': (0.8, 0.15),
        'done': (0.5, 0.05)
    }
    
    # 绘制节点
    for name, (x, y) in nodes.items():
        if name in ['start', 'ready', 'done']:
            # 椭圆形节点
            circle = plt.Circle((x, y), 0.03, color='#e8f5e8', ec='#388e3c', linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, name.title(), ha='center', va='center', fontsize=8, fontweight='bold')
        elif name == 'decision':
            # 菱形节点
            diamond = plt.Polygon([(x, y+0.04), (x+0.06, y), (x, y-0.04), (x-0.06, y)], 
                                 facecolor='#fff3e0', edgecolor='#f57c00', linewidth=2)
            ax.add_patch(diamond)
            ax.text(x, y, '决策', ha='center', va='center', fontsize=8, fontweight='bold')
        else:
            # 矩形节点
            box = FancyBboxPatch((x-0.06, y-0.03), 0.12, 0.06, boxstyle="round,pad=0.01",
                                facecolor='#e1f5fe', edgecolor='#0288d1', linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, name.title(), ha='center', va='center', fontsize=8)
    
    # 绘制箭头
    arrow_style = "Simple, tail_width=1, head_width=5, head_length=3"
    
    # 主流程
    connections = [
        ('start', 'install'), ('install', 'setup'), ('setup', 'config'), ('config', 'ready'),
        ('ready', 'decision'), ('decision', 'grill'), ('decision', 'tdd'), ('decision', 'review'),
        ('decision', 'architecture'), ('grill', 'spec'), ('spec', 'tickets'), ('tickets', 'implement'),
        ('implement', 'review'), ('tdd', 'red'), ('red', 'green'), ('green', 'refactor'),
        ('refactor', 'review'), ('review', 'done'), ('architecture', 'survey'), ('survey', 'candidates'),
        ('candidates', 'grill')
    ]
    
    for start, end in connections:
        start_pos = nodes[start]
        end_pos = nodes[end]
        ax.annotate('', xy=end_pos, xytext=start_pos,
                    arrowprops=dict(arrowstyle=arrow_style, color='#666666'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/user/skills/docs/images/output/02-workflow.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("生成工作流程图完成")

def create_installation_steps():
    """创建安装步骤图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    ax.set_title('Skills 安装步骤图', fontsize=16, fontweight='bold', pad=20)
    
    # 方法1
    method1_box = FancyBboxPatch((0.05, 0.6), 0.25, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#e1f5fe', edgecolor='#0288d1', linewidth=2)
    ax.add_patch(method1_box)
    ax.text(0.175, 0.9, '方法1: Claude Code 插件', ha='center', va='center', fontsize=10, fontweight='bold')
    
    steps1 = ['1. 打开 Claude Code', '2. 运行命令', '3. 插件自动安装', '4. 运行设置命令']
    for i, step in enumerate(steps1):
        ax.text(0.175, 0.85 - i*0.06, step, ha='center', va='center', fontsize=8)
    
    # 方法2
    method2_box = FancyBboxPatch((0.375, 0.6), 0.25, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(method2_box)
    ax.text(0.5, 0.9, '方法2: npx skills', ha='center', va='center', fontsize=10, fontweight='bold')
    
    steps2 = ['1. 打开终端', '2. 运行命令', '3. 选择技能', '4. 运行设置命令']
    for i, step in enumerate(steps2):
        ax.text(0.5, 0.85 - i*0.06, step, ha='center', va='center', fontsize=8)
    
    # 方法3
    method3_box = FancyBboxPatch((0.7, 0.6), 0.25, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#fff3e0', edgecolor='#f57c00', linewidth=2)
    ax.add_patch(method3_box)
    ax.text(0.825, 0.9, '方法3: 手动安装', ha='center', va='center', fontsize=10, fontweight='bold')
    
    steps3 = ['1. 克隆仓库', '2. 复制文件', '3. 运行设置命令', '4. 配置完成']
    for i, step in enumerate(steps3):
        ax.text(0.825, 0.85 - i*0.06, step, ha='center', va='center', fontsize=8)
    
    # 设置过程
    setup_box = FancyBboxPatch((0.2, 0.15), 0.6, 0.3, boxstyle="round,pad=0.02",
                               facecolor='#e8f5e8', edgecolor='#388e3c', linewidth=2)
    ax.add_patch(setup_box)
    ax.text(0.5, 0.4, '设置过程', ha='center', va='center', fontsize=12, fontweight='bold')
    
    setup_steps = ['选择问题追踪器', '配置分类标签', '指定文档位置']
    for i, step in enumerate(setup_steps):
        ax.text(0.5, 0.35 - i*0.06, step, ha='center', va='center', fontsize=9)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/user/skills/docs/images/output/03-installation-steps.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("生成安装步骤图完成")

def create_skills_comparison():
    """创建功能对比图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    ax.set_title('Skills 功能对比图', fontsize=16, fontweight='bold', pad=20)
    
    # 工程技能
    eng_box = FancyBboxPatch((0.05, 0.55), 0.4, 0.4, boxstyle="round,pad=0.02",
                             facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(eng_box)
    ax.text(0.25, 0.9, '工程技能', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 工程技能 - 用户调用
    user_eng_box = FancyBboxPatch((0.08, 0.7), 0.15, 0.15, boxstyle="round,pad=0.01",
                                  facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1)
    ax.add_patch(user_eng_box)
    ax.text(0.155, 0.775, '用户调用', ha='center', va='center', fontsize=8)
    
    user_eng_skills = ['ask-matt', 'grill-with-docs', 'triage', 'to-spec', 'implement']
    for i, skill in enumerate(user_eng_skills):
        ax.text(0.08, 0.72 - i*0.025, f'• {skill}', ha='left', va='center', fontsize=7)
    
    # 工程技能 - 模型调用
    model_eng_box = FancyBboxPatch((0.27, 0.7), 0.15, 0.15, boxstyle="round,pad=0.01",
                                   facecolor='#fce4ec', edgecolor='#c2185b', linewidth=1)
    ax.add_patch(model_eng_box)
    ax.text(0.345, 0.775, '模型调用', ha='center', va='center', fontsize=8)
    
    model_eng_skills = ['tdd', 'code-review', 'diagnosing-bugs', 'research', 'prototype']
    for i, skill in enumerate(model_eng_skills):
        ax.text(0.27, 0.72 - i*0.025, f'• {skill}', ha='left', va='center', fontsize=7)
    
    # 生产力技能
    prod_box = FancyBboxPatch((0.55, 0.55), 0.4, 0.4, boxstyle="round,pad=0.02",
                              facecolor='#e8f5e8', edgecolor='#388e3c', linewidth=2)
    ax.add_patch(prod_box)
    ax.text(0.75, 0.9, '生产力技能', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 生产力技能 - 用户调用
    user_prod_box = FancyBboxPatch((0.58, 0.7), 0.15, 0.15, boxstyle="round,pad=0.01",
                                   facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1)
    ax.add_patch(user_prod_box)
    ax.text(0.655, 0.775, '用户调用', ha='center', va='center', fontsize=8)
    
    user_prod_skills = ['grill-me', 'handoff', 'teach', 'to-questionnaire', 'wait-what']
    for i, skill in enumerate(user_prod_skills):
        ax.text(0.58, 0.72 - i*0.025, f'• {skill}', ha='left', va='center', fontsize=7)
    
    # 生产力技能 - 模型调用
    model_prod_box = FancyBboxPatch((0.77, 0.7), 0.15, 0.15, boxstyle="round,pad=0.01",
                                    facecolor='#fce4ec', edgecolor='#c2185b', linewidth=1)
    ax.add_patch(model_prod_box)
    ax.text(0.845, 0.775, '模型调用', ha='center', va='center', fontsize=8)
    
    model_prod_skills = ['grilling', 'writing-for-agents']
    for i, skill in enumerate(model_prod_skills):
        ax.text(0.77, 0.72 - i*0.025, f'• {skill}', ha='left', va='center', fontsize=7)
    
    # 技能选择指南
    guide_box = FancyBboxPatch((0.1, 0.1), 0.8, 0.35, boxstyle="round,pad=0.02",
                               facecolor='#e8f4fc', edgecolor='#0288d1', linewidth=2)
    ax.add_patch(guide_box)
    ax.text(0.5, 0.4, '技能选择指南', ha='center', va='center', fontsize=12, fontweight='bold')
    
    guide_items = [
        '新功能开发: /grill-with-docs → /to-spec → /to-tickets → /implement → /code-review',
        'Bug 修复: /diagnosing-bugs 或 /tdd',
        '架构改进: /improve-codebase-architecture → /grill-me → /implement',
        '学习新技能: /teach',
        '技术研究: /research'
    ]
    
    for i, item in enumerate(guide_items):
        ax.text(0.15, 0.35 - i*0.04, item, ha='left', va='center', fontsize=8)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/user/skills/docs/images/output/04-skills-comparison.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("生成功能对比图完成")

def create_core_concepts():
    """创建核心概念图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    ax.set_title('Skills 核心概念图', fontsize=16, fontweight='bold', pad=20)
    
    # 核心概念
    concepts = [
        ('问题追踪器', 0.2, 0.8),
        ('问题', 0.4, 0.8),
        ('分类角色', 0.6, 0.8),
        ('共享语言', 0.8, 0.8),
        ('决策工单', 0.5, 0.6)
    ]
    
    for name, x, y in concepts:
        box = FancyBboxPatch((x-0.08, y-0.04), 0.16, 0.08, boxstyle="round,pad=0.02",
                            facecolor='#e1f5fe', edgecolor='#0288d1', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # 问题追踪器类型
    tracker_types = [
        ('GitHub Issues', 0.1, 0.5),
        ('Linear', 0.2, 0.5),
        ('本地文件', 0.3, 0.5)
    ]
    
    for name, x, y in tracker_types:
        box = FancyBboxPatch((x-0.06, y-0.03), 0.12, 0.06, boxstyle="round,pad=0.01",
                            facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8)
    
    # 分类角色
    roles = [
        ('needs-triage', 0.5, 0.5),
        ('ready-for-afk', 0.6, 0.5),
        ('in-progress', 0.7, 0.5),
        ('done', 0.8, 0.5)
    ]
    
    for name, x, y in roles:
        box = FancyBboxPatch((x-0.06, y-0.03), 0.12, 0.06, boxstyle="round,pad=0.01",
                            facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8)
    
    # 箭头连接
    arrow_style = "Simple, tail_width=1, head_width=5, head_length=3"
    
    # 问题追踪器到类型
    for name, x, y in tracker_types:
        ax.annotate('', xy=(x, y+0.03), xytext=(0.2, 0.76),
                    arrowprops=dict(arrowstyle=arrow_style, color='#7b1fa2'))
    
    # 分类角色到角色
    for name, x, y in roles:
        ax.annotate('', xy=(x, y+0.03), xytext=(0.6, 0.76),
                    arrowprops=dict(arrowstyle=arrow_style, color='#f57c00'))
    
    # 决策工单到问题
    ax.annotate('', xy=(0.4, 0.76), xytext=(0.5, 0.64),
                arrowprops=dict(arrowstyle=arrow_style, color='#388e3c'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/user/skills/docs/images/output/05-core-concepts.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("生成核心概念图完成")

if __name__ == "__main__":
    print("开始生成 Skills 图解教程图片...")
    
    # 创建输出目录
    import os
    os.makedirs('/home/user/skills/docs/images/output', exist_ok=True)
    
    # 生成图片
    create_overall_architecture()
    create_workflow()
    create_installation_steps()
    create_skills_comparison()
    create_core_concepts()
    
    print("所有图片生成完成！")
    print("输出目录: /home/user/skills/docs/images/output/")