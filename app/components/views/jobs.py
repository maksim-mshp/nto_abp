import flet as ft

from components.modals.job import JobModal
from components.modals.job_type import JobTypeModal
from components.modals.rooms import RoomModal


class Jobs:
    VIEW_TITLE: str = "Заявки"
    VIEW_ICON = ft.icons.TASK_ALT

    def __init__(self, page: ft.Page):
        self.page = page
        self.modal = None
        self.component = ft.Column(controls=[], expand=1)

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab('Рабочий стол'),
                ft.Tab('Все заявки'),
            ]
        )

        header_btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=17
        )

        self.create_btn = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)
        self.page.add(self.create_btn)

        self.component.controls.append(ft.Row([
            self.tabs,
            ft.Row([
                ft.ElevatedButton('Управление видами работ', style=header_btn_style,
                                  on_click=self.manage_job_types_clicked),
                ft.ElevatedButton('Управление помещениями', style=header_btn_style,
                                  on_click=self.manage_rooms_clicked)])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))

        self.hide()
        self.page.update()

    def show(self):
        self.component.visible = True
        self.create_btn.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()

    def add_clicked(self, e):
        self.modal = JobModal(self.page, close_event=self.on_change)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.safe_update()
        self.page.update()

    def hide(self):
        self.component.visible = False
        self.create_btn.visible = False
        self.safe_update()

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass

    def on_change(self):
        self.page.update()

    def manage_rooms_clicked(self, e):
        self.modal = RoomModal(self.page, close_event=self.on_change)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.safe_update()
        self.page.update()

    def manage_job_types_clicked(self, e):
        self.modal = JobTypeModal(self.page, close_event=self.on_change)
        self.page.dialog = self.modal.dialog
        self.modal.open()
        self.safe_update()
        self.page.update()
