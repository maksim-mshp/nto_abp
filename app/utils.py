from sqlalchemy import inspect

from repositories.event_type import EventTypeRepository

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def get_types():
    result = EventTypeRepository().get_list_items_by_filter()
    return [object_as_dict(i) for i in result]
