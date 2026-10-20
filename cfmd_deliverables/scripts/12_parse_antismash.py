# -*- coding: utf-8 -*-
"""汇总 antiSMASH 结果：BGC 明细表、类群统计、与发酵类别和益生菌归属的交叉表

用法:
    python 12_parse_antismash.py [antiSMASH输出目录] [MAG主表] [输出目录]
默认:
    ../antismash/results  ../tables/00_MAG主表_全部.csv  ../tables
输出:
    20_BGC明细表.csv
    21_BGC类型统计_按属.csv
    22_BGC类型x发酵类别.csv
    23_BGC类型x益生菌归属.csv
"""
import os, sys, json, glob, re
import pandas as pd

RES = sys.argv[1] if len(sys.argv) > 1 else "../antismash/results"
MASTER = sys.argv[2] if len(sys.argv) > 2 else "../tables/00_MAG主表_全部.csv"
OUT = sys.argv[3] if len(sys.argv) > 3 else "../tables"
os.makedirs(OUT, exist_ok=True)

records = []
for path in glob.glob(os.path.join(RES, "**", "*.json"), recursive=True):
    if os.path.basename(path).startswith(("cluster", "known")):
        continue
    try:
        with open(path) as fh:
            data = json.load(fh)
    except Exception as e:
        print("skip", path, e)
        continue
    mag = os.path.basename(path).rsplit(".", 1)[0]
    for rec in data.get("records", []):
        acc = rec.get("accession") or rec.get("id") or ""
        for feat in rec.get("features", []):
            if feat.get("type") != "region":
                continue
            q = feat.get("qualifiers", {})
            def first(k, default=""):
                v = q.get(k, default)
                return v[0] if isinstance(v, list) and v else (v if isinstance(v, str) else default)
            loc = feat.get("location", "")
            m = re.match(r"\[<?(\d+):>?(\d+)\]", loc)
            start, end = (int(m.group(1)), int(m.group(2))) if m else (None, None)
            products = q.get("product", [])
            if isinstance(products, str):
                products = [products]
            sim = q.get("similarity", [])
            if isinstance(sim, str):
                sim = [sim]
            rec_name = q.get("knowncluster", []) or q.get("cluster_number", [])
            if isinstance(rec_name, str):
                rec_name = [rec_name]
            records.append({
                "MAG_id": mag,
                "contig": acc,
                "region": first("region_number", ""),
                "start": start,
                "end": end,
                "长度_bp": (end - start) if (start and end) else None,
                "簇类型": ";".join(products),
                "相似度": ";".join(sim),
                "已知簇": ";".join(rec_name),
                "部分簇": first("partial", "no"),
                "来源": os.path.basename(os.path.dirname(path)),
            })

bgc = pd.DataFrame(records)
if bgc.empty:
    print("未解析到 BGC，请检查 antiSMASH 输出目录")
    sys.exit(0)

# 多类型簇拆分为长表，便于统计
bgc["主类型"] = bgc["簇类型"].str.split(";").str[0]
bgc.to_csv(f"{OUT}/20_BGC明细表.csv", index=False, encoding="utf-8-sig")

meta = pd.read_csv(MASTER, encoding="utf-8-sig", low_memory=False)
keep = ["MAG_id", "属", "物种", "发酵类别中文", "益生菌归属", "SGB_id", "质量等级"]
m = bgc.merge(meta[[c for c in keep if c in meta.columns]], on="MAG_id", how="left")

t1 = (m.groupby(["属", "主类型"]).size().reset_index(name="BGC数")
        .sort_values(["属", "BGC数"], ascending=[True, False]))
t1.to_csv(f"{OUT}/21_BGC类型统计_按属.csv", index=False, encoding="utf-8-sig")

t2 = (m.groupby(["发酵类别中文", "主类型"]).size().unstack(fill_value=0)
        .sort_values(by=list(m["主类型"].unique())[:1], ascending=False))
t2.to_csv(f"{OUT}/22_BGC类型x发酵类别.csv", encoding="utf-8-sig")

t3 = (m.groupby(["益生菌归属", "主类型"]).size().unstack(fill_value=0))
t3.to_csv(f"{OUT}/23_BGC类型x益生菌归属.csv", encoding="utf-8-sig")

print(f"解析 {len(bgc)} 个 BGC，来自 {bgc['MAG_id'].nunique()} 个基因组")
print(t1.head(20).to_string(index=False))
