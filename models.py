from database import Base

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Float, String, Text

class Users(Base):
    __tablename__ = "Users"
    
    UserId = Column(Integer, primary_key=True)
    Username = Column(String, unique=True)
    Password = Column(String)

    def to_dict(self):
        return {
            "UserId": self.UserId,
            "Username": self.Username,
        }

class Items(Base):
    __tablename__ = "Items"
    
    ItemId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey("Users.UserId"))
    Name = Column(String)
    Description = Column(Text)
    Price = Column(Float)

    def to_dict(self):
        return {
            "ItemId": self.ItemId,
            "UserId": self.UserId,
            "Name": self.Name,
            "Description": self.Description,
            "Price": self.Price,
        }