import os

from dotenv import load_dotenv
from models.task import Task
from sqlmodel import Session, SQLModel, create_engine


load_dotenv()  # take environment variables from .env.
Database_URL = os.getenv("DATABASE_URL")

engine = create_engine(Database_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        total_tasks = session.query(Task).count()
        if total_tasks == 0:
            
            initial_tasks = [
                Task(title="Task 1", done=False),
                Task(title="Task 2", done=True),
                Task(title="Task 3", done=False)
            ]
            session.add_all(initial_tasks)
            session.commit()
            