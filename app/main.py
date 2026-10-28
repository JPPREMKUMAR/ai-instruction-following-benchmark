import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from app.assessment import build_report, evaluate_response, load_jsonl
from app.models import EvaluateRequest

load_dotenv()
app=FastAPI(title="Instruction Following and Reasoning Assessment Suite", version="0.1.0")
TASKS=load_jsonl(os.getenv("TASK_BANK_PATH", "data/tasks.jsonl"))
RESULTS=[]

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.get("/api/tasks")
def tasks(): return [task.model_dump() for task in TASKS]

@app.post("/api/evaluate")
def evaluate(payload: EvaluateRequest):
    task=next((t for t in TASKS if t.task_id==payload.task_id),None)
    if task is None: raise HTTPException(404,"Task not found")
    result=evaluate_response(task,payload.response)
    result["semantic_judgment"]=payload.semantic_judgment or "human_review_required"
    result["rationale"]=payload.rationale
    RESULTS.append(result)
    return result

@app.get("/api/report")
def report():
    return build_report(TASKS,RESULTS)
