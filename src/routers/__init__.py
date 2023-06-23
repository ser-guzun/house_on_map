from fastapi import APIRouter

from src.routers import house

router = APIRouter()

router.include_router(house.router)
