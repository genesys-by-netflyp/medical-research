# Human Review Log — CDC in acute leukaemia case series

**Version v0.2 (current):** cohort restricted to 7 full-text-accessible sources (10 cases) per the full-access feasibility gate (option 2 chosen by author). All 7 full texts retrieved into `papers/` and analysed individually; dataset = `extraction/case_extraction_fulltext.csv`. Manuscript = `manuscript/manuscript_v02.docx`. Superseded abstract-level extraction retained for audit. 3 Chinese-language cases (S38) retrieved but not individually extracted — flagged for author (Chinese reader) or exclusion.

## Automation summary (what was done without human input)
- Search: 4 queries (Europe PMC ×2, PubMed ×2; see `search_log.md`), 48 deduplicated records.
- Screening: 29 excluded, 19 sources met case definition → `screening_review.csv`.
- Full-access gate: 7/19 sources (≈37%) had retrievable full text — below the 80% case-series threshold; author chose to restrict the cohort (option 2).
- Full-text analysis: all 7 sources read; 10 case rows extracted (7 fully, 3 Chinese-language pending).
- Analysis: descriptive statistics only (`analysis/summary_stats.json`), Figure 1.
- Manuscript: draft v0.2 (`manuscript/manuscript_v02.docx`).

## Gate 1 — Screening review
- What to review: `screening_review.csv` (48 rows) — confirm or override `screening_decision_hermes` (19 INCLUDE / 29 EXCLUDE), fill `screening_decision_review`.
- Reviewed by: ______  Date: ______
- Changes/notes:

## Gate 2 — Extraction review (CRITICAL for this project)
- **Extraction was abstract-level only.** Every `UNVERIFIED` cell (12 of 24 cases lack species; several lack sex/age/outcome) and every extracted value must be checked against the full texts (PMIDs in the CSV). Papers to obtain are listed by PMID in `screening_review.csv`.
- What to review: `extraction/case_extraction.csv` — all rows, against source PDFs.
- Reviewed by: ______  Date: ______
- Rows checked / corrections:

## Gate 3 — Final manuscript review
- What to review: `manuscript/manuscript.docx` (draft v0.1), Figure 1, `analysis/summary_stats.json`, reference list (PMIDs only — full citations pending Gate 2), AI-disclosure wording.
- Known draft weaknesses to check: (1) abstract says "24 case-level rows (21 unique patients)" — verify counting convention; (2) case C04 (infant, pre-treatment infection) arguably fails the classic CDC definition — consider excluding; (3) candidate journals: Journal of Fungi, Mycoses, Leukemia & Lymphoma, IDCases — check AI policy and case-series acceptance.
- Reviewed by: ______  Date: ______
- Decision: [ ] approve for submission  [ ] revise (notes below)
- Notes:
