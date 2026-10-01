import csv, json, statistics, re
base="/opt/data/medical-research/2026-09_opportunistic-infections-haematology/"
rows=list(csv.DictReader(open(base+"extraction/case_extraction.csv",encoding="utf-8")))
n=len(rows)
is_unv=lambda v: v.startswith("UNVERIFIED")
known_age=[r for r in rows if not is_unv(r["age_years"]) and r["age_years"] not in ("infant (<2)",) and r["age_years"].replace(".","").replace("y","").isdigit()]
ages=[int(float(r["age_years"])) for r in known_age]
peds=sum(1 for a in ages if a<18)
sex_m=sum(1 for r in rows if r["sex"]=="M"); sex_f=sum(1 for r in rows if r["sex"]=="F")
aml=sum(1 for r in rows if "AML" in r["leukaemia_type"])
allc=sum(1 for r in rows if "ALL" in r["leukaemia_type"] and "AML" not in r["leukaemia_type"])
species_known=sum(1 for r in rows if not is_unv(r["candida_species"]) and not r["candida_species"].startswith("probable") and not r["candida_species"].startswith("culture-proven"))
ctrop=sum(1 for r in rows if "tropicalis" in r["candida_species"])
iris=sum(1 for r in rows if r["iris"].startswith("Yes"))
surg=sum(1 for r in rows if r["surgery"].startswith("Yes"))
died=sum(1 for r in rows if "died" in r["outcome"].lower())
resolved=sum(1 for r in rows if re.search(r"resolv|well|favor|controlled|disease-free|discharged|survived|completed", r["outcome"], re.I))
summary=dict(n_cases=n, n_sources=len({r["source_id"] for r in rows}),
 median_age=statistics.median(ages), age_range=[min(ages),max(ages)],
 paediatric=peds, adult=len(ages)-peds, age_unreported=n-len(ages),
 male=sex_m, female=sex_f, sex_unreported=n-sex_m-sex_f,
 aml=aml, all_=allc, leukaemia_other=n-aml-allc,
 species_reported=species_known, c_tropicalis=ctrop,
 iris=iris, splenectomy=surg, mortality=died, resolved_or_surviving=resolved)
json.dump(summary, open(base+"analysis/summary_stats.json","w"), indent=1)
print(summary)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
labels=["Reported\ncases","Paediatric","Male","AML","Species\nidentified","IRIS","Splenectomy","Resolved /\nalive"]
keys=["n_cases","paediatric","male","aml","species_reported","iris","splenectomy","resolved_or_surviving"]
vals=[summary[k] for k in keys]
fig,ax=plt.subplots(figsize=(8,4.5))
b=ax.bar(labels, vals, color="#4472c4")
for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2, v+0.15, str(v), ha="center")
ax.set_ylabel("Cases (n = %d)"%summary["n_cases"])
ax.set_title("Chronic disseminated candidiasis in acute leukaemia\nliterature-derived case series (abstract-level extraction)")
plt.tight_layout(); plt.savefig(base+"figures/fig1_characteristics.png", dpi=300)
print("figure saved")
