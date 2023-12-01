from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

from models.room import Room
from models.event import Event


class Reservation(Base):
    __tablename__ = 'reservation'

    id: Mapped[int] = mapped_column(primary_key=True)

    half_reservation: Mapped[bool] = mapped_column(default=False)

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped["Room"] = relationship("Room", lazy="joined")

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship("Event", lazy="joined")

    intervals: Mapped[list["TimeInterval"] | None] = relationship(back_populates="reservation",
                                                                  lazy='joined',
                                                                  cascade="all,delete")
