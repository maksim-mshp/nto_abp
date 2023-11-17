from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.job_room import JobRoom
from models.job_type import JobType


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]

    job_type_id: Mapped[int] = mapped_column(ForeignKey("jobs_type.id"))
    job_type: Mapped["JobType"] = relationship("JobType")

    job_room_id: Mapped[int] = mapped_column(ForeignKey("jobs_room.id"))
    job_room: Mapped["JobRoom"] = relationship("JobRoom")

    registration_date: Mapped[datetime] = mapped_column(default=datetime.now())
    deadline: Mapped[datetime]
    status: Mapped[str]  # строка по типу (создано, к работе, выполнено)
