import datetime
import flet as ft

from services.event import event_service
from services.job import job_service
import utils
from utils import JOB_STATUSES, truncate_text
from components.job_status_chip import JobStatusChip


class JobModal:

    def __init__(self, page: ft.Page, close_event, category=None, id=None):
        self.registration_date = None
        self.page = page
        self.close_event = close_event
        self.category = category
        self.id = id

        self.event = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], truncate_text(i['title'], 67)) for i in event_service.get_events()],
            label='Мероприятие',
            on_change=self.on_event_change,
            dense=True
        )

        self.job_type = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_types_with_id()],
            label='Вид работы',
            on_change=self.on_job_type_change,
            dense=True
        )

        self.room = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_rooms_with_id()],
            label='Помещение',
            on_change=self.on_room_change,
            dense=True
        )

        self.status = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in JOB_STATUSES],
            label='Статус',
            on_change=self.on_status_change,
            value=JOB_STATUSES[0],
            dense=True
        )

        self.reg_text = ft.Text('', visible=False)

        self.name = ft.TextField(label="Название", on_change=self.on_name_change, dense=True)
        self.description = ft.TextField(label="Описание", multiline=True, dense=True)

        self.date = ft.DatePicker(
            on_dismiss=self.on_close_datepicker,
            on_change=self.on_close_datepicker,
            first_date=datetime.datetime.now(),
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
        )
        self.page.overlay.append(self.date)

        self.normal_btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=17
        )

        self.err_btn_style = ft.ButtonStyle(
            bgcolor={
                ft.MaterialState.DEFAULT: ft.colors.RED_ACCENT_700,
                ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_700,
            },
            color={
                ft.MaterialState.DEFAULT: ft.colors.WHITE,
                ft.MaterialState.HOVERED: ft.colors.WHITE,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=17
        )

        self.date_btn = ft.ElevatedButton(self.get_btn_text(), on_click=self.open_datepicker,
                                          icon=ft.icons.EDIT_CALENDAR, style=self.normal_btn_style)

        self.form = ft.Column(controls=[
            self.reg_text,
            self.name,
            self.status,
            self.event,
            self.job_type,
            self.room,
            self.date_btn,
            ft.Container(expand=1, content=self.description),
        ], width=625, spacing=17, height=530, scroll=ft.ScrollMode.ADAPTIVE)

        self.reset()
        self.date_btn.text = self.get_btn_text()

        self.dialog = ft.AlertDialog(
            title=ft.Text("Создание заявки" if self.id is None else 'Редактирование заявки'),
            content=self.form,
            actions=[
                ft.Row([
                    ft.TextButton("Отмена", on_click=self.cancel, style=utils.DEFAULT_BTN_STYLE),
                    ft.TextButton("Сохранить", on_click=self.save, style=utils.DEFAULT_BTN_STYLE),
                ], tight=True)
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            modal=True
        )

        if self.id is None:
            self.dialog.actions_alignment = ft.MainAxisAlignment.END
            return

        self.dialog.actions.insert(0, ft.TextButton("Удалить заявку", on_click=self.remove, style=ft.ButtonStyle(
            color=ft.colors.RED_ACCENT_700,
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.RED_100,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )))

    def get_reg_text(self):
        return f'Дата регистрации заявки: {utils.get_formatted_date(self.registration_date)}'

    def reset(self):
        self.name.error_text = None
        self.event.error_text = None
        self.job_type.error_text = None
        self.room.error_text = None
        self.status.error_text = None
        self.date_btn.style = self.normal_btn_style

        if self.id is None:
            self.name.value = ''
            self.event.value = None
            self.job_type.value = None
            self.room.value = None
            self.status.value = JOB_STATUSES[0]
            self.date.value = None
            self.description.value = ''
            self.reg_text.value = ''
            self.reg_text.visible = False
        else:
            job = job_service.get_job_by_id(self.id)
            self.name.value = job['title']
            self.description.value = job['description']
            self.event.value = job['event_id']
            self.job_type.value = job['job_type_id']
            self.room.value = job['job_room_id']
            self.date.value = job['deadline']
            self.status.value = job['status']
            self.registration_date = job['registration_date']
            self.reg_text.value = self.get_reg_text()
            self.reg_text.visible = True

    def close(self):
        self.dialog.open = False
        self.close_event()
        self.reset()

    def open(self):
        self.dialog.open = True

    def get_btn_text(self):
        if self.date.value is not None:
            return utils.get_formatted_date(self.date.value)
        return 'Выберите срок выполнения'

    def cancel(self, e):
        self.close()

    def remove(self, e):
        job_service.delete_job(self.id)
        self.id = None
        self.close()

    def open_datepicker(self, e):
        self.date.pick_date()

    def on_close_datepicker(self, e):
        if self.date.value is not None:
            self.date_btn.style = self.normal_btn_style

        self.date_btn.text = self.get_btn_text()
        self.dialog.update()

    def on_name_change(self, e):
        if self.name.value.strip() != '':
            self.name.error_text = None
            self.dialog.update()

    def on_event_change(self, e):
        if self.event.value is not None:
            self.event.error_text = None
            self.dialog.update()

    def on_job_type_change(self, e):
        if self.job_type.value is not None:
            self.job_type.error_text = None
            self.dialog.update()

    def on_room_change(self, e):
        if self.job_type.value is not None:
            self.job_type.error_text = None
            self.dialog.update()

    def on_status_change(self, e):
        if self.job_type.value is not None:
            self.job_type.error_text = None
            self.dialog.update()

    def save(self, e):
        err = False

        if self.name.value.strip() == '':
            self.name.error_text = 'Введите название'
            err = True
        if self.event.value is None:
            self.event.error_text = 'Выберите мероприятие'
            err = True
        if self.job_type.value is None:
            self.job_type.error_text = 'Выберите вид работы'
            err = True
        if self.room.value is None:
            self.room.error_text = 'Выберите помещение'
            err = True
        if self.status.value is None:
            self.status.error_text = 'Выберите статус'
            err = True

        if self.date.value is None:
            self.date_btn.style = self.err_btn_style
            err = True

        if err:
            self.dialog.update()
            return

        if self.id is None:
            job_service.create_job(
                self.name.value.strip(),
                self.description.value.strip(),
                self.event.value,
                self.job_type.value,
                self.room.value,
                self.date.value,
                self.status.value
            )
        else:
            job_service.update_job(
                self.id,
                self.name.value.strip(),
                self.description.value.strip(),
                self.event.value,
                self.job_type.value,
                self.room.value,
                self.date.value,
                self.status.value
            )

        self.close()
