# Anemia — Animated Explainer (plan.md)

## Narrative arc
Misconception corrected: anemia is not a disease — it is a *sign* with a differential.
The viewer moves from "low hemoglobin" → why the body cares (oxygen delivery) →
the two mechanistic buckets (less production vs. more loss/destruction) → the practical
MCV-based workup they'd actually use in clinic. Aha moment: one number (Hb) plus one
ratio (MCV) almost organizes the whole differential.

## Scene list
1. **S1 Title** — "Anemia" + subtitle "A sign, not a diagnosis". Sparse, red accent.
2. **S2 Why it matters** — a red blood cell, hemoglobin dots, oxygen molecules flowing to
   tissue; contrast normal vs. low Hb delivery. Dominant color: red/crimson.
3. **S3 Definition** — WHO thresholds as a clean bar/number layout: Hb < 13 g/dL (men),
   < 12 g/dL (non-pregnant women). Dominant: blue.
4. **S4 Mechanisms** — balance visual: bone marrow production arrow up vs. loss/destruction
   arrow down; both paths land on the same low-Hb state. Dominant: green + red.
5. **S5 MCV workup** — three columns: microcytic (<80), normocytic (80–100), macrocytic
   (>100) with key differentials under each. Dominant: yellow/gold.
6. **S6 Symptoms + close** — constellation of symptoms around a patient glyph; closing line:
   "Treat the cause, not just the number."

## Visual language
- Palette: BG #1C1C1C; RED #FF4D4D; BLUE #58C4DD; GREEN #83C167; GOLD #FFD93D; GREY #888888
- Font: DejaVu Sans Mono (no LaTeX available in this environment — all text via Text())
- Opacity layering: primary 1.0, contextual 0.4, structure 0.15
- Every animation followed by a wait; key reveals get 2–3 s.

## Voiceover
Not used (silent, subtitled) — every animation carries an `add_subcaption`.
