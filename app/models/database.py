from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    
    try:
        yield db
        
    finally:
        db.close()

class Base(DeclarativeBase):
    pass
