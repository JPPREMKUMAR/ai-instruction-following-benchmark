from typing import Any
from pydantic import BaseModel, Field

class Checks(BaseModel):
    exact_bullets: int | None = Field(default=None, ge=0, le=50)
    max_words: int | None = Field(default=None, ge=1, le=10000)
    required_phrases: list[str] = Field(default_factory=list)
    required_json_keys: list[str] = Field(default_factory=list)
    required_sections: list[str] = Field(default_factory=list)

class Task(BaseModel):
    task_id: str = Field(min_length=1, max_length=100)
    task_type: str = Field(min_length=1, max_length=80)
    prompt: str = Field(min_length=1, max_length=10000)
    expected_behavior: str = Field(min_length=1, max_length=2000)
    reference_reasoning: str = Field(min_length=1, max_length=2000)
    underdetermined: bool = False
    checks: Checks = Field(default_factory=Checks)

class EvaluateRequest(BaseModel):
    task_id: str
    response: str = Field(min_length=1, max_length=20000)
    semantic_judgment: str | None = None
    rationale: str | None = None

class CheckResult(BaseModel):
    name: str
    passed: bool
    detail: str

class EvaluationResult(BaseModel):
    task_id: str
    checks: list[CheckResult]
    mechanical_pass: bool
    semantic_judgment: str
    uncertainty_note: str

