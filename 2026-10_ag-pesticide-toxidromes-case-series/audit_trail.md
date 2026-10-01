# Audit Trail — <project title>

Chronological, append-only log of every automated action. The agent appends; never rewrites history. This file is published to GitHub with the project.

| # | Timestamp (UTC) | Step | Action | Input/queries | Output artifact | Decisions & rationale |
|---|-----------------|------|--------|---------------|-----------------|----------------------|
| 1 | 2026-10-01T09:19Z | Topic viability | Parallel feasibility screening of 8 candidate topics (delegated subagents) | 8 topic briefs | (discarded) | Subagent results were corrupted/off-topic; ALL discarded as unreliable. No data from them used. |
| 2 | 2026-10-01T09:30–09:45Z | Topic viability | Full-access gate re-run directly by primary agent: PubMed E-utilities esearch/esummary + Europe PMC per-record OA flags | Exact queries in em_occupational_health_topics.md + search_log.md rows 1–3 | em_occupational_health_topics.md | 2 topics passed (E1 ag-pesticide toxidromes, E2 occupational EHS); 2 viable-with-caveat (E3 micro-mobility 11/24 OA; E4 Li-ion ~12/21); 4 no-go (3D-printing inhalation, solar PV electrocution, suspension trauma, post-naloxone paramedic assault). User chose to scaffold E1. |
| 3 | 2026-10-01T09:45Z | Charter | Project scaffolded from templates; project.md charter filled (case-series synthesis, CARE) | templates/ | project.md, search_log.md | Worker scope broadened per user decision; non-English sources in scope. |
| 4 | 2026-10-01T09:49Z | Search | Formal Europe PMC searches (main + case-series supplement), paginated, deduplicated | search_log.md rows 4–5; raw JSON in analysis/raw/ | 186 unique records; 177/186 OA/PMC | Europe PMC PUB_TYPE facet used (see search_log Note A on PubMed pt-tag unreliability). |
| 5 | 2026-10-01T09:50Z | Screening | Title/abstract-level screening of all 186 records: keyword heuristics + manual review of every exclusion (6 genuine cases rescued from over-exclusion) | screening_review.csv | 93 include / 93 exclude; decisions+reasons per record | Occupational/agricultural context of agent-only cases flagged for verification at full text (subcohort). Human screening review gate now OPEN. |
| 6 | 2026-10-01T09:52Z | Full-text retrieval | Fetched Europe PMC fullTextXML for all included records with a PMCID | 93 included records | papers/ (88 XML files, 5.1 MB) | 88/93 (95%) retrieved — exceeds the 80% case-series gate. 5 unavailable (3 no PMC ID, 2 empty XML); listed in analysis/raw/fulltext_status.json. |
| 7 | 2026-10-01T10:15–10:45Z | Extraction | 7 parallel subagents extracted per-case data from all 88 source texts into extraction/PMC*.json; primary agent validated: schema check (88/88 pass), 709-quote verbatim audit vs source texts | sources/*.txt | extraction/*.json (102 case objects) | AUDIT FINDINGS: (a) 28 quotes were not verbatim (1 subagent) → neutralised to UNVERIFIED, then re-extracted verbatim by a repair subagent (29 recovered); (b) 3 JSONs had contents rotated vs filenames (subagent file mix-up) → detected via global agent-vs-source cross-check, relabelled; 2 files lost in the relabelling were re-extracted directly by the primary agent from source (PMC13367297 emamectin, PMC13291128 chloropicrin) plus PMC13290272 paraquat re-extracted; (c) final verification: 708/708 quotes verbatim, 102 cases, 73 suitable papers, 15 excluded at full text with reasons (aggregate-only cohorts, reviews, chronic-exposure, non-pesticide). |

## Environment & reproducibility
- Agent: Hermes Agent (model/provider noted per session)
- Search date(s): see search_log.md — live web results, not reproducible snapshots; save raw responses in analysis/raw/
- Script versions: analysis/*.py committed as-is
- Data integrity: no value in any dataset was invented; UNVERIFIED marks fields not present in retrieved text
