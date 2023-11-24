from datetime import datetime

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository

from utils import object_as_dict


class EventService:

    def __init__(self):
        self.event_repository = EventRepository()
        self.event_type_repository = EventTypeRepository()

    # ---------- EVENTS ----------

    def get_event_by_id(self, event_id: int) -> dict:
        filt = {
            'id': event_id
        }
        data = self.event_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)

    def create_event(
            self,
            name: str,
            date: datetime,
            event_type: str,
            description: str,
            category: str
    ) -> dict:
        event = {
            'title': name.strip(),
            'description': description.strip(),
            'date': date,
            'category': category,
            'event_type_id': self.get_event_type_id_by_name(event_type) if event_type else None
        }
        event = self.event_repository.create(**event)
        return object_as_dict(event)

    def update_event(
            self,
            event_id: int,
            name: str,
            date: datetime,
            event_type: str,
            description: str,
            category: str
    ) -> dict:
        event = {
            'title': name.strip(),
            'description': description.strip(),
            'date': date,
            'category': category,
            'event_type_id': self.get_event_type_id_by_name(event_type) if event_type else None
        }
        event = self.event_repository.update_by_id(event_id, **event)
        return object_as_dict(event)

    def delete_event(self, event_id: int) -> None:
        self.event_repository.delete_by_id(event_id)

    def get_events(self, category=None) -> list:
        filt = {
            'category': category
        }
        if category is None:
            result = self.event_repository.get_list_items_by_filter()
        else:
            result = self.event_repository.get_list_items_by_filter(**filt)
        return [object_as_dict(i) for i in result]

    # ---------- EVENT TYPE ----------

    def is_event_type_using(self, event_id: int) -> bool:
        return self.event_repository.get_list_items_by_filter(event_type_id=event_id) != []

    def create_event_type(self, name: str) -> dict:
        event_type = self.event_type_repository.create(name=name)
        return object_as_dict(event_type)

    def update_event_type(self, event_id: int, name: str) -> dict:
        event_type = self.event_type_repository.update_by_id(event_id, name=name)
        return object_as_dict(event_type)

    def delete_event_type(self, event_id: int) -> None:
        self.event_type_repository.delete_by_id(event_id)

    def get_event_type_id_by_name(self, name: str) -> int:
        filt = {
            'name': name
        }
        data = self.event_type_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)['id']

    def get_events_types(self) -> list:
        data = self.event_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_event_type_by_id(self, event_id: int) -> str | None:
        if event_id is None:
            return None
        filt = {
            'id': event_id
        }
        data = self.event_type_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)['name']

    def get_events_types_with_id(self) -> list:
        data = self.event_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        return data


event_service = EventService()
