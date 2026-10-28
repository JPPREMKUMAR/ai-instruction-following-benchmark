# Evaluation methodology

Mechanical checks should test observable requirements without pretending to infer meaning. The suite supports exact bullet counts, maximum word counts, required phrases/section strings, and required JSON keys. Human reviewers still determine whether the answer is factually correct, whether reasoning follows from premises, whether units are appropriate, and whether uncertainty is stated honestly.

## Human review rubric

Score each dimension 0–3: instruction adherence (all explicit constraints), reasoning validity (each inference follows), correctness (answer is supported), and uncertainty handling (identifies missing or conflicting information). Use 0 for absent/invalid, 1 for substantial failure, 2 for partial success, and 3 for satisfactory. Record a short rationale citing the prompt and response. Do not average away a critical error.

## Mechanical report metrics

The report gives task-bank size, the number of evaluations held in this process, task-type counts, and failed-check counts. The sample size is shown explicitly. API results are currently in memory and reset when the process restarts. A mechanical pass rate describes only these configured checks; it is not a model-wide score.

## Boundary cases

The dataset includes exact-bullet compliance and failure, arithmetic with units, an underspecified comparison, and JSON shape. Tests cover zero/missing/extra bullets, word limits, absent keys, malformed JSON, and duplicate task IDs. Semantic tasks remain human-reviewed.
