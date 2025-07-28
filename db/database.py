from sqlalchemy import create_engine    # wraps around the database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # base class for  models to inherit from, so that we know which data models we have in DB

from core.config import settings

enginer = create_engine(
    settings.DATABASE_URL,  # database url
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=enginer)  # session to interact with the database

Base = declarative_base()  # base class for our models to inherit from, so that we know which data models we have in DB


def get_db():
    db = SessionLocal()
    try:
        yield db    # yield db allows us to use this function as a dependency in FastAPI routes
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=enginer)  # create all tables in the database based on the models we have defined