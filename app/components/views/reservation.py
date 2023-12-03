from app.components.views.rooms import Rooms
import flet as ft


class Reservation(Rooms):
    VIEW_TITLE: str = "НОВАЯ ВЬЮШКА"
    NAVBAR_HIDDEN: bool = True

    def __init__(self, page: ft.Page):
        super().__init__(page)
