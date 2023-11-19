import flet as ft


class Tasks:
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

        self.component.controls.append(ft.Row([
            self.tabs,
            ft.Row([
                ft.ElevatedButton('Управление видами работ', style=header_btn_style),
                ft.ElevatedButton('Управление помещениями', style=header_btn_style)])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))

        self.hide()
        self.page.update()

    def show(self):
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()

    def hide(self):
        self.component.visible = False
        self.safe_update()

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass
