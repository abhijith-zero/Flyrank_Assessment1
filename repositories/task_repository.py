from database import engine
from models.task import Task
from sqlmodel import Session, select

class TaskRepository:
    
    def get_all_tasks():
        with Session(engine) as session:
            return session.exec(select(Task)).all()
    
    def get_by_id(task_id: int):
        with Session(engine) as session:
            return session.get(Task, task_id)
    
    def add(task):
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def update(task_id, task):
        with Session(engine) as session:
            db_task = session.get(Task, task_id)
            if not db_task:
                return None
            db_task.title = task.title
            db_task.done = task.done
            session.commit()
            session.refresh(db_task)
            return db_task
    
    def delete(task_id):
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()
                return task
