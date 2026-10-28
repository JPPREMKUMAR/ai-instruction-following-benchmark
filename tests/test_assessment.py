import json
import pytest
from app.assessment import build_report, evaluate_response, load_jsonl
from app.models import Task

def task(checks):
    return Task(task_id="t",task_type="test",prompt="p",expected_behavior="e",reference_reasoning="r",checks=checks)

def test_exact_bullets_and_required_phrase():
    result=evaluate_response(task({"exact_bullets":2,"required_phrases":["unique password"]}),"- Use a unique password.\n- Turn on MFA.")
    assert result["mechanical_pass"] is True

@pytest.mark.parametrize("response,expected",[("one\ntwo",False),("- one\n- two\n- three",False),("- one\n- two",True)])
def test_bullet_boundary(response,expected):
    assert evaluate_response(task({"exact_bullets":2}),response)["mechanical_pass"] is expected

def test_word_limit_and_missing_json_keys():
    assert not evaluate_response(task({"max_words":2}),"one two three")["mechanical_pass"]
    result=evaluate_response(task({"required_json_keys":["answer"]}),'{"other":true}')
    assert result["checks"][0]["passed"] is False

def test_malformed_json_is_a_failed_check():
    result=evaluate_response(task({"required_json_keys":["answer"]}),"{bad")
    assert result["checks"][0]["detail"] == "Response is not valid JSON."

def test_report_tracks_sample_size_and_failures():
    t=task({"exact_bullets":2})
    result=evaluate_response(t,"one line")
    report=build_report([t],[result])
    assert report["evaluation_count"] == 1
    assert report["failure_counts"] == {"bullet_count":1}
    assert report["limitations"]

def test_duplicate_task_ids_rejected():
    from pathlib import Path
    row=json.dumps({"task_id":"x","task_type":"test","prompt":"p","expected_behavior":"e","reference_reasoning":"r"})
    path=Path(__file__).parent/"duplicate-tasks.tmp.jsonl"
    try:
        path.write_text(row+"\n"+row,encoding="utf-8")
        with pytest.raises(ValueError,match="unique"):
            load_jsonl(str(path))
    finally:
        path.unlink(missing_ok=True)
