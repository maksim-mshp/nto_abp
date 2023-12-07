from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class ClubType(Base):
    __tablename__ = 'clubs_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
