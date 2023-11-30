from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class TimeInterval(Base):
    __tablename__ = 'time_intervals'

    id: Mapped[int] = mapped_column(primary_key=True)

    start_date_time: Mapped[datetime]
    end_date_time: Mapped[datetime]

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))
