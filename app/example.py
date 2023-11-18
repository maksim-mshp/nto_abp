from datetime import datetime

from repositories.event_type import EventTypeRepository
from repositories.event import EventRepository

from utils import object_as_dict
from core.database import add_sample_data

add_sample_data()


def example():
    sample_type = {
        'name': 'Выставка'
    }

    result_event_type = EventTypeRepository().create(**sample_type)
    print(result_event_type.id)
    print(object_as_dict(result_event_type))
    sample_event = {
        'title': 'Название',
        'description': 'описание',
        'date': datetime.now(),
        'category': 'просвещение',
        'event_type_id': result_event_type.id
    }
    # создание мероприятия
    result_event = EventRepository().create(**sample_event)
    print(object_as_dict(result_event))

    # получение списка мероприятий
    result = EventRepository().get_list_items_by_filter()
    print(result)

    # редактирование мероприятия
    update_data = {
        'description': 'описание123'
    }
    result = EventRepository().update_by_id(result_event.id, **update_data)
    print(object_as_dict(result))

    result = EventRepository().get_list_items_by_filter()
    print(result)

    # удаление мероприятия
    result = EventRepository().delete_by_id(result_event.id)
    result = EventRepository().get_list_items_by_filter()
    print(result)
