# -*- coding: utf-8 -*-
"""生成【汇报版】报告 DOCX —— cFMD v1.3.2，无文献标注"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import docxkit as K

T = "/home/user/skills/cfmd_latest/tables"
F = "/home/user/skills/cfmd_latest/figures"
OUT = "/home/user/skills/cfmd_latest/文档/cFMD_v1.3.2_发酵与益生菌MAG分析报告_汇报版.docx"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

s = pd.read_csv(f"{T}/02_按发酵种类汇总.csv", encoding="utf-8-sig")
s10 = s[s["发酵类别"] != "合计"].copy()
tier = pd.read_csv(f"{T}/22_益生菌分层汇总.csv", encoding="utf-8-sig")
strict = pd.read_csv(f"{T}/21_益生菌严格名单MAG表.csv", encoding="utf-8-sig")
pair = pd.read_csv(f"{T}/15_同基质发酵vs非发酵多样性.csv", encoding="utf-8-sig")
work = pd.read_csv(f"{T}/18_antiSMASH_BGC预期工作量_按属.csv", encoding="utf-8-sig")
euk = pd.read_csv(f"{T}/19_antiSMASH_BGC预期工作量_真核属.csv", encoding="utf-8-sig")

doc = K.new_document()
K.add_header_text(doc, "cFMD v1.3.2 食品微生物组 MAG 分析")
K.add_page_number_footer(doc, "汇报版")

K.title(doc,
        "发酵与益生菌方向的食品 MAG 资源盘点",
        "cFMD v1.3.2：4,125 份食品宏基因组、18,180 个 MAG、1,654 个 SGB",
        "数据：curatedFoodMetagenomicData v1.3.2（GitHub SegataLab/cFMD，2026-06-18）\n"
        "分析日期：2026 年 10 月")

doc.add_paragraph()
K.h2(doc, "目  录")
for line in ["一、要点",
             "二、数据与方法",
             "三、库的整体情况",
             "四、发酵模块",
             "五、益生菌",
             "六、antiSMASH 与次级代谢产物",
             "七、下一步做什么",
             "八、局限",
             "附  文件清单"]:
    K.para(doc, line, indent=False, space_after=1)

# ============================================================ 一
K.h1(doc, "一、要点", page_break=True)
K.numbered(doc, [
    "cFMD 已从论文版 v1.1.0 更新到 v1.3.2（2026-06-18）。总数从 2,533 份样品、10,899 个 MAG 增至 "
    "4,125 份、18,180 个；SGB 从 1,144 增至 1,654。此前用 v1.1.0 的表做统计，与别人按最新表整理的结果对不上，"
    "差的是版本，不是口径。本文全部数字基于 v1.3.2。",
    "发酵样品 3,293 份，占 79.8%，重建 15,446 个 MAG、1,142 个 SGB。乳制品独占 72.8% 的发酵 MAG，"
    "发酵饮料 13.9%，其余八个类别合计不到 14%。",
    "乳酸菌相关 23 个属共 8,183 个 MAG，占发酵原核 MAG 的 56.1%。发酵与同基质非发酵样品的物种多样性差异"
    "在肉制品与果蔬上显著（Shannon 1.89 对 1.22、2.52 对 1.63），乳制品与鱼不显著。",
    "益生菌要分四个口径看：制剂样品 42 个 MAG；名单内 28 个种、4,925 个 MAG；属级放宽的乳酸菌与双歧杆菌"
    "类群 6,385 个；另有发酵剂/QPS 相关 1,869 个、肠球菌等 292 个。对外只报前两个，第三个要注明是类群口径。",
    "antiSMASH 没有实际运行：本机没有 antiSMASH、HMMER、Prodigal，也没有 MAG 序列（Zenodo 上的序列集合"
    "约 272 GB，当前环境无法下载）。按 SGB 去重得到 1,142 个代表基因组，按文献报道的单基因组簇数估算，"
    "原核 1,461–4,554 个 BGC、真核 315–878 个。这是工作量估计，不是结果。",
])

# ============================================================ 二
K.h1(doc, "二、数据与方法", page_break=True)
K.para(doc, "数据取自 cFMD 仓库主分支的三个总表：cFMD_metadata.tsv（4,125 行、32 列，样品级元数据）、"
            "cFMD_mags_list.tsv（18,180 行、20 列，MAG 级注释与质量）、cFMD_datasets.tsv（109 行，数据集索引）。"
            "v1.3.2 取消了顶层的 SGB 汇总表，SGB 级信息需要在 MAG 清单上自行聚合，本文的 SGB 表、类别表、"
            "属种矩阵都是这样重建的。物种谱取自 cFMD_data/<dataset>/ 下的 107 个 TSV，覆盖 4,067 份样品。")
K.para(doc, "四条口径：")
K.numbered(doc, [
    "发酵与否直接取 fermented 字段（F/NF），不按类别名反推。乳制品里有 203 份非发酵样品（鲜奶 132、"
    "奶酪盐水 53、生乳 18），单独留作同基质对照。",
    "MAG 质量按完整度 ≥90%、污染 <5% 记 HQ，完整度 ≥50%、污染 <5% 记 MQ。同时满足质量与 SGB 归属的 "
    "17,621 个 MAG 进入分析，占全库 96.9%。",
    "SGB 的新颖性类型（kSGB/uSGB/ufSGB）源表按 MAG 标注，有 21 个 SGB 被标了两种；本文按 SGB 内多数"
    "MAG 的标注统一，票数相同时取 uSGB。",
    "物种谱文件本身已是百分比，直接用于 alpha 多样性与丰度比较，不再缩放。",
])

# ============================================================ 三
K.h1(doc, "三、库的整体情况")
K.para(doc, "4,125 份样品来自 109 个数据集、54 个国家，测序碱基合计 25.09 Tb。乳制品 2,336 份，占样品总数的 56.6%；"
            "发酵肉、发酵饮料、发酵果蔬各在 60–460 份之间；发酵鱼、发酵薯类、发酵豆类都不到 30 份。"
            "真核 MAG 979 个，其中 848 个来自发酵样品，含酒精饮料的真核占比最高（44.7%），乳制品最低（3.8%）。")
d1 = pd.DataFrame([
    ["样品", "4,125", "发酵 3,293、非发酵 832"],
    ["数据集 / 国家", "109 / 54", "v1.0.0 59、v1.2.1 26、v1.3.1 2、v1.3.2 22"],
    ["MAG 总数", "18,180", "细菌 17,048、真核 979、古菌 17、未定 136"],
    ["分析用 MAG", "17,621", "质量合格且有 SGB 编号"],
    ["SGB", "1,654", "已知种 1,054、未知种 374、食品新种 226"],
    ["发酵 MAG / SGB", "15,446 / 1,142", "HQ 7,431、MQ 8,015"],
], columns=["项目", "数值", "说明"])
K.table(doc, d1, widths=[3.6, 5.4, 7.2], font_size=8.8)
K.caption(doc, "表 1  数据集规模")
K.para(doc, "600 个 SGB 没有参考基因组，占 36.3%，其中 226 个只在食品样品中出现。与 v1.1.0 的 290 个相比，"
            "食品新种净减 64 个。期间既有新数据集带来的新食品种，也有旧类群因参考基因组补齐转为已知种，后者占多数。"
            "这 600 个仍是该资源相对人体肠道库的主要增量。")

# ============================================================ 四
K.h1(doc, "四、发酵模块", page_break=True)
K.para(doc, "15,446 个发酵 MAG 中，原核 14,598 个、真核 848 个，HQ 占 48.1%。分属 1,142 个 SGB：已知种 749、"
            "未知种 244、食品新种 149。十个类别之间极不平衡，表 2 是全表。")
d2 = s10[["发酵类别", "样品数", "数据集数", "国家数", "MAG总数", "原核MAG", "真核MAG",
          "高质量MAG(HQ)", "SGB总数", "已知种SGB(kSGB)", "属数", "已定名种数"]].copy()
d2.columns = ["类别", "样品", "数据集", "国家", "MAG", "原核", "真核", "HQ", "SGB", "kSGB", "属", "种"]
K.table(doc, d2, widths=[3.4, 1.3, 1.3, 1.1, 1.5, 1.3, 1.1, 1.3, 1.2, 1.2, 1.0, 1.0], font_size=8.2)
K.caption(doc, "表 2  各发酵类别的样品、MAG 与 SGB")

K.para(doc, "乳制品 2,336 份、11,242 个 MAG，占发酵 MAG 的 72.8%，来自 48 个数据集、37 个国家。主导种是"
            "Lactococcus lactis（940 个）、Streptococcus thermophilus（802 个）、Lacticaseibacillus paracasei"
            "（716 个）、Lactococcus cremoris（490 个）、Lactobacillus delbrueckii（474 个）、L. helveticus（405 个）。"
            "优势种与商业发酵剂配方高度重合，这与 48 个数据集以欧洲奶酪专项为主有关。")
K.para(doc, "发酵饮料 456 份、2,144 个 MAG，水开菲尔占 85%，其余是康普茶、米醋、咖啡发酵、Pulque 与 Pozol。"
            "菌群由三块叠加：Liquorilactobacillus（403 个）、Acetobacter（259 个）、Lacticaseibacillus（251 个）。"
            "含酒精饮料只有 48 份，真核却占 44.7%，"
            "Saccharomyces cerevisiae 在物种谱里平均占 41.0%，是全部类别中最高的。")
K.para(doc, "发酵肉 168 份、607 个 MAG，优势种为 Latilactobacillus sakei（物种谱占比 36.6%）、Staphylococcus xylosus、"
            "Latilactobacillus curvatus，属典型的低温慢发酵香肠群落。发酵谷物 83 份、244 个 MAG，以酸面团为主，"
            "Lactiplantibacillus plantarum、Levilactobacillus brevis、Fructilactobacillus sanfranciscensis 三分天下。"
            "发酵种子在 v1.3.2 里扩充最快，从 13 份增至 65 份，可可豆发酵贡献主体，Acetobacter pasteurianus "
            "在物种谱中占 27.8%，符合可可豆堆肥式发酵的醋酸菌主导特征。")
K.para(doc, "长尾类别要谨慎。发酵鱼 25 份样品来自两个数据集（韩国洪鱼 5 份、中国油茶 20 份），MAG 却有 214 个，"
            "集中在 Lactiplantibacillus pentosus 与 L. plantarum，两个数据集的工艺差异远大于同类别内的重复；"
            "发酵豆类 26 份、172 个 MAG，以 Bacillus velezensis、Enterococcus faecium、Weissella confusa 为主，"
            "Bacillus 的比例明显高于其他类别，提示以细菌发酵为主的亚洲豆制品与乳酸发酵体系不同。"
            "发酵薯类、发酵果蔬各只有 24 与 62 份，只能作趋势描述。")
K.figure(doc, f"{F}/fig1_类别MAG数量.png", 15.2)
K.caption(doc, "图 1  各发酵类别的 MAG 数量与质量构成")
K.figure(doc, f"{F}/fig2_优势属热图.png", 15.2)
K.caption(doc, "图 2  前 22 个属在 10 个类别中的 MAG 数量")

K.para(doc, "同基质对照在这一版才够用。v1.3.2 的非发酵样品增加到肉 204 份、鱼 155 份、果蔬 237 份，"
            "比 v1.1.0 分别多出 157、141、212 份，其中有物种谱、能进入多样性计算的为 197、150、231 份。结果与预期一致但幅度不同："
            "肉制品与果蔬的 Shannon 指数在发酵后显著下降，乳制品与鱼几乎没有变化。乳制品本身多样性就低"
            "（1.13 对 1.08，P=0.79），发酵与否不改变这一格局；鱼的非发酵对照只有 150 份有物种谱且来源集中，"
            "P=0.53 不能理解为“发酵不影响”。")
d3 = pair.copy()
d3.columns = ["比较", "非发酵 n", "发酵 n", "非发酵 Shannon", "发酵 Shannon", "P 值"]
d3["P 值"] = d3["P 值"].map(lambda x: "<0.0001" if x < 1e-4 else f"{x:.3f}")
K.table(doc, d3, widths=[3.2, 2.2, 2.0, 3.4, 3.2, 2.2], font_size=8.6)
K.caption(doc, "表 3  同基质条件下发酵与非发酵的 alpha 多样性")
K.para(doc, "物种层面看得更清楚：发酵组里 Lactococcus lactis 平均 14.02%、Streptococcus thermophilus 15.75%、"
            "Lactococcus cremoris 9.69%，对应的非发酵组只有 1.43%、4.33%、0.65%；反向富集的是 Brochothrix "
            "thermosphacta（4.57%）、Pseudomonas fragi（3.74%）、P. immobilis（3.07%）等冷藏腐败菌。"
            "发酵对腐败菌的抑制在物种层面是干净的信号，可以直接用于货架期与工艺评估。")

# ============================================================ 五
K.h1(doc, "五、益生菌", page_break=True)
K.para(doc, "“益生菌 MAG 有多少”这个问题没有单一答案，取决于把边界画在哪里。四组数字放在一起，差别一目了然。")
d4 = tier.copy()
d4.columns = ["层级", "种数", "SGB", "MAG", "HQ"]
K.table(doc, d4, widths=[8.2, 2.0, 2.0, 2.2, 2.0], font_size=8.8)
K.caption(doc, "表 4  益生菌相关的四个口径")
K.para(doc, "制剂样品是唯一确定来自益生菌产品的部分：14 份样品（美国 10、意大利 4）、42 个 MAG、21 个 SGB。"
            "平均完整度 76.7%，HQ 只有 16 个，低于发酵食品整体的 83.5%。制剂配方里菌株种类少、辅料 DNA 占比高，"
            "组装效果本来就差一档，做下游分析建议只取 HQ 的 16 个。")
K.para(doc, "名单内 28 个种共 4,925 个 MAG，HQ 1,968 个。分布高度集中：乳制品 4,124 个（83.7%）、发酵饮料 425 个、"
            "发酵谷物 105 个、发酵种子 69 个，其余六个类别合计不到 210 个。乳制品之外，名单内物种多是辅助菌，"
            "丰度低、MAG 数少，做统计时要按类别分层。")
sc = strict.groupby("物种").agg(MAG=("MAG_id", "size"),
                               HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                               SGB=("SGB_id", "nunique"),
                               主要来源=("发酵类别中文", lambda x: x.value_counts().index[0]))
sc = sc.sort_values("MAG", ascending=False).reset_index()
sc.columns = ["物种", "MAG", "HQ", "SGB", "主要来源"]
K.table(doc, sc, widths=[6.6, 1.4, 1.2, 1.2, 3.6], font_size=8.2)
K.caption(doc, "表 5  名单内 28 个益生菌种的 MAG 数量")

K.para(doc, "属级放宽到 18 个乳杆菌相关属加双歧杆菌属，得到 133 个种、6,385 个 MAG。多出来的 105 个种不是随机噪声，"
            "而是集中在两类基质：水开菲尔与康普茶来源的 Liquorilactobacillus satsumensis（200 个）、L. nagelii（129 个）、"
            "Bifidobacterium aquikefiri（73 个），以及奶酪与发酵肉来源的 Lentilactobacillus parabuchneri（136 个）、"
            "Lactobacillus kefiranofaciens（89 个）。这些种缺益生功能评价，也不在监管名单上，但恰恰是这份资源"
            "相对商业菌株库的增量。")
K.para(doc, "双歧杆菌要单独说。全库 Bifidobacterium 只有 192 个 MAG，以食品来源的 B. aquikefiri、B. psychraerophilum、"
            "B. mongoliense 为主，临床常用的 B. longum 与 B. animalis 分别只有 11 个和 2 个。双歧杆菌主要栖居肠道，"
            "食品中的数量取决于是否外源添加，用它做益生性研究样本量不够。")
K.figure(doc, f"{F}/fig3_益生菌物种热图.png", 14.2)
K.caption(doc, "图 3  前 20 个乳酸菌与双歧杆菌种在各类别中的分布")

# ============================================================ 六
K.h1(doc, "六、antiSMASH 与次级代谢产物", page_break=True)
K.para(doc, "先说明状态：antiSMASH 没有跑。运行它需要 MAG 序列，而序列在 Zenodo 上按数据集打包，全量约 272 GB，"
            "当前环境既连不上 Zenodo，也没有足够磁盘与内存；分析环境里没有 antiSMASH、HMMER、Prodigal 和 conda。"
            "下面给的是输入清单、按文献推算的规模，以及拿到序列后的执行方案。")
K.para(doc, "输入按 SGB 去重，每个 SGB 取完整度最高、污染最低的一株，共 1,142 个代表基因组（原核 1,045、真核 97）。"
            "同一 SGB 内不同 MAG 的簇结构差异通常小于测序噪声，去重不会丢信息，能把计算量压到十分之一。"
            "清单表 09 里已标好 P1/P2 优先级：P1 为名单内益生菌种与食品新种，共 176 个，P2 为其余 869 个。")
d6 = work.head(12)[["属", "SGB数", "单基因组BGC预期下限", "单基因组BGC预期上限",
                    "预期BGC总数(下限)", "预期BGC总数(上限)", "预期主要簇类型"]].copy()
d6.columns = ["属", "SGB", "单株下限", "单株上限", "合计下限", "合计上限", "主要簇类型"]
_map = {
    "bacteriocin/lanthipeptide 为主，罕见 NRPS/PKS": "细菌素/羊毛硫肽",
    "bacteriocin 为主；部分种带 head-to-tail 环肽": "细菌素",
    "blp/thermophilin 类细菌素": "blp/thermophilin 类细菌素",
    "bacteriocin / RiPP-like 为主": "细菌素/RiPP",
    "bacteriocin + EPS/葡聚糖簇": "细菌素+EPS",
    "bacteriocin": "细菌素",
    "铁载体、类胡萝卜素萜类": "铁载体/萜类",
    "纤维素合成、少见 PKS": "纤维素合成",
    "铁载体、NRPS": "铁载体/NRPS",
    "plantaricin 多拷贝簇；偶见 lanthipeptide": "plantaricin/羊毛硫肽",
    "铁载体": "铁载体",
}
d6["主要簇类型"] = d6["主要簇类型"].map(lambda x: _map.get(x, x))
K.table(doc, d6, widths=[4.4, 1.3, 1.6, 1.6, 1.9, 1.9, 4.0], font_size=8.2)
K.caption(doc, "表 6  主要属的 BGC 数量估算（前 12 属）")
K.para(doc, "原核合计 1,461–4,554 个，真核 315–878 个。真核部分有四到六成落在 Penicillium（8 个 SGB，160–320 个）"
            "与 Scopulariopsis（3 个 SGB，30–75 个）。乳酸菌的基因组小，单株一般 2–7 个簇，但簇密度不低，"
            "且高度集中在细菌素与羊毛硫肽，这是它们能压制腐败菌的分子基础。")
K.para(doc, "拿到结果后值得追三条线。一是细菌素：乳球菌的 nisin、植物乳植杆菌的 plantaricin、片球菌的 pediocin、"
            "清酒乳杆菌的 sakacin，都是已验证的 I/II 类细菌素，可直接对应发酵过程中的菌群控制能力。"
            "二是风味与质构：短杆菌的类胡萝卜素决定奶酪表面颜色，Acetobacter 与 Komagataeibacter 的纤维素合成"
            "决定红茶菌膜，Leuconostoc 的葡聚糖蔗糖酶决定黏度，这三类产物不是“次级代谢副产物”，而是工艺指标。"
            "三是安全：Penicillium roqueforti 的 roquefortine C 与 PR-toxin 簇、Aspergillus 的霉毒素簇、"
            "Staphylococcus 的毒力簇，是发酵食品风险评估的直接靶点。")
K.para(doc, "执行按三步走：10_download_mags.sh 按数据集分包下载，只取清单里的代表株；11_run_antismash.sh "
            "以 --cfinder-molarmass 和 --taxon 参数批量运行，输出 genbank 与 JSON；12_parse_antismash.py 汇总簇类型、"
            "产物预测与基因坐标。判读时把 HQ 与 MQ 分开统计：完整度 50%–70% 的基因组常缺簇的调控区或模块，"
            "会低估总数；contig 断裂还会把一个簇切成两段，造成重复计数。")

# ============================================================ 七
K.h1(doc, "七、下一步做什么")
K.para(doc, "按所需数据分三档，前两档与现有资源匹配，第三档要另找数据。")
K.para(doc, "只用总表就能做的四件：")
K.bullets(doc, [
    "类群指示物种。用 indicspecies 在 10 个发酵类别上找标志种，输出每类的诊断性分类单元。发酵种子与发酵鱼"
    "的样品量在 v1.3.2 里刚够支撑这一分析，是新的切入点。",
    "跨类别共现网络。以 4,067 份样品的属水平丰度建 SparCC 网络，重点看乳酸菌—醋酸菌—酵母的三方关系，"
    "水开菲尔与可可豆发酵是两个天然的比较体系。",
    "地理与工艺的方差分解。元数据有 54 个国家，可用 PERMANOVA 拆国家、类别、工艺三个因素，"
    "回答“地域风味”在微生物层面有没有对应。意大利、西班牙、爱尔兰样本量最大，也可做国家内部比较。",
    "发酵剂与背景菌的比例。按已知发酵剂名单给每个 MAG 打标签，统计各类别中接种菌与自然发酵菌的比例，"
    "可作为工业化程度的代理指标。",
])
K.para(doc, "需要 MAG 序列的三件（与第六章共用一次下载）：")
K.bullets(doc, [
    "BGC 家族聚类。antiSMASH 之后用 BiG-SLiCE 把上千个 BGC 聚成家族，统计食品特有家族与类别富集，"
    "这是把描述性结果变成可比较数据的关键一步。",
    "细菌素专项。BAGEL4 与 RiPPer 交叉验证，输出候选细菌素的成熟肽序列与预测抑菌谱，"
    "再与发酵食品中的敏感菌做对接。",
    "益生性状与耐药基因。dbCAN3 注释 CAZy，AMRFinderPlus 注释耐药基因，重点看接合质粒与转座子上的"
    "四环素、大环内酯类基因，这是监管关注点。",
])
K.para(doc, "需要原始测序数据的两件：HUMAnN3 或 gapseq 重建功能通路，补 MAG 方法对低丰度成员的系统性遗漏；"
            "以及与人体宏基因组（cMD）配对做菌株追踪，复现原文报告的食物到肠道传播。后者的价值最高，"
            "但需要另外申请数据权限。")
K.para(doc, "如果只做一件事，建议做“类别指示物种 + 名单外乳酸菌的基因组特征”这一组合：前者用现有总表两周内可出，"
            "后者只需下载这 105 个种的代表基因组（105 个 MAG，约 300 MB），能把“传统发酵食品里有哪些未被认识的"
            "益生候选”这个问题回答到菌株水平。")

# ============================================================ 八
K.h1(doc, "八、局限")
K.numbered(doc, [
    "类别严重不平衡。乳制品占 72.8% 的发酵 MAG，发酵薯类只有 123 个、发酵果蔬 149 个。跨类别比较只能看趋势，"
    "不能当定论。",
    "批次效应。109 个数据集的提取方法、平台、读长各不相同，元数据虽有记录，无法完全校正。",
    "MAG 方法本身有偏。高丰度、低复杂度的群落（接种发酵）更容易得到高质量基因组，低丰度成员被系统性低估，"
    "这会放大发酵剂菌株的表观重要性。直接用 MAG 数代表物种重要性并不可靠。",
    "两个版本的数据不能混用。本文全部基于 v1.3.2；与他人的 v1.1.0 结果并列时必须在表头注明版本，"
    "否则样品数、MAG 数、SGB 数会出现 30%–60% 的表面差异。",
    "antiSMASH 部分是估算。表 6 的区间来自文献报道的单基因组簇数，不是本资源的实测值，"
    "在拿到序列前不要引用为结果。",
])

# ============================================================ 附
K.h1(doc, "附  文件清单", page_break=True)
files = pd.DataFrame([
    ["00", "MAG主表_全部.csv", "18,180 个 MAG 的合并注释", "18,180 行"],
    ["01", "发酵MAG总表.csv", "发酵样品全部 MAG", "15,446 行"],
    ["02", "按发酵种类汇总.csv", "10 个类别的统计", "11 行"],
    ["04", "SGB水平汇总.csv", "1,654 个 SGB", "1,654 行"],
    ["05", "益生菌制剂来源MAG表.csv", "制剂来源 42 个 MAG", "42 行"],
    ["06", "益生菌物种MAG全库表.csv", "属级放宽口径 6,385 个", "6,385 行"],
    ["21", "益生菌严格名单MAG表.csv", "名单内 28 个种 4,925 个", "4,925 行"],
    ["22", "益生菌分层汇总.csv", "四个口径计数", "5 行"],
    ["09", "antiSMASH输入清单.csv", "1,142 个代表基因组", "1,142 行"],
    ["17-19", "antiSMASH 知识表与工作量", "50 个分类单元的产物对应与估算", "3 个表"],
    ["10-16", "物种谱与多样性", "发酵/非发酵差异、alpha 多样性", "8 个表"],
    ["20", "发酵类型明细.csv", "91 个发酵类型的明细", "91 行"],
    ["—", "figures/", "图 1–6，PNG 300 dpi", "6 个"],
], columns=["编号", "文件", "内容", "规模"])
K.table(doc, files, widths=[1.4, 5.6, 7.0, 2.0], font_size=8.2)
K.caption(doc, "附表  随报告交付的数据文件")
K.para(doc, "逐条 MAG 编号、SGB 归属与质量指标都在 00 主表里，按 dataset_id 与 MAG_id 可以回溯到原始数据集。"
            "需要重跑时按 scripts/ 下的编号顺序执行：01 建表、02 物种谱、04–06 图表、08/09 报告。")

doc.save(OUT)
print("saved", OUT, os.path.getsize(OUT) // 1024, "KB")
