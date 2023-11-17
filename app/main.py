import flet as ft
from utils import *
from components.MainView import MainView


def main(page: ft.Page):
    page.title = "Мероприятия"
    page.theme_mode = ft.ThemeMode.LIGHT

    main_view = MainView(page)


ft.app(target=main)
