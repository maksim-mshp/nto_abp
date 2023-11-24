import flet as ft

from components.job_status_chip import JobStatusChip
from components.modals.job import JobModal
from components.modals.job_type import JobTypeModal
from components.modals.rooms import RoomModal

from services.job import job_service
from utils import get_formatted_date, JOB_STATUSES


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
            ],
            on_change=self.on_change
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

        self.filter_by = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_types_with_id()],
            label='Фильтр',
            on_change=self.on_change,
            dense=True,
        )

        self.dt = None
        self.filter = ft.Row([
            ft.Container(ft.Icon(ft.icons.FILTER_LIST), padding=ft.Padding(left=10, right=10, top=0, bottom=0)),
            self.filter_by,
            ft.IconButton(ft.icons.CLEAR, tooltip='Очистить фильтр', on_click=self.clear_filter)
        ])
        self.nothing = ft.Container(ft.Text("Ничего не найдено"), width=100000, padding=50,
                                    alignment=ft.alignment.center)

        self.component.controls.append(self.filter)

        self.hide()
        self.on_change()

    def show(self):
        self.component.visible = True
        self.create_btn.visible = True
        self.page.title = self.VIEW_TITLE
        self.safe_update()

    def clear_filter(self, e):
        self.filter_by = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_types_with_id()],
            label='Фильтр',
            on_change=self.on_change,
            dense=True,
        )
        self.filter.controls[1] = self.filter_by
        self.filter.update()
        self.on_change()

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

    def safe_remove(self, obj):
        try:
            self.component.controls.remove(obj)
        except ValueError:
            pass

    def on_change(self, e=None):
        filt = {}
        if self.tabs.selected_index == 0:
            filt['status'] = JOB_STATUSES[1]
        if self.filter_by.value is not None and self.filter_by.value != '':
            filt['job_type_id'] = self.filter_by.value
        print(filt)

        jobs = job_service.get_jobs(**filt)

        self.safe_remove(self.dt)
        self.safe_remove(self.nothing)
        self.dt = ft.Column([ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название")),
                ft.DataColumn(ft.Text("Дедлайн")),
                ft.DataColumn(ft.Text("Статус")),
                ft.DataColumn(ft.Text("Вид работы")),
            ],
            width=100000,
        )], scroll=ft.ScrollMode.ADAPTIVE, expand=1)
        self.dt.controls[0].rows.clear()

        if len(jobs) > 0:
            self.dt.controls[0].rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(job['title'])),
                        ft.DataCell(ft.Text(get_formatted_date(job['deadline']))),
                        ft.DataCell(JobStatusChip(JOB_STATUSES.index(job['status'])).chip),
                        ft.DataCell(ft.Text(job_service.get_job_type_by_id(job['job_type_id']))),
                    ],
                    data=job['id']
                ) for job in jobs
            ]

            self.component.controls.append(self.dt)
        else:
            self.component.controls.append(self.nothing)

        self.safe_update()
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
