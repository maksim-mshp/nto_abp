import datetime
import flet as ft

from app import utils


class CreateEvent:

    def __init__(self, page: ft.Page, close_event):
        self.page = page
        self.close_event = close_event

        self.type = ft.Dropdown(
            options=[ft.dropdown.Option(i) for i in utils.get_types()],
            label='Вид мероприятия'
        )

        self.description = ft.TextField(label="Описание", multiline=True, keyboard_type=ft.KeyboardType.DATETIME)

        self.date = ft.DatePicker(
            on_dismiss=self._on_close_datepicker,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT_ONLY
        )

        self.page.overlay.append(self.date)

        self.form = ft.Column(controls=[
            self.type,
            ft.TextButton('pick date', on_click=self._open_datepicker),
            ft.Container(expand=1, content=self.description),
        ], height=400, width=500)

        self.dialog = ft.AlertDialog(
            title=ft.Text("Создание мероприятия"),
            content=self.form,
            actions=[
                ft.TextButton("Сохранить", on_click=self._save),
                ft.TextButton("Отмена", on_click=self._cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.START,
            modal=True
        )

    def close(self):
        self.dialog.open = False
        self.close_event()

    def open(self):
        self.dialog.open = True

    def _cancel(self, e):
        self.close()

    def _open_datepicker(self, e):
        self.date.pick_date()

    def _on_close_datepicker(self, e):
        pass

    def _save(self, e):
        print(self.description.value)
        self.close()
