# -*- coding: utf-8 -*-
"""MetaPhlAn4 物种谱分析: 发酵 vs 非发酵, 类别间差异, 真菌组成"""
import pandas as pd, numpy as np, os
OUT = "/home/user/skills/cfmd_deliverables/tables"
p = pd.read_csv('/tmp/cfmd/cFMD_taxonomic_profiles.tsv', sep='\t', low_memory=False, encoding='latin-1')
meta_rows = p['sample'].isin(['macrocategory','category','type','subtype','country','source'])
meta = p[meta_rows].set_index('sample').T
prof = p[~meta_rows].set_index('sample')
prof = prof.apply(pd.to_numeric, errors='coerce').fillna(0.0)
print("profiles", prof.shape)
CAT_CN = {"dairy":"乳制品","fermented_beverages":"发酵饮料","fermented_meat":"发酵肉制品",
 "fermented_grains":"发酵谷物制品","alcohol":"含酒精发酵饮料","fermented_tubers_and_roots":"发酵薯类与根茎",
 "fermented_fruits_and_vegetables":"发酵果蔬","fermented_legumes":"发酵豆类","fermented_seeds":"发酵种子/油料",
 "fermented_fish":"发酵鱼制品","probiotics":"益生菌制剂","meat":"肉制品(非发酵)",
 "fruits_and_vegetables":"果蔬(非发酵)","fish":"鱼(非发酵)","other":"其他"}
# species level rows
sp = prof[prof.index.str.contains(r'\|s__[A-Za-z]', regex=True)]
sp = sp[~sp.index.str.contains(r'\|t__SGB\d+$') | True]
sp.index = [r.split('|s__')[1].split('|')[0] for r in sp.index]
sp = sp.groupby(level=0).sum()
print("species rows", sp.shape)
# 只保留真核+原核可解析名
meta = meta.loc[sp.columns]
meta['category_cn'] = meta['category'].astype(str).map(CAT_CN)
ferm_cols = meta.index[meta['category'].isin([c for c in CAT_CN if c.startswith('fermented') or c in ('dairy','alcohol')])]
# 更准确: 用 metadata 的 fermented 标记
md = pd.read_csv('/tmp/cfmd/cFMD_metadata.tsv', sep='\t', low_memory=False, encoding='latin-1')
md = md.rename(columns={'fermented/non-fermented':'fermented'})
md['key'] = md['dataset_name'] + '__' + md['sample_id']
keymap = dict(zip(md['key'], md['fermented']))
meta['F'] = [keymap.get(k, 'NA') for k in meta.index]
print(meta['F'].value_counts().to_string())
F = meta.index[meta['F']=='F']; NF = meta.index[meta['F']=='NF']
res = pd.DataFrame({
  '发酵组平均相对丰度%': sp[F].mean(axis=1),
  '非发酵组平均相对丰度%': sp[NF].mean(axis=1),
  '发酵组检出率%': (sp[F]>0.01).mean(axis=1)*100,
  '非发酵组检出率%': (sp[NF]>0.01).mean(axis=1)*100,
})
res['差值'] = res['发酵组平均相对丰度%'] - res['非发酵组平均相对丰度%']
res['来源'] = np.select([res.index.str.contains('_')], ['物种'], '属')
res = res.sort_values('差值', ascending=False)
res.round(3).to_csv(f"{OUT}/10_物种谱_发酵vs非发酵差异.csv", encoding='utf-8-sig')
print(res.head(25).round(2).to_string())
print("\n--- 非发酵富集 ---"); print(res.tail(15).round(2).to_string())

# 类别水平 top species
cat_tab = {}
for c, cn in CAT_CN.items():
    cols = meta.index[meta['category']==c]
    if len(cols)==0: continue
    cat_tab[cn] = sp[cols].mean(axis=1)
ct = pd.DataFrame(cat_tab)
ct.to_csv(f"{OUT}/11_类别水平物种平均丰度.csv", encoding='utf-8-sig')
print("\n=== 各类别 Top5 物种 ===")
for c in ct.columns:
    top = ct[c].sort_values(ascending=False).head(5)
    print(c, '|', '; '.join(f"{k} {v:.1f}%" for k,v in top.items()))

# 物种丰富度
rich = (sp[meta.index]>0.01).sum(axis=0)
meta['物种丰富度(>0.01%)'] = rich
meta['category_cn'] = meta['category'].astype(str).map(CAT_CN)
r = meta.groupby('category_cn')['物种丰富度(>0.01%)'].agg(['count','mean','median']).round(1)
r.to_csv(f"{OUT}/12_类别物种丰富度.csv", encoding='utf-8-sig')
print("\n", r.to_string())
print("\nF richness mean", rich[F].mean(), "NF", rich[NF].mean())
