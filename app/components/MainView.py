import flet as ft
from app.components.CreateEvent import CreateEvent
from app.utils import CATEGORIES


class MainView:
    def __init__(self, page):
        self.page = page

        self.lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[ft.Tab(text='Все мероприятия')] + [ft.Tab(text=x) for x in CATEGORIES],
            on_change=self.on_change
        )

        page.add(self.tabs)
        page.add(self.lv)
        page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked))

        self.modal = CreateEvent(self.page,
                                 close_event=self.page.update,
                                 categoty=CATEGORIES[self.tabs.selected_index])

    def add_clicked(self, e):
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.page.update()

    def on_change(self, e):
        self.lv.controls.clear()
        self.lv.controls.append(ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text('page'),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                        ),
                    ],
                ),
            ],
        ))
        self.page.update()
