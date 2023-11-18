import datetime
import flet as ft

from app import utils


class CreateEvent:

    def __init__(self, page: ft.Page, close_event, categoty):
        self.page = page
        self.close_event = close_event
        self.categoty = categoty

        self.type = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in utils.get_types()],
            label='Вид мероприятия',
            on_change=self._on_type_change
        )

        self.name = ft.TextField(label="Название", on_change=self._on_name_change)
        self.description = ft.TextField(label="Описание", multiline=True)

        self.date = ft.DatePicker(
            on_dismiss=self._on_close_datepicker,
            on_change=self._on_close_datepicker,
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

        self.date_btn = ft.ElevatedButton(self._get_btn_text(), on_click=self._open_datepicker,
                                          icon=ft.icons.EDIT_CALENDAR, style=self.normal_btn_style)

        self.form = ft.Column(controls=[
            self.name,
            self.type,
            self.date_btn,
            ft.Container(expand=1, content=self.description),
        ], height=400, width=500, spacing=17)

        self.dialog = ft.AlertDialog(
            title=ft.Text("Создание мероприятия"),
            content=self.form,
            actions=[
                ft.TextButton("Отмена", on_click=self._cancel),
                ft.TextButton("Сохранить", on_click=self._save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )

    def close(self):
        self.dialog.open = False
        self.close_event()
        self.name.value = ''
        self.type.value = None
        self.date.value = None
        self.description.value = ''
        self.name.error_text = None
        self.type.error_text = None
        self.date_btn.style = self.normal_btn_style

    def open(self):
        self.dialog.open = True

    def _get_btn_text(self):
        if self.date.value is not None:
            return utils.get_formatted_date(self.date.value)
        return 'Выберите дату'

    def _cancel(self, e):
        self.close()

    def _open_datepicker(self, e):
        self.date.pick_date()

    def _on_close_datepicker(self, e):
        if self.date.value is not None:
            self.date_btn.style = self.normal_btn_style

        self.date_btn.text = self._get_btn_text()
        self.dialog.update()

    def _on_name_change(self, e):
        if self.name.value.strip() != '':
            self.name.error_text = None
            self.dialog.update()

    def _on_type_change(self, e):
        if self.type.value is not None:
            self.type.error_text = None
            self.dialog.update()

    def _save(self, e):
        err = False

        if self.name.value.strip() == '':
            self.name.error_text = 'Введите название'
            err = True
        if self.type.value is None:
            self.type.error_text = 'Выберите вид'
            err = True

        if self.date.value is None:
            self.date_btn.style = self.err_btn_style
            err = True

        if err:
            self.dialog.update()
            return

        utils.create_event(self.name.value, self.date.value, self.type.value, self.description.value, self.categoty)
        self.close()
