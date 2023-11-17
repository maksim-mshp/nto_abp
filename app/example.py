from datetime import datetime

from core.database import engine
from core.database import Base

from models.event_type import EventType
from models.event import Event
from models.job_type import JobType
from models.job_room import JobRoom
from models.job import Job

from repositories.event_type import EventTypeRepository
from repositories.event import EventRepository

from utils import object_as_dict, add_sample_data


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
add_sample_data()

sample_type = {
    'name': 'Выставка'
}

result_event_type = EventTypeRepository().create(**sample_type)
print(result_event_type.id)
print(object_as_dict(result_event_type))
sample_event = {
    'description': 'описание',
    'date': datetime.now(),
    'category': 'просвещение',
    'event_type_id': result_event_type.id
}
# создание мероприятия
result_event = EventRepository().create(**sample_event)
print(object_as_dict(result_event))

#получение списка мероприятий
result = EventRepository().get_list_items_by_filter()
print(result)

# редактирование мероприятия
update_data = {
    'description': 'описание123'
}
result = EventRepository().update_by_id(3, **update_data)
print(object_as_dict(result))

result = EventRepository().get_list_items_by_filter()
print(result)

# удаление мероприятия
result = EventRepository().delete_by_id(3)
result = EventRepository().get_list_items_by_filter()
print(result)
