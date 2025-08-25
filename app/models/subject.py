from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Subject(Base):
    __tablename__ = 'subject'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    career_id: Mapped[int] = mapped_column(ForeignKey('career.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'''Subject (id={self.id!r}, name={self.name!r},
                    course={self.course!r}, career_id={self.career_id!r})'''
