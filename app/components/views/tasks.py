import flet as ft


class Tasks:
    VIEW_TITLE: str = "Задачи"
    VIEW_ICON = ft.icons.TASK_ALT

    def __init__(self, page: ft.Page):
        self.page = page
        self.modal = None
        self.component = ft.Text('tasks')
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