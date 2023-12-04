import flet as ft
from services.job import job_service
from components.modals.manage import ManageModal
from utils import STORAGE


class JobRoomModal(ManageModal):
    def __init__(self, page: ft.Page, close_event):
        super().__init__(page, close_event)
        self.title = 'Управление помещениями'
        self.objects = job_service.get_jobs_rooms_with_id()
        STORAGE['job_room_modal_checkbox'] = True
        super().init()

    @staticmethod
    def check_is_using(id: int) -> bool:
        return job_service.is_job_room_using(id)

    @staticmethod
    def create(title: str) -> dict:
        return job_service.create_job_room(title)

    @staticmethod
    def update(id: int, title: str):
        job_service.update_job_room(id, title)

    @staticmethod
    def delete(id: int):
        job_service.delete_job_room(id)
