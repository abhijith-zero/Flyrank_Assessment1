from fastapi.responses import JSONResponse

from repositories.task_repository import TaskRepository
from models.task import Task

class TaskService:
    
    def get_tasks(done=None, search=None):
        tasks = TaskRepository.get_all_tasks()

        if done is not None:
            tasks = [t for t in tasks if t.done == done]

        if search:
            tasks = [
                t for t in tasks
                if search.lower() in t.title.lower()
            ]

        return tasks
    def get_task(task_id):
        return TaskRepository.get_by_id(task_id)
    
    def create_task(task):
        new_task = Task(title=task.title)
        return TaskRepository.add(new_task)
    
    def update_task(task_id, task):
        if not task.title.strip():
            return JSONResponse(
            status_code=400,
            content={"error": "Task title is required"}
        )
        return TaskRepository.update(task_id, task)
    def delete_task(task_id):
        return TaskRepository.delete(task_id)

    def get_stats():
        tasks = TaskRepository.get_all_tasks()

        total = len(tasks)
        completed = len([t for t in tasks if t.done])

        return {
            "total": total,
            "done": completed,
            "open": total - completed
        }