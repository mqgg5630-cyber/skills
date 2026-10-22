# -*- coding: utf-8 -*-
"""BGC 预期工作量表 + SGB 优先级清单"""
import pandas as pd, numpy as np

OUT = "/home/user/skills/cfmd_latest/tables"
f = pd.read_pickle("/tmp/ferm_new.pkl")
prok = f[f["superkingdom"] != "Eukaryota"]
euk = f[f["superkingdom"] == "Eukaryota"]

# 文献经验值：每个基因组被 antiSMASH 识别的 BGC 数量区间
EXP = {
    "Lactococcus": (3, 6, "bacteriocin/lanthipeptide 为主，罕见 NRPS/PKS"),
    "Lactobacillus": (2, 5, "bacteriocin 为主；部分种带 head-to-tail 环肽"),
    "Lacticaseibacillus": (2, 5, "bacteriocin / RiPP-like 为主"),
    "Lactiplantibacillus": (4, 7, "plantaricin 多拷贝簇；偶见 lanthipeptide"),
    "Limosilactobacillus": (2, 5, "环状细菌素"),
    "Ligilactobacillus": (3, 6, "salivaricin 类 lanthipeptide"),
    "Levilactobacillus": (2, 4, "bacteriocin"),
    "Latilactobacillus": (2, 4, "bacteriocin（sakacin/curvacin）"),
    "Lentilactobacillus": (2, 4, "bacteriocin"),
    "Liquorilactobacillus": (2, 4, "bacteriocin"),
    "Leuconostoc": (2, 5, "bacteriocin + EPS/葡聚糖簇"),
    "Pediococcus": (2, 5, "pediocin 类 IIa 细菌素"),
    "Weissella": (2, 4, "bacteriocin"),
    "Oenococcus": (1, 3, "bacteriocin"),
    "Tetragenococcus": (1, 3, "bacteriocin"),
    "Enterococcus": (3, 6, "cytolysin 型 lanthipeptide + enterocin"),
    "Streptococcus": (2, 5, "blp/thermophilin 类细菌素"),
    "Bifidobacterium": (1, 3, "bifidocin 类细菌素；rare lanthipeptide"),
    "Carnobacterium": (2, 4, "IIa 细菌素"),
    "Propionibacterium": (2, 4, "propionicin 类细菌素"),
    "Bacillus": (7, 14, "NRPS/PKS 丰富：surfactin、fengycin、bacillaene、bacillibactin"),
    "Weizmannia": (2, 4, "bacteriocin"),
    "Staphylococcus": (2, 5, "铁载体、NRPS"),
    "Pseudomonas": (4, 9, "铁载体、吩嗪、NRPS/PKS"),
    "Serratia": (4, 8, "prodigiosin 等杂合 NRPS-PKS"),
    "Brevibacterium": (1, 4, "铁载体、类胡萝卜素萜类"),
    "Corynebacterium": (1, 4, "铁载体"),
    "Brachybacterium": (1, 3, "萜类/铁载体"),
    "Acetobacter": (0, 2, "纤维素合成、少见 PKS"),
    "Komagataeibacter": (0, 2, "纤维素合成簇"),
    "Gluconobacter": (0, 2, "少见"),
    "Halomonas": (1, 3, "ectoine、铁载体"),
    "Alkalibacterium": (0, 2, "少见"),
    "Zymomonas": (0, 1, "基本无次级代谢簇"),
    "Psychrobacter": (0, 2, "少见"),
    "Flaviflexus": (0, 2, "少见"),
    "Garicola": (0, 2, "少见"),
    "Clostridium": (3, 6, "NRPS/细菌素"),
}

rows = []
for g, sub in prok.groupby("属"):
    lo, hi, note = EXP.get(g, (1, 4, "同科经验值"))
    sgbs = sub["SGB_id"].nunique()
    mags = len(sub)
    hq = (sub["质量等级"] == "高质量(HQ)").sum()
    rows.append({
        "属": g,
        "发酵食品MAG数": mags,
        "HQ MAG数": int(hq),
        "SGB数": sgbs,
        "建议antiSMASH输入数(每SGB代表株)": sgbs,
        "单基因组BGC预期下限": lo,
        "单基因组BGC预期上限": hi,
        "预期BGC总数(下限)": sgbs * lo,
        "预期BGC总数(上限)": sgbs * hi,
        "预期主要簇类型": note,
    })
df = pd.DataFrame(rows).sort_values("发酵食品MAG数", ascending=False)
df.to_csv(f"{OUT}/18_antiSMASH_BGC预期工作量_按属.csv", index=False, encoding="utf-8-sig")

# 真核
erows = []
EUK_EXP = {"Saccharomyces": (0, 2, "萜类/极少"), "Debaryomyces": (0, 2, "少见"),
           "Penicillium": (20, 40, "NRPS/PKS 丰富，roquefortine、andrastin、霉毒素"),
           "Aspergillus": (20, 45, "NRPS/PKS 极丰富，含霉毒素簇"),
           "Scopulariopsis": (10, 25, "NRPS/PKS"),
           "Kluyveromyces": (0, 2, "少见"), "Pichia": (0, 3, "少见"),
           "Mucor": (8, 18, "萜类/生物碱"), "Fusarium": (15, 30, "霉毒素为主"),
           "Yarrowia": (0, 3, "少见"), "Brettanomyces": (0, 2, "少见"),
           "Hanseniaspora": (0, 2, "少见"), "Lachancea": (0, 2, "少见"),
           "Candida": (1, 4, "少见"), "Zygosaccharomyces": (0, 2, "少见"),
           "Zygotorulaspora": (0, 2, "少见"), "Wickerhamiella": (0, 2, "少见"),
           "Kazachstania": (0, 2, "少见"), "Diutina": (0, 2, "少见"),
           "Teunomyces": (0, 2, "少见"), "Blastobotrys": (0, 2, "少见")}
for g, sub in euk.groupby("属"):
    lo, hi, note = EUK_EXP.get(g, (0, 3, "少见"))
    erows.append({"属": g, "发酵食品MAG数": len(sub), "SGB数": sub["SGB_id"].nunique(),
                  "单基因组BGC预期下限": lo, "单基因组BGC预期上限": hi,
                  "预期BGC总数(下限)": sub["SGB_id"].nunique() * lo,
                  "预期BGC总数(上限)": sub["SGB_id"].nunique() * hi,
                  "预期主要簇类型": note})
edf = pd.DataFrame(erows).sort_values("发酵食品MAG数", ascending=False)
edf.to_csv(f"{OUT}/19_antiSMASH_BGC预期工作量_真核属.csv", index=False, encoding="utf-8-sig")

print(df.head(20).to_string(index=False))
print("\n合计 SGB:", df["SGB数"].sum(), "预期BGC:", df["预期BGC总数(下限)"].sum(), "-", df["预期BGC总数(上限)"].sum())
print("真核 SGB:", edf["SGB数"].sum(), "预期BGC:", edf["预期BGC总数(下限)"].sum(), "-", edf["预期BGC总数(上限)"].sum())
print(edf.head(10).to_string(index=False))
