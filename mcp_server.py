from fastapi import FastAPI
import json
import os

app = FastAPI()
TASK_FILE = "tasks.json"

def read_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.get("/get_tasks")
async def get_tasks():
    return {"tasks": read_tasks()}

@app.post("/add_task")
async def add_task(title: str, due_date: str = None):
    tasks = read_tasks()
    new_task = {"title": title, "due_date": due_date, "created_at": "now"}
    tasks.append(new_task)
    save_tasks(tasks)
    return {"success": True, "new_task": new_task}
