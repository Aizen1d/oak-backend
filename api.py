from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session

from dotenv import load_dotenv
load_dotenv()

import os 

app = FastAPI()

#################################################################
""" Settings """

tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication for users.",
    },
    {
        "name": "items",
        "description": "Items have a name, description and price.",
    },
]

app = FastAPI(
    title="API for Oak Test Assessment",
    description="This is the RESTful APIs for the Oak Test Assessment.",
    version="v1",
    docs_url="/",
    redoc_url="/redoc",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('LOCAL_FRONTEND'), os.getenv('PRODUCTION_FRONTEND')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#################################################################
""" Initial Setup """

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#################################################################
""" Routers """
auth = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

items = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
)


#################################################################
""" API Endpoints """

# Auth API

# Items API

app.include_router(auth)
app.include_router(items)