# cFMD 发酵与益生菌 MAG 分析：交付说明

数据来源：curatedFoodMetagenomicData（cFMD）v1.1.0，GitHub `SegataLab/cFMD`，与 Carlino et al., *Cell*, 2024（PMID 39214080）配套。
规模：2,533 份食品宏基因组、59 个数据集、50 个国家、14.7 Tb 碱基；10,899 个 MAG、1,144 个 SGB。

## 目录

```
cfmd_deliverables/
├── 文档/
│   ├── cFMD食品微生物组MAG分析报告_含文献版.docx     主报告，含数据来源、参考文献、核对表
│   ├── cFMD发酵与益生菌MAG分析_汇报版.docx           汇报稿，无参考文献，结论与下一步为主
│   └── cFMD分析结果表.xlsx                            16 个工作表，关键结果汇总
├── tables/                                            23 个 CSV
├── figures/                                           6 张 PNG（300 dpi）
└── scripts/                                           14 个脚本（整理、统计、绘图、报告、antiSMASH 流程）
```

## 主要结论

- 发酵样品 2,262 份，10,202 个 MAG（原核 9,445、真核 757），957 个 SGB，其中已知种 537、未知种 204、食品新种 216。
- 乳制品占 67.4% 的 MAG，发酵饮料 19.7%，两者接近九成；发酵鱼仅 32 个。
- 乳酸菌相关 23 属合计 5,273 个 MAG，占发酵样品原核 MAG 的 55.8%。
- 益生菌制剂样品 14 份、42 个 MAG、23 个 SGB；核心益生菌物种 28 种、30 个 SGB、2,884 个 MAG。
- antiSMASH 输入建议 957 个代表株（每 SGB 一株），预期原核 1,185–3,695 个 BGC、真核 315–872 个。

## 脚本

| 脚本 | 作用 |
| --- | --- |
| 01_build_tables.py | 合并元数据与 MAG 清单，生成主表、类别汇总、SGB 表、益生菌表、antiSMASH 输入清单 |
| 02_profiles.py | MetaPhlAn4 物种谱分析：发酵 vs 非发酵、类别间差异 |
| 02b_type_detail.py | type 层级明细（80 类） |
| 03_diversity.py | alpha 多样性与同基质配对比较 |
| 04_bgc_table.py | antiSMASH 产物知识表（50 个分类单元） |
| 05_figures.py | 6 张图 |
| 06_bgc_workload.py | 按属估算 BGC 数量与工作量 |
| 08_report_lit.py | 生成含文献版 DOCX |
| 09_report_brief.py | 生成汇报版 DOCX |
| 13_make_excel.py | 生成 Excel 工作簿 |
| 10_download_mags.sh | 从 Zenodo 按数据集下载 MAG，仅保留代表株 |
| 11_run_antismash.sh | 批量运行 antiSMASH 8.0.4，支持断点续跑 |
| 12_parse_antismash.py | 汇总 antiSMASH 结果，输出 BGC 明细与交叉表 |

## 复现

```bash
git clone --depth 1 --branch v1.1.0 https://github.com/SegataLab/cFMD.git
# 将 cFMD_*.tsv 放到 /tmp/cfmd，或修改 01_build_tables.py 中的 SRC
python scripts/01_build_tables.py
python scripts/02_profiles.py && python scripts/02b_type_detail.py && python scripts/03_diversity.py
python scripts/04_bgc_table.py && python scripts/06_bgc_workload.py
python scripts/05_figures.py
python scripts/08_report_lit.py && python scripts/09_report_brief.py && python scripts/13_make_excel.py
```

antiSMASH 部分需在能访问 Zenodo 的服务器上执行：

```bash
bash scripts/10_download_mags.sh tables/09_antiSMASH输入MAG清单_每SGB代表株.csv ./mags
conda create -n antismash -c conda-forge -c bioconda antismash=8.0.4
conda run -n antismash bash scripts/11_run_antismash.sh ./mags/fasta ./antismash 4 8
python scripts/12_parse_antismash.py ./antismash/results tables/00_MAG主表_全部.csv tables
```

## 注意

- MAG 序列未下载（Zenodo 9.8 GB 压缩包，按数据集拆分 272.5 GB；当前环境无 Zenodo 出站访问），报告中 antiSMASH 部分为基于分类学与文献的产物预判，不是实测结果。
- 类别样本量差异大，跨类别比较以趋势解读为宜。
