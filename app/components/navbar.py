import flet as ft


class NavigationBar:
    def __init__(self, page: ft.Page, views, on_page_change):
        self.page = page
        self.on_page_change = on_page_change
        self.views = views

        self.nav = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(i.VIEW_ICON),
                    label=i.VIEW_TITLE,
                ) for i in views
            ],
            on_change=self.on_page_change,
        )

        self.component = ft.Row(
            [
                self.nav,
                ft.VerticalDivider(width=1)
            ],
        )

    def get_index(self):
        return self.nav.selected_index



