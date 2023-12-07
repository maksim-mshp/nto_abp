import datetime
import flet as ft

from services.event import event_service
import utils
from services.job import job_service
from services.reservation import reservation_service
from services.room import room_service


class EventModal:

    def __init__(self, page: ft.Page, close_event, category=None, id=None):
        self.dialog = None
        self.reservation_id = None
        self.page = page
        self.close_event = close_event
        self.category = category
        self.id = id

        self.type = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in event_service.get_events_types()],
            label='Вид мероприятия',
            on_change=self.on_type_change, dense=True
        )

        self.clubs_type = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in event_service.get_clubs_types()],
            label='Вид кружка',
            on_change=self.on_clubs_type_change, dense=True
        )

        self.teacher = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in event_service.get_teachers()],
            label='Преподаватель',
            on_change=self.on_teacher_change, dense=True
        )

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

        self.schedule_btn = ft.ElevatedButton('Выберите расписание кружка', on_click=self.redirect_view_obr,
                                              icon=ft.icons.SCHEDULE, style=self.normal_btn_style)

        self.select_time_btn = ft.ElevatedButton('Бронирование помещения', on_click=self.redirect_view,
                                                 icon=ft.icons.MEETING_ROOM, style=self.normal_btn_style,
                                                 )

        self.room = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_rooms_with_id()],
            label='Помещение',
            on_change=self.on_room_change,
            dense=True
        )

        self.half_reservation = ft.Checkbox(label='Бронь половины помещения', visible=False,
                                            on_change=self.half_reservation_change)

        self.form = ft.Column(controls=[
            self.name,
            self.type,
            self.clubs_type,
            self.date_btn,
            self.room,
            self.half_reservation,
            self.select_time_btn,
            self.schedule_btn,
            self.teacher,
            ft.Container(expand=1, content=self.description),
        ], height=530, width=625, spacing=17)

        self.build()

        self.started_room_id = None
        self.started_half_reservation = None
        self.was_redirected = False

    def is_obr(self):
        """Проверка является ли мероприятие кружком"""
        return self.category == utils.CATEGORIES[2]

    def get_modal_title(self) -> str:
        res = 'Создание '
        if self.id:
            res = 'Редактирование '
        if self.is_obr():
            res += 'кружка'
        else:
            res += 'мероприятия'
        return res

    def build(self):
        self.dialog = ft.AlertDialog(
            title=ft.Text(self.get_modal_title()),
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

        self.dialog.actions.insert(0, ft.TextButton("Удалить мероприятие", on_click=self.remove, style=ft.ButtonStyle(
            color=ft.colors.RED_ACCENT_700,
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.RED_100,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )))

    def update_schedule_btn(self):
        self.schedule_btn.disabled = not (self.room.value and self.date.value)

    def on_room_change(self, e=None):
        utils.STORAGE['selected_fields'] = []
        utils.STORAGE['room_id'] = int(self.room.value)
        self.half_reservation.visible = room_service.get_room_by_id(self.room.value)['half_reservation']
        self.half_reservation.value = False
        self.select_time_btn.disabled = False
        self.room.error_text = None
        self.update_schedule_btn()
        self.was_redirected = False
        self.page.update()

    def half_reservation_change(self, e):
        self.was_redirected = False

    def prepare_storage(self):
        if self.is_obr():
            utils.STORAGE['club_start_datetime'] = self.date.value
            reservation = reservation_service.get_schedule_by_room_and_event(self.room.value, self.id)
            utils.STORAGE['selected_fields'] = [i['start_date_time'] for i in
                                                reservation
                                                ]
        if not self.id:
            return
        if self.started_room_id != self.room.value or self.started_half_reservation != self.half_reservation.value:
            utils.STORAGE['selected_fields'] = []
            return
        if len(utils.STORAGE.get('selected_fields', [])) > 0:
            return
        if self.was_redirected:
            return

        if not self.is_obr():
            utils.STORAGE['selected_fields'] = [
                i['start_date_time']
                for i in reservation_service.get_by_event_id(self.id)['intervals']
            ]

    def redirect_view(self, e=None):
        utils.STORAGE['room_id'] = int(self.room.value)
        utils.STORAGE['half_reservation'] = self.half_reservation.value
        utils.STORAGE['event_id'] = self.id
        self.prepare_storage()
        self.close(clear=False)
        self.was_redirected = True
        utils.on_page_change_func(new_index=3)

    def redirect_view_obr(self, e=None):
        utils.STORAGE['room_id'] = int(self.room.value)
        utils.STORAGE['half_reservation'] = self.half_reservation.value
        utils.STORAGE['event_id'] = self.id

        self.prepare_storage()
        self.close(clear=False)
        self.was_redirected = True

        utils.on_page_change_func(new_index=4)

    def reset(self):
        self.name.error_text = None
        self.type.error_text = None
        self.clubs_type.error_text = None
        self.teacher.error_text = None
        self.room.error_text = None
        self.date_btn.style = self.normal_btn_style
        self.select_time_btn.style = self.normal_btn_style
        self.schedule_btn.style = self.normal_btn_style
        self.select_time_btn.disabled = not self.id
        self.schedule_btn.disabled = not self.id

        if self.id is None:
            self.name.value = ''
            self.type.value = None
            self.clubs_type.value = None
            self.teacher.value = None
            self.date.value = None
            self.room.value = None
            self.description.value = ''
            self.started_room_id = None
            self.started_half_reservation = None
            self.half_reservation.value = None

        else:
            event = event_service.get_event_by_id(self.id)
            reservation = reservation_service.get_by_event_id(self.id)
            self.category = event['category']
            self.name.value = event['title']
            self.room.value = reservation['room_id']
            self.type.value = event_service.get_event_type_by_id(event['event_type_id'])
            self.date.value = event['date']
            self.description.value = event['description']
            self.reservation_id = reservation['reservation_id']

            if self.is_obr():
                self.clubs_type.value = event_service.get_club_type_by_id(event['club_type_id'])
                self.teacher.value = event_service.get_teacher_by_id(event['teacher_id'])['name']

            self.started_room_id = reservation['room_id']
            self.started_half_reservation = reservation['half_reservation']
            self.half_reservation.value = reservation['half_reservation']

            self.half_reservation.visible = room_service.get_room_by_id(self.room.value)['half_reservation']

        self.date_btn.text = self.get_btn_text()
        self.dialog.title = ft.Text(self.get_modal_title())

        self.type.visible = not self.is_obr()
        self.clubs_type.visible = self.is_obr()
        self.description.visible = not self.is_obr()
        self.select_time_btn.visible = not self.is_obr()
        self.schedule_btn.visible = self.is_obr()
        self.teacher.visible = self.is_obr()

    def close(self, clear=True):
        self.dialog.open = False
        self.was_redirected = False
        self.page.update()
        self.close_event()

        if clear:
            utils.STORAGE['selected_fields'] = []
            utils.STORAGE['room_id'] = None
            utils.STORAGE['event_id'] = None
            utils.STORAGE['from_reservation'] = False

    def open(self):
        self.type.options = [ft.dropdown.Option(i) for i in event_service.get_events_types()]
        self.room.options = [ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_rooms_with_id()]
        self.type.visible = not self.is_obr()

        if utils.STORAGE.get('from_reservation', False):
            if len(utils.STORAGE.get('selected_fields', [])) > 0:
                self.select_time_btn.style = self.normal_btn_style

        if len(utils.STORAGE.get('selected_fields', [])) == 0 and self.id and not self.was_redirected:
            reservation = reservation_service.get_by_event_id(self.id)
            if self.is_obr():
                res = reservation_service.get_schedule_by_room_and_event(self.room.value, self.id)
                utils.STORAGE['selected_fields'] = [i['start_date_time'] for i in
                                                    res
                                                    ]
            else:
                utils.STORAGE['selected_fields'] = [i['start_date_time'] for i in
                                                    reservation['intervals']
                                                    ]
            utils.STORAGE['half_reservation'] = reservation['half_reservation']
            self.reset()
        else:
            if utils.STORAGE.get('from_reservation', False):
                self.room.value = utils.STORAGE.get('room_id', None)
            else:
                self.reset()

        self.dialog.open = True

    def get_btn_text(self):
        if self.date.value is not None:
            return utils.get_formatted_date(self.date.value)
        if self.is_obr():
            return 'Выберите дату начала кружка'
        return 'Выберите дату'

    def cancel(self, e):
        self.close()

    def remove(self, e):
        event_service.delete_event(self.id)
        reservation = reservation_service.get_by_event_id(self.id)
        reservation_service.delete_by_id(reservation['reservation_id'])
        self.id = None
        self.close()

    def open_datepicker(self, e):
        self.date.pick_date()

    def on_close_datepicker(self, e):
        if self.date.value is not None:
            self.date_btn.style = self.normal_btn_style

        self.update_schedule_btn()
        self.date_btn.text = self.get_btn_text()
        self.page.update()

    def on_name_change(self, e):
        if self.name.value.strip() != '':
            self.name.error_text = None
            self.dialog.update()

    def on_type_change(self, e):
        if self.type.value is not None:
            self.type.error_text = None
            self.dialog.update()

    def on_clubs_type_change(self, e):
        if self.clubs_type.value is not None:
            self.clubs_type.error_text = None
            self.dialog.update()

    def on_teacher_change(self, e):
        if self.teacher.value is not None:
            self.teacher.error_text = None
            self.dialog.update()

    def save(self, e):
        err = False

        if self.name.value.strip() == '':
            self.name.error_text = 'Введите название'
            err = True
        if not self.type.value and not self.is_obr():
            self.type.error_text = 'Выберите вид мероприятия'
            err = True

        if not self.room.value:
            self.room.error_text = 'Выберите помещение'
            err = True

        if not self.teacher.value and self.is_obr():
            self.teacher.error_text = 'Выберите преподавателя'
            err = True

        if not self.clubs_type.value and self.is_obr():
            self.clubs_type.error_text = 'Выберите вид кружка'
            err = True

        if not self.date.value:
            self.date_btn.style = self.err_btn_style
            err = True

        need_intervals_update = True

        if not self.was_redirected:
            if self.started_room_id != self.room.value or self.started_half_reservation != self.half_reservation.value:
                utils.STORAGE['selected_fields'] = []
                self.select_time_btn.style = self.err_btn_style
                self.schedule_btn.style = self.err_btn_style
                err = True
            else:
                need_intervals_update = False
                self.select_time_btn.style = self.normal_btn_style
                self.schedule_btn.style = self.normal_btn_style
        elif len(utils.STORAGE.get('selected_fields', [])) == 0:
            self.select_time_btn.style = self.err_btn_style
            self.schedule_btn.style = self.err_btn_style
            err = True

        if err:
            self.dialog.update()
            return

        if self.id is None:
            res = event_service.create_event(
                self.name.value.strip(),
                self.date.value,
                self.category,
                self.description.value.strip(),
                self.type.value,
                self.clubs_type.value,
                self.teacher.value,
            )

            reservation_service.create(
                self.room.value,
                res['id'],
                utils.STORAGE['selected_fields'],
                utils.STORAGE['half_reservation'],
                self.is_obr()
            )
        else:
            event_service.update_event(
                self.id,
                self.name.value.strip(),
                self.date.value,
                self.category,
                self.description.value.strip(),
                self.type.value,
                self.clubs_type.value,
                self.teacher.value,
            )

            if need_intervals_update:
                reservation_service.update_by_id(
                    self.reservation_id,
                    self.room.value,
                    self.id,
                    utils.STORAGE['selected_fields'],
                    utils.STORAGE['half_reservation'],
                    self.is_obr()
                )

        self.close()
