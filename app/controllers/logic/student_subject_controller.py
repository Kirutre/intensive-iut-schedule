from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.student_subject import StudentSubject

from controllers.logic.student_controller import StudentController
from controllers.logic.subject_schedule_controller import SubjectScheduleController

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class SubjectScheduleController:
    def __init__(self, session: Session, model: StudentSubject = StudentSubject,
                 student_controller: StudentController = StudentController,
                 subject_schedule_controller: SubjectScheduleController = SubjectScheduleController
                 ):
        self._session = session
        self._model = model
        self._student_controller = student_controller
        self._subject_schedule_controller = subject_schedule_controller
        
    def create(self, data: dict[str, int]) -> None:
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        self._validate(data)
        
        student_subject = self._create_student_subject_object(data)
        
        try:
            self._session.add(student_subject)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'''Student with id {data['student_id']} is already attending classes from
                                               id {data['subject_schedule_id']}''')
        
    def _validate(self, data: dict[str, any]) -> None:       
        try:
            student = self._student_controller.get_by_id(data['student_id'])
            subject_schedule = self._subject_schedule_controller.get_by_id(data['subject_schedule_id'])
                    
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'''Student {student.name} or subject_schedule with id {subject_schedule.id} not found''')
        
        if self.exists(data):
            raise ObjectAlreadyExistsException(f'''Student {student.name} is already attending classes from
                                               id {subject_schedule.id}''')
        
    def _create_student_subject_object(self, data: dict[str, any]) -> StudentSubject:
        return StudentSubject(
            student_id=data['student_id'],
            subject_schedule_id=data['subject_schedule_id']
        )
        
    def get_by_id(self, id: int) -> StudentSubject:
        statement = select(self._model).where(self._model.id == id)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Student_subject with id "{id}" not found')
        
        return result
        
    def get_by_student(self, student_id: int) -> list[StudentSubject]:
        try:
            student = self._student_controller.get_by_id(student_id)
            
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'Student with id "{student_id}" not found')
        
        statement = select(self._model).where(self._model.student_id == student.id)
        
        result = self._session.execute(statement).scalars().all()
        
        if result is None:
            raise ObjectNotFoundException(f'Student_subject for student "{student.name}" not found')
        
        return result
    
    def get_all(self) -> list[StudentSubject]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def exists(self, data: dict[str, any]) -> bool:
        statement =  and_(self._model.student_id == data['student_id'],
                          self._model.subject_schedule_id == data['subject_schedule_id']).exists()
        
        return self._session.scalar(statement)
