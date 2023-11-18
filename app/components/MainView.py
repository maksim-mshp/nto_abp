import flet as ft
from app.components.CreateEvent import CreateEvent
from app.utils import *


class MainView:
    def __init__(self, page):
        self.page = page

        self.dt = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название")),
                ft.DataColumn(ft.Text("Вид")),
                ft.DataColumn(ft.Text("Дата")),
            ]
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[ft.Tab(text='Все мероприятия')] + [ft.Tab(text=x) for x in CATEGORIES],
            on_change=self.on_change
        )

        self.on_change()

        page.add(self.tabs)
        page.add(self.dt)
        page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked))

        self.modal = CreateEvent(self.page,
                                 close_event=self.page.update,
                                 categoty=CATEGORIES[self.tabs.selected_index - 1])

    def add_clicked(self, e):
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
            ) for event in get_events(category)
        ]

        self.page.update()
