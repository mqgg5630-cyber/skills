# -*- coding: utf-8 -*-
"""构建 antiSMASH 产物知识表（文献/数据库依据）并输出"""
import pandas as pd, numpy as np

OUT = "/home/user/skills/cfmd_deliverables/tables"
ferm = pd.read_pickle("/tmp/ferm.pkl")
prok = ferm[ferm["superkingdom"] != "Eukaryota"]
genus_cnt = ferm["属"].value_counts()
species_cnt = ferm["物种"].value_counts()

# 每个属的主要发酵类别
cat_by_genus = (prok.groupby("属")["发酵类别中文"]
                .apply(lambda s: " / ".join(s.value_counts().head(2).index)))

R = []


def add(taxon, level, regions, products, class_, ferm_func, prob_func, ref, nmag=None, order="中"):
    R.append({
        "分类单元": taxon, "层级": level,
        "发酵食品MAG数": int(genus_cnt.get(taxon, 0)) if level == "属" else int(species_cnt.get(taxon, 0)),
        "主要来源发酵类别": cat_by_genus.get(taxon, ""),
        "antiSMASH可识别区域类型": regions,
        "代表性已知产物": products,
        "产物化学类别": class_,
        "文献报道BGC数量级": order,
        "对发酵过程的作用": ferm_func,
        "对益生菌功能的关联": prob_func,
        "依据文献": ref,
    })


# ---- 乳酸菌类群
add("Lactococcus", "属", "lanthipeptide(class I); bacteriocin; RiPP-like",
    "nisin A/Z; lacticin 3147; lactococcin A/B/M/G/Q; lactococcin 972",
    "羊毛硫肽 / II类细菌素", "抑菌、发酵剂竞争、发酵进程控制", "nisin 抑制食源性致病菌, 菌群竞争屏障", "Alvarez-Sieiro2016; Cotter2013; McAuliffe2001", None, "高")
add("Lactococcus lactis", "种", "lanthipeptide; bacteriocin; RiPP-like",
    "nisin; lactococcin A/B/M; lacticin 481/3147",
    "羊毛硫肽 / II类细菌素", "乳品发酵剂核心菌, 产酸与风味", "产 nisin 菌株用于食品保鲜与抑菌", "McAuliffe2001; Alvarez-Sieiro2016", None, "高")
add("Lactococcus cremoris", "种", "bacteriocin; RiPP-like", "lactococcin 972; cremocin",
    "II类细菌素", "乳品发酵剂, 低温发酵", "抑菌、抑制腐败菌", "Alvarez-Sieiro2016", None, "中高")
add("Lactobacillus", "属", "bacteriocin; RiPP-like; head_to_tail",
    "lactacin B/F; acidocin A/B; gassericin A(环肽); helveticin J",
    "II/III类细菌素", "酸奶、开菲尔、发酵谷物主体", "肠道定植与抑菌", "Zacharof2012; Alvarez-Sieiro2016", None, "中")
add("Lactobacillus helveticus", "种", "bacteriocin", "helveticin J; helveticin M; lactocin 150",
    "III类细菌素(大分子)", "瑞士型奶酪发酵剂, 肽酶促 ACE 抑制肽生成", "产活性肽, 可能降血压", "Zacharof2012", None, "中")
add("Lactobacillus delbrueckii", "种", "bacteriocin; RiPP-like", "bulgaricin; lactocin 51",
    "II类细菌素", "酸奶/奶酪发酵剂(bulgaricus)", "抑菌、乳糖利用", "Alvarez-Sieiro2016", None, "中")
add("Lacticaseibacillus", "属", "bacteriocin; RiPP-like; lanthipeptide(少数)",
    "caseicin A/B; lactocin 160; paracasin",
    "II类细菌素", "发酵乳、发酵谷物", "肠道存活、抑菌", "Alvarez-Sieiro2016", None, "中")
add("Lacticaseibacillus paracasei", "种", "bacteriocin; RiPP-like", "caseicin A/B; lactocin 160",
    "II类细菌素", "奶酪/发酵乳非起始发酵剂(NSLAB)", "临床证据较多的益生菌种", "Alvarez-Sieiro2016", None, "中高")
add("Lacticaseibacillus rhamnosus", "种", "bacteriocin; RiPP-like; exopolysaccharide",
    "rhamnosin; lactocin; 胞外多糖簇", "II类细菌素 / EPS", "发酵乳", "GG 菌株为研究最充分的益生菌之一", "Alvarez-Sieiro2016", None, "中")
add("Lactiplantibacillus plantarum", "种", "bacteriocin; lanthipeptide(plantaricin W); RiPP-like",
    "plantaricin EF/JK/NC8/W; plantaricicin A(信息素)",
    "IIb 双肽细菌素 / 羊毛硫肽", "植物发酵、酸面团、泡菜", "抑菌谱广, 肠道黏附", "Alvarez-Sieiro2016; Diep2007", None, "高")
add("Limosilactobacillus", "属", "bacteriocin; head_to_tail", "reutericin 6; gassericin A/K",
    "环状细菌素", "发酵谷物、发酵肉", "reuteri 为经典益生菌, 产 reuterin 抑菌", "Alvarez-Sieiro2016", None, "中")
add("Limosilactobacillus reuteri", "种", "bacteriocin; head_to_tail", "reutericin 6; gassericin A",
    "环状细菌素", "猪/禽/人源, 发酵食品中检出", "reuterin(3-HPA)抑制病原; 非BGC途径", "Alvarez-Sieiro2016; Talarico1988", None, "中高")
add("Ligilactobacillus salivarius", "种", "lanthipeptide(class I); bacteriocin",
    "salivaricin A/B/ABP-118; salivaricin P", "羊毛硫肽 / IIb 双肽", "青贮与发酵饲料", "口腔/肠道益生, 抑菌", "Ross2001; Alvarez-Sieiro2016", None, "中高")
add("Levilactobacillus", "属", "bacteriocin; RiPP-like", "brevicin 174A/286; curvaticin",
    "II类细菌素", "酸面团、发酵果蔬", "抑菌", "Alvarez-Sieiro2016", None, "中")
add("Latilactobacillus sakei", "种", "bacteriocin", "sakacin A/P/G; lactocin S",
    "II类细菌素", "发酵肉制品主导菌, 抑制李斯特菌", "抑菌", "Alvarez-Sieiro2016; Hugas1998", None, "中高")
add("Latilactobacillus curvatus", "种", "bacteriocin", "curvacin A; sakacin P",
    "II类细菌素", "发酵香肠", "抑菌", "Alvarez-Sieiro2016", None, "中")
add("Leuconostoc", "属", "bacteriocin; dextran/EPS 簇", "leucocin A/C; mesentericin Y105; 葡聚糖",
    "IIa 细菌素 / EPS", "泡菜、酸菜、开菲尔、奶酪", "抑菌与质构", "Alvarez-Sieiro2016", None, "中")
add("Pediococcus", "属", "bacteriocin", "pediocin PA-1/AcH; penocin A; pediocin PD-1",
    "IIa 细菌素(抗李斯特菌)", "发酵肉、青贮、发酵果蔬", "强抗李斯特菌活性", "Rodriguez1997; Alvarez-Sieiro2016", None, "中")
add("Weissella", "属", "bacteriocin", "weissellicin 110/Y/M; weissellicin D",
    "II类细菌素", "泡菜、发酵豆类", "抑菌; 部分菌株为条件致病", "Alvarez-Sieiro2016", None, "中")
add("Enterococcus", "属", "lanthipeptide(cytolysin); bacteriocin",
    "enterocin A/B/P/P1; cytolysin; enterolysin A",
    "羊毛硫肽 + II类细菌素", "发酵肉、奶酪、发酵豆类", "抑菌强, 但需评估毒力/耐药", "Alvarez-Sieiro2016; Franz2007", None, "中高")
add("Streptococcus thermophilus", "种", "bacteriocin; RiPP-like", "thermophilin A/B/13; streptococcin; blp 簇",
    "II类细菌素", "酸奶/奶酪必需发酵剂", "QPS 安全菌, 产 β-半乳糖苷酶", "Alvarez-Sieiro2016", None, "中")
add("Tetragenococcus", "属", "bacteriocin", "tetragenocin; halocin 类",
    "II类细菌素", "酱油、鱼露高盐发酵", "耐盐发酵剂", "Alvarez-Sieiro2016", None, "低")
add("Oenococcus", "属", "bacteriocin(少见)", "oenococcin B/84/β",
    "II类细菌素", "苹果酸-乳酸发酵", "葡萄酒降酸", "Alvarez-Sieiro2016", None, "低")
add("Carnobacterium", "属", "bacteriocin", "carnobacteriocin B2/BM1; piscicolin 126",
    "IIa 细菌素", "真空包装肉、鱼类", "抗李斯特菌", "Alvarez-Sieiro2016", None, "中")
add("Bifidobacterium", "属", "lanthipeptide; bacteriocin; RiPP-like; arylpolyene(少数)",
    "bifidocin B; bifidocin A; lantibiotic 簇(B. longum)",
    "羊毛硫肽 / II类细菌素", "发酵乳、开菲尔", "婴幼儿肠道核心菌, 免疫调节", "Martinez2013; Westermann2017", None, "中低")
add("Propionibacterium freudenreichii", "种", "bacteriocin; RiPP-like",
    "propionicin SM1/SM2/T1; jenseniin G", "II类细菌素",
    "瑞士型奶酪丙酸发酵, 眼孔与风味", "产 B12/丙酸, 免疫调节", "Gwenzietal2010; Alvarez-Sieiro2016", None, "中低")

# ---- 芽孢杆菌 / 放线菌 / 其他
add("Bacillus", "属", "NRPS; transAT-PKS; T3PKS; sactipeptide; lanthipeptide; siderophore; terpene",
    "surfactin; fengycin/plipastatin; iturin; bacillaene; difficidin; bacillibactin; subtilosin A; subtilin",
    "脂肽 / 聚酮 / 核糖体肽", "发酵种子与谷物(纳豆、豆豉), 产蛋白酶与风味", "spore-based 益生菌, 抑菌与耐胃酸",
    "Harwood2018; Kaspar2019; Caulier2019", None, "高")
add("Bacillus subtilis", "种", "NRPS; transAT-PKS; siderophore; sactipeptide; lanthipeptide",
    "surfactin; plipastatin; bacillaene; bacillibactin; subtilosin A",
    "脂肽 / 聚酮 / 铁载体", "发酵豆制品主导菌, 产纳豆激酶", "QPS 认定, 抑菌与免疫刺激",
    "Harwood2018; Kaspar2019", None, "高")
add("Bacillus velezensis", "种", "NRPS; transAT-PKS; T3PKS; terpene",
    "surfactin; fengycin; bacillomycin; macrolactin; difficidin",
    "脂肽 / 聚酮", "发酵种子表面菌", "生防与抑菌", "Rabbee2019", None, "高")
add("Weizmannia coagulans", "种", "bacteriocin; NRPS(少见)", "coagulin",
    "II类细菌素", "发酵谷物", "耐热芽孢益生菌, 调节肠道", "Honda2018; Hyronimus1998", None, "低")
add("Staphylococcus", "属", "siderophore; NRPS; betalactone(少数)",
    "staphyloferrin A/B; 金黄色葡萄球菌 aureusimine",
    "铁载体 / NRPS", "奶酪表面与发酵香肠成熟菌群", "非益生; 需监测肠毒素与耐药",
    "Schoenfelder2019; Wilson2019", None, "中")
add("Pseudomonas", "属", "NRPS; T1PKS; phenazine; siderophore; HSAF 类",
    "pyoverdine; phenazine-1-carboxylic acid; 2,4-DAPG; pyoluteorin",
    "铁载体 / 吩嗪 / 聚酮", "奶酪表面、鱼类腐败菌群", "非益生, 与腐败和冷适应相关",
    "Gross2007; Weller2007", None, "高")
add("Serratia", "属", "NRPS-PKS 杂合; NRPS", "prodigiosin; serratamolide; althiomycin",
    "灵菌红素 / 脂肽", "奶酪表面色素污染", "非益生, 条件致病", "Williamson2006", None, "中")
add("Halomonas", "属", "ectoine; siderophore", "ectoine; 铁载体",
    "相容性溶质", "高盐发酵(鱼露、酱)", "耐盐, 工业底盘", "Schwibbert2011", None, "低")
add("Brevibacterium", "属", "NRPS; terpene(carotenoid); siderophore",
    "brevibactin; 类胡萝卜素(橙色素)", "铁载体 / 萜类", "奶酪表面涂抹成熟, 产橙色与硫化物风味",
    "非益生, 风味贡献", "Leclercq2014; Irlinger2015", None, "中")
add("Corynebacterium", "属", "NRPS; terpene", "corynebactin 类铁载体; 类胡萝卜素",
    "铁载体 / 萜类", "奶酪表面成熟菌群", "非益生", "Irlinger2015", None, "中")
add("Acetobacter", "属", "T3PKS(少数); 纤维素簇", "细菌纤维素; 少数聚酮",
    "聚酮 / EPS", "开菲尔、果醋、可可发酵", "氧化乙醇产酸", "Gullo2013", None, "低")
add("Komagataeibacter", "属", "纤维素合成簇; T3PKS(少数)", "细菌纤维素",
    "EPS", "红茶菌(Kombucha)、果醋", "膜形成, 质构", "Gullo2013", None, "低")
add("Zymomonas", "属", "少见", "无代表性次级代谢产物", "-", "棕榈酒、龙舌兰酒",
    "乙醇发酵", "无", "He2014")
add("Psychrobacter", "属", "少见", "无代表性次级代谢产物", "-", "发酵鱼(洪鱼)", "低温适应", "无", "Bakermans2012")

# ---- 真核（真菌）
add("Penicillium roqueforti", "种", "NRPS; T1PKS; terpene; NRPS-like",
    "roquefortine C; PR-toxin; andrastin A; mycophenolic acid; isofumigaclavine",
    "生物碱 / 聚酮 / 萜类", "蓝纹奶酪成熟菌, 脂肪分解与风味", "非益生; 产霉毒素需评估",
    "Coton2021; O'Brien2006; Nielsen2005", None, "高")
add("Penicillium camemberti", "种", "NRPS; T1PKS; terpene",
    "cyclopiazonic acid; asperphenamate; 类胡萝卜素",
    "生物碱 / 聚酮", "白霉奶酪表面菌", "非益生", "Coton2021; Frisvad2015", None, "高")
add("Penicillium nalgiovense", "种", "NRPS; T1PKS", "cyclopiazonic acid; 青霉素类(少见)",
    "生物碱", "发酵香肠表面菌", "非益生", "Coton2021", None, "中")
add("Aspergillus", "属", "NRPS; T1PKS; terpene; PKS-like",
    "kojic acid; 曲酸; 黄曲霉毒素(部分种); ochratoxin",
    "聚酮 / 生物碱", "酱油、味噌、清酒制曲", "非益生; 产毒种需筛查",
    "Frisvad2015; Rank2011", None, "高")
add("Saccharomyces", "属", "NRPS(稀少); terpene", "无代表性次级代谢产物",
    "-", "酒类、面包、开菲尔", "发酵产乙醇与风味; boulardii 为益生菌酵母",
    "无", None)
add("Debaryomyces hansenii", "种", "NRPS(稀少)", "无代表性次级代谢产物", "-",
    "奶酪、发酵肉表面", "耐盐, 风味与抑菌", "无", "Irlinger2015", None)
add("Kluyveromyces", "属", "NRPS(稀少); terpene", "无代表性次级代谢产物", "-",
    "开菲尔、乳制品", "乳糖利用, 风味", "无", "无", None)
add("Mucor", "属", "NRPS; terpene", "rhizonin 类(部分种); β-胡萝卜素",
    "生物碱 / 萜类", "豆豉、腐乳、发酵豆制品", "非益生", "Jennessen2005", None, "中")
add("Fusarium", "属", "NRPS; T1PKS; terpene",
    "fumonisin; zearalenone; deoxynivalenol; enniatin",
    "聚酮 / 生物碱", "污染发酵谷物", "产霉毒素风险", "Desjardins2006", None, "高")
add("Scopulariopsis", "属", "NRPS; T1PKS", "roquefortine 类; 部分霉毒素",
    "生物碱", "奶酪表面腐败菌", "非益生", "Coton2021", None, "中")

df = pd.DataFrame(R)

import re as _re
def _cjk_fix(t):
    if not isinstance(t, str):
        return t
    t = _re.sub(r"(?<=[\u4e00-\u9fa5]);\s*(?=[\u4e00-\u9fa5])", "；", t)
    t = _re.sub(r"(?<=[\u4e00-\u9fa5]),\s*(?=[\u4e00-\u9fa5])", "，", t)
    t = _re.sub(r"(?<=[\u4e00-\u9fa5]),\s*(?=[A-Za-z])", "，", t)
    return t

for _c in ["主要来源发酵类别", "antiSMASH可识别区域类型", "代表性已知产物", "产物化学类别",
           "对发酵过程的作用", "对益生菌功能的关联"]:
    df[_c] = df[_c].map(_cjk_fix)
df = df.sort_values(["层级", "发酵食品MAG数"], ascending=[False, False])
df.to_csv(f"{OUT}/17_antiSMASH产物知识表_文献依据.csv", index=False, encoding="utf-8-sig")
print(len(df), "rows")
print(df[["分类单元", "层级", "发酵食品MAG数", "antiSMASH可识别区域类型"]].head(50).to_string(index=False))
