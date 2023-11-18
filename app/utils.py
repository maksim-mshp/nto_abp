import os
import flet as ft
from datetime import datetime

from sqlalchemy import inspect

from core.config import config
from core.database import create_database

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository
from repositories.job import JobRepository
from repositories.job_type import JobTypeRepository
from repositories.job_room import JobRoomRepository

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']

DEFAULT_BTN_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=10),
    padding=15
)


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def add_sample_data():
    if os.path.exists(f'../{config.DATABASE_NAME}'):
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
            'description': 'Очень крутое событие приходите!!!',
            'date': datetime(2023, 11, 18),
            'category': CATEGORIES[1],
            'event_type_id': 4
        },
        {
            'title': 'Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
            'description': 'Очень крутое событие приходите!!!',
            'date': datetime(2023, 11, 25),
            'category': CATEGORIES[2],
            'event_type_id': 5
        },
        {
            'title': 'Спектакль-концерт в рамках проекта «П» в кубе: «Неделя просвещения»',
            'description': 'Очень круто событие приходите!!!',
            'date': datetime(2023, 11, 19),
            'category': CATEGORIES[1],
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


def get_types() -> list:
    data = EventTypeRepository().get_list_items_by_filter()
    return [object_as_dict(i)['name'] for i in data]


def get_formatted_date(date: datetime) -> str:
    return date.strftime('%d.%m.%Y')


def get_type_by_id(id: int):
    if id is None:
        return None
    filt = {
        'id': id
    }
    data = EventTypeRepository().get_list_items_by_filter(**filt)[0]
    return object_as_dict(data)['name']


def get_event_by_id(id: int) -> dict:
    filt = {
        'id': id
    }
    data = EventRepository().get_list_items_by_filter(**filt)[0]
    return object_as_dict(data)


def get_type_id_by_name(name: str) -> int:
    filt = {
        'name': name
    }
    data = EventTypeRepository().get_list_items_by_filter(**filt)[0]
    return object_as_dict(data)['id']


def get_events(category):
    filt = {
        'category': category
    }
    result = EventRepository().get_list_items_by_filter(**filt)
    return [object_as_dict(i) for i in result]


def create_event(name: str, date: datetime, event_type: str, description: str, category: str):
    event = {
        'title': name.strip(),
        'description': description.strip(),
        'date': date,
        'category': category,
        'event_type_id': get_type_id_by_name(event_type) if event_type else None
    }

    EventRepository().create(**event)


def update_event(id: int, name: str, date: datetime, event_type: str, description: str, category: str):
    event = {
        'title': name.strip(),
        'description': description.strip(),
        'date': date,
        'category': category,
        'event_type_id': get_type_id_by_name(event_type)
    }

    EventRepository().update_by_id(id, **event)


def is_type_using(id: int) -> bool:
    return EventRepository().get_list_items_by_filter(event_type_id=id) != []


if __name__ == '__main__':
    print(get_event_by_id(1))
