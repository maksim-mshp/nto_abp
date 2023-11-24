import datetime
import flet as ft

from services.event import event_service
import utils


class JobModal:

    def __init__(self, page: ft.Page, close_event, category=None, id=None):
        self.page = page
        self.close_event = close_event
        self.category = category
        self.id = id

        self.type = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in event_service.get_events_types()],
            label='Вид мероприятия',
            on_change=self.on_type_change
        )

        self.name = ft.TextField(label="Название", on_change=self.on_name_change)
        self.description = ft.TextField(label="Описание", multiline=True)

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
            self.name,
            self.type,
            self.date_btn,
            ft.Container(expand=1, content=self.description),
        ], height=400, width=500, spacing=17)

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

        self.dialog.actions.insert(0, ft.TextButton("Удалить мероприятие", on_click=self.remove, style=ft.ButtonStyle(
            color=ft.colors.RED_ACCENT_700,
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.RED_100,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )))

    def reset(self):
        self.name.error_text = None
        self.type.error_text = None
        self.date_btn.style = self.normal_btn_style

        if self.id is None:
            self.name.value = ''
            self.type.value = None
            self.date.value = None
            self.description.value = ''
        else:
            event = event_service.get_event_by_id(self.id)
            self.category = event['category']
            self.name.value = event['title']
            self.type.value = event_service.get_event_type_by_id(event['event_type_id'])
            self.date.value = event['date']
            self.description.value = event['description']

        if self.category == utils.CATEGORIES[2]:
            self.type.visible = False

    def close(self):
        self.dialog.open = False
        self.close_event()
        self.reset()

    def open(self):
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

        if err:
            self.dialog.update()
            return

        if self.id is None:
            event_service.create_event(self.name.value.strip(), self.date.value, self.type.value,
                                       self.description.value.strip(), self.category)
        else:
            event_service.update_event(self.id, self.name.value.strip(), self.date.value, self.type.value,
                                       self.description.value.strip(), self.category)

        self.close()
