from sqlalchemy import inspect

CATEGORIES = ['Развлечения', 'Просвещение', 'Образование']

def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }
