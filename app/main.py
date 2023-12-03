from components.views.events import Events
from components.views.jobs import Jobs
from components.views.rooms import Rooms
from components.views.reservation import Reservation
from components.navbar import NavigationBar
from core.database import add_sample_data
from tendo import singleton
from sys import exit
import flet as ft
import utils

try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException:
    exit(-1)


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_min_width = 850
    page.window_min_height = 770
    page.window_maximized = True
    add_sample_data()

    def on_page_change(e=None, new_index=None):
        nonlocal page_index
        if e is not None:
            new_index = e.control.selected_index
        views[page_index].hide()
        views[new_index].show()
        page_index = new_index
        page.update()

    utils.on_page_change_func = on_page_change

    page_index = 0
    views = [
        Events(page),
        Jobs(page),
        Rooms(page),
        Reservation(page)
    ]

    nav = NavigationBar(page, views, on_page_change, page_index)
    views[page_index].show()

    page.add(ft.Row(
        [nav.component] + [i.component for i in views],
        expand=1
    ))

    for i in views:
        i.safe_update()


ft.app(target=main)
