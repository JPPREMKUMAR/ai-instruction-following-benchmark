import argparse
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from app.assessment import evaluate_response, load_jsonl

load_dotenv()

def main():
    parser=argparse.ArgumentParser(description="Run mechanical instruction checks against one response.")
    parser.add_argument("--tasks",default=os.getenv("TASK_BANK_PATH", "data/tasks.jsonl"))
    parser.add_argument("--task-id",required=True)
    parser.add_argument("--response-file",required=True)
    parser.add_argument("--output",default="reports/result.json")
    args=parser.parse_args()
    tasks=load_jsonl(args.tasks)
    task=next((t for t in tasks if t.task_id==args.task_id),None)
    if task is None: parser.error("unknown task ID")
    with open(args.response_file,encoding="utf-8") as f: response=f.read()
    result=evaluate_response(task,response)
    output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("w",encoding="utf-8") as f: json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
