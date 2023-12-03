from datetime import datetime

import flet as ft
import utils

from components.tables.reservation_table import ReservationTable
from utils import STORAGE, DEFAULT_BTN_STYLE


class Reservation:
    VIEW_TITLE: str = "Бронирование"
    NAVBAR_HIDDEN: bool = True

    def __init__(self, page: ft.Page):
        self.page = page
        self.component = ft.Column(controls=[], expand=1, alignment=ft.MainAxisAlignment.CENTER)
        self.half_reservation = STORAGE.get('half_reservation', False)
        self.room_id = STORAGE.get('room_id', 1)

        table = ft.Row([ReservationTable(
            date_time=datetime.now(), room_id=self.room_id, tile_width=90, tile_height=27, days_count=7,
            half_reservation=self.half_reservation, editable=True)], alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER)

        btn_row = ft.Row([
            ft.TextButton("Отмена",
                          style=DEFAULT_BTN_STYLE),
            ft.TextButton("Ок",
                          style=DEFAULT_BTN_STYLE)
        ], alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self.component.controls.append(table)

        self.component.controls.append(btn_row)

        self.hide()

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass

    def safe_remove(self, obj):
        try:
            self.component.controls.remove(obj)
        except ValueError:
            pass

    def hide(self):
        self.component.visible = False
        self.safe_update()

    def show(self):
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()

    @staticmethod
    def go_back_handler(e=None):
        utils.on_page_change_func(new_index=0)
