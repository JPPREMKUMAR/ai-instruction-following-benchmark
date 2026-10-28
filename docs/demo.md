# Demonstration script

1. From the project directory, run the CLI command shown in the README with `examples/response.txt` and task `format-two-bullets`.
2. Inspect each mechanical check and the explicit `human_review_required` signal.
3. In the web interface, compare a compliant response with a response that has the wrong number of bullets or omits the required phrase.
4. Submit an underdetermined task response that says information is insufficient, then inspect the summary.

**Expected behavior:** The supplied sample meets the configured two-bullet and required-phrase checks. That pass only confirms those mechanical conditions; a reviewer must still judge factual accuracy and reasoning. The four bundled tasks are synthetic examples, not benchmark results.
