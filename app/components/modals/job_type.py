import flet as ft
import utils

from services.job import job_service


class JobType:
    def __init__(self, on_delete, text: str = '', id=None):
        self.is_editing = id is None
        self.text = text
        self.error = False
        self.id = id
        self.on_delete = on_delete

        del_btn = ft.IconButton(
            ft.icons.DELETE_OUTLINE,
            tooltip="Удалить",
            on_click=self.delete,
        )

        if (self.id is not None) and job_service.is_job_type_using(self.id):
            del_btn.disabled = True
            del_btn.tooltip = 'Невозможно удалить, т.к. этот вид используется'

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            visible=not self.is_editing,
            controls=[
                ft.Text(self.text),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Редактировать",
                            on_click=self.toggle_editing
                        ),
                        del_btn
                    ],
                ),
            ],
        )

        self.input = ft.TextField(expand=1, value=self.text, on_focus=self.on_focus_input, dense=True)

        self.edit_view = ft.Row(
            visible=self.is_editing,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.input,
                ft.IconButton(
                    icon=ft.icons.DONE,
                    tooltip="Сохранить",
                    on_click=self.save
                ),
            ],
        )

        self.component = ft.Column(controls=[self.display_view, self.edit_view], data=self.id)

    def on_focus_input(self, e=None):
        if self.error:
            self.error = False
            self.input.error_text = None
            self.component.update()

    def toggle_editing(self, e=None):
        self.is_editing = not self.is_editing
        self.display_view.visible = not self.is_editing
        self.edit_view.visible = self.is_editing
        if not self.is_editing:
            self.error = False
            self.input.error_text = None

        self.component.update()

    def save(self, e):
        if self.input.value.strip() == '':
            self.error = True
            self.input.error_text = 'Введите значение'
            self.component.update()
            return

        self.text = self.input.value.strip()
        self.display_view.controls[0].value = self.text
        self.toggle_editing()

        if self.id is None:
            self.id = job_service.create_job_type(name=self.text)['id']
            self.component.data = self.id
            return
        job_service.update_job_type(self.id, name=self.text)

    def delete(self, e):
        job_service.delete_job_type(self.id)
        self.on_delete(self.id)


class JobTypeModal:
    def __init__(self, page: ft.Page, close_event):
        self.page = page
        self.close_event = close_event

        self.form = ft.Column(controls=[], height=400, width=500)
        for i in job_service.get_jobs_types_with_id():
            self.form.controls.append(JobType(self.on_type_delete, i['name'], i['id']).component)

        self.dialog = ft.AlertDialog(
            title=ft.Row([ft.Text("Управление видами работ"), ft.IconButton(
                icon=ft.icons.ADD,
                tooltip="Добавить",
                on_click=self.add_type
            )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=self.form,
            actions=[
                ft.TextButton("ОК", style=utils.DEFAULT_BTN_STYLE, on_click=self.close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )

    def add_type(self, e):
        self.form.controls.append(JobType(self.on_type_delete).component)
        self.dialog.update()
        self.form.controls[-1].controls[-1].controls[0].focus()

    def on_type_delete(self, e):
        for idx, i in enumerate(self.form.controls):
            if i.data == e:
                self.form.controls.pop(idx)
                self.dialog.update()
                return

    def open(self):
        self.dialog.open = True

    def close(self, e=None):
        self.dialog.open = False
        self.close_event()
