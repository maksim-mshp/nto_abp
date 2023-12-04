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

        self.select_time_btn = ft.ElevatedButton('Бронирование помещения', on_click=self.redirect_view,
                                                 icon=ft.icons.MEETING_ROOM, style=self.normal_btn_style,
                                                 )

        self.room = ft.Dropdown(
            options=[ft.dropdown.Option(i['id'], i['name']) for i in job_service.get_jobs_rooms_with_id()],
            label='Помещение',
            on_change=self.on_room_change,
            dense=True
        )

        self.half_reservation = ft.Checkbox(label='Бронь половины помещения', visible=False)

        self.form = ft.Column(controls=[
            self.name,
            self.type,
            self.date_btn,
            self.room,
            self.half_reservation,
            self.select_time_btn,
            ft.Container(expand=1, content=self.description),
        ], height=530, width=625, spacing=17)

        self.build()

        self.started_room_id = None
        self.started_half_reservation = None

    def build(self):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Создание мероприятия" if self.id is None else 'Редактирование мероприятия'),
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

    def on_room_change(self, e=None):
        utils.STORAGE['selected_fields'] = []
        utils.STORAGE['room_id'] = int(self.room.value)
        self.half_reservation.visible = room_service.get_room_by_id(self.room.value)['half_reservation']
        self.half_reservation.value = False
        self.select_time_btn.disabled = False
        self.form.update()

    def redirect_view(self, e=None):
        utils.STORAGE['room_id'] = int(self.room.value)
        utils.STORAGE['half_reservation'] = self.half_reservation.value
        utils.STORAGE['event_id'] = self.id

        def prepare_storage():
            if not self.id:
                return
            if self.started_room_id != self.room.value or self.started_half_reservation != self.half_reservation.value:
                utils.STORAGE['selected_fields'] = []
                return
            if len(utils.STORAGE.get('selected_fields', [])) > 0:
                return

            utils.STORAGE['selected_fields'] = [
                i['start_date_time']
                for i in reservation_service.get_by_event_id(self.id)['intervals']
            ]

        prepare_storage()
        self.close(clear=False)
        utils.on_page_change_func(new_index=3)

    def reset(self):
        self.name.error_text = None
        self.type.error_text = None
        self.date_btn.style = self.normal_btn_style
        self.select_time_btn.style = self.normal_btn_style
        self.select_time_btn.disabled = not self.id

        if self.id is None:
            self.name.value = ''
            self.type.value = None
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

            self.started_room_id = reservation['room_id']
            self.started_half_reservation = reservation['half_reservation']
            self.half_reservation.value = reservation['half_reservation']

            self.half_reservation.visible = room_service.get_room_by_id(self.room.value)['half_reservation']

        self.date_btn.text = self.get_btn_text()

        self.type.visible = self.category != utils.CATEGORIES[2]

    def close(self, clear=True):
        self.dialog.open = False
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
        self.type.visible = self.category != utils.CATEGORIES[2]

        if utils.STORAGE.get('from_reservation', False):
            if len(utils.STORAGE.get('selected_fields', [])) > 0:
                self.select_time_btn.style = self.normal_btn_style

            self.room.value = utils.STORAGE.get('room_id', None)

        else:
            self.reset()
        self.dialog.open = True

    def get_btn_text(self):
        if self.date.value is not None:
            return utils.get_formatted_date(self.date.value)
        return 'Выберите дату'

    def cancel(self, e):
        self.close()

    def remove(self, e):
        event_service.delete_event(self.id)
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

    def on_type_change(self, e):
        if self.type.value is not None:
            self.type.error_text = None
            self.dialog.update()

    def save(self, e):
        err = False

        if self.name.value.strip() == '':
            self.name.error_text = 'Введите название'
            err = True
        if (self.type.value is None) and self.category != utils.CATEGORIES[2]:
            self.type.error_text = 'Выберите вид'
            err = True

        if self.date.value is None:
            self.date_btn.style = self.err_btn_style
            err = True

        if len(utils.STORAGE.get('selected_fields', [])) == 0:
            self.select_time_btn.style = self.err_btn_style
            err = True

        if err:
            self.dialog.update()
            return

        if self.id is None:
            res = event_service.create_event(self.name.value.strip(), self.date.value, self.type.value,
                                             self.description.value.strip(), self.category)
            reservation_service.create(
                self.room.value,
                res['id'],
                utils.STORAGE['selected_fields'],
                utils.STORAGE['half_reservation'],
            )
        else:
            event_service.update_event(self.id, self.name.value.strip(), self.date.value, self.type.value,
                                       self.description.value.strip(), self.category)

            reservation_service.update_by_id(
                self.reservation_id,
                self.room.value,
                self.id,
                utils.STORAGE['selected_fields'],
                utils.STORAGE['half_reservation'],
            )

        self.close()
