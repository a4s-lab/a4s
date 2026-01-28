from fastapi import APIRouter

from app.routers.v1.agents import router as agents_router

router = APIRouter(prefix="/api/v1")
router.include_router(agents_router)

__all__ = ["router"]
