# cFMD v1.3.2 发酵与益生菌 MAG 分析

本目录是对公开食品宏基因组资源 cFMD（curatedFoodMetagenomicData）最新版的重建与分析，重点在发酵食品模块与益生菌方向。
原始研究为 Carlino N. 等 2024 年发表于 Cell 的工作（PMID 39214080）。

## 一、为什么是 v1.3.2

论文发表时配套的数据版本是 v1.1.0，仓库主分支此后迭代到 v1.3.2（2026-06-18）。两版的差别不是口径而是数据量：

| 指标 | v1.1.0（论文版） | v1.3.2（本目录） |
| --- | --- | --- |
| 样品 | 2,533 | 4,125 |
| 数据集 | 59 | 109 |
| MAG | 10,899 | 18,180 |
| SGB | 1,144 | 1,654 |
| 发酵样品 | 2,262 | 3,293 |
| 发酵 MAG | 10,202 | 15,446 |

凡是用 v1.1.0 的表做出来的统计，与按最新表整理的数对不上，基本都是版本差。本目录所有数字基于 v1.3.2，与 v1.1.0 的结果不可混用。

v1.3.2 取消了顶层的 SGB 汇总表（`cFMD_sgbs_prokaryotic/eukaryotic.tsv`），SGB 级信息需要在 MAG 清单上自行聚合，`scripts/01_build_tables.py` 做的就是这件事。

## 一点五、两个口径：记录数与分析数

cFMD 的 MAG 清单里，一个 MAG 行对应一个样品中的一次分箱；这些行并不都满足质量与 SGB 归属要求。

| 口径 | 全库 | 发酵样品 | 说明 |
| --- | --- | --- | --- |
| MAG 记录数 | 18,180 | 15,722 | 与样品关联的全部 MAG 行，用于与元数据、外部汇总表对齐 |
| 纳入分析 MAG | 17,621 | 15,446 | 完整度 ≥50%、污染 <5% 且有 SGB 编号 |

发酵部分两者相差 276 条：78 个原核（污染 ≥5% 或完整度 <50%）、99 个真核、99 条 superkingdom 为空的未分类记录。
按类别、按样品核对后与外部的《cFMD_全发酵食品统计汇总.xlsx》完全一致（该表用的是记录口径），核对明细见 `tables/23_与外部汇总表核对.csv`。
另有 220 份发酵样品没有任何 MAG 关联（乳制品 171 份），计算"每样品 MAG 数"时应用 3,073 作分母。

## 二、主要结果

- 4,125 份样品、109 个数据集、54 个国家、25.09 Tb；18,180 个 MAG，进入分析 17,621 个；1,654 个 SGB，其中 600 个无参考基因组。
- 发酵样品 3,293 份（79.8%），15,446 个 MAG、1,142 个 SGB；乳制品占 72.8%，发酵饮料 13.9%。
- 乳酸菌相关 23 个属 8,183 个 MAG，占发酵原核 MAG 的 56.1%。
- 益生菌分四个口径：制剂来源 42 个 MAG；名单内 28 个种 4,925 个 MAG；属级放宽 6,385 个；另有发酵剂/QPS 相关 1,869 个、肠球菌等 292 个。
- antiSMASH 未实际运行（无序列、无算力）。按 SGB 去重的 1,142 个代表基因组预计产生原核 1,461–4,554 个 BGC、真核 315–878 个，属工作量估算。

## 三、文件

```
文档/
  cFMD_v1.3.2_发酵与益生菌MAG分析报告_含文献版.docx   九章 + 附录，正文带 [n] 文献标注，16 篇参考文献
  cFMD_v1.3.2_发酵与益生菌MAG分析报告_汇报版.docx     无文献标注，给顾问/汇报用
  cFMD_v1.3.2_结果表汇总.xlsx                        全部结果表，含说明页与核对页
tables/     22 个 CSV，编号与报告中的表号对应
figures/    6 张图，PNG 300 dpi
scripts/    建表、物种谱、绘图、报告与 Excel 生成脚本
```

表格编号对应关系见报告附录；`00_MAG主表_全部.csv` 是 18,180 个 MAG 的完整注释，逐条 MAG 都可用 `MAG_id` 回溯。

## 四、复现

依赖：Python 3.11、pandas、numpy、scipy、matplotlib、openpyxl、python-docx。

```bash
python scripts/01_build_tables.py     # 建表，输出 00–09、20–22
python scripts/02_profiles.py         # 物种谱，输出 10–16
python scripts/04_bgc_table.py        # BGC 知识表，输出 17
python scripts/05_figures.py          # 图 1–6
python scripts/06_bgc_workload.py     # BGC 工作量，输出 18–19
python scripts/08_report_lit.py       # 含文献版 DOCX
python scripts/09_report_brief.py     # 汇报版 DOCX
python scripts/10_make_excel.py       # 汇总 xlsx
```

数据源为 cFMD 仓库的三个总表（`cFMD_metadata.tsv`、`cFMD_mags_list.tsv`、`cFMD_datasets.tsv`）与 `cFMD_data/<dataset>/` 下的 107 个物种谱 TSV，路径写在脚本头部 `SRC`。

## 五、需要说明的三点

1. MAG 序列在 Zenodo（DOI 10.5281/zenodo.10891046），全量约 272 GB。本目录只用了总表，没有下载序列，因此 antiSMASH 部分为预判而非实测。
2. `cFMD_mags_list.tsv` 里部分 MAG 的物种名带 `_SGB` 后缀，表示只到属级或未定种；本文的“已定名种”统计只计不带后缀的记录。
3. 有 21 个 SGB 的 MAG 在源表中被同时标为 uSGB 与 ufSGB，本文按 SGB 内多数 MAG 的标注统一，票数相同时取 uSGB，保证每个 SGB 只归一类。
