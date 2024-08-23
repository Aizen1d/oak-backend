from database import Base

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Float, String, Text

class Users(Base):
    __tablename__ = "Users"
    
    UserId = Column(Integer, primary_key=True)
    Username = Column(String, unique=True)
    Password = Column(String)

class Items(Base):
    __tablename__ = "Items"
    
    ItemId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey("Users.UserId"))
    Name = Column(String)
    Description = Column(Text)
    Price = Column(Float)