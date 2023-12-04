import flet as ft

import utils
from components.modals.event import EventModal
from components.modals.event_type import EventTypeModal

from services.event import event_service
from services.reservation import reservation_service
from utils import CATEGORIES, get_formatted_date, STORAGE


class Events:
    VIEW_TITLE: str = "Мероприятия"
    VIEW_ICON = ft.icons.EVENT_ROUNDED
    NAVBAR_HIDDEN: bool = False

    def __init__(self, page: ft.Page):
        self.page = page
        self.modal_edit = None
        self.dt = None
        self.component = ft.Column(controls=[], expand=1)
        self.nothing = ft.Container(ft.Text("Ничего не найдено"), width=100000, padding=50,
                                    alignment=ft.alignment.center)

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[ft.Tab(text=x) for x in CATEGORIES],
            on_change=self.on_change,
        )

        self.modal = EventModal(self.page,
                                close_event=self.on_change,
                                category=CATEGORIES[self.tabs.selected_index])

        self.create_btn = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)
        self.page.add(self.create_btn)
        self.component.controls.append(ft.Row(
            [self.tabs, ft.ElevatedButton('Управление видами мероприятий', style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=17
            ), on_click=self.manage_types_clicked)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))
        self.on_change()
        self.hide()

    def show(self):
        self.component.visible = True
        self.create_btn.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()
        self.page.update()
        if STORAGE.get('from_reservation', False):
            self.add_clicked()
            STORAGE['from_reservation'] = False
        if STORAGE.get('event_id', None) is not None:
            self.open_modal(id=STORAGE['event_id'])
            STORAGE['event_id'] = None

    def hide(self):
        self.component.visible = False
        self.create_btn.visible = False
        self.modal.dialog.open = False
        self.safe_update()
        self.page.update()

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass

    def add_clicked(self, e=None):
        """открывает модалку создания"""
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.safe_update()
        self.page.update()

    def manage_types_clicked(self, e):
        self.modal = EventTypeModal(self.page, close_event=self.on_change)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.safe_update()
        self.page.update()

    def open_modal(self, e=None, id=None):
        """открывает модалку редактирования"""
        if e:
            id = e.control.data
        self.modal_edit = EventModal(self.page, close_event=self.on_change, id=id)
        self.page.dialog = self.modal_edit.dialog
        self.modal_edit.open()
        self.safe_update()
        self.page.update()

    def safe_remove(self, obj):
        try:
            self.component.controls.remove(obj)
        except ValueError:
            pass

    def on_change(self, e=None):
        category = CATEGORIES[self.tabs.selected_index]
        events = event_service.get_events(category)
        self.safe_remove(self.dt)
        self.dt = ft.Column([ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название")),
                ft.DataColumn(ft.Text("Дата")),
            ],
            width=100000,
        )], scroll=ft.ScrollMode.ADAPTIVE, expand=1)

        if self.tabs.selected_index != 2:
            self.dt.controls[0].columns.insert(1, ft.DataColumn(ft.Text("Вид")))

        self.dt.controls[0].rows.clear()
        if len(events) > 0:
            self.dt.controls[0].rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(event['title'])),
                        ft.DataCell(ft.Text(get_formatted_date(event['date']))),
                    ]
                    if self.tabs.selected_index == 2 else
                    [
                        ft.DataCell(ft.Text(event['title'])),
                        ft.DataCell(ft.Text(event_service.get_event_type_by_id(event['event_type_id']))),
                        ft.DataCell(ft.Text(get_formatted_date(event['date']))),
                    ],
                    on_select_changed=self.open_modal,
                    data=event['id']
                ) for event in events
            ]

            self.safe_remove(self.nothing)
            self.component.controls.append(self.dt)
        else:
            self.safe_remove(self.nothing)
            self.component.controls.append(self.nothing)

        self.safe_update()
        self.page.update()
