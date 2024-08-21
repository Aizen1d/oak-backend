from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv 
load_dotenv()

import os

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()