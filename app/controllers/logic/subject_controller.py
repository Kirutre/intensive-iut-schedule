from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.subject import Subject

from controllers.logic.career_controller import CareerController

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class SubjectController:
    def __init__(self, session: Session, model: Subject = Subject,
                 career_controller: CareerController = CareerController
                 ):
        self._session = session
        self._model = model
        self._career_controller = career_controller
        
    def create(self, data: dict[str, str]) -> None:
        sanitize_name = self._sanitize(data)
        
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        validate_data = self._validate(data, sanitize_name)
        
        subject = self._create_subject_object(validate_data)
        
        try:
            self._session.add(subject)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Subject "{sanitize_name}" already exists')

    def _sanitize(self, data: dict[str, any]) -> str:
        return data['name'].strip()
        
    def _validate(self, data: dict[str, any], name: str) -> dict[str, any]:
        if self.exists(name):
            raise ObjectAlreadyExistsException(f'Subject "{name}" already exists')
        
        try:
            career = self._career_controller.get_by_id(data['career_id'])
        
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'Career with id {data['career_id']} not found')
        
        return {'name': name, 'course': data['course'], 'career_id': career.id}
        
    def _create_subject_object(self, data: dict[str, any]) -> Subject:
        return Subject(
            name=data['name'],
            course=data['course'],
            career_id=data['career_id']
        )
        
    def get_by_name(self, name: str) -> Subject:
        statement = select(self._model).where(self._model.name == name)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Subject "{name}" not found')
        
        return result
        
    def get_by_career(self, career_id: int) -> list[Subject]:
        try:
            career = self._career_controller.get_by_id(career_id)
            
        except ObjectNotFoundException:
            raise ObjectNotFoundException(f'Career with id "{career_id}" not found')
        
        statement = select(self._model).where(self._model.career_id == career.id)
        
        result = self._session.execute(statement).scalars().all()
        
        if result is None:
            raise ObjectNotFoundException(f'Subject of career "{career.name}" not found')
        
        return result
    
    def get_all(self) -> list[Subject]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def exists(self, name: str) -> bool:
        statement = select(self._model.id).where(self._model.name == name).exists()
        
        return self._session.scalar(statement)
