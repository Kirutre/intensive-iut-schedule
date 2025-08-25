from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class SubjectSchedule(Base):
    __tablename__ = 'subject_schedule'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    section: Mapped[str] = mapped_column(nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'), nullable=False)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.id'), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'''SubjectSchedule (id={self.id!r}, section={self.section!r},
                    subject_id={self.subject_id!r}, schedule_id={self.schedule_id!r},
                    teacher_id={self.teacher_id!r})'''
