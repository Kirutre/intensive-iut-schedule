from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.career import Career

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class CareerController:
    def __init__(self, session: Session, model: Career = Career):
        self._session = session
        self._model = model
        
    def create(self, name: str) -> None:
        sanitize_name = self._sanitize(name)
        
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        self._validate(sanitize_name)
        
        career = self._create_career_object(sanitize_name)
        
        try:
            self._session.add(career)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Career "{sanitize_name}" already exists')

    def _sanitize(self, name: str) -> str:
        return name.strip()
        
    def _validate(self, name: str) -> None:
        if self.exists(name):
            raise ObjectAlreadyExistsException(f'Career "{name}" already exists')
        
    def _create_career_object(self, name: str) -> Career:
        return Career(
            name=name
        )
        
    def get_by_name(self, name: str) -> Career:
        statement = select(self._model).where(self._model.name == name)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'Career "{name}" not found')
        
        return result
    
    def get_all(self) -> list[Career]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def update(self, old_name: str, new_name: str) -> None:
        new_name = self._sanitize(new_name)
        
        if self.exists(new_name):
            raise ObjectAlreadyExistsException(f'Career "{new_name}" already exists')
        
        career = self.get_by_name(old_name)
        
        career.name = new_name
        
        try:
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Career "{new_name}" already exists')
        
    def exists(self, name: str) -> bool:
        statement = select(self._model.id).where(self._model.name == name).exists()
        
        return self._session.scalar(statement)
