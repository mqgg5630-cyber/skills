#!/usr/bin/env python3

"""
Skills Tutorial - Generate PDF file only
"""

from fpdf import FPDF
import os

# Create output directory
output_dir = '/home/user/skills/docs/images/output'
os.makedirs(output_dir, exist_ok=True)

def create_pdf():
    """Create PDF file"""
    
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page 1: Title page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 36)
    pdf.cell(0, 40, '', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 20, 'Skills Tutorial', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('Helvetica', '', 24)
    pdf.cell(0, 15, 'Zero to Hero Guide', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('Helvetica', '', 16)
    pdf.cell(0, 20, '', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, 'AI Agent Skills System', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, 'Improve Development Efficiency', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, 'Enhance Code Quality', new_x="LMARGIN", new_y="NEXT", align='C')
    
    # Page 2: Tutorial overview
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Tutorial Overview', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    overview_lines = [
        "This tutorial uses 5 diagrams to help beginners",
        "quickly understand the core concepts and usage",
        "of the Skills repository.",
        "",
        "Diagram List:",
        "1. Overall Architecture - Understand the structure",
        "2. Workflow - Master daily development workflows",
        "3. Installation Steps - Learn how to install",
        "4. Skills Comparison - Understand each skill",
        "5. Core Concepts - Understand key concepts",
        "",
        "Learning Path:",
        "- Beginners: Architecture -> Installation -> Concepts",
        "- Advanced: Comparison -> Practice -> Community"
    ]
    
    for line in overview_lines:
        pdf.cell(0, 8, line, new_x="LMARGIN", new_y="NEXT", align='L')
    
    # Page 3-7: Diagrams
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
        pdf.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT", align='L')
        pdf.ln(5)
        
        img_path = f'{output_dir}/{img_file}'
        if os.path.exists(img_path):
            # Calculate image position and size
            img_width = 180
            pdf.image(img_path, x=15, y=40, w=img_width)
    
    # Page 8: Skills classification
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Skills Classification', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Engineering Skills', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.set_font('Helvetica', '', 12)
    
    eng_skills = [
        "User-Invoked Skills:",
        "- ask-matt - Ask which skill fits your situation",
        "- grill-with-docs - Deep interview + documentation",
        "- triage - Issue classification",
        "- to-spec - Create specifications",
        "- implement - Implement features",
        "- wayfinder - Plan large tasks",
        "",
        "Model-Invoked Skills:",
        "- tdd - Test-driven development",
        "- code-review - Code review",
        "- diagnosing-bugs - Bug diagnosis",
        "- research - Technical research",
        "- prototype - Prototype design"
    ]
    
    for line in eng_skills:
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT", align='L')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Productivity Skills', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.set_font('Helvetica', '', 12)
    
    prod_skills = [
        "User-Invoked Skills:",
        "- grill-me - Deep interview",
        "- handoff - Handoff documentation",
        "- teach - Teaching functionality",
        "- to-questionnaire - Create questionnaire",
        "- wait-what - Clarify misunderstandings",
        "",
        "Model-Invoked Skills:",
        "- grilling - Interview primitive",
        "- writing-for-agents - Writing for agents"
    ]
    
    for line in prod_skills:
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT", align='L')
    
    # Page 9: Quick start
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'Quick Start', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    
    quick_start = [
        "Install Skills (30 seconds):",
        "",
        "# Method 1: Claude Code Plugin (Recommended)",
        "claude plugins install mattpocock-skills",
        "",
        "# Method 2: npx skills",
        "npx skills@latest add mattpocock/skills",
        "",
        "Run setup command:",
        "/setup-matt-pocock-skills",
        "",
        "Start using:",
        "/grill-me          - Deep interview for new features",
        "/tdd               - Test-driven development",
        "/code-review       - Code review",
        "/ask-matt          - Ask which skill fits"
    ]
    
    for line in quick_start:
        pdf.cell(0, 8, line, new_x="LMARGIN", new_y="NEXT", align='L')
    
    # Page 10: More resources
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'More Resources', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 14)
    
    resources = [
        "Official Resources:",
        "- Repository: https://github.com/mattpocock/skills",
        "- Website: https://skills.sh",
        "- Documentation: https://skills.sh/mattpocock/skills",
        "",
        "Learning Tips:",
        "- Start with simple skills, gradually go deeper",
        "- Practice oriented, theory as supplement",
        "- Use shared language to improve efficiency",
        "- Regular review, continuous improvement",
        "",
        "Start your Skills learning journey now!"
    ]
    
    for line in resources:
        pdf.cell(0, 8, line, new_x="LMARGIN", new_y="NEXT", align='L')
    
    # Save PDF
    pdf_path = f'{output_dir}/skills-tutorial.pdf'
    pdf.output(pdf_path)
    print(f"PDF file generated: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    print("Generating PDF file...")
    
    # Generate PDF
    pdf_path = create_pdf()
    
    print("\nFile generation complete!")
    print(f"PDF file: {pdf_path}")
    print(f"\nFile size:")
    print(f"PDF: {os.path.getsize(pdf_path) / 1024:.2f} KB")