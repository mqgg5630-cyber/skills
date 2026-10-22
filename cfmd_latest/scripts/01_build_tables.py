# -*- coding: utf-8 -*-
"""
cFMD v1.3.2 (main, 2026-06-18) MAG 数据整理
输入: cFMD 最新版公开总表 (GitHub SegataLab/cFMD)
输出: MAG 主表、类别汇总、SGB 汇总、益生菌表、antiSMASH 输入清单
"""
import os
import re
import numpy as np
import pandas as pd

SRC = "/tmp/cfmd_new"
OUT = "/home/user/skills/cfmd_latest/tables"
os.makedirs(OUT, exist_ok=True)

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
    "cheese": "奶酪", "water_kefir": "水开菲尔", "kefir": "奶开菲尔", "kefir_grain": "开菲尔粒",
    "milk": "乳", "raw_milk": "生乳", "whey": "乳清", "whey_protein": "乳清蛋白",
    "salami": "萨拉米", "meat": "肉", "beef": "牛肉", "pork": "猪肉", "chicken": "鸡肉",
    "raw_meat": "生肉", "meat_batter": "肉糜", "meat_mixture": "混合肉", "deli_meat": "熟食肉",
    "sausage": "香肠", "cheese_brine": "奶酪盐水", "cheese_starter": "奶酪发酵剂",
    "sourdough": "酸面团", "koumiss": "马奶酒", "tea": "茶(康普茶)", "yucha": "油茶",
    "wine": "葡萄酒", "grape_must": "葡萄醪", "grape": "葡萄", "grapes": "葡萄",
    "yogurt": "酸奶", "cured_meat_before_ripening": "成熟前腌肉",
    "soybean": "大豆", "fermented_soybean": "发酵大豆", "tofu_chili": "辣味豆腐",
    "soy_powder": "大豆粉", "probiotics": "益生菌制剂",
    "sausage_before_ripening": "成熟前香肠", "ogi": "Ogi(发酵玉米粥)",
    "spinach": "菠菜", "leafy_greens": "叶菜", "lettuce": "生菜", "cultivated lettuce": "栽培生菜",
    "choy_sum": "菜心", "chinese_broccoli": "芥蓝", "nunu": "Nunu(发酵乳)",
    "sauerkraut": "酸菜", "brine_fermented_vegetables": "盐水发酵蔬菜",
    "cattle_pig_chicken_and_turkey_sausage": "混合肉香肠",
    "red_pepper_sauce": "红椒酱", "beer": "啤酒", "kunu": "Kunu(发酵小米饮料)",
    "iru": "Iru(发酵角豆)", "palm_wine": "棕榈酒", "pre_processed_vegetables": "预处理蔬菜",
    "post_processed_vegetables": "后处理蔬菜", "coffee": "咖啡", "pulque": "Pulque",
    "honey": "蜂蜜", "kimchi": "泡菜", "gari": "Gari(发酵木薯)",
    "cattle_pig_sheep_and_horse_sausage": "混合肉香肠", "fufu": "Fufu(发酵木薯)",
    "ogiri": "Ogiri(发酵瓜籽)", "ugi": "Ugi(发酵谷物)", "skate_fish": "鳐鱼",
    "cod": "鳕鱼", "salmon": "三文鱼", "grain": "谷物", "kvass": "格瓦斯",
    "ugba": "Ugba(发酵非洲油豆)", "wara": "Wara(发酵豆制品)", "lafun": "Lafun(发酵木薯)",
    "pito": "Pito(发酵高粱酒)", "nono": "Nono(发酵乳)", "burukutu": "Burukutu(发酵高粱啤酒)",
    "injera": "英吉拉(发酵苔麸饼)", "daikon": "白萝卜", "otika": "Otika(发酵高粱)",
    "zonkom": "Zonkom(发酵小米)", "agadagidi": "Agadagidi(发酵车前草)",
    "okpehe": "Okpehe(发酵槐豆)", "haddock": "黑线鳕", "arctic_char": "北极红点鲑",
    "laban": "Laban(发酵乳)", "cabbage": "卷心菜", "boza": "Boza(发酵谷物饮料)",
    "turnip": "芜菁", "orange": "橙", "tepache": "Tepache(发酵菠萝)",
    "ginger_beer": "姜汁啤酒", "cucumber": "黄瓜", "tofu_chili": "辣味豆腐",
    "pickled_vegetables": "腌蔬菜", "raw_sauerkraut_and_juniper_berries": "生酸菜+杜松子",
    "brown_rice_amazake": "糙米甘酒", "mead": "蜂蜜酒",
    "apple_cider_vinegar": "苹果醋", "dilly_carrots": "莳萝胡萝卜",
    "garlic": "大蒜", "dukkah": "Dukkah(混合香料)", "ginger": "姜",
    "okra": "秋葵", "tomato_and_mustards": "番茄+芥菜籽", "carrot_sticks": "胡萝卜条",
    "chocolate_coating": "巧克力涂层", "emu": "鸸鹋", "massa": "Massa(发酵谷物)",
    "foura": "Foura(发酵小米)", "soumbala": "Soumbala(发酵角豆)",
    "mou": "Mou(发酵乳)", "attieke": "Attieke(发酵木薯)", "dolo": "Dolo(发酵高粱啤酒)",
    "koko": "Koko(发酵小米)", "fura": "Fura(发酵小米)", "maasa": "Maasa(发酵小米)",
    "brukina": "Brukina(发酵乳+小米)", "wagashi": "Wagashi(发酵乳)",
    "kantong": "Kantong(发酵木薯叶)", "dawa_dawa": "Dawa-dawa(发酵角豆)",
    "cocoa_beans": "可可豆", "pozol": "Pozol(发酵玉米)", "amaranth": "苋菜",
    "korean_rice_vinegar": "韩国米醋", "keem": "Keem(发酵小米)", "obiolor": "Obiolor(发酵高粱)",
    "sekete": "Sekete(发酵高粱)", "otiru": "Otiru(发酵木薯)", "mou": "Mou(发酵乳)",
    "shiso-zoku": "紫苏", "mustard": "芥菜", "radish": "萝卜", "lotus root": "莲藕",
    "cantaloupe": "哈密瓜", "honeydew_melon": "蜜瓜", "papaya": "木瓜",
    "strawberry": "草莓", "watermelon": "西瓜", "asparagus broccoli": "芦笋西兰花",
    "anchioves": "凤尾鱼", "prawns": "虾", "shrimp": "虾", "oysters": "牡蛎",
    "golden trout": "金鳟", "mallard": "野鸭", "paralichthys_olivaceus": "牙鲆",
    "rawcarcasses/meat_before_processing": "胴体/未加工肉", "cereal_batter": "谷物面糊",
    "rostagroekport_voroznyj": "腌黄瓜(俄式)", "ruza": "Ruza(发酵乳)", "agousha": "Agousha(发酵乳)",
    "brown kelp": "海带",
}


def fmt_sp(x):
    x = str(x)
    if x in ("nan", "None"):
        return ""
    if "_SGB" in x:
        g, sg = x.split("_SGB")
        return f"{g} sp. SGB{sg}"
    return x.replace("_", " ")


# ---------------------------------------------------------------- 读表
meta = pd.read_csv(f"{SRC}/cFMD_metadata.tsv", sep="\t", low_memory=False, encoding="latin-1")
meta = meta.rename(columns={"fermented/non-fermented": "fermented"})
meta["发酵类别中文"] = meta["category"].map(CAT_CN).fillna(meta["category"])
meta["食品类型中文"] = meta["type"].str.strip().map(TYPE_CN).fillna(meta["type"])

mags = pd.read_csv(f"{SRC}/cFMD_mags_list.tsv", sep="\t", low_memory=False, encoding="latin-1")
ds = pd.read_csv(f"{SRC}/cFMD_datasets.tsv", sep="\t", encoding="latin-1", low_memory=False)
ds.columns = [c.strip() for c in ds.columns]

# ---------------------------------------------------------------- 合并
m = mags.merge(
    meta[["dataset_name", "sample_id", "macrocategory", "category", "type", "subtype",
          "commercial_name", "fermented", "country"]],
    left_on=["dataset_id", "sample_id"], right_on=["dataset_name", "sample_id"], how="left"
)
m["发酵类别中文"] = m["category"].map(CAT_CN).fillna(m["category"])
m["食品类型中文"] = m["type"].str.strip().map(TYPE_CN).fillna(m["type"])
m["界"] = m["superkingdom"].map({"Bacteria": "细菌", "Eukaryota": "真核生物",
                                 "Archaea": "古菌"}).fillna("未定")
m["是否发酵"] = m["fermented"].map({"F": "发酵", "NF": "非发酵"})
m["SGB类型"] = m["unknown"].map({"kSGB": "已知种(kSGB)", "uSGB": "未知种(uSGB)",
                                 "ufSGB": "食品中新种(ufSGB)"}).fillna("未归属SGB")

# 源表中同一 SGB 的 MAG 偶有 uSGB / ufSGB 两种标注（全库 21 个 SGB），
# 按该 SGB 内多数 MAG 的标注统一；票数相同时取更保守的 uSGB，保证每个 SGB 只归一类。
_v = (m[m["SGB_id"].notna()].groupby(["SGB_id", "SGB类型"]).size()
      .unstack(fill_value=0))
_prio = ["食品中新种(ufSGB)", "未知种(uSGB)", "已知种(kSGB)"]  # 列顺序
_tie = ["未知种(uSGB)", "食品中新种(ufSGB)", "已知种(kSGB)"]  # 平票取更保守者
_v = _v.reindex(columns=[c for c in _prio if c in _v.columns], fill_value=0)
_sgb_type = pd.Series(
    [sorted(_v.columns, key=lambda c: (-_v.loc[i, c], _tie.index(c)))[0] for i in _v.index],
    index=_v.index)
m["SGB类型"] = m["SGB_id"].map(_sgb_type).fillna(m["SGB类型"])
m["完整度"] = m["completeness"].round(2)
m["污染度"] = m["contamination"].round(2)
m["基因组大小Mb"] = (m["genome_size"] / 1e6).round(3)
m["GC%"] = (m["GC_content"] * 100).round(2)


def qual(r):
    if r["completeness"] >= 90 and r["contamination"] < 5:
        return "高质量(HQ)"
    if r["completeness"] >= 50 and r["contamination"] < 5:
        return "中等质量(MQ)"
    return "未达标"


m["质量等级"] = m.apply(qual, axis=1)
m["物种"] = m["species"].apply(fmt_sp)
m["属"] = m["genus"].astype(str).replace({"nan": ""})
m["物种是否注释到种"] = m["species"].astype(str).str.contains("SGB").map({True: "仅属级/未定种", False: "已定名种"})
m["纳入分析"] = (m["质量等级"].isin(["高质量(HQ)", "中等质量(MQ)"])) & (m["SGB_id"].notna())
m.loc[m["SGB_id"].isna(), "物种是否注释到种"] = "未归属SGB"

# ---------------------------------------------------------------- 益生菌
PROB_SPECIES_CORE = {
    "Lactobacillus acidophilus", "Lactobacillus gasseri", "Lactobacillus johnsonii",
    "Lactobacillus crispatus", "Lactobacillus delbrueckii", "Lactobacillus helveticus",
    "Lactobacillus amylovorus", "Lactobacillus gallinarum",
    "Lacticaseibacillus rhamnosus", "Lacticaseibacillus paracasei", "Lacticaseibacillus casei",
    "Lactiplantibacillus plantarum", "Lactiplantibacillus paraplantarum",
    "Limosilactobacillus reuteri", "Limosilactobacillus fermentum", "Limosilactobacillus mucosae",
    "Ligilactobacillus salivarius", "Ligilactobacillus ruminis", "Ligilactobacillus agilis",
    "Levilactobacillus brevis", "Fructilactobacillus sanfranciscensis", "Lentilactobacillus kefiri",
    "Bifidobacterium animalis", "Bifidobacterium longum", "Bifidobacterium breve",
    "Bifidobacterium bifidum", "Bifidobacterium adolescentis", "Bifidobacterium catenulatum",
    "Bifidobacterium lactis",
    "Streptococcus thermophilus", "Streptococcus salivarius",
    "Lactococcus lactis", "Lactococcus cremoris",
    "Propionibacterium freudenreichii", "Saccharomyces cerevisiae", "Saccharomyces boulardii",
    "Weizmannia coagulans", "Bacillus subtilis", "Bacillus clausii",
}
TIER_B = {
    "Latilactobacillus sakei", "Latilactobacillus curvatus", "Pediococcus acidilactici",
    "Pediococcus pentosaceus", "Pediococcus parvulus", "Leuconostoc mesenteroides",
    "Leuconostoc citreum", "Leuconostoc lactis", "Weissella cibaria", "Weissella confusa",
    "Tetragenococcus halophilus", "Oenococcus oeni", "Enterococcus faecium",
    "Enterococcus faecalis", "Enterococcus durans", "Bacillus licheniformis",
    "Bacillus pumilus", "Bacillus amyloliquefaciens", "Kluyveromyces marxianus",
    "Debaryomyces hansenii", "Yarrowia lipolytica", "Acidipropionibacterium acidipropionici",
    "Lentilactobacillus buchneri", "Companilactobacillus alimentarius",
    "Companilactobacillus farciminis", "Furfurilactobacillus rossiae",
    "Loigolactobacillus coryniformis",
}
LAB_GENERA = {
    "Lactobacillus", "Lacticaseibacillus", "Lactiplantibacillus", "Limosilactobacillus",
    "Ligilactobacillus", "Levilactobacillus", "Latilactobacillus", "Lentilactobacillus",
    "Liquorilactobacillus", "Loigolactobacillus", "Companilactobacillus",
    "Fructilactobacillus", "Furfurilactobacillus", "Schleiferilactobacillus",
    "Secundilactobacillus", "Paucilactobacillus", "Amylolactobacillus", "Dellaglioa",
    "Pediococcus", "Leuconostoc", "Weissella", "Oenococcus", "Tetragenococcus",
    "Carnobacterium", "Enterococcus", "Streptococcus", "Lactococcus", "Bifidobacterium",
    "Propionibacterium", "Acidipropionibacterium", "Bacillus", "Weizmannia",
}


def prob_flag(row):
    sp = str(row["species"]).replace("_", " ")
    ge = row["genus"]
    if sp in PROB_SPECIES_CORE:
        return "A 核心益生菌种"
    if sp in TIER_B:
        return "B QPS/发酵剂相关种"
    if ge == "Bifidobacterium":
        return "A 核心益生菌种"
    if ge in {"Lactobacillus", "Lacticaseibacillus", "Lactiplantibacillus", "Limosilactobacillus",
              "Ligilactobacillus", "Levilactobacillus", "Latilactobacillus", "Lentilactobacillus",
              "Liquorilactobacillus", "Loigolactobacillus", "Companilactobacillus",
              "Fructilactobacillus", "Furfurilactobacillus", "Schleiferilactobacillus",
              "Secundilactobacillus", "Paucilactobacillus", "Amylolactobacillus", "Dellaglioa"}:
        return "A 核心益生菌种"
    if ge in {"Pediococcus", "Leuconostoc", "Weissella", "Oenococcus", "Tetragenococcus",
              "Carnobacterium", "Propionibacterium", "Acidipropionibacterium",
              "Bacillus", "Weizmannia", "Saccharomyces", "Kluyveromyces", "Debaryomyces"}:
        return "B QPS/发酵剂相关种"
    if ge in {"Enterococcus", "Escherichia", "Streptococcus"}:
        return "C 需谨慎/条件致病"
    return ""


m["益生菌归属"] = m.apply(prob_flag, axis=1)

m.to_pickle("/tmp/m_new.pkl")
m.to_csv(f"{OUT}/00_MAG主表_全部.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 分析集
A = m[m["纳入分析"]].copy()
A.to_pickle("/tmp/A_new.pkl")
ferm = A[A["fermented"] == "F"].copy()
ferm.to_pickle("/tmp/ferm_new.pkl")
ferm.to_csv(f"{OUT}/01_发酵MAG总表.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 类别汇总
ORDER = ["dairy", "fermented_beverages", "fermented_meat", "fermented_grains", "alcohol",
         "fermented_fruits_and_vegetables", "fermented_tubers_and_roots", "fermented_legumes",
         "fermented_seeds", "fermented_fish"]
rows = []
for cat in ORDER:
    sub = ferm[ferm["category"] == cat]
    ms = meta[(meta["category"] == cat) & (meta["fermented"] == "F")]
    prok = sub[sub["superkingdom"].isin(["Bacteria", "Archaea"])]
    euk = sub[sub["superkingdom"] == "Eukaryota"]
    allr = m[(m["category"] == cat) & (m["fermented"] == "F")]
    rows.append({
        "发酵类别": CAT_CN.get(cat, cat), "category": cat,
        "样品数": len(ms), "数据集数": ms["dataset_name"].nunique(), "国家数": ms["country"].nunique(),
        "有关联MAG样品数": allr[["dataset_id", "sample_id"]].drop_duplicates().shape[0],
        "MAG记录数": len(allr),
        "记录_原核": allr["superkingdom"].isin(["Bacteria", "Archaea"]).sum(),
        "记录_真核": (allr["superkingdom"] == "Eukaryota").sum(),
        "记录_未分类": (allr["superkingdom"].isna()).sum(),
        "HQ_记录数": ((allr["completeness"] >= 90) & (allr["contamination"] < 5)).sum(),
        "MQ_记录数": ((allr["completeness"] >= 50) & (allr["completeness"] < 90)
                     & (allr["contamination"] < 5)).sum(),
        "未纳入分析": len(allr) - len(sub),
        "MAG总数": len(sub), "原核MAG": len(prok), "真核MAG": len(euk),
        "高质量MAG(HQ)": (sub["质量等级"] == "高质量(HQ)").sum(),
        "中等质量MAG(MQ)": (sub["质量等级"] == "中等质量(MQ)").sum(),
        "SGB总数": sub["SGB_id"].nunique(),
        "已知种SGB(kSGB)": sub[sub["SGB类型"] == "已知种(kSGB)"]["SGB_id"].nunique(),
        "未知种SGB(uSGB)": sub[sub["SGB类型"] == "未知种(uSGB)"]["SGB_id"].nunique(),
        "食品新种SGB(ufSGB)": sub[sub["SGB类型"] == "食品中新种(ufSGB)"]["SGB_id"].nunique(),
        "属数": prok["属"].nunique(),
        "已定名种数": prok[prok["物种是否注释到种"] == "已定名种"]["物种"].nunique(),
        "每样品平均MAG数": round(len(sub) / max(allr[["dataset_id", "sample_id"]].drop_duplicates().shape[0], 1), 2),
        "优势属Top3": " / ".join(f"{k}({v})" for k, v in prok["属"].value_counts().head(3).items()),
        "优势种Top3": " / ".join(f"{k}({v})" for k, v in
                                prok[prok["物种是否注释到种"] == "已定名种"]["物种"].value_counts().head(3).items()),
    })
summ = pd.DataFrame(rows)
F_meta = meta[meta["fermented"] == "F"]
F_all = m[m["fermented"] == "F"]
tot = {
    "发酵类别": "合计", "category": "-",
    "样品数": len(F_meta), "数据集数": F_meta["dataset_name"].nunique(), "国家数": F_meta["country"].nunique(),
    "有关联MAG样品数": F_all[["dataset_id", "sample_id"]].drop_duplicates().shape[0],
    "MAG记录数": len(F_all),
    "记录_原核": int(F_all["superkingdom"].isin(["Bacteria", "Archaea"]).sum()),
    "记录_真核": int((F_all["superkingdom"] == "Eukaryota").sum()),
    "记录_未分类": int(F_all["superkingdom"].isna().sum()),
    "HQ_记录数": int(((F_all["completeness"] >= 90) & (F_all["contamination"] < 5)).sum()),
    "MQ_记录数": int(((F_all["completeness"] >= 50) & (F_all["completeness"] < 90)
                     & (F_all["contamination"] < 5)).sum()),
    "未纳入分析": len(F_all) - len(ferm),
    "MAG总数": len(ferm),
    "原核MAG": len(ferm[ferm["superkingdom"].isin(["Bacteria", "Archaea"])]),
    "真核MAG": len(ferm[ferm["superkingdom"] == "Eukaryota"]),
    "高质量MAG(HQ)": (ferm["质量等级"] == "高质量(HQ)").sum(),
    "中等质量MAG(MQ)": (ferm["质量等级"] == "中等质量(MQ)").sum(),
    "SGB总数": ferm["SGB_id"].nunique(),
    "已知种SGB(kSGB)": ferm[ferm["SGB类型"] == "已知种(kSGB)"]["SGB_id"].nunique(),
    "未知种SGB(uSGB)": ferm[ferm["SGB类型"] == "未知种(uSGB)"]["SGB_id"].nunique(),
    "食品新种SGB(ufSGB)": ferm[ferm["SGB类型"] == "食品中新种(ufSGB)"]["SGB_id"].nunique(),
    "属数": ferm[ferm["superkingdom"] != "Eukaryota"]["属"].nunique(),
    "已定名种数": ferm[ferm["物种是否注释到种"] == "已定名种"]["物种"].nunique(),
    "每样品平均MAG数": round(len(ferm) / F_all[["dataset_id", "sample_id"]].drop_duplicates().shape[0], 2),
    "优势属Top3": " / ".join(f"{k}({v})" for k, v in
                            ferm[ferm["superkingdom"] != "Eukaryota"]["属"].value_counts().head(3).items()),
    "优势种Top3": " / ".join(f"{k}({v})" for k, v in
                            ferm[ferm["物种是否注释到种"] == "已定名种"]["物种"].value_counts().head(3).items()),
}
summ = pd.concat([summ, pd.DataFrame([tot])], ignore_index=True)
summ.to_csv(f"{OUT}/02_按发酵种类汇总.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 属矩阵
pk = ferm[ferm["superkingdom"] != "Eukaryota"]
gt = pd.crosstab(pk["属"], pk["发酵类别中文"])
gt = gt.loc[gt.sum(axis=1).sort_values(ascending=False).index[:40]]
gt.to_csv(f"{OUT}/03_属水平MAG数量矩阵.csv", encoding="utf-8-sig")

# ---------------------------------------------------------------- SGB 汇总（新版无 cFMD 级 SGB 表，自行聚合）
CATS = [c for c in ORDER]
srows = []
for sgb, d in A.groupby("SGB_id"):
    first = d.iloc[0]
    rec = {
        "SGB_id": sgb, "SGB类型": first["SGB类型"], "分类层级": first["assigned_taxonomy_level"],
        "superkingdom": first["superkingdom"], "phylum": first["phylum"], "class": first["class"],
        "order": first["order"], "family": first["family"], "genus": first["genus"],
        "species": first["species"], "物种": first["物种"],
        "MAG总数": len(d), "HQ数": (d["质量等级"] == "高质量(HQ)").sum(),
        "发酵来源MAG": (d["fermented"] == "F").sum(),
        "非发酵来源MAG": (d["fermented"] == "NF").sum(),
        "样品数": d["sample_id"].nunique(), "数据集数": d["dataset_id"].nunique(),
        "国家数": d["country"].nunique(),
        "界": first["界"],
    }
    for c in CATS:
        rec[CAT_CN[c]] = (d["category"] == c).sum()
    rec["发酵类别数"] = sum(1 for c in CATS if (d["category"] == c).sum() > 0)
    srows.append(rec)
sgb = pd.DataFrame(srows)
sgb["益生菌归属"] = sgb.apply(lambda r: prob_flag({"species": r["species"], "genus": str(r["genus"])}), axis=1)
sgb = sgb.sort_values("MAG总数", ascending=False)
sgb.to_csv(f"{OUT}/04_SGB水平汇总_含发酵类别.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 益生菌
A[A["category"] == "probiotics"].sort_values(["species", "completeness"], ascending=[True, False]) \
    .to_csv(f"{OUT}/05_益生菌制剂来源MAG表.csv", index=False, encoding="utf-8-sig")

prob_all = ferm[ferm["益生菌归属"] == "A 核心益生菌种"].copy()
prob_all.to_csv(f"{OUT}/06_益生菌物种MAG全库表.csv", index=False, encoding="utf-8-sig")

pt = pd.crosstab(prob_all["物种"], prob_all["发酵类别中文"])
pt = pt.loc[pt.sum(axis=1).sort_values(ascending=False).index]
pt.to_csv(f"{OUT}/07_益生菌物种x发酵类别矩阵.csv", encoding="utf-8-sig")

# 严格种级名单（PROB_SPECIES_CORE）：与 A 层的属级放宽口径分开统计
strict = ferm[ferm["species"].astype(str).str.replace("_", " ", regex=False).isin(PROB_SPECIES_CORE)].copy()
strict.sort_values(["物种", "completeness"], ascending=[True, False]).to_csv(
    f"{OUT}/21_益生菌严格名单MAG表.csv", index=False, encoding="utf-8-sig")

tiers = []
for name, d in [("A 核心：乳酸菌与双歧杆菌类群", prob_all),
                ("A 严格：名单内益生菌种", strict),
                ("B QPS/发酵剂相关种", ferm[ferm["益生菌归属"] == "B QPS/发酵剂相关种"]),
                ("C 需谨慎(肠球菌等)", ferm[ferm["益生菌归属"] == "C 需谨慎/条件致病"]),
                ("益生菌制剂样品", A[A["category"] == "probiotics"])]:
    tiers.append({"层级": name, "种数": d["物种"].nunique(), "SGB数": d["SGB_id"].nunique(),
                  "MAG数": len(d), "HQ数": (d["质量等级"] == "高质量(HQ)").sum()})
tier_df = pd.DataFrame(tiers)
tier_df.to_csv(f"{OUT}/22_益生菌分层汇总.csv", index=False, encoding="utf-8-sig")
print(tier_df.to_string(index=False))

# ---------------------------------------------------------------- 真核
euk = ferm[ferm["superkingdom"] == "Eukaryota"].copy()
euk.sort_values(["genus", "completeness"], ascending=[True, False]).to_csv(
    f"{OUT}/08_发酵食品真核MAG表.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- antiSMASH 输入
rep = (ferm[ferm["superkingdom"].isin(["Bacteria", "Archaea"])]
       .sort_values(["SGB_id", "completeness", "contamination"], ascending=[True, False, True])
       .groupby("SGB_id", as_index=False).first())
rep = rep.sort_values("completeness", ascending=False)
rep["antiSMASH优先级"] = np.where(rep["物种"].isin(PROB_SPECIES_CORE) | (rep["SGB类型"] == "食品中新种(ufSGB)"),
                                  "P1", "P2")
rep.to_csv(f"{OUT}/09_antiSMASH输入MAG清单_每SGB代表株.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- type 明细
# 样品、数据集、国家一律按元数据统计（含没有 MAG 的样品），MAG 相关列按分析集与全部记录分别给出。
trows = []
for (cat, typ), ms in F_meta.groupby(["category", "type"]):
    d = ferm[(ferm["category"] == cat) & (ferm["type"] == typ)]
    dall = m[(m["category"] == cat) & (m["type"] == typ) & (m["fermented"] == "F")]
    prok2 = d[d["superkingdom"] != "Eukaryota"]
    trows.append({
        "发酵类别": ms["发酵类别中文"].iloc[0], "食品类型": ms["食品类型中文"].iloc[0], "type_code": typ,
        "样品数": len(ms),
        "有关联MAG样品数": dall[["dataset_id", "sample_id"]].drop_duplicates().shape[0],
        "数据集数": ms["dataset_name"].nunique(), "国家数": ms["country"].nunique(),
        "MAG记录数": len(dall), "MAG数": len(d), "HQ数": (d["质量等级"] == "高质量(HQ)").sum(),
        "SGB数": d["SGB_id"].nunique(), "属数": prok2["属"].nunique(),
        "优势种Top3": " / ".join(f"{k}({v})" for k, v in prok2["物种"].value_counts().head(3).items()),
        "代表MAG": d.sort_values("completeness", ascending=False)["MAG_id"].iloc[0] if len(d) else "",
    })
pd.DataFrame(trows).sort_values("样品数", ascending=False).to_csv(
    f"{OUT}/20_发酵类型明细_按type.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------- 与外部汇总表核对
# 外部表（cFMD_全发酵食品统计汇总.xlsx）按"与 F 样品关联的 MAG 记录"统计，不做质量与 SGB 过滤。
ext = {
    "dairy": (2336, 11436, 10850), "fermented_beverages": (456, 2154, 1905),
    "fermented_meat": (168, 618, 562), "fermented_grains": (83, 244, 233),
    "alcohol": (48, 161, 89), "fermented_fruits_and_vegetables": (62, 166, 144),
    "fermented_tubers_and_roots": (24, 123, 116), "fermented_legumes": (26, 190, 184),
    "fermented_seeds": (65, 397, 361), "fermented_fish": (25, 233, 232),
}
srow = []
for cat in ORDER:
    r = summ[summ["category"] == cat].iloc[0]
    es, er, eb = ext[cat]
    srow.append({
        "发酵类别": r["发酵类别"], "category": cat,
        "外部表_样品": es, "本表_样品": int(r["样品数"]), "样品差": int(r["样品数"]) - es,
        "外部表_MAG记录": er, "本表_MAG记录": int(r["MAG记录数"]), "记录差": int(r["MAG记录数"]) - er,
        "外部表_Bacteria": eb, "本表_原核": int(r["记录_原核"]), "原核差": int(r["记录_原核"]) - eb,
        "本表_纳入分析": int(r["MAG总数"]),
        "剔除_原核": int(r["记录_原核"]) - int(r["原核MAG"]),
        "剔除_真核": int(r["记录_真核"]) - int(r["真核MAG"]),
        "剔除_未分类": int(r["记录_未分类"]),
    })
rec = pd.DataFrame(srow)
rec.loc[len(rec)] = {"发酵类别": "合计", "category": "-",
                     "外部表_样品": int(rec["外部表_样品"].sum()), "本表_样品": int(rec["本表_样品"].sum()),
                     "样品差": int(rec["样品差"].sum()),
                     "外部表_MAG记录": int(rec["外部表_MAG记录"].sum()),
                     "本表_MAG记录": int(rec["本表_MAG记录"].sum()), "记录差": int(rec["记录差"].sum()),
                     "外部表_Bacteria": int(rec["外部表_Bacteria"].sum()),
                     "本表_原核": int(rec["本表_原核"].sum()), "原核差": int(rec["原核差"].sum()),
                     "本表_纳入分析": int(rec["本表_纳入分析"].sum()),
                     "剔除_原核": int(rec["剔除_原核"].sum()), "剔除_真核": int(rec["剔除_真核"].sum()),
                     "剔除_未分类": int(rec["剔除_未分类"].sum())}
rec.to_csv(f"{OUT}/23_与外部汇总表核对.csv", index=False, encoding="utf-8-sig")
print(rec.tail(1).to_string(index=False))

print("总 MAG", len(m), "纳入分析", len(A), "发酵", len(ferm))
print(summ[["发酵类别", "样品数", "MAG总数", "原核MAG", "真核MAG", "SGB总数"]].to_string(index=False))
print("\nSGB", len(sgb), " A 核心益生菌 MAG", len(prob_all), "SGB", prob_all.SGB_id.nunique())
print("probiotics MAG", (m["category"] == "probiotics").sum())
