from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.teacher import Teacher

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class TeacherController:
    def __init__(self, session: Session, model: Teacher = Teacher):
        self._session = session
        self._model = model
        
    def create(self, data: dict[str, str]) -> None:
        sanitize_data = self._sanitize(data)
        
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        self._validate(sanitize_data)
        
        teacher = self._create_teacher_object(sanitize_data)
        
        try:
            self._session.add(teacher)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Teacher with identification number "{data['identification_number']}" already exists')

    def _sanitize(self, data: dict[str, str]) -> dict[str, str]:
        name = data['name'].strip()
        identification_numer = data['identification_number'].strip().upper().replace('-', '')
        
        return {'name': name, 'identification_number': identification_numer}
        
    def _validate(self, data: dict[str, str]) -> None:
        if self.exists(data['identification_number']):
            raise ObjectAlreadyExistsException(f'Teacher with identification number "{data['identification_number']}" already exists')
        
    def _create_teacher_object(self, data: dict[str, str]) -> Teacher:
        return Teacher(
            name=data['name'],
            identification_number=data['identification_number']
        )
        
    def get_by_name(self, name: str) -> Teacher:
        statement = select(self._model).where(self._model.name == name)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Teacher "{name}" not found')
        
        return result
        
    def get_by_identification_number(self, identification_number: str) -> Teacher:
        statement = select(self._model).where(self._model.identification_number == identification_number)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Teacher with identification number "{identification_number}" not found')
        
        return result
    
    def get_all(self) -> list[Teacher]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def update(self, old_name: str, new_name: str) -> None:
        sanitize_new_name = new_name.strip()
        
        teacher = self.get_by_name(old_name)
        
        teacher.name = sanitize_new_name
        
        self._session.commit()
        
    def exists(self, identification_number: str) -> bool:
        statement = select(self._model.id).where(self._model.identification_number == identification_number).exists()
        
        return self._session.scalar(statement)
