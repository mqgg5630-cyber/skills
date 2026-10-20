# -*- coding: utf-8 -*-
"""把关键表合并成一个 Excel 工作簿，带格式与工作表说明"""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

T = "/home/user/skills/cfmd_deliverables/tables"
OUT = "/home/user/skills/cfmd_deliverables/文档/cFMD分析结果表.xlsx"

SHEETS = [
    ("00 说明", None),
    ("01 数据总览", f"{T}/02_按发酵种类汇总.csv"),
    ("02 发酵MAG总表", f"{T}/01_发酵MAG总表.csv"),
    ("03 属矩阵", f"{T}/03_属水平MAG数量矩阵.csv"),
    ("04 SGB汇总", f"{T}/04_SGB水平汇总_含发酵类别.csv"),
    ("05 益生菌_制剂", f"{T}/05_益生菌制剂来源MAG表.csv"),
    ("06 益生菌_核心种", f"{T}/06_益生菌物种MAG全库表.csv"),
    ("07 益生菌x类别", f"{T}/07_益生菌物种x发酵类别矩阵.csv"),
    ("08 真核MAG", f"{T}/08_发酵食品真核MAG表.csv"),
    ("09 antiSMASH输入", f"{T}/09_antiSMASH输入MAG清单_每SGB代表株.csv"),
    ("10 物种谱差异", f"{T}/10_物种谱_发酵vs非发酵差异.csv"),
    ("11 类别物种丰度", f"{T}/11_类别水平物种平均丰度.csv"),
    ("12 alpha多样性", f"{T}/14_alpha多样性_按类别.csv"),
    ("13 BGC知识表", f"{T}/17_antiSMASH产物知识表_文献依据.csv"),
    ("14 BGC工作量", f"{T}/18_antiSMASH_BGC预期工作量_按属.csv"),
    ("15 类型明细", f"{T}/20_发酵类型明细_按type.csv"),
]

notes = pd.DataFrame([
    ["数据来源", "curatedFoodMetagenomicData (cFMD) v1.1.0，GitHub: SegataLab/cFMD；对应 Carlino et al., Cell, 2024"],
    ["样品与 MAG", "2,533 份食品宏基因组、59 个数据集、50 个国家；10,899 个 MAG、1,144 个 SGB"],
    ["发酵样品", "2,262 份，10,202 个 MAG，957 个 SGB"],
    ["质量分级", "HQ：完整度 ≥90% 且污染 <5%；MQ：完整度 50%–90% 且污染 <5%"],
    ["益生菌归属", "A 核心益生菌种；B QPS/发酵剂相关种；C 需谨慎/条件致病；空为未归类"],
    ["工作表", "01 类别汇总；02 发酵 MAG 全表；03 属水平计数；04 SGB 级；05–07 益生菌；08 真核；09 antiSMASH 输入；10–12 物种谱与多样性；13–14 BGC"],
    ["字段说明", "完整度、污染度由 CheckM 估计；基因组大小单位 Mb；相对丰度单位 %"],
    ["生成日期", "2026-10-20"],
], columns=["项目", "说明"])

with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
    notes.to_excel(xw, sheet_name="00 说明", index=False)
    for name, path in SHEETS:
        if path is None:
            continue
        try:
            df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
        except Exception as e:
            print("skip", name, e)
            continue
        if len(df) > 10000:
            df = df.iloc[:10000]
        df.to_excel(xw, sheet_name=name, index=False)

wb = load_workbook(OUT)
head_fill = PatternFill("solid", fgColor="E4EBF3")
head_font = Font(name="微软雅黑", size=9, bold=True, color="1F3A55")
body_font = Font(name="微软雅黑", size=9)
thin = Side(style="thin", color="D0D7DE")
for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    for c in ws[1]:
        c.fill = head_fill
        c.font = head_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = body_font
            c.border = Border(bottom=thin)
    for j, col in enumerate(ws.columns, start=1):
        width = max((len(str(c.value)) if c.value is not None else 0) for c in list(col)[:200])
        ws.column_dimensions[get_column_letter(j)].width = min(max(10, width * 1.25), 48)
    ws.row_dimensions[1].height = 26

# 说明页排版
ws = wb["00 说明"]
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 96
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    row[1].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[row[0].row].height = 30

wb.save(OUT)
print("saved", OUT, round(os.path.getsize(OUT) / 1024 / 1024, 2), "MB")
