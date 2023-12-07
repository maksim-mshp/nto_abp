from core.database import session_maker
from repositories.base import BaseRepository
from models.schedule import Schedule


class ScheduleRepository(BaseRepository):
    model = Schedule

    def get_list_items_by_filter(self, **kwargs):
        with session_maker() as session:
            items = session.query(self.model).filter_by(**kwargs).order_by(self.model.date_time).all()
            return items
