from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.room import Room
from models.event import Event


class Schedule(Base):
    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(primary_key=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped["Room"] = relationship("Room", lazy="joined")

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship("Event", lazy="joined")

    date_time: Mapped[datetime]
    weekday: Mapped[int]
