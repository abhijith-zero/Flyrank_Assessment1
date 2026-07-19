from fastapi import FastAPI
from fastapi.responses import JSONResponse

app= FastAPI()

class Task:
    def __init__(self, id: int, title: str, done: bool):
        self.id = id
        self.title = title
        self.done = done

tasks = [
    Task(1, "Task 1", False),
    Task(2, "Task 2", True),
    Task(3, "Task 3", False)
]

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def healthcheck():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return  task
    return JSONResponse(status_code=404, content= {"error":f"Task {task_id} not found"})
