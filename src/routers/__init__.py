from fastapi import APIRouter

from src.routers import house, user

router = APIRouter()

router.include_router(house.router)
router.include_router(user.router)
