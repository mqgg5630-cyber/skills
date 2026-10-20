# -*- coding: utf-8 -*-
"""生成【汇报精简版】报告 DOCX（无参考文献、无说明性套话）"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import docxkit as K

T = "/home/user/skills/cfmd_deliverables/tables"
F = "/home/user/skills/cfmd_deliverables/figures"
OUT = "/home/user/skills/cfmd_deliverables/文档/cFMD发酵与益生菌MAG分析_汇报版.docx"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

s = pd.read_csv(f"{T}/02_按发酵种类汇总.csv")
s10 = s[s["发酵类别"] != "合计"].copy()
bgc = pd.read_csv(f"{T}/17_antiSMASH产物知识表_文献依据.csv")
work = pd.read_csv(f"{T}/18_antiSMASH_BGC预期工作量_按属.csv")
pair = pd.read_csv(f"{T}/15_同基质发酵vs非发酵多样性.csv")
tab6 = pd.read_csv(f"{T}/06_益生菌物种MAG全库表.csv", encoding="utf-8-sig")
probmag = pd.read_csv(f"{T}/05_益生菌制剂来源MAG表.csv", encoding="utf-8-sig")

doc = K.new_document()
K.add_header_text(doc, "cFMD 发酵与益生菌 MAG 分析")
K.add_page_number_footer(doc, "")

# ============================================================ 题头
p = doc.add_paragraph()
p.paragraph_format.space_before = K.Pt(8)
p.paragraph_format.space_after = K.Pt(2)
K._set_run(p.add_run("食品宏基因组资源 cFMD 的发酵与益生菌 MAG 分析"), 17, True, K.DARK, K.HEAD_CN)
p2 = doc.add_paragraph()
p2.paragraph_format.space_after = K.Pt(3)
K._set_run(p2.add_run("2,533 份食品宏基因组     10,899 个 MAG     957 个发酵相关 SGB"), 9.5, False, K.GREY)
p3 = doc.add_paragraph()
p3.paragraph_format.space_after = K.Pt(10)
K._border(p3._p.get_or_add_pPr(), sz="8", color="2E5E8E")

# ============================================================ 一
K.h1(doc, "一、数据")
K.para(doc, "使用 curatedFoodMetagenomicData（cFMD）v1.1.0 的公开总表。该版本含 59 个数据集、2,533 份食品宏基因组、"
            "50 个国家，测序碱基合计 14.7 Tb。"
            "表中记录 10,899 个 MAG、1,144 个 SGB；其中 613 个 SGB 含参考基因组（已知种），531 个不含参考基因组，"
            "290 个为仅见于食品样品的新种。2,483 份样品有物种水平相对丰度谱。", indent=True)

t1 = pd.DataFrame([
    ["食品宏基因组", "2,533 份", "59 个数据集，50 个国家，14.7 Tb"],
    ["MAG 总数", "10,899 个", "细菌 10,097、古菌 15、真核 787"],
    ["SGB 总数", "1,144 个", "原核 1,036、真核 108"],
    ["已知种 / 未知种 / 食品新种", "613 / 241 / 290", "未知种无参考基因组"],
    ["发酵样品", "2,262 份", "占 89.3%"],
    ["发酵样品 MAG", "10,202 个", "原核 9,445、真核 757；分属 957 个 SGB"],
    ["MAG 质量", "HQ 5,203 / MQ 4,998", "完整度 ≥90% 且污染 <5% 记 HQ，另有 1 个未达 MQ"],
], columns=["项目", "规模", "说明"])
K.table(doc, t1, widths=[4.4, 3.6, 7.6], font_size=8.6)
K.caption(doc, "表 1  数据概况")

K.para(doc, "MAG 序列未下载（Zenodo 压缩包 9.8 GB，按数据集拆分后 272.5 GB），第四节的 antiSMASH 部分为产物预判，"
            "输入清单与运行脚本已备好，可在服务器上直接补跑。")

# ============================================================ 二
K.h1(doc, "二、发酵模块", page_break=True)
K.para(doc, "元数据中发酵样品分 10 个类别。乳制品独占 67.4% 的 MAG，发酵饮料 19.7%，两者合计接近九成；"
            "发酵鱼仅 32 个 MAG（5 份样品、1 个数据集）。跨类别比较只能看趋势，不能当定论。")

d = s10.copy()
d = d[["发酵类别", "样品数", "MAG总数", "原核MAG", "真核MAG", "高质量MAG(HQ)", "SGB总数", "属数", "已定名种数"]]
d.columns = ["发酵类别", "样品", "MAG", "原核", "真核", "HQ", "SGB", "属", "种"]
K.table(doc, d, widths=[3.0, 1.4, 1.5, 1.4, 1.4, 1.3, 1.4, 1.2, 1.2], font_size=8.6)
K.caption(doc, "表 2  各类别的 MAG 与 SGB 数量")

K.figure(doc, f"{F}/fig1_类别MAG数量.png", 14.6)
K.caption(doc, "图 1  各类别 MAG 数量与质量")

adv = s10[["发酵类别", "优势属Top3", "优势种Top3"]].copy()
adv.columns = ["发酵类别", "优势属（MAG 数）", "优势种（MAG 数）"]
K.table(doc, adv, widths=[2.4, 6.6, 6.6], font_size=7.8)
K.caption(doc, "表 3  各类别的优势属与优势种")

K.para(doc, "乳酸菌相关 23 个属合计 5,273 个 MAG，占发酵样品原核 MAG 的 55.8%，是明确的主体。"
            "种水平前四位依次是 Lactococcus lactis（655）、Streptococcus thermophilus（418）、"
            "Lacticaseibacillus paracasei（412）、Lactococcus cremoris（394），均为发酵剂核心菌，"
            "且数量显著高于第五位（Leuconostoc mesenteroides，222）。MAG 数量与菌株重要性不完全等价，"
            "接种发酵的高丰度会系统性抬高发酵剂的表观占比。")

K.para(doc, "类别之间的差异体现在三条带上：乳制品与发酵饮料以 Lactococcus、Lactobacillus、Lacticaseibacillus、"
            "Leuconostoc、Liquorilactobacillus 为主；发酵肉与乳制品表面以 Staphylococcus、Latilactobacillus、"
            "Brevibacterium、Corynebacterium 为主；发酵豆类与发酵种子以 Weissella、Enterococcus、Bacillus 为主。"
            "同一属在不同类别中的占比差异来自基质与工艺，而非属本身的分布偏好。")
K.figure(doc, f"{F}/fig2_优势属热图.png", 13.6)
K.caption(doc, "图 2  优势属在各类别中的 MAG 数量")

K.h2(doc, "与同基质非发酵样品的对照")
K.para(doc, "元数据含未发酵的鲜肉、鲜鱼与生鲜果蔬，可作同基质对照。发酵样品的物种水平 Shannon 指数普遍低于"
            "同基质生样，肉与鱼达到统计显著（表 4），说明发酵伴随群落收敛。果蔬样本量小，未达显著。")
K.table(doc, pair, widths=[5.4, 1.8, 1.5, 2.5, 2.5, 1.5], font_size=8.4)
K.caption(doc, "表 4  同基质发酵与非发酵样品的 alpha 多样性（Mann-Whitney U 检验）")

K.para(doc, "物种层面的升与降更能说明问题。肉制品中 Pseudomonas fragi 由 6.20% 降到 0.13%，"
            "Brochothrix thermosphacta 由 3.17% 降到 0.49%，而 Latilactobacillus sakei 升至 34.3%、"
            "Staphylococcus xylosus 升至 9.5%。鱼类发酵后 Psychrobacter 占绝对优势。"
            "腐败菌被抑制、发酵剂接管群落，这一格局在乳、肉、鱼三类中重复出现。")
K.figure(doc, f"{F}/fig4_alpha多样性.png", 14.6)
K.caption(doc, "图 3  各类别的物种水平 alpha 多样性")

K.h2(doc, "真核部分")
K.para(doc, "757 个真核 MAG 分属 95 个 SGB。属水平以 Saccharomyces（192）、Debaryomyces（133）、"
            "Penicillium（83）、Scopulariopsis（40）、Kluyveromyces（34）为主；种水平以 Saccharomyces cerevisiae（190）、"
            "Debaryomyces hansenii（128）、Penicillium roqueforti（37）、Scopulariopsis brevicaulis（36）、"
            "Penicillium camemberti（24）为代表。含酒精发酵饮料中真核占 44.7%，为各类别中最高；"
            "乳制品虽只占 5.4%，但青霉与德巴利酵母直接决定白霉、蓝纹奶酪的成熟与风味。")
K.figure(doc, f"{F}/fig5_真核组成.png", 13.6)
K.caption(doc, "图 4  真核 MAG 的属组成")

# ============================================================ 三
K.h1(doc, "三、益生菌模块", page_break=True)
K.para(doc, "cFMD 里的“益生菌”分三层，最大与最小相差两个量级，混用会得出错误结论。")

t3 = pd.DataFrame([
    ["益生菌制剂样品", "category = probiotics，市售粉剂与胶囊", "14 份样品", "42", "23"],
    ["核心益生菌物种", "种级名单（QPS、ISAPP、国内菌种名单）", "28 个种", "2,884", "30"],
    ["乳酸菌发酵剂类群", "23 个属的归并", "23 个属", "5,273", "192"],
], columns=["层级", "界定", "范围", "MAG", "SGB"])
K.table(doc, t3, widths=[3.4, 6.4, 2.6, 1.8, 1.4], font_size=8.6)
K.caption(doc, "表 5  益生菌相关的三个层级")

K.para(doc, "益生菌制剂与其他食品基质一样经过组装分箱，得到的 MAG 与其他类别同质，可以直接合并分析。"
            "14 份样品产出的 42 个 MAG 平均完整度 76.7%，低于发酵食品整体的 84.3%，HQ 仅 16 个。"
            "原因是配方菌种单一、各菌丰度受配比限制，辅料 DNA 占比高，覆盖度分布不均。下游分析建议只用这 16 个 HQ。")

ps = probmag.groupby("物种").agg(MAG=("MAG_id", "size"),
                                 HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                                 最高完整度=("completeness", "max")).reset_index()
ps["最高完整度"] = ps["最高完整度"].round(1)
ps = ps.sort_values(["MAG", "HQ"], ascending=False)
ps.columns = ["物种", "MAG", "HQ", "最高完整度%"]
K.table(doc, ps, widths=[7.4, 1.6, 1.4, 2.6], font_size=8.4)
K.caption(doc, "表 6  益生菌制剂来源的 MAG（42 个，23 个 SGB）")

core = tab6.groupby("物种").agg(MAG=("MAG_id", "size"), HQ=("质量等级", lambda x: (x == "高质量(HQ)").sum()),
                                SGB=("SGB_id", "nunique"), 主要来源=("发酵类别中文", lambda x: x.value_counts().index[0]))
core = core.sort_values("MAG", ascending=False).head(16).reset_index()
core.columns = ["物种", "MAG", "HQ", "SGB", "主要来源"]
K.table(doc, core, widths=[6.4, 1.7, 1.4, 1.3, 3.2], font_size=8.4)
K.caption(doc, "表 7  发酵食品中数量最多的核心益生菌物种（前 16 位）")

K.figure(doc, f"{F}/fig3_益生菌物种热图.png", 13.6)
K.caption(doc, "图 5  核心益生菌物种在各类别中的 MAG 数量")

K.para(doc, "双歧杆菌需要单独看。全库只有 155 个 MAG、8 个 SGB，且以食品来源的 Bifidobacterium aquikefiri（72）、"
            "B. psychraerophilum（38）、B. mongoliense（17）为主，临床常用的 B. longum（11）、B. animalis（2）很少。"
            "这与双歧杆菌主要栖居肠道、在食品中多为外源添加相符，也意味着用这套资源做双歧杆菌益生性研究样本不足。")
K.para(doc, "结论：益生菌方向的 MAG 是齐的，制剂来源 42 个、核心益生菌物种 2,884 个，两套可以对照使用——"
            "前者是商业化菌株，后者是食品基质中的同种野生型菌株。受限于 14 份制剂样品，前者的统计能力弱，"
            "只能作菌株参考，不足以单独支撑一项工作。")

# ============================================================ 四
K.h1(doc, "四、antiSMASH 产物预测", page_break=True)
K.para(doc, "输入按 SGB 去重，每个 SGB 取完整度最高、污染最低的一株，共 957 个代表株（原核 862、真核 95）。"
            "同一 SGB 内不同 MAG 的簇组成通常只差个别位点，全量跑 10,202 个基因组既耗算力，也会让近重复序列"
            "抬高家族计数。清单见交付文件 09，P1 为益生菌种与食品新种，P2 为其余。")

t4 = pd.DataFrame([
    ["版本", "antiSMASH 8.0.4", "可识别 101 类簇"],
    ["细菌参数", "--genefinding-tool prodigal", "--cb-general --cb-knownclusters --cb-subclusters --asf"],
    ["真菌参数", "--taxon fungi", "--genefinding-tool prodigal-m"],
    ["单株耗时", "3–8 min（16 线程）", "真菌 10–20 min"],
    ["总量估算", "40–80 CPU·h", "20 并发约 3–5 h"],
], columns=["项目", "设置", "说明"])
K.table(doc, t4, widths=[2.8, 5.4, 7.4], font_size=8.4)
K.caption(doc, "表 8  运行配置")

K.para(doc, "乳酸菌类群的簇类型高度集中，基本只有细菌素与羊毛硫肽两类，单株 2–7 个；芽孢杆菌与假单胞菌的"
            "簇型最丰富，NRPS、PKS、萜类、铁载体都有，单株 7–14 个。按属的经验区间估算，原核部分预期 1,185–3,695 个 BGC，"
            "真核部分 315–872 个，后者主要来自青霉属。")

sel = ["Lactococcus lactis", "Lactiplantibacillus plantarum", "Lacticaseibacillus paracasei", "Leuconostoc",
       "Pediococcus", "Latilactobacillus sakei", "Streptococcus thermophilus", "Bifidobacterium",
       "Bacillus subtilis", "Staphylococcus", "Brevibacterium", "Pseudomonas", "Penicillium roqueforti",
       "Saccharomyces"]
b = bgc[bgc["分类单元"].isin(sel)][["分类单元", "antiSMASH可识别区域类型", "代表性已知产物", "对发酵过程的作用"]].copy()
b.columns = ["类群", "可识别簇类型", "代表产物", "在发酵中的作用"]
K.table(doc, b, widths=[3.4, 3.6, 4.4, 4.2], font_size=7.4, header_size=7.8)
K.caption(doc, "表 9  主要类群的簇类型与已知产物")

K.h2(doc, "与发酵和益生菌的挂钩点")
K.para(doc, "菌群控制。乳球菌的 nisin、植物乳植杆菌的 plantaricin、片球菌的 pediocin、清酒乳杆菌的 sakacin "
            "都属于细菌素，作用靶点是细胞膜或细胞壁前体，对李斯特菌、芽孢杆菌有效。这与上文肉制品中物种的升降一致："
            "Latilactobacillus sakei 升至 34.3% 的同时，Brochothrix thermosphacta 由 3.17% 降到 0.49%。若在对应 MAG 中找到完整操纵子，"
            "基因、表达与群落结果就能串成一条链。")
K.para(doc, "风味与质构。短杆菌的类胡萝卜素簇对应奶酪表面的橙红色，醋酸菌与木葡糖酸醋杆菌的纤维素簇对应红茶菌膜，"
            "明串珠菌的葡聚糖蔗糖酶簇对应黏度。这类产物在 antiSMASH 中部分以 PKS 或萜类出现，要配合 CAZyme 注释一起看。")
K.para(doc, "安全风险。Penicillium roqueforti 的 roquefortine C 与 PR-toxin 簇、Aspergillus 的霉毒素簇、"
            "Staphylococcus 的毒力相关簇，都是发酵食品风险评估的直接靶点。本资源的青霉有 83 个 MAG、8 个 SGB，"
            "覆盖蓝纹与白霉奶酪的主成熟菌，具备做簇层面筛查的条件。")
K.para(doc, "益生菌方向相对间接。可做的是三件事：统计细菌素簇在益生菌株中的分布作为拮抗能力指标；"
            "用双歧杆菌的羊毛硫肽簇做菌株分型；把制剂来源的 42 个 MAG 与食品中同种菌株比簇组成，"
            "看商业菌株长期传代后是否丢了某些簇。")

K.para(doc, "判读要注意四点。完整度 50%–70% 的基因组常缺调控区或模块，会低估簇数，HQ 与 MQ 要分开统计。"
            "contig 断裂会把一个簇报成两个部分簇，需按位置合并。相似度低于 30% 的簇可信度有限，要与已知簇做系统发育比对。"
            "细菌素，尤其是 RiPP-like 类，假阳性偏高，建议用 BAGEL4 交叉验证。")

# ============================================================ 五
K.h1(doc, "五、下一步可做的分析", page_break=True)
t5 = pd.DataFrame([
    ["A", "类别指示物种（LEfSe / indicspecies）", "现有总表", "各类别的诊断分类单元，可用于溯源与真伪鉴别"],
    ["A", "跨类别共现网络（SparCC）", "现有总表", "乳酸菌—醋酸菌—酵母的稳定模块"],
    ["A", "国家、类别、工艺的方差分解（PERMANOVA）", "现有总表", "地域风味的微生物学对应"],
    ["A", "食物 SGB 与人体肠道对接", "总表 + cMD", "各类别 SGB 在肠道的检出率"],
    ["A", "菌株水平追踪（StrainPhlAn）", "总表 + 原始数据", "食物到肠道的传播证据"],
    ["B", "BGC 家族聚类（BiG-SLiCE）", "MAG 序列", "食品特有簇与类别富集"],
    ["B", "细菌素专项（BAGEL4 / RiPPer）", "MAG 序列", "候选成熟肽与预期抑菌谱"],
    ["B", "CAZyme 谱（dbCAN3）", "MAG 序列", "底物利用与终产物差异"],
    ["B", "益生性状基因筛查", "MAG 序列", "耐酸、耐胆盐、黏附基因分布"],
    ["B", "耐药基因与可移动元件", "MAG 序列", "食品安全监管关注点"],
    ["B", "噬菌体与 CRISPR", "MAG 序列", "发酵剂的噬菌体防御能力"],
    ["B", "同 SGB 的食品—人体泛基因组", "MAG 序列", "食品特异辅助基因，区分过路菌与定植菌"],
    ["B", "新种描述（ANI + GTDB-Tk）", "MAG 序列", "290 个食品新种中完整度 ≥90% 的部分"],
    ["C", "功能通路重建（HUMAnN3 / gapseq）", "原始 reads", "补 MAG 方法对低丰度成员的遗漏"],
    ["C", "宏转录组与 BGC 表达", "配套 RNA-seq", "解决 antiSMASH 只能看“有没有”的问题"],
], columns=["优先级", "分析项", "数据", "产出"])
K.table(doc, t5, widths=[1.3, 6.0, 3.4, 5.1], font_size=7.8)
K.caption(doc, "表 10  可继续开展的分析")

K.para(doc, "建议先做 A 组前两项加 B 组前两项，四件事串起来能支撑一篇完整的论文：从类别标志物种出发，"
            "落到 BGC 家族与细菌素候选，再用益生性状基因收尾。C 组依赖额外数据，适合放到下一阶段。")

# ============================================================ 六
K.h1(doc, "六、需要注意的问题")
K.numbered(doc, [
    "类别严重不平衡。乳制品占 67.4%，发酵鱼只有 32 个 MAG，发酵豆类与发酵种子不足 100 个。"
    "跨类别结论都受这条限制。",
    "批次效应无法完全消除。59 个数据集的提取方法、平台、读长各不相同，元数据虽有记录，校正有限。",
    "MAG 方法本身有偏。高丰度、低复杂度群落（接种发酵）更容易得到高质量基因组，"
    "低丰度成员与传统自然发酵被系统性低估。",
    "SGB 判定依赖参考库。参考库厚的类群（乳球菌、乳杆菌）多判为已知种，参考库薄的类群（发酵鱼、发酵豆类）"
    "集中落在未知种，类别间的新颖性差异有一部分是数据库偏倚。",
    "益生菌名单是种级的。同种不同菌株的益生功能差异很大，基因组层面的“益生菌物种”不等于“益生菌菌株”。",
    "antiSMASH 部分尚未实测。产物对应关系来自已知报道，BGC 数量为区间估算，拿到序列后需以实测替换。",
])

K.h1(doc, "附：交付文件")
files = pd.DataFrame([
    ["00", "MAG主表_全部.csv", "10,899 个 MAG 的注释与元数据合并表"],
    ["01", "发酵MAG总表.csv", "10,202 个发酵 MAG，含类别、质量、益生菌归属"],
    ["02–04", "类别汇总、属矩阵、SGB 汇总", "1,144 个 SGB 的分类与来源"],
    ["05–07", "益生菌系列", "制剂 42 个、核心种 2,884 个、物种×类别矩阵"],
    ["08", "发酵食品真核MAG表.csv", "757 个真核 MAG"],
    ["09", "antiSMASH输入MAG清单.csv", "957 个代表株，含 P1/P2 优先级"],
    ["10–16", "物种谱系列", "发酵与非发酵差异、类别丰度、alpha 多样性"],
    ["17–19", "antiSMASH 知识表与工作量表", "50 个类群的产物对应，按属的 BGC 估算"],
    ["—", "figures/", "图 1–5 的 PNG（300 dpi）"],
    ["—", "scripts/", "整理、统计、绘图与 antiSMASH 流程脚本"],
], columns=["编号", "文件", "内容"])
K.table(doc, files, widths=[1.4, 6.2, 8.2], font_size=8.0)
K.caption(doc, "附表  随报告交付的数据文件")

doc.save(OUT)
print("saved", OUT, round(os.path.getsize(OUT) / 1024), "KB")
