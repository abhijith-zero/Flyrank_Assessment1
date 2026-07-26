from sqlmodel import create_engine

Database_URL = "sqlite:///./tasks.db"
engine = create_engine(Database_URL, echo=True)
