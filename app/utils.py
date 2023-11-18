import os
from datetime import datetime

from sqlalchemy import inspect

from core.database import create_database

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository
from core.config import config

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']


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
        }
    ]
    for event in events:
        EventRepository().create(**event)


def get_types() -> list:
    data = EventTypeRepository().get_list_items_by_filter()
    return [object_as_dict(i)['name'] for i in data]


def get_formatted_date(date: datetime) -> str:
    return date.strftime('%d.%m.%Y')


def get_type_by_id(id: int) -> str:
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


def get_events(category=None):
    if category is None:
        result = EventRepository().get_list_items_by_filter()
    else:
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
        'event_type_id': get_type_id_by_name(event_type)
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


if __name__ == '__main__':
    print(get_event_by_id(1))
