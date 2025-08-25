from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base

from app.utils.day_of_week import DayOfWeek


class Schedule(Base):
    __tablename__ = 'schedule'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[Time] = mapped_column(nullable=False)
    end_time: Mapped[Time] = mapped_column(nullable=False)
    day: Mapped[DayOfWeek] = mapped_column(String(10), nullable=False)
    
    def __repr__(self) -> str:
        return f'''Schedule (id={self.id!r}, start_time={self.start_time!r},
                    end_time={self.end_time!r}, day={self.day!r})'''
