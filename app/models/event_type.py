from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class EventType(Base):
    __tablename__ = 'events_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
