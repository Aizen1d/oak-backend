from pydantic import BaseModel

""" Types """
class ItemsCreate(BaseModel):
  Name: str
  Description: str
  Price: float

class ItemsUpdate(BaseModel):
  ItemId: int
  Name: str
  Description: str
  Price: float

class ItemsDelete(BaseModel):
  ItemId: int

#################################################################
""" Methods """

def validate_create_item(item: ItemsCreate):
  if not item.Name:
    return False
  
  if not item.Description:
    return False
  
  if not item.Price or item.Price < 0:
    return False
  
  return True

def validate_update_item(item: ItemsUpdate):
  if not item.ItemId:
    return False
  
  if not item.Name:
    return False
  
  if not item.Description:
    return False
  
  if not item.Price or item.Price < 0:
    return False
  
  return True
  
