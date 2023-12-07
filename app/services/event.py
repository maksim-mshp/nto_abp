from datetime import datetime

from repositories.event import EventRepository
from repositories.event_type import EventTypeRepository
from repositories.club_type import ClubTypeRepository
from repositories.teacher import TeacherRepository

from utils import object_as_dict


class EventService:

    def __init__(self):
        self.event_repository = EventRepository()
        self.event_type_repository = EventTypeRepository()
        self.club_type_repository = ClubTypeRepository()
        self.teacher_repository = TeacherRepository()

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
            category: str,
            description: str = '',
            event_type: str | None = None,
            club_type: str | None = None,
            teacher: str | None = None,
    ) -> dict:
        event = {
            'title': name.strip(),
            'description': description.strip(),
            'date': date,
            'category': category,
            'event_type_id': self.get_event_type_id_by_name(event_type) if event_type else None,
            'club_type_id': self.get_club_type_id_by_name(club_type) if club_type else None,
            'teacher_id': self.get_teacher_id_by_name(teacher) if teacher else None
        }
        event = self.event_repository.create(**event)
        return object_as_dict(event)

    def update_event(
            self,
            event_id: int,
            name: str,
            date: datetime,
            event_type: str,
            club_type: str,
            teacher: str,
            description: str,
            category: str
    ) -> dict:
        event = {
            'title': name.strip(),
            'description': description.strip(),
            'date': date,
            'category': category,
            'event_type_id': self.get_event_type_id_by_name(event_type) if event_type else None,
            'club_type_id': self.get_club_type_id_by_name(club_type) if club_type else None,
            'teacher_id': self.get_teacher_id_by_name(teacher) if teacher else None
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

    def is_event_type_using(self, event_type_id: int) -> bool:
        return self.event_repository.get_list_items_by_filter(event_type_id=event_type_id) != []

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
        data.sort(key=lambda x: x['name'])
        return data

    # ---------- CLUB TYPE ----------

    def is_club_type_using(self, club_type_id: int) -> bool:
        return self.event_repository.get_list_items_by_filter(club_type_id=club_type_id) != []

    def create_club_type(self, name: str) -> dict:
        club_type = self.club_type_repository.create(name=name)
        return object_as_dict(club_type)

    def update_club_type(self, event_id: int, name: str) -> dict:
        club_type = self.club_type_repository.update_by_id(event_id, name=name)
        return object_as_dict(club_type)

    def delete_club_type(self, event_id: int) -> None:
        self.club_type_repository.delete_by_id(event_id)

    def get_club_type_id_by_name(self, name: str) -> int:
        filt = {
            'name': name
        }
        data = self.club_type_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)['id']

    def get_clubs_types(self) -> list:
        data = self.club_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_club_type_by_id(self, event_id: int) -> str | None:
        if event_id is None:
            return None
        filt = {
            'id': event_id
        }
        data = self.club_type_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)['name']

    def get_clubs_types_with_id(self) -> list:
        data = self.club_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        data.sort(key=lambda x: x['name'])
        return data

    # ---------- TEACHER ----------

    def create_teacher(self, name: str) -> dict:
        teacher = self.teacher_repository.create(name=name)
        return object_as_dict(teacher)

    def update_teacher(self, teacher_id: int, name: str = None) -> dict:
        filt = {}
        if name:
            filt['name'] = name

        teacher = self.teacher_repository.update_by_id(teacher_id, **filt)
        return object_as_dict(teacher)

    def delete_teacher(self, teacher_id: int) -> None:
        self.teacher_repository.delete_by_id(teacher_id)

    def is_teacher_using(self, teacher_id: int) -> bool:
        return self.event_repository.get_list_items_by_filter(teacher_id=teacher_id) != []

    def get_teacher_by_name(self, name: str) -> dict:
        teacher = self.teacher_repository.get_item_by_filter(name=name)
        return object_as_dict(teacher)

    def get_teacher_by_id(self, teacher_id: int) -> dict:
        teacher = self.teacher_repository.get_item_by_filter(id=teacher_id)
        return object_as_dict(teacher)

    def get_teachers(self) -> list[str]:
        data = self.teacher_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_teacher_id_by_name(self, name: str) -> int:
        filt = {
            'name': name
        }
        data = self.teacher_repository.get_list_items_by_filter(**filt)[0]
        return object_as_dict(data)['id']

    def get_teachers_with_id(self) -> list[dict]:
        data = self.teacher_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        data.sort(key=lambda x: x['name'])
        return data


event_service = EventService()
