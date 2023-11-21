import flet as ft
from datetime import datetime

from sqlalchemy import inspect


CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']

JOB_STATUSES = ['Черновик', 'К работе', 'Выполнено']

DEFAULT_BTN_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=10),
    padding=15
)


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def get_formatted_date(date: datetime) -> str:
    return date.strftime('%d.%m.%Y')

