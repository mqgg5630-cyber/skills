# -*- coding: utf-8 -*-
"""alpha 多样性 + 同类基质内 发酵/非发酵 配对比较"""
import pandas as pd, numpy as np, json
OUT="/home/user/skills/cfmd_deliverables/tables"
p = pd.read_csv('/tmp/cfmd/cFMD_taxonomic_profiles.tsv', sep='\t', low_memory=False, encoding='latin-1')
meta_rows = p['sample'].isin(['macrocategory','category','type','subtype','country','source'])
meta = p[meta_rows].set_index('sample').T
prof = p[~meta_rows].set_index('sample').apply(pd.to_numeric, errors='coerce').fillna(0.)
sp = prof[prof.index.str.contains(r'\|s__[A-Za-z]', regex=True)]
sp.index = [r.split('|s__')[1].split('|')[0] for r in sp.index]
sp = sp.groupby(level=0).sum()
sp = sp.loc[:, sp.sum(axis=0) > 0]
rel = sp.div(sp.sum(axis=0), axis=1).fillna(0)
def shannon(x):
    x = x[x > 0]
    return float(-(x*np.log(x)).sum())
div = pd.DataFrame({
  'Shannon': rel.apply(shannon),
  '物种数': (rel > 0.0001).sum(),
}, index=rel.columns)
md = pd.read_csv('/tmp/cfmd/cFMD_metadata.tsv', sep='\t', low_memory=False, encoding='latin-1')
md = md.rename(columns={'fermented/non-fermented':'fermented'}); md['key']=md['dataset_name']+'__'+md['sample_id']
CAT_CN={"dairy":"乳制品","fermented_beverages":"发酵饮料","fermented_meat":"发酵肉制品","fermented_grains":"发酵谷物制品",
"alcohol":"含酒精发酵饮料","fermented_tubers_and_roots":"发酵薯类与根茎","fermented_fruits_and_vegetables":"发酵果蔬",
"fermented_legumes":"发酵豆类","fermented_seeds":"发酵种子/油料","fermented_fish":"发酵鱼制品","probiotics":"益生菌制剂",
"meat":"肉制品(非发酵)","fruits_and_vegetables":"果蔬(非发酵)","fish":"鱼(非发酵)","other":"其他"}
info = md.set_index('key')[['category','fermented']]
div = div.join(info, how='left')
div['类别']=div['category'].map(CAT_CN)
div.to_csv(f"{OUT}/13_alpha多样性_每样品.csv", encoding='utf-8-sig')
g = div.groupby('类别').agg(样品数=('Shannon','size'), Shannon均值=('Shannon','mean'),
                             Shannon中位数=('Shannon','median'), 物种数均值=('物种数','mean')).round(2)
g.to_csv(f"{OUT}/14_alpha多样性_按类别.csv", encoding='utf-8-sig')
print(g.to_string())

# 配对: 同一大类内 发酵 vs 非发酵
pairs = {'dairy':('dairy','dairy'),'meat':('meat','fermented_meat'),
         'fish':('fish','fermented_fish'),'fv':('fruits_and_vegetables','fermented_fruits_and_vegetables')}
rows=[]
for k,(nf,f) in pairs.items():
    a=div[(div.category==nf)&(div.fermented=='NF')]; b=div[(div.category==f)&(div.fermented=='F')]
    from scipy.stats import mannwhitneyu
    if len(a)>2 and len(b)>2:
        u,pv = mannwhitneyu(a.Shannon,b.Shannon,alternative='two-sided')
        rows.append({'比较':f'{nf} vs {f}','非发酵n':len(a),'发酵n':len(b),
                     '非发酵Shannon均值':round(a.Shannon.mean(),2),'发酵Shannon均值':round(b.Shannon.mean(),2),
                     'P值':round(pv,4)})
pair=pd.DataFrame(rows); pair.to_csv(f"{OUT}/15_同基质发酵vs非发酵多样性.csv", index=False, encoding='utf-8-sig')
print(pair.to_string(index=False))

# 物种谱: 同一大类内差异
for nf,f in [('meat','fermented_meat'),('fish','fermented_fish'),('fruits_and_vegetables','fermented_fruits_and_vegetables')]:
    ka=[k for k in md[(md.category==nf)&(md.fermented=='NF')].key if k in rel.columns]
    kb=[k for k in md[(md.category==f)&(md.fermented=='F')].key if k in rel.columns]
    a=rel.loc[:, ka]; b=rel.loc[:, kb]
    d=pd.DataFrame({'非发酵均值%':a.mean(1)*100,'发酵均值%':b.mean(1)*100,
                    '非发酵检出%':(a>0.0001).mean(1)*100,'发酵检出%':(b>0.0001).mean(1)*100})
    d['差值']=d['发酵均值%']-d['非发酵均值%']
    d.sort_values('差值',ascending=False).round(3).to_csv(f"{OUT}/16_同基质差异_{nf}.csv", encoding='utf-8-sig')
print("done")
