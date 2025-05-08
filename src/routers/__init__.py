from fastapi import APIRouter
from . import auth_router

router = APIRouter()

router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
