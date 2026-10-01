# Audit Trail — CDC in acute leukaemia case series

Append-only log of automated actions. Published to GitHub with the project.

| # | Date (UTC) | Step | Action | Output | Decisions & rationale |
|---|-----------|------|--------|--------|----------------------|
| 1 | 2026-09-30 | Topic selection | User selected topic #6 (opportunistic infections in haematology; example: CDC in acute leukaemia) from haematology_research_topics.md | project.md | Duplicate pre-check run for Tier-1 topics; #6 chosen for low duplication risk |
| 2 | 2026-09-30 | Search | 4 queries: Europe PMC ×2 (30 + 384 hits, first 100 retrieved), PubMed E-utilities ×2 (42 + 20 hits) | search_log.md, analysis/search_raw.json | Europe PMC rate-limited (HTTP 503) on extra queries; compensated with PubMed queries |
| 3 | 2026-09-30 | Screening | 48 unique records screened by title/abstract | screening_review.csv (19 INCLUDE / 29 EXCLUDE) | Automated screening with documented per-record reasons |
| 4 | 2026-09-30 | Extraction v1 | Abstract-level extraction (24 case rows, 19 sources) | extraction/case_extraction.csv | Later superseded — retained for audit |
| 5 | 2026-09-30 | Analysis v1 | Descriptive stats + Figure 1 | analysis/summary_stats.json, figures/fig1_characteristics.png | Descriptive only — no pooling, heterogeneity too high |
| 6 | 2026-09-30 | Manuscript v0.1 | Full draft docx | manuscript/manuscript.docx | Zipped and sent to user (v0.1 package) |
| 7 | 2026-09-30 | Full-access audit | User asked about full access; audit found 7/19 sources with retrievable full text | analysis + chat | Below the 80% case-series threshold → user informed with options |
| 8 | 2026-09-30 | Pipeline update | New Step-0 full-access feasibility gate added to skill, CONTEXT.md, AGENTS.md templates (user instruction) | skills | Applies to all future projects |
| 9 | 2026-09-30 | User decision | Option 2 chosen: restrict cohort to full-text-accessible sources | project.md notes | |
| 10 | 2026-09-30 | Full-text retrieval | 7 sources fetched (6 PMC XML + 1 BMC HTML; 1 PMC XML failed → fetched via PMC website) | papers/*.txt | |
| 11 | 2026-09-30 | Full-text analysis | All 7 sources read sentence-by-sentence; case data verified at full text | extraction/case_extraction_fulltext.csv | S38 (Chinese) initially unparseable with English term filters — flagged |
| 12 | 2026-09-30 | Analysis v2 + Manuscript v0.2 | Restricted-cohort stats, figure, draft v0.2 (docx + PDF) | analysis/, figures/, manuscript/ | Zipped and sent to user (v0.2 package) |
| 13 | 2026-10-01 | Pipeline update | New rules from user: (a) non-English papers MUST be analysed in original language; (b) no-go rule: <2 papers passing full-access + suitability filters → skip title | skills | |
| 14 | 2026-10-01 | Refinement | Chinese full text (S38, PMC9800221) parsed in original language; 3 cases fully extracted (C. albicans ×2 by tissue NGS, C. parapsilosis by blood NGS; 1 suspected IRIS; 1 lost to follow-up) | extraction/case_extraction_fulltext.csv v0.3 | CSV column-shift bug from unquoted comma ("46,XX") found and fixed — all stats re-verified |
| 15 | 2026-10-01 | Analysis v3 + Manuscript v0.3 | Final stats (10/10 cases extracted; median age 18; species 8/10; IRIS 3; 0 deaths), figure, draft v0.3 (PDF) | analysis/, figures/, manuscript/manuscript_v03.pdf | |

## Environment & reproducibility
- Agent: Hermes Agent, model glm-5.3-flash (provider nous), hosted instance
- Search dates: 2026-09-30 (live queries — not reproducible snapshots; raw responses in analysis/)
- Analysis scripts: analysis/summarize*.py, analysis/make_figure*.py (committed as-is)
- Data integrity: no value in any dataset was invented; UNVERIFIED marks fields not present in retrieved text; all UNVERIFIED rows were later resolved at full text except the S40a age (adult female, exact age not stated in text)
