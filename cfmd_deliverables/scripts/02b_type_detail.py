# -*- coding: utf-8 -*-
"""发酵食品在 type 层级的明细汇总"""
import pandas as pd
T="/home/user/skills/cfmd_deliverables/tables"
m=pd.read_pickle('/tmp/m_master.pkl'); f=m[m.fermented=='F']
g=f.groupby(['category','type'])
rows=[]
for (cat,typ),d in g:
    prok=d[d.superkingdom!='Eukaryota']
    top=prok['物种'].value_counts().head(3)
    rows.append({'发酵类别':d['发酵类别中文'].iloc[0],'食品类型':d['食品类型中文'].iloc[0],'type_code':typ,
                 '样品数':d[['dataset_id','sample_id']].drop_duplicates().shape[0],'数据集数':d.dataset_id.nunique(),
                 '国家数':d.country.nunique(),'MAG数':len(d),'HQ数':(d['质量等级']=='高质量(HQ)').sum(),
                 'SGB数':d.SGB_id.nunique(),'属数':prok['属'].nunique(),
                 '优势种Top3':' / '.join(f"{k}({v})" for k,v in top.items()),
                 '该类型代表MAG':d.sort_values('completeness',ascending=False).MAG_id.iloc[0]})
t=pd.DataFrame(rows).sort_values(['MAG数'],ascending=False)
t.to_csv(f"{T}/20_发酵类型明细_按type.csv",index=False,encoding='utf-8-sig')
print(len(t),'types'); print(t.head(20).to_string(index=False))
