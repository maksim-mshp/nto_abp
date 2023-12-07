import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import config

engine = create_engine(config.DATABASE_URL, echo=False)  # echo=True for database debug

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


from models.event_type import EventType
from models.club_type import ClubType
from models.teacher import Teacher
from models.event import Event
from models.job_type import JobType
from models.room import Room
from models.job import Job
from models.reservation import Reservation

from utils import CATEGORIES, JOB_STATUSES, STORAGE


def get_session():
    with session_maker() as session:
        yield session


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)


def add_sample_data():
    from services.reservation import reservation_service

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
            Teacher(name="Иванова Анна Петровна"),
            Teacher(name="Смирнов Алексей Игоревич"),
            Teacher(name="Козлова Екатерина Дмитриевна"),
            Teacher(name="Попов Денис Сергеевич"),
            ClubType(name='Музыкальное творчество'),
            ClubType(name="Робототехника"),
            ClubType(name="Рисование"),
            ClubType(name="Танцы"),
            # event_id 1
            Event(title='Выставка «Архитектура и мода. В потоке времени»',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 14), category=CATEGORIES[1],
                  event_type_id=4),
            # event_id 2
            Event(title='Спектакль-концерт в рамках проекта «П» в кубе: «Неделя просвещения»',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 5), category=CATEGORIES[1],
                  event_type_id=1),
            # event_id 3
            Event(
                title='Выставка «Под занавесом. Мировые звезды — в объективе легендарного фотографа «Известий» Сергея Смирнова»',
                description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 14), category=CATEGORIES[1],
                event_type_id=4),
            # event_id 4
            Event(title='Выставка современного искусства «Компот»',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 14), category=CATEGORIES[1],
                  event_type_id=4),
            # event_id 5
            Event(title='Мастер-классы по эстрадному вокалу',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 15), category=CATEGORIES[2],
                  club_type_id=1, teacher_id=1),
            # event_id 6
            Event(title='ИЗО',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 13), category=CATEGORIES[2],
                  club_type_id=3, teacher_id=2),
            # event_id 7
            Event(title='Гитара',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 14), category=CATEGORIES[2],
                  club_type_id=1, teacher_id=3),
            # event_id 8
            Event(title='Хореография',
                  description='Очень крутое событие приходите!!!', date=datetime(2023, 12, 20), category=CATEGORIES[2],
                  club_type_id=4, teacher_id=4),

            JobType(name='Уборка'),
            JobType(name='Установка экспонатов'),
            JobType(name='Настройка оборудования'),
            JobType(name='Настройка освещения'),
            # room_id 1
            Room(name='Концертный зал'),
            # room_id 2
            Room(name='Выставочный зал', half_reservation=True),
            # room_id 3
            Room(name='Театральная сцена'),
            # room_id 4
            Room(name='Звукозаписывающая студия', half_reservation=True),
            # room_id 5
            Room(name='Студия Арт-мастерства', half_reservation=True),

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
        # 2 выставки смежная резервация
        datetimes_list = []
        start_date_time = datetime(2023, 12, 10, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(9)])
        start_date_time = datetime(2023, 12, 11, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(9)])
        start_date_time = datetime(2023, 12, 12, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(9)])
        reservation_service.create(room_id=2, event_id=3, intervals=datetimes_list, half_reservation=True)
        reservation_service.create(room_id=2, event_id=1, intervals=datetimes_list, half_reservation=True)

        # Спектакль полная регистрация
        datetimes_list = []

        start_date_time = datetime(2023, 12, 10, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(5)])
        reservation_service.create(room_id=3, event_id=2, intervals=datetimes_list, half_reservation=False)

        # выставка частичная регистрация
        datetimes_list = []

        start_date_time = datetime(2023, 12, 15, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(5)])
        reservation_service.create(room_id=2, event_id=4, intervals=datetimes_list, half_reservation=False)

        # 1 кружок
        STORAGE['club_start_datetime'] = datetime(2023, 12, 15)
        datetimes_list = []

        start_date_time = datetime(2023, 12, 11, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(3)])
        start_date_time = datetime(2023, 12, 13, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(3)])
        start_date_time = datetime(2023, 12, 15, 9, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(3)])
        reservation_service.create(room_id=4, event_id=5, intervals=datetimes_list, half_reservation=False, club=True)

        # 2 кружок ИЗО
        STORAGE['club_start_datetime'] = datetime(2023, 12, 13)
        datetimes_list = []

        start_date_time = datetime(2023, 12, 12, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        start_date_time = datetime(2023, 12, 15, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        start_date_time = datetime(2023, 12, 17, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        reservation_service.create(room_id=5, event_id=6, intervals=datetimes_list, half_reservation=False, club=True)

        # 3 кружок ГИТАРА
        STORAGE['club_start_datetime'] = datetime(2023, 12, 14)
        datetimes_list = []

        start_date_time = datetime(2023, 12, 12, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        start_date_time = datetime(2023, 12, 14, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        reservation_service.create(room_id=4, event_id=7, intervals=datetimes_list, half_reservation=False, club=True)

        # 4 кружок ХОРЕОГРАФИЯ
        STORAGE['club_start_datetime'] = datetime(2023, 12, 20)
        datetimes_list = []

        start_date_time = datetime(2023, 12, 12, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        start_date_time = datetime(2023, 12, 14, 10, 0, 0)
        datetimes_list.extend([start_date_time + timedelta(hours=i) for i in range(2)])
        reservation_service.create(room_id=3, event_id=8, intervals=datetimes_list, half_reservation=False, club=True)

        #
        STORAGE.pop('club_start_datetime')
        session.commit()
