# Audit Trail — <project title>

Chronological, append-only log of every automated action. The agent appends; never rewrites history. This file is published to GitHub with the project.

| # | Timestamp (UTC) | Step | Action | Input/queries | Output artifact | Decisions & rationale |
|---|-----------------|------|--------|---------------|-----------------|----------------------|
| 1 | | Topic viability | Full-access pilot check | | | |
| 2 | | Search | Query 1 | exact string; db; date | search_log.md | |
| 3 | | Full-text retrieval | Fetched N full texts | sources | papers/*.txt | which failed & why |
| 4 | | Suitability | Verified at full text | | screening_review.csv | exclusions + reasons |
| 5 | | Extraction | Case/study-level extraction | papers/ | extraction/*.csv | UNVERIFIED fields listed |
| 6 | | Analysis | Descriptive/pooled stats | | analysis/* | method choices |
| 7 | | Synthesis | Manuscript draft vX | | manuscript/* | |
| 8 | | Packaging | references.md, checklist, zip | | | |
| 9 | | Human review | Sent to reviewers | | reviewers.md | gate outcomes |
| 10 | | Publication | GitHub commit + site publish (post sign-off) | commit hash | site URL | |

## Environment & reproducibility
- Agent: Hermes Agent (model/provider noted per session)
- Search date(s): see search_log.md — live web results, not reproducible snapshots; save raw responses in analysis/raw/
- Script versions: analysis/*.py committed as-is
- Data integrity: no value in any dataset was invented; UNVERIFIED marks fields not present in retrieved text
