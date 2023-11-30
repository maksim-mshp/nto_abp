from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.room import Room
from models.job_type import JobType
from models.event import Event


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship("Event", lazy="joined")

    job_type_id: Mapped[int] = mapped_column(ForeignKey("jobs_type.id"))
    job_type: Mapped["JobType"] = relationship("JobType", lazy="joined")

    job_room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    job_room: Mapped["Room"] = relationship("Room", lazy="joined")

    registration_date: Mapped[datetime] = mapped_column(default=datetime.now())
    deadline: Mapped[datetime]
    status: Mapped[str]  # строка по типу (создано, к работе, выполнено)
