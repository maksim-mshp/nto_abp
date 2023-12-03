from datetime import datetime

import flet as ft

from services.room import room_service
from components.tables.reservation_table import ReservationTable


class Rooms:
    VIEW_TITLE: str = "Бронирование помещений"
    VIEW_ICON = ft.icons.MEETING_ROOM
    NAVBAR_HIDDEN: bool = False

    def __init__(self, page: ft.Page):
        self.page = page
        self.component = ft.Column(controls=[], expand=1)

        rooms = room_service.get_rooms_with_id()
        self.room_selector = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in rooms],
            label='Помещение',
            on_change=self.on_change,
            dense=True,
            value=rooms[0]['id'],
        )
        self.component.controls.append(self.room_selector)

        self.reservation_table = ReservationTable(
            date_time=datetime.now(), room_id=rooms[0]['id'], tile_width=90, tile_height=27, days_count=7, half_reservation=False, editable=True)
        self.component.controls.append(self.reservation_table)

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

    def on_change(self, e):
        self.reservation_table.reset(e.control.value)
