from turtle import done

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app= FastAPI()

class Task(BaseModel):
    title: str
    done:bool = False
    
tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False}
]

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", summary="Health Check", description="Check the health of the API")
async def healthcheck():
    return {"status": "ok"}

@app.get("/tasks", summary="Get Tasks", description="Get all tasks")
async def get_tasks( done: bool = None,search: str = None):
    if done is not None:
        filtered_tasks = [task for task in tasks if task["done"] == done]
        return filtered_tasks
    if search is not None:
        filtered_tasks = [task for task in tasks if search.lower() in task["title"].lower()]
        return filtered_tasks
    return tasks

@app.get("/tasks/{task_id}", summary="Get Task", description="Get a task by its ID")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.get("/stats", summary="Get Stats", description="Get statistics about tasks")
async def get_stats():
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task["done"]])
    return {"total": total_tasks, "done": completed_tasks,"open": total_tasks - completed_tasks}

@app.post("/tasks", summary="Create Task", description="Create a new task", status_code=201)
async def create_task(task: Task):
    if task.title:
        new_task= {"id": len(tasks) + 1, "title": task.title, "done": "False"}
        tasks.append(new_task)
        return new_task
    return JSONResponse(status_code=400, content={"error": "Task title is required"})

@app.put("/tasks/{task_id}", summary="Update Task", description="Update a task by its ID")
async def update_task(task_id: int, task: Task):
    if not task.title:
        return JSONResponse(status_code=400, content={"error": "Task title is required"})
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            t["done"] = task.done
            return t
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}", summary="Delete Task", description="Delete a task by its ID", status_code=204)
async def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})