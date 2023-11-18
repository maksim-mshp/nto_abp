import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import config

engine = create_engine(config.DATABASE_URL, echo=True)  # echo=True for database debug

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


from models.event_type import EventType
from models.event import Event
from models.job_type import JobType
from models.job_room import JobRoom
from models.job import Job


def get_session():
    with session_maker() as session:
        yield session


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)


def add_sample_data():
    if os.path.exists('../sqlite.db'):
        create_database()
        return
    create_database()

    with session_maker() as session:
        session.add_all([
            EventType(name='Cпектакль'),
            EventType(name='Концерт'),
            EventType(name='Репетиция'),
            EventType(name='Выставка'),
            EventType(name='Мастер-класс'),
            Event(title='Выставка «Архитектура и мода. В потоке времени»',
                  description='Очень круто событие приходите!!!', date=datetime(2023, 11, 18), category='Просвещение',
                  event_type_id=4),
            Event(title='Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
                  description='Очень круто событие приходите!!!', date=datetime(2023, 11, 25), category='Образование',
                  event_type_id=5),
            Event(title='Спектакль-концерт в рамках проекта «П» в кубе: «Неделя просвещения»',
                  description='Очень круто событие приходите!!!', date=datetime(2023, 11, 19), category='Просвещение',
                  event_type_id=5),
            JobType(name='Уборка'),
            JobType(name='Установка экспонатов'),
            JobType(name='Настройка оборудования'),
            JobType(name='Настройка освещения'),
            JobRoom(name='Концертный зал'),
            JobRoom(name='Выставочный зал'),
            JobRoom(name='Театральная сцена'),
            JobRoom(name='Звукозаписывающая студия'),
            Job(title='Подготовка и установка экспонатов в выставочном зале', description='', event_id=1, job_type_id=2,
                job_room_id=2, registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status='Создано'),
            Job(title='Настройка освещения в концертном зале', description='', event_id=3, job_type_id=4, job_room_id=1,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status='Создано'),
            Job(title='Настройка освещения в выставочном зале', description='', event_id=1, job_type_id=4,
                job_room_id=2, registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status='К работе'),
            Job(title='Настройка звукозаписывающего оборудования в концертном зале', description='', event_id=3,
                job_type_id=3, job_room_id=1, registration_date=datetime.now(), deadline=datetime(2023, 11, 25),
                status='К работе'),
            Job(title='Уборка выставочного зала', description='', event_id=1, job_type_id=1, job_room_id=2,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status='Выполнено'),
            Job(title='Уборка концертного зала', description='', event_id=3, job_type_id=1, job_room_id=1,
                registration_date=datetime.now(), deadline=datetime(2023, 11, 25), status='Выполнено')
        ])
        session.commit()
