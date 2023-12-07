import flet as ft
import utils


class ClubsSchedule:
    VIEW_TITLE: str = "Расписание кружков"
    VIEW_ICON = ft.icons.SCHOOL
    NAVBAR_HIDDEN: bool = False

    def __init__(self, page: ft.Page):
        self.page = page
        self.component = ft.Column(controls=[], expand=1)

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
