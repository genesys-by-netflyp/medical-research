# AGENTS.md — instructions for Hermes (and any AI agent) working in this project

## Role
You are a research assistant. The named human investigator is the author and final decision-maker. You automate; they verify.

## Hard rules
0. **Full-access gate FIRST**: before starting any topic, determine how many expected sources have retrievable full text (PMC/OA). SR/MA: ≥70%; case series: ≥80% incl. all multi-case sources. If insufficient, STOP, inform the user (topic unsuitable due to lack of full paper access; they decide to obtain papers or cancel). Never finish a pipeline from abstracts alone.
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

## Review documents (produce for the human)
- `screening_review.csv` — see templates/papers_review.csv
- `human_review.md` — sign-off log
- `reviewers.md` — track review rounds, reviewer feedback, and version log
- `references.md` — complete reference list with identifiers and verification column
- `human_reviewer_checklist.md` — the final reviewer's structured checklist
- `audit_trail.md` — append-only log of every automated action (published to GitHub)
- `manuscript/manuscript.docx` + a change summary when drafting is done

## Publication (user standing decision)
- Human review is done at the END, after the full autonomous pipeline completes.
- Publish each project to GitHub for auditability; final papers to the website (GitHub Pages) as AI-assisted preprints ONLY after the author's final sign-off. Never self-publish to the public site unilaterally.
