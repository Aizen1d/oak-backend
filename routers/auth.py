from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from typing import Annotated

from sqlalchemy.orm import Session

from dependencies.auth import Token
from dependencies.auth import VerifyToken
from dependencies.auth import User
from dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies.auth import authenticate_user
from dependencies.auth import get_current_user
from dependencies.auth import verify_token
from dependencies.auth import create_access_token
from dependencies.auth import hash_password
from dependencies.database import get_db

from models import Users

auth = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

@auth.post("/signup", tags=["auth"])
def signup_user(data: User, db: Session = Depends(get_db)):
  try:
    if db.query(Users).filter(Users.Username == data.username).first():
        return JSONResponse(status_code=200, content={"reason": "existing", "message": "User already exists."})
    
    new_user = Users(Username=data.username, Password=hash_password(data.password))
    db.add(new_user)
    db.commit()
    
    return JSONResponse(status_code=201, content={"message": "User created successfully."})
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
  finally:
    db.close()

@auth.post("/login", tags=["auth"])
async def login_for_access_token(form_data: User, response: Response):
  user_data = User(username=form_data.username, password=form_data.password)
  user = authenticate_user(user_data) 

  if not user:
    return JSONResponse(content={'status': 'error', 'message': 'Invalid username or password'}, status_code=401)
  
  access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
  access_token = create_access_token(
      data={"sub": user.Username}, expires_delta=access_token_expires
  )

  # return a httpOnly cookie with the access token
  response.set_cookie(key="access_token", 
                      value=access_token,
                      samesite="none", 
                      secure=True, 
                      httponly=True, 
                      expires=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                      max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                      domain="oakfrontend-6fkfw.ondigitalocean.app"
                      )

  return {"status": "success", "message": "Login successful", "data": {"access_token": access_token}}

@auth.post("/logout", tags=["auth"])
def logout(response: Response):
  response.delete_cookie("access_token")
  return {"status": "success", "message": "Logout successful"}

@auth.post("/token-verify", tags=["auth"])
def verify_token_received(data: VerifyToken):
  try:
    payload = verify_token(data.token)
    if payload:
      return JSONResponse(content={'status': 'success', 'message': 'Token is valid'}, status_code=200)
    else:
      return JSONResponse(content={'status': 'error', 'message': 'Token is invalid or expired'}, status_code=401)
  except InvalidTokenError:
    return JSONResponse(content={'status': 'error', 'message': 'Token is invalid or expired'}, status_code=401)

@auth.get("/users/me", tags=["auth"])
async def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user.to_dict()