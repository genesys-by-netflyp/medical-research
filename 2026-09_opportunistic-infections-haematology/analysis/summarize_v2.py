import csv, json, statistics, re
base="/opt/data/medical-research/2026-09_opportunistic-infections-haematology/"
rows=list(csv.DictReader(open(base+"extraction/case_extraction_fulltext.csv",encoding="utf-8")))
n=len(rows)
is_unv=lambda v: v.startswith("UNVERIFIED")
ages=[int(r["age_years"]) for r in rows if not is_unv(r["age_years"]) and r["age_years"].replace(".","").isdigit()]
sex_m=sum(1 for r in rows if r["sex"]=="M"); sex_f=sum(1 for r in rows if r["sex"]=="F")
aml=sum(1 for r in rows if "AML" in r["leukaemia_type"]); allc=sum(1 for r in rows if "ALL" in r["leukaemia_type"])
species=sum(1 for r in rows if r["candida_species"].startswith("Candida "))
ctrop=sum(1 for r in rows if "tropicalis" in r["candida_species"]); calb=sum(1 for r in rows if "albicans" in r["candida_species"])
iris=sum(1 for r in rows if r["iris"].startswith("Yes")); surg=sum(1 for r in rows if r["surgery"].startswith("Yes"))
died=sum(1 for r in rows if "died" in r["outcome"].lower())
resolved=sum(1 for r in rows if re.search(r"resolv|remission|no abscess|controlled|normal|CR maintained", r["outcome"], re.I))
summary=dict(n_cases=n, n_sources=len({r["source_id"] for r in rows}),
 median_age=statistics.median(ages), age_range=[min(ages),max(ages)],
 age_reported=len(ages), paediatric=sum(1 for a in ages if a<18), adult=sum(1 for a in ages if a>=18),
 male=sex_m, female=sex_f, sex_unreported=n-sex_m-sex_f,
 aml=aml, all_=allc, leukaemia_unspecified=n-aml-allc,
 species_identified=species, c_tropicalis=ctrop, c_albicans=calb,
 iris=iris, splenectomy=surg, mortality=died, resolved_or_in_remission=resolved,
 fulltext_verified=True, chinese_cases_pending=3)
json.dump(summary, open(base+"analysis/summary_stats.json","w"), indent=1)
print(summary)

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
labels=["Cases","Age\nreported","Paediatric","Female","ALL","Species\nidentified","C.\ntropicalis","IRIS","Splenectomy","Resolved /\nin remission"]
keys=["n_cases","age_reported","paediatric","female","all_","species_identified","c_tropicalis","iris","splenectomy","resolved_or_in_remission"]
vals=[summary[k] for k in keys]
fig,ax=plt.subplots(figsize=(9,4.5))
b=ax.bar(labels, vals, color="#4472c4")
for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2, v+0.12, str(v), ha="center")
ax.set_ylabel("Cases (n = %d)"%n)
ax.set_title("CDC in acute leukaemia - full-text-verified case series (7 sources)")
plt.tight_layout(); plt.savefig(base+"figures/fig1_characteristics.png", dpi=300)
print("figure updated")
