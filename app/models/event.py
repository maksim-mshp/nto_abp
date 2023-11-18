from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.event_type import EventType


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    date: Mapped[datetime]
    category: Mapped[str]
    event_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("events_type.id"))
    event_type: Mapped[Optional["EventType"]] = relationship("EventType", lazy="joined")
