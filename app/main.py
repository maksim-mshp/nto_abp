import flet as ft
from utils import *
from components.MainView import MainView

from core.database import engine
from core.database import Base


def main(page: ft.Page):
    page.title = "Мероприятия"
    page.theme_mode = ft.ThemeMode.LIGHT

    add_sample_data()

    main_view = MainView(page)


ft.app(target=main)
