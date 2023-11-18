import os
import flet as ft
from datetime import datetime

from sqlalchemy import inspect

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository

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
