# -*- coding: utf-8 -*-
"""
cFMD (curatedFoodMetagenomicData, Carlino et al., Cell 2024) 数据整理脚本
输入: cFMD v1.1.0 公开总表 (GitHub SegataLab/cFMD tag v1.1.0 / Zenodo 记录快照)
输出: MAG 主表、按发酵类别汇总、SGB 汇总、益生菌 MAG 表等
"""
import os, re
import numpy as np
import pandas as pd

SRC = "/tmp/cfmd"
OUT = "/home/user/skills/cfmd_deliverables/tables"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- 中文映射
CAT_CN = {
    "dairy": "乳制品",
    "fermented_beverages": "发酵饮料",
    "fermented_meat": "发酵肉制品",
    "fermented_grains": "发酵谷物制品",
    "alcohol": "含酒精发酵饮料",
    "fermented_fruits_and_vegetables": "发酵果蔬",
    "fermented_tubers_and_roots": "发酵薯类与根茎",
    "fermented_legumes": "发酵豆类",
    "fermented_seeds": "发酵种子/油料",
    "fermented_fish": "发酵鱼制品",
    "probiotics": "益生菌制剂",
    "meat": "肉制品(非发酵)",
    "fruits_and_vegetables": "果蔬(非发酵)",
    "fish": "鱼(非发酵)",
    "other": "其他",
}
TYPE_CN = {
    "cheese": "奶酪", "water_kefir": "水开菲尔", "kefir": "奶开菲尔", "milk": "乳",
    "whey": "乳清", "salami": "萨拉米", "meat": "肉", "cheese_brine": "奶酪盐水",
    "sourdough": "酸面团", "koumiss": "马奶酒", "tea": "茶(康普茶)", "wine": "葡萄酒",
    "yogurt": "酸奶", "cured_meat_before_ripening": "成熟前腌肉",
    "soybean": "大豆制品", "probiotics": "益生菌制剂", "meat_batter": "肉糜",
    "sausage_before_ripening": "成熟前香肠", "ogi": "Ogi(发酵玉米粥)",
    "spinach": "菠菜", "nunu": "Nunu(发酵乳)", "sauerkraut": "酸菜",
    "cattle_pig_chicken_and_turkey_sausage": "混合肉香肠", "red_pepper_sauce": "红椒酱",
    "beer": "啤酒", "kunu": "Kunu(发酵小米饮料)", "iru": "Iru(发酵角豆)",
    "palm_wine": "棕榈酒", "pre_processed_vegetables": "预处理蔬菜",
    "post_processed_vegetables": "后处理蔬菜", "coffee": "咖啡", "pulque": "Pulque",
    "honey": "蜂蜜", "kimchi": "泡菜", "gari": "Gari(发酵木薯)",
    "cattle_pig_sheep_and_horse_sausage": "混合肉香肠", "fufu": "Fufu(发酵木薯)",
    "ogiri": "Ogiri(发酵瓜籽)", "ugi": "Ugi(发酵谷物)", "skate_fish": "鳐鱼",
    "cod": "鳕鱼", "salmon": "三文鱼", "grain": "谷物", "kvass": "格瓦斯",
    "ugba": "Ugba(发酵非洲油豆)", "wara": "Wara(发酵豆制品)",
    "lafun": "Lafun(发酵木薯)", "pito": "Pito(发酵高粱酒)",
    "nono": "Nono(发酵乳)", "burukutu": "Burukutu(发酵高粱啤酒)",
    "injera": "英吉拉(发酵苔麸饼)", "daikon": "白萝卜", "otika": "Otika(发酵高粱)",
    "zonkom": "Zonkom(发酵小米)", "agadagidi": "Agadagidi(发酵车前草)",
    "okpehe": "Okpehe(发酵槐豆)", "haddock": "黑线鳕", "arctic_char": "北极红点鲑",
    "grape": "葡萄", "laban": "Laban(发酵乳)", "cabbage": "卷心菜",
    "boza": "Boza(发酵谷物饮料)", "turnip": "芜菁", "orange": "橙",
    "tepache": "Tepache(发酵菠萝)", "ginger_beer": "姜汁啤酒", "cucumber": "黄瓜",
    "tofu_chili": "辣味豆腐", "pickled_vegetables": "腌蔬菜",
    "raw_sauerkraut_and_juniper_berries": "生酸菜+杜松子",
    "brown_rice_amazake": "糙米甘酒", "mead": "蜂蜜酒",
    "apple_cider_vinegar": "苹果醋", "dilly_carrots": "莳萝胡萝卜",
    "garlic": "大蒜", "dukkah": "Dukkah(混合香料)", "ginger": "姜",
    "okra": "秋葵", "tomato_and_mustards": "番茄+芥菜籽",
    "carrot_sticks": "胡萝卜条", "chocolate_coating": "巧克力涂层",
    "soy_powder": "大豆粉", "whey_protein": "乳清蛋白",
    "cheese_starter": "奶酪发酵剂", "emu": "鸸鹋", "massa": "Massa(发酵谷物)",
    "foura": "Foura(发酵小米)", "soumbala": "Soumbala(发酵角豆)",
    "mou": "Mou(发酵乳)", "attieke": "Attieke(发酵木薯)", "dolo": "Dolo(发酵高粱啤酒)",
    "koko": "Koko(发酵小米)", "fura": "Fura(发酵小米)", "maasa": "Maasa(发酵小米)",
    "brukina": "Brukina(发酵乳+小米)", "wagashi": "Wagashi(发酵乳)",
    "kantong": "Kantong(发酵木薯叶)", "dawa_dawa": "Dawa-dawa(发酵角豆)",
    "lafun_2": "Lafun", "iru_2": "Iru", "palm_wine_2": "棕榈酒",
    "paralichthys_olivaceus": "牙鲆", "emu_2": "鸸鹋",
}

# ---------------------------------------------------------------- 读表
meta = pd.read_csv(f"{SRC}/cFMD_metadata.tsv", sep="\t", low_memory=False, encoding="latin-1")
meta = meta.rename(columns={"fermented/non-fermented": "fermented"})
meta["发酵类别中文"] = meta["category"].map(CAT_CN).fillna(meta["category"])
meta["食品类型中文"] = meta["type"].map(TYPE_CN).fillna(meta["type"])

mags = pd.read_csv(f"{SRC}/cFMD_mags_list.tsv", sep="\t", low_memory=False, encoding="latin-1")
sgbs_p = pd.read_csv(f"{SRC}/cFMD_sgbs_prokaryotic.tsv", sep="\t", encoding="latin-1", low_memory=False)
sgbs_e = pd.read_csv(f"{SRC}/cFMD_sgbs_eukaryotic.tsv", sep="\t", encoding="latin-1", low_memory=False)
ds = pd.read_csv(f"{SRC}/cFMD_datasets.tsv", sep="\t", encoding="latin-1", low_memory=False)

# 数据集 → 文献
ds.columns = [c.strip() for c in ds.columns]
ds["Reference"] = ds["Reference"].astype(str).str.replace("�", "'", regex=False)

# ---------------------------------------------------------------- MAG 主表
m = mags.merge(
    meta[["dataset_name", "sample_id", "macrocategory", "category", "type", "subtype",
          "commercial_name", "fermented", "country"]],
    left_on=["dataset_id", "sample_id"], right_on=["dataset_name", "sample_id"], how="left"
)
m["发酵类别中文"] = m["category"].map(CAT_CN).fillna(m["category"])
m["食品类型中文"] = m["type"].map(TYPE_CN).fillna(m["type"])
m["界"] = m["superkingdom"].map({"Bacteria": "细菌", "Eukaryota": "真核生物",
                                 "Archaea": "古菌"}).fillna(m["superkingdom"])
m["是否发酵"] = m["fermented"].map({"F": "发酵", "NF": "非发酵"})
m["SGB类型"] = m["unknown"].map({"kSGB": "已知种(kSGB)", "uSGB": "未知种(uSGB)",
                                 "ufSGB": "食品中新种(ufSGB)"})
m["完整度"] = m["completeness"].round(2)
m["污染度"] = m["contamination"].round(2)
m["基因组大小Mb"] = (m["genome_size"] / 1e6).round(3)
m["GC%"] = (m["GC_content"] * 100).round(2)


def qual(r):
    if r["completeness"] >= 90 and r["contamination"] < 5:
        return "高质量(HQ)"
    if r["completeness"] >= 50 and r["contamination"] < 5:
        return "中等质量(MQ)"
    return "低质量(LQ)"


m["质量等级"] = m.apply(qual, axis=1)
def fmt_sp(x):
    x = str(x)
    if "_SGB" in x:
        g, sg = x.split("_SGB")
        return f"{g} sp. SGB{sg}"
    return x.replace("_", " ")


m["物种"] = m["species"].apply(fmt_sp)
m["属"] = m["genus"].astype(str)

# ---------------------------------------------------------------- 益生菌清单
# 依据: EFSA QPS 名单 / ISAPP 核心益生菌共识 / 中国《可用于保健食品的益生菌菌种名单》
PROB_GENUS = {
    "Lactobacillus", "Lacticaseibacillus", "Lactiplantibacillus", "Limosilactobacillus",
    "Ligilactobacillus", "Levilactobacillus", "Latilactobacillus", "Loigolactobacillus",
    "Fructilactobacillus", "Furfurilactobacillus", "Companilactobacillus",
    "Schleiferilactobacillus", "Secundilactobacillus", "Paucilactobacillus",
    "Apilactobacillus", "Bombilactobacillus", "Lentilactobacillus", "Amylolactobacillus",
    "Holzapfelia", "Agrilactobacillus", "Dellaglioa", "Liquorilactobacillus",
    "Bifidobacterium", "Lactococcus", "Leuconostoc", "Pediococcus", "Tetragenococcus",
    "Enterococcus", "Streptococcus", "Weissella", "Oenococcus", "Carnobacterium",
    "Propionibacterium", "Acidipropionibacterium", "Bacillus", "Weizmannia",
    "Saccharomyces", "Kluyveromyces", "Debaryomyces", "Yarrowia", "Akkermansia",
    "Faecalibacterium", "Bacteroides", "Roseburia", "Anaerobutyricum", "Escherichia",
}
# 严格“益生菌功能菌种”名单（种级）
PROB_SPECIES_CORE = {
    "Lactobacillus acidophilus", "Lactobacillus gasseri", "Lactobacillus johnsonii",
    "Lactobacillus crispatus", "Lactobacillus delbrueckii", "Lactobacillus helveticus",
    "Lactobacillus amylovorus", "Lactobacillus gallinarum",
    "Lacticaseibacillus rhamnosus", "Lacticaseibacillus paracasei", "Lacticaseibacillus casei",
    "Lactiplantibacillus plantarum", "Lactiplantibacillus paraplantarum",
    "Limosilactobacillus reuteri", "Limosilactobacillus fermentum", "Limosilactobacillus mucosae",
    "Ligilactobacillus salivarius", "Ligilactobacillus ruminis", "Ligilactobacillus agilis",
    "Levilactobacillus brevis", "Latilactobacillus sakei", "Latilactobacillus curvatus",
    "Fructilactobacillus sanfranciscensis", "Furfurilactobacillus rossiae",
    "Lentilactobacillus kefiri", "Lentilactobacillus buchneri",
    "Companilactobacillus alimentarius", "Companilactobacillus farciminis",
    "Bifidobacterium animalis", "Bifidobacterium longum", "Bifidobacterium breve",
    "Bifidobacterium bifidum", "Bifidobacterium adolescentis", "Bifidobacterium catenulatum",
    "Bifidobacterium lactis", "Bifidobacterium infantis",
    "Streptococcus thermophilus", "Streptococcus salivarius",
    "Lactococcus lactis", "Lactococcus cremoris",
    "Enterococcus faecium", "Enterococcus faecalis", "Enterococcus durans",
    "Pediococcus acidilactici", "Pediococcus pentosaceus", "Pediococcus parvulus",
    "Leuconostoc mesenteroides", "Leuconostoc citreum", "Leuconostoc lactis",
    "Weissella cibaria", "Weissella confusa",
    "Propionibacterium freudenreichii", "Acidipropionibacterium acidipropionici",
    "Bacillus subtilis", "Bacillus licheniformis", "Bacillus clausii",
    "Bacillus pumilus", "Weizmannia coagulans", "Bacillus amyloliquefaciens",
    "Saccharomyces cerevisiae", "Saccharomyces boulardii", "Kluyveromyces marxianus",
    "Debaryomyces hansenii", "Yarrowia lipolytica",
    "Akkermansia muciniphila", "Faecalibacterium prausnitzii",
    "Bacteroides xylanisolvens", "Roseburia intestinalis",
    "Anaerobutyricum hallii",
}


TIER_A = {
    "Lactobacillus acidophilus","Lactobacillus gasseri","Lactobacillus johnsonii","Lactobacillus crispatus",
    "Lactobacillus delbrueckii","Lactobacillus helveticus","Lactobacillus amylovorus","Lactobacillus gallinarum",
    "Lacticaseibacillus rhamnosus","Lacticaseibacillus paracasei","Lacticaseibacillus casei",
    "Lactiplantibacillus plantarum","Lactiplantibacillus paraplantarum",
    "Limosilactobacillus reuteri","Limosilactobacillus fermentum","Limosilactobacillus mucosae",
    "Ligilactobacillus salivarius","Ligilactobacillus ruminis","Ligilactobacillus agilis",
    "Levilactobacillus brevis","Fructilactobacillus sanfranciscensis","Lentilactobacillus kefiri",
    "Bifidobacterium animalis","Bifidobacterium longum","Bifidobacterium breve","Bifidobacterium bifidum",
    "Bifidobacterium adolescentis","Bifidobacterium catenulatum","Bifidobacterium lactis",
    "Streptococcus thermophilus","Streptococcus salivarius","Lactococcus lactis","Lactococcus cremoris",
    "Propionibacterium freudenreichii","Saccharomyces cerevisiae","Saccharomyces boulardii",
    "Weizmannia coagulans","Bacillus subtilis","Bacillus clausii",
}
TIER_B = {"Latilactobacillus sakei","Latilactobacillus curvatus","Pediococcus acidilactici",
          "Pediococcus pentosaceus","Pediococcus parvulus","Leuconostoc mesenteroides","Leuconostoc citreum",
          "Leuconostoc lactis","Weissella cibaria","Weissella confusa","Tetragenococcus halophilus",
          "Oenococcus oeni","Enterococcus faecium","Enterococcus faecalis","Enterococcus durans",
          "Bacillus licheniformis","Bacillus pumilus","Bacillus amyloliquefaciens",
          "Kluyveromyces marxianus","Debaryomyces hansenii","Yarrowia lipolytica",
          "Acidipropionibacterium acidipropionici","Lentilactobacillus buchneri",
          "Companilactobacillus alimentarius","Companilactobacillus farciminis",
          "Furfurilactobacillus rossiae","Loigolactobacillus coryniformis"}


def prob_flag(row):
    sp = str(row["species"]).replace("_", " ")
    ge = row["genus"]
    if sp in TIER_A:
        return "A_核心益生菌种"
    if sp in TIER_B:
        return "B_QPS/发酵剂相关种"
    if ge == "Bifidobacterium":
        return "A_核心益生菌种"
    if ge in {"Lactobacillus", "Lacticaseibacillus", "Lactiplantibacillus", "Limosilactobacillus",
              "Ligilactobacillus", "Levilactobacillus", "Latilactobacillus", "Lentilactobacillus",
              "Liquorilactobacillus", "Loigolactobacillus", "Companilactobacillus",
              "Fructilactobacillus", "Furfurilactobacillus", "Schleiferilactobacillus",
              "Secundilactobacillus", "Paucilactobacillus", "Amylolactobacillus", "Dellaglioa"}:
        return "A_核心益生菌种"
    if ge in {"Pediococcus", "Leuconostoc", "Weissella", "Oenococcus", "Tetragenococcus",
              "Carnobacterium", "Propionibacterium", "Acidipropionibacterium",
              "Bacillus", "Weizmannia", "Saccharomyces", "Kluyveromyces", "Debaryomyces"}:
        return "B_QPS/发酵剂相关种"
    if ge in {"Enterococcus", "Escherichia", "Streptococcus"}:
        return "C_需谨慎/条件致病"
    return ""


m["益生菌归属"] = m.apply(prob_flag, axis=1)
m["益生菌归属"] = m["益生菌归属"].replace({"A_核心益生菌种": "A 核心益生菌种",
                                           "B_QPS/发酵剂相关种": "B QPS/发酵剂相关种",
                                           "C_需谨慎/条件致病": "C 需谨慎/条件致病"})
m["物种是否注释到种"] = m["species"].astype(str).str.contains("SGB").map(
    {True: "仅属级/未定种", False: "已定名种"})

m.to_pickle("/tmp/m_master.pkl")
m.to_csv(f"{OUT}/00_MAG主表_全部.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 1. 发酵 MAG
ferm = m[m["fermented"] == "F"].copy()
ferm.to_pickle("/tmp/ferm.pkl")
ferm.to_csv(f"{OUT}/01_发酵MAG总表.csv", index=False, encoding="utf-8-sig")

# 2. 按发酵种类汇总
rows = []
order = ["dairy", "fermented_beverages", "fermented_meat", "fermented_grains", "alcohol",
         "fermented_tubers_and_roots", "fermented_fruits_and_vegetables", "fermented_legumes",
         "fermented_seeds", "fermented_fish"]
for cat in order:
    sub = ferm[ferm["category"] == cat]
    meta_sub = meta[(meta["category"] == cat) & (meta["fermented"] == "F")]
    prok = sub[sub["superkingdom"].isin(["Bacteria", "Archaea"])]
    euk = sub[sub["superkingdom"] == "Eukaryota"]
    top_g = prok["属"].value_counts().head(3)
    top_s = prok[prok["物种是否注释到种"] == "已定名种"]["物种"].value_counts().head(3)
    rows.append({
        "发酵类别": CAT_CN.get(cat, cat),
        "category": cat,
        "样品数": len(meta_sub),
        "数据集数": meta_sub["dataset_name"].nunique(),
        "国家数": meta_sub["country"].nunique(),
        "MAG总数": len(sub),
        "原核MAG": len(prok),
        "真核MAG": len(euk),
        "高质量MAG(HQ)": (sub["质量等级"] == "高质量(HQ)").sum(),
        "中等质量MAG(MQ)": (sub["质量等级"] == "中等质量(MQ)").sum(),
        "SGB总数": sub["SGB_id"].nunique(),
        "已知种SGB(kSGB)": sub[sub["unknown"] == "kSGB"]["SGB_id"].nunique(),
        "未知种SGB(uSGB)": sub[sub["unknown"] == "uSGB"]["SGB_id"].nunique(),
        "食品新种SGB(ufSGB)": sub[sub["unknown"] == "ufSGB"]["SGB_id"].nunique(),
        "属数": prok["属"].nunique(),
        "已定名种数": prok[prok["物种是否注释到种"] == "已定名种"]["物种"].nunique(),
        "每样品平均MAG数": round(len(sub) / max(len(meta_sub), 1), 2),
        "优势属Top3": " / ".join(f"{k}({v})" for k, v in top_g.items()),
        "优势种Top3": " / ".join(f"{k}({v})" for k, v in top_s.items()),
    })
summ = pd.DataFrame(rows)
tot = {
    "发酵类别": "合计", "category": "-",
    "样品数": len(meta[meta["fermented"] == "F"]),
    "数据集数": meta[meta["fermented"] == "F"]["dataset_name"].nunique(),
    "国家数": meta[meta["fermented"] == "F"]["country"].nunique(),
    "MAG总数": len(ferm),
    "原核MAG": len(ferm[ferm["superkingdom"].isin(["Bacteria", "Archaea"])]),
    "真核MAG": len(ferm[ferm["superkingdom"] == "Eukaryota"]),
    "高质量MAG(HQ)": (ferm["质量等级"] == "高质量(HQ)").sum(),
    "中等质量MAG(MQ)": (ferm["质量等级"] == "中等质量(MQ)").sum(),
    "SGB总数": ferm["SGB_id"].nunique(),
    "已知种SGB(kSGB)": ferm[ferm["unknown"] == "kSGB"]["SGB_id"].nunique(),
    "未知种SGB(uSGB)": ferm[ferm["unknown"] == "uSGB"]["SGB_id"].nunique(),
    "食品新种SGB(ufSGB)": ferm[ferm["unknown"] == "ufSGB"]["SGB_id"].nunique(),
    "属数": ferm[ferm["superkingdom"] != "Eukaryota"]["属"].nunique(),
    "已定名种数": ferm[ferm["物种是否注释到种"] == "已定名种"]["物种"].nunique(),
    "每样品平均MAG数": round(len(ferm) / meta[meta["fermented"] == "F"].shape[0], 2),
    "优势属Top3": " / ".join(f"{k}({v})" for k, v in
                            ferm[ferm["superkingdom"] != "Eukaryota"]["属"].value_counts().head(3).items()),
    "优势种Top3": " / ".join(f"{k}({v})" for k, v in
                            ferm[ferm["物种是否注释到种"] == "已定名种"]["物种"].value_counts().head(3).items()),
}
summ = pd.concat([summ, pd.DataFrame([tot])], ignore_index=True)
summ.to_csv(f"{OUT}/02_按发酵种类汇总.csv", index=False, encoding="utf-8-sig")

# 3. 每类别的优势属矩阵 (用于热图)
genus_tab = pd.crosstab(ferm[ferm["superkingdom"] != "Eukaryota"]["属"],
                        ferm[ferm["superkingdom"] != "Eukaryota"]["发酵类别中文"])
genus_tab = genus_tab.loc[genus_tab.sum(1).sort_values(ascending=False).index[:40]]
genus_tab.to_csv(f"{OUT}/03_属水平MAG数量矩阵.csv", encoding="utf-8-sig")

# 4. SGB 级汇总
sgb = pd.concat([sgbs_p.assign(界="原核"), sgbs_e.assign(界="真核")], ignore_index=True)
sgb = sgb.rename(columns={
    "sgb_id": "SGB_id", "Unknown": "SGB类型", "Level of assigned taxonomy": "分类层级",
    "Assigned taxonomy": "完整分类", "MAGs": "MAG总数", "isolates": "参考基因组数",
    "MAGs_filtered": "过滤MAG数", "Food": "食品来源MAG", "Human": "人源MAG",
    "Animal": "动物源MAG", "Other_categories": "其他来源", "NA": "来源未知"})
sgb["SGB类型"] = sgb["SGB类型"].map({"kSGB": "已知种(kSGB)", "uSGB": "未知种(uSGB)",
                                     "ufSGB": "食品中新种(ufSGB)"}).fillna(sgb["SGB类型"])
sgb["物种"] = sgb["species"].apply(fmt_sp)
sgb["发酵来源MAG"] = sgb[[c for c in ["alcohol", "dairy", "fermented_beverages", "fermented_fish",
                                      "fermented_fruits_and_vegetables", "fermented_grains",
                                      "fermented_legumes", "fermented_meat", "fermented_seeds",
                                      "fermented_tubers_and_roots"] if c in sgb.columns]].sum(axis=1)
sgb["非发酵来源MAG"] = sgb[[c for c in ["fish", "fruits_and_vegetables", "meat", "other", "probiotics"]
                            if c in sgb.columns]].sum(axis=1)
sgb["益生菌归属"] = sgb.apply(lambda r: prob_flag({"species": r["species"], "genus": str(r["genus"])}), axis=1)
sgb["益生菌归属"] = sgb["益生菌归属"].replace({"A_核心益生菌种": "A 核心益生菌种",
                                               "B_QPS/发酵剂相关种": "B QPS/发酵剂相关种",
                                               "C_需谨慎/条件致病": "C 需谨慎/条件致病"})
sgb["发酵类别数"] = (sgb[[c for c in CAT_CN if c in sgb.columns]] > 0).sum(axis=1)
sgb.to_csv(f"{OUT}/04_SGB水平汇总_含发酵类别.csv", index=False, encoding="utf-8-sig")

# 5. 益生菌专用表
prob_mag = m[m["category"] == "probiotics"].copy()
prob_mag.sort_values(["species", "completeness"], ascending=[True, False]).to_csv(
    f"{OUT}/05_益生菌制剂来源MAG表.csv", index=False, encoding="utf-8-sig")

# 6. 全部食品中“益生菌物种”MAG
prob_all = m[m["益生菌归属"] == "A 核心益生菌种"].copy()
prob_all.sort_values(["species", "quality_rank"] if "quality_rank" in prob_all else ["species", "completeness"],
                     ascending=[True, False]).to_csv(
    f"{OUT}/06_益生菌物种MAG全库表.csv", index=False, encoding="utf-8-sig")

# 7. 益生菌物种 × 发酵类别 矩阵
prob_tab = pd.crosstab(prob_all["物种"], prob_all["发酵类别中文"])
prob_tab = prob_tab.loc[prob_tab.sum(1).sort_values(ascending=False).index]
prob_tab.to_csv(f"{OUT}/07_益生菌物种x发酵类别矩阵.csv", encoding="utf-8-sig")

# 8. 真核（酵母/霉菌）MAG
euk = ferm[ferm["superkingdom"] == "Eukaryota"].copy()
euk.sort_values(["genus", "completeness"], ascending=[True, False]).to_csv(
    f"{OUT}/08_发酵食品真核MAG表.csv", index=False, encoding="utf-8-sig")

# 9. 代表 MAG 清单（每 SGB 一株，antiSMASH 输入）
rep = (ferm[ferm["superkingdom"].isin(["Bacteria", "Archaea"])]
       .sort_values(["SGB_id", "completeness", "contamination"], ascending=[True, False, True])
       .groupby("SGB_id", as_index=False).first())
rep = rep.sort_values(["complete_rank"] if "complete_rank" in rep else ["completeness"], ascending=False)
rep["antiSMASH优先级"] = np.where(rep["物种"].isin(PROB_SPECIES_CORE) | (rep["SGB类型"] == "食品中新种(ufSGB)"),
                                  "P1", "P2")
rep.to_csv(f"{OUT}/09_antiSMASH输入MAG清单_每SGB代表株.csv", index=False, encoding="utf-8-sig")

print("MAG", len(m), "发酵", len(ferm), "益生菌制剂", len(prob_mag), "益生菌物种MAG", len(prob_all))
print(summ[["发酵类别", "样品数", "MAG总数", "原核MAG", "真核MAG", "SGB总数"]].to_string(index=False))
