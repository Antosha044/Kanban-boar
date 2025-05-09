from fastapi import APIRouter
from . import auth_router, project_router

router = APIRouter()

router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
router.include_router(project_router.router, prefix="/projects", tags=["projects"]) 
