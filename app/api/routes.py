from fastapi import APIRouter
from app.routers import atividades

router = APIRouter()
router.include_router(atividades.router)  # fica /api/atividades
