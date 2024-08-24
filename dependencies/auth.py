from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from dependencies.database import get_db
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users

import jwt

from dotenv import load_dotenv
load_dotenv()

import os

#################################################################
""" Utils """
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

#################################################################
""" Types """
class Token(BaseModel):
  access_token: str
  token_type: str

class VerifyToken(BaseModel):
  token: str

class TokenData(BaseModel):
  username: str | None = None

class User(BaseModel):
  username: str
  password: str

#################################################################
""" Methods """

def hash_password(password: str):
    return pwd_context.hash(password)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(data: User):
  db = SessionLocal()
  user = db.query(Users).filter(Users.Username == data.username).first()

  if not user:
      return False
  if not verify_password(data.password, user.Password):
      return False
  return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
  return encoded_jwt

def verify_token(token: str):
  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    
    return payload
  except InvalidTokenError:
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
      payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
      username: str = payload.get("sub")
      if username is None:
          raise credentials_exception
      token_data = TokenData(username=username)
  except:
      raise credentials_exception
  db = SessionLocal()
  user = db.query(Users).filter(Users.Username == token_data.username).first()

  if user is None:
      raise credentials_exception
  return user
