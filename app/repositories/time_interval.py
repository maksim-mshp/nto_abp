from datetime import datetime, timedelta

import sqlalchemy

from core.database import session_maker
from repositories.base import BaseRepository
from models.time_interval import TimeInterval
from models.reservation import Reservation


class TimeIntervalRepository(BaseRepository):
    model = TimeInterval

    def create(self, reservation_id: int, intervals: list[datetime]):
        with session_maker() as session:
            for interval in intervals:
                item = self.model(reservation_id=reservation_id,
                                  start_date_time=interval,
                                  end_date_time=interval + timedelta(hours=1)
                                  )
                session.add(item)
            session.commit()
            return item

    def get_all_by_date_and_room(self, date_time: datetime, room_id: int):
        with session_maker() as session:
            objects_on_date = session.query(TimeInterval).join(TimeInterval.reservation).filter(
                sqlalchemy.and_(
                    sqlalchemy.func.date(TimeInterval.start_date_time) == date_time.date(),
                    Reservation.room_id == room_id
                )
            ).all()
            return objects_on_date

    def get_all_by_room(self, room_id: int):
        with session_maker() as session:
            objects_on_date = session.query(TimeInterval).join(TimeInterval.reservation).filter(
                    Reservation.room_id == room_id
            ).all()
            return objects_on_date
