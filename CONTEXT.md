# Medical Research — Master Context

This directory holds ALL medical research projects. One subfolder per project.
Completed projects move to `_archive/`.

## Standards that apply to EVERY project (reusable — do not duplicate in projects)

### Authorship & integrity
- The human (Dr. Shafira / named investigator) is the author. Hermes is a tool.
- AI assistance must be disclosed in the methods/acknowledgements per the target journal's policy and ICMJE/COPE guidance.
- The human's clinical interpretation, novelty, and final conclusions are theirs. Hermes drafts; the human decides.

### Mandatory human-review gates
0. **Full-access feasibility gate (BEFORE starting any topic)** — run a pilot search and determine full-text availability first. A topic needs ≥70% (SR/MA) or ≥80% (case series; all multi-case sources) of expected sources with retrievable full text. If insufficient, STOP and inform the user — the topic is unsuitable due to lack of full paper access until they obtain the papers or cancel. Never complete a pipeline on abstract-level extraction alone.
1. **Screening gate** — Hermes produces the screening CSV; the human approves final include/exclude before full-text extraction.
2. **Extraction gate** — extracted data are spot-checked by the human against source PDFs before any pooled statistics are computed.
3. **Final review gate** — full manuscript + analyses reviewed and edited by the human before submission. Human review ALWAYS comes after the full automated process is complete, never interleaved as a blocker.

### Methodology defaults
- Systematic reviews / meta-analyses: follow PRISMA 2020; register protocol (PROSPERO) before screening.
- Case-series syntheses: follow CARE guidelines; case table is the core artifact.
- Searches: PubMed, Europe PMC, Cochrane Library, plus hand-searching of references. Record exact search strings and dates in `search_log.md`.
- Statistics: Python (numpy/scipy/statsmodels) in a venv; fixed vs random effects chosen by heterogeneity (I², Q); assess publication bias (funnel plot, Egger's test).
- Every number in the manuscript must be traceable to an extraction sheet row and a source paper.

### File conventions
- CSVs are UTF-8, comma-delimited; one row per paper/case; every review column ends with `_review` suffix and is left blank for the human.
- Figures: PNG, 300 dpi, saved in `figures/`; source scripts in `analysis/`.
- Never overwrite human-entered cells in review CSVs; write Hermes updates to new columns or a versioned file.

## Project scaffold
Every new project starts from `templates/` — see `templates/README.md` for the copy procedure.
