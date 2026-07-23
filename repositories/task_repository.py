tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False}
]

class TaskRepository:
    
    def get_all_tasks():
        return tasks
    
    def get_by_id(task_id: int):
        return next((t for t in tasks if t["id"] == task_id), None)
    
    def add(task):
        tasks.append(task)
        return task

    def update(task_id, data):
        task = TaskRepository.get_by_id(task_id)

        if task:
            task.update(data)

        return task
    
    def delete(task_id):
        task = TaskRepository.get_by_id(task_id)

        if task:
            tasks.remove(task)

        return task