# -*- coding: utf-8 -*-
"""MetaPhlAn4 物种谱（新版按数据集分文件，先合并）"""
import glob, os
import numpy as np
import pandas as pd

SRC = "/tmp/cfmd_new"
OUT = "/home/user/skills/cfmd_latest/tables"

files = sorted(glob.glob(f"{SRC}/cFMD_data/*/*_taxonomic_profiles.tsv"))
print("数据集谱文件", len(files))

def _read(fpath):
    d = pd.read_csv(fpath, sep="\t", low_memory=False, encoding="latin-1")
    d = d.rename(columns={d.columns[0]: "sample"})
    return d.set_index("sample")


allf = pd.concat([_read(f) for f in files], axis=0)
allf.index.name = "sample"
allf = allf.apply(pd.to_numeric, errors="coerce").fillna(0.0)
print("合并后", allf.shape)

# 物种水平行
sp = allf[allf.index.astype(str).str.contains(r"\|s__[A-Za-z]", regex=True)].copy()
sp.index = [r.split("|s__")[1].split("|")[0] for r in sp.index]
sp = sp.groupby(level=0).sum()
sp = sp.loc[:, sp.sum(axis=0) > 0]
print("物种行", sp.shape)
sp.to_pickle("/tmp/sp_new.pkl")

rel = sp.div(sp.sum(axis=0), axis=1).fillna(0)


def shannon(x):
    x = x[x > 0]
    return float(-(x * np.log(x)).sum())


md = pd.read_csv(f"{SRC}/cFMD_metadata.tsv", sep="\t", low_memory=False, encoding="latin-1")
md = md.rename(columns={"fermented/non-fermented": "fermented"})
md["key"] = md["dataset_name"] + "__" + md["sample_id"]
CAT_CN = {"dairy": "乳制品", "fermented_beverages": "发酵饮料", "fermented_meat": "发酵肉制品",
          "fermented_grains": "发酵谷物制品", "alcohol": "含酒精发酵饮料",
          "fermented_tubers_and_roots": "发酵薯类与根茎", "fermented_fruits_and_vegetables": "发酵果蔬",
          "fermented_legumes": "发酵豆类", "fermented_seeds": "发酵种子/油料", "fermented_fish": "发酵鱼制品",
          "probiotics": "益生菌制剂", "meat": "肉制品(非发酵)", "fruits_and_vegetables": "果蔬(非发酵)",
          "fish": "鱼(非发酵)", "other": "其他"}

keys = set(rel.columns)
info = md[md.key.isin(keys)].set_index("key")
F = [k for k in info.index[info.fermented == "F"]]
NF = [k for k in info.index[info.fermented == "NF"]]
print("谱中发酵", len(F), "非发酵", len(NF))

res = pd.DataFrame({
    "发酵组平均相对丰度%": rel[F].mean(axis=1) * 100,
    "非发酵组平均相对丰度%": rel[NF].mean(axis=1) * 100,
    "发酵组检出率%": (rel[F] > 0.0001).mean(axis=1) * 100,
    "非发酵组检出率%": (rel[NF] > 0.0001).mean(axis=1) * 100,
})
res["差值"] = res["发酵组平均相对丰度%"] - res["非发酵组平均相对丰度%"]
res.sort_values("差值", ascending=False).round(4).to_csv(f"{OUT}/10_物种谱_发酵vs非发酵差异.csv", encoding="utf-8-sig")

cat_tab = {}
for c, cn in CAT_CN.items():
    cols = [k for k in info.index[info.category == c] if k in keys]
    if not cols:
        continue
    cat_tab[cn] = rel[cols].mean(axis=1) * 100
ct = pd.DataFrame(cat_tab)
ct.round(4).to_csv(f"{OUT}/11_类别水平物种平均丰度.csv", encoding="utf-8-sig")
print("\n各类别 Top5：")
for c in ct.columns:
    top = ct[c].sort_values(ascending=False).head(5)
    print(f"  {c}: " + "; ".join(f"{k} {v:.1f}%" for k, v in top.items()))

div = pd.DataFrame({"Shannon": rel.apply(shannon), "物种数": (rel > 0.0001).sum()}, index=rel.columns)
div = div.join(md.set_index("key")[["category", "fermented"]], how="left")
div["类别"] = div["category"].map(CAT_CN)
div.to_csv(f"{OUT}/13_alpha多样性_每样品.csv", encoding="utf-8-sig")

g = div.groupby("类别").agg(样品数=("Shannon", "size"), Shannon均值=("Shannon", "mean"),
                            Shannon中位数=("Shannon", "median"), 物种数均值=("物种数", "mean")).round(2)
g.to_csv(f"{OUT}/14_alpha多样性_按类别.csv", encoding="utf-8-sig")
print("\n", g.to_string())

from scipy.stats import mannwhitneyu
pairs = {"乳制品": ("dairy", "dairy"), "肉制品": ("meat", "fermented_meat"),
         "鱼": ("fish", "fermented_fish"), "果蔬": ("fruits_and_vegetables", "fermented_fruits_and_vegetables")}
rows = []
for name, (nf, f) in pairs.items():
    a = div[(div.category == nf) & (div.fermented == "NF")]["Shannon"]
    b = div[(div.category == f) & (div.fermented == "F")]["Shannon"]
    if len(a) > 2 and len(b) > 2:
        u, pv = mannwhitneyu(a, b, alternative="two-sided")
        rows.append({"比较": name, "非发酵n": len(a), "发酵n": len(b),
                     "非发酵Shannon均值": round(a.mean(), 2), "发酵Shannon均值": round(b.mean(), 2),
                     "P值": round(pv, 4)})
pair = pd.DataFrame(rows)
pair.to_csv(f"{OUT}/15_同基质发酵vs非发酵多样性.csv", index=False, encoding="utf-8-sig")
print("\n", pair.to_string(index=False))

for nf, f in [("meat", "fermented_meat"), ("fish", "fermented_fish"),
              ("fruits_and_vegetables", "fermented_fruits_and_vegetables"), ("dairy", "dairy")]:
    ka = [k for k in md[(md.category == nf) & (md.fermented == "NF")].key if k in keys]
    kb = [k for k in md[(md.category == f) & (md.fermented == "F")].key if k in keys]
    if not ka or not kb:
        continue
    a, b = rel[ka], rel[kb]
    d = pd.DataFrame({"非发酵均值%": a.mean(1) * 100, "发酵均值%": b.mean(1) * 100,
                      "非发酵检出%": (a > 0.0001).mean(1) * 100, "发酵检出%": (b > 0.0001).mean(1) * 100})
    d["差值"] = d["发酵均值%"] - d["非发酵均值%"]
    d.sort_values("差值", ascending=False).round(3).to_csv(f"{OUT}/16_同基质差异_{nf}.csv", encoding="utf-8-sig")
print("done")
