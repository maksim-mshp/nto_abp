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
        self.dt = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(i)) for i in
                ["", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
            ],
            width=10000,
            data_row_min_height=300
        )

        self.component = ft.Column(controls=[self.dt, self.nothing], expand=1)
        self.hide()

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
            bgcolor=bgcolor, border_radius=10,
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
                self.dt.rows.append(ft.DataRow([
                    ft.DataCell(self.get_column([{
                        'start_time': datetime.now(),
                        'end_time': datetime.now(),
                        'room': 'room',
                        'teacher': 'teacher',
                    }])) for i in range(7)
                ]))

                self.dt.rows[-1].cells.insert(0, ft.DataCell(ft.Text('ИЗО', weight=ft.FontWeight.W_600)))

    def hide(self):
        self.component.visible = False
        self.safe_update()

    def show(self):
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.build()
        self.safe_update()
        self.page.update()
