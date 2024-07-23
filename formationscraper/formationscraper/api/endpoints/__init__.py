from fastapi import APIRouter
from .main import router as formations_router

main_router = APIRouter()

main_router.include_router(formations_router, tags=["formations"])
