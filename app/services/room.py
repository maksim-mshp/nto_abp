from repositories.job import JobRepository
from repositories.room import RoomRepository

from utils import object_as_dict


class RoomService:
    def __init__(self):
        self.job_repository = JobRepository()
        self.room_repository = RoomRepository()

    # -------- JOB ROOM --------

    def create_room(self, name: str) -> dict:
        job_room = self.room_repository.create(name=name)
        return object_as_dict(job_room)

    def update_room(self, room_id: int, name: str = None, half_reservation: bool = None) -> dict:
        filt = {}
        if name:
            filt['name'] = name
        if half_reservation:
            filt['half_reservation'] = half_reservation

        job_room = self.room_repository.update_by_id(room_id, **filt)
        return object_as_dict(job_room)

    def delete_job_room(self, room_id: int) -> None:
        self.room_repository.delete_by_id(room_id)

    def is_room_using(self, room_id: int) -> bool:
        return self.job_repository.get_list_items_by_filter(job_room_id=room_id) != []

    def get_room_by_name(self, name: str) -> dict:
        job_room = self.room_repository.get_item_by_filter(name=name)
        return object_as_dict(job_room)

    def get_room_by_id(self, room_id: int) -> dict:
        job_room = self.room_repository.get_item_by_filter(id=room_id)
        return object_as_dict(job_room)

    def get_rooms(self) -> list[str]:
        data = self.room_repository.get_list_items_by_filter()
        data = [object_as_dict(i)['name'] for i in data]
        data.sort()
        return data

    def get_rooms_with_id(self) -> list[dict]:
        data = self.room_repository.get_list_items_by_filter()
        data = [object_as_dict(i) for i in data]
        data.sort(key=lambda x: x['name'])
        return data


room_service = RoomService()
