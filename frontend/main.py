import flet as ft


def main(page: ft.Page):
    page.title = "Мероприятия"

    def add_clicked(e):
        page.update()

    def on_change(e):
        print(tabs.selected_index)

    page.theme_mode = ft.ThemeMode.LIGHT

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[ft.Tab(text="Развлечения"), ft.Tab(text="Просвещение"), ft.Tab(text="Образование")],
        on_change=on_change
    )

    page.add(tabs)

    page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))


ft.app(target=main)
