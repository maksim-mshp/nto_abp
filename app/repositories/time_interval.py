from datetime import datetime, timedelta

import sqlalchemy

from core.database import session_maker
from repositories.base import BaseRepository
from models.time_interval import TimeInterval


class TimeIntervalRepository(BaseRepository):
    model = TimeInterval

    def create(self, reservation_id: int, intervals: list[datetime]):
        with session_maker() as session:
            for interval in intervals:
                item = self.model(reservation_id=reservation_id,
                                  start_date_time=interval,
                                  end_date_time=interval+timedelta(hours=1)
                                  )
                session.add(item)
            session.commit()
            return item

    def get_all_by_datetime(self, date_time: datetime):
        with session_maker() as session:
            objects_on_date = session.query(self.model).filter(
                sqlalchemy.func.date(TimeInterval.start_date_time) == date_time.date()
            ).all()
            return objects_on_date
