
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
labels=["Cases","ALL","AML/APL","Female","Male","Species\nidentified","C.\ntropicalis","C.\nalbicans","IRIS","Surgery","Resolved /\nremission"]
vals=[10,5,5,7,3,7,4,2,2,4,8]
fig,ax=plt.subplots(figsize=(9.5,4.5))
b=ax.bar(labels, vals, color="#4472c4")
for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2, v+0.12, str(v), ha="center")
ax.set_ylabel("Cases (n = 10)")
ax.set_title("CDC in acute leukaemia - full-text-verified case series\n(7 sources; 10 fully analysed incl. 3 Chinese-language cases)")
plt.tight_layout(); plt.savefig("/opt/data/medical-research/2026-09_opportunistic-infections-haematology/figures/fig1_characteristics.png", dpi=300)
print("fig ok")
