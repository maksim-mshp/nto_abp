import flet as ft


class CreateEvent:

    def __init__(self, close_event):
        self.close_event = close_event

        self.description = ft.TextField(label="Описание", multiline=True)

        self.form = ft.Column(controls=[
            ft.Container(expand=1, content=self.description),
        ], height=500, width=500)

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

    def _save(self, e):
        print(self.description.value)
        self.close()
