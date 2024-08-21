from database import Base

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = "Users"
    
    UserId = Column(Integer, primary_key=True)
    Username = Column(String, unique=True)
    Password = Column(String)

class Items(Base):
    __tablename__ = "Items"
    
    ItemId = Column(Integer, primary_key=True)
    Name = Column(String)
    Description = Column(Text)
    Price = Column(Float)