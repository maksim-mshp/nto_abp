from datetime import datetime
from typing import Any

from repositories.job import JobRepository
from repositories.job_type import JobTypeRepository
from repositories.room import RoomRepository

from utils import object_as_dict


class JobService:
    def __init__(self):
        self.job_repository = JobRepository()
        self.job_type_repository = JobTypeRepository()
        self.job_room_repository = RoomRepository()

    # -------- JOB ROOM --------

    def create_job_room(self, name: str) -> dict:
        job_room = self.job_room_repository.create(name=name)
        return object_as_dict(job_room)

    def update_job_room(self, room_id: int, name: str) -> dict:
        job_room = self.job_room_repository.update_by_id(room_id, name=name)
        return object_as_dict(job_room)

    def delete_job_room(self, room_id: int) -> None:
        self.job_room_repository.delete_by_id(room_id)

    def is_job_room_using(self, room_id: int) -> bool:
        return self.job_repository.get_list_items_by_filter(job_room_id=room_id) != []

    def get_job_room_by_name(self, name: str) -> dict:
        job_room = self.job_room_repository.get_item_by_filter(name=name)
        return object_as_dict(job_room)

    def get_job_room_by_id(self, room_id: int) -> dict:
        job_room = self.job_room_repository.get_item_by_filter(id=room_id)
        return object_as_dict(job_room)

    def get_jobs_rooms(self) -> list[str]:
        data = self.job_room_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_jobs_rooms_with_id(self) -> list[dict]:
        data = self.job_room_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        data.sort(key=lambda x: x['name'])
        return data

    # -------- JOB TYPE --------

    def create_job_type(self, name: str) -> dict:
        job_type = self.job_type_repository.create(name=name)
        return object_as_dict(job_type)

    def update_job_type(self, room_id: int, name: str) -> dict:
        job_type = self.job_type_repository.update_by_id(room_id, name=name)
        return object_as_dict(job_type)

    def delete_job_type(self, room_id: int) -> None:
        self.job_type_repository.delete_by_id(room_id)

    def is_job_type_using(self, room_id: int) -> bool:
        return self.job_repository.get_list_items_by_filter(job_type_id=room_id) != []

    def get_job_type_by_name(self, name: str) -> dict:
        job_type = self.job_type_repository.get_item_by_filter(name=name)
        return object_as_dict(job_type)

    def get_job_type_by_id(self, job_type_id: int) -> dict | None:
        if job_type_id is None:
            return None
        data = self.job_type_repository.get_item_by_filter(id=job_type_id)
        return object_as_dict(data)['name']

    def get_jobs_types(self) -> list[str]:
        data = self.job_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_jobs_types_with_id(self) -> list[dict]:
        data = self.job_type_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        data.sort(key=lambda x: x['name'])
        return data

    # -------- JOB --------

    def create_job(
            self,
            title: str,
            description: str,
            event_id: int,
            job_type_id: int,
            job_room_id: int,
            deadline: datetime,
            status: str,
    ) -> dict:
        job = {
            'title': title.strip(),
            'description': description.strip(),
            'event_id': event_id,
            'job_type_id': job_type_id,
            'job_room_id': job_room_id,
            'deadline': deadline,
            'status': status,
        }
        job = self.job_repository.create(**job)
        return object_as_dict(job)

    def update_job(
            self,
            job_id: int,
            title: str,
            description: str,
            event_id: int,
            job_type_id: int,
            job_room_id: int,
            deadline: datetime,
            status: str,
    ) -> dict:
        job = {
            'title': title.strip(),
            'description': description.strip(),
            'event_id': event_id,
            'job_type_id': job_type_id,
            'job_room_id': job_room_id,
            'deadline': deadline,
            'status': status,
        }
        job = self.job_repository.update_by_id(job_id, **job)
        return object_as_dict(job)

    def delete_job(self, job_id: int) -> None:
        self.job_repository.delete_by_id(job_id)

    def get_job_by_id(self, job_id: int) -> dict:
        job = self.job_repository.get_item_by_filter(id=job_id)
        return object_as_dict(job)

    def get_jobs(self, **filters) -> list:
        result = self.job_repository.get_list_items_by_filter(**filters)
        return [object_as_dict(i) for i in result]

    def change_job_status(self, job_id: int, status: str):
        job = self.job_repository.update_by_id(job_id, status=status)
        return object_as_dict(job)


job_service = JobService()
