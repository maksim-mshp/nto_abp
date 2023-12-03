import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import config

engine = create_engine(config.DATABASE_URL, echo=False)  # echo=True for database debug

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


from models.event_type import EventType
from models.event import Event
from models.job_type import JobType
from models.room import Room
from models.job import Job
from models.reservation import Reservation

from utils import CATEGORIES, JOB_STATUSES


def get_session():
    with session_maker() as session:
        yield session


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)


def add_sample_data():
    if os.path.exists(config.PROJECT_ROOT + '/' + config.DATABASE_NAME):
        create_database()
        return
    create_database()

    with session_maker() as session:
        session.add_all([
            EventType(name='Спектакль'),
            EventType(name='Концерт'),
            EventType(name='Репетиция'),
            EventType(name='Выставка'),
            EventType(name='Мастер-класс'),
            Event(title='Выставка «Архитектура и мода. В потоке времени»',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 11, 18), category=CATEGORIES[1],
                  event_type_id=4),
            Event(title='Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 11, 25), category=CATEGORIES[2],
                  event_type_id=5),
            Event(title='Спектакль-концерт в рамках проекта «П» в кубе: «Неделя просвещения»',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 11, 19), category=CATEGORIES[1],
                  event_type_id=5),
            JobType(name='Уборка'),
            JobType(name='Установка экспонатов'),
            JobType(name='Настройка оборудования'),
            JobType(name='Настройка освещения'),
            Room(name='Концертный зал'),
            Room(name='Выставочный зал'),
            Room(name='Театральная сцена'),
            Room(name='Звукозаписывающая студия'),
            Reservation(room_id=3, event_id=3),
            Reservation(room_id=4, event_id=2),
            Reservation(room_id=2, event_id=1),
            Job(title='Подготовка и установка экспонатов в выставочном зале', description='', event_id=1, job_type_id=2,
                job_room_id=2, registration_date=datetime.now(), deadline=datetime(2023, 11, 29),
                status=JOB_STATUSES[0]),
            Job(title='Настройка освещения в концертном зале', description='', event_id=3, job_type_id=4, job_room_id=1,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status=JOB_STATUSES[0]),
            Job(title='Настройка освещения в выставочном зале', description='', event_id=1, job_type_id=4,
                job_room_id=2, registration_date=datetime.now(), deadline=datetime(2023, 11, 29),
                status=JOB_STATUSES[1]),
            Job(title='Настройка звукозаписывающего оборудования в концертном зале', description='', event_id=3,
                job_type_id=3, job_room_id=1, registration_date=datetime.now(), deadline=datetime(2023, 12, 6),
                status=JOB_STATUSES[1]),
            Job(title='Уборка выставочного зала', description='', event_id=1, job_type_id=1, job_room_id=2,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 26), status=JOB_STATUSES[2]),
            Job(title='Уборка концертного зала', description='', event_id=3, job_type_id=1, job_room_id=1,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 27), status=JOB_STATUSES[2])
        ])
        session.commit()
