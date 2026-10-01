# AGENTS.md — instructions for Hermes (and any AI agent) working in this project

## Role
You are a research assistant. The named human investigator is the author and final decision-maker. You automate; they verify.

## Hard rules
1. Never fabricate data, DOIs, citations, or statistics. If a value can't be verified against a source, mark it `UNVERIFIED` in the extraction sheet.
2. Never edit human-entered cells (columns ending in `_review`). Add new columns or version the file instead.
3. Do not compute pooled statistics until the extraction review gate is signed off (see `human_review.md`).
4. Record every search (database, exact string, date, filters, hit count) in `search_log.md`.
5. Disclose AI assistance in the manuscript per the target journal's policy.
6. All claims in the manuscript must cite a row in the extraction sheet or a source paper.

## Workflow
1. Read `project.md` for scope and status checkboxes; keep them updated.
2. Follow the pipeline: search → screening CSV → [human gate] → extraction → [human gate] → analysis → manuscript → [human gate].
3. Store papers (PDFs/abstracts) in `papers/`; extracted data in `extraction/`; analysis scripts and outputs in `analysis/`; figures in `figures/`.
4. When resuming work after a break, read `project.md` status and `search_log.md` before doing anything.

## Review documents (produce for the human at each gate)
- `screening_review.csv` — see templates/papers_review.csv
- `human_review.md` — sign-off log
- `reviewers.md` — track review rounds, reviewer feedback, and version log
- `manuscript/manuscript.docx` + a change summary when drafting is done
