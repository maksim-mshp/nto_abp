import os
from datetime import datetime

from sqlalchemy import inspect

from core.database import create_database

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository

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
        }
    ]
    for event in events:
        EventRepository().create(**event)


def get_types():
    result = EventTypeRepository().get_list_items_by_filter()
    return [object_as_dict(i) for i in result]
