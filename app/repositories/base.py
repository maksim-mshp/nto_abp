from core.database import session_maker
from sqlalchemy.orm.exc import NoResultFound


class BaseRepository:
    model = None

    def get_item_by_filter(self, **kwargs):
        with session_maker() as session:
            item = session.query(self.model).filter_by(**kwargs).first()
            return item

    def get_list_items_by_filter(self, **kwargs):
        with session_maker() as session:
            items = session.query(self.model).filter_by(**kwargs).all()
            return items

    def create(self, **kwargs):
        with session_maker() as session:
            item = self.model(**kwargs)
            session.add(item)
            session.commit()
            return item

    def delete_by_id(self, item_id):
        with session_maker() as session:
            try:
                item = session.query(self.model).filter_by(id=item_id).one()
                session.delete(item)
                session.commit()
            except NoResultFound:
                raise ValueError(f"No item with id {item_id} found")

    def update_by_id(self, item_id, **kwargs):
        with session_maker() as session:
            try:
                item = session.query(self.model).filter_by(id=item_id).one()
                for key, value in kwargs.items():
                    setattr(item, key, value)
                session.commit()
                return item
            except NoResultFound:
                raise ValueError(f"No item with id {item_id} found")

