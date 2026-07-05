from sqlmodel import create_engine, Session
from config import database_url

engine = create_engine(database_url)

def get_session():
    with Session(engine) as session:
        yield session