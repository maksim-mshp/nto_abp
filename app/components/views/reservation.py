from app.components.views.rooms import Rooms
import flet as ft
import utils


class Reservation(Rooms):
    VIEW_TITLE: str = "НОВАЯ ВЬЮШКА"
    NAVBAR_HIDDEN: bool = True

    def __init__(self, page: ft.Page):
        super().__init__(page)

    @staticmethod
    def go_back_handler(e=None):
        utils.on_page_change_func(new_index=0)
