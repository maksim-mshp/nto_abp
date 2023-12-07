import flet as ft
from services.event import event_service
from components.modals.manage import ManageModal


class TeachersModal(ManageModal):
    def __init__(self, page: ft.Page, close_event):
        super().__init__(page, close_event)
        self.title = 'Управление преподавателями'
        self.objects = event_service.get_teachers_with_id()
        super().init()

    @staticmethod
    def check_is_using(id: int) -> bool:
        return event_service.is_teacher_using(id)

    @staticmethod
    def create(title: str) -> dict:
        return event_service.create_teacher(title)

    @staticmethod
    def update(id: int, title: str):
        event_service.update_teacher(id, title)

    @staticmethod
    def delete(id: int):
        event_service.delete_teacher(id)
