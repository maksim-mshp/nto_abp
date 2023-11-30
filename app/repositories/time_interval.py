from datetime import datetime, timedelta

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
