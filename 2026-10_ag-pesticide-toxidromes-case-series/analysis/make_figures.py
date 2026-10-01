#!/usr/bin/env python3
"""Generate figures for the ag-pesticide toxidrome case series (descriptive only)."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "figures"); os.makedirs(FIG, exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases_dataset.csv"))))

# Fig 1: PRISMA-style flow
fig, ax = plt.subplots(figsize=(8, 6)); ax.axis("off")
boxes = [
    (0.5, 0.92, "Records identified via Europe PMC search\n(n = 186)"),
    (0.5, 0.72, "Screened on title/abstract (n = 186)"),
    (0.28, 0.52, "Excluded (n = 93):\nanimal studies, conference abstracts,\nreviews without per-case data,\nnon-pesticide toxicology, topic drift"),
    (0.72, 0.52, "Full texts sought (n = 93)"),
    (0.72, 0.32, "Full texts retrieved (n = 88)"),
    (0.72, 0.12, "Suitable case-level sources (n = 73);\n15 excluded: aggregate-only cohorts,\nreviews, chronic/non-pesticide"),
    (0.28, 0.12, "Cases extracted (n = 102)"),
]
for x, y, t in boxes:
    ax.text(x, y, t, ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4", fc="#eef2f7", ec="#1f4e79"))
arrows = [((0.5,0.88),(0.5,0.76)), ((0.5,0.68),(0.34,0.57)), ((0.5,0.68),(0.66,0.57)),
          ((0.72,0.47),(0.72,0.37)), ((0.72,0.27),(0.72,0.18)), ((0.62,0.12),(0.38,0.12))]
for (x1,y1),(x2,y2) in arrows:
    ax.annotate("", xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle="->", color="#8a2b2b"))
ax.set_xlim(0,1); ax.set_ylim(0,1)
fig.savefig(os.path.join(FIG, "prisma_flow.png"), dpi=150, bbox_inches="tight"); plt.close(fig)

# Fig 2: agent class by outcome (stacked horizontal bar)
ct = Counter((r["agent_class"], r["outcome_cat"]) for r in rows)
classes = sorted(set(r["agent_class"] for r in rows), key=lambda c: -ct[(c,"died")]-ct[(c,"survived/recovered")])
died = [ct[(c,"died")] for c in classes]
surv = [ct[(c,"survived/recovered")] for c in classes]
other = [ct[(c,"other/unstated")] for c in classes]
fig, ax = plt.subplots(figsize=(9, 6))
y = range(len(classes))
ax.barh(y, surv, color="#4a7c59", label="survived/recovered")
ax.barh(y, died, left=surv, color="#8a2b2b", label="died")
ax.barh(y, other, left=[a+b for a,b in zip(surv,died)], color="#b0b0b0", label="other/unstated")
ax.set_yticks(list(y)); ax.set_yticklabels([c.replace(" (", "\n(") for c in classes], fontsize=8)
ax.invert_yaxis(); ax.set_xlabel("Number of published cases")
ax.legend(); ax.set_title("Published pesticide-poisoning cases by agent class and outcome (n = 102)")
fig.savefig(os.path.join(FIG, "agent_outcome.png"), dpi=150, bbox_inches="tight"); plt.close(fig)

# Fig 3: exposure context pie
cc = Counter(r["exposure_context"] for r in rows)
fig, ax = plt.subplots(figsize=(5.5, 5.5))
ax.pie(cc.values(), labels=cc.keys(), autopct=lambda p: f"{int(round(p*sum(cc.values())/100))}",
       colors=["#c9d6e5", "#e6d3b3", "#d6c9e5"], startangle=90)
ax.set_title("Exposure context (n = 102); 'unclear' = not stated in source")
fig.savefig(os.path.join(FIG, "exposure_context.png"), dpi=150, bbox_inches="tight"); plt.close(fig)
print("figures written:", os.listdir(FIG))
