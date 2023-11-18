from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class JobType(Base):
    __tablename__ = 'jobs_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
