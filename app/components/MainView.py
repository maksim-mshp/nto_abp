import flet as ft
from app.components.EventModal import EventModal
from app.utils import *


class MainView:
    def __init__(self, page):
        self.page = page
        self.modal = None

        self.dt = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название")),
                ft.DataColumn(ft.Text("Вид")),
                ft.DataColumn(ft.Text("Дата")),
            ],
            width=10000
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[ft.Tab(text='Все мероприятия')] + [ft.Tab(text=x) for x in CATEGORIES],
            on_change=self.on_change,
        )

        self.on_change()

        page.add(self.tabs)
        page.add(self.dt)
        page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked))

    def add_clicked(self, e):
        self.modal = EventModal(self.page,
                                close_event=self.page.update,
                                category=CATEGORIES[self.tabs.selected_index - 1])
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def on_edit_modal_close(self):
        self.on_change()
        self.page.update()

    def open_modal(self, e):
        self.modal = EventModal(self.page, close_event=self.on_edit_modal_close, id=e.control.data)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def on_change(self, e=None):
        category = None
        if self.tabs.selected_index > 0:
            category = CATEGORIES[self.tabs.selected_index - 1]

        self.dt.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(event['title'])),
                    ft.DataCell(ft.Text(get_type_by_id(event['event_type_id']))),
                    ft.DataCell(ft.Text(get_formatted_date(event['date']))),
                ],
                on_select_changed=self.open_modal,
                data=event['id']
            ) for event in get_events(category)
        ]

        self.page.update()
