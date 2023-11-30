from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
