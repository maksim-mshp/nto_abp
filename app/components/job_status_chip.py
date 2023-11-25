import flet as ft
from utils import JOB_STATUSES


class JobStatusChip:
    def __init__(self, status_id: int):
        self.status_id = status_id
        self.status = JOB_STATUSES[self.status_id]

        colors = {
            0: {
                'color': ft.colors.BLACK,
                'bgcolor': ft.colors.WHITE,
                'border': ft.colors.BLACK,
            },
            1: {
                'color': ft.colors.BLACK,
                'bgcolor': ft.colors.PINK_ACCENT_200,
                'border': ft.colors.PINK_ACCENT_200,
            },
            2: {
                'color': ft.colors.BLACK,
                'bgcolor': ft.colors.GREY_400,
                'border': ft.colors.GREY_400,
            }
        }

        self.color = colors[self.status_id]

        self.text = ft.Text(self.status, color=self.color['color'], bgcolor=self.color['bgcolor'])
        self.chip = ft.Container(self.text, padding=ft.Padding(top=5, bottom=5, left=15, right=15),
                                 bgcolor=self.color['bgcolor'], border_radius=10,
                                 data=self.status_id,
                                 border=ft.Border(*[ft.BorderSide(1, self.color['border']) for _ in range(4)]))
