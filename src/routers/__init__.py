from fastapi import APIRouter

from src.routers import house, users

router = APIRouter()

router.include_router(house.router)
router.include_router(users.router)
