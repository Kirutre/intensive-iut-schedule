from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Teacher(Base):
    __tablename__ = 'teacher'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    identification_number: Mapped[str] = mapped_column(nullable=False)
    
    def __repr__(self) -> str:
        return f'''Teacher (id={self.id!r}, name={self.name!r},
                    identification_number={self.identification_number!r})'''
