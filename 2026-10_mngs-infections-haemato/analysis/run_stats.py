#!/usr/bin/env python3
"""Pooled statistics for diagnostic-accuracy MA of mNGS in haemato-oncology.
Univariate random-effects (DerSimonian-Laird) on logit-transformed
sensitivity/specificity/diagnostic-yield proportions + I2, Egger/funnel data.
Every input traces to analysis/analysis_dataset.csv (itself traceable to
extraction/<PMID>.json with verbatim quotes)."""
import csv, json, math, os
import numpy as np
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, "analysis_dataset.csv"), encoding="utf-8")))

def logit_prop(tp_or_pos, denom):
    p = (tp_or_pos + 0.5) / (denom + 1.0)  # continuity correction
    l = math.log(p / (1 - p))
    se = math.sqrt(1/(tp_or_pos+0.5) + 1/(denom-tp_or_pos+0.5))
    return l, se

def inv_logit(l): return 1/(1+math.exp(-l))

def dl_pool(vals):
    """DerSimonian-Laird random effects on (effect, se) pairs; returns pooled eff, se, I2, Q, p, k"""
    eff = np.array([e for e, s in vals]); se = np.array([s for e, s in vals])
    k = len(eff)
    w = 1 / se**2
    mu = np.sum(w * eff) / np.sum(w)
    Q = np.sum(w * (eff - mu) ** 2)
    df = k - 1
    C = np.sum(w) - np.sum(w**2) / np.sum(w)
    tau2 = max(0.0, (Q - df) / C if C > 0 else 0.0)
    w2 = 1 / (se**2 + tau2)
    mu2 = np.sum(w2 * eff) / np.sum(w2)
    se2 = math.sqrt(1 / np.sum(w2))
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    pQ = 1 - stats.chi2.cdf(Q, df) if df > 0 else 1.0
    z = mu2 / se2; pz = 2 * (1 - stats.norm.cdf(abs(z)))
    return dict(k=k, mu=mu2, se=se2, I2=I2, Q=Q, pQ=pQ, z=z, p=pz, tau2=tau2,
                ci=(mu2 - 1.96*se2, mu2 + 1.96*se2), effs=eff, ses=se)

def report(name, vals, unit=""):
    r = dl_pool(vals)
    print(f"\n== {name} ==")
    print(f"  k={r['k']}  pooled={inv_logit(r['mu'])*100:.1f}% ({inv_logit(r['ci'][0])*100:.1f}-{inv_logit(r['ci'][1])*100:.1f})  "
          f"I2={r['I2']:.0f}%  Q={r['Q']:.1f} p={r['pQ']:.3g}  z={r['z']:.2f} p={r['p']:.3g}")
    return r

groups = {
    "A_final_dx": ["33824437","35509305","35837537","40453877","41645073","41868021","42131265"],
    "B_vs_CMT":   ["37780852","38371300","38438967","38590441","40415957","41327021","42755623"],
}
yields = ["33824437","34835435","35837477","35837537","36211959","38057898","38725449",
          "40415957","40453877","41189926","41645073","42131265","42359352","38567023"]

by = {r["pmid"]: r for r in rows}
results = {}
for gname, pmids in groups.items():
    for metric, (tpk, den_fn) in {"sensitivity": ("TP", lambda r: int(r["TP"]) + int(r["FN"])), "specificity": ("TN", lambda r: int(r["TN"]) + int(r["FP"]))}.items():
        vals = []
        for p in pmids:
            r = by[p]
            tp = int(r[tpk]); den = int(den_fn(r))
            vals.append(logit_prop(tp, den))
        results[f"{gname}_{metric}"] = report(f"{gname} {metric} vs {by[pmids[0]]['comparator'][:30]}...", vals)

# Diagnostic yield (positivity rate), single-arm
def _toint(v):
    s = str(v).split()[0] if str(v).strip() else ""
    return int(s) if s.isdigit() else None

    # (int-safe accessor)

yvals = []
yield_rows = []
for p in yields:
    r = by[p]
    yt, yp = _toint(r["yield_tests"]), _toint(r["yield_pos"])
    # fall back to 2x2 numerator sums where yield fields are junk
    if yp is None or yt is None:
        if str(r["TP"]).strip():
            yt = int(r["TP"]) + int(r["FP"]) + int(r["FN"]) + int(r["TN"]); yp = int(r["TP"]) + int(r["FP"])
        else:
            continue
    else:
        yt = int(str(yt).split()[0]); yp = int(str(yp).split()[0])
    if not (yt and yp is not None and yt >= yp >= 0): continue
    yvals.append(logit_prop(yp, yt))
    yield_rows.append(dict(pmid=p, n=yt, pos=yp))
ry = report("Diagnostic yield (mNGS positivity rate)", yvals)
results["yield"] = {k: v for k, v in ry.items() if k not in ("effs", "ses")}
json.dump(yield_rows, open(os.path.join(BASE, "yield_rows.json"), "w"), indent=1)

# leave-one-out sensitivity for the primary group
print("\n== Leave-one-out (A_final_dx sensitivity) ==")
g = groups["A_final_dx"]
for p in g:
    sub = [logit_prop(int(by[x]["TP"]), int(by[x]["TP"]) + int(by[x]["FN"])) for x in g if x != p]
    r = dl_pool(sub)
    print(f"  without {p}: pooled sens={inv_logit(r['mu'])*100:.1f}% I2={r['I2']:.0f}%")

json.dump({k: {kk: (float(vv) if not isinstance(vv, tuple) else [float(vv[0]), float(vv[1])])
               for kk, vv in v.items() if kk not in ("effs", "ses")}
           for k, v in results.items()},
          open(os.path.join(BASE, "pooled_results.json"), "w"), indent=1)
print("\nsaved pooled_results.json")
