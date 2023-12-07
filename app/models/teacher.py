from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
