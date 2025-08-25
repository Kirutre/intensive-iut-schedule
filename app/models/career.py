from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Career(Base):
    __tablename__ = 'career'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    def __repr__(self) -> str:
        return f'''Career (id={self.id!r}, name={self.name!r})'''
