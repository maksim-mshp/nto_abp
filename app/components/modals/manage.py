import flet as ft

import utils


class Object:
    def __init__(self, on_delete, check_is_using, create, update, delete, text: str = '', id=None):
        self.is_editing = id is None
        self.text = text
        self.error = False
        self.id = id
        self.on_delete = on_delete
        self.check_is_using = check_is_using
        self.create = create
        self.update = update
        self.delete = delete

        del_btn = ft.IconButton(
            ft.icons.DELETE_OUTLINE,
            tooltip="Удалить",
            on_click=self._delete,
        )

        if (self.id is not None) and self.check_is_using(self.id):
            del_btn.disabled = True
            del_btn.tooltip = 'Невозможно удалить, т.к. объект используется'

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
                            on_click=self._toggle_editing
                        ),
                        del_btn
                    ],
                ),
            ],
        )

        self.input = ft.TextField(expand=1, value=self.text, on_focus=self._on_focus_input, dense=True)

        self.edit_view = ft.Row(
            visible=self.is_editing,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.input,
                ft.IconButton(
                    icon=ft.icons.DONE,
                    tooltip="Сохранить",
                    on_click=self._save
                ),
            ],
        )

        self.component = ft.Column(controls=[self.display_view, self.edit_view], data=self.id)

    def _on_focus_input(self, e=None):
        if self.error:
            self.error = False
            self.input.error_text = None
            self.component.update()

    def _toggle_editing(self, e=None):
        self.is_editing = not self.is_editing
        self.display_view.visible = not self.is_editing
        self.edit_view.visible = self.is_editing
        if not self.is_editing:
            self.error = False
            self.input.error_text = None

        self.component.update()

    def _save(self, e):
        if self.input.value.strip() == '':
            self.error = True
            self.input.error_text = 'Введите значение'
            self.component.update()
            return

        self.text = self.input.value.strip()
        self.display_view.controls[0].value = self.text
        self._toggle_editing()

        if self.id is None:
            self.id = self.create(self.text)['id']
            self.component.data = self.id
            return
        self.update(self.id, self.text)

    def _delete(self, e):
        self.delete(self.id)
        self.on_delete(self.id)


class ManageModal:
    def __init__(self, page: ft.Page, close_event):
        self.page = page
        self.close_event = close_event

        self.title = ''
        self.objects = []

        self.form = None
        self.dialog = None

    @staticmethod
    def check_is_using(id: int) -> bool:
        pass

    @staticmethod
    def create(title: str) -> dict:
        pass

    @staticmethod
    def update(id: int, title: str):
        pass

    @staticmethod
    def delete(id: int):
        pass

    def init(self):
        self.form = ft.Column(controls=[], height=400, width=500, scroll=ft.ScrollMode.ADAPTIVE, expand=1)
        for i in self.objects:
            self.form.controls.append(
                Object(self.on_type_delete, self.check_is_using, self.create, self.update, self.delete, i['name'],
                       i['id']).component)

        self.dialog = ft.AlertDialog(
            title=ft.Row([ft.Text(self.title), ft.IconButton(
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
        self.form.controls.append(
            Object(self.on_type_delete, self.check_is_using, self.create, self.update, self.delete).component)
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
