#!/usr/bin/env python3
"""Figures for mNGS-in-haemato-oncology MA: PRISMA flow, forest plots (sens/spec,
yield), SROC scatter. 300 dpi PNG into ../figures/."""
import csv, json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(BASE, "..", "figures")
os.makedirs(FIG, exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(BASE, "analysis_dataset.csv"), encoding="utf-8")))
by = {r["pmid"]: r for r in rows}
res = json.load(open(os.path.join(BASE, "pooled_results.json")))
short = {"33824437": "Xu et al. 2020 (CSF, allo-HSCT)", "35509305": "Zhao et al. 2021 (BALF, ped allo-HSCT)",
         "35837537": "Xu et al. 2022 (blood, HM-FN)", "40453877": "Wang et al. 2025 (whole blood, FN)",
         "41645073": "Liu et al. 2026 (blood+LRTS, HM)", "41868021": "Chen et al. 2026 (CSF, HM)",
         "42131265": "Kanemasa et al. 2026 (blood, HM)", "37780852": "Hu et al. 2023 (plasma, allo-HSCT)",
         "38371300": "Liu et al. 2024 (plasma, HM)", "38438967": "He et al. 2024 (blood, allo-HSCT FUO)",
         "38590441": "Zheng et al. 2024 (plasma, HSCT IFD)", "40415957": "Hu et al. 2025 (plasma, ped HM)",
         "41327021": "Wang et al. 2024 (blood vs BC)", "42755623": "Wang et al. 2026 (stool, ped allo-HSCT)"}

def logit_prop(tp, den):
    p = (tp + 0.5) / (den + 1.0)
    return 1/(1+math.exp(-math.log(p/(1-p)))), math.log(p/(1-p)), math.sqrt(1/(tp+0.5) + 1/(den-tp+0.5))

def forest(name, pmids, tpk, den_fn, title, fname):
    data = []
    for p in pmids:
        r = by[p]
        est, l, se = logit_prop(int(r[tpk]), int(den_fn(r)))
        lo, hi = 1/(1+math.exp(-(l-1.96*se))), 1/(1+math.exp(-(l+1.96*se)))
        data.append((short.get(p, p), est, lo, hi))
    k = len(data)
    fig, ax = plt.subplots(figsize=(9, 0.6*k + 2.2))
    ys = np.arange(k)[::-1]
    pooled = res[name]
    for (lbl, est, lo, hi), y in zip(data, ys):
        ax.plot([lo*100, hi*100], [y, y], color="#1f4e79", lw=1.4)
        ax.plot(est*100, y, "s", color="#1f4e79", ms=7)
        ax.text(102, y, f"{est*100:.0f}% ({lo*100:.0f}-{hi*100:.0f})", va="center", fontsize=9)
    mu, lo, hi = pooled["mu"], pooled["ci"][0], pooled["ci"][1]
    pm, plo, phi = 1/(1+math.exp(-mu)), 1/(1+math.exp(-lo)), 1/(1+math.exp(-hi))
    ax.axvline(50, color="grey", ls=":", lw=0.8)
    ax.axvspan(plo*100, phi*100, color="#f2c94c", alpha=0.25, zorder=0)
    ax.plot(pm*100, -0.8, "D", color="#c0392b", ms=8)
    ax.text(102, -0.8, f"Pooled {pm*100:.0f}% ({plo*100:.0f}-{phi*100:.0f})", va="center", fontsize=9, color="#c0392b", weight="bold")
    ax.set_yticks(list(ys)+[-0.8]); ax.set_yticklabels([d[0] for d in data]+["Pooled (RE)"], fontsize=9)
    ax.set_xlim(0, 122); ax.set_xlabel("%", fontsize=9); ax.set_title(title, fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, fname), dpi=300); plt.close(fig)
    print("wrote", fname)

A = ["33824437","35509305","35837537","40453877","41645073","41868021","42131265"]
B = ["37780852","38371300","38438967","38590441","40415957","41327021","42755623"]
forest("A_final_dx_sensitivity", A, "TP", lambda r: int(r["TP"])+int(r["FN"]),
       "Sensitivity of mNGS vs final/clinical diagnosis (haemato-oncology)", "forest_A_sensitivity.png")
forest("A_final_dx_specificity", A, "TN", lambda r: int(r["TN"])+int(r["FP"]),
       "Specificity of mNGS vs final/clinical diagnosis (haemato-oncology)", "forest_A_specificity.png")
forest("B_vs_CMT_sensitivity", B, "TP", lambda r: int(r["TP"])+int(r["FN"]),
       "mNGS agreement-with-CMT sensitivity (see notes: incremental detection)", "forest_B_sensitivity.png")
forest("B_vs_CMT_specificity", B, "TN", lambda r: int(r["TN"])+int(r["FP"]),
       "mNGS agreement-with-CMT specificity (positives = additional yield)", "forest_B_specificity.png")

# Yield forest
yrows = json.load(open(os.path.join(BASE, "yield_rows.json")))
fig, ax = plt.subplots(figsize=(9, 0.55*len(yrows)+2.2))
ys = np.arange(len(yrows))[::-1]
for (r, y) in zip(yrows, ys):
    est, l, se = logit_prop(r["pos"], r["n"])
    lo, hi = 1/(1+math.exp(-(l-1.96*se))), 1/(1+math.exp(-(l+1.96*se)))
    ax.plot([lo*100, hi*100], [y, y], color="#1f4e79", lw=1.4); ax.plot(est*100, y, "s", color="#1f4e79", ms=7)
    ax.text(102, y, f"{r['pos']}/{r['n']} = {est*100:.0f}%", va="center", fontsize=9)
    ax.set_yticks(ys); ax.set_yticklabels([short.get(r["pmid"], r["pmid"]) for r in yrows], fontsize=9)
ry = res["yield"]
py, plo, phi = 1/(1+math.exp(-ry["mu"])), 1/(1+math.exp(-ry["ci"][0])), 1/(1+math.exp(-ry["ci"][1]))
ax.axvspan(plo*100, phi*100, color="#f2c94c", alpha=0.25, zorder=0)
ax.plot(py*100, -0.8, "D", color="#c0392b", ms=8)
ax.set_yticks(list(ys)+[-0.8]); ax.set_yticklabels([short.get(r["pmid"], r["pmid"]) for r in yrows]+["Pooled"], fontsize=9)
ax.set_xlim(0, 122); ax.set_title("Diagnostic yield (mNGS positivity) in haemato-oncology", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "forest_yield.png"), dpi=300); plt.close(fig)
print("wrote forest_yield.png")

# SROC scatter (A group): sens vs spec scatter, pooled point
sens_lo = []
for p in A:
    r = by[p]
    se_, _ , _ = logit_prop(int(r["TP"]), int(r["TP"])+int(r["FN"]))
    sp_, _, _ = logit_prop(int(r["TN"]), int(r["TN"])+int(r["FP"]))
    sens_lo.append((se_, sp_, p))
fig, ax = plt.subplots(figsize=(6.4, 6))
ax.scatter([1-x[1] for x in sens_lo], [x[0] for x in sens_lo], s=70, color="#1f4e79")
for s_, sp_, p in sens_lo:
    ax.annotate(short.get(p, p)[:24], (1-sp_, s_), fontsize=7.5, xytext=(4, 3), textcoords="offset points")
muS = 1/(1+math.exp(-res["A_final_dx_sensitivity"]["mu"])); muP = 1/(1+math.exp(-res["A_final_dx_specificity"]["mu"]))
ax.plot(1-muP, muS, "D", color="#c0392b", ms=10, label="Pooled")
ax.set_xlabel("1 - Specificity (false positive rate)"); ax.set_ylabel("Sensitivity (true positive rate)")
ax.set_title("SROC space: mNGS vs final/clinical diagnosis"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "sroc_A.png"), dpi=300); plt.close(fig)
print("wrote sroc_A.png")

# PRISMA flow
fig, ax = plt.subplots(figsize=(9, 7)); ax.axis("off")
def box(x, y, w, h, txt, c="#dbe9f6"):
    ax.add_patch(plt.Rectangle((x, y), w, h, fill=True, color=c, ec="#1f4e79"))
    ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=9.5)
box(2, 78, 42, 10, "Records identified: PubMed 162\n(+ hand-search: pending)")
box(2, 58, 42, 9, "Records after dedup: 162")
box(2, 38, 42, 9, "Title/abstract screening: 162\nExcluded: 111 (56 case reports, 17 reviews/guidelines, 38 out of scope)")
box(2, 18, 42, 9, "Full-text candidates: 51")
box(52, 18, 40, 9, "Excluded at full text: 11\n(no retrievable full text, paywalled)")
box(52, 38, 40, 9, "Full texts retrieved: 40 (OA/PMC)")
box(52, 2, 40, 12, "Included in synthesis: 26\n(14 with 2x2 tables; 12 yield-only)\nExcluded: 5 non-haemato populations,\n9 not-usable (n<5/protocol/no denominators)")
box(2, 2, 42, 9, "Excluded at screening: 1 duplicated\nnone in screened 51")
ax.annotate("", xy=(23, 67), xytext=(23, 76), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(23, 47), xytext=(23, 56), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(23, 27), xytext=(23, 36), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(52, 22.5), xytext=(44, 22.5), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(52, 42.5), xytext=(44, 42.5), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(72, 14), xytext=(72, 16), arrowprops=dict(arrowstyle="->"))
fig.tight_layout(); fig.savefig(os.path.join(FIG, "prisma_flow.png"), dpi=300); plt.close(fig)
print("wrote prisma_flow.png")
