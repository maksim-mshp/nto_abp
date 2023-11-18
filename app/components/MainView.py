import flet as ft
from components.EventModal import EventModal
from components.TypesModal import TypesModal
from utils import *


class MainView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.modal = None

        self.dt = None

        self.nothing = ft.Container(ft.Text("Ничего не найдено"), width=100000, padding=50,
                                    alignment=ft.alignment.center)

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[ft.Tab(text=x) for x in CATEGORIES],
            on_change=self.on_change,
        )

        self.create_btn = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)
        self.page.add(self.create_btn)
        page.add(ft.Row(
            [self.tabs, ft.ElevatedButton('Управление видами мероприятий', style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=17
            ), on_click=self.manage_types_clicked)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))
        self.on_change()

    def add_clicked(self, e):
        self.modal = EventModal(self.page,
                                close_event=self.on_change,
                                category=CATEGORIES[self.tabs.selected_index])
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def manage_types_clicked(self, e):
        self.modal = TypesModal(self.page, close_event=self.on_change)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def open_modal(self, e):
        self.modal = EventModal(self.page, close_event=self.on_change, id=e.control.data)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def safe_remove(self, obj):
        try:
            self.page.remove(obj)
        except ValueError:
            pass

    def on_change(self, e=None):
        category = CATEGORIES[self.tabs.selected_index]
        events = get_events(category)
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
                        ft.DataCell(ft.Text(get_type_by_id(event['event_type_id']))),
                        ft.DataCell(ft.Text(get_formatted_date(event['date']))),
                    ],
                    on_select_changed=self.open_modal,
                    data=event['id']
                ) for event in events
            ]

            self.safe_remove(self.nothing)
            self.page.add(self.dt)
        else:
            self.safe_remove(self.nothing)
            self.page.add(self.nothing)

        self.page.update()
