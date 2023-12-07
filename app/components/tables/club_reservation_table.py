from datetime import datetime, timedelta
from typing import Optional

import flet as ft

from services.reservation import reservation_service
from utils import STORAGE

SELECTED_COLOR = ft.colors.LIGHT_BLUE
BOOKED_COLOR = ft.colors.GREY
NONE_COLOR = ft.colors.WHITE

WEEKDAYS = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПН', 'СБ', 'ВС']
WEEKDAYS2 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


class TimeTile(ft.UserControl):
    def __init__(self, date_time: datetime, tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.date_time = date_time
        self.tile_width = tile_width
        self.tile_height = tile_height

    def build(self):
        return ft.Container(
            content=ft.Text(
                size=14,
                value=f"{self.date_time.strftime('%H:%M')}-{(self.date_time + timedelta(hours=1)).strftime('%H:%M')}"),
            width=self.tile_width,
            height=self.tile_height,
            bgcolor=ft.colors.WHITE,
        )


class DateTile(ft.UserControl):
    def __init__(self, date_time: datetime, tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.date_time = date_time
        self.tile_width = tile_width
        self.tile_height = tile_height

    def build(self):
        return ft.Container(
            content=ft.Text(
                value=f"{WEEKDAYS[self.date_time.weekday()]}",
                size=14,
                text_align=ft.TextAlign.CENTER),
            width=self.tile_width,
            height=self.tile_height,
            bgcolor=ft.colors.AMBER,
            alignment=ft.alignment.center,
        )


class ReservationContainer(ft.UserControl):
    def __init__(self, is_booked: bool = False, is_selected: bool = False, half_reservation: bool = False,
                 message: str = " ",
                 tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.is_booked = is_booked
        self.is_selected = is_selected
        self.half_reservation = half_reservation
        self.tile_width = tile_width
        if half_reservation:
            self.tile_width //= 2
        self.tile_height = tile_height
        self.color = NONE_COLOR
        self.message = message

    def build(self):
        if self.is_booked:
            self.color = BOOKED_COLOR
            return ft.Tooltip(
                message=self.message,
                vertical_offset=20,
                content=ft.Container(
                    width=self.tile_width,
                    height=self.tile_height,
                    bgcolor=self.color,
                )
            )
        elif self.is_selected:
            self.color = SELECTED_COLOR
        return ft.Container(
            width=self.tile_width,
            height=self.tile_height,
            bgcolor=self.color,
        )


class ReservationTile(ft.UserControl):
    def __init__(self, date_time: datetime, selected_fields: list[datetime], reservation_tile_click,
                 booked_fields: list[dict], half_reservation: bool = False,
                 tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.date_time = date_time
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.selected_fields = selected_fields
        self.reservation_tile_click = reservation_tile_click
        self.booked_fields = booked_fields
        self.half_reservation = half_reservation

    def build(self):
        container = ft.Container(
            height=self.tile_height,
            width=self.tile_width,
            border=ft.border.all(0.2, ft.colors.BLACK),
            data=self.date_time,
            on_click=self.reservation_tile_click,
        )
        row = ft.Row(spacing=0)
        if self.booked_fields:
            for field in self.booked_fields:
                if field['start_date_time'] == self.date_time and field['reservation']['event_id'] != STORAGE.get(
                        'event_id', None):
                    message = field['reservation']['event']
                    if field['reservation']['half_reservation']:
                        row.controls.append(
                            ReservationContainer(is_booked=True, half_reservation=True, message=message,
                                                 tile_width=self.tile_width,
                                                 tile_height=self.tile_height)
                        )
                    else:
                        row.controls.append(
                            ReservationContainer(is_booked=True, half_reservation=False, message=message,
                                                 tile_width=self.tile_width,
                                                 tile_height=self.tile_height)
                        )
        if self.date_time in self.selected_fields:
            row.controls.append(
                ReservationContainer(is_selected=True, half_reservation=self.half_reservation,
                                     tile_width=self.tile_width,
                                     tile_height=self.tile_height)
            )
        container.content = row
        return container


class TimeColumn(ft.UserControl):
    def __init__(self, date_time: datetime, tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.date_time = date_time
        self.tile_width = tile_width
        self.tile_height = tile_height

    def build(self):
        time_column = ft.Column(spacing=0)
        time_column.controls.append(
            ft.Container(
                width=self.tile_width,
                height=50,
                bgcolor=ft.colors.WHITE
            )
        )
        for i in range(24):
            time_column.controls.append(
                TimeTile(self.date_time, self.tile_width, self.tile_height)
            )
            self.date_time += timedelta(hours=1)
        return time_column


class ReservationColumn(ft.UserControl):
    def __init__(self, date_time: datetime, selected_fields: list[datetime], reservation_tile_click, room_id: int,
                 half_reservation: bool = False,
                 tile_width: int = 100, tile_height: int = 20):
        super().__init__()
        self.date_time = date_time
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.selected_fields = selected_fields
        self.reservation_tile_click = reservation_tile_click
        self.room_id = room_id
        self.booked_fields = self.get_booked_fields()
        self.half_reservation = half_reservation

    def build(self):
        column = ft.Column(spacing=0)
        column.controls.append(
            DateTile(self.date_time, self.tile_width, 50)  # TODO: ВЫНЕСТИ КУДА ТО РАЗМЕР ВЕРХНЕЙ СТРОЧКИ
        )
        for i in range(24):
            column.controls.append(
                ReservationTile(self.date_time, self.selected_fields, self.reservation_tile_click, self.booked_fields,
                                self.half_reservation,
                                self.tile_width,
                                self.tile_height)
            )
            self.date_time += timedelta(hours=1)

        return column

    def get_booked_fields(self):
        booked_fields = reservation_service.get_time_intervals_by_and_room(self.room_id)
        column_booked = []
        for field in booked_fields:
            if field['weekday'] == self.date_time.weekday():
                date_time = field['start_date_time']
                date_time = date_time.replace(year=self.date_time.year, month=self.date_time.month, day=self.date_time.day)
                field['start_date_time'] = date_time
                if field not in column_booked:
                    column_booked.append(field)
        return column_booked


class ReservationTable(ft.UserControl):
    def __init__(self, date_time: datetime, room_id: int, editable: bool = False, days_count: int = 5,
                 half_reservation: bool = False,
                 tile_width: int = 100,
                 tile_height: int = 20):
        super().__init__()
        date_time = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        self.start_date_time = date_time - timedelta(days=date_time.weekday()-1)
        self.date_time = date_time - timedelta(days=date_time.weekday()-1)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.main_row = ft.Row(spacing=0, alignment=ft.alignment.top_center,
                               vertical_alignment=ft.CrossAxisAlignment.START)
        self.selected_fields = STORAGE.get('selected_fields', []).copy()
        self.room_id = room_id
        self.editable = editable
        self.days_count = days_count
        self.half_reservation = half_reservation

    def build(self):
        self.main_row.controls.append(TimeColumn(self.date_time, self.tile_width, self.tile_height))

        for i in range(self.days_count):
            self.main_row.controls.append(
                ReservationColumn(self.date_time, self.selected_fields, self.reservation_tile_click, self.room_id,
                                  self.half_reservation,
                                  self.tile_width, self.tile_height)
            )
            self.date_time += timedelta(days=1)

        return self.main_row

    def reservation_tile_click(self, e):
        if self.editable:
            if self.half_reservation:
                if len(e.control.content.controls) == 0:
                    e.control.content.controls.append(
                        ReservationContainer(is_selected=True, half_reservation=True, tile_width=self.tile_width,
                                             tile_height=self.tile_height))
                    self.selected_fields.append(e.control.data)
                elif len(e.control.content.controls) == 1:
                    if e.control.content.controls[0].color == SELECTED_COLOR:
                        e.control.content.controls.pop()
                        self.selected_fields.remove(e.control.data)
                    elif e.control.content.controls[0].color == BOOKED_COLOR:
                        e.control.content.controls.append(
                            ReservationContainer(is_selected=True, half_reservation=True, tile_width=self.tile_width,
                                                 tile_height=self.tile_height))
                        self.selected_fields.append(e.control.data)
                elif len(e.control.content.controls) == 2:
                    if e.control.content.controls[1].color == SELECTED_COLOR:
                        e.control.content.controls.pop()
                        self.selected_fields.remove(e.control.data)
            else:
                if len(e.control.content.controls) == 0:
                    e.control.content.controls.append(
                        ReservationContainer(is_selected=True, half_reservation=False, tile_width=self.tile_width,
                                             tile_height=self.tile_height))
                    self.selected_fields.append(e.control.data)
                elif len(e.control.content.controls) == 1:
                    if e.control.content.controls[0].color == SELECTED_COLOR:
                        e.control.content.controls.pop()
                        self.selected_fields.remove(e.control.data)
            print(self.selected_fields)
            e.control.update()

    def reset(self, new_room_id: Optional[int] = None, half_reservation: bool = None):
        if new_room_id:
            self.room_id = new_room_id
        if half_reservation is not None:
            self.half_reservation = half_reservation

        self.selected_fields = STORAGE.get('selected_fields', []).copy()
        self.date_time = self.start_date_time
        for i in range(1, self.days_count + 1):
            self.main_row.controls[i] = ReservationColumn(self.date_time + timedelta(days=i - 2), self.selected_fields,
                                                          self.reservation_tile_click, self.room_id,
                                                          self.half_reservation,
                                                          self.tile_width,
                                                          self.tile_height)

        self.update()
