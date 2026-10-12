#!/usr/bin/env python3

"""
Skills 图解教程 - 生成 PPT 和 PDF 文件
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from fpdf import FPDF
import os

# 创建输出目录
output_dir = '/home/user/skills/docs/images/output'
os.makedirs(output_dir, exist_ok=True)

def create_pptx():
    """创建 PPT 文件"""
    prs = Presentation()
    
    # 设置幻灯片尺寸
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 定义颜色
    BLUE = RGBColor(0x02, 0x88, 0xD1)
    GREEN = RGBColor(0x38, 0x8E, 0x3C)
    ORANGE = RGBColor(0xF5, 0x7C, 0x00)
    PURPLE = RGBColor(0x7B, 0x1F, 0xA2)
    DARK = RGBColor(0x2C, 0x3E, 0x50)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    LIGHT_BLUE = RGBColor(0xE1, 0xF5, 0xFE)
    LIGHT_GREEN = RGBColor(0xE8, 0xF5, 0xE8)
    LIGHT_ORANGE = RGBColor(0xFF, 0xF3, 0xE0)
    LIGHT_PURPLE = RGBColor(0xF3, 0xE5, 0xF5)
    
    # 幻灯片 1: 标题页
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = "Skills 图解教程"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(48)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    title_para.alignment = PP_ALIGN.CENTER
    
    # 添加副标题
    subtitle_box = slide.shapes.add_textbox(Inches(2), Inches(3.5), Inches(9), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "零基础入门指南"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(32)
    subtitle_para.font.color.rgb = BLUE
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    # 添加描述
    desc_box = slide.shapes.add_textbox(Inches(2), Inches(5), Inches(9), Inches(1))
    desc_frame = desc_box.text_frame
    desc_frame.text = "AI 代理技能系统 | 提高开发效率 | 提升代码质量"
    desc_para = desc_frame.paragraphs[0]
    desc_para.font.size = Pt(20)
    desc_para.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
    desc_para.alignment = PP_ALIGN.CENTER
    
    # 幻灯片 2: 教程概述
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "教程概述"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加内容
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12), Inches(5.5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """本教程通过 5 张图表，帮助零基础的你快速理解 Skills 仓库的核心概念和使用方法。

图表列表：
1. 整体架构图 - 了解 Skills 的整体结构
2. 工作流程图 - 掌握日常开发流程
3. 安装步骤图 - 学习如何安装和设置
4. 功能对比图 - 了解各个技能的用途
5. 核心概念图 - 理解关键概念和关系

学习路径：
- 初学者：阅读整体架构图 → 学习安装步骤 → 查看核心概念
- 进阶者：研究功能对比 → 实践技能组合 → 参与社区"""
    
    content_frame.text = content
    for para in content_frame.paragraphs:
        para.font.size = Pt(18)
        para.font.color.rgb = DARK
        para.space_after = Pt(10)
    
    # 幻灯片 3: 整体架构图
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "1. 整体架构图"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加图片
    img_path = f'{output_dir}/01-overall-architecture.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    
    # 幻灯片 4: 工作流程图
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "2. 工作流程图"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加图片
    img_path = f'{output_dir}/02-workflow.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    
    # 幻灯片 5: 安装步骤图
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "3. 安装步骤图"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加图片
    img_path = f'{output_dir}/03-installation-steps.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    
    # 幻灯片 6: 功能对比图
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "4. 功能对比图"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加图片
    img_path = f'{output_dir}/04-skills-comparison.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    
    # 幻灯片 7: 核心概念图
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "5. 核心概念图"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加图片
    img_path = f'{output_dir}/05-core-concepts.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    
    # 幻灯片 8: 技能分类
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "技能分类详解"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加工程技能内容
    eng_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(5.5), Inches(5.5))
    eng_frame = eng_box.text_frame
    eng_frame.word_wrap = True
    
    eng_content = """工程技能 (Engineering Skills)

用户调用技能：
- ask-matt - 询问适合的技能
- grill-with-docs - 深入访谈 + 文档
- triage - 问题分类
- to-spec - 创建规格说明
- implement - 实现功能
- wayfinder - 规划大型任务

模型调用技能：
- tdd - 测试驱动开发
- code-review - 代码审查
- diagnosing-bugs - 诊断 Bug
- research - 技术研究
- prototype - 原型设计"""
    
    eng_frame.text = eng_content
    for para in eng_frame.paragraphs:
        para.font.size = Pt(14)
        para.font.color.rgb = DARK
        para.space_after = Pt(5)
    
    # 添加生产力技能内容
    prod_box = slide.shapes.add_textbox(Inches(6.5), Inches(1.5), Inches(6), Inches(5.5))
    prod_frame = prod_box.text_frame
    prod_frame.word_wrap = True
    
    prod_content = """生产力技能 (Productivity Skills)

用户调用技能：
- grill-me - 深入访谈
- handoff - 交接文档
- teach - 教学功能
- to-questionnaire - 创建问卷
- wait-what - 澄清误解

模型调用技能：
- grilling - 访谈原语
- writing-for-agents - 为代理写作

技能选择指南：
- 新功能开发：/grill-with-docs → /to-spec → /implement
- Bug 修复：/diagnosing-bugs 或 /tdd
- 架构改进：/improve-codebase-architecture"""
    
    prod_frame.text = prod_content
    for para in prod_frame.paragraphs:
        para.font.size = Pt(14)
        para.font.color.rgb = DARK
        para.space_after = Pt(5)
    
    # 幻灯片 9: 快速开始
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "快速开始"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加内容
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12), Inches(5.5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """安装 Skills（30秒）：

# 方法1: Claude Code 插件（推荐）
claude plugins install mattpocock-skills

# 方法2: npx skills
npx skills@latest add mattpocock/skills

运行设置命令：
/setup-matt-pocock-skills

开始使用：
/grill-me          - 深入访谈新功能
/tdd               - 测试驱动开发
/code-review       - 代码审查
/ask-matt          - 询问适合的技能"""
    
    content_frame.text = content
    for para in content_frame.paragraphs:
        para.font.size = Pt(18)
        para.font.color.rgb = DARK
        para.space_after = Pt(10)
    
    # 幻灯片 10: 更多资源
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "更多资源"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = DARK
    
    # 添加内容
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(5.5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """官方资源：
- 官方仓库：https://github.com/mattpocock/skills
- 官方网站：https://skills.sh
- 文档：https://skills.sh/mattpocock/skills

学习建议：
- 从简单技能开始，逐步深入
- 实践为主，理论为辅
- 善用共享语言，提高效率
- 定期回顾，持续改进

开始你的 Skills 学习之旅吧！"""
    
    content_frame.text = content
    for para in content_frame.paragraphs:
        para.font.size = Pt(20)
        para.font.color.rgb = DARK
        para.space_after = Pt(15)
    
    # 保存 PPT
    pptx_path = f'{output_dir}/skills-tutorial.pptx'
    prs.save(pptx_path)
    print(f"PPT 文件已生成：{pptx_path}")
    return pptx_path

def create_pdf():
    """创建 PDF 文件"""
    
    # 创建 PDF 对象
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 添加中文字体支持
    # 注意：由于环境中没有中文字体，我们将使用英文
    
    # 第 1 页：标题页
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 36)
    pdf.cell(0, 40, '', 0, 1, 'C')
    pdf.cell(0, 20, 'Skills Tutorial', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 24)
    pdf.cell(0, 15, 'Zero to Hero Guide', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 16)
    pdf.cell(0, 20, '', 0, 1, 'C')
    pdf.cell(0, 10, 'AI Agent Skills System', 0, 1, 'C')
    pdf.cell(0, 10, 'Improve Development Efficiency', 0, 1, 'C')
    pdf.cell(0, 10, 'Enhance Code Quality', 0, 1, 'C')
    
    # 第 2 页：教程概述
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Tutorial Overview', 0, 1, 'L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    overview = """This tutorial uses 5 diagrams to help beginners quickly understand the core concepts and usage of the Skills repository.

Diagram List:
1. Overall Architecture - Understand the overall structure of Skills
2. Workflow - Master daily development workflows
3. Installation Steps - Learn how to install and set up
4. Skills Comparison - Understand the purpose of each skill
5. Core Concepts - Understand key concepts and relationships

Learning Path:
- Beginners: Read architecture -> Learn installation -> View core concepts
- Advanced: Study skills comparison -> Practice skill combinations -> Join community"""
    
    for line in overview.split('\n'):
        pdf.cell(0, 8, line, 0, 1, 'L')
    
    # 第 3-7 页：图表
    diagrams = [
        ('01-overall-architecture.png', '1. Overall Architecture'),
        ('02-workflow.png', '2. Workflow'),
        ('03-installation-steps.png', '3. Installation Steps'),
        ('04-skills-comparison.png', '4. Skills Comparison'),
        ('05-core-concepts.png', '5. Core Concepts')
    ]
    
    for img_file, title in diagrams:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 28)
        pdf.cell(0, 15, title, 0, 1, 'L')
        pdf.ln(5)
        
        img_path = f'{output_dir}/{img_file}'
        if os.path.exists(img_path):
            # 计算图片位置和大小
            img_width = 180
            pdf.image(img_path, x=15, y=40, w=img_width)
    
    # 第 8 页：技能分类
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Skills Classification', 0, 1, 'L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Engineering Skills', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 12)
    
    eng_skills = """User-Invoked Skills:
- ask-matt - Ask which skill fits your situation
- grill-with-docs - Deep interview + documentation
- triage - Issue classification
- to-spec - Create specifications
- implement - Implement features
- wayfinder - Plan large tasks

Model-Invoked Skills:
- tdd - Test-driven development
- code-review - Code review
- diagnosing-bugs - Bug diagnosis
- research - Technical research
- prototype - Prototype design"""
    
    for line in eng_skills.split('\n'):
        pdf.cell(0, 7, line, 0, 1, 'L')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Productivity Skills', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 12)
    
    prod_skills = """User-Invoked Skills:
- grill-me - Deep interview
- handoff - Handoff documentation
- teach - Teaching functionality
- to-questionnaire - Create questionnaire
- wait-what - Clarify misunderstandings

Model-Invoked Skills:
- grilling - Interview primitive
- writing-for-agents - Writing for agents"""
    
    for line in prod_skills.split('\n'):
        pdf.cell(0, 7, line, 0, 1, 'L')
    
    # 第 9 页：快速开始
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Quick Start', 0, 1, 'L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    
    quick_start = """Install Skills (30 seconds):

# Method 1: Claude Code Plugin (Recommended)
claude plugins install mattpocock-skills

# Method 2: npx skills
npx skills@latest add mattpocock/skills

Run setup command:
/setup-matt-pocock-skills

Start using:
/grill-me          - Deep interview for new features
/tdd               - Test-driven development
/code-review       - Code review
/ask-matt          - Ask which skill fits"""
    
    for line in quick_start.split('\n'):
        pdf.cell(0, 8, line, 0, 1, 'L')
    
    # 第 10 页：更多资源
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'More Resources', 0, 1, 'L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    
    resources = """Official Resources:
- Repository: https://github.com/mattpocock/skills
- Website: https://skills.sh
- Documentation: https://skills.sh/mattpocock/skills

Learning Tips:
- Start with simple skills, gradually go deeper
- Practice为主, theory为辅
- Use shared language to improve efficiency
- Regular review, continuous improvement

Start your Skills learning journey now!"""
    
    for line in resources.split('\n'):
        pdf.cell(0, 8, line, 0, 1, 'L')
    
    # 保存 PDF
    pdf_path = f'{output_dir}/skills-tutorial.pdf'
    pdf.output(pdf_path)
    print(f"PDF 文件已生成：{pdf_path}")
    return pdf_path

if __name__ == '__main__':
    print("开始生成 PPT 和 PDF 文件...")
    
    # 生成 PPT
    pptx_path = create_pptx()
    
    # 生成 PDF
    pdf_path = create_pdf()
    
    print("\n文件生成完成！")
    print(f"PPT 文件：{pptx_path}")
    print(f"PDF 文件：{pdf_path}")
    print(f"\n文件大小：")
    print(f"PPT: {os.path.getsize(pptx_path) / 1024:.2f} KB")
    print(f"PDF: {os.path.getsize(pdf_path) / 1024:.2f} KB")