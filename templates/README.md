# Templates — how to start a new project

To create a new project (e.g. `2026-10_venous-thrombosis-oral-cancer`):

```
cd /opt/data/medical-research
mkdir -p <project-slug>/{papers,extraction,analysis,figures,manuscript}
cp templates/project.md templates/AGENTS.md templates/human_review.md \
   templates/papers_review.csv templates/search_log.md templates/reviewers.md \
   templates/audit_trail.md templates/references.md templates/human_reviewer_checklist.md <project-slug>/
```

Then rename `papers_review.csv` → `screening_review.csv` in the project folder and fill in `project.md`.

## Included files
- `project.md` — project charter: question, criteria, status checkboxes
- `AGENTS.md` — standing rules for any AI agent working in the folder
- `human_review.md` — the 3 human sign-off gates (always LAST, after each automated step completes)
- `papers_review.csv` — screening/review sheet (blank `_review` columns are for the human only)
- `search_log.md` — reproducible search record + PRISMA counts
- `audit_trail.md` — append-only log of every automated action (published to GitHub)
- `references.md` — complete reference list with identifiers + verification column
- `human_reviewer_checklist.md` — structured checklist for the final human reviewer

Master-level reusable rules live in `../CONTEXT.md` — do not copy them into projects.
