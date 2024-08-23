from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from typing import Annotated

from sqlalchemy.orm import Session

from dependencies.auth import Token
from dependencies.auth import User
from dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies.auth import authenticate_user
from dependencies.auth import get_current_user
from dependencies.auth import create_access_token
from dependencies.auth import hash_password
from dependencies.database import get_db

from models import Users

auth = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

@auth.post("/register", tags=["auth"])
def register_user(data: User, db: Session = Depends(get_db)):
  try:
    if db.query(Users).filter(Users.Username == data.username).first():
        return JSONResponse(status_code=400, content={"message": "User already exists."})
    
    new_user = Users(Username=data.username, Password=hash_password(data.password))
    db.add(new_user)
    db.commit()
    
    return JSONResponse(status_code=201, content={"message": "User created successfully."})
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
  finally:
    db.close()

@auth.post("/login")
async def login_for_access_token(form_data: User) -> Token:
  user_data = User(username=form_data.username, password=form_data.password)
  user = authenticate_user(user_data) 

  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Bearer"},
      )
  
  access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
  access_token = create_access_token(
      data={"sub": user.Username}, expires_delta=access_token_expires
  )

  return {
      "access_token": access_token,
      "token_type": "bearer",
  }

@auth.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user.to_dict()