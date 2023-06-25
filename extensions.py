from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

DATABASE_HOST = settings.DATABASE_HOST
DATABASE_PORT = settings.DATABASE_PORT
DATABASE_USER = settings.DATABASE_USER
DATABASE_PASSWORD = settings.DATABASE_PASSWORD
DATABASE_NAME = settings.DATABASE_NAME

engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
