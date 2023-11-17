import flet as ft
from utils import *

def main(page: ft.Page):
    page.title = "Мероприятия"

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    i = 0

    def add_clicked(e):
        nonlocal i
        lv.controls.append(ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(str(i)),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                        ),
                    ],
                ),
            ],
        ))

        i += 1
        page.update()

    def on_change(e):
        print(tabs.selected_index)

    page.theme_mode = ft.ThemeMode.LIGHT

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[ft.Tab(text=x) for x in CATEGORIES],
        on_change=on_change
    )

    page.add(tabs)

    page.add(lv)

    page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))


ft.app(target=main)
