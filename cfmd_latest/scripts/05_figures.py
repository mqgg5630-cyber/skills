# -*- coding: utf-8 -*-
"""生成报告插图"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mtick

FONT = "/tmp/.venv/lib/python3.11/site-packages/mplfonts/fonts/NotoSansCJKsc-Regular.otf"
fm.fontManager.addfont(FONT)
CN = fm.FontProperties(fname=FONT).get_name()
plt.rcParams["font.family"] = CN
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 200
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["axes.edgecolor"] = "#4a4a4a"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["font.size"] = 9

OUT = "/home/user/skills/cfmd_latest/figures"
os.makedirs(OUT, exist_ok=True)
T = "/home/user/skills/cfmd_latest/tables"

BLUE = "#2E5E8E"; ORANGE = "#C9762F"; GREEN = "#4F7B52"; GREY = "#9AA0A6"; RED = "#A63A3A"

# ---------------------------------------------------------------- 图1 类别 MAG 数与质量
s = pd.read_csv(f"{T}/02_按发酵种类汇总.csv")
s = s[s["发酵类别"] != "合计"].copy()
s = s.sort_values("MAG总数", ascending=True).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(6.6, 3.6))
y = np.arange(len(s))
ax.barh(y, s["高质量MAG(HQ)"], color=BLUE, label="高质量 MAG (完整度≥90%，污染<5%)", height=0.62)
ax.barh(y, s["中等质量MAG(MQ)"], left=s["高质量MAG(HQ)"], color="#8FB3D3",
        label="中等质量 MAG (50%–90%)", height=0.62)
ax.set_yticks(y); ax.set_yticklabels(s["发酵类别"])
for i, (a, b) in enumerate(zip(s["高质量MAG(HQ)"], s["中等质量MAG(MQ)"])):
    ax.text(a + b + 40, i, f"{a+b:,}", va="center", fontsize=8, color="#333333")
ax.set_xlabel("MAG 数量")
ax.set_xlim(0, s["MAG总数"].max() * 1.14)
ax.legend(frameon=False, fontsize=8, loc="lower right")
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
ax.set_title("图1  各发酵食品类别重建的 MAG 数量与质量分布", fontsize=10, pad=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig1_类别MAG数量.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- 图2 优势属热图
g = pd.read_csv(f"{T}/03_属水平MAG数量矩阵.csv", index_col=0)
g = g.loc[g.sum(axis=1).sort_values(ascending=False).index[:22]]
cols = [c for c in ["乳制品", "发酵饮料", "含酒精发酵饮料", "发酵肉制品", "发酵谷物制品",
                    "发酵薯类与根茎", "发酵果蔬", "发酵豆类", "发酵种子/油料", "发酵鱼制品"] if c in g.columns]
g = g[cols]
glog = np.log10(g + 1)
cmap = LinearSegmentedColormap.from_list("cf", ["#FFFFFF", "#D6E4F0", "#7FA8C9", "#2E5E8E", "#16324F"])
fig, ax = plt.subplots(figsize=(6.4, 5.4))
im = ax.imshow(glog.values, aspect="auto", cmap=cmap)
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=42, ha="right", fontsize=8)
ax.set_yticks(range(len(g))); ax.set_yticklabels([i if len(i) < 26 else i[:24] + "…" for i in g.index],
                                                 fontsize=8, style="italic")
for i in range(len(g)):
    for j in range(len(cols)):
        v = g.values[i, j]
        if v >= 1:
            ax.text(j, i, f"{v:,.0f}", ha="center", va="center", fontsize=6.2,
                    color="white" if glog.values[i, j] > 1.9 else "#333333")
ax.set_xticks(np.arange(-.5, len(cols), 1), minor=True)
ax.set_yticks(np.arange(-.5, len(g), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.8)
ax.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ax=ax, shrink=0.62, pad=0.02)
cb.set_label("log10(MAG 数 + 1)", fontsize=8)
cb.ax.tick_params(labelsize=7)
ax.set_title("图2  发酵食品中优势菌属的 MAG 数量分布", fontsize=10, pad=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_优势属热图.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- 图3 益生菌物种热图
pg = pd.read_csv(f"{T}/07_益生菌物种x发酵类别矩阵.csv", index_col=0)
pg = pg.loc[pg.sum(axis=1).sort_values(ascending=False).index[:20]]
pg = pg[[c for c in cols if c in pg.columns]]
cmap2 = LinearSegmentedColormap.from_list("cf2", ["#FFFFFF", "#F2E2D0", "#DCA46B", "#C9762F", "#7C4515"])
fig, ax = plt.subplots(figsize=(6.4, 5.0))
im = ax.imshow(np.log10(pg.values + 1), aspect="auto", cmap=cmap2)
ax.set_xticks(range(pg.shape[1])); ax.set_xticklabels(pg.columns, rotation=42, ha="right", fontsize=8)
ax.set_yticks(range(len(pg))); ax.set_yticklabels(pg.index, fontsize=7.6, style="italic")
for i in range(pg.shape[0]):
    for j in range(pg.shape[1]):
        v = pg.values[i, j]
        if v >= 1:
            ax.text(j, i, f"{v:,}", ha="center", va="center", fontsize=6.4,
                    color="white" if np.log10(v + 1) > 1.9 else "#333333")
ax.set_xticks(np.arange(-.5, pg.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-.5, len(pg), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.8); ax.tick_params(which="minor", length=0)
ax.set_title("图3  核心益生菌物种在各类发酵食品中的 MAG 数量", fontsize=10, pad=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig3_益生菌物种热图.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- 图4 alpha 多样性
d = pd.read_csv(f"{T}/13_alpha多样性_每样品.csv")
order = ["乳制品", "发酵饮料", "含酒精发酵饮料", "发酵肉制品", "发酵谷物制品", "发酵薯类与根茎",
         "发酵果蔬", "发酵豆类", "发酵种子/油料", "发酵鱼制品", "益生菌制剂",
         "肉制品(非发酵)", "果蔬(非发酵)", "鱼(非发酵)"]
order = [o for o in order if o in d["类别"].unique()]
data = [d[d["类别"] == o]["Shannon"].dropna().values for o in order]
fig, ax = plt.subplots(figsize=(6.8, 3.3))
bp = ax.boxplot(data, patch_artist=True, widths=0.6, showfliers=False,
                medianprops=dict(color="#333333", linewidth=1))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor("#8FB3D3" if i < 11 else "#D9C7B4")
    patch.set_edgecolor("#4a4a4a"); patch.set_linewidth(0.6)
for i, o in enumerate(order):
    v = d[d["类别"] == o]["Shannon"].dropna()
    ax.scatter(np.random.normal(i + 1, 0.06, len(v)), v, s=2.5, color=BLUE if i < 11 else ORANGE, alpha=0.45, zorder=3)
ax.set_xticks(range(1, len(order) + 1)); ax.set_xticklabels(order, rotation=42, ha="right", fontsize=7.6)
ax.set_ylabel("Shannon 指数")
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
ax.set_title("图4  各食品类别的物种水平 alpha 多样性", fontsize=10, pad=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig4_alpha多样性.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- 图5 真核组成
e = pd.read_csv(f"{T}/08_发酵食品真核MAG表.csv")
top = e["属"].value_counts().head(12)
cats = ["乳制品", "发酵饮料", "含酒精发酵饮料", "发酵肉制品", "发酵谷物制品", "发酵果蔬", "发酵薯类与根茎", "发酵豆类"]
tab = pd.crosstab(e["属"], e["发酵类别中文"]).reindex(top.index)[[c for c in cats if c in e["发酵类别中文"].unique()]]
fig, ax = plt.subplots(figsize=(6.2, 3.4))
bottom = np.zeros(len(tab))
pal = ["#2E5E8E", "#4F7B52", "#C9762F", "#8E6C9A", "#A63A3A", "#6B8E9E", "#C0A15A",
       "#7C8B57", "#B57C8A", "#5C7A99", "#9AA0A6", "#4A4A4A"]
for i, c in enumerate(tab.columns):
    ax.bar(range(len(tab)), tab[c], bottom=bottom, label=c, color=pal[i % len(pal)], width=0.68)
    bottom += tab[c].values
ax.set_xticks(range(len(tab))); ax.set_xticklabels(tab.index, rotation=38, ha="right", fontsize=8, style="italic")
ax.set_ylabel("MAG 数量", labelpad=2)
ax.legend(frameon=False, fontsize=7, ncol=2, loc="upper right", bbox_to_anchor=(1.0, 1.02))
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
ax.set_title("图5  发酵食品真核 MAG 的属组成", fontsize=10, pad=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_真核组成.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- 图6 SGB 新颖性
sg = pd.read_csv(f"{T}/04_SGB水平汇总_含发酵类别.csv")
lab = ["已知种(kSGB)", "未知种(uSGB)", "食品中新种(ufSGB)"]
colr = {"已知种(kSGB)": BLUE, "未知种(uSGB)": "#8FB3D3", "食品中新种(ufSGB)": ORANGE}
cnt = sg["SGB类型"].value_counts().reindex(lab)
fig, ax = plt.subplots(figsize=(3.6, 3.0))
w, _, at = ax.pie(cnt.values, colors=[colr[l] for l in lab], startangle=90,
                  wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.4),
                  autopct=lambda p: f"{p:.1f}%", pctdistance=0.79,
                  textprops=dict(fontsize=7.4, color="white"))
ax.text(0, 0.08, f"{cnt.sum():,}", ha="center", va="center", fontsize=15, color="#2b2b2b")
ax.text(0, -0.16, "SGB 总数", ha="center", va="center", fontsize=8, color="#555555")
ax.legend([f"{l} ({cnt[l]})" for l in lab], frameon=False, fontsize=7.4,
          loc="upper center", bbox_to_anchor=(0.5, 0.06))
ax.set_title("图6  食品 MAG 所属 SGB 的新颖性构成", fontsize=9.5, pad=6)
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_SGB新颖性.png", bbox_inches="tight"); plt.close(fig)
print("figures done", os.listdir(OUT))
