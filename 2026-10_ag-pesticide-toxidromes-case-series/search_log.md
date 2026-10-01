# Search Log — Acute pesticide poisoning in agricultural workers (aggregated case-series synthesis)

| # | Date | Database | Exact search string | Filters | Hits |
|---|------|----------|---------------------|---------|------|
| 1 | 2026-10-01 | Europe PMC | `(pesticide OR herbicide OR fungicide OR paraquat OR glyphosate OR neonicotinoid* OR organophosphate) AND (farmer OR "agricultural worker*" OR applicator) AND (poisoning OR intoxication OR toxidrome) AND PUB_TYPE:"Case Reports"` | Case Reports | 80 |
| 2 | 2026-10-01 | PubMed (E-utilities) | Feasibility probing: `(pesticide[tiab] AND farmer[tiab] AND poisoning[tiab])` | — | 0 (see note A) |
| 3 | 2026-10-01 | Europe PMC | Sample OA check on top 25 records of search #1 | `isOpenAccess`/`inPMC` flags | 25/25 OA |

**Note A:** PubMed's `Case Reports` [pt] tag is unreliable for this literature — queries
combining topic terms with `"case report"[pt]` returned 0 despite relevant cases existing.
The Europe PMC `PUB_TYPE:"Case Reports"` facet is the primary case-type filter for this
project; title/abstract screening will additionally catch untagged case reports/series.

## PRISMA counts (update as pipeline progresses)
- Records identified:
- Duplicates removed:
- Titles/abstracts screened:
- Excluded at screening:
- Full texts assessed:
- Excluded at full text (with reasons):
- Included:

## Planned formal search strings (to execute next)
PubMed / Europe PMC (same string both, subject to field syntax):
```
(pesticide* OR herbicide* OR fungicide* OR insecticide* OR rodenticide* OR fumigant*
 OR organophosphate* OR carbamate* OR pyrethroid* OR paraquat OR glyphosate
 OR neonicotinoid* OR strobilurin* OR indoxacarb OR avermectin* OR abamectin
 OR 2,4-D OR atrazine OR paraoxon)
AND (farmer* OR "agricultural worker*" OR "farm worker*" OR "pesticide applicator"
 OR agriculturalist OR "crop worker*" OR "farm labourer" OR "farm laborer")
AND (poisoning OR intoxication OR toxidrome OR "acute exposure")
```
Filters: English AND non-English (no language filter — non-English sources are in scope);
publication types: Case Reports + title/abstract-level manual catch of untagged case series.
Supplementary: reference-list hand-search of included multi-case series; China National
Knowledge Infrastructure (CNKI) / Ichushi for Chinese/Japanese cases, extracted in-source.
