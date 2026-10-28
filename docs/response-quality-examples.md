# Response-quality examples

These examples are synthetic task/response pairs for the assessment suite. Mechanical checks validate only the stated constraints; semantic correctness still needs a reviewer.

| Category | Task and sample response | Expected check / human note |
|---|---|---|
| Correct | “Give exactly two bullets and include ‘unique password’.” Response has two accurate bullets and the exact phrase. | Bullet and phrase checks pass; reviewer confirms the advice is sound. |
| Incorrect | “A vehicle travels 150 km in 3 hours. Show the division and speed in km/h.” Response: “150 ÷ 3 = 60 km/h.” | Required tokens might all appear, but the arithmetic is wrong; human correctness judgment must catch it. |
| Incomplete | Same task; response: “50.” | Missing the division and unit; constraints fail and answer is incomplete. |
| Misleading | “Are these two candidates comparable?” with no candidates. Response: “A is definitely better.” | Unsupported conclusion; the underdetermined-task signal calls for clarification. |
| Ambiguous | “Which candidate is better?” Response: “I need the candidates and criteria to compare them.” | Appropriate uncertainty; no winner should be forced. |
| Poorly formatted | “Return JSON with keys answer and confidence.” Response: `{"answer":"4","confidence":}` | JSON parse fails; report the format failure separately from semantic correctness. |

A phrase match is not proof of reasoning quality. Inspect per-check details and preserve uncertainty in the reviewer judgment.
