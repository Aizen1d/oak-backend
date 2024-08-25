from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies.database import get_db
from dependencies.auth import verify_token
from dependencies.items import ItemsCreate, ItemsUpdate, ItemsDelete, validate_create_item, validate_update_item

from models import Items, Users

items = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
)

@items.get("/")
async def fetch_all_items(token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})

        getUser = db.query(Users).filter(Users.Username == payload["sub"]).first()
        if not getUser:
            return JSONResponse(status_code=404, content={"message": "User not found."})
        
        getUserId = getUser.UserId

        items = db.query(Items).filter(Items.UserId == getUserId).all()
        
        return items
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@items.get("/{item_id}")
async def fetch_item(item_id: int, token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})
        
        item = db.query(Items).filter(Items.ItemId == item_id).first()
        if not item:
            return JSONResponse(status_code=404, content={"message": "Item not found."})

        # Check if the item belongs to the user
        getUser = db.query(Users).filter(Users.Username == payload["sub"]).first()

        if item.UserId != getUser.UserId:
            return JSONResponse(status_code=401, content={"message": "Unauthorized access."})
        
        return item
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
@items.post("/")
async def create_item(item: ItemsCreate, token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})
        
        if not validate_create_item(item):
            return JSONResponse(status_code=400, content={"message": "Invalid item data."})
        
        # Check duplicate item
        checkItem = db.query(Items).filter(Items.Name == item.Name).first()
        if checkItem:
            return JSONResponse(status_code=200, content={"reason": "existing", "message": "Item already exists."})
        
        # Associate the item with the user
        getUser = db.query(Users).filter(Users.Username == payload["sub"]).first()
        if not getUser:
            return JSONResponse(status_code=404, content={"message": "User not found."})
        
        getUserId = getUser.UserId

        new_item = Items(UserId=getUserId, 
                         Name=item.Name, 
                         Description=item.Description, 
                         Price=item.Price)
        db.add(new_item)
        db.commit()

        return JSONResponse(status_code=201, content={"message": "Item created successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    finally:
        db.close()

@items.put("/")
async def update_item(item_update: ItemsUpdate, token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})
        
        if not validate_update_item(item_update):
            return JSONResponse(status_code=400, content={"message": "Invalid item data."})

        item = db.query(Items).filter(Items.ItemId == item_update.ItemId).first()
        if not item:
            return JSONResponse(status_code=404, content={"message": "Item not found."})
        
        # Check if the item belongs to the user
        getUser = db.query(Users).filter(Users.Username == payload["sub"]).first()

        if item.UserId != getUser.UserId:
            return JSONResponse(status_code=401, content={"message": "Unauthorized access."})

        item.Name = item_update.Name
        item.Description = item_update.Description
        item.Price = item_update.Price
        db.commit()

        return JSONResponse(status_code=200, content={"message": "Item updated successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@items.delete("/")
async def delete_item(item: ItemsDelete, token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})
        
        item = db.query(Items).filter(Items.ItemId == item.ItemId).first()
        if not item:
            return JSONResponse(status_code=404, content={"message": "Item not found."})

        db.delete(item)
        db.commit()

        return JSONResponse(status_code=200, content={"message": "Item deleted successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    finally:
        db.close()