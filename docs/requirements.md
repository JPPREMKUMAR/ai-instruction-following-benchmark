# Product requirements and acceptance criteria

## Problem and users

Evaluators need to separate easy-to-check output constraints from semantic judgments about correctness and reasoning. Users are benchmark authors, annotators, and reviewers checking model responses against a transparent task bank.

## MVP behavior

1. Read validated JSONL tasks with task type, constraints, expected behavior, reference reasoning, and ambiguity label.
2. Check configured phrase/section requirements, bullet count, word bounds, JSON parsing, and required keys.
3. Return each mechanical check separately and preserve a human-review-required signal.
4. Provide a CLI, FastAPI endpoints, a React review interface, and summary reports by task and failure.
5. Include arithmetic, format, multi-constraint, and underdetermined examples.

## Acceptance checks

- Exact boundaries for word/bullet limits and malformed JSON are tested.
- Mechanical pass is never presented as proof of correctness or sound reasoning.
- Ambiguous and underdetermined tasks invite uncertainty instead of forced guesses.
- CLI, API, tests, and frontend build run without a paid model API.

## Risks and limits

The current API keeps review results in memory, so they reset when its process restarts. JSON keys are checked, but JSON Schema value types and semantic constraint equivalence are not. Treat the small synthetic task bank as a software demonstration, not a model benchmark.
