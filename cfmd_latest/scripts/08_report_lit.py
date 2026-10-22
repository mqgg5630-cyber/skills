# -*- coding: utf-8 -*-
"""生成【含文献版】报告 DOCX —— cFMD v1.3.2"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import docxkit as K

T = "/home/user/skills/cfmd_latest/tables"
F = "/home/user/skills/cfmd_latest/figures"
OUT = "/home/user/skills/cfmd_latest/文档/cFMD_v1.3.2_发酵与益生菌MAG分析报告_含文献版.docx"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

s = pd.read_csv(f"{T}/02_按发酵种类汇总.csv")
s10 = s[s["发酵类别"] != "合计"].copy()
bgc = pd.read_csv(f"{T}/17_antiSMASH产物知识表_文献依据.csv", encoding="utf-8-sig")
work = pd.read_csv(f"{T}/18_antiSMASH_BGC预期工作量_按属.csv", encoding="utf-8-sig")
probmag = pd.read_csv(f"{T}/05_益生菌制剂来源MAG表.csv", encoding="utf-8-sig")
pair = pd.read_csv(f"{T}/15_同基质发酵vs非发酵多样性.csv", encoding="utf-8-sig")
tab6 = pd.read_csv(f"{T}/06_益生菌物种MAG全库表.csv", encoding="utf-8-sig")
td = pd.read_csv(f"{T}/20_发酵类型明细_按type.csv", encoding="utf-8-sig")

doc = K.new_document()
K.add_header_text(doc, "cFMD v1.3.2 食品微生物组 MAG 分析")
K.add_page_number_footer(doc, "cFMD v1.3.2")

# ============================================================ 封面
K.title(doc,
        "食品宏基因组 MAG 资源中的发酵与益生菌模块分析",
        "基于 cFMD v1.3.2：4,125 份食品宏基因组、18,180 个 MAG、1,654 个 SGB",
        "数据版本：curatedFoodMetagenomicData v1.3.2（GitHub SegataLab/cFMD，2026-06-18）\n"
        "原始文献：Carlino et al., Cell, 2024（PMID 39214080）\n"
        "分析日期：2026 年 10 月    文件版本：含文献版")

doc.add_paragraph()
K.h2(doc, "目  录")
toc = [
    "一、数据来源与版本",
    "    1.1 原始文献与本资源的关系",
    "    1.2 使用的最新版总表",
    "    1.3 与论文版（v1.1.0）的差异",
    "    1.4 与他人整理结果的核对",
    "二、数据库总体情况",
    "三、分析口径与分组规则",
    "四、发酵种类模块",
    "    4.1 总体分布",
    "    4.2 各发酵类别的菌群构成",
    "    4.3 优势属与优势种",
    "    4.4 与同基质非发酵样品的对照",
    "    4.5 真核微生物部分",
    "五、益生菌模块",
    "    5.1 四个口径",
    "    5.2 益生菌制剂来源的 MAG",
    "    5.3 名单内益生菌种在发酵食品中的分布",
    "    5.4 名单之外的乳酸菌类群",
    "六、antiSMASH 次级代谢产物分析",
    "    6.1 方法与输入",
    "    6.2 已知产物对应关系",
    "    6.3 预期 BGC 规模",
    "    6.4 与发酵过程和益生菌功能的关联",
    "    6.5 执行方案与判读要点",
    "七、可继续开展的分析",
    "八、局限说明",
    "九、参考文献",
    "附录  交付文件清单",
]
for t in toc:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = K.Pt(2.5)
    p.paragraph_format.left_indent = K.Pt(6 if not t.startswith("    ") else 22)
    K._set_run(p.add_run(t), 10, False, K.DARK)

# ============================================================ 一
K.h1(doc, "一、数据来源与版本", page_break=True)
K.h2(doc, "1.1 原始文献与本资源的关系")
K.para(doc, "本分析的起点是 Carlino 等 2024 年发表于 Cell 的食品宏基因组研究。该文构建了 cFMD"
            "（curatedFoodMetagenomicData）资源：整合 1,950 份新测序与 583 份公共食品宏基因组，"
            "重建 10,899 个 MAG，聚类为 1,036 个原核与 108 个真核 SGB，其中 320 个为此前未描述的分类单元；"
            "并与 20,000 余份人体宏基因组比对，估计食物来源 SGB 平均占成人肠道微生物组的 3% 左右[1]。")
ref = pd.DataFrame([
    ["题目", "Unexplored microbial diversity from 2,500 food metagenomes and links with the human microbiome"],
    ["作者", "Carlino N, Blanco-Míguez A, Manghi P, et al.（通讯作者 Nicola Segata）"],
    ["期刊", "Cell, 2024, 187(20): 5775–5795.e15"],
    ["DOI / PMID", "10.1016/j.cell.2024.07.039 / 39214080"],
    ["论文配套数据版本", "cFMD v1.1.0（GitHub release tag v1.1.0）"],
    ["本报告使用版本", "cFMD v1.3.2（GitHub main，2026-06-18）"],
], columns=["项目", "内容"])
K.table(doc, ref, widths=[3.0, 12.4], font_size=9, header_size=9)
K.caption(doc, "表 1  文献与数据版本")

K.h2(doc, "1.2 使用的最新版总表")
K.para(doc, "cFMD 是一个持续更新的公开资源，仓库主分支已从论文时的 v1.1.0 迭代到 v1.3.2。"
            "v1.3.2 相对 v1.1.0 增加 50 个数据集、1,592 份样品、7,281 个 MAG，SGB 总数由 1,144 增至 1,654。"
            "早期版本把 SGB 汇总表（cFMD_sgbs_prokaryotic/eukaryotic）作为顶层文件提供，"
            "新版改为按数据集拆分的目录结构（cFMD_data/<dataset>/），SGB 级信息需要在样品级 MAG 清单上自行聚合。"
            "本次分析按新版结构重新构建了全部 SGB 级汇总，口径写在第三章。")
d2 = pd.DataFrame([
    ["cFMD_metadata.tsv", "样品级元数据：类别、发酵属性、国家、测序与组装统计", "4,125 行 × 32 列"],
    ["cFMD_mags_list.tsv", "MAG 清单：所属样品、SGB 归属、分类、完整度/污染度", "18,180 行 × 20 列"],
    ["cFMD_datasets.tsv", "数据集清单、Bioproject 号、加入版本", "109 行"],
    ["cFMD_data/<dataset>/<dataset>_taxonomic_profiles.tsv", "按数据集拆分的 MetaPhlAn4 物种谱", "107 个文件，4,067 份样品"],
    ["cFMD_data/<dataset>/<dataset>_{prok,euk}_mags_info.tsv", "按数据集拆分的 MAG 信息", "109 个数据集"],
    ["download_mags.sh", "官方 MAG 序列下载脚本（序列托管于 Zenodo）", "1 个"],
], columns=["文件", "内容", "规模"])
K.table(doc, d2, widths=[7.2, 6.2, 2.6], font_size=8.4)
K.caption(doc, "表 2  本报告使用的 cFMD v1.3.2 公开总表")

K.para(doc, "MAG 序列本身仍托管在 Zenodo，按数据集打包后合计超过 250 GB。本次分析只用总表，未下载序列，"
            "原因有两点：当前运行环境对 Zenodo 无出站访问权限，且本地磁盘不足以容纳序列集合。"
            "因此第六章的 antiSMASH 部分为基于分类学与文献的产物预判，运行脚本与输入清单随报告提供，"
            "在有 conda 与存储条件的服务器上补跑即可得到实测结果。")

K.h2(doc, "1.3 与论文版（v1.1.0）的差异")
K.para(doc, "两张表并排放，差异主要来自新增数据集，而不是口径调整。v1.3.2 的 109 个数据集中，"
            "59 个属于 v1.0.0（即论文所用）、26 个在 v1.2.1 加入、2 个在 v1.3.1、22 个在 v1.3.2。"
            "发酵相关类别的样品数从 2,262 增至 3,293，MAG 从 10,202 增至 15,446，增幅 51%。")
cmp = pd.DataFrame([
    ["样品数", "2,533", "4,125", "+1,592"],
    ["数据集", "59", "109", "+50"],
    ["国家", "50", "54", "+4"],
    ["测序碱基", "14.7 Tb", "25.09 Tb", "+10.4 Tb"],
    ["MAG 总数", "10,899", "18,180", "+7,281"],
    ["SGB 总数", "1,144（1,036 原核 + 108 真核）", "1,654（细菌 1,531 + 真核 110 + 古菌 13）", "+510"],
    ["发酵样品", "2,262", "3,293", "+1,031"],
    ["发酵样品 MAG", "10,202", "15,446", "+5,244"],
    ["发酵样品 SGB", "957", "1,142", "+185"],
    ["食品类型（type）层级数", "107", "149", "+42"],
], columns=["指标", "v1.1.0（论文配套）", "v1.3.2（本次）", "增量"])
K.table(doc, cmp, widths=[3.6, 5.4, 5.6, 1.6], font_size=8.4)
K.caption(doc, "表 3  两个版本的总量对比")

K.para(doc, "增量在不同类别之间很不均衡。乳制品新增 849 份样品、4,363 个 MAG，主要来自奶酪专项数据集"
            "（GardonH_2025、MagliuloR_2024、UNINA_SM_2025 等）；发酵种子类由 13 份增至 65 份，"
            "新增的几乎全是可可豆发酵（AlmeidaO_2020、LimaC_2020、MotaGutierrezJ_2021）；"
            "发酵鱼类由 5 份增至 25 份，新增的 20 份是中国的油茶（yucha）；发酵豆类由 16 份增至 26 份，"
            "新增为纳豆、豆豉一类的发酵大豆制品。")
cc = pd.DataFrame([
    ["乳制品", 1487, 2336, 6879, 11242, 535, 664],
    ["发酵饮料", 422, 456, 2011, 2144, 174, 183],
    ["发酵肉制品", 133, 168, 526, 607, 128, 142],
    ["发酵谷物制品", 80, 83, 225, 244, 97, 96],
    ["含酒精发酵饮料", 48, 48, 161, 161, 67, 67],
    ["发酵果蔬", 34, 62, 91, 149, 57, 74],
    ["发酵薯类与根茎", 24, 24, 123, 123, 76, 71],
    ["发酵豆类", 16, 26, 90, 172, 54, 82],
    ["发酵种子/油料", 13, 65, 64, 390, 40, 122],
    ["发酵鱼制品", 5, 25, 32, 214, 21, 98],
    ["合计", 2262, 3293, 10202, 15446, 957, 1142],
], columns=["类别", "样品 v1.1.0", "样品 v1.3.2", "MAG v1.1.0", "MAG v1.3.2", "SGB v1.1.0", "SGB v1.3.2"])
K.table(doc, cc, widths=[3.6, 1.9, 1.9, 1.9, 1.9, 1.7, 1.7], font_size=8.2)
K.caption(doc, "表 4  发酵类别在两版之间的变化",
          note="注：SGB 数在两版间不具严格可比性，因为 v1.2 之后 SGB 编号体系（MetaRefSGB）整体更新，同一物种的编号已改变。")

K.h2(doc, "1.4 与他人整理结果的核对")
K.para(doc, "按 v1.3.2 的 category 字段统计发酵样品，结果与外部整理的表逐行一致：乳制品 2,336 份 / 48 个数据集，"
            "发酵饮料 456 / 10，发酵肉 168 / 9，发酵谷物 83 / 6，发酵种子 65 / 5，发酵果蔬 62 / 6，"
            "含酒精饮料 48 / 6，发酵豆类 26 / 7，发酵鱼 25 / 2，发酵薯类与根茎 24 / 2。"
            "十个类别的数据集数相加为 101，而全库发酵数据集为 87，差值来自一个数据集同时覆盖多个类别"
            "（如 LeechJ_2020 同时含发酵肉、发酵果蔬、发酵鱼与发酵谷物样品）。"
            "乳制品出现 2,336 条记录、2,335 个唯一 sample_id，是因为同一 sample_id 出现在两个数据集下，"
            "查询时应以 dataset_name + sample_id 作为唯一键。")
K.para(doc, "此前若按论文版 v1.1.0 统计，同样十个类别只有 2,262 份样品、87 个数据集，乳制品只有 1,487 份，"
            "总量约少 31%。凡是用 v1.1.0 表的整理结果，与用最新表的整理结果对不上，基本都是版本差异，不是口径差异。"
            "本报告全部数字基于 v1.3.2，可与最新版仓库直接复核。")

# ============================================================ 二
K.h1(doc, "二、数据库总体情况", page_break=True)
d3 = pd.DataFrame([
    ["食品宏基因组样品", "4,125", "发酵 3,293、非发酵 832"],
    ["其中：新测序 / 公共数据", "1,986 / 2,139", "按仓库 Version 字段统计"],
    ["数据集", "109", "v1.0.0 59、v1.2.1 26、v1.3.1 2、v1.3.2 22"],
    ["国家", "54", "意大利、西班牙、爱尔兰居前三"],
    ["测序碱基总量", "25.09 Tb", "乳制品占 17.6 Tb"],
    ["MAG 总数", "18,180", "细菌 17,048、真核 979、古菌 17、未定 136"],
    ["通过质量过滤的 MAG", "17,965", "完整度 ≥50% 且污染 <5%"],
    ["成功归属 SGB 的 MAG", "17,723", "未归属 457（321 原核 + 136 真核）"],
    ["纳入分析集", "17,621", "质量与 SGB 归属同时满足"],
    ["SGB 总数", "1,654", "细菌 1,531、真核 110、古菌 13"],
    ["　已知种（kSGB）", "1,054", "含至少一个参考基因组"],
    ["　未知种（uSGB）", "374", "仅由重建基因组构成"],
    ["　食品新种（ufSGB）", "226", "仅见于食品样品"],
    ["发酵样品", "3,293（79.8%）", "87 个数据集、53 个国家"],
    ["发酵样品 MAG", "15,446（85.0%）", "原核 14,598、真核 848"],
], columns=["指标", "数值", "说明"])
K.table(doc, d3, widths=[4.6, 3.6, 7.2], font_size=8.5)
K.caption(doc, "表 5  cFMD v1.3.2 总体指标")

K.para(doc, "结构上最值得注意的是新颖性：1,654 个 SGB 中有 600 个不含任何参考基因组（36.3%），"
            "其中 226 个只在食品样品中出现。这一部分正是发酵食品微生物组相对临床与环境样本库的主要增量。"
            "与 v1.1.0 相比，ufSGB 的绝对数从 290 降到 226，原因是 MetaRefSGB 在 2025 年更新后，"
            "原先无参考基因组的若干食品类群已被新发表的基因组覆盖，转为 kSGB；这是数据库进步的表现，不是数据缩水。")
K.figure(doc, f"{F}/fig6_SGB新颖性.png", 9.6)
K.caption(doc, "图 1  食品 MAG 所属 SGB 的新颖性构成（n = 1,654）")

# ============================================================ 三
K.h1(doc, "三、分析口径与分组规则")
K.para(doc, "全部统计遵循以下五条规则，表格与图件均按此口径生成。")
K.numbered(doc, [
    "发酵属性直接取自元数据 fermented 字段（F / NF），不根据类别名反推。乳制品中另有 203 份非发酵样品"
    "（鲜奶 132、奶酪盐水 53、生乳 18），其中 189 份有可用的物种谱，与发酵乳制品在第四章第四节做同基质对照。",
    "食品类别按 category（15 类）划分，共 149 个 type。发酵相关类别 10 个，另有 probiotics、meat、fish、"
    "fruits_and_vegetables、other 五个非发酵类别。",
    "MAG 质量按 CheckM 分级：完整度 ≥90% 且污染 <5% 记 HQ，完整度 50%–90% 且污染 <5% 记 MQ。"
    "v1.3.2 放宽了入库门槛，全库有 215 个 MAG 不满足该条件（53 个完整度 <50%、214 个污染 ≥5%，两类有交叉），"
    "分析时剔除。",
    "SGB 归属以 MAG 清单中的 SGB_id 为准。457 个 MAG 的 SGB_id 为空（SGB_assignment 为 "
    "unassigned_prokaryote 或 unassigned_eukaryote），多为高污染或嵌合分箱，分析时剔除。"
    "剔除后进入分析的 17,621 个 MAG 占全库 96.9%。SGB 的新颖性类型（kSGB / uSGB / ufSGB）在源表中按 MAG 标注，"
    "有 21 个 SGB 的 MAG 分别标为 uSGB 与 ufSGB，本报告按该 SGB 内多数 MAG 的标注统一归类，票数相同时取 uSGB，"
    "以保证每个 SGB 只计入一类。",
    "SGB 是物种水平聚类单元，同一 SGB 的多个 MAG 代表同一物种的不同菌株。基因组层面分析（如 antiSMASH）"
    "按 SGB 去重，每 SGB 取完整度最高、污染最低的一株作代表。",
])

# ============================================================ 四
K.h1(doc, "四、发酵种类模块", page_break=True)
K.h2(doc, "4.1 总体分布")
K.para(doc, "3,293 份发酵样品共产生 15,446 个 MAG，其中原核 14,598 个、真核 848 个；高质量 7,431 个（48.1%），"
            "中等质量 8,015 个。这些 MAG 分属 1,142 个 SGB，包括 749 个已知种、244 个未知种与 149 个食品新种。"
            "乳酸菌相关 23 个属合计 8,183 个 MAG，占发酵样品原核 MAG 的 56.1%，仍是绝对主体。")
K.para(doc, "十个发酵类别的分布依然高度不均：乳制品独占 72.8% 的 MAG，发酵饮料 13.9%，两者合计接近九成。"
            "但与 v1.1.0 相比，长尾类别的代表性明显改善——发酵种子从 64 个 MAG 增至 390 个（+509%），"
            "发酵鱼从 32 增至 214（+569%），发酵豆类从 90 增至 172（+91%）。这几个类别在论文版中样本过少、"
            "无法单独成论，现在可以给出可信度更高的描述。")
cols = ["发酵类别", "样品数", "数据集数", "国家数", "MAG总数", "原核MAG", "真核MAG",
        "高质量MAG(HQ)", "SGB总数", "已知种SGB(kSGB)", "食品新种SGB(ufSGB)", "属数", "已定名种数"]
disp = s10[cols].copy()
disp.columns = ["发酵类别", "样品", "数据集", "国家", "MAG", "原核", "真核", "HQ", "SGB", "kSGB", "ufSGB", "属", "种"]
K.table(doc, disp, widths=[2.5, 1.05, 1.0, 0.95, 1.15, 1.05, 1.05, 1.0, 1.0, 1.15, 1.25, 0.8, 0.9], font_size=8)
K.caption(doc, "表 6  各发酵食品类别的 MAG 与 SGB 数量（cFMD v1.3.2）",
          note="注：HQ 指完整度 ≥90%、污染 <5%；kSGB 为已知种，ufSGB 为仅见于食品样品的新种 SGB。")

K.figure(doc, f"{F}/fig1_类别MAG数量.png", 15.0)
K.caption(doc, "图 2  各发酵食品类别重建的 MAG 数量与质量分布")

K.h2(doc, "4.2 各发酵类别的菌群构成")
K.para(doc, "以下按类别给出主导菌群。样品量小于 30 的类别（发酵薯类、发酵豆类、发酵鱼制品）只作趋势描述，"
            "不据此下结论。")

K.h2(doc, "（1）乳制品：2,336 份样品，11,242 个 MAG")
K.para(doc, "乳制品是资源最厚的部分，来自 48 个数据集、37 个国家，占全库发酵 MAG 的 72.8%。"
            "主导菌为 Lactococcus lactis（940 个 MAG）、Streptococcus thermophilus（802 个）、"
            "Lacticaseibacillus paracasei（716 个）、Lactococcus cremoris（490 个）、Lactobacillus delbrueckii（474 个）"
            "与 Lactobacillus helveticus（405 个），对应嗜温、嗜热两条发酵剂路线与酸奶、瑞士型奶酪两类工艺。"
            "奶酪表面成熟带来的 Brevibacterium（492 个）、Corynebacterium（261 个）、Brachybacterium（226 个）"
            "构成乳制品独有的组成。真核部分以 Debaryomyces hansenii（141 个）与 Penicillium roqueforti（38 个）为主。")
K.para(doc, "乳制品的样品量与 MAG 数在 v1.3.2 中增幅最大（+849 份、+4,363 个），主要来自奶酪专项："
            "GardonH_2025、MagliuloR_2024、UNINA_SM_2025 三个数据集合计贡献约 2,300 个 MAG。"
            "SGB 数由 535 增至 664，其中 313 个不含参考基因组（47.1%），说明即便研究最充分的乳制品，"
            "仍有大量未培养类群只以 MAG 形式存在。")

K.h2(doc, "（2）发酵饮料：456 份样品，2,144 个 MAG")
K.para(doc, "该类以水开菲尔为主体（388 份，占 85%），其余为康普茶（30 份）、韩国米醋（21 份）、咖啡发酵（6 份）、"
            "Pulque（5 份）、Pozol（4 份）。菌群由三部分叠加：Liquorilactobacillus（433 个）、"
            "Lacticaseibacillus（251 个）、Leuconostoc（163 个）构成乳酸菌骨架，Acetobacter（259 个）承担"
            "乙醇到乙酸的氧化，Zymomonas mobilis（109 个）在棕榈酒等含糖汁液中主导乙醇发酵。"
            "物种谱上，Zymomonas mobilis 平均占 12.2%、Liquorilactobacillus satsumensis 10.9%。"
            "真核占 11.2%，以 Saccharomyces cerevisiae 为主。")

K.h2(doc, "（3）发酵肉制品：168 份样品，607 个 MAG")
K.para(doc, "以萨拉米（80 份）与肉糜灌肠（69 份）为主，来自意大利、西班牙、瑞士、葡萄牙、希腊、摩洛哥 6 国、9 个数据集。"
            "主导菌为 Staphylococcus xylosus、Latilactobacillus sakei、Latilactobacillus curvatus（属水平 219 个 MAG），"
            "符合硝酸盐还原、脂质氧化与酸化的成熟工艺。物种谱上 Latilactobacillus sakei 平均占 36.6%，"
            "是该类别的绝对优势种。真核占 8.2%，以 Debaryomyces hansenii 与 Penicillium nalgiovense 为代表。")

K.h2(doc, "（4）发酵谷物制品：83 份样品，244 个 MAG")
K.para(doc, "以酸面团（40 份）为主，其余为西非与东非传统谷物料：Ogi（12 份）、Kunu（6 份）、Ugi（4 份）、"
            "Injera（2 份）等，覆盖 13 个国家。主导种为 Lactiplantibacillus plantarum、Fructilactobacillus sanfranciscensis、"
            "Levilactobacillus brevis 与 Limosilactobacillus fermentum，与酸面团中酵母—乳酸菌共生体系一致。"
            "物种谱上 Lactiplantibacillus plantarum 占 12.8%、Levilactobacillus brevis 8.8%、"
            "Fructilactobacillus sanfranciscensis 8.6%。")

K.h2(doc, "（5）含酒精发酵饮料：48 份样品，161 个 MAG")
K.para(doc, "葡萄酒（20 份，霞多丽葡萄醪）、兰比克啤酒（7 份）、棕榈酒（6 份）、中国白酒与非洲小米酒（各 3 份）等。"
            "真核占 44.7%，为各类别中最高。Saccharomyces cerevisiae 在物种谱中平均占 41.0%，"
            "Lactobacillus isalae、Pediococcus damnosus 承担苹果酸—乳酸发酵。该类别的分析价值主要在酵母与乳酸菌互作，"
            "而非细菌多样性。")

K.h2(doc, "（6）发酵薯类与根茎：24 份样品，123 个 MAG")
K.para(doc, "木薯制品（Gari 5 份、Fufu 4 份、Lafun 3 份、Otiru 1 份）与腌萝卜、芜菁、姜等根茎类，来自 6 国、2 个数据集。"
            "Limosilactobacillus fermentum 在物种谱中占 10.8%、Lactobacillus delbrueckii 8.8%，属数达 40，"
            "每样品平均 5.12 个 MAG，是 MAG 产出效率最高的类别。样本量小但地理来源分散，适合做传统发酵食品的"
            "地域特异性分析。")

K.h2(doc, "（7）发酵果蔬：62 份样品，149 个 MAG")
K.para(doc, "盐水发酵蔬菜（18 份）、葡萄醪（10 份）、酸菜（9 份）、红椒酱（8 份）、泡菜（5 份）等，来自 10 国。"
            "Lactiplantibacillus plantarum（属水平 298 个 MAG）、Levilactobacillus brevis、Lactobacillus acetotolerans "
            "为主。该类样品中植物来源的 Cutibacterium、Pantoea 等同时存在，反映发酵初期与终产品之间的差异。"
            "样品量在 v1.3.2 中由 34 份增至 62 份，新增主要来自 brine_fermented_vegetables 与 grape_must。")

K.h2(doc, "（8）发酵豆类：26 份样品，172 个 MAG")
K.para(doc, "基质全部为大豆：中国酱油盐水与豆酱、尼泊尔 Kinema、印尼天贝、印度与马来西亚的发酵大豆制品，来自 5 国、7 个数据集。"
            "Weissella confusa 在物种谱中占 13.8%，Enterococcus faecium 4.6%，Bacillus 属亦有分布。"
            "样品量由 16 份增至 26 份，MAG 由 90 增至 172，属数 51，是长尾类别中改善最明显的一个。")

K.h2(doc, "（9）发酵种子与油料：65 份样品，390 个 MAG")
K.para(doc, "该类在 v1.3.2 中变化最大：由 13 份增至 65 份，MAG 由 64 增至 390。构成上以可可豆发酵（43 份）为主体，"
            "另有芥菜籽（9 份）与非洲角豆制品（Iru 6 份、Ugba 3 份、Okpehe 2 份）。"
            "物种谱上 Acetobacter pasteurianus 平均占 27.8%，是可可发酵的特征菌；"
            "Lactiplantibacillus plantarum 7.5%。这一类别此前被非洲角豆类制品主导，现在更适合作为可可发酵的参考集，"
            "与巧克力风味的微生物学基础直接相关。")

K.h2(doc, "（10）发酵鱼制品：25 份样品，214 个 MAG")
K.para(doc, "由韩国的洪鱼（skate_fish，5 份）与中国的油茶（yucha，20 份）两个数据集构成。"
            "此前该类只有 5 份洪鱼样品、32 个 MAG，结论极不稳定；现在 MAG 增至 214、SGB 98 个，"
            "其中 74 个已知种。物种谱上 Limosilactobacillus fermentum 16.2%、Lactiplantibacillus plantarum 14.4%，"
            "洪鱼特有的 Psychrobacter maritimus 占 6.4%。")

K.h2(doc, "4.3 优势属与优势种")
K.para(doc, "图 3 给出前 22 个属在 10 个类别中的 MAG 数量，可以清楚看到三条分带：第一带为 Lactococcus、"
            "Lactobacillus、Streptococcus、Lacticaseibacillus、Leuconostoc，集中在乳制品与发酵饮料；"
            "第二带为 Staphylococcus、Latilactobacillus、Brevibacterium、Corynebacterium，集中在发酵肉与乳制品表面；"
            "第三带为 Bacillus、Weissella、Enterococcus、Pediococcus，出现在发酵种子与发酵豆类。"
            "与 v1.1.0 相比，Acetobacter 在发酵种子中的占比显著上升（48 个 MAG），对应新纳入的可可豆发酵。")
K.figure(doc, f"{F}/fig2_优势属热图.png", 14.2)
K.caption(doc, "图 3  发酵食品中优势菌属的 MAG 数量分布（前 22 属，数值为 MAG 数）")

K.para(doc, "种水平前 15 位为：Lactococcus lactis（940）、Streptococcus thermophilus（802）、"
            "Lacticaseibacillus paracasei（716）、Lactococcus cremoris（490）、Lactobacillus delbrueckii（474）、"
            "Lactobacillus helveticus（405）、Leuconostoc mesenteroides（352）、Brevibacterium aurantiacum（246）、"
            "Staphylococcus equorum（240）、Lactiplantibacillus plantarum（232）、Liquorilactobacillus satsumensis（200）、"
            "Leuconostoc falkenbergense（197）、Saccharomyces cerevisiae（194）、Corynebacterium casei（153）、"
            "Latilactobacillus curvatus（152）。")
K.para(doc, "前六位全部是发酵剂核心菌，且 MAG 数远超第七位，这与“人工接种 + 强选择”的生产方式相符："
            "发酵剂菌株以极高丰度存在，组装时更容易获得完整基因组。直接用 MAG 数量代表物种重要性，"
            "会系统性高估发酵剂、低估非接种的背景菌群。这一偏倚在 v1.3.2 中因乳制品权重上升而被进一步放大。")

K.h2(doc, "4.4 与同基质非发酵样品的对照")
K.para(doc, "v1.3.2 大幅扩充了非发酵对照：肉 204 份、鱼 155 份、果蔬 237 份，比 v1.1.0 分别多 157、141、212 份；"
            "其中有物种谱、能进入多样性计算的为 197、150、231 份。"
            "物种水平 Shannon 指数上，发酵样品的多样性低于同基质生样，肉制品与果蔬差异显著（P<0.001），"
            "乳制品与鱼类未达显著。乳制品不显著有其原因：非发酵乳样品本身就是生乳，菌群简单且与发酵乳的起始菌群重叠，"
            "二者的 Shannon 差异因此被稀释；鱼类则受样本来源差异影响（发酵侧以洪鱼、油茶为主，非发酵侧为海水鱼）。")
K.table(doc, pair, widths=[3.4, 1.9, 1.6, 2.6, 2.6, 1.6], font_size=8.5)
K.caption(doc, "表 7  同基质条件下发酵与非发酵样品的 alpha 多样性比较",
          note="注：Shannon 指数基于 MetaPhlAn4 物种水平相对丰度计算；P 值为 Mann-Whitney U 检验（双尾）。")

K.para(doc, "物种层面的升与降更能说明问题。全库范围内，发酵组相对非发酵组富集最多的是 Lactococcus lactis"
            "（14.02% 对 1.43%）、Streptococcus thermophilus（15.75% 对 4.33%）、Lactococcus cremoris（9.69% 对 0.65%）；"
            "下降最多的是 Brochothrix thermosphacta（0.42% 对 4.57%）、Pseudomonas fragi（0.13% 对 3.74%）、"
            "Psychrobacter immobilis（0.27% 对 3.07%）与 Pseudomonas paraversuta（0.12% 对 2.62%）。"
            "肉制品中 Latilactobacillus sakei 由 0.39% 升至 36.6%，同时热杀索丝菌由 15.4% 降至 6.9%，"
            "发酵对腐败菌群的抑制在物种层面清晰可见。")
K.figure(doc, f"{F}/fig4_alpha多样性.png", 15.0)
K.caption(doc, "图 4  各食品类别的物种水平 alpha 多样性（蓝色为发酵类别，棕色为非发酵类别）")

K.h2(doc, "4.5 真核微生物部分")
K.para(doc, "848 个真核 MAG 分布在 97 个 SGB 中。属水平以 Saccharomyces（196 个）、Debaryomyces（146 个）、"
            "Penicillium（87 个）、Kluyveromyces（54 个）、Hanseniaspora（42 个）、Pichia（42 个）、Scopulariopsis（40 个）为主。"
            "种水平以 Saccharomyces cerevisiae（194 个）、Debaryomyces hansenii（141 个）、Penicillium roqueforti（38 个）、"
            "Scopulariopsis brevicaulis（36 个）、Kluyveromyces marxianus 与 K. lactis（各 27 个）、"
            "Hanseniaspora opuntiae（26 个）、Penicillium camemberti（24 个）为代表。")
K.para(doc, "真核的类别分布与细菌明显不同：含酒精饮料 44.7%、发酵种子 7.7%、发酵饮料 11.2%、发酵肉 8.2%，"
            "而乳制品仅 3.8%。奶酪中的真菌种类虽少但功能关键，Penicillium 属的次级代谢产物直接决定蓝纹与白霉奶酪的"
            "风味与安全性，这一点在第六章讨论。")
K.figure(doc, f"{F}/fig5_真核组成.png", 14.2)
K.caption(doc, "图 5  发酵食品真核 MAG 的属组成（前 12 属）")

# ============================================================ 五
K.h1(doc, "五、益生菌模块", page_break=True)
K.h2(doc, "5.1 四个口径")
K.para(doc, "益生菌在 cFMD 里不是一个字段，而是几组互不相同的口径。口径不同，数量差一个数量级，"
            "先定边界再谈数量。")
tier = pd.read_csv(f"{T}/22_益生菌分层汇总.csv", encoding="utf-8-sig")
tier["定义"] = ["属级放宽：18 个乳杆菌相关属 + 双歧杆菌属", "种级名单：QPS、ISAPP、国内保健食品菌种名单",
              "QPS/发酵剂相关：明串珠菌、片球菌、芽孢杆菌、酵母等", "条件致病，筛选时应排除",
              "元数据 probiotics 类别（14 份样品）"]
tier["层级"] = ["A 宽口径：乳酸菌与双歧杆菌类群", "A 严格：名单内益生菌种", "B：QPS/发酵剂相关种",
              "C：需谨慎（肠球菌等）", "益生菌制剂样品"]
tier = tier[["层级", "定义", "种数", "SGB数", "MAG数", "HQ数"]]
K.table(doc, tier, widths=[4.5, 6.4, 1.2, 1.4, 1.6, 1.4], font_size=8.2)
K.caption(doc, "表 8  益生菌相关 MAG 的四个口径", note="注：发酵样品为分母，制剂样品单独成类，四组互不包含。")

K.numbered(doc, [
    "益生菌制剂样品。probiotics 是元数据中的独立类别，14 份样品来自 PatroJN_2016（美国 10 份）与 "
    "PasolliE_2020（意大利 4 份），共 42 个 MAG、21 个 SGB。这是唯一能确认“菌株来自益生菌产品”的集合。",
    "名单内益生菌种。按 EFSA 安全资格认定（QPS）、ISAPP 共识[3,4]与《可用于保健食品的益生菌菌种名单》"
    "整理出 39 个种名，在发酵样品中出现 28 个，对应 28 个 SGB、4,925 个 MAG（HQ 1,968）。这一层只认种名，"
    "不含属级推断。",
    "乳酸菌与双歧杆菌类群。把 18 个乳杆菌相关属与双歧杆菌属整体纳入，得到 133 个种、134 个 SGB、"
    "6,385 个 MAG（HQ 2,879）。其中大量是发酵剂菌株与背景菌，只能作对照集。",
    "另两层用于排除。B 层为 QPS 或发酵剂相关种（明串珠菌、片球菌、芽孢杆菌、酵母等）76 种、80 个 SGB、"
    "1,869 个 MAG；C 层为肠球菌等条件致病类群，31 种、32 个 SGB、292 个 MAG。",
])
K.para(doc, "回到问题本身：益生菌当然是微生物 MAG 的一部分，它们在 cFMD 中与乳制品、发酵肉等类别同质，"
            "同样经过组装、分箱与质量评估，可以直接进入同一套分析。可以放心用于益生菌分析的是两层："
            "制剂来源 42 个，名单内种 4,925 个，合计 4,967 个。6,385 这个数被引用得最多，但它对应第三层口径，"
            "比严格口径多 30%，写进结论时需要注明。")

K.h2(doc, "5.2 益生菌制剂来源的 MAG")
K.para(doc, "42 个 MAG 分属 21 个 SGB。物种构成为 Lactiplantibacillus plantarum（7 个）、Lactobacillus acidophilus（5 个）、"
            "Lacticaseibacillus rhamnosus（4 个）、Bifidobacterium animalis 与 Lacticaseibacillus paracasei（各 3 个），"
            "Bifidobacterium breve、Bifidobacterium longum、Ligilactobacillus salivarius、Limosilactobacillus reuteri"
            "（各 2 个），其余 12 个种各 1 个。")
K.para(doc, "质量上，42 个 MAG 的平均完整度 76.7%，低于发酵食品整体的 83.5%；HQ 仅 16 个，MQ 26 个。"
            "原因在于制剂样品中菌株种类少、每种菌的相对丰度受配方比例限制，且辅料（麦芽糊精、微晶纤维素）DNA 比例高，"
            "组装时覆盖度分布不均。做下游分析时建议优先取 HQ 的 16 个。")
ps = probmag.groupby("物种").agg(MAG=("MAG_id", "size"),
                                 HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                                 最高完整度=("completeness", "max")).reset_index()
ps["最高完整度"] = ps["最高完整度"].round(1)
ps = ps.sort_values(["MAG", "HQ"], ascending=False)
ps.columns = ["物种", "MAG数", "HQ数", "最高完整度%"]
K.table(doc, ps, widths=[7.4, 1.6, 1.4, 2.6], font_size=8.4)
K.caption(doc, "表 9  益生菌制剂来源的 MAG（42 个，21 个 SGB）",
          note="注：完整度与污染度由 CheckM 估计；逐条 MAG 编号见附表 05。")

K.h2(doc, "5.3 名单内益生菌种在发酵食品中的分布")
K.para(doc, "4,925 个 MAG 在类别上的集中度比预想更高：乳制品 4,124 个，占 83.7%；发酵饮料 425 个，"
            "发酵谷物 105 个，发酵种子 69 个，发酵薯类 45 个，发酵肉与含酒精饮料各 41 个，发酵鱼 32 个，"
            "其余类别合计不足 50 个。乳制品之外，名单内物种多以辅助菌或污染菌的形式出现，丰度低、MAG 数少。")
strict = pd.read_csv(f"{T}/21_益生菌严格名单MAG表.csv", encoding="utf-8-sig")
sc = strict.groupby("物种").agg(MAG=("MAG_id", "size"),
                               HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                               SGB=("SGB_id", "nunique"),
                               主要来源=("发酵类别中文", lambda x: x.value_counts().index[0]))
sc = sc.sort_values("MAG", ascending=False).reset_index()
sc.columns = ["物种", "MAG数", "HQ数", "SGB数", "主要来源"]
K.table(doc, sc, widths=[6.2, 1.7, 1.4, 1.3, 3.4], font_size=8.5)
K.caption(doc, "表 10  名单内 28 个益生菌种在发酵食品中的分布",
          note="注：种级名单共 39 个种名，数据中出现 28 个；逐条 MAG 编号见附表 21。")

K.h2(doc, "5.4 名单之外的乳酸菌类群")
K.para(doc, "133 个种里 105 个不在名单内。这些种不是随机分布，而是集中在两类基质上：水开菲尔与康普茶来源的"
            "Liquorilactobacillus satsumensis（200 个）、L. nagelii（129 个）、Lentilactobacillus hilgardii（76 个）、"
            "Bifidobacterium aquikefiri（73 个），以及奶酪与发酵肉来源的 Lentilactobacillus parabuchneri（136 个）、"
            "Lactobacillus kefiranofaciens（89 个）、Companilactobacillus versmoldensis（40 个）。"
            "前者是传统发酵饮料的特有菌群，后者多为二次发酵或成熟过程的参与者，两者都缺少系统的益生功能评价，"
            "也都不在监管名单上。这一部分反而是该资源最有增量的地方：名单是静态的，菌群不是。")
nl = tab6[~tab6["物种"].isin(strict["物种"].unique())]
core = nl.groupby("物种").agg(MAG=("MAG_id", "size"), HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                              SGB=("SGB_id", "nunique"), 主要来源=("发酵类别中文", lambda x: x.value_counts().index[0]))
core = core.sort_values("MAG", ascending=False).head(18).reset_index()
core.columns = ["物种", "MAG数", "HQ数", "SGB数", "主要来源"]
K.table(doc, core, widths=[6.2, 1.7, 1.4, 1.3, 3.4], font_size=8.5)
K.caption(doc, "表 11  名单之外的乳酸菌与双歧杆菌种（前 18 位）")

K.para(doc, "图 6 的矩阵把这种分工显示得更清楚：Lactococcus lactis 与 Streptococcus thermophilus 几乎只出现在乳制品，"
            "Liquorilactobacillus satsumensis 的 200 个 MAG 全部来自发酵饮料，Lacticaseibacillus paracasei 则一分为二，"
            "乳制品 461 个、发酵饮料 249 个。用类别×物种的矩阵可以很快判断一个种是“某类基质的专性成员”还是“跨基质的通才”。")
K.figure(doc, f"{F}/fig3_益生菌物种热图.png", 14.0)
K.caption(doc, "图 6  乳酸菌与双歧杆菌类群在各类发酵食品中的 MAG 数量（前 20 位）")

K.para(doc, "双歧杆菌值得单独说明。全库 Bifidobacterium 共 192 个 MAG，仍以食品来源的 Bifidobacterium aquikefiri、"
            "B. psychraerophilum、B. mongoliense 为主，临床常用的 B. longum、B. animalis 数量有限。"
            "这与双歧杆菌主要栖居于肠道、在食品中多为外源添加的生态特征一致，也意味着用该资源做双歧杆菌"
            "益生性研究时样本不足。")
K.para(doc, "跨版本比较要按同一口径做。v1.1.0 的严格名单同样是 28 个种，MAG 为 2,884 个，v1.3.2 增至 4,925 个；"
            "SGB 却由 30 降到 28。MAG 增加来自新增数据集，SGB 减少是 MetaRefSGB 重新划分的结果。"
            "如果拿 v1.1.0 的 28 个种去对比 v1.3.2 的 133 个种，得到的是口径差，不是数据变化。")

K.h1(doc, "六、antiSMASH 次级代谢产物分析", page_break=True)
K.h2(doc, "6.1 方法与输入")
K.para(doc, "antiSMASH 是目前覆盖最全的次级代谢产物基因簇（BGC）识别工具，8.0 版可识别 101 类簇，"
            "包含细菌素、羊毛硫肽、NRPS、PKS、萜类、铁载体等与发酵食品高度相关的类别[7]。"
            "本次未能实际运行，原因见 1.2 节；以下给出输入口径、参数、预期结果与关联分析框架。")
K.para(doc, "输入按 SGB 去重，每个 SGB 取完整度最高、污染最低的一株代表，共 1,142 个（原核 1,045 个、真核 97 个），"
            "比 v1.1.0 的 957 个增加 19%。去重是必要的：同一 SGB 内不同 MAG 的 BGC 组成通常只差几个单核苷酸变异，"
            "全量运行 15,446 个基因组既浪费算力，也会因近重复序列造成 BGC 家族计数的偏倚。")
t8 = pd.DataFrame([
    ["原核代表基因组", "1,045", "完整度中位 88.4%，HQ 占 47%"],
    ["真核代表基因组", "97", "以 Saccharomyces、Debaryomyces、Penicillium 为主"],
    ["运行参数（细菌）", "antiSMASH 8.0.4", "--genefinding-tool prodigal --cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go"],
    ["运行参数（真菌）", "antiSMASH 8.0.4", "--taxon fungi --genefinding-tool prodigal-m --cb-general --cb-knownclusters"],
    ["单基因组耗时", "3–8 min（16 线程）", "真菌基因组较大，10–20 min"],
    ["总耗时估算", "45–90 CPU·h", "20 并发约 4–6 h"],
], columns=["项目", "设置", "说明"])
K.table(doc, t8, widths=[3.6, 3.4, 8.8], font_size=8.5)
K.caption(doc, "表 12  antiSMASH 运行配置")

K.h2(doc, "6.2 已知产物对应关系")
K.para(doc, "在拿到实测结果之前，可以按分类单元预先判断会检出什么。表 13 与表 14 整理了本资源中 MAG 数量较多的"
            "类群、其已被文献报道的 BGC 类型与代表化合物，同时给出该类群在发酵食品中的功能角色。"
            "这两张表的作用是给实测结果提供核对基准：若某属的实测簇类型与表中预期完全不符，应先检查注释或分箱质量。")

short = {"Alvarez-Sieiro2016": "Alvarez-Sieiro 2016", "Cotter2013": "Cotter 2013",
         "McAuliffe2001": "McAuliffe 2001", "Zacharof2012": "Zacharof 2012",
         "Diep2007": "Diep 2007", "Talarico1988": "Talarico 1988", "Ross2001": "Ross 2001",
         "Hugas1998": "Hugas 1998", "Rodriguez1997": "Rodríguez 1997", "Franz2007": "Franz 2007",
         "Martinez2013": "Martínez 2013", "Westermann2017": "Westermann 2017",
         "Gwenzietal2010": "Gwenzietal 2010", "Harwood2018": "Harwood 2018",
         "Kaspar2019": "Kaspar 2019", "Caulier2019": "Caulier 2019", "Rabbee2019": "Rabbee 2019",
         "Honda2018": "Honda 2018", "Hyronimus1998": "Hyronimus 1998",
         "Schoenfelder2019": "Schoenfelder 2019", "Wilson2019": "Wilson 2019",
         "Gross2007": "Gross 2007", "Weller2007": "Weller 2007", "Williamson2006": "Williamson 2006",
         "Schwibbert2011": "Schwibbert 2011", "Leclercq2014": "Leclercq 2014",
         "Irlinger2015": "Irlinger 2015", "Gullo2013": "Gullo 2013", "He2014": "He 2014",
         "Bakermans2012": "Bakermans 2012", "Coton2021": "Coton 2021", "O'Brien2006": "O'Brien 2006",
         "Nielsen2005": "Nielsen 2005", "Frisvad2015": "Frisvad 2015", "Rank2011": "Rank 2011",
         "Desjardins2006": "Desjardins 2006", "Jennessen2005": "Jennessen 2005"}


def bgc_table(names):
    b = bgc[bgc["分类单元"].isin(names)][["分类单元", "发酵食品MAG数", "antiSMASH可识别区域类型",
                                      "代表性已知产物", "对发酵过程的作用", "依据文献"]].copy()
    b.columns = ["分类单元", "MAG数", "可识别簇类型", "代表产物", "在发酵中的作用", "依据"]
    b["依据"] = [short.get(str(x).split(";")[0].strip(), str(x).split(";")[0].strip()) for x in b["依据"]]
    order = {n: i for i, n in enumerate(names)}
    b["_o"] = b["分类单元"].map(order)
    return b.sort_values("_o").drop(columns="_o")


LAB_SEL = ["Lactococcus", "Lactococcus lactis", "Lactobacillus", "Lactobacillus helveticus",
           "Lactobacillus delbrueckii", "Lacticaseibacillus", "Lactiplantibacillus plantarum",
           "Leuconostoc", "Pediococcus", "Latilactobacillus sakei", "Limosilactobacillus",
           "Streptococcus thermophilus", "Bifidobacterium", "Propionibacterium freudenreichii"]
K.table(doc, bgc_table(LAB_SEL), widths=[3.5, 1.2, 3.3, 4.0, 3.7, 2.3], font_size=7.3, header_size=7.6)
K.caption(doc, "表 13  乳酸菌相关类群的 BGC 类型与已知产物",
          note="注：产物为已被实验验证的代表化合物，不代表本资源中每一株都能检出；完整 50 行见附表 17。")

OTH_SEL = ["Bacillus", "Bacillus subtilis", "Staphylococcus", "Enterococcus", "Weissella",
           "Brevibacterium", "Pseudomonas", "Penicillium roqueforti", "Scopulariopsis"]
K.para(doc, "非乳酸菌类群与真菌的簇型结构完全不同，单列于表 14。芽孢杆菌与假单胞菌以 NRPS/PKS 为主，"
            "青霉属则以生物碱与聚酮为主，这两类正是发酵食品中产物发现与安全风险的两个集中点。")
K.table(doc, bgc_table(OTH_SEL), widths=[3.5, 1.2, 3.3, 4.0, 3.7, 2.3], font_size=7.3, header_size=7.6)
K.caption(doc, "表 14  非乳酸菌类群与真菌的 BGC 类型与已知产物")

K.h2(doc, "6.3 预期 BGC 规模")
K.para(doc, "按各属已报道的单基因组 BGC 数量区间，结合本资源的 SGB 数，可以估算工作量与产出规模。"
            "原核部分预期 1,461–4,554 个 BGC，真核部分 315–878 个。乳酸菌类群虽然基因组小，但簇密度不低，"
            "且高度集中在细菌素与羊毛硫肽两类；Bacillus 与 Pseudomonas 的单基因组簇数最多，是 NRPS/PKS 类新产物的主要来源。"
            "与 v1.1.0 的估算（1,185–3,695）相比增加约 23%，主要来自乳制品与发酵种子两类新增的 SGB。")
w = work.head(12)[["属", "SGB数", "单基因组BGC预期下限", "单基因组BGC预期上限",
                   "预期BGC总数(下限)", "预期BGC总数(上限)", "预期主要簇类型"]].copy()
w.columns = ["属", "SGB数", "单株下限", "单株上限", "合计下限", "合计上限", "主要簇类型"]
K.table(doc, w, widths=[3.4, 1.2, 1.5, 1.5, 1.6, 1.6, 5.4], font_size=8)
K.caption(doc, "表 15  主要属的预期 BGC 数量（前 12 属）",
          note="注：单株区间取自文献报道的同属基因组统计值，仅用于估算工作量，不作为实测结果。")

K.h2(doc, "6.4 与发酵过程和益生菌功能的关联")
K.para(doc, "antiSMASH 的结果要与发酵、益生菌挂钩，需要落在三条具体的线索上，而不是泛泛地统计簇的数量。")

K.rich(doc, [("线索一：细菌素与发酵过程的菌群控制。", True),
             ("乳球菌的 nisin 簇、植物乳植杆菌的 plantaricin 簇、片球菌的 pediocin 簇、清酒乳杆菌的 sakacin 簇，"
              "都是 II 类或 I 类细菌素，作用靶点是细胞膜或细胞壁前体，能抑制李斯特菌、芽孢杆菌等腐败与致病菌。"
              "在发酵体系里，产细菌素菌株的丰度变化与腐败菌的消长在时间上互补，这一点可以用 4.4 节的物种谱变化来验证："
              "肉制品中 Latilactobacillus sakei 升至 36.6% 的同时，Brochothrix thermosphacta 由 15.4% 降到 6.9%。"
              "若 antiSMASH 在这些 MAG 中检出完整的 sakacin 操纵子，就可以把“基因存在—表达—群落结果”串成一条链。", False)])

K.rich(doc, [("线索二：风味与质构相关的次级代谢。", True),
             ("短杆菌的类胡萝卜素簇对应奶酪表面的橙红色，Acetobacter 与 Komagataeibacter 的纤维素合成簇对应红茶菌膜的"
              "形成，Leuconostoc 的葡聚糖蔗糖酶簇对应黏度与质构。这类产物不是典型的小分子次级代谢物，"
              "在 antiSMASH 中部分以 PKS/萜类或 EPS 相关区域的形式出现，需要结合 CAZyme 注释一起看。"
              "v1.3.2 新增的可可豆发酵数据为这一类提供了新的切入点：Acetobacter pasteurianus 在发酵种子中占 27.8%，"
              "其乙酸代谢与可可风味前体直接相关。", False)])

K.rich(doc, [("线索三：安全风险相关的簇。", True),
             ("Penicillium roqueforti 的 roquefortine C、PR-toxin 簇，Aspergillus 的霉毒素簇，Staphylococcus 的"
              "毒力相关簇，都是发酵食品风险评估的直接靶点。本资源中 Penicillium 有 87 个 MAG、8 个 SGB，"
              "覆盖蓝纹与白霉奶酪的主要成熟菌，具备做簇层面筛查的条件。", False)])

K.para(doc, "益生菌方向的关联相对间接，但有明确切入点。一是细菌素基因簇在益生菌株中的分布，"
            "可直接作为拮抗能力的基因组指标；二是双歧杆菌的羊毛硫肽簇在部分菌株中存在，可作为菌株分型的标记；"
            "三是把制剂来源的 42 个 MAG 与食品中同种菌株的 MAG 做簇组成比较，能看出商业菌株是否丢失了某些 BGC，"
            "这在工业化长期传代后并不罕见。名单内益生菌种在 v1.3.2 中有 4,925 个 MAG，这一比较的统计基础比之前扎实得多。")

K.h2(doc, "6.5 执行方案与判读要点")
K.para(doc, "脚本已随报告提供，分为三步：下载 MAG（10_download_mags.sh）、运行 antiSMASH（11_run_antismash.sh）、"
            "汇总结果（12_parse_antismash.py）。第一步按数据集分包下载，只取代表株所在的包，"
            "可把全网 250 GB 以上的序列压缩到 50 GB 左右。")
K.para(doc, "判读时有四点需要注意。第一，MAG 的完整度直接决定漏检率：完整度 50%–70% 的基因组常缺失簇的调控区或"
            "部分模块，会低估 BGC 总数，建议把 MQ 与 HQ 分开统计。第二，contig 断裂会造成簇被切成两段，"
            "antiSMASH 会报成两个部分簇，汇总时应把同一 contig 邻近的部分簇合并。第三，低相似度簇（--cb-general 中"
            "相似度 < 30%）的可信度有限，需要与已知簇做系统发育比对再判定。第四，细菌素的预测假阳性偏高，"
            "尤其 RiPP-like 类，建议用 BAGEL4 做交叉验证。")

# ============================================================ 七
K.h1(doc, "七、可继续开展的分析", page_break=True)
K.para(doc, "按所需数据分成三档，标注每项的直接产出。前六项只用已下载的总表即可完成，是当前条件下性价比最高的部分。")

K.h2(doc, "A. 仅用公开总表即可完成")
K.numbered(doc, [
    "类别的指示物种分析。用 indicspecies 或 LEfSe 在 15 个类别上找标志物种，输出各类别的诊断性分类单元，"
    "可用于食品溯源与真伪鉴别。v1.3.2 中长尾类别的样品量已足以支撑这一分析，尤其是发酵种子（可可豆）与发酵鱼。",
    "跨类别共现网络。以 4,067 份样品的属水平丰度为输入构建 SparCC 或 SPIEC-EASI 网络，识别发酵体系中的稳定模块，"
    "重点看乳酸菌—醋酸菌—酵母三方关系。",
    "地理与基质对菌群的影响。元数据含 54 个国家，可用 PERMANOVA 分解国家、类别、工艺三个因素的方差贡献，"
    "回答“地域风味”在微生物层面是否有对应。意大利、西班牙、爱尔兰三国样品量最大，也可做国家内部的比较。",
    "发酵剂与非发酵剂菌群的比例。按已知发酵剂名单标注每个 MAG 的来源属性，统计各类别中接种菌与背景菌的比例，"
    "可用于评估工业化程度。",
    "与人体肠道的对接。cFMD 的姊妹资源 cMD（curatedMetagenomicData）可提供人体宏基因组，"
    "原文已用 20,000 余份样品估计食物 SGB 占肠道 3%，可在此基础上细化到类别层面，看哪类发酵食品的 SGB 更容易在肠道中检出[1]。",
    "菌株水平追踪。用 StrainPhlAn 对 Lacticaseibacillus paracasei 等高频种做食品—肠道配对分析，"
    "复现原文提到的食物到肠道传播案例。v1.3.2 中该种已有 716 个 MAG，菌株分辨率明显优于前版。",
    "版本演进分析。cFMD 的每个数据集都记录了加入版本，可按 v1.0.0 / v1.2.1 / v1.3.1 / v1.3.2 分层，"
    "评估数据库扩张对多样性估计的影响，这是少见的、可直接量化的“数据库偏倚”研究素材。",
])

K.h2(doc, "B. 需要 MAG 序列")
K.numbered(doc, [
    "BGC 家族聚类。antiSMASH 后用 BiG-SLiCE 把 1,461–4,554 个 BGC 聚成家族，统计食品特有家族与类别富集，"
    "这是把 antiSMASH 从描述性结果变成可比较数据的关键一步。",
    "细菌素专项预测。BAGEL4 与 RiPPer 交叉验证，输出候选细菌素的成熟肽序列、核心肽与预期抑菌谱，"
    "并可进一步做分子对接筛选敏感菌株。",
    "碳水化合物活性酶谱。dbCAN3 注释 CAZy，比较不同类别中淀粉、乳糖、纤维素、果胶降解能力的差异，"
    "直接对应发酵底物利用与终产物。可可豆发酵中的果胶降解尤其值得关注。",
    "益生性状基因筛查。耐酸（谷氨酸脱羧酶 gadB）、耐胆盐（胆盐水解酶 bsh）、黏附（黏液结合蛋白）、"
    "抗氧化（硫氧还蛋白）等基因在 4,925 个名单内益生菌 MAG 中的分布，可作为菌株筛选的基因组依据。",
    "耐药基因与可移动元件。AMRFinderPlus 与 mobileOG-db 联合注释，重点是接合质粒与转座子上的四环素、"
    "大环内酯类耐药基因，这是食品安全监管关注点，原文也报告了发酵食品中耐药基因的富集。",
    "噬菌体与 CRISPR。用 geNomad 与 CrisprCasFinder 识别前噬菌体与 CRISPR 阵列，分析发酵剂菌株的噬菌体防御能力，"
    "对发酵工业的噬菌体污染问题有直接价值。",
    "比较基因组与泛基因组。同一 SGB 内食品来源与人体来源的 MAG 做泛基因组分析，找食品特异的辅助基因，"
    "这是区分“过路菌”与“定植菌”的基因组证据。",
    "新种描述。226 个 ufSGB 中完整度 ≥90% 的部分，配合 ANI 与 GTDB-Tk 结果，具备新种描述的基因组基础。",
])

K.h2(doc, "C. 需要原始测序数据")
K.numbered(doc, [
    "功能通路重建。HUMAnN3 或 gapseq 从 reads 出发重建代谢通路，可补上 MAG 方法对低丰度成员的系统性遗漏。",
    "宏转录组整合。若有配套 RNA-seq，可把 BGC 的存在与表达对应起来，解决 antiSMASH 只能看“有没有”的问题。",
    "时间序列分析。部分数据集（奶酪成熟、酸面团传代、可可豆发酵）含时间点信息，可做菌群演替与 BGC 表达的动态建模。",
])

K.para(doc, "优先级建议：A 组的第 1、2、5 项与 B 组的第 1、2、4 项组合起来，可以构成一篇完整的论文框架——"
            "从类别标志物种出发，落到 BGC 家族与细菌素候选，最后用益生性状基因收尾。C 组依赖额外数据，"
            "适合作为后续课题而非当前阶段的工作。")

# ============================================================ 八
K.h1(doc, "八、局限说明")
K.numbered(doc, [
    "类别严重不平衡。乳制品占 72.8% 的 MAG，发酵薯类 123 个、发酵果蔬 149 个、发酵鱼 214 个。"
    "任何跨类别比较都受此制约，类别间差异应理解为趋势而非定论。v1.3.2 虽改善长尾类别的代表性，"
    "但没有改变整体结构。",
    "批次效应难以完全消除。109 个数据集的 DNA 提取方法、测序平台、读长与建库策略各不相同，"
    "元数据虽记录了提取试剂盒与平台，但无法完全校正。原文对此做了标准化处理，残余效应仍然存在[15]。",
    "MAG 方法本身的偏倚。高丰度、低复杂度的群落（如接种发酵）更容易得到高质量 MAG，"
    "低丰度成员与高复杂度群落（如传统自然发酵）被系统性低估，这会放大发酵剂菌株的表观重要性。",
    "SGB 划分依赖参考数据库。kSGB 的定义是簇内至少有一个参考基因组，参考库覆盖好的类群（乳球菌、乳杆菌）"
    "更容易被判为已知种，参考库薄弱的类群（发酵鱼、发酵种子中的新颖类群）则集中落在 uSGB/ufSGB。"
    "v1.2 之后 MetaRefSGB 整体更新，SGB 编号与 v1.1.0 不可直接对齐，跨版本比较必须以物种名为准。",
    "antiSMASH 部分为预判而非实测。第六章的产物对应关系来自文献，BGC 数量为区间估算，"
    "均需在拿到 MAG 序列后以实测结果替换。",
    "益生菌名单的边界问题。种级名单依据 QPS 与国内名单整理，但同一物种内不同菌株的益生功能差异很大，"
    "基因组层面的“益生菌物种”不等于“益生菌菌株”，这一点在解读表 10 时需保留。",
    "两版数据不可混用。本报告全部数字基于 v1.3.2；若与他人的 v1.1.0 结果并列，需在表头注明版本，"
    "否则样品数、MAG 数、SGB 数三项都会出现 30%–60% 的表面差异。",
])

# ============================================================ 九
K.h1(doc, "九、参考文献", page_break=True)
refs = [
    "Carlino N, Blanco-Míguez A, Manghi P, et al. Unexplored microbial diversity from 2,500 food metagenomes and links with the human microbiome. Cell, 2024, 187(20): 5775–5795.e15. doi:10.1016/j.cell.2024.07.039",
    "SegataLab. curatedFoodMetagenomicData (cFMD), v1.3.2. GitHub, 2026. https://github.com/SegataLab/cFMD",
    "EFSA Panel on Biological Hazards. Update of the list of qualified presumption of safety (QPS) recommended microorganisms. EFSA Journal, 2024, 22(1): e8488.",
    "Hill C, Guarner F, Reid G, et al. The ISAPP consensus statement on the scope and appropriate use of the term probiotic. Nature Reviews Gastroenterology & Hepatology, 2014, 11: 506–514.",
    "Patro JN, Ramachandran P, Barnaba T, et al. Comparison of metagenomic sequencing and conventional culture methods for characterization of probiotic products. Food Microbiology, 2016, 59: 1–10.",
    "Pasolli E, De Filippis F, Mauriello IE, et al. Large-scale genome-wide analysis links lactic acid bacteria from food with the gut microbiome. Nature Communications, 2020, 11: 2610.",
    "Blin K, Shaw S, Augustijn HE, et al. antiSMASH 8.0: extended gene cluster detection capabilities and analyses of chemistry, enzymology, and regulation. Nucleic Acids Research, 2025, 53(W1): W32–W38.",
    "Alvarez-Sieiro P, Montalbán-López M, Mu D, Kuipers OP. Bacteriocins of lactic acid bacteria: extending the family. Applied Microbiology and Biotechnology, 2016, 100: 2939–2951.",
    "McAuliffe O, Ross RP, Hill C. Lantibiotics: structure, biosynthesis and mode of action. FEMS Microbiology Reviews, 2001, 25: 285–308.",
    "Zacharof MP, Lovitt RW. Bacteriocins produced by lactic acid bacteria: a review article. APCBEE Procedia, 2012, 2: 50–56.",
    "Caulier S, Nannan C, Gillis A, et al. Overview of the antimicrobial compounds produced by members of the Bacillus subtilis group. Frontiers in Microbiology, 2019, 10: 302.",
    "Coton M, Deniel F, Mounier J, et al. Penicillium roqueforti: an overview of its genetics, physiology, metabolism and biotechnological applications. Fungal Biology Reviews, 2021, 35: 1–19.",
    "Irlinger F, Helinck S, Jany JL. Secondary and adjunct cultures. In: Cheese: Chemistry, Physics and Microbiology, 4th ed. Academic Press, 2017: 273–300.",
    "Marco ML, Sanders ME, Gänzle M, et al. The International Scientific Association for Probiotics and Prebiotics (ISAPP) consensus statement on fermented foods. Nature Reviews Gastroenterology & Hepatology, 2021, 18: 196–208.",
    "Walsh AM, Leech J, Sheehan JJ, et al. Fermented-food metagenomics reveals substrate-associated differences in taxonomy and health-associated and antibiotic resistance determinants. mSystems, 2020, 5: e00522-20.",
    "Pasolli E, Asnicar F, Manara S, et al. Extensive unexplored human microbiome diversity revealed by over 150,000 genomes from metagenomes spanning age, geography, and lifestyle. Cell, 2019, 176: 649–662.",
]
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = K.Pt(24)
    p.paragraph_format.first_line_indent = K.Pt(-24)
    p.paragraph_format.space_after = K.Pt(4)
    p.paragraph_format.line_spacing = 1.25
    p.alignment = K.WD_ALIGN_PARAGRAPH.JUSTIFY
    K._set_run(p.add_run(f"[{i}] "), 9, False, K.GREY)
    K._set_run(p.add_run(r), 9, False, K.DARK)

# ============================================================ 附录
K.h1(doc, "附录  交付文件清单", page_break=True)
K.para(doc, "正文引用的表与图均可在此清单中找到对应的数据文件，编号一致。")
files = pd.DataFrame([
    ["00", "MAG主表_全部.csv", "18,180 个 MAG 的注释与元数据合并表，含是否纳入分析", "18,180 行"],
    ["01", "发酵MAG总表.csv", "发酵样品的全部 MAG，含类别、质量、益生菌归属", "15,446 行"],
    ["02", "按发酵种类汇总.csv", "10 个发酵类别的统计汇总", "11 行"],
    ["03", "属水平MAG数量矩阵.csv", "前 40 属 × 10 类别的计数矩阵", "40 × 10"],
    ["04", "SGB水平汇总_含发酵类别.csv", "1,654 个 SGB 的分类、来源、发酵类别分布", "1,654 行"],
    ["05", "益生菌制剂来源MAG表.csv", "14 份制剂样品的 42 个 MAG", "42 行"],
    ["06", "益生菌物种MAG全库表.csv", "A 宽口径（133 种）的 6,385 个 MAG", "6,385 行"],
    ["07", "益生菌物种x发酵类别矩阵.csv", "益生菌物种在各类别中的分布", "—"],
    ["08", "发酵食品真核MAG表.csv", "848 个真核 MAG", "848 行"],
    ["09", "antiSMASH输入MAG清单_每SGB代表株.csv", "1,142 个代表株（P1/P2 优先级）", "1,142 行"],
    ["10-16", "物种谱系列", "发酵与非发酵的物种差异、类别丰度、alpha 多样性", "8 个表"],
    ["17", "antiSMASH产物知识表.csv", "50 个分类单元的簇类型与代表产物", "50 行"],
    ["18-19", "BGC预期工作量表", "按属估算的 BGC 数量", "2 个表"],
    ["20", "发酵类型明细_按type.csv", "91 个发酵食品类型的样品、MAG、优势种", "91 行"],
    ["21", "益生菌严格名单MAG表.csv", "名单内 28 个种的 4,925 个 MAG", "4,925 行"],
    ["22", "益生菌分层汇总.csv", "四个口径的种 / SGB / MAG 计数", "5 行"],
    ["—", "figures/", "图 1–6 的 PNG 文件（300 dpi）", "6 个"],
    ["—", "scripts/", "数据整理、统计、绘图与 antiSMASH 流程脚本", "14 个"],
], columns=["编号", "文件", "内容", "规模"])
K.table(doc, files, widths=[1.3, 5.4, 7.3, 2.2], font_size=8)
K.caption(doc, "附表 A  随报告交付的数据文件")

K.para(doc, "表 6 的类别之下还有一层更细的 type 划分，v1.3.2 共 149 类。下表给出 MAG 数最多的 15 类，"
            "含样品量、地理覆盖、优势种与该类型的代表 MAG，可用于挑选具体工艺做深入分析。完整清单见附表 20。")
t15 = td[["发酵类别", "食品类型", "样品数", "数据集数", "国家数", "MAG数", "HQ数", "SGB数", "属数", "优势种Top3"]].head(15)
t15.columns = ["类别", "类型", "样品", "数据集", "国家", "MAG", "HQ", "SGB", "属", "优势种（MAG 数）"]
K.table(doc, t15, widths=[2.4, 2.6, 1.0, 1.1, 1.0, 1.0, 0.9, 0.9, 0.8, 6.0], font_size=7.4, header_size=7.8)
K.caption(doc, "附表 B  发酵食品类型明细（前 15 类）")

doc.save(OUT)
print("saved", OUT, round(os.path.getsize(OUT) / 1024), "KB")
