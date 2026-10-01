
# Per-study extraction task (mNGS in haemato-oncology project)

You are extracting data for a diagnostic-accuracy systematic review/meta-analysis.
Source files: /opt/data/medical-research/2026-10_mngs-infections-haemato/papers/<PMID>_<PMCID>.xml (Europe PMC full-text XML).
Output: /opt/data/medical-research/2026-10_mngs-infections-haemato/extraction/<PMID>.json — ONE file per paper.

JSON schema (all fields required; use null or [] when absent; NEVER fabricate — only numbers you can quote from the text):
{
  "pmid", "pmcid", "citation" (authors, title, journal, year),
  "language",
  "study_design" (retrospective/prospective cohort etc),
  "study_period",
  "population": {"n_total", "n_haemato_or_transplant" (only counts usable by us), "population_description", "haemato_subtypes"},
  "neutropenic_status" (how defined, if reported),
  "specimens": list of {type, n_tests},
  "index_test": {"platform_or_panel", "commercial_or_inhouse", "dna_and_or_rna"},
  "reference_standard" (final diagnosis basis: clinical + microbiology + follow-up?),
  "comparator_2x2": null or {"TP","FP","FN","TN","against" (what the mNGS was compared with), "unit" (patient/episode/specimen)},
  "diagnostic_yield": {"n_tests","n_positive_relevant_pathogens","yield_percent","basis"},
  "additional_yield_vs_conventional" (mNGS positive where conventional negative, with counts),
  "turnaround_time" (hours/days if reported),
  "therapy_change" (counts if reported),
  "mortality_or_outcomes" (if reported),
  "quality_flags": {"prospective_consecutive_enrollment" bool/null, "blinding_of_index_result" yes/no/unclear, "paired_data" bool, "overlap_risk" (notes)},
  "quadas2_notes",
  "evidence_quotes": list of {"claim", "quote" (verbatim sentence(s) from full text), "section"},
  "usable_for_pooled_analysis": "2x2" | "yield-only" | "not-usable",
  "exclusion_reason" (if not usable)
}

RULES:
1. Read the FULL text (use python xml.etree to strip tags or read raw text; files are on disk).
2. Every numeric value you extract MUST have a verbatim quote in evidence_quotes. If a number cannot be verified, write null and note in quadas2_notes.
3. Build comparator_2x2 only when the paper reports it (or reports TP/FN counts vs final diagnosis that let you build it). Do not invent denominators. If the paper reports only "mNGS detected X% more pathogens than culture", record it verbatim under additional_yield_vs_conventional and set usable_for_pooled_analysis = "yield-only".
4. Case reports/small n (<5 patients): usable_for_pooled_analysis = "not-usable".
5. Chinese/Japanese/non-English text: extract normally in source language.
6. Write the JSON file atomically. Print a one-line summary per paper: PMID | design | n | specimens | usable.
7. Do not modify any other project file.
