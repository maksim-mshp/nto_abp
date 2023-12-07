from datetime import datetime

import flet as ft
import utils

from components.tables.club_reservation_table import ReservationTable
from utils import STORAGE, DEFAULT_BTN_STYLE


class ClubReservation:
    VIEW_TITLE: str = "Бронирование помещения"
    NAVBAR_HIDDEN: bool = True

    def __init__(self, page: ft.Page):
        self.page = page
        self.component = ft.Column(controls=[], expand=1, alignment=ft.MainAxisAlignment.CENTER)
        self.half_reservation = STORAGE.get('half_reservation', False)
        self.room_id = STORAGE.get('room_id', 1)

        self.table = ft.Row([ReservationTable(
            date_time=datetime.now(), room_id=self.room_id, tile_width=90, tile_height=27, days_count=7,
            half_reservation=self.half_reservation, editable=True)], alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER)

        btn_row = ft.Row([
            ft.TextButton("Отмена",
                          style=DEFAULT_BTN_STYLE, on_click=self.cancel_handler),
            ft.TextButton("Ок",
                          style=DEFAULT_BTN_STYLE, on_click=self.save_handler)
        ], alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self.component.controls.append(self.table)

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
        self.table.controls[0].reset(STORAGE['room_id'], STORAGE['half_reservation'])
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()

    def cancel_handler(self, e):
        self.go_back()

    @staticmethod
    def go_back():
        STORAGE['from_reservation'] = True
        utils.on_page_change_func(new_index=0)

    def save_handler(self, e=None):
        STORAGE['selected_fields'] = self.table.controls[0].selected_fields.copy()
        self.go_back()
