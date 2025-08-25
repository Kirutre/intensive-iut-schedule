from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class StudentSubject(Base):
    __tablename__ = 'student_schedule'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'), nullable=False)
    subject_schedule_id: Mapped[int] = mapped_column(ForeignKey('subject_schedule.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'''StudentSubject (id={self.id!r}, student_id={self.student_id!r},
                    subject_schedule_id={self.subject_schedule_id!r})'''
