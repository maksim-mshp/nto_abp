import flet as ft
from services.event import event_service
from components.modals.manage import ManageModal


class ClubsTypeModal(ManageModal):
    def __init__(self, page: ft.Page, close_event):
        super().__init__(page, close_event)
        self.title = 'Управление видами кружков'
        self.objects = event_service.get_clubs_types_with_id()
        super().init()

    @staticmethod
    def check_is_using(id: int) -> bool:
        return event_service.is_club_type_using(id)

    @staticmethod
    def create(title: str) -> dict:
        return event_service.create_club_type(title)

    @staticmethod
    def update(id: int, title: str):
        event_service.update_club_type(id, title)

    @staticmethod
    def delete(id: int):
        event_service.delete_club_type(id)
