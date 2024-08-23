from fastapi import APIRouter

items = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
)