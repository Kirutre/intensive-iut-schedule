from datetime import datetime

from sqlalchemy import select, Time
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.schedule import Schedule

from utils.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from utils.day_of_week import DayOfWeek


class ScheduleController:
    FORMAT = '%H:%M:%S' #* 24 hours format
    
    def __init__(self, session: Session, model: Schedule = Schedule):
        self._session = session
        self._model = model
        
    def create(self, data: dict[str, any]) -> None:
        day = self._sanitize(data)
        
        #! Modify the DB so that the respective fields are UNIQUE (eliminate this method if necessary)
        validate_data = self._validate(data, day)
        
        schedule = self._create_schedule_object(validate_data)
        
        try:
            self._session.add(schedule)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Schedule block already exists')
    
    def _sanitize(self, data: dict[str, any]) -> str:
        return data['day'].strip().lower().capitalize()
    
    #* validates and converts data
    def _validate(self, data: dict[str, any], day: str) -> dict[str, any]:       
        try:
            start_time = datetime.strptime(data['start_time'], self.FORMAT).time()
            end_time = datetime.strptime(data['end_time'], self.FORMAT).time()
            
            DayOfWeek(day)
            
        except ValueError as e:
            raise ValueError(f'Invalid input data: {e}')
        
        if start_time > end_time:
            raise ValueError('The start time cannot be greater than the end time')

        if self.exists(data, day):
            raise ObjectAlreadyExistsException(f'Schedule block already exists')
        
        return {'start_time': start_time, 'end_time': end_time, 'day': DayOfWeek(day)}
        
    def _create_schedule_object(self, data: dict[str, any]) -> Schedule:
        #* can be return self.model(**data)
        
        return Schedule(
            start_time = data['start_time'],
            end_time = data['end_time'],
            day = data['day']
        )
    
    def get_all(self) -> list[Schedule]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def exists(self, data: dict[str, any], day: DayOfWeek) -> bool:
        statement = select(self._model.id).where(
            self._model.start_time == data['start_time'],
            self._model.end_time == data['end_time'],
            self._model.day == day
        ).exists()
        
        return self._session.scalar(statement)
