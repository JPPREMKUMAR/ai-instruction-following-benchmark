import json
import re
from app.models import CheckResult, Task

def evaluate_response(task: Task, response: str) -> dict:
    results: list[CheckResult] = []
    checks = task.checks
    if checks.exact_bullets is not None:
        count = sum(bool(re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line)) for line in response.splitlines())
        results.append(CheckResult(name="bullet_count", passed=count == checks.exact_bullets,
                                   detail=f"Expected exactly {checks.exact_bullets}; found {count}."))
    if checks.max_words is not None:
        count = len(response.split())
        results.append(CheckResult(name="word_limit", passed=count <= checks.max_words,
                                   detail=f"Maximum {checks.max_words} words; found {count}."))
    for phrase in checks.required_phrases:
        present = phrase.casefold() in response.casefold()
        results.append(CheckResult(name="required_phrase", passed=present,
                                   detail=f"Required phrase {'present' if present else 'missing'}: {phrase}"))
    for section in checks.required_sections:
        present = section.casefold() in response.casefold()
        results.append(CheckResult(name="required_section", passed=present,
                                   detail=f"Required section {'present' if present else 'missing'}: {section}"))
    if checks.required_json_keys:
        try:
            parsed = json.loads(response)
            missing = [key for key in checks.required_json_keys if key not in parsed]
            results.append(CheckResult(name="json_schema_keys", passed=not missing,
                                       detail="Valid JSON; " + ("all required keys present." if not missing else f"missing keys: {', '.join(missing)}.")))
        except (json.JSONDecodeError, TypeError):
            results.append(CheckResult(name="json_schema_keys", passed=False, detail="Response is not valid JSON."))
    passed = all(result.passed for result in results)
    return {"task_id": task.task_id, "checks": [r.model_dump() for r in results],
            "mechanical_pass": passed, "semantic_judgment": "human_review_required",
            "uncertainty_note": "Mechanical checks cannot establish reasoning validity or factual correctness."}

def load_jsonl(path: str) -> list[Task]:
    tasks=[]
    with open(path, encoding="utf-8") as source:
        for line_no, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                tasks.append(Task.model_validate_json(line))
            except Exception as exc:
                raise ValueError(f"Invalid task on line {line_no}: {exc}") from exc
    if not tasks:
        raise ValueError("Task bank is empty")
    ids=[task.task_id for task in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("Task IDs must be unique")
    return tasks

def build_report(tasks: list[Task], results: list[dict]) -> dict:
    by_type={}
    for task in tasks:
        group=by_type.setdefault(task.task_type,{"task_count":0,"evaluated_count":0,"mechanical_pass_count":0})
        group["task_count"]+=1
    task_types={task.task_id:task.task_type for task in tasks}
    failures={}
    for result in results:
        task_type=task_types.get(result.get("task_id"),"unknown")
        group=by_type.setdefault(task_type,{"task_count":0,"evaluated_count":0,"mechanical_pass_count":0})
        group["evaluated_count"]+=1
        group["mechanical_pass_count"]+=int(result.get("mechanical_pass",False))
        for check in result.get("checks",[]):
            if not check.get("passed"):
                failures[check.get("name","unknown")]=failures.get(check.get("name","unknown"),0)+1
    return {"task_count":len(tasks),"evaluation_count":len(results),"by_task_type":by_type,
            "failure_counts":failures,"underdetermined_count":sum(t.underdetermined for t in tasks),
            "limitations":"Mechanical pass rates cover only these examples and checks; they do not measure general model quality. Semantic judgments require human review."}
