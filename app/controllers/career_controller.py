from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from models.database import Session
from models.career import Career

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


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
            
            raise ObjectAlreadyExistsException(f'Career "{name}" already exists')

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
        
        return self._session.scalar(statement)
    
    def get_all(self) -> list[Career]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def update(self, old_name: str, new_name: str) -> None:
        new_name = self._sanitize(new_name)
        
        if not self.exists(old_name):
            raise ObjectNotFoundException(f'Career "{old_name}" not found')
        
        if self.exists(new_name):
            raise ObjectAlreadyExistsException(f'Career "{new_name}" already exists')
        
        statement = update(self._model).where(self._model.name == old_name).values(name=new_name)
        
        try:
            self._session.execute(statement)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Career "{new_name}" already exists')
        
    def exists(self, name: str) -> bool:
        statement = select(self._model.id).where(self._model.name == name).exists()
        
        return self._session.query(statement).scalar()
