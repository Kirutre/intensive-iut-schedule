from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.database import Session
from models.career import Career

from utils.exceptions import ObjectAlreadyExistsException


class CareerController:
    def __init__(self, model: Career = Career):
        self._session = Session()
        self._model = model
        
    def create(self, name: str) -> None:
        name = self._sanitize(name)
        
        self._validate(name)
        
        career = self._create_career_object(name)
        
        try:
            self._session.add(career)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Career "{name}", already exists')

    def _sanitize(self, name: str) -> str:
        return name.strip()
        
    def _validate(self, name: str) -> None:
        if self.exists(name):
            raise ObjectAlreadyExistsException(f'Career "{name}", already exists')
        
    def _create_career_object(self, name: str) -> Career:
        return Career(
            name=name
        )
    
    def exists(self, name: str) -> bool:
        statement = select(self._model.id).where(self._model.name == name).exists()
        
        return self._session.query(statement).scalar()
