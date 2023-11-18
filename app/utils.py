from datetime import datetime

from sqlalchemy import inspect

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository
import os
from core.config import config

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def add_sample_data():
    if EventTypeRepository().get_list_items_by_filter():
        return
    # -------- Виды мероприятий ----------
    events_type = ['Cпектакль', 'Концерт', 'Репетиция', 'Выставка', 'Мастер-класс']
    for event_type in events_type:
        EventTypeRepository().create(name=event_type)
    # -------- Мероприятия ----------
    events = [
        {
            'description': 'Выставка «Архитектура и мода. В потоке времени»',
            'date': datetime(2023, 11, 18),
            'category': CATEGORIES[1],
            'event_type_id': 4
        },
        {
            'description': 'Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
            'date': datetime(2023, 11, 25),
            'category': CATEGORIES[2],
            'event_type_id': 5
        }
    ]
    for event in events:
        EventRepository().create(**event)


def get_types() -> dict:
    data = EventTypeRepository().get_list_items_by_filter()
    result = {}
    for i in data:
        t = object_as_dict(i)
        result[t['name']] = t['id']
    return result


def get_events():
    result = EventRepository().get_list_items_by_filter()
    return [object_as_dict(i) for i in result]


def create_event(name: str, date: datetime, event_type: str, description: str, category: str):
    event = {
        'name': name.strip(),
        'description': description.strip(),
        'date': date,
        'category': category,
        'event_type_id': get_types()[event_type]
    }

    EventRepository().create(**event)


if __name__ == '__main__':
    print(get_types())
