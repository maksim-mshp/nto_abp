from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.event_type import EventType
from models.teacher import Teacher
from models.club_type import ClubType


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    date: Mapped[datetime]
    category: Mapped[str]

    club_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("clubs_type.id"))
    club_type: Mapped[Optional["ClubType"]] = relationship("ClubType", lazy="joined")

    teacher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped[Optional["Teacher"]] = relationship("Teacher", lazy="joined")

    event_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("events_type.id"))
    event_type: Mapped[Optional["EventType"]] = relationship("EventType", lazy="joined")
