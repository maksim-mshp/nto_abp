import flet as ft
from datetime import datetime
from services.reservation import reservation_service


class ClubsSchedule:
    VIEW_TITLE: str = "Расписание кружков"
    VIEW_ICON = ft.icons.SCHOOL
    NAVBAR_HIDDEN: bool = False

    def __init__(self, page: ft.Page):
        self.page = page

        self.nothing = ft.Container(ft.Text("Ничего не найдено"), width=100000, padding=50,
                                    alignment=ft.alignment.center)
        self.dt = ft.Column(width=10000, scroll=ft.ScrollMode.ADAPTIVE, expand=1)

        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.add_row([self.create_header_cell(i) for i in days_of_week], '')

        self.component = ft.Column(controls=[self.dt, self.nothing], expand=1)
        self.hide()

    @staticmethod
    def create_header_cell(text: str):
        return ft.Container(ft.Text(text, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                            padding=ft.Padding(15, 15, 15, 15), expand=1)

    @staticmethod
    def create_header_cell_col(text: str):
        return ft.Container(ft.Text(text, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                            padding=ft.Padding(15, 15, 15, 15), width=140)

    def add_row(self, controls: list, title: str):
        self.dt.controls.append(
            ft.Container(
                ft.Row(
                    [self.create_header_cell_col(title),
                     ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_AROUND, expand=True)],
                ),
                border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.OUTLINE_VARIANT)))
        )

    def safe_update(self):
        try:
            self.component.update()
        except AssertionError:
            pass

    @staticmethod
    def prepare_teacher_name(name: str):
        name = name.split()
        for i, j in enumerate(name[1:], 1):
            name[i] = f'{j[0]}.'
        return ' '.join(name)

    def get_chip(self, start_time: datetime, end_time: datetime, room: str, teacher: str):
        bgcolor = ft.colors.PRIMARY_CONTAINER

        time = ft.Text(f'{start_time:%H:%M} – {end_time:%H:%M}', weight=ft.FontWeight.W_600,
                       text_align=ft.TextAlign.CENTER, bgcolor=bgcolor, width=10000)
        room = ft.Text(room, text_align=ft.TextAlign.CENTER, bgcolor=bgcolor, width=10000)
        teacher = ft.Text(self.prepare_teacher_name(teacher), text_align=ft.TextAlign.CENTER, bgcolor=bgcolor,
                          width=10000, italic=True)

        return ft.Container(
            ft.Column(
                [time, room, teacher],
                expand=1,
                spacing=0
            ),
            bgcolor=bgcolor, border_radius=10, padding=12, width=10000
        )

    def get_column(self, one_day_list: list[dict]):
        return ft.Container(ft.Column(
            [self.get_chip(**i) for i in one_day_list],
            expand=1
        ), expand=1, alignment=ft.alignment.center,
            padding=ft.Padding(5, 0, 5, 10)
        )

    def build(self):
        self.dt.visible = False
        self.nothing.visible = False

        schedule = reservation_service.get_schedule_for_data_table()

        if len(schedule) == 0:
            self.nothing.visible = True
            return
        else:
            self.dt.visible = True
            del self.dt.controls[1:]

            for event_name, event in schedule.items():
                self.add_row([
                    self.get_column(day) for day in event
                ], event_name)

            self.dt.controls[-1].border = None

    def hide(self):
        self.component.visible = False
        self.safe_update()

    def show(self):
        self.component.visible = True
        self.page.title = self.VIEW_TITLE
        self.build()
        self.safe_update()
        self.page.update()
