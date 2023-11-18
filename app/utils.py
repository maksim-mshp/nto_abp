import os
from datetime import datetime

from sqlalchemy import inspect

from core.database import create_database

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository
from repositories.job import JobRepository
from repositories.job_type import JobTypeRepository
from repositories.job_room import JobRoomRepository

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def add_sample_data():
    if os.path.exists('../sqlite.db'):
        create_database()
        return
    create_database()

    # -------- Виды мероприятий ----------
    events_type = ['Cпектакль', 'Концерт', 'Репетиция', 'Выставка', 'Мастер-класс']
    for event_type in events_type:
        EventTypeRepository().create(name=event_type)
    # -------- Мероприятия ----------
    events = [
        {
            'title': 'Выставка «Архитектура и мода. В потоке времени»',
            'description': 'Очень круто событие приходите!!!',
            'date': datetime(2023, 11, 18),
            'category': 'Просвещение',
            'event_type_id': 4
        },
        {
            'title': 'Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
            'description': 'Очень круто событие приходите!!!',
            'date': datetime(2023, 11, 25),
            'category': 'Образовние',
            'event_type_id': 5
        },
        {
            'title': 'Спектакль-концерт в рамках проекта «П» в кубе: «Неделя просвещения»',
            'description': 'Очень круто событие приходите!!!',
            'date': datetime(2023, 11, 19),
            'category': 'Образовние',
            'event_type_id': 5
        },
    ]
    for event in events:
        EventRepository().create(**event)
    # -------- Помещения ----------
    jobs_room = ['Концертный зал', 'Выставочный зал', 'Театральная сцена', 'Звукозаписывающая студия']
    for room in jobs_room:
        JobRoomRepository().create(name=room)
    # -------- Виды работ ----------
    jobs_type = ['Уборка', 'Установка экспонатов', 'Настройка оборудования', 'Настройка освещения']
    for room in jobs_type:
        JobTypeRepository().create(name=room)
    # -------- Работы ----------
    jobs = [
        {
            'title': 'Подготовка и установка экспонатов в выставочном зале',
            'description': '',
            'event_id': 1,
            'job_type_id': 2,
            'job_room_id': 2,
            'deadline': datetime(2023, 11, 25),
            'status': 'Создано'
        },
        {
            'title': 'Настройка освещения в концертном зале',
            'description': '',
            'event_id': 3,
            'job_type_id': 4,
            'job_room_id': 1,
            'deadline': datetime(2023, 11, 25),
            'status': 'Создано'
        },
        {
            'title': 'Настройка освещения в выставочном зале',
            'description': '',
            'event_id': 1,
            'job_type_id': 4,
            'job_room_id': 2,
            'deadline': datetime(2023, 11, 25),
            'status': 'К работе'
        },
        {
            'title': 'Настройка звукозаписывающего оборудования в концертном зале',
            'description': '',
            'event_id': 3,
            'job_type_id': 3,
            'job_room_id': 1,
            'deadline': datetime(2023, 11, 25),
            'status': 'К работе'
        },
        {
            'title': 'Уборка выставочного зала',
            'description': '',
            'event_id': 1,
            'job_type_id': 1,
            'job_room_id': 2,
            'deadline': datetime(2023, 11, 25),
            'status': 'Выполнено'
        },
        {
            'title': 'Уборка концертного зала',
            'description': '',
            'event_id': 3,
            'job_type_id': 1,
            'job_room_id': 1,
            'deadline': datetime(2023, 11, 25),
            'status': 'Выполнено'
        }
    ]
    for job in jobs:
        JobRepository().create(**job)


def get_types():
    result = EventTypeRepository().get_list_items_by_filter()
    return [object_as_dict(i) for i in result]
