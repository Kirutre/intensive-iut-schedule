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
        self._validate(data, day)
        
        schedule = self._create_schedule_object(data, day)
        
        try:
            self._session.add(schedule)
            self._session.commit()
            
        except IntegrityError:
            self._session.rollback()
            
            raise ObjectAlreadyExistsException(f'Schedule block already exists')
    
    def _sanitize(self, data: dict[str, any]) -> str:
        return data['day'].strip().lower().capitalize()
    
    def _validate(self, data: dict[str, any], day: str) -> None:       
        try:
            datetime.strptime(data['start_time'], self.FORMAT)
            datetime.strptime(data['end_time'], self.FORMAT)
            
            DayOfWeek(day)
            
        except ValueError as e:
            raise ValueError(f'Invalid input data: {e}')
        
        if data['start_time'] > data['end_time']:
            raise ValueError('The start time cannot be greater than the end time')

        if self.exists(data, day):
            raise ObjectAlreadyExistsException(f'Schedule block already exists')
        
    def _create_schedule_object(self, data: dict[str, any], day: str) -> Schedule:
        #* can be return self.model(**data)
        
        return Schedule(
            start_time = data['start_time'],
            end_time = data['end_time'],
            day = DayOfWeek(day)
        )
        
    def get_by_start_time(self, start_time: Time) -> Schedule:
        statement = select(self._model).where(self._model.start_time == start_time)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'No Schedule found with start time {start_time}')
        
        return result
        
    def get_by_end_time(self, end_time: Time) -> Schedule:
        statement = select(self._model).where(self._model.end_time == end_time)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'No Schedule found with end time {end_time}')
        
        return result
        
    def get_by_day(self, day: DayOfWeek) -> Schedule:        
        statement = select(self._model).where(self._model.day == day)
        
        result = self._session.scalar(statement)
        
        if result is None:
            raise ObjectNotFoundException(f'No Schedule found with {day} as the day')
        
        return result
    
    def get_all(self) -> list[Schedule]:
        return self._session.execute(select(self._model)).scalars().all()
        
    def exists(self, data: dict[str, any], day: DayOfWeek) -> bool:
        statement = select(self._model.id).where(
            self._model.start_time == data['start_time'],
            self._model.end_time == data['end_time'],
            self._model.day == day
        ).exists()
        
        return self._session.scalar(statement)
