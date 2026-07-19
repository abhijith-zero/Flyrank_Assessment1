from fastapi import FastAPI

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

