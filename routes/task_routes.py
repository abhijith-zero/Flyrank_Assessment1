from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from models.task import Task
from services.task_services import TaskService


router = APIRouter()

@router.get("/tasks")
async def get_tasks(done: bool = None, search: str = None):
    return TaskService.get_tasks(done, search)

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = TaskService.get_task(task_id)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task
@router.post("/tasks", status_code=201)
async def create_task(task: Task):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Task title is required"}
        )
        
    return TaskService.create_task(task)


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    updated = TaskService.update_task(task_id, task)

    if not updated:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return updated
@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    deleted = TaskService.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return Response(status_code=204)


@router.get("/stats")
async def stats():
    return TaskService.get_stats()