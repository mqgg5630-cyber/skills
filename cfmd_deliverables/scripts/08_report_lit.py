# -*- coding: utf-8 -*-
"""生成【含文献版】报告 DOCX"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import docxkit as K

T = "/home/user/skills/cfmd_deliverables/tables"
F = "/home/user/skills/cfmd_deliverables/figures"
OUT = "/home/user/skills/cfmd_deliverables/文档/cFMD食品微生物组MAG分析报告_含文献版.docx"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

s = pd.read_csv(f"{T}/02_按发酵种类汇总.csv")
s10 = s[s["发酵类别"] != "合计"].copy()
bgc = pd.read_csv(f"{T}/17_antiSMASH产物知识表_文献依据.csv")
work = pd.read_csv(f"{T}/18_antiSMASH_BGC预期工作量_按属.csv")
probmag = pd.read_csv(f"{T}/05_益生菌制剂来源MAG表.csv", encoding="utf-8-sig")
prob_sgb = pd.read_csv(f"{T}/04_SGB水平汇总_含发酵类别.csv")
tab = pd.read_csv(f"{T}/10_物种谱_发酵vs非发酵差异.csv")
pair = pd.read_csv(f"{T}/15_同基质发酵vs非发酵多样性.csv")

doc = K.new_document()
K.add_header_text(doc, "cFMD 食品微生物组 MAG 分析")
K.add_page_number_footer(doc, "cFMD v1.1.0")

# ============================================================ 封面
K.title(doc,
        "食品宏基因组 MAG 资源中的发酵与益生菌模块分析",
        "基于 cFMD 数据库 2,533 份食品宏基因组、10,899 个 MAG",
        "数据版本：curatedFoodMetagenomicData v1.1.0（Carlino et al., Cell, 2024）\n"
        "分析日期：2026 年 10 月    文件版本：含文献版")

doc.add_paragraph()
K.h2(doc, "目  录")
toc = [
    "一、数据来源与下载清单",
    "二、数据库总体情况",
    "三、MAG 的提取口径与分组规则",
    "四、发酵种类模块",
    "    4.1 总体分布",
    "    4.2 各发酵类别的菌群构成",
    "    4.3 优势属与优势种",
    "    4.4 与同基质非发酵样品的对照",
    "    4.5 真核微生物部分",
    "五、益生菌模块",
    "    5.1 三个层次的界定",
    "    5.2 益生菌制剂来源的 MAG",
    "    5.3 全库范围内的核心益生菌物种",
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
K.h1(doc, "一、数据来源与下载清单", page_break=True)
K.h2(doc, "1.1 原始文献")
lit = pd.DataFrame([
    ["题目", "Unexplored microbial diversity from 2,500 food metagenomes and links with the human microbiome"],
    ["作者", "Carlino N, Blanco-Míguez A, Manghi P, et al.（通讯作者 Nicola Segata）"],
    ["期刊", "Cell, 2024, 187(20): 5775–5795.e15"],
    ["DOI", "10.1016/j.cell.2024.07.039"],
    ["PMID", "39214080"],
    ["数据资源", "curatedFoodMetagenomicData（cFMD），GitHub: SegataLab/cFMD；MAG 序列存于 Zenodo, doi:10.5281/zenodo.10891046"],
], columns=["项目", "内容"])
K.table(doc, lit, widths=[2.6, 13.0], font_size=9, header_size=9)
K.caption(doc, "表 1  原始文献信息", above=True)

K.para(doc, "该研究整合了 1,950 份新测序与 583 份公共食品宏基因组，重建 10,899 个宏基因组拼接基因组"
            "（MAG），聚类为 1,036 个原核与 108 个真核物种水平基因组 bin（SGB），其中 320 个为此前未描述的分类单元；"
            "并进一步与 20,000 余份人体宏基因组比对，估计食物来源 SGB 平均占成人肠道微生物组的 3% 左右[1]。")

K.h2(doc, "1.2 下载的公开总表")
K.para(doc, "cFMD 的样品元数据、MAG 清单、SGB 汇总与物种谱均以制表符分隔文本形式公开，随版本标签发布，"
            "无需下载序列即可完成全部统计。本次使用的文件如表 2。")
t2 = pd.DataFrame([
    ["cFMD_metadata.tsv", "样品级元数据：类别、发酵属性、国家、测序与组装统计", "2,533 行 × 32 列"],
    ["cFMD_mags_list.tsv", "MAG 清单：所属样品、SGB、分类、完整度/污染度、基因组大小", "10,899 行 × 19 列"],
    ["cFMD_sgbs_prokaryotic.tsv", "原核 SGB 汇总：分类、MAG 数、参考基因组数、各食品类别 MAG 数", "1,036 行 × 34 列"],
    ["cFMD_sgbs_eukaryotic.tsv", "真核 SGB 汇总", "108 行"],
    ["cFMD_taxonomic_profiles.tsv", "MetaPhlAn4 物种水平相对丰度谱", "3,628 行 × 2,483 列"],
    ["cFMD_datasets.tsv", "数据集清单与对应文献、Bioproject 号", "59 行"],
], columns=["文件", "内容", "规模"])
K.table(doc, t2, widths=[4.4, 8.6, 2.9], font_size=8.5)
K.caption(doc, "表 2  本次使用的 cFMD 公开总表")

K.h2(doc, "1.3 版本与可及性说明")
K.para(doc, "受版本更新的影响，cFMD 现行主分支已累计至 18,180 个 MAG、4,125 份样品、109 个数据集与 54 个国家[2]，"
            "与论文发表时的数字不再一致。为保证结果可与原文逐项核对，本报告固定使用与论文配套的 v1.1.0 标签所对应的表文件。"
            "该版本在 Zenodo 上对应的记录为 10.5281/zenodo.13285428，包含 cFMD_mags.tar.gz（9.8 GB，MAG 序列压缩包）"
            "与 cFMD_humann.tar.gz（1.4 GB，功能谱）；按数据集拆分的 MAG 包（记录 14871720）合计约 272.5 GB。")
K.para(doc, "本次分析仅使用总表文件，未下载 MAG 序列。原因有两点：一是当前计算环境对 Zenodo 无出站访问权限，"
            "仅可访问 GitHub 与 PyPI 等少数主机；二是本地磁盘 20 GB，不足以容纳 272.5 GB 的序列集合。"
            "因此第六章的 antiSMASH 部分为基于分类学与文献的产物预判，并附可直接执行的运行脚本，"
            "在有 conda 与存储条件的服务器上补跑即可得到实测结果。")

# ============================================================ 二
K.h1(doc, "二、数据库总体情况", page_break=True)
t3 = pd.DataFrame([
    ["食品宏基因组样品", "2,533", "2,533", "与原文一致"],
    ["其中：新测序 / 公共数据", "1,950 / 583", "1,986 / 547", "版本更新导致的细微差异"],
    ["数据集", "59", "59", "一致"],
    ["国家", "50", "50", "一致"],
    ["测序碱基总量", "—", "14.7 Tb", "乳制品占 11.6 Tb"],
    ["MAG 总数", "10,899", "10,899", "一致"],
    ["　原核 / 真核", "10,112 / 787", "10,112 / 787", "原核含细菌 10,097、古菌 15"],
    ["SGB 总数", "1,036 原核 + 108 真核", "1,144", "一致"],
    ["　已知种（kSGB）", "—", "613", "含至少一个参考基因组"],
    ["　未知种（uSGB）", "—", "241", "仅由重建基因组构成"],
    ["　食品新种（ufSGB）", "320 个未描述类群", "290", "均为原核；原文口径另含部分未知种"],
    ["发酵样品 / 占比", "—", "2,262 / 89.3%", "按元数据 fermented 字段"],
    ["发酵样品来源 MAG / 占比", "—", "10,202 / 93.6%", "本报告分析主体"],
], columns=["指标", "原文（Cell 2024）", "本表核对（v1.1.0）", "说明"])
K.table(doc, t3, widths=[4.6, 3.6, 3.6, 4.1], font_size=8.5)
K.caption(doc, "表 3  数据库总体指标与原文核对")

K.para(doc, "从结构上看，该资源的三分之一以上是新描述的分类单元：1,144 个 SGB 中有 531 个不含任何参考基因组，"
            "其中 290 个为仅见于食品样品的新种（图 1）。这一部分正是发酵食品微生物组相对临床与环境样本库的主要增量，"
            "也是后续做新种挖掘、新产物发现的空间。")
K.figure(doc, f"{F}/fig6_SGB新颖性.png", 9.6)
K.caption(doc, "图 1  食品 MAG 所属 SGB 的新颖性构成（n = 1,144）")

# ============================================================ 三
K.h1(doc, "三、MAG 的提取口径与分组规则")
K.para(doc, "全部统计遵循以下四条规则，后续表格与图件均按此口径生成。")
K.numbered(doc, [
    "发酵属性直接取自元数据 fermented 字段（F / NF），不根据类别名反推。乳制品中另有 163 份非发酵样品（鲜奶 110 份、奶酪盐水 53 份），"
    "发酵肉与非发酵肉、发酵果蔬与非发酵果蔬同理，二者在第四章第四节做同基质对照。",
    "食品类别按 category（15 类）划分，type 与 subtype 作为更细的基质描述保留在主表中。发酵相关类别共 10 个，"
    "另有 probiotics、meat、fish、fruits_and_vegetables、other 五个非发酵类别。",
    "MAG 质量按 CheckM 结果分级：完整度 ≥ 90% 且污染 < 5% 记为高质量（HQ），完整度 50%–90% 且污染 < 5% 记中等质量（MQ）。"
    "cFMD 收录的全部 MAG 均已满足完整度 ≥ 50%、污染 < 5% 的准入条件，因此表中只出现 HQ 与 MQ 两级。",
    "SGB 是物种水平的聚类单元，同一 SGB 内的多个 MAG 来自不同样品，代表同一物种的不同菌株集合[16]。"
    "做基因组层面的分析（如 antiSMASH）时按 SGB 去重，每个 SGB 取完整度最高、污染最低的一株作代表。",
])

# ============================================================ 四
K.h1(doc, "四、发酵种类模块", page_break=True)
K.h2(doc, "4.1 总体分布")
K.para(doc, "2,262 份发酵样品共产生 10,202 个 MAG，其中原核 9,445 个、真核 757 个；高质量 5,203 个（51.0%），"
            "中等质量 4,998 个，另 1 个未达 MQ。这些 MAG 分属 957 个 SGB，包括 537 个已知种、204 个未知种与 216 个食品新种。"
            "从类群上看，乳酸菌相关属（Lactococcus、Lactobacillus 及其拆分后的 11 个属、Leuconostoc、Pediococcus、"
            "Weissella、Oenococcus、Tetragenococcus、Enterococcus、Streptococcus、Bifidobacterium 等共 23 属）"
            "合计 5,273 个 MAG，占发酵样品原核 MAG 的 55.8%，是绝对主体。")
K.para(doc, "十个发酵类别的分布高度不均：乳制品独占 67.4% 的 MAG，发酵饮料 19.7%，两者合计接近九成；"
            "发酵鱼制品仅有 32 个 MAG，来自 1 个数据集、5 份样品。这一偏倚决定了后续任何跨类别比较都必须以类别内比较为主，"
            "不宜直接以 MAG 总数衡量某类发酵食品的微生物多样性。")

cols = ["发酵类别", "样品数", "数据集数", "国家数", "MAG总数", "原核MAG", "真核MAG",
        "高质量MAG(HQ)", "SGB总数", "已知种SGB(kSGB)", "食品新种SGB(ufSGB)", "属数", "已定名种数"]
disp = s10[cols].copy()
disp.columns = ["发酵类别", "样品", "数据集", "国家", "MAG", "原核", "真核", "HQ", "SGB", "kSGB", "ufSGB", "属", "种"]
K.table(doc, disp, widths=[2.5, 1.05, 1.0, 0.95, 1.15, 1.05, 1.05, 1.0, 1.0, 1.15, 1.25, 0.8, 0.9], font_size=8)
K.caption(doc, "表 4  各发酵食品类别的 MAG 与 SGB 数量（数据来源：cFMD v1.1.0 元数据与 MAG 清单）",
          note="注：HQ 指完整度 ≥90%、污染 <5%；kSGB 为已知种，ufSGB 为仅见于食品样品的新种 SGB。")

K.figure(doc, f"{F}/fig1_类别MAG数量.png", 15.0)
K.caption(doc, "图 2  各发酵食品类别重建的 MAG 数量与质量分布")

K.h2(doc, "4.2 各发酵类别的菌群构成")
K.para(doc, "以下按类别给出主导菌群。样品量小于 20 的类别（发酵豆类、发酵种子、发酵鱼制品）只作趋势描述，"
            "不据此下结论。")

K.h2(doc, "（1）乳制品：1,487 份样品，6,879 个 MAG")
K.para(doc, "乳制品是资源最厚的部分，来自 30 个数据集、36 个国家。主导菌为 Lactococcus lactis（634 个 MAG）、"
            "Streptococcus thermophilus（415 个）、Lactococcus cremoris（392 个）、Lacticaseibacillus paracasei（230 个）"
            "与 Lactobacillus helveticus（163 个），与嗜温发酵剂、嗜热发酵剂两大工艺路线直接对应。"
            "奶酪表面成熟带来的 Brevibacterium（370 个）、Corynebacterium（134 个）、Brachybacterium（157 个）"
            "是乳制品独有的组成，在其余类别中几乎不出现。真核部分以 Debaryomyces hansenii（128 个）与 "
            "Penicillium roqueforti（37 个）为主，对应白霉与蓝纹奶酪。")
K.para(doc, "乳制品的 SGB 新颖性同样突出：535 个 SGB 中 242 个不含参考基因组（45.2%），其中 83 个为食品新种。"
            "说明即便在研究最充分的乳制品中，仍有大量未培养类群只以 MAG 形式存在。")

K.h2(doc, "（2）发酵饮料：422 份样品，2,011 个 MAG")
K.para(doc, "该类以水开菲尔（water kefir）为主体，388 份占九成以上，其余为康普茶（21 份）、咖啡发酵（6 份）、Pulque（5 份）等。"
            "菌群由三部分叠加：Liquorilactobacillus（432 个）、Lacticaseibacillus（247 个）、Leuconostoc（139 个）"
            "构成乳酸菌骨架，Acetobacter（250 个）与 Gluconobacter（85 个）承担乙醇到乙酸的氧化，"
            "Zymomonas mobilis（109 个）在棕榈酒等含糖汁液中主导乙醇发酵。真核占比 11.6%，为各类别中较高，"
            "以 Saccharomyces cerevisiae（149 个）与 Brettanomyces（19 个）为主。")
K.para(doc, "水开菲尔颗粒（grain）样品同时提供了液相与颗粒相两种取样，为研究颗粒生物膜的空间分层提供了条件，"
            "这是其余类别不具备的特点。")

K.h2(doc, "（3）发酵肉制品：133 份样品，526 个 MAG")
K.para(doc, "以萨拉米（66 份）与肉糜灌肠（67 份）为主，来自意大利、西班牙、瑞士 3 个国家、6 个数据集。主导菌为 Staphylococcus xylosus（42 个）、"
            "Latilactobacillus sakei（41 个）、Latilactobacillus curvatus（36 个），符合硝酸盐还原、脂质氧化与酸化的"
            "成熟工艺。Brevibacterium、Corynebacterium 亦有一定比例。真核占 9.1%，以 Debaryomyces hansenii 与 "
            "Penicillium nalgiovense 为代表，对应表面发酵剂。")

K.h2(doc, "（4）发酵谷物制品：80 份样品，225 个 MAG")
K.para(doc, "以酸面团（40 份）为主，其余为西非与东非传统谷物料：Ogi（12 份）、Kunu（6 份）、Ugi（4 份）、Injera（2 份）等。主导种为 Lactiplantibacillus plantarum（19 个）、"
            "Fructilactobacillus sanfranciscensis（13 个）、Levilactobacillus brevis（17 个）与 Limosilactobacillus fermentum（14 个），"
            "与酸面团中酵母—乳酸菌共生体系一致。该类 HQ 比例 56.9%，高于发酵食品整体的 51.0%，说明基质相对简单、组装质量较好。")

K.h2(doc, "（5）含酒精发酵饮料：48 份样品，161 个 MAG")
K.para(doc, "葡萄酒（20 份，霞多丽葡萄醪）、兰比克啤酒（7 份）、棕榈酒（6 份）、中国白酒与非洲小米酒（各 3 份）等。真核占 44.7%，为各类别中最高。"
            "Saccharomyces cerevisiae 在物种谱中平均占 40.5%，Lactobacillus 与 Oenococcus 承担苹果酸—乳酸发酵。"
            "该类别的分析价值主要在酵母与乳酸菌的互作，而非细菌多样性。")

K.h2(doc, "（6）发酵薯类与根茎：24 份样品，123 个 MAG")
K.para(doc, "木薯制品（Gari 5 份、Fufu 4 份、Lafun 3 份、Attieke 1 份）与腌萝卜、芜菁、姜等根茎类。Limosilactobacillus fermentum（11 个）、"
            "Lactobacillus delbrueckii（8 个）、Lactobacillus helveticus（8 个）为主，属数达 40，"
            "每样品平均 5.12 个 MAG，是 MAG 产出效率最高的类别之一。该类样本量小但地理来源分散（6 国），"
            "适合做传统发酵食品的地域特异性分析。")

K.h2(doc, "（7）发酵果蔬：34 份样品，91 个 MAG")
K.para(doc, "酸菜（9 份）、红椒酱（8 份）、泡菜（5 份）、腌黄瓜与腌胡萝卜等。Lactiplantibacillus plantarum（6 个）、Leuconostoc mesenteroides（5 个）、"
            "Levilactobacillus brevis（10 个）为主，Weissella 与 Pediococcus 亦有分布。"
            "该类样品中植物来源的 Enterobacter、Citrobacter 等肠杆菌科同时存在，反映发酵初期与终产品之间的差异。")

K.h2(doc, "（8）发酵豆类：16 份样品，90 个 MAG")
K.para(doc, "基质全部为大豆：中国酱油盐水与豆酱 8 份、尼泊尔 Kinema 4 份、印尼天贝 3 份、辣味豆腐 1 份。Weissella confusa 在物种谱中占 22.7%，"
            "Enterococcus faecium、Bacillus velezensis 亦有分布。样本仅 16 份，覆盖 5 国，代表性有限，"
            "但亚洲与非洲传统豆制品的高熵发酵体系在此有所体现。")

K.h2(doc, "（9）发酵种子与油料：13 份样品，64 个 MAG")
K.para(doc, "以非洲角豆（Parkia）与油料种子为基质：Iru 6 份、Ugba 3 份、Okpehe 2 份、Dawa-dawa 与 Soumbala 各 1 份。Bacillus subtilis（10 个）与 Caldibacillus thermoamylovorans（6 个）"
            "占主导，属于典型的碱性发酵（alkaline fermentation），与乳酸发酵路径明显不同。该类 ufSGB 比例达 13/40，"
            "新种比例高。")

K.h2(doc, "（10）发酵鱼制品：5 份样品，32 个 MAG")
K.para(doc, "仅韩国洪鱼（hongeo）1 个数据集。Psychrobacter maritimus 在物种谱中占 66.6%，"
            "Jeotgalibaca dankookensis 占 12.9%。21 个 SGB 中 20 个为 uSGB 或 ufSGB（95.2%），"
            "新颖性最高，但样本量过小，只能作为高盐低温发酵体系的个案线索。")

K.h2(doc, "4.3 优势属与优势种")
K.para(doc, "图 3 给出前 22 个属在 10 个类别中的 MAG 数量。可以清楚看到三条分带：第一带为 Lactococcus、"
            "Lactobacillus、Lacticaseibacillus、Streptococcus、Leuconostoc，集中在乳制品与发酵饮料；"
            "第二带为 Staphylococcus、Latilactobacillus、Brevibacterium、Corynebacterium，集中在发酵肉与乳制品表面；"
            "第三带为 Bacillus、Caldibacillus、Weissella、Enterococcus，出现在发酵种子与发酵豆类。"
            "同一属在不同类别中的数量差异，反映的是基质与工艺的选择，而不是属本身的分布偏好。")
K.figure(doc, f"{F}/fig2_优势属热图.png", 14.2)
K.caption(doc, "图 3  发酵食品中优势菌属的 MAG 数量分布（前 22 属，数值为 MAG 数）")

K.para(doc, "属水平之外，种水平的前 15 位为：Lactococcus lactis（655）、Streptococcus thermophilus（418）、"
            "Lacticaseibacillus paracasei（412）、Lactococcus cremoris（394）、Leuconostoc mesenteroides（222）、"
            "Liquorilactobacillus satsumensis（200）、Leuconostoc pseudomesenteroides（196）、Lactobacillus helveticus（163）、"
            "Staphylococcus equorum（161）、Lactobacillus delbrueckii（155）、Brevibacterium aurantiacum（154）、"
            "Lactiplantibacillus plantarum（126）、Liquorilactobacillus nagelii（118）、Zymomonas mobilis（115）、"
            "Latilactobacillus curvatus（94）。")
K.para(doc, "前四位全部是发酵剂核心菌，且 MAG 数远超第五位，这与发酵食品“人工接种 + 强选择”的生产方式相符："
            "发酵剂菌株以极高丰度存在，组装时更容易获得完整基因组。这一结构提示，直接用 MAG 数量代表物种重要性时，"
            "会系统性高估发酵剂、低估非接种的背景菌群。")

K.h2(doc, "4.4 与同基质非发酵样品的对照")
K.para(doc, "元数据中同时收录了未发酵的鲜肉、鲜鱼与生鲜果蔬，可以做同基质对照。物种水平 Shannon 指数上，"
            "发酵样品的多样性普遍低于同基质生样（表 5），说明发酵过程伴随明显的群落收敛。"
            "其中乳制品、肉制品、鱼制品的差异达到统计显著，果蔬因样本量小未达显著。")
K.table(doc, pair, widths=[5.2, 1.9, 1.6, 2.6, 2.6, 1.6], font_size=8.5)
K.caption(doc, "表 5  同基质条件下发酵与非发酵样品的 alpha 多样性比较",
          note="注：Shannon 指数基于 MetaPhlAn4 物种水平相对丰度计算；P 值由 Mann-Whitney U 检验得到（双尾）。")

K.para(doc, "从物种组成看，肉制品中 Pseudomonas fragi（非发酵 6.20% 对发酵 0.13%）、Brochothrix thermosphacta、"
            "Acinetobacter 等在发酵后大幅下降；取而代之的是 Latilactobacillus sakei（34.3%）、Staphylococcus xylosus（9.5%）。"
            "这一升一降正好刻画了发酵对腐败菌群的抑制。鱼类样品呈现类似格局，发酵后 Psychrobacter 占绝对优势。")
K.figure(doc, f"{F}/fig4_alpha多样性.png", 15.0)
K.caption(doc, "图 4  各食品类别的物种水平 alpha 多样性（蓝色为发酵类别，棕色为非发酵类别）")

K.h2(doc, "4.5 真核微生物部分")
K.para(doc, "757 个真核 MAG 分布在 95 个 SGB 中，涉及 108 个真核 SGB 的绝大部分。属水平以 Saccharomyces（192 个）、"
            "Debaryomyces（133 个）、Penicillium（83 个）、Scopulariopsis（40 个）、Kluyveromyces（34 个）为主。"
            "种水平以 Saccharomyces cerevisiae（190 个）、Debaryomyces hansenii（128 个）、Penicillium roqueforti（37 个）、"
            "Scopulariopsis brevicaulis（36 个）、Kluyveromyces lactis（25 个）、Penicillium camemberti（24 个）为代表。")
K.para(doc, "真核 MAG 的类别分布与细菌明显不同：含酒精饮料 44.7%、发酵饮料 11.6%、发酵肉 9.1%，"
            "而乳制品仅 5.4%。奶酪中的真菌种类虽少但功能关键，Penicillium 属的次生代谢产物直接决定蓝纹与白霉奶酪的"
            "风味与安全性，这一点在第六章讨论。")
K.figure(doc, f"{F}/fig5_真核组成.png", 14.2)
K.caption(doc, "图 5  发酵食品真核 MAG 的属组成（前 12 属）")

# ============================================================ 五
K.h1(doc, "五、益生菌模块", page_break=True)
K.h2(doc, "5.1 三个层次的界定")
K.para(doc, "在 cFMD 中，“益生菌”需要区分三个不同层面，混用会导致数量上的误判。")
K.numbered(doc, [
    "益生菌制剂样品。元数据中 probiotics 是一个独立的食品类别，共 14 份样品、42 个 MAG，"
    "对应市售益生菌粉剂与胶囊。这是最严格的“益生菌 MAG”。",
    "核心益生菌物种。以 EFSA 安全资格认定（QPS）名单、ISAPP 益生菌共识与中国《可用于保健食品的益生菌菌种名单》"
    "为依据整理出的种级名单，在全库发酵样品中筛出 28 个种、30 个 SGB、2,884 个 MAG[3,4]。"
    "需与 ISAPP 对发酵食品的界定区分：发酵食品中的活菌不等于益生菌[14]。",
    "乳酸菌发酵剂类群。按属归并的 23 个属，共 5,273 个 MAG，占发酵样品原核 MAG 的 55.8%。"
    "这一层包含大量不具有明确益生功能证据的发酵剂菌株，不宜统称为益生菌。",
])
K.para(doc, "对“益生菌属于微生物的 MAG 吗”这一问题，答案是肯定的，但需要说明两点。第一，益生菌制剂在 cFMD 中与"
            "乳制品、发酵肉等并列，是食品基质的一种，其样品同样经过组装与分箱，得到的 42 个 MAG 与其他类别完全同质，"
            "可以直接合并分析。第二，这 42 个 MAG 只来自 14 份样品，样本量决定了它无法支撑独立的统计推断，"
            "更适合作为菌株参考基因组的补充。")
K.para(doc, "对“有益生菌方面的 MAG 吗”，答案同样是肯定的：制剂来源 42 个，加上全库范围内核心益生菌物种的 2,884 个，"
            "两者合计构成益生菌方向的 MAG 集合。前者提供的是商业化菌株，后者提供的是食品基质中的同种野生型菌株，"
            "两组对照可以回答“商业菌株与食品中同种菌株在基因组上有何差异”这一问题。")

K.h2(doc, "5.2 益生菌制剂来源的 MAG")
K.para(doc, "14 份制剂样品来自两项研究：PatroJN_2016（美国，10 份）与 PasolliE_2020（意大利，4 份）[5,6]。"
            "共得到 42 个 MAG、23 个 SGB。物种构成为 Lactiplantibacillus plantarum（7 个）、Lactobacillus acidophilus（5 个）、"
            "Bifidobacterium animalis（4 个）、Lacticaseibacillus rhamnosus（3 个），Bifidobacterium breve、"
            "Bifidobacterium longum、Lacticaseibacillus paracasei、Ligilactobacillus salivarius 各 2 个，"
            "其余 15 个种各 1 个。")
K.para(doc, "质量上，这 42 个 MAG 的平均完整度 76.7%，低于发酵食品整体的 84.3%；HQ 仅 16 个，MQ 26 个。"
            "原因在于制剂样品中菌株种类少、每种菌的相对丰度受配方比例限制，且辅料（麦芽糊精、微晶纤维素）DNA 比例高，"
            "组装时覆盖度分布不均。做下游分析时建议优先取 HQ 的 16 个。")

ps = probmag.groupby(["物种", "属"]).agg(
    MAG数=("MAG_id", "size"), SGB数=("SGB_id", "nunique"),
    HQ数=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
    MAG列表=("MAG_id", lambda x: "；".join(list(x)[:2]) + ("等" if len(x) > 2 else "")),
    HQ数2=("completeness", lambda x: round(x.max(), 1))).reset_index()
ps = ps.sort_values("MAG数", ascending=False)
ps.columns = ["物种", "属", "MAG数", "SGB数", "HQ数", "代表MAG", "最高完整度%"]
ps_disp = ps[["物种", "MAG数", "HQ数", "最高完整度%", "SGB数"]]
K.table(doc, ps_disp, widths=[6.4, 1.6, 1.3, 2.2, 1.3], font_size=8.5)
K.caption(doc, "表 6  益生菌制剂来源的 MAG（按物种合并，共 42 个 MAG、23 个 SGB）",
          note="注：完整度与污染度由 CheckM 估计；详细 MAG 编号见附表 05。")

K.h2(doc, "5.3 全库范围内的核心益生菌物种")
K.para(doc, "以种级名单在 10,202 个发酵 MAG 中筛选，得到 28 个种、30 个 SGB、2,884 个 MAG，其中 HQ 1,335 个。"
            "从基质看，乳制品 2,241 个、发酵饮料 396 个、发酵谷物 89 个、含酒精饮料 42 个，其余类别均不足 40 个。"
            "这一分布与发酵剂的使用直接相关，也说明“益生菌物种”在食品中的载体高度集中于乳制品。")
psp = ps_disp.copy()
tab6 = pd.read_csv(f"{T}/06_益生菌物种MAG全库表.csv", encoding="utf-8-sig")
core = tab6.groupby("物种").agg(MAG数=("MAG_id", "size"), HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                                SGB=("SGB_id", "nunique"), 主要类别=("发酵类别中文", lambda x: x.value_counts().index[0]))
core = core.sort_values("MAG数", ascending=False).head(18).reset_index()
core.columns = ["物种", "MAG数", "HQ数", "SGB数", "主要来源类别"]
K.table(doc, core, widths=[6.2, 1.7, 1.4, 1.3, 3.4], font_size=8.5)
K.caption(doc, "表 7  发酵食品中数量最多的核心益生菌物种（前 18 位）")

K.figure(doc, f"{F}/fig3_益生菌物种热图.png", 14.0)
K.caption(doc, "图 6  核心益生菌物种在各类发酵食品中的 MAG 数量（前 20 位）")

K.para(doc, "双歧杆菌值得单独说明。全库仅有 155 个 Bifidobacterium MAG、8 个 SGB，且以食品来源的 "
            "Bifidobacterium aquikefiri（72 个）、B. psychraerophilum（38 个）、B. mongoliense（17 个）为主，"
            "临床常用的 B. longum（11 个）、B. animalis（2 个）反而很少。这与双歧杆菌主要栖居于肠道、"
            "在食品中多为外源添加的生态特征一致，也意味着用该资源做双歧杆菌益生性研究时样本不足。")

# ============================================================ 六
K.h1(doc, "六、antiSMASH 次级代谢产物分析", page_break=True)
K.h2(doc, "6.1 方法与输入")
K.para(doc, "antiSMASH 是目前覆盖最全的次级代谢产物基因簇（BGC）识别工具，8.0 版可识别 101 类簇，"
            "包含细菌素、羊毛硫肽、NRPS、PKS、萜类、铁载体等与发酵食品高度相关的类别[7]。"
            "本次未能实际运行，原因见 1.3 节；以下给出输入口径、参数、预期结果与关联分析框架。")
K.para(doc, "输入按 SGB 去重，每个 SGB 取完整度最高、污染最低的一株代表，共 957 个（原核 862 个、真核 95 个）。"
            "去重是必要的：同一 SGB 内不同 MAG 的 BGC 组成通常只差几个单核苷酸变异，全量运行 10,202 个基因组"
            "既浪费算力，也会因近重复序列造成 BGC 家族计数的偏倚。")
t8 = pd.DataFrame([
    ["原核代表基因组", "862", "完整度中位 87.2%，HQ 占 46%"],
    ["真核代表基因组", "95", "以 Saccharomyces、Debaryomyces、Penicillium 为主"],
    ["运行参数（细菌）", "antiSMASH 8.0.4", "--genefinding-tool prodigal --cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go"],
    ["运行参数（真菌）", "antiSMASH 8.0.4", "--taxon fungi --genefinding-tool prodigal-m --cb-general --cb-knownclusters"],
    ["单基因组耗时", "约 3–8 min（16 线程）", "真菌基因组较大，约 10–20 min"],
    ["总耗时估算", "40–80 CPU·h", "可按 20 并发在 3–5 h 内完成"],
], columns=["项目", "设置", "说明"])
K.table(doc, t8, widths=[3.6, 3.4, 8.8], font_size=8.5)
K.caption(doc, "表 8  antiSMASH 运行配置")

K.h2(doc, "6.2 已知产物对应关系")
K.para(doc, "在拿到实测结果之前，可以按分类单元预先判断会检出什么。表 9 与表 10 整理了本资源中 MAG 数量较多的"
            "类群、其已被文献报道的 BGC 类型与代表化合物，同时给出该类群在发酵食品中的功能角色。"
            "这张表的作用是给实测结果提供核对基准：若某属的实测簇类型与表中预期完全不符，应先检查注释或分箱质量。")
LAB_SEL = ["Lactococcus", "Lactococcus lactis", "Lactobacillus", "Lactobacillus helveticus",
           "Lacticaseibacillus", "Lactiplantibacillus plantarum", "Leuconostoc", "Pediococcus",
           "Latilactobacillus sakei", "Limosilactobacillus", "Streptococcus thermophilus", "Bifidobacterium"]
OTH_SEL = ["Propionibacterium freudenreichii", "Bacillus", "Bacillus subtilis", "Staphylococcus",
           "Enterococcus", "Weissella", "Brevibacterium", "Pseudomonas",
           "Penicillium roqueforti", "Scopulariopsis"]

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


K.table(doc, bgc_table(LAB_SEL), widths=[3.5, 1.2, 3.3, 4.0, 3.7, 2.3], font_size=7.3, header_size=7.6)
K.caption(doc, "表 9  乳酸菌相关类群的 BGC 类型与已知产物",
          note="注：产物为已被实验验证的代表化合物，不代表本资源中每一株都能检出；完整 50 行见附表 17。")

K.para(doc, "非乳酸菌类群与真菌的簇型结构完全不同，单列于表 10。芽孢杆菌与假单胞菌以 NRPS/PKS 为主，"
            "青霉属则以生物碱与聚酮为主，这两类正是发酵食品中产物发现与安全风险的两个集中点。")
K.table(doc, bgc_table(OTH_SEL), widths=[3.5, 1.2, 3.3, 4.0, 3.7, 2.3], font_size=7.3, header_size=7.6)
K.caption(doc, "表 10  非乳酸菌类群与真菌的 BGC 类型与已知产物")

K.h2(doc, "6.3 预期 BGC 规模")
K.para(doc, "按各属已报道的单基因组 BGC 数量区间，结合本资源的 SGB 数，可以估算工作量与产出规模。"
            "原核部分预期 1,185–3,695 个 BGC，真核部分 315–872 个。乳酸菌类群虽然基因组小，但簇密度不低，"
            "且高度集中在细菌素与羊毛硫肽两类；Bacillus 与 Pseudomonas 的单基因组簇数最多，是 NRPS/PKS 类新产物的主要来源。")
w = work.head(12)[["属", "SGB数", "单基因组BGC预期下限", "单基因组BGC预期上限",
                   "预期BGC总数(下限)", "预期BGC总数(上限)", "预期主要簇类型"]].copy()
w.columns = ["属", "SGB数", "单株下限", "单株上限", "合计下限", "合计上限", "主要簇类型"]
K.table(doc, w, widths=[3.4, 1.2, 1.5, 1.5, 1.6, 1.6, 5.4], font_size=8)
K.caption(doc, "表 11  主要属的预期 BGC 数量（前 12 属）",
          note="注：单株区间取自文献报道的同属基因组统计值，仅用于估算工作量，不作为实测结果。")

K.h2(doc, "6.4 与发酵过程和益生菌功能的关联")
K.para(doc, "antiSMASH 的结果要与发酵、益生菌挂钩，需要落在三条具体的线索上，而不是泛泛地统计簇的数量。")

K.rich(doc, [("线索一：细菌素与发酵过程的菌群控制。", True),
             ("乳球菌的 nisin 簇、植物乳植杆菌的 plantaricin 簇、片球菌的 pediocin 簇、清酒乳杆菌的 sakacin 簇，"
              "都是 II 类或 I 类细菌素，作用靶点是细胞膜或细胞壁前体，能抑制李斯特菌、芽孢杆菌等腐败与致病菌。"
              "在发酵体系里，产细菌素菌株的丰度变化与腐败菌的消长在时间上互补，这一点可以用 4.4 节的物种谱变化来验证："
              "肉制品中 Latilactobacillus sakei 升至 34.3% 的同时，Brochothrix thermosphacta 从 3.17% 降到 0.49%。"
              "若 antiSMASH 在这些 MAG 中检出完整的 sakacin 操纵子，就可以把“基因存在—表达—群落结果”串成一条链。", False)])

K.rich(doc, [("线索二：风味与质构相关的次级代谢。", True),
             ("短杆菌的类胡萝卜素簇对应奶酪表面的橙红色，Acetobacter 与 Komagataeibacter 的纤维素合成簇对应红茶菌膜的"
              "形成，Leuconostoc 的葡聚糖蔗糖酶簇对应黏度与质构。这类产物不是典型的小分子次级代谢物，"
              "在 antiSMASH 中部分以 PKS/萜类或 EPS 相关区域的形式出现，需要结合 CAZyme 注释一起看。", False)])

K.rich(doc, [("线索三：安全风险相关的簇。", True),
             ("Penicillium roqueforti 的 roquefortine C、PR-toxin 簇，Aspergillus 的霉毒素簇，Staphylococcus 的"
              "毒力相关簇，都是发酵食品风险评估的直接靶点。本资源中 Penicillium 有 83 个 MAG、8 个 SGB，"
              "覆盖蓝纹与白霉奶酪的主要成熟菌，具备做簇层面筛查的条件。", False)])

K.para(doc, "益生菌方向的关联相对间接，但也有明确切入点。一是细菌素基因簇在益生菌株中的分布，"
            "可直接作为拮抗能力的基因组指标；二是双歧杆菌的羊毛硫肽簇在部分菌株中存在，可作为菌株分型的标记；"
            "三是把制剂来源的 42 个 MAG 与食品中同种菌株的 MAG 做簇组成比较，能看出商业菌株是否丢失了某些 BGC，"
            "这在工业化长期传代后并不罕见。")

K.h2(doc, "6.5 执行方案与判读要点")
K.para(doc, "脚本已随报告提供，分为三步：下载 MAG（10_download_mags.sh）、运行 antiSMASH（11_run_antismash.sh）、"
            "汇总结果（12_parse_antismash.py）。第一步按数据集分包下载，只取代表株所在的包，可把 272.5 GB 压缩到 40 GB 左右。")
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
    "可用于食品溯源与真伪鉴别。这是原文“food authentication”方向最直接的延伸。",
    "跨类别共现网络。以 2,483 份样品的属水平丰度为输入构建 SparCC 或 SPIEC-EASI 网络，识别发酵体系中的稳定模块，"
    "重点看乳酸菌—醋酸菌—酵母三方关系。",
    "地理与基质对菌群的影响。元数据含 50 个国家，可用 PERMANOVA 分解国家、类别、工艺三个因素的方差贡献，"
    "回答“地域风味”在微生物层面是否有对应。",
    "发酵剂与非发酵剂菌群的比例。按已知发酵剂名单标注每个 MAG 的来源属性，统计各类别中接种菌与背景菌的比例，"
    "可用于评估工业化程度。",
    "与人体肠道的对接。cFMD 的姊妹资源 cMD（curatedMetagenomicData）可提供人体宏基因组，原文已用 20,000 余份样品"
    "估计食物 SGB 占肠道 3%，可在此基础上细化到类别层面，看哪类发酵食品的 SGB 更容易在肠道中检出[1]。",
    "菌株水平追踪。用 StrainPhlAn 对 Lacticaseibacillus paracasei 等高频种做食品—肠道配对分析，"
    "复现原文提到的食物到肠道传播案例。",
])

K.h2(doc, "B. 需要 MAG 序列")
K.numbered(doc, [
    "BGC 家族聚类。antiSMASH 后用 BiG-SLiCE 把 1,185–3,695 个 BGC 聚成家族，统计食品特有家族与类别富集，"
    "这是把 antiSMASH 从描述性结果变成可比较数据的关键一步。",
    "细菌素专项预测。BAGEL4 与 RiPPer 交叉验证，输出候选细菌素的成熟肽序列、核心肽与预期抑菌谱，"
    "并可进一步做分子对接筛选敏感菌株。",
    "碳水化合物活性酶谱。dbCAN3 注释 CAZy，比较不同类别中淀粉、乳糖、纤维素、果胶降解能力的差异，"
    "直接对应发酵底物利用与终产物。",
    "益生性状基因筛查。耐酸（谷氨酸脱羧酶 gadB）、耐胆盐（胆盐水解酶 bsh）、黏附（黏液结合蛋白）、"
    "抗氧化（硫氧还蛋白）等基因在 2,884 个益生菌 MAG 中的分布，可作为菌株筛选的基因组依据。",
    "耐药基因与可移动元件。AMRFinderPlus 与 mobileOG-db 联合注释，重点是接合质粒与转座子上的四环素、"
    "大环内酯类耐药基因，这是食品安全监管关注点，原文也报告了发酵食品中耐药基因的富集。",
    "噬菌体与 CRISPR。用 geNomad 与 CrisprCasFinder 识别前噬菌体与 CRISPR 阵列，分析发酵剂菌株的噬菌体防御能力，"
    "对发酵工业的噬菌体污染问题有直接价值。",
    "比较基因组与泛基因组。同一 SGB 内食品来源与人体来源的 MAG 做泛基因组分析，找食品特异的辅助基因，"
    "这是区分“过路菌”与“定植菌”的基因组证据。",
    "新种描述。290 个 ufSGB 中完整度 ≥ 90% 的部分，配合 ANI 与 GTDB-Tk 结果，具备新种描述的基因组基础。",
])

K.h2(doc, "C. 需要原始测序数据")
K.numbered(doc, [
    "功能通路重建。HUMAnN3 或 gapseq 从 reads 出发重建代谢通路，可补上 MAG 方法对低丰度成员的系统性遗漏。",
    "宏转录组整合。若有配套 RNA-seq，可把 BGC 的存在与表达对应起来，解决 antiSMASH 只能看“有没有”的问题。",
    "时间序列分析。部分数据集（奶酪成熟、酸面团传代）含时间点信息，可做菌群演替与 BGC 表达的动态建模。",
])

K.para(doc, "优先级建议：A 组的第 1、2、5 项与 B 组的第 1、2、4 项组合起来，可以构成一篇完整的论文框架——"
            "从类别标志物种出发，落到 BGC 家族与细菌素候选，最后用益生性状基因收尾。C 组依赖额外数据，"
            "适合作为后续课题而非当前阶段的工作。")

# ============================================================ 八
K.h1(doc, "八、局限说明")
K.numbered(doc, [
    "类别严重不平衡。乳制品占 67.4% 的 MAG，发酵鱼仅 32 个，发酵豆类、发酵种子均不足 100 个。"
    "任何跨类别比较都受此制约，报告中的类别间差异应理解为趋势而非定论。",
    "批次效应难以完全消除。59 个数据集的 DNA 提取方法、测序平台、读长与建库策略各不相同，"
    "元数据虽记录了提取试剂盒与平台，但无法完全校正。原文对此做了标准化处理，残余效应仍然存在[15]。",
    "MAG 方法本身的偏倚。高丰度、低复杂度的群落（如接种发酵）更容易得到高质量 MAG，"
    "低丰度成员与高复杂度群落（如传统自然发酵）被系统性低估，这会放大发酵剂菌株的表观重要性。",
    "SGB 划分依赖参考数据库。kSGB 的定义是簇内至少有一个参考基因组，因此参考库覆盖好的类群（乳球菌、乳杆菌）"
    "更容易被判为已知种，参考库薄弱的类群（发酵鱼、发酵豆类中的新颖类群）则集中落在 uSGB/ufSGB，"
    "新颖性比例在类别间的差异有一部分是数据库偏倚造成的。",
    "antiSMASH 部分为预判而非实测。第六章的产物对应关系来自文献，BGC 数量为区间估算，"
    "均需在拿到 MAG 序列后以实测结果替换。",
    "益生菌名单的边界问题。种级名单依据 QPS 与国内名单整理，但同一物种内不同菌株的益生功能差异很大，"
    "基因组层面的“益生菌物种”不等于“益生菌菌株”，这一点在解读表 7 时需保留。",
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
    ["00", "MAG主表_全部.csv", "10,899 个 MAG 的完整注释与元数据合并表", "10,899 行"],
    ["01", "发酵MAG总表.csv", "发酵样品的全部 MAG，含类别、质量、益生菌归属", "10,202 行"],
    ["02", "按发酵种类汇总.csv", "10 个发酵类别的统计汇总", "11 行"],
    ["03", "属水平MAG数量矩阵.csv", "前 40 属 × 11 类别的计数矩阵", "40 × 11"],
    ["04", "SGB水平汇总_含发酵类别.csv", "1,144 个 SGB 的分类、来源、发酵类别分布", "1,144 行"],
    ["05", "益生菌制剂来源MAG表.csv", "14 份制剂样品的 42 个 MAG", "42 行"],
    ["06", "益生菌物种MAG全库表.csv", "28 个核心益生菌种的 2,884 个 MAG", "2,884 行"],
    ["07", "益生菌物种x发酵类别矩阵.csv", "益生菌物种在各类别中的分布", "—"],
    ["08", "发酵食品真核MAG表.csv", "757 个真核 MAG", "757 行"],
    ["09", "antiSMASH输入MAG清单_每SGB代表株.csv", "957 个代表株（P1/P2 优先级）", "957 行"],
    ["10-16", "物种谱系列", "发酵与非发酵的物种差异、类别丰度、alpha 多样性", "8 个表"],
    ["17", "antiSMASH产物知识表.csv", "50 个分类单元的簇类型与代表产物", "50 行"],
    ["18-19", "BGC预期工作量表", "按属估算的 BGC 数量", "2 个表"],
    ["20", "发酵类型明细_按type.csv", "80 个食品类型的样品、MAG、优势种", "80 行"],
    ["—", "figures/", "图 1–6 的 PNG 文件（300 dpi）", "6 个"],
    ["—", "scripts/", "数据整理、统计、绘图与 antiSMASH 流程脚本", "14 个"],
], columns=["编号", "文件", "内容", "规模"])
K.table(doc, files, widths=[1.3, 5.4, 7.3, 2.2], font_size=8)
K.caption(doc, "附表 A  随报告交付的数据文件")

K.para(doc, "表 4 的类别之下还有一层更细的 type 划分，共 80 类。下表给出 MAG 数最多的 15 类，"
            "含样品量、地理覆盖、优势种与该类型的代表 MAG，可用于挑选具体工艺做深入分析。完整 80 类见附表 20。")
td = pd.read_csv(f"{T}/20_发酵类型明细_按type.csv", encoding="utf-8-sig")
td = td[["发酵类别", "食品类型", "样品数", "数据集数", "国家数", "MAG数", "HQ数", "SGB数", "属数", "优势种Top3"]].head(15)
td.columns = ["类别", "类型", "样品", "数据集", "国家", "MAG", "HQ", "SGB", "属", "优势种（MAG 数）"]
K.table(doc, td, widths=[2.4, 2.6, 1.0, 1.1, 1.0, 1.0, 0.9, 0.9, 0.8, 6.0], font_size=7.4, header_size=7.8)
K.caption(doc, "附表 B  发酵食品类型明细（前 15 类）")

doc.save(OUT)
print("saved", OUT, os.path.getsize(OUT) / 1024, "KB")
