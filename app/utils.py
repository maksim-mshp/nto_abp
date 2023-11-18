from datetime import datetime

from sqlalchemy import inspect

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def add_sample_data():
    # -------- Виды мероприятий ----------
    events_type = ['Cпектакль', 'Концерт', 'Репетиция', 'Выставка', 'Мастер-класс']
    for event_type in events_type:
        EventTypeRepository().create(name=event_type)
    # -------- Мероприятия ----------
    events = [
        {
            'description': 'Выставка «Архитектура и мода. В потоке времени»',
            'date': datetime(2023, 11, 18),
            'category': 'Просвещение',
            'event_type_id': 4
        },
        {
            'description': 'Мастер-классы по эстрадному вокалу «Мне нужно петь» в ноябре',
            'date': datetime(2023, 11, 25),
            'category': 'Образовние',
            'event_type_id': 5
        }
    ]
    for event in events:
        EventRepository().create(**event)


def get_types():
    return ['спектакль', 'концерт']
