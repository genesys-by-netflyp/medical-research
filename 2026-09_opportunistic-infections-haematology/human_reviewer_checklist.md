# Human Reviewer Checklist — <project title>

For the reviewing clinician(s). The pipeline was completed autonomously; your review is the final quality gate before the paper is published to the website / submitted to a journal.

## A. Suitability of listed papers (~30 min)
- [ ] Open `screening_review.csv`; scan the included sources list.
- [ ] Confirm the case/study definition matches your clinical judgement (would you include these?).
- [ ] Flag any paper that does NOT belong in the series (wrong population, wrong syndrome, duplicate case).
- [ ] Check `references.md` excluded list — should any exclusion be reversed?

## B. Data extraction (~60 min for a case series)
- [ ] Spot-check every case row in `extraction/` against the source paper (`papers/`).
- [ ] Resolve every `UNVERIFIED` cell (species, sex, age, outcome...).
- [ ] Confirm no value was misread or invented.

## C. Analysis (~15 min)
- [ ] Review `analysis/summary_stats.json` and figures — do the numbers match the data?
- [ ] Agree with the choice of descriptive-only vs pooled statistics.
- [ ] Confirm heterogeneity/publication-bias discussion is adequate.

## D. Manuscript (~60 min)
- [ ] Read `manuscript/` (docx/PDF). Check clinical interpretation and conclusions — they must be defensible.
- [ ] Verify every claim maps to a data row or reference.
- [ ] Check AI-disclosure wording is accurate and sufficient.
- [ ] Confirm authorship list and order; acknowledgements for non-author reviewers.

## E. Sign-off
- Reviewer name: ______ Date: ______
- Decision: [ ] Publish to site (AI-assisted preprint)  [ ] Submit to journal  [ ] Revise first
- Notes:
