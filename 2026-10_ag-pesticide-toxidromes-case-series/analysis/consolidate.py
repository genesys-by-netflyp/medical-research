#!/usr/bin/env python3
"""Consolidate per-paper extraction JSONs into one case-level dataset (cases_dataset.csv)
and print descriptive statistics. No pooled/inferential statistics (pre human gate).
Every field value in the dataset is either verbatim-quote-backed or UNVERIFIED at source.
"""
import json, glob, os, csv, re, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(BASE, "extraction")

AGENT_CLASSES = [
    ("organophosphate", r"organophosph|chlorpyrifos|malathion|diazinon|methamidophos|monocrotophos|parathion|dichlorvos|acephate|profenofos|paraoxon|diclorvos"),
    ("pyrethroid", r"pyrethroid|cypermethrin|deltamethrin|permethrin|lambda-cyhalothrin|cyhalothrin"),
    ("neonicotinoid", r"neonicotinoid|imidacloprid|thiamethoxam|imidacloprid"),
    ("bipyridyl herbicide (paraquat/diquat)", r"paraquat|diquat|gramashru"),
    ("glyphosate/other herbicide", r"glyphosate|atrazine|2,4-d|2,4-dichlorophenoxy|dicamba|bispyribac|pretilachlor|butachlor"),
    ("avermectin/emamectin", r"avermectin|abamectin|emamectin|ivermectin"),
    ("indoxacarb", r"indoxacarb"),
    ("fipronil/phenylpyrazole", r"fipronil"),
    ("amitraz (formamidine)", r"amitraz"),
    ("fumigant (aluminium phosphide/chloropicrin)", r"phosphide|phosphine|chloropicrin"),
    ("rodenticide (anticoagulant)", r"brodifacoum|bromadiolone|superwarfarin|warfarin"),
    ("copper sulfate", r"copper (sulfate|sulphate)"),
    ("carbamate", r"carbamat|carbofuran|aldicarb"),
    ("mixed/other/unclassified", r"."),
]

def classify(agent):
    a = (agent or "").lower()
    for name, pat in AGENT_CLASSES:
        if re.search(pat, a):
            return name
    return "mixed/other/unclassified"

def first_num(s):
    m = re.search(r"(\d{1,3})", str(s))
    return int(m.group(1)) if m else None

rows = []
for f in sorted(glob.glob(os.path.join(EX, "PMC*.json"))):
    d = json.load(open(f))
    if not d.get("suitable"):
        continue
    for c in d.get("cases", []):
        agent_class = classify(c.get("agent", ""))
        outcome = (c.get("outcome") or "").lower()
        if re.search(r"\bdied|death|fatal|mortality|dema?se\b|expired", outcome):
            outcome_cat = "died"
        elif re.search(r"recover|discharg|improv|surviv|resol|improved", outcome):
            outcome_cat = "survived/recovered"
        elif outcome.strip():
            outcome_cat = "other/unstated"
        else:
            outcome_cat = "other/unstated"
        rows.append({
            "case_id": c.get("case_id", ""),
            "pmcid": d["pmcid"],
            "age_raw": c.get("age", "UNVERIFIED"),
            "age_num": first_num(c.get("age", "")) or "",
            "sex_raw": c.get("sex", "UNVERIFIED"),
            "agent_class": agent_class,
            "agent": c.get("agent", ""),
            "exposure_context": c.get("exposure_context", "unclear"),
            "route": c.get("route", "UNVERIFIED"),
            "time_to_care": c.get("time_to_care", "UNVERIFIED"),
            "n_symptoms": len(c.get("symptoms", [])),
            "icu": c.get("icu_admission", "UNVERIFIED"),
            "outcome_cat": outcome_cat,
            "outcome_raw": (c.get("outcome") or "")[:200],
        })

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases_dataset.csv")
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

from collections import Counter
n = len(rows)
print(f"TOTAL CASES: {n} from {len(set(r['pmcid'] for r in rows))} papers")
print("\nAgent class:"); [print(f"  {k}: {v}") for k, v in Counter(r['agent_class'] for r in rows).most_common()]
print("\nExposure context:"); [print(f"  {k}: {v}") for k, v in Counter(r['exposure_context'] for r in rows).most_common()]
print("\nOutcome category:"); [print(f"  {k}: {v}") for k, v in Counter(r['outcome_cat'] for r in rows).most_common()]
print("\nSex:"); [print(f"  {k}: {v}") for k, v in Counter(r['sex_raw'].lower() for r in rows).most_common()]
ages = [r["age_num"] for r in rows if r["age_num"] != ""]
print(f"\nAge (n={len(ages)} numeric): min {min(ages)}, max {max(ages)}, median {sorted(ages)[len(ages)//2]}")
print("\nRoute:"); [print(f"  {k}: {v}") for k, v in Counter(r['route'].lower()[:40] for r in rows).most_common(8)]
icu = Counter(r["icu"].lower()[:30] for r in rows)
print("\nICU (raw):"); [print(f"  {k}: {v}") for k, v in icu.most_common(6)]
print(f"\nDataset written: {out}")
