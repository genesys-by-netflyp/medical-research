# Human Reviewer Checklist — mNGS in haemato-oncology SR/MA

Prepared 2026-10-01 by the autonomous pipeline. **The paper is published as an AI-assisted preprint but awaits your final sign-off; any correction after sign-off triggers a versioned update (see reviewers.md).**

## 1. Screening review
- Open `screening_review.csv`. Columns `include_exclude` and `reason` (your columns) are blank for you.
- Check the 40 INCLUDE?/MAYBE records; the auto-exclusions (case reports/reviews/out-of-scope) are in `screen_auto`.

## 2. Extraction spot-check (mandatory before pooled numbers are final)
For each of the 14 2x2 studies in `analysis/analysis_dataset.csv`, open the source full text in `papers/<PMID>_<PMCID>.xml` and compare against `extraction/<PMID>.json` → `evidence_quotes`. Priority checks:
- PMID 40453877 (TP59/FP3/FN3/TN52) — headline study
- PMID 42131265 (127/16/35/26)
- PMID 37780852 (90/94/23/51 — note the subagent reordered to TP/FP/FN/TN)
- PMID 41868021 (reconstructed from Table 3; heavy incorporation bias)
- All four back-derived tables: 35509305, 35837537, 40415957, 41868021

## 3. Statistics
- `analysis/run_stats.py` (input: analysis_dataset.csv). Results in `pooled_results.json`.
- Verify: A-group pooled sens 84% (65–94), spec 86% (70–94); B-group sens 77% (67–84), spec 24% (17–33); yield 78% (69–84).
- Confirm you accept the grouping choice (A vs final/clinical dx; B vs CMT agreement) and the treatment of B-group specificity as incremental detection.

## 4. Manuscript
- `manuscript/manuscript.docx` (validated). Check every number, the AI-disclosure section, and the title/authorship.

## 5. Publication decision
- GitHub audit repo: published (public).
- Preprint site: published with AI-assisted/not-peer-reviewed/not-medical-advice disclaimer, per your instruction. If you do NOT want it live before journal submission, say so and it will be taken down immediately (versions are preserved in git history).

## Sign-off
| Item | Reviewer | Date | Decision |
|---|---|---|---|
| Screening | ______ | | ☐ approve ☐ revise |
| Extraction | ______ | | ☐ approve ☐ revise |
| Statistics | ______ | | ☐ approve ☐ revise |
| Manuscript | ______ | | ☐ approve ☐ revise |
