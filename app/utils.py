import flet as ft
from datetime import datetime
from sqlalchemy import inspect

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']

JOB_STATUSES = ['Создана', 'К выполнению', 'Выполнена']

DEFAULT_BTN_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=10),
    padding=15
)

on_page_change_func = None


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def get_formatted_date(date: datetime | None) -> str | None:
    if date is None:
        return None
    return date.strftime('%d.%m.%Y')


def truncate_text(s: str, max_length: int = 50) -> str:
    if len(s) <= max_length:
        return s
    return s[:max_length] + '...'
