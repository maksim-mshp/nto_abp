from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import config

engine = create_engine(config.DATABASE_URL, echo=False)  # echo=True for database debug

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    with session_maker() as session:
        yield session


def create_database():
    from models.event_type import EventType
    from models.event import Event
    from models.job_type import JobType
    from models.job_room import JobRoom
    from models.job import Job

    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)
