# -*- coding: utf-8 -*-
"""把交付表汇总成一个 Excel 工作簿"""
import os
import pandas as pd
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

T = "/home/user/skills/cfmd_latest/tables"
OUT = "/home/user/skills/cfmd_latest/文档/cFMD_v1.3.2_结果表汇总.xlsx"

SHEETS = [
    ("说明", None),
    ("类别汇总", "02_按发酵种类汇总.csv"),
    ("SGB汇总", "04_SGB水平汇总_含发酵类别.csv"),
    ("类型明细", "20_发酵类型明细_按type.csv"),
    ("益生菌分层", "22_益生菌分层汇总.csv"),
    ("益生菌_制剂", "05_益生菌制剂来源MAG表.csv"),
    ("益生菌_严格名单", "21_益生菌严格名单MAG表.csv"),
    ("益生菌_宽口径", "06_益生菌物种MAG全库表.csv"),
    ("antiSMASH输入", "09_antiSMASH输入MAG清单_每SGB代表株.csv"),
    ("BGC产物知识", "17_antiSMASH产物知识表_文献依据.csv"),
    ("BGC工作量_原核", "18_antiSMASH_BGC预期工作量_按属.csv"),
    ("BGC工作量_真核", "19_antiSMASH_BGC预期工作量_真核属.csv"),
    ("alpha多样性", "15_同基质发酵vs非发酵多样性.csv"),
    ("物种差异", "10_物种谱_发酵vs非发酵差异.csv"),
    ("类别物种丰度", "11_类别水平物种平均丰度.csv"),
    ("与外部表核对", "23_与外部汇总表核对.csv"),
    ("MAG主表", "00_MAG主表_全部.csv"),
]

KEEP = {
    "MAG主表": ["dataset_id", "MAG_id", "sample_id", "SGB_id", "superkingdom", "phylum", "class",
              "order", "family", "genus", "species", "completeness", "contamination", "genome_size",
              "category", "发酵类别中文", "type", "食品类型中文", "fermented", "country",
              "质量等级", "SGB类型", "物种", "属", "纳入分析", "益生菌归属"],
    "益生菌_宽口径": ["MAG_id", "SGB_id", "物种", "属", "发酵类别中文", "食品类型中文",
                  "completeness", "contamination", "质量等级", "country"],
    "益生菌_严格名单": ["MAG_id", "SGB_id", "物种", "属", "发酵类别中文", "食品类型中文",
                  "completeness", "contamination", "质量等级", "country"],
    "antiSMASH输入": ["MAG_id", "SGB_id", "物种", "属", "发酵类别中文", "SGB类型",
                   "completeness", "contamination", "genome_size", "antiSMASH优先级"],
}

HDR_FILL = PatternFill("solid", fgColor="2E5E8E")
HDR_FONT = Font(color="FFFFFF", bold=True, size=10, name="微软雅黑")
BODY_FONT = Font(size=9.5, name="微软雅黑")
THIN = Border(*[Side(style="thin", color="D9D9D9")] * 4)

notes = [
    ["cFMD v1.3.2 结果表汇总"],
    [""],
    ["数据版本", "curatedFoodMetagenomicData v1.3.2（GitHub SegataLab/cFMD，主分支 7c09082，2026-06-18）"],
    ["规模", "4,125 份食品宏基因组、109 个数据集、54 个国家、18,180 个 MAG、1,654 个 SGB"],
    ["分析集", "完整度 ≥50%、污染 <5% 且有 SGB 编号的 17,621 个 MAG"],
    ["发酵样品", "3,293 份，15,446 个 MAG，1,142 个 SGB"],
    ["对照表", "论文版 v1.1.0 为 2,533 份样品、10,899 个 MAG、1,144 个 SGB；两版数字不可混用"],
    ["两个口径", "MAG 记录数（与样品关联的全部行，全库 18,180 / 发酵 15,722）与纳入分析 MAG 数"
             "（通过质量与 SGB 筛选，全库 17,621 / 发酵 15,446）相差 276 条，原因见“与外部表核对”页"],
    [""],
    ["工作表说明"],
    ["类别汇总", "10 个发酵类别的样品、MAG、HQ、SGB、属种数与优势类群"],
    ["SGB汇总", "1,654 个 SGB 的分类、新颖性、来源类别与 MAG 数"],
    ["类型明细", "91 个发酵食品类型（type）的明细，可直接挑选工艺做深入分析"],
    ["益生菌分层", "四个口径的种 / SGB / MAG 计数，先看这张表再看下面三张"],
    ["益生菌_制剂", "益生菌产品来源的 42 个 MAG"],
    ["益生菌_严格名单", "QPS、ISAPP 与国内名单内 28 个种的 4,925 个 MAG"],
    ["益生菌_宽口径", "18 个乳杆菌相关属 + 双歧杆菌属的 6,385 个 MAG（类群口径，非全部益生菌）"],
    ["antiSMASH输入", "按 SGB 去重的 1,142 个代表基因组，含 P1/P2 优先级"],
    ["BGC产物知识", "50 个分类单元的已知 BGC 类型与代表产物，附文献依据"],
    ["BGC工作量", "按属估算的 BGC 数量区间，仅用于评估工作量"],
    ["alpha多样性", "同基质条件下发酵与非发酵的 Shannon 指数与检验结果"],
    ["物种差异", "发酵组与非发酵组的物种平均相对丰度差异"],
    ["MAG主表", "18,180 个 MAG 的完整注释，可按 MAG_id 回溯"],
    [""],
    ["注意", "antiSMASH 未实际运行，BGC 相关工作表为文献推算，不是实测结果。"],
]

with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
    pd.DataFrame(notes).to_excel(xw, sheet_name="说明", index=False, header=False)
    for name, fn in SHEETS:
        if fn is None:
            continue
        df = pd.read_csv(f"{T}/{fn}", encoding="utf-8-sig", low_memory=False)
        if name in KEEP:
            cols = [c for c in KEEP[name] if c in df.columns]
            df = df[cols]
        df.to_excel(xw, sheet_name=name, index=False)

    wb = xw.book
    ws = wb["说明"]
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 95
    ws["A1"].font = Font(size=14, bold=True, color="2E5E8E", name="微软雅黑")
    for r in range(3, ws.max_row + 1):
        c = ws.cell(row=r, column=1)
        if c.value:
            c.font = Font(size=10, bold=True, name="微软雅黑")
        v = ws.cell(row=r, column=2)
        v.font = Font(size=10, name="微软雅黑")
        v.alignment = Alignment(wrap_text=True, vertical="top")

    for name, _ in SHEETS[1:]:
        sh = wb[name]
        sh.freeze_panes = "A2"
        for cell in sh[1]:
            cell.fill = HDR_FILL
            cell.font = HDR_FONT
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sh.row_dimensions[1].height = 30
        for i, col in enumerate(sh.iter_cols(min_row=2, max_row=min(sh.max_row, 200)), start=1):
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            sh.column_dimensions[get_column_letter(i)].width = min(max(9, width * 1.35), 46)
        for row in sh.iter_rows(min_row=2, max_row=sh.max_row, max_col=sh.max_column):
            for c in row:
                c.font = BODY_FONT
    wb["类别汇总"].sheet_view.zoomScale = 90

print("saved", OUT, os.path.getsize(OUT) // 1024, "KB")
