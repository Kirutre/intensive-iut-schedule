from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.subject_schedule import SubjectSchedule

from controllers.logic.subject_controller import SubjectController
from controllers.logic.schedule_controller import ScheduleController
from controllers.logic.teacher_controller import TeacherController

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class SubjectScheduleController:
    def __init__(self, session: Session, model: SubjectSchedule = SubjectSchedule,
                 subject_controller: SubjectController = SubjectController,
                 schedule_controller: ScheduleController = ScheduleController,
                 teacher_controller: TeacherController = TeacherController
                 ):
        self._session = session
        self._model = model
        self._subject_controller = subject_controller
        self._schedule_controller = schedule_controller
        self._teacher_controller = teacher_controller
        
    def create(self, data: dict[str, any]) -> None:
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        self._validate(data)
        
        student_subject = self._create_subject_schedule_object(data)
        
        try:
            self._session.add(student_subject)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'''Teacher with id {data['teacher_id']} already teaches classes in the
                                               schedule with id {data['schedule_id']} or section {data['section']} already exists for
                                               the subject with id {data['subject_id']}''')
        
    def _validate(self, data: dict[str, any]) -> None:       
        try:
            subject = self._subject_controller.get_by_id(data['subject_id'])
            schedule = self._schedule_controller.get_by_id(data['schedule_id'])
            teacher = self._teacher_controller.get_by_id(data['teacher_id'])
                    
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'''Subject {subject.name} or schedule with id {schedule.id}
                                          or teacher {teacher.name} not found''')
        
        if self.exists(data):
            raise ObjectAlreadyExistsException(f'''Teacher {teacher.name} already teaches classes at time
                                               {schedule.start_time}-{schedule.end_time} or
                                               section {data['section']} already exists for the subject {subject.name}''')
        
    def _create_subject_schedule_object(self, data: dict[str, any]) -> SubjectSchedule:
        return SubjectSchedule(
            section=data['section'],
            subject_id=data['subject_id'],
            schedule_id=data['schedule_id'],
            teacher_id=data['teacher_id']
        )
        
    def get_by_id(self, id: int) -> SubjectSchedule:
        statement = select(self._model).where(self._model.id == id)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Subject_schedule with id "{id}" not found')
        
        return result
        
    def get_by_subject(self, subject_id: int) -> list[SubjectSchedule]:
        try:
            subject = self._subject_controller.get_by_id(subject_id)
            
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'Subject with id "{subject_id}" not found')
        
        statement = select(self._model).where(self._model.subject_id == subject.id)
        
        result = self._session.execute(statement).scalars().all()
        
        if result is None:
            raise ObjectNotFoundException(f'Subject_schedule for subject "{subject.name}" not found')
        
        return result
    
    def get_by_subject_schedule(self, subject_id: int, schedule_id: int) -> SubjectSchedule:
        try:
            subject = self._subject_controller.get_by_id(subject_id)
            schedule = self._schedule_controller.get_by_id(schedule_id)
            
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'Subject with id "{subject_id}" or schedule with id {schedule_id} not found')
        
        statement = select(self._model).where(and_(self._model.subject_id == subject.id,
                                                   self._model.schedule_id == schedule_id))
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'''Subject_schedule for subject "{subject.name}" and
                                          schedule {schedule.start_time}-{schedule.end_time} not found''')
        
        return result
    
    def get_all(self) -> list[SubjectSchedule]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def exists(self, data: dict[str, any]) -> bool:
        section_exists =  and_(self._model.section == data['section'],
                               self._model.subject_id == data['subject_id'])
        
        teacher_ocuppied = and_(self._model.teacher_id == data['teacher_id'],
                                self._model.schedule_id == data['schedule_id'])
        
        statement = select(self._model.id).where(or_(section_exists,
                                                     teacher_ocuppied
                                                     )).exists()
        
        return self._session.scalar(statement)
