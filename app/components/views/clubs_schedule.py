import flet as ft
from datetime import datetime


class ClubsSchedule:
    VIEW_TITLE: str = "Расписание кружков"
    VIEW_ICON = ft.icons.SCHOOL
    NAVBAR_HIDDEN: bool = False

    def __init__(self, page: ft.Page):
        self.page = page

        self.nothing = ft.Container(ft.Text("Ничего не найдено"), width=100000, padding=50,
                                    alignment=ft.alignment.center)

        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        self.dt = ft.Column(width=10000)
        self.add_row([self.create_header_cell(i) for i in days_of_week], '')

        self.component = ft.Column(controls=[self.dt, self.nothing], expand=1)
        self.hide()

    @staticmethod
    def create_header_cell(text: str):
        return ft.Container(ft.Text(text, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                            padding=ft.Padding(15, 15, 15, 15), width=150)

    def add_row(self, controls: list, title: str):
        self.dt.controls.append(
            ft.Container(
                ft.Row([self.create_header_cell(title)] + controls,
                       alignment=ft.MainAxisAlignment.SPACE_AROUND),
                border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.OUTLINE_VARIANT)))
        )

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass

    @staticmethod
    def get_chip(start_time: datetime, end_time: datetime, room: str, teacher: str):
        bgcolor = ft.colors.PRIMARY_CONTAINER
        text = f'{start_time:%H:%M} - {end_time:%H:%M}\n{room}\n{teacher}'

        return ft.Container(
            ft.Text(text, bgcolor=bgcolor),
            bgcolor=bgcolor, border_radius=10, padding=10
        )

    def get_column(self, one_day_list: list[dict]):
        return ft.Column(
            [self.get_chip(**i) for i in one_day_list]
        )

    def build(self):
        self.dt.visible = False
        self.nothing.visible = False

        if len([1]) == 0:
            self.nothing.visible = True
            return
        else:
            self.dt.visible = True

            for event in range(3):
                self.add_row([
                    self.get_column([{
                        'start_time': datetime.now(),
                        'end_time': datetime.now(),
                        'room': 'room',
                        'teacher': 'teacher',
                    }]) for i in range(7)
                ], 'ИЗО11111111111111111111111111111111111111111111111111111111111111')

    def hide(self):
        self.component.visible = False
        self.safe_update()

    def show(self):
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.build()
        self.safe_update()
        self.page.update()
