import flet as ft
from services.event import event_service
from components.modals.manage import ManageModal


class EventTypeModal(ManageModal):
    def __init__(self, page: ft.Page, close_event):
        super().__init__(page, close_event)
        self.title = 'Управление видами мероприятий'
        self.objects = event_service.get_events_types_with_id()
        super().init()

    @staticmethod
    def check_is_using(id: int) -> bool:
        return event_service.is_event_type_using(id)

    @staticmethod
    def create(title: str) -> dict:
        return event_service.create_event_type(title)

    @staticmethod
    def update(id: int, title: str):
        event_service.update_event_type(id, title)

    @staticmethod
    def delete(id: int):
        event_service.delete_event_type(id)
